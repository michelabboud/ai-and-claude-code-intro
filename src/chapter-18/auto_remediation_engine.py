#!/usr/bin/env python3
"""
Auto-Remediation Engine for Production Systems
Implements safe/unsafe classifications, approval workflows, circuit breakers, and rollback logic.

Part of Chapter 18: Advanced AIOps
"""

import asyncio
import os
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import json
import logging

import anthropic
from kubernetes import client, config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RemediationSafety(Enum):
    """Safety classification for remediation actions"""
    SAFE = "safe"                      # Fully automated, low risk
    REQUIRES_APPROVAL = "approval"      # Needs human approval
    FORBIDDEN = "forbidden"             # Never automate


@dataclass
class RemediationAction:
    """Represents a remediation action with metadata"""
    name: str
    safety: RemediationSafety
    description: str
    blast_radius: str
    typical_duration: str
    rollback_available: bool = True


@dataclass
class CircuitBreakerState:
    """Circuit breaker to prevent runaway automation"""
    failure_threshold: float = 0.30  # Open circuit at 30% failure rate
    window_size: int = 10            # Track last 10 attempts
    recent_results: List[bool] = field(default_factory=list)
    is_open: bool = False
    opened_at: Optional[datetime] = None
    reset_timeout_minutes: int = 15

    def record_result(self, success: bool):
        """Record a remediation attempt result"""
        self.recent_results.append(success)

        # Keep only last window_size results
        if len(self.recent_results) > self.window_size:
            self.recent_results.pop(0)

        # Check if should open circuit
        if len(self.recent_results) >= self.window_size:
            failure_rate = 1 - (sum(self.recent_results) / len(self.recent_results))

            if failure_rate > self.failure_threshold:
                self.open_circuit()
            elif self.is_open and self._should_reset():
                self.close_circuit()

    def open_circuit(self):
        """Open circuit breaker (stop automation)"""
        if not self.is_open:
            self.is_open = True
            self.opened_at = datetime.now()
            logger.error("Circuit breaker OPENED: Failure rate exceeded threshold")

    def close_circuit(self):
        """Close circuit breaker (resume automation)"""
        self.is_open = False
        self.opened_at = None
        self.recent_results = []
        logger.info("Circuit breaker CLOSED: Reset timeout expired, resuming automation")

    def _should_reset(self) -> bool:
        """Check if enough time has passed to reset circuit breaker"""
        if not self.is_open or not self.opened_at:
            return False

        elapsed = datetime.now() - self.opened_at
        return elapsed > timedelta(minutes=self.reset_timeout_minutes)

    def can_execute(self) -> bool:
        """Check if remediation is allowed"""
        if self.is_open and not self._should_reset():
            logger.warning("Circuit breaker is OPEN, blocking remediation")
            return False
        return True


