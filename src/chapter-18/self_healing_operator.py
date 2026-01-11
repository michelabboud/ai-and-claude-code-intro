#!/usr/bin/env python3
"""
Self-Healing Kubernetes Operator with AI
Automatically detects and fixes unhealthy pods using AI-powered diagnosis.

Part of Chapter 18: Advanced AIOps

Requires:
  pip install kopf kubernetes anthropic
"""

import os
import json
import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime

import kopf
import kubernetes
from kubernetes import client, config
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SelfHealingOperator:
    """
    Kubernetes operator that monitors pods and automatically heals failures.

    Features:
    - Real-time pod health monitoring
    - AI-powered failure diagnosis
    - Automatic remediation with confidence thresholds
    - Escalation to humans for uncertain cases
    """

    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        # Load Kubernetes config
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()

        self.k8s_core = client.CoreV1Api()
        self.k8s_apps = client.AppsV1Api()

        # Confidence threshold for automatic healing
        self.confidence_threshold = 0.80

    async def analyze_pod_failure(self, pod: Dict) -> Dict:
        """
        Use AI to analyze why a pod is unhealthy and recommend a fix.

        Args:
            pod: Kubernetes pod object (dict)

        Returns:
            Dict with diagnosis and recommended fix
        """
        pod_name = pod['metadata']['name']
        namespace = pod['metadata']['namespace']

        logger.info(f"Analyzing pod failure: {namespace}/{pod_name}")

        # Gather pod context
        pod_status = pod.get('status', {})
        container_statuses = pod_status.get('containerStatuses', [])

        # Get pod events
        events = self._get_pod_events(pod_name, namespace)

        # Get pod logs (if available)
        logs = self._get_pod_logs(pod_name, namespace)

        # AI diagnosis
        diagnosis = await self._ai_diagnose_pod(pod_status, container_statuses, events, logs)

        logger.info(f"AI diagnosis for {pod_name}: {diagnosis.get('root_cause')}")
        return diagnosis

    def _get_pod_events(self, pod_name: str, namespace: str) -> List[Dict]:
        """Fetch Kubernetes events for a pod"""
        try:
            events = self.k8s_core.list_namespaced_event(
                namespace=namespace,
                field_selector=f"involvedObject.name={pod_name}"
            )

            return [
                {
                    'reason': event.reason,
                    'message': event.message,
                    'type': event.type,
                    'count': event.count,
                    'timestamp': event.last_timestamp.isoformat() if event.last_timestamp else None
                }
                for event in events.items
            ]
        except client.exceptions.ApiException as e:
            logger.error(f"Failed to fetch events for {pod_name}: {e}")
            return []

    def _get_pod_logs(self, pod_name: str, namespace: str, tail_lines: int = 100) -> str:
        """Fetch pod logs"""
        try:
            logs = self.k8s_core.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                tail_lines=tail_lines
            )
            return logs
        except client.exceptions.ApiException as e:
            logger.warning(f"Failed to fetch logs for {pod_name}: {e}")
            return "No logs available"

    async def _ai_diagnose_pod(self, pod_status: Dict, container_statuses: List[Dict],
                               events: List[Dict], logs: str) -> Dict:
        """Use Claude to diagnose pod failure"""

        prompt = f"""Diagnose why this Kubernetes pod is unhealthy and recommend a fix.

**Pod Status**:
Phase: {pod_status.get('phase')}
Conditions: {json.dumps(pod_status.get('conditions', []), indent=2)}

**Container Statuses**:
{json.dumps(container_statuses, indent=2)}

**Recent Events**:
{json.dumps(events, indent=2)}

**Recent Logs** (last 100 lines):
{logs[:2000]}  # Truncate to avoid token limits

Based on this data, provide diagnosis:

Available fixes:
- restart_pod: Delete pod, let controller recreate it
- increase_memory_limit: Pod is OOMKilled, needs more memory
- increase_cpu_limit: Pod is CPU throttled
- fix_image_pull_error: Image doesn't exist or auth issue
- rollback_deployment: Bad deployment causing crashes
- escalate_to_human: Uncertain or complex issue

Return JSON:
{{
  "root_cause": "One-sentence explanation of why pod failed",
  "fix": "restart_pod|increase_memory_limit|increase_cpu_limit|fix_image_pull_error|rollback_deployment|escalate_to_human",
  "confidence": 0.0-1.0,
  "reasoning": "Why this fix will work",
  "details": {{
    "failure_type": "CrashLoopBackOff|OOMKilled|ImagePullBackOff|Error|Unknown",
    "error_message": "Key error message from logs/events"
  }}
}}

Return ONLY valid JSON."""

        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        diagnosis = json.loads(response.content[0].text)
        return diagnosis

    async def apply_fix(self, pod: Dict, diagnosis: Dict) -> Dict:
        """
        Execute the AI-recommended fix.

        Args:
            pod: Kubernetes pod object
            diagnosis: AI diagnosis with recommended fix

        Returns:
            Dict with fix result
        """
        fix = diagnosis['fix']
        pod_name = pod['metadata']['name']
        namespace = pod['metadata']['namespace']

        logger.info(f"Applying fix '{fix}' to pod {pod_name}")

        try:
            if fix == 'restart_pod':
                return await self._restart_pod(pod_name, namespace)

            elif fix == 'increase_memory_limit':
                return await self._increase_memory_limit(pod, diagnosis)

            elif fix == 'increase_cpu_limit':
                return await self._increase_cpu_limit(pod, diagnosis)

            elif fix == 'fix_image_pull_error':
                return await self._fix_image_pull_error(pod, diagnosis)

            elif fix == 'rollback_deployment':
                return await self._rollback_deployment(pod)

            elif fix == 'escalate_to_human':
                return await self._escalate_to_human(pod, diagnosis)

            else:
                logger.error(f"Unknown fix: {fix}")
                return await self._escalate_to_human(pod, diagnosis)

        except Exception as e:
            logger.error(f"Fix failed for {pod_name}: {e}")
            return {
                'status': 'failed',
                'error': str(e)
            }

    async def _restart_pod(self, pod_name: str, namespace: str) -> Dict:
        """Restart pod by deleting it (controller will recreate)"""
        try:
            self.k8s_core.delete_namespaced_pod(
                name=pod_name,
                namespace=namespace
            )
            logger.info(f"Deleted pod {pod_name}, controller will recreate it")
            return {
                'status': 'success',
                'action': 'restart_pod',
                'pod': pod_name
            }
        except client.exceptions.ApiException as e:
            raise Exception(f"Failed to delete pod: {e}")

    async def _increase_memory_limit(self, pod: Dict, diagnosis: Dict) -> Dict:
        """Increase memory limit for OOMKilled pods"""
        deployment_name = pod['metadata']['labels'].get('app')
        namespace = pod['metadata']['namespace']

        if not deployment_name:
            raise Exception("Pod doesn't have 'app' label, can't find deployment")

        try:
            # Get deployment
            deployment = self.k8s_apps.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace
            )

            # Find container and current memory
            container = deployment.spec.template.spec.containers[0]
            current_memory_str = container.resources.limits.get('memory', '256Mi')
            current_memory_mb = int(current_memory_str.replace('Mi', ''))

            # Increase by 50%
            new_memory_mb = int(current_memory_mb * 1.5)
            container.resources.limits['memory'] = f"{new_memory_mb}Mi"

            # Apply patch
            self.k8s_apps.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )

            logger.info(f"Increased memory limit for {deployment_name}: {current_memory_mb}Mi → {new_memory_mb}Mi")

            return {
                'status': 'success',
                'action': 'increase_memory_limit',
                'deployment': deployment_name,
                'old_limit': f"{current_memory_mb}Mi",
                'new_limit': f"{new_memory_mb}Mi"
            }

        except client.exceptions.ApiException as e:
            raise Exception(f"Failed to update deployment: {e}")

    async def _increase_cpu_limit(self, pod: Dict, diagnosis: Dict) -> Dict:
        """Increase CPU limit for throttled pods"""
        deployment_name = pod['metadata']['labels'].get('app')
        namespace = pod['metadata']['namespace']

        if not deployment_name:
            raise Exception("Pod doesn't have 'app' label, can't find deployment")

        try:
            deployment = self.k8s_apps.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace
            )

            container = deployment.spec.template.spec.containers[0]
            current_cpu_str = container.resources.limits.get('cpu', '500m')
            current_cpu_millicores = int(current_cpu_str.replace('m', ''))

            # Increase by 50%
            new_cpu_millicores = int(current_cpu_millicores * 1.5)
            container.resources.limits['cpu'] = f"{new_cpu_millicores}m"

            self.k8s_apps.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )

            logger.info(f"Increased CPU limit for {deployment_name}: {current_cpu_millicores}m → {new_cpu_millicores}m")

            return {
                'status': 'success',
                'action': 'increase_cpu_limit',
                'deployment': deployment_name,
                'old_limit': f"{current_cpu_millicores}m",
                'new_limit': f"{new_cpu_millicores}m"
            }

        except client.exceptions.ApiException as e:
            raise Exception(f"Failed to update deployment: {e}")

    async def _fix_image_pull_error(self, pod: Dict, diagnosis: Dict) -> Dict:
        """
        Handle image pull errors.
        In production, this would check image exists, fix auth, etc.
        """
        logger.warning("ImagePullBackOff detected, escalating to human")
        return await self._escalate_to_human(pod, diagnosis)

    async def _rollback_deployment(self, pod: Dict) -> Dict:
        """Rollback deployment to previous version"""
        deployment_name = pod['metadata']['labels'].get('app')
        namespace = pod['metadata']['namespace']

        if not deployment_name:
            raise Exception("Pod doesn't have 'app' label, can't find deployment")

        try:
            self.k8s_apps.create_namespaced_deployment_rollback(
                name=deployment_name,
                namespace=namespace,
                body={'rollbackTo': {'revision': 0}}
            )

            logger.info(f"Rolled back deployment {deployment_name} to previous version")

            return {
                'status': 'success',
                'action': 'rollback_deployment',
                'deployment': deployment_name
            }

        except client.exceptions.ApiException as e:
            raise Exception(f"Failed to rollback deployment: {e}")

    async def _escalate_to_human(self, pod: Dict, diagnosis: Dict) -> Dict:
        """Escalate to on-call engineer"""
        pod_name = pod['metadata']['name']
        namespace = pod['metadata']['namespace']

        alert_message = f"""
🚨 **POD HEALTH ISSUE - MANUAL INTERVENTION REQUIRED** 🚨

**Pod**: {namespace}/{pod_name}
**Root Cause**: {diagnosis.get('root_cause', 'Unknown')}
**Failure Type**: {diagnosis.get('details', {}).get('failure_type', 'Unknown')}

**AI Confidence**: {diagnosis.get('confidence', 0)*100:.1f}%
**AI Reasoning**: {diagnosis.get('reasoning', 'N/A')}

Pod requires manual investigation.
"""

        logger.warning(alert_message)

        # In production: Send to Slack/PagerDuty
        # await slack.send_alert(alert_message)

        return {
            'status': 'escalated',
            'action': 'escalate_to_human',
            'pod': pod_name,
            'reason': diagnosis.get('root_cause')
        }


