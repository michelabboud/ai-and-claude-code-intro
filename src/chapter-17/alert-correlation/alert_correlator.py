#!/usr/bin/env python3
"""
Chapter 17: AI-Powered Observability & AIOps
Intelligent Alert Correlation

Groups related alerts and identifies root causes using AI.
Reduces alert fatigue by correlating cascading failures.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install anthropic pyyaml slack-sdk

Usage:
    # Analyze alerts from JSON file
    python alert_correlator.py \
        --alerts alerts.json \
        --topology service-map.yaml

    # Process alerts from stdin (for webhook integration)
    cat grafana-alerts.json | python alert_correlator.py --stdin

    # Run as webhook server
    python alert_correlator.py \
        --webhook \
        --port 5000 \
        --topology service-map.yaml \
        --slack-channel #incidents
"""

import anthropic
import argparse
import json
import os
import sys
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
from flask import Flask, request, jsonify
from slack_sdk import WebClient


@dataclass
class Alert:
    """Single alert instance."""
    id: str
    timestamp: str
    service: str
    severity: str  # critical, high, medium, low
    message: str
    labels: Dict[str, str]
    annotations: Dict[str, str]


@dataclass
class CorrelationResult:
    """Result of alert correlation analysis."""
    timestamp: str
    total_alerts: int
    root_cause_alert: Alert
    symptom_alerts: List[Alert]
    confidence: float  # 0.0-1.0
    explanation: str
    incident_summary: str
    recommended_actions: List[str]
    affected_services: List[str]
    estimated_impact: str


