#!/usr/bin/env python3
"""
Chapter 17: AI-Powered Observability & AIOps
Grafana Alert Webhook Handler

Receives Grafana alerts, enriches them with AI analysis, and posts to Slack.
Provides context-aware explanations and troubleshooting steps.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install anthropic flask slack-sdk pyyaml

Usage:
    # Start webhook server
    python grafana_webhook.py \
        --port 5000 \
        --slack-channel #alerts

    # Configure in Grafana:
    # Contact Points → Add webhook
    # URL: http://your-server:5000/webhook/grafana
    # Method: POST

    # Test with sample alert
    curl -X POST http://localhost:5000/webhook/grafana \
      -H "Content-Type: application/json" \
      -d @sample-alert.json
"""

import anthropic
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import yaml


app = Flask(__name__)


class GrafanaAlertEnricher:
    """
    Enriches Grafana alerts with AI-powered analysis.

    Takes raw alert webhooks and adds:
    - Plain English explanations
    - Urgency assessment
    - Troubleshooting steps
    - Related runbook links
    """

    def __init__(
        self,
        anthropic_api_key: str,
        runbook_config: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        Initialize alert enricher.

        Args:
            anthropic_api_key: API key for Claude
            runbook_config: Path to YAML file with runbook mappings
            model: Claude model to use
        """
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.model = model
        self.runbooks = self._load_runbooks(runbook_config) if runbook_config else {}

    def enrich_alert(self, grafana_alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich a Grafana alert with AI analysis.

        Args:
            grafana_alert: Raw alert payload from Grafana webhook

        Returns:
            Dict with enriched alert information
        """
        # Extract alert details
        alert_info = self._parse_grafana_alert(grafana_alert)

        # Check for matching runbook
        runbook_url = self._find_runbook(alert_info['alert_name'], alert_info['labels'])

        # Get AI analysis
        ai_analysis = self._analyze_with_claude(alert_info, runbook_url)

        return {
            "original_alert": grafana_alert,
            "parsed": alert_info,
            "ai_enrichment": ai_analysis,
            "runbook": runbook_url,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _parse_grafana_alert(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Grafana webhook payload into structured data."""
        # Grafana alert format (v9+)
        return {
            "alert_name": alert.get('title', alert.get('ruleName', 'Unknown Alert')),
            "state": alert.get('state', 'unknown'),
            "message": alert.get('message', alert.get('annotations', {}).get('description', '')),
            "labels": alert.get('labels', {}),
            "annotations": alert.get('annotations', {}),
            "dashboard_url": alert.get('dashboardURL', ''),
            "panel_url": alert.get('panelURL', ''),
            "severity": alert.get('labels', {}).get('severity', 'warning'),
            "service": alert.get('labels', {}).get('service', 'unknown'),
            "fired_at": alert.get('startsAt', datetime.utcnow().isoformat())
        }

    def _analyze_with_claude(
        self,
        alert_info: Dict[str, Any],
        runbook_url: Optional[str]
    ) -> Dict[str, Any]:
        """Get AI analysis of the alert."""

        labels_str = "\n".join(f"  {k}: {v}" for k, v in alert_info['labels'].items())
        annotations_str = "\n".join(f"  {k}: {v}" for k, v in alert_info['annotations'].items())

        prompt = f"""You are analyzing a production alert from Grafana.

Alert: {alert_info['alert_name']}
Severity: {alert_info['severity']}
Service: {alert_info['service']}
State: {alert_info['state']}

Message:
{alert_info['message']}

Labels:
{labels_str}

Annotations:
{annotations_str}

{f"Runbook Available: {runbook_url}" if runbook_url else "No runbook configured for this alert."}

Provide:
1. **Plain English Explanation**: What does this alert mean? Assume the on-call engineer isn't familiar with this service.

2. **Urgency Assessment**: How urgent is this? Consider:
   - P1 (Critical): Production down, revenue impact, customer-facing
   - P2 (High): Degraded performance, imminent failure risk
   - P3 (Medium): Should investigate soon, no immediate impact
   - P4 (Low): Informational, monitor

3. **First Steps**: What should the on-call engineer do FIRST? Be specific (e.g., "Check pod logs with kubectl logs...", "Verify database connections...", "Review recent deploys...")

4. **Possible Causes**: Top 3 most likely root causes based on alert details.

5. **Quick Checks**: 3-5 commands or checks to diagnose the issue.

Output ONLY valid JSON:
{{
  "plain_english": "explanation for non-experts",
  "urgency": "P1/P2/P3/P4",
  "urgency_reasoning": "why this urgency level",
  "first_action": "specific first step to take",
  "likely_causes": ["cause 1", "cause 2", "cause 3"],
  "diagnostic_commands": ["command 1", "command 2", "command 3"],
  "escalation_needed": true/false,
  "escalation_reason": "when to escalate to senior engineer"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1536,
                messages=[{"role": "user", "content": prompt}]
            )

            return json.loads(response.content[0].text)

        except json.JSONDecodeError as e:
            return {
                "plain_english": f"Alert analysis failed: {e}",
                "urgency": "P2",
                "urgency_reasoning": "Unable to assess - manual review required",
                "first_action": "Review alert details manually",
                "likely_causes": ["AI analysis error"],
                "diagnostic_commands": [],
                "escalation_needed": True,
                "escalation_reason": "AI enrichment failed"
            }

    def _find_runbook(self, alert_name: str, labels: Dict[str, str]) -> Optional[str]:
        """Find matching runbook URL from config."""
        # Try exact alert name match
        if alert_name in self.runbooks:
            return self.runbooks[alert_name]

        # Try service match
        service = labels.get('service', labels.get('job', ''))
        if service and service in self.runbooks:
            return self.runbooks[service]

        return None

    def _load_runbooks(self, filepath: str) -> Dict[str, str]:
        """Load runbook configuration from YAML."""
        try:
            with open(filepath, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"⚠️  Failed to load runbooks: {e}")
            return {}


class SlackNotifier:
    """Send enriched alerts to Slack."""

    def __init__(self, slack_token: str, default_channel: str = "#alerts"):
        """
        Initialize Slack notifier.

        Args:
            slack_token: Slack bot token
            default_channel: Default channel for alerts
        """
        self.client = WebClient(token=slack_token)
        self.default_channel = default_channel

    def send_enriched_alert(
        self,
        enriched_alert: Dict[str, Any],
        channel: Optional[str] = None
    ):
        """
        Send enriched alert to Slack with formatted message.

        Args:
            enriched_alert: Output from GrafanaAlertEnricher
            channel: Slack channel (uses default if not specified)
        """
        alert = enriched_alert['parsed']
        ai = enriched_alert['ai_enrichment']
        runbook = enriched_alert.get('runbook')

        # Determine color based on urgency
        color_map = {
            'P1': 'danger',
            'P2': 'warning',
            'P3': '#439FE0',  # Blue
            'P4': 'good'
        }
        color = color_map.get(ai['urgency'], 'warning')

        # Build message
        title = f"{self._get_emoji(ai['urgency'])} {alert['alert_name']}"

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Urgency:* {ai['urgency']}"},
                    {"type": "mrkdwn", "text": f"*Service:* `{alert['service']}`"},
                    {"type": "mrkdwn", "text": f"*Severity:* {alert['severity']}"},
                    {"type": "mrkdwn", "text": f"*State:* {alert['state']}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*What's Happening:*\n{ai['plain_english']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*First Action:*\n:point_right: {ai['first_action']}"
                }
            }
        ]

        # Add likely causes
        causes_text = "\n".join(f"• {cause}" for cause in ai['likely_causes'])
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Likely Causes:*\n{causes_text}"
            }
        })

        # Add diagnostic commands
        if ai['diagnostic_commands']:
            commands_text = "\n".join(f"`{cmd}`" for cmd in ai['diagnostic_commands'])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Diagnostic Commands:*\n{commands_text}"
                }
            })

        # Add links
        links = []
        if alert['dashboard_url']:
            links.append(f"<{alert['dashboard_url']}|:chart_with_upwards_trend: Dashboard>")
        if runbook:
            links.append(f"<{runbook}|:book: Runbook>")

        if links:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": " | ".join(links)
                }
            })

        # Add escalation warning
        if ai['escalation_needed']:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":warning: *Escalation:* {ai['escalation_reason']}"
                }
            })

        # Send to Slack
        try:
            self.client.chat_postMessage(
                channel=channel or self.default_channel,
                text=title,  # Fallback text
                blocks=blocks
            )
        except SlackApiError as e:
            print(f"❌ Slack notification failed: {e.response['error']}")
            raise

    def _get_emoji(self, urgency: str) -> str:
        """Get emoji for urgency level."""
        emoji_map = {
            'P1': ':rotating_light:',
            'P2': ':warning:',
            'P3': ':large_blue_circle:',
            'P4': ':information_source:'
        }
        return emoji_map.get(urgency, ':bell:')


