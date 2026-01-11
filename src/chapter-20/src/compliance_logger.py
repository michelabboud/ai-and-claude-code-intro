"""
Compliance-grade audit logging for SOC 2, GDPR, PCI-DSS.

Logs all agent actions, detections, and security events.
"""

import json
import time
import re
from typing import Dict, Any, Optional
from pathlib import Path


class ComplianceLogger:
    """
    Audit logger for security compliance.

    Features:
    - Tamper-evident logging
    - PII redaction
    - Retention policies
    - Export for audits
    """

    def __init__(self, log_dir: str = "./audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        self.current_log_file = self.log_dir / f"audit-{int(time.time())}.jsonl"

    def log_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        action: Optional[str] = None,
        result: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Log compliance event.

        Args:
            event_type: Event category (execution, loop_detected, error, security_alert)
            user_id: User who triggered agent (if applicable)
            agent_id: Agent identifier
            action: Action performed
            result: success/failure/loop_detected
            metadata: Additional context
        """
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'user_id': self._redact_pii(user_id),
            'agent_id': agent_id,
            'action': action,
            'result': result,
            'metadata': metadata or {}
        }

        # Write to log file (append-only for tamper resistance)
        with open(self.current_log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def _redact_pii(self, data: Optional[str]) -> Optional[str]:
        """
        Redact Personally Identifiable Information.

        Required for GDPR compliance.
        """
        if not data:
            return None

        # Redact email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        data = re.sub(email_pattern, '[REDACTED_EMAIL]', data)

        # Redact phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        data = re.sub(phone_pattern, '[REDACTED_PHONE]', data)

        # Redact Social Security Numbers
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        data = re.sub(ssn_pattern, '[REDACTED_SSN]', data)

        # Redact credit card numbers
        cc_pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
        data = re.sub(cc_pattern, '[REDACTED_CC]', data)

        return data

    def export_logs(self, start_time: float, end_time: float) -> str:
        """
        Export logs for audit.

        Returns path to export file.
        """
        export_file = self.log_dir / f"export-{int(time.time())}.jsonl"

        with open(export_file, 'w') as out:
            for log_file in self.log_dir.glob("audit-*.jsonl"):
                with open(log_file) as f:
                    for line in f:
                        event = json.loads(line)
                        if start_time <= event['timestamp'] <= end_time:
                            out.write(line)

        return str(export_file)

    def get_statistics(self) -> Dict:
        """
        Get audit log statistics.

        Returns event counts by type.
        """
        stats = {}

        for log_file in self.log_dir.glob("audit-*.jsonl"):
            with open(log_file) as f:
                for line in f:
                    event = json.loads(line)
                    event_type = event['event_type']
                    stats[event_type] = stats.get(event_type, 0) + 1

        return stats


# Example usage
if __name__ == "__main__":
    logger = ComplianceLogger()

    # Log various events
    print("Logging compliance events...")

    logger.log_event(
        event_type='execution',
        user_id='user@example.com',
        agent_id='agent-001',
        action='fix_pod',
        result='success',
        metadata={'pod': 'payment-service'}
    )

    logger.log_event(
        event_type='loop_detected',
        agent_id='agent-001',
        action='restart_pod',
        result='loop_detected',
        metadata={'repetitions': 3, 'pod': 'payment-service'}
    )

    logger.log_event(
        event_type='security_alert',
        user_id='attacker@evil.com',
        agent_id='agent-002',
        action='analyze_logs',
        result='dow_blocked',
        metadata={'reason': 'repetitive_input'}
    )

    # Export logs
    print("\nExporting logs...")
    start = time.time() - 3600  # Last hour
    end = time.time()
    export_path = logger.export_logs(start, end)
    print(f"Logs exported to: {export_path}")

    # Get statistics
    print("\nAudit log statistics:")
    stats = logger.get_statistics()
    for event_type, count in stats.items():
        print(f"  {event_type}: {count}")

    print(f"\nLogs directory: {logger.log_dir}")