# Kopf operator handlers
operator = SelfHealingOperator()


@kopf.on.startup()
async def configure(settings: kopf.OperatorSettings, **_):
    """Configure operator settings"""
    settings.posting.enabled = False  # Disable kopf event posting
    logger.info("Self-healing operator starting up...")


@kopf.on.event('pods')
async def pod_event_handler(event, **kwargs):
    """
    Watch for pod events and auto-heal failures.

    This handler is called for every pod event (created, modified, deleted).
    """
    pod = event['object']
    pod_name = pod['metadata']['name']
    namespace = pod['metadata']['namespace']
    phase = pod.get('status', {}).get('phase', 'Unknown')

    # Skip healthy pods
    if phase == 'Running':
        # Check container statuses for restarts/failures
        container_statuses = pod.get('status', {}).get('containerStatuses', [])
        has_issues = any(
            not cs.get('ready') or cs.get('restartCount', 0) > 3
            for cs in container_statuses
        )

        if not has_issues:
            return  # Pod is healthy

    # Pod is unhealthy, analyze
    logger.info(f"Detected unhealthy pod: {namespace}/{pod_name} (phase: {phase})")

    try:
        # AI diagnoses the issue
        diagnosis = await operator.analyze_pod_failure(pod)

        # Check confidence threshold
        confidence = diagnosis.get('confidence', 0)

        if confidence > operator.confidence_threshold:
            # High confidence, apply fix automatically
            logger.info(f"High confidence ({confidence:.2f}), applying fix automatically")
            result = await operator.apply_fix(pod, diagnosis)
            logger.info(f"Fix applied to {pod_name}: {result.get('status')}")

        else:
            # Low confidence, escalate to human
            logger.warning(f"Low confidence ({confidence:.2f}), escalating to human")
            await operator._escalate_to_human(pod, diagnosis)

    except Exception as e:
        logger.error(f"Failed to handle pod failure {pod_name}: {e}")


@kopf.on.create('deployments')
async def deployment_created(spec, name, namespace, **kwargs):
    """Log when deployments are created"""
    logger.info(f"New deployment created: {namespace}/{name}")


if __name__ == '__main__':
    """
    Run the operator.

    Usage:
      python self_healing_operator.py

    The operator will watch for pod failures and automatically heal them.
    Press Ctrl+C to stop.
    """
    logger.info("Starting self-healing Kubernetes operator...")
    logger.info(f"Confidence threshold: {operator.confidence_threshold}")

    # Run operator (blocking call)
    kopf.run()
