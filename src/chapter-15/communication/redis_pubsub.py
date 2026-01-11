#!/usr/bin/env python3
"""
Chapter 15: Multi-Agent Orchestration - Fundamentals
Redis Pub/Sub Communication Protocol

Demonstrates how agents communicate via Redis pub/sub channels.
Agents publish findings and subscribe to messages from other agents.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install redis

Usage:
    # Terminal 1: Start security agent
    python redis_pubsub.py --agent security

    # Terminal 2: Start performance agent
    python redis_pubsub.py --agent performance

    # Terminal 3: Coordinator
    python redis_pubsub.py --agent coordinator
"""

import redis
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Callable


class AgentCommunicator:
    """
    Redis pub/sub based agent communication.
    Agents publish findings to shared channel and subscribe to others' messages.
    """

    def __init__(self, agent_id: str, redis_host='localhost', redis_port=6379):
        """
        Initialize agent communicator.

        Args:
            agent_id: Unique identifier for this agent
            redis_host: Redis server hostname
            redis_port: Redis server port
        """
        self.agent_id = agent_id
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
        self.findings = []

        print(f"[{self.agent_id}] Connected to Redis at {redis_host}:{redis_port}")

    def publish_finding(self, finding: Dict):
        """
        Publish a finding to all listening agents.

        Args:
            finding: Dictionary containing finding details
        """
        message = {
            'agent_id': self.agent_id,
            'timestamp': datetime.utcnow().isoformat(),
            'finding': finding
        }

        self.redis_client.publish('agent_findings', json.dumps(message))
        print(f"[{self.agent_id}] Published finding: {finding['type']}")

    def subscribe_to_findings(self, callback: Callable):
        """
        Subscribe to findings from other agents.

        Args:
            callback: Function to call when receiving a message
        """
        self.pubsub.subscribe('agent_findings')
        print(f"[{self.agent_id}] Subscribed to agent_findings channel")

        for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])

                    # Ignore own messages
                    if data['agent_id'] != self.agent_id:
                        callback(data)
                except json.JSONDecodeError:
                    print(f"[{self.agent_id}] Failed to decode message")

    def store_finding(self, data: Dict):
        """Store received finding for later analysis."""
        self.findings.append(data)
        print(f"[{self.agent_id}] Received from {data['agent_id']}: "
              f"{data['finding']['type']}")


# Example: Security Agent
def run_security_agent():
    """Security agent that analyzes code for vulnerabilities."""
    agent = AgentCommunicator('security-agent-001')

    # Subscribe to findings in the background
    import threading

    def listen():
        agent.subscribe_to_findings(agent.store_finding)

    listener_thread = threading.Thread(target=listen, daemon=True)
    listener_thread.start()

    # Simulate security analysis
    time.sleep(2)
    agent.publish_finding({
        'type': 'security_vulnerability',
        'severity': 'high',
        'description': 'SQL injection found in /api/users endpoint',
        'file': 'src/api/users.js',
        'line': 45,
        'recommendation': 'Use parameterized queries'
    })

    # Wait for other agents
    print(f"[{agent.agent_id}] Waiting for other agents' findings...")
    time.sleep(5)

    # Display all findings
    print(f"\n[{agent.agent_id}] Received {len(agent.findings)} findings from other agents:")
    for finding in agent.findings:
        print(f"  - {finding['agent_id']}: {finding['finding']['type']}")


# Example: Performance Agent
def run_performance_agent():
    """Performance agent that analyzes code for bottlenecks."""
    agent = AgentCommunicator('performance-agent-001')

    # Subscribe to findings
    import threading

    def listen():
        agent.subscribe_to_findings(agent.store_finding)

    listener_thread = threading.Thread(target=listen, daemon=True)
    listener_thread.start()

    # Simulate performance analysis
    time.sleep(3)
    agent.publish_finding({
        'type': 'performance_bottleneck',
        'severity': 'critical',
        'description': 'N+1 query problem in getUserOrders()',
        'file': 'src/api/orders.js',
        'line': 123,
        'current_time': '2.5s average',
        'potential_improvement': '250ms with JOIN',
        'recommendation': 'Use eager loading with JOIN'
    })

    # Wait for other agents
    print(f"[{agent.agent_id}] Waiting for other agents' findings...")
    time.sleep(5)

    print(f"\n[{agent.agent_id}] Received {len(agent.findings)} findings:")
    for finding in agent.findings:
        print(f"  - {finding['agent_id']}: {finding['finding']['type']}")


# Example: Coordinator Agent
def run_coordinator_agent():
    """Coordinator agent that aggregates findings from all specialist agents."""
    agent = AgentCommunicator('coordinator-001')

    # Subscribe to all findings
    def handle_finding(data):
        agent.store_finding(data)

        # Coordinator takes action based on severity
        severity = data['finding'].get('severity', 'unknown')
        if severity in ['critical', 'high']:
            print(f"[{agent.agent_id}] ⚠️  HIGH PRIORITY: "
                  f"{data['agent_id']} found {severity} issue")

    print(f"[{agent.agent_id}] Coordinator waiting for agent findings...")
    print(f"[{agent.agent_id}] Will aggregate for 10 seconds...\n")

    import threading

    def listen():
        agent.subscribe_to_findings(handle_finding)

    listener_thread = threading.Thread(target=listen, daemon=True)
    listener_thread.start()

    # Wait for agents to report
    time.sleep(10)

    # Synthesize findings
    print(f"\n[{agent.agent_id}] === SYNTHESIS ===")
    print(f"Total findings: {len(agent.findings)}")

    by_severity = {}
    for finding in agent.findings:
        sev = finding['finding'].get('severity', 'unknown')
        by_severity[sev] = by_severity.get(sev, 0) + 1

    print(f"By severity: {by_severity}")

    critical_issues = [
        f for f in agent.findings
        if f['finding'].get('severity') == 'critical'
    ]

    if critical_issues:
        print(f"\n🚨 {len(critical_issues)} CRITICAL ISSUES REQUIRE IMMEDIATE ACTION:")
        for issue in critical_issues:
            print(f"  - {issue['agent_id']}: {issue['finding']['description']}")


def main():
    """Main entry point with agent selection."""
    parser = argparse.ArgumentParser(
        description='Multi-agent Redis pub/sub communication demo'
    )
    parser.add_argument(
        '--agent',
        choices=['security', 'performance', 'coordinator'],
        required=True,
        help='Which agent to run'
    )

    args = parser.parse_args()

    if args.agent == 'security':
        run_security_agent()
    elif args.agent == 'performance':
        run_performance_agent()
    elif args.agent == 'coordinator':
        run_coordinator_agent()


if __name__ == '__main__':
    main()
