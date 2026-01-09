#!/usr/bin/env python3
"""
Chapter 1: Introduction to AI
AIOps Examples for DevOps Engineers

Practical examples of AI applications in operations.
"""

import re
from datetime import datetime
from typing import List, Dict, Any


# =============================================================================
# LOG ANALYSIS PATTERNS
# =============================================================================

def analyze_logs_for_anomalies(logs: List[str]) -> Dict[str, Any]:
    """
    Analyze logs for patterns and anomalies.

    In production, this would use ML models for:
    - Anomaly detection
    - Log clustering
    - Pattern recognition
    """
    analysis = {
        "total_lines": len(logs),
        "error_count": 0,
        "warning_count": 0,
        "patterns": {},
        "anomalies": [],
    }

    error_pattern = re.compile(r'(ERROR|FATAL|CRITICAL)', re.IGNORECASE)
    warning_pattern = re.compile(r'WARNING', re.IGNORECASE)

    for log in logs:
        if error_pattern.search(log):
            analysis["error_count"] += 1
        if warning_pattern.search(log):
            analysis["warning_count"] += 1

    # Calculate error rate
    if analysis["total_lines"] > 0:
        error_rate = analysis["error_count"] / analysis["total_lines"]
        if error_rate > 0.1:  # More than 10% errors
            analysis["anomalies"].append({
                "type": "high_error_rate",
                "rate": error_rate,
                "severity": "critical" if error_rate > 0.25 else "warning"
            })

    return analysis


# =============================================================================
# CAPACITY PLANNING
# =============================================================================

def predict_capacity_needs(
    current_cpu: float,
    current_memory: float,
    growth_rate: float = 0.15,  # 15% monthly growth
    months_ahead: int = 6
) -> Dict[str, Any]:
    """
    Predict future capacity needs based on growth rate.

    In production, use ML models trained on historical data for:
    - Time series forecasting
    - Seasonal pattern detection
    - Anomaly-aware predictions
    """
    predictions = []
    cpu = current_cpu
    memory = current_memory

    for month in range(1, months_ahead + 1):
        cpu = cpu * (1 + growth_rate)
        memory = memory * (1 + growth_rate)

        predictions.append({
            "month": month,
            "predicted_cpu_percent": min(cpu, 100),
            "predicted_memory_percent": min(memory, 100),
            "action_needed": cpu > 80 or memory > 80
        })

    # Calculate when scaling is needed
    scale_month = None
    for p in predictions:
        if p["action_needed"] and scale_month is None:
            scale_month = p["month"]

    return {
        "current": {
            "cpu_percent": current_cpu,
            "memory_percent": current_memory
        },
        "predictions": predictions,
        "recommendation": {
            "scale_in_months": scale_month,
            "scale_factor": 2 if scale_month and scale_month <= 3 else 1.5
        }
    }


# =============================================================================
# ALERTING OPTIMIZATION
# =============================================================================

class SmartAlerting:
    """
    AI-enhanced alerting system concepts.

    Real AIOps platforms use ML for:
    - Alert correlation and deduplication
    - Dynamic threshold adjustment
    - Predictive alerting (before issues occur)
    - Noise reduction
    """

    def __init__(self):
        self.alert_history = []
        self.correlation_window = 300  # 5 minutes

    def should_alert(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """Determine if alert should fire or be suppressed."""
        # Check for correlation with existing alerts
        correlated = self._find_correlated_alerts(alert)

        # Check for flapping (rapid on/off)
        is_flapping = self._detect_flapping(alert)

        decision = {
            "fire": True,
            "reason": "new_alert",
            "correlations": correlated,
            "is_flapping": is_flapping
        }

        if correlated:
            decision["fire"] = False
            decision["reason"] = "correlated_with_existing"

        if is_flapping:
            decision["fire"] = False
            decision["reason"] = "flapping_detected"

        self.alert_history.append({
            "alert": alert,
            "decision": decision,
            "timestamp": datetime.now()
        })

        return decision

    def _find_correlated_alerts(self, alert: Dict) -> List[Dict]:
        """Find alerts that might be related to this one."""
        correlated = []
        for hist in self.alert_history[-100:]:  # Check last 100
            if self._are_correlated(alert, hist["alert"]):
                correlated.append(hist["alert"])
        return correlated

    def _are_correlated(self, alert1: Dict, alert2: Dict) -> bool:
        """Check if two alerts are correlated."""
        # Simple correlation: same service or same type
        return (
            alert1.get("service") == alert2.get("service") or
            alert1.get("type") == alert2.get("type")
        )

    def _detect_flapping(self, alert: Dict) -> bool:
        """Detect if an alert is flapping (rapid on/off)."""
        # Count occurrences in recent history
        count = sum(
            1 for h in self.alert_history[-20:]
            if h["alert"].get("name") == alert.get("name")
        )
        return count >= 5  # Flapping if 5+ occurrences recently


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Log analysis example
    sample_logs = [
        "2024-01-15 10:00:00 INFO Application started",
        "2024-01-15 10:00:01 ERROR Database connection failed",
        "2024-01-15 10:00:02 ERROR Retry attempt 1",
        "2024-01-15 10:00:03 WARNING High memory usage",
        "2024-01-15 10:00:04 INFO Request processed",
    ]

    print("Log Analysis Results:")
    print("-" * 40)
    analysis = analyze_logs_for_anomalies(sample_logs)
    print(f"Total lines: {analysis['total_lines']}")
    print(f"Errors: {analysis['error_count']}")
    print(f"Warnings: {analysis['warning_count']}")
    if analysis['anomalies']:
        print(f"Anomalies: {analysis['anomalies']}")

    print("\n" + "=" * 40)
    print("Capacity Planning:")
    print("-" * 40)
    capacity = predict_capacity_needs(
        current_cpu=45,
        current_memory=55,
        growth_rate=0.20,  # 20% monthly growth
        months_ahead=6
    )
    print(f"Current CPU: {capacity['current']['cpu_percent']}%")
    print(f"Current Memory: {capacity['current']['memory_percent']}%")
    print(f"Scale needed in: {capacity['recommendation']['scale_in_months']} months")