# Global instances (initialized in main)
enricher = None
notifier = None


@app.route('/webhook/grafana', methods=['POST'])
def webhook_grafana():
    """Handle Grafana alert webhook."""
    try:
        alert = request.json

        if not alert:
            return jsonify({"error": "No alert data"}), 400

        print(f"📨 Received alert: {alert.get('title', 'Unknown')}")

        # Enrich with AI
        enriched = enricher.enrich_alert(alert)

        # Send to Slack
        notifier.send_enriched_alert(enriched)

        print(f"✓ Sent enriched alert to Slack")

        return jsonify({
            "status": "success",
            "alert": enriched['parsed']['alert_name'],
            "urgency": enriched['ai_enrichment']['urgency']
        })

    except Exception as e:
        print(f"❌ Error processing alert: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "grafana-webhook-handler"})


def main():
    parser = argparse.ArgumentParser(description='Grafana alert webhook with AI enrichment')
    parser.add_argument('--port', type=int, default=5000, help='HTTP server port')
    parser.add_argument('--slack-channel', default='#alerts', help='Slack channel for alerts')
    parser.add_argument('--runbooks', help='YAML file with runbook mappings')

    args = parser.parse_args()

    # Get API keys
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    slack_token = os.getenv('SLACK_BOT_TOKEN')

    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)

    if not slack_token:
        print("❌ SLACK_BOT_TOKEN not set")
        sys.exit(1)

    # Initialize global instances
    global enricher, notifier

    enricher = GrafanaAlertEnricher(
        anthropic_api_key=anthropic_key,
        runbook_config=args.runbooks
    )

    notifier = SlackNotifier(
        slack_token=slack_token,
        default_channel=args.slack_channel
    )

    # Start server
    print(f"🚀 Starting Grafana webhook handler")
    print(f"   Port: {args.port}")
    print(f"   Webhook URL: http://localhost:{args.port}/webhook/grafana")
    print(f"   Slack channel: {args.slack_channel}")
    print(f"   Runbooks: {args.runbooks or 'Not configured'}")
    print(f"\nReady to receive alerts...")

    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