class AutoRemediationEngine:
    """
    Production-ready auto-remediation engine with safety checks.

    Features:
    - Safe/unsafe action classification
    - Human approval workflow for risky actions
    - Circuit breaker to prevent runaway automation
    - Comprehensive audit logging
    - Rollback capability
    """

    # Action catalog with safety classifications
    ACTIONS = {
        'restart_pod': RemediationAction(
            name='restart_pod',
            safety=RemediationSafety.SAFE,
            description='Restart a stateless pod/container',
            blast_radius='single pod',
            typical_duration='5-30 seconds',
            rollback_available=False  # Pod restart is idempotent
        ),
        'clear_cache': RemediationAction(
            name='clear_cache',
            safety=RemediationSafety.SAFE,
            description='Clear application cache (Redis/Memcached)',
            blast_radius='single cache instance',
            typical_duration='1-5 seconds',
            rollback_available=False
        ),
        'scale_up_pods': RemediationAction(
            name='scale_up_pods',
            safety=RemediationSafety.SAFE,
            description='Increase pod replicas (within limits)',
            blast_radius='deployment',
            typical_duration='30-60 seconds',
            rollback_available=True
        ),
        'rollback_deployment': RemediationAction(
            name='rollback_deployment',
            safety=RemediationSafety.REQUIRES_APPROVAL,
            description='Rollback deployment to previous version',
            blast_radius='entire deployment',
            typical_duration='2-5 minutes',
            rollback_available=True
        ),
        'restart_database': RemediationAction(
            name='restart_database',
            safety=RemediationSafety.REQUIRES_APPROVAL,
            description='Restart database instance',
            blast_radius='database cluster',
            typical_duration='5-15 minutes',
            rollback_available=False
        ),
        'delete_database': RemediationAction(
            name='delete_database',
            safety=RemediationSafety.FORBIDDEN,
            description='Delete production database',
            blast_radius='entire system',
            typical_duration='immediate',
            rollback_available=False
        ),
        'revoke_ssl_certificate': RemediationAction(
            name='revoke_ssl_certificate',
            safety=RemediationSafety.FORBIDDEN,
            description='Revoke SSL/TLS certificate',
            blast_radius='entire system',
            typical_duration='immediate',
            rollback_available=False
        )
    }

    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.circuit_breaker = CircuitBreakerState()
        self.audit_log: List[Dict] = []

        # Load Kubernetes config
        try:
            config.load_incluster_config()  # Running in K8s
        except:
            config.load_kube_config()  # Running locally

        self.k8s_core = client.CoreV1Api()
        self.k8s_apps = client.AppsV1Api()

    async def handle_alert(self, alert: Dict) -> Dict:
        """
        Main entry point for handling alerts.

        Args:
            alert: Prometheus/monitoring alert dict

        Returns:
            Dict with remediation results
        """
        incident_id = f"INC-{int(time.time())}"
        logger.info(f"{incident_id}: Received alert: {alert.get('alertname', 'unknown')}")

        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            return {
                'incident_id': incident_id,
                'status': 'blocked',
                'reason': 'circuit_breaker_open',
                'message': 'Auto-remediation blocked: too many recent failures'
            }

        # Step 1: AI diagnoses the issue
        try:
            diagnosis = await self._ai_diagnose(alert)
            logger.info(f"{incident_id}: AI diagnosis complete", extra={'diagnosis': diagnosis})
        except Exception as e:
            logger.error(f"{incident_id}: AI diagnosis failed: {e}")
            return {
                'incident_id': incident_id,
                'status': 'failed',
                'reason': 'diagnosis_error',
                'error': str(e)
            }

        # Step 2: Validate recommended action
        recommended_action = diagnosis.get('recommended_action')
        if recommended_action not in self.ACTIONS:
            logger.warning(f"{incident_id}: Unknown action: {recommended_action}, escalating")
            await self._escalate_to_human(incident_id, diagnosis, "Unknown action")
            return {
                'incident_id': incident_id,
                'status': 'escalated',
                'reason': 'unknown_action'
            }

        action = self.ACTIONS[recommended_action]

        # Step 3: Check action safety
        if action.safety == RemediationSafety.FORBIDDEN:
            logger.error(f"{incident_id}: FORBIDDEN action {action.name} requested, blocking!")
            await self._escalate_to_human(incident_id, diagnosis, "Forbidden action attempted")
            return {
                'incident_id': incident_id,
                'status': 'blocked',
                'reason': 'forbidden_action',
                'action': action.name
            }

        # Step 4: Execute or request approval
        if action.safety == RemediationSafety.SAFE:
            # Execute immediately
            result = await self._execute_remediation(incident_id, action, diagnosis)
        elif action.safety == RemediationSafety.REQUIRES_APPROVAL:
            # Request human approval
            approved = await self._request_approval(incident_id, action, diagnosis)
            if approved:
                result = await self._execute_remediation(incident_id, action, diagnosis)
            else:
                result = {
                    'incident_id': incident_id,
                    'status': 'approval_denied',
                    'action': action.name
                }

        # Record result in circuit breaker
        success = result.get('status') == 'success'
        self.circuit_breaker.record_result(success)

        # Audit log
        self._log_audit(incident_id, alert, diagnosis, action, result)

        return result

    async def _ai_diagnose(self, alert: Dict) -> Dict:
        """Use AI to diagnose the incident and recommend remediation"""

        # Gather context (would fetch from real monitoring system)
        metrics = self._fetch_recent_metrics(alert)
        logs = self._fetch_recent_logs(alert)

        prompt = f"""Diagnose this production incident and recommend remediation.

**Alert**: {alert.get('alertname', 'Unknown')}
**Description**: {alert.get('description', 'No description')}
**Severity**: {alert.get('severity', 'unknown')}

**Recent Metrics** (last 10 minutes):
{json.dumps(metrics, indent=2)}

**Recent Error Logs** (last 5 minutes):
{json.dumps(logs[:20], indent=2)}

Available remediation actions:
- restart_pod: Restart failing pods (SAFE, automated)
- clear_cache: Clear application cache (SAFE, automated)
- scale_up_pods: Increase pod replicas (SAFE, automated)
- rollback_deployment: Rollback to previous version (REQUIRES APPROVAL)
- restart_database: Restart database (REQUIRES APPROVAL)

Provide diagnosis in JSON format:
{{
  "issue_type": "db_connection_pool_exhausted|memory_leak|high_cpu|disk_full|other",
  "root_cause": "One-sentence explanation",
  "severity": "critical|high|medium|low",
  "recommended_action": "restart_pod|clear_cache|scale_up_pods|rollback_deployment|restart_database",
  "confidence": 0.0-1.0,
  "reasoning": "Why this action will fix the issue"
}}

Return ONLY valid JSON, no explanation."""

        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        diagnosis = json.loads(response.content[0].text)
        return diagnosis

    def _fetch_recent_metrics(self, alert: Dict) -> Dict:
        """
        Fetch recent metrics from Prometheus/monitoring system.
        In production, this would query Prometheus API.
        """
        # Mock data for demonstration
        return {
            'cpu_percent': 87.5,
            'memory_percent': 92.1,
            'disk_percent': 45.2,
            'db_connections_active': 98,
            'db_connections_max': 100,
            'http_request_rate': 1250,
            'error_rate_5xx': 12.3
        }

    def _fetch_recent_logs(self, alert: Dict) -> List[str]:
        """
        Fetch recent error logs.
        In production, this would query Elasticsearch/log aggregator.
        """
        # Mock data for demonstration
        return [
            "ERROR: Database connection timeout after 5000ms",
            "ERROR: Connection pool exhausted, rejecting new connections",
            "WARN: Memory usage at 92%, approaching limit",
            "ERROR: Failed to acquire database connection from pool"
        ]

    async def _request_approval(self, incident_id: str, action: RemediationAction,
                                diagnosis: Dict) -> bool:
        """
        Request human approval for risky actions.
        In production, this would integrate with Slack/PagerDuty.
        """
        logger.info(f"{incident_id}: Requesting approval for {action.name}")

        # Generate AI recommendation
        recommendation = self._format_approval_request(incident_id, action, diagnosis)

        logger.info(f"Approval request:\n{recommendation}")

        # In production: Send to Slack with approve/reject buttons
        # For demo: Auto-approve after timeout (would be human decision)

        # Simulate waiting for approval (5 minute timeout)
        timeout_seconds = 300

        # For demo purposes, we'll just log and return False (no auto-approval)
        logger.warning(f"{incident_id}: Approval request sent, awaiting human decision (timeout: {timeout_seconds}s)")

        # In real system:
        # approved = await self._wait_for_slack_approval(incident_id, timeout_seconds)
        # return approved

        return False  # Default to safe (no auto-approval in demo)

    def _format_approval_request(self, incident_id: str, action: RemediationAction,
                                 diagnosis: Dict) -> str:
        """Format approval request message"""
        return f"""
🚨 **AUTO-REMEDIATION APPROVAL REQUIRED** 🚨

**Incident ID**: {incident_id}
**Issue**: {diagnosis.get('root_cause', 'Unknown')}
**Severity**: {diagnosis.get('severity', 'unknown').upper()}

**Recommended Action**: `{action.name}`
**Description**: {action.description}
**Blast Radius**: {action.blast_radius}
**Estimated Duration**: {action.typical_duration}
**Rollback Available**: {'Yes' if action.rollback_available else 'No'}

**AI Confidence**: {diagnosis.get('confidence', 0)*100:.1f}%
**AI Reasoning**: {diagnosis.get('reasoning', 'N/A')}

**Approve this remediation?**
[Approve] [Reject] [View Details]
"""

    async def _execute_remediation(self, incident_id: str, action: RemediationAction,
                                   diagnosis: Dict) -> Dict:
        """Execute the remediation action"""
        logger.info(f"{incident_id}: Executing remediation: {action.name}")

        try:
            # Execute based on action type
            if action.name == 'restart_pod':
                result = await self._restart_pod(diagnosis)
            elif action.name == 'clear_cache':
                result = await self._clear_cache(diagnosis)
            elif action.name == 'scale_up_pods':
                result = await self._scale_up_pods(diagnosis)
            elif action.name == 'rollback_deployment':
                result = await self._rollback_deployment(diagnosis)
            else:
                raise ValueError(f"Unknown action: {action.name}")

            logger.info(f"{incident_id}: Remediation successful")
            return {
                'incident_id': incident_id,
                'status': 'success',
                'action': action.name,
                'result': result
            }

        except Exception as e:
            logger.error(f"{incident_id}: Remediation failed: {e}")
            await self._escalate_to_human(incident_id, diagnosis, f"Remediation failed: {e}")
            return {
                'incident_id': incident_id,
                'status': 'failed',
                'action': action.name,
                'error': str(e)
            }

    async def _restart_pod(self, diagnosis: Dict) -> Dict:
        """Restart a Kubernetes pod"""
        # In production: Get pod name from diagnosis/alert
        pod_name = "example-pod"
        namespace = "production"

        try:
            self.k8s_core.delete_namespaced_pod(
                name=pod_name,
                namespace=namespace
            )
            logger.info(f"Deleted pod {pod_name}, K8s will recreate it")
            return {'pod': pod_name, 'namespace': namespace}
        except client.exceptions.ApiException as e:
            raise Exception(f"Failed to restart pod: {e}")

    async def _clear_cache(self, diagnosis: Dict) -> Dict:
        """Clear Redis/Memcached cache"""
        # In production: Connect to Redis and FLUSHDB
        logger.info("Cache cleared (mock)")
        return {'cache_type': 'redis', 'keys_deleted': 'all'}

    async def _scale_up_pods(self, diagnosis: Dict) -> Dict:
        """Scale up pod replicas"""
        deployment_name = "example-deployment"
        namespace = "production"
        max_replicas = 10  # Safety limit

        try:
            # Get current replicas
            deployment = self.k8s_apps.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace
            )
            current_replicas = deployment.spec.replicas
            new_replicas = min(current_replicas + 2, max_replicas)  # Add 2, cap at max

            # Scale up
            deployment.spec.replicas = new_replicas
            self.k8s_apps.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )

            logger.info(f"Scaled {deployment_name} from {current_replicas} to {new_replicas} replicas")
            return {
                'deployment': deployment_name,
                'old_replicas': current_replicas,
                'new_replicas': new_replicas
            }
        except client.exceptions.ApiException as e:
            raise Exception(f"Failed to scale deployment: {e}")

    async def _rollback_deployment(self, diagnosis: Dict) -> Dict:
        """Rollback deployment to previous version"""
        deployment_name = "example-deployment"
        namespace = "production"

        try:
            # Rollback to previous revision
            self.k8s_apps.create_namespaced_deployment_rollback(
                name=deployment_name,
                namespace=namespace,
                body={'rollbackTo': {'revision': 0}}  # 0 = previous revision
            )

            logger.info(f"Rolled back deployment {deployment_name}")
            return {'deployment': deployment_name, 'action': 'rollback'}
        except client.exceptions.ApiException as e:
            raise Exception(f"Failed to rollback deployment: {e}")

    async def _escalate_to_human(self, incident_id: str, diagnosis: Dict, reason: str):
        """Escalate incident to on-call engineer"""
        logger.warning(f"{incident_id}: Escalating to human: {reason}")

        # In production: Send to PagerDuty/Slack
        alert_message = f"""
🚨 **AUTO-REMEDIATION ESCALATION** 🚨

**Incident ID**: {incident_id}
**Reason**: {reason}
**Issue**: {diagnosis.get('root_cause', 'Unknown')}
**Severity**: {diagnosis.get('severity', 'unknown').upper()}

Manual intervention required.
"""
        logger.info(alert_message)

    def _log_audit(self, incident_id: str, alert: Dict, diagnosis: Dict,
                   action: RemediationAction, result: Dict):
        """Log remediation attempt for audit/compliance"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'incident_id': incident_id,
            'alert': alert.get('alertname'),
            'severity': alert.get('severity'),
            'ai_model': 'claude-3-5-sonnet-20241022',
            'diagnosis': diagnosis,
            'action_name': action.name,
            'action_safety': action.safety.value,
            'result_status': result.get('status'),
            'circuit_breaker_state': {
                'is_open': self.circuit_breaker.is_open,
                'recent_success_rate': sum(self.circuit_breaker.recent_results) / max(len(self.circuit_breaker.recent_results), 1)
            }
        }

        self.audit_log.append(audit_entry)
        logger.info(f"Audit log entry created for {incident_id}")

        # In production: Store in database/S3 for compliance
        # with open(f'/var/log/auto-remediation/{incident_id}.json', 'w') as f:
        #     json.dump(audit_entry, f, indent=2)


async def main():
    """Example usage"""
    engine = AutoRemediationEngine()

    # Example alert from Prometheus
    alert = {
        'alertname': 'HighDatabaseConnections',
        'severity': 'critical',
        'description': 'Database connection pool at 98% capacity',
        'labels': {
            'service': 'api-server',
            'namespace': 'production'
        }
    }

    # Handle alert
    result = await engine.handle_alert(alert)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