class AIAlertCorrelator:
    """
    Use Claude AI to intelligently correlate alerts.

    Analyzes multiple concurrent alerts to identify root causes
    and separate them from cascading symptom alerts.
    """

    def __init__(
        self,
        anthropic_api_key: str,
        service_topology: Optional[Dict[str, Any]] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        Initialize alert correlator.

        Args:
            anthropic_api_key: API key for Claude
            service_topology: Service dependency graph
            model: Claude model to use
        """
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.model = model
        self.topology = service_topology or {}

    def correlate_alerts(
        self,
        alerts: List[Alert],
        time_window_minutes: int = 5
    ) -> CorrelationResult:
        """
        Analyze alerts and identify root cause.

        Args:
            alerts: List of Alert objects
            time_window_minutes: Consider alerts within this window as related

        Returns:
            CorrelationResult with root cause analysis
        """
        if not alerts:
            raise ValueError("No alerts to correlate")

        # Filter alerts within time window
        recent_alerts = self._filter_recent_alerts(alerts, time_window_minutes)

        if not recent_alerts:
            raise ValueError(f"No alerts within last {time_window_minutes} minutes")

        # Group alerts by service
        by_service = self._group_by_service(recent_alerts)

        # Prepare alert summary for AI
        alert_summary = self._format_alert_summary(recent_alerts)

        # Get service dependency context
        topology_context = self._format_topology_context(recent_alerts)

        # Ask Claude to analyze
        prompt = f"""You are analyzing a production incident with multiple concurrent alerts.

{len(recent_alerts)} alerts fired in the last {time_window_minutes} minutes:

{alert_summary}

Service Topology and Dependencies:
{topology_context}

Alerts by Service:
{self._format_service_breakdown(by_service)}

Your task:
1. Identify the ROOT CAUSE alert (the original failure that triggered everything else)
2. Identify SYMPTOM alerts (cascading failures caused by the root cause)
3. Explain the failure propagation path
4. Assess confidence in your analysis (0-100%)
5. Provide specific troubleshooting steps for the on-call engineer

Consider:
- Service dependencies (upstream failures cause downstream symptoms)
- Timing (which alert fired first?)
- Severity levels
- Alert patterns (e.g., database down → API errors → frontend timeouts)

Output ONLY valid JSON:
{{
  "root_cause_alert_id": "id of the root cause alert",
  "symptom_alert_ids": ["list", "of", "symptom", "alert", "ids"],
  "confidence": 0.0-1.0,
  "explanation": "detailed explanation of why this is the root cause and how failures propagated",
  "incident_summary": "one-line summary for incident report",
  "recommended_actions": ["step 1", "step 2", "step 3"],
  "estimated_impact": "brief description of customer/business impact"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            analysis = json.loads(response.content[0].text)

            # Find root cause and symptom alerts
            root_cause = next(a for a in recent_alerts if a.id == analysis['root_cause_alert_id'])
            symptoms = [a for a in recent_alerts if a.id in analysis['symptom_alert_ids']]

            # Identify affected services
            affected_services = list(set(a.service for a in recent_alerts))

            return CorrelationResult(
                timestamp=datetime.utcnow().isoformat(),
                total_alerts=len(recent_alerts),
                root_cause_alert=root_cause,
                symptom_alerts=symptoms,
                confidence=analysis['confidence'],
                explanation=analysis['explanation'],
                incident_summary=analysis['incident_summary'],
                recommended_actions=analysis['recommended_actions'],
                affected_services=affected_services,
                estimated_impact=analysis['estimated_impact']
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response: {e}")
        except StopIteration:
            raise ValueError("AI identified non-existent alert ID")
        except Exception as e:
            raise RuntimeError(f"Correlation failed: {e}")

    def _filter_recent_alerts(self, alerts: List[Alert], minutes: int) -> List[Alert]:
        """Filter alerts within time window."""
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        recent = []

        for alert in alerts:
            try:
                alert_time = datetime.fromisoformat(alert.timestamp.replace('Z', '+00:00'))
                if alert_time >= cutoff:
                    recent.append(alert)
            except ValueError:
                # If timestamp parsing fails, include the alert
                recent.append(alert)

        return recent

    def _group_by_service(self, alerts: List[Alert]) -> Dict[str, List[Alert]]:
        """Group alerts by service name."""
        by_service = defaultdict(list)
        for alert in alerts:
            by_service[alert.service].append(alert)
        return dict(by_service)

    def _format_alert_summary(self, alerts: List[Alert]) -> str:
        """Format alerts for AI prompt."""
        lines = []
        for i, alert in enumerate(alerts, 1):
            lines.append(
                f"{i}. [{alert.timestamp}] {alert.severity.upper()} - "
                f"{alert.service} (ID: {alert.id})\n"
                f"   Message: {alert.message}"
            )
        return "\n\n".join(lines)

    def _format_topology_context(self, alerts: List[Alert]) -> str:
        """Format service topology for relevant services."""
        if not self.topology:
            return "No topology information available."

        relevant_services = set(a.service for a in alerts)
        lines = []

        for service in relevant_services:
            if service in self.topology:
                deps = self.topology[service].get('depends_on', [])
                lines.append(f"  {service} depends on: {', '.join(deps) if deps else 'none'}")

        return "\n".join(lines) if lines else "No topology information for these services."

    def _format_service_breakdown(self, by_service: Dict[str, List[Alert]]) -> str:
        """Format alerts grouped by service."""
        lines = []
        for service, service_alerts in by_service.items():
            lines.append(f"  {service}: {len(service_alerts)} alert(s)")
            for alert in service_alerts:
                lines.append(f"    - {alert.severity}: {alert.message[:80]}")
        return "\n".join(lines)


def load_alerts_from_file(filepath: str) -> List[Alert]:
    """Load alerts from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    alerts = []
    for item in data if isinstance(data, list) else [data]:
        alerts.append(Alert(
            id=item.get('id', str(hash(item.get('message', '')))),
            timestamp=item.get('timestamp', datetime.utcnow().isoformat()),
            service=item.get('service', 'unknown'),
            severity=item.get('severity', 'medium'),
            message=item.get('message', ''),
            labels=item.get('labels', {}),
            annotations=item.get('annotations', {})
        ))

    return alerts


def load_topology(filepath: str) -> Dict[str, Any]:
    """Load service topology from YAML file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def send_correlation_to_slack(
    slack_client: WebClient,
    result: CorrelationResult,
    channel: str = "#incidents"
):
    """Send correlation results to Slack."""
    color = "danger" if result.root_cause_alert.severity in ["critical", "high"] else "warning"

    message = f"""*🚨 Incident Detected: {result.incident_summary}*

*Root Cause:*
`{result.root_cause_alert.service}`: {result.root_cause_alert.message}

*Symptom Alerts:* {len(result.symptom_alerts)} cascading failure(s)
{chr(10).join(f"• `{a.service}`: {a.message[:60]}..." for a in result.symptom_alerts[:3])}

*Affected Services:* {', '.join(result.affected_services)}
*Estimated Impact:* {result.estimated_impact}

*Recommended Actions:*
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(result.recommended_actions))}

*AI Analysis (confidence: {result.confidence:.0%}):*
{result.explanation[:500]}...

_Correlated {result.total_alerts} alerts_
"""

    try:
        slack_client.chat_postMessage(
            channel=channel,
            text=result.incident_summary,
            attachments=[{
                "color": color,
                "text": message,
                "footer": "AI Alert Correlation System",
                "ts": int(datetime.utcnow().timestamp())
            }]
        )
    except Exception as e:
        print(f"❌ Slack notification failed: {e}")


# Flask webhook server
app = Flask(__name__)
correlator = None
slack_client = None
slack_channel = "#incidents"


@app.route('/webhook/alerts', methods=['POST'])
def webhook_alerts():
    """Receive alerts from Grafana/Prometheus webhook."""
    try:
        data = request.json

        # Convert webhook payload to Alert objects
        # (This format varies by monitoring system - adjust as needed)
        alerts = []
        for alert_data in data.get('alerts', []):
            alerts.append(Alert(
                id=alert_data.get('fingerprint', str(hash(alert_data.get('summary', '')))),
                timestamp=alert_data.get('startsAt', datetime.utcnow().isoformat()),
                service=alert_data.get('labels', {}).get('service', 'unknown'),
                severity=alert_data.get('labels', {}).get('severity', 'medium'),
                message=alert_data.get('annotations', {}).get('summary', ''),
                labels=alert_data.get('labels', {}),
                annotations=alert_data.get('annotations', {})
            ))

        if not alerts:
            return jsonify({"error": "No alerts in payload"}), 400

        # Correlate alerts
        result = correlator.correlate_alerts(alerts)

        # Send to Slack
        if slack_client:
            send_correlation_to_slack(slack_client, result, channel=slack_channel)

        return jsonify({
            "status": "success",
            "incident_summary": result.incident_summary,
            "root_cause": result.root_cause_alert.service,
            "total_alerts": result.total_alerts,
            "confidence": result.confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    parser = argparse.ArgumentParser(description='AI-powered alert correlation')
    parser.add_argument('--alerts', help='JSON file with alerts')
    parser.add_argument('--topology', help='YAML file with service topology')
    parser.add_argument('--stdin', action='store_true', help='Read alerts from stdin')
    parser.add_argument('--webhook', action='store_true', help='Run as webhook server')
    parser.add_argument('--port', type=int, default=5000, help='Webhook server port')
    parser.add_argument('--slack-channel', default='#incidents', help='Slack channel')
    parser.add_argument('--time-window', type=int, default=5, help='Alert time window (minutes)')
    parser.add_argument('--output', help='Output file (JSON)')

    args = parser.parse_args()

    # Get API keys
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    slack_token = os.getenv('SLACK_BOT_TOKEN')

    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)

    # Load topology
    topology = load_topology(args.topology) if args.topology else None

    if args.webhook:
        # Run as webhook server
        global correlator, slack_client, slack_channel

        correlator = AIAlertCorrelator(
            anthropic_api_key=anthropic_key,
            service_topology=topology
        )

        if slack_token:
            slack_client = WebClient(token=slack_token)
            slack_channel = args.slack_channel

        print(f"🚀 Starting webhook server on port {args.port}")
        print(f"   Endpoint: http://localhost:{args.port}/webhook/alerts")
        print(f"   Slack channel: {args.slack_channel if slack_token else 'disabled'}")
        app.run(host='0.0.0.0', port=args.port)

    else:
        # Single correlation analysis
        if args.stdin:
            data = json.load(sys.stdin)
            alerts = [Alert(**a) for a in (data if isinstance(data, list) else [data])]
        elif args.alerts:
            alerts = load_alerts_from_file(args.alerts)
        else:
            print("❌ Provide --alerts FILE or --stdin")
            sys.exit(1)

        correlator = AIAlertCorrelator(
            anthropic_api_key=anthropic_key,
            service_topology=topology
        )

        result = correlator.correlate_alerts(alerts, time_window_minutes=args.time_window)

        # Display results
        print(f"{'='*70}")
        print("Alert Correlation Results")
        print(f"{'='*70}")
        print(f"Analyzed: {result.total_alerts} alerts")
        print(f"Confidence: {result.confidence:.0%}")
        print(f"\n*ROOT CAUSE:*")
        print(f"  Service: {result.root_cause_alert.service}")
        print(f"  Message: {result.root_cause_alert.message}")
        print(f"  Severity: {result.root_cause_alert.severity}")
        print(f"\n*SYMPTOMS:* {len(result.symptom_alerts)} cascading failures")
        for alert in result.symptom_alerts:
            print(f"  • {alert.service}: {alert.message[:70]}")
        print(f"\n*INCIDENT SUMMARY:*")
        print(f"  {result.incident_summary}")
        print(f"\n*ESTIMATED IMPACT:*")
        print(f"  {result.estimated_impact}")
        print(f"\n*RECOMMENDED ACTIONS:*")
        for i, action in enumerate(result.recommended_actions, 1):
            print(f"  {i}. {action}")
        print(f"\n*AI EXPLANATION:*")
        print(f"  {result.explanation}")
        print(f"{'='*70}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(asdict(result), f, indent=2, default=str)
            print(f"\n✓ Saved to: {args.output}")

        if slack_token:
            slack = WebClient(token=slack_token)
            send_correlation_to_slack(slack, result, channel=args.slack_channel)
            print(f"✓ Sent to Slack: {args.slack_channel}")


if __name__ == '__main__':
    main()
