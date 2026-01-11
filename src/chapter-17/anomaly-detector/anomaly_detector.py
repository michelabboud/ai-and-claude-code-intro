#!/usr/bin/env python3
"""
Chapter 17: AI-Powered Observability & AIOps
AI Anomaly Detector

Detects anomalies in time-series metrics using Claude AI analysis.
Goes beyond static thresholds by understanding context and patterns.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install anthropic prometheus-api-client numpy scipy

Usage:
    # Analyze a single metric
    python anomaly_detector.py \
        --prometheus http://localhost:9090 \
        --metric 'http_requests_total{job="api"}' \
        --lookback 7d

    # Continuous monitoring mode
    python anomaly_detector.py \
        --prometheus http://localhost:9090 \
        --metric 'memory_usage_bytes' \
        --continuous \
        --check-interval 60

    # Batch analysis of multiple metrics
    python anomaly_detector.py \
        --prometheus http://localhost:9090 \
        --config metrics.yaml \
        --output anomalies.json
"""

import anthropic
import argparse
import json
import time
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import numpy as np
from scipy import stats
from prometheus_api_client import PrometheusConnect


@dataclass
class AnomalyResult:
    """Result of anomaly detection analysis."""
    metric_name: str
    timestamp: str
    current_value: float
    is_anomalous: bool
    confidence: float  # 0.0 to 1.0
    severity: str  # low, medium, high, critical
    deviation_magnitude: float  # How many standard deviations from mean
    likely_cause: str
    should_alert: bool
    recommended_action: str
    explanation: str
    statistical_context: Dict[str, float]


class AIAnomalyDetector:
    """
    AI-powered anomaly detection for time-series metrics.

    Combines statistical analysis with Claude AI's contextual understanding
    to identify genuine anomalies while reducing false positives.
    """

    def __init__(
        self,
        anthropic_api_key: str,
        prometheus_url: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        Initialize the anomaly detector.

        Args:
            anthropic_api_key: API key for Claude
            prometheus_url: URL of Prometheus server (optional)
            model: Claude model to use for analysis
        """
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.model = model
        self.prom = PrometheusConnect(url=prometheus_url) if prometheus_url else None

    def detect_anomalies(
        self,
        metric_name: str,
        current_value: float,
        historical_data: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> AnomalyResult:
        """
        Analyze metric for anomalies using AI + statistical methods.

        Args:
            metric_name: Name of the metric being analyzed
            current_value: Current value of the metric
            historical_data: List of {timestamp, value} dicts for historical context
            context: Additional context (labels, related metrics, events, etc.)

        Returns:
            AnomalyResult with detailed analysis
        """
        # Step 1: Calculate statistical baseline
        values = [float(d['value']) for d in historical_data if 'value' in d]

        if len(values) < 10:
            raise ValueError(f"Insufficient data: need at least 10 historical points, got {len(values)}")

        stats_context = self._calculate_statistics(values, current_value)

        # Step 2: Prepare context for AI analysis
        context_str = ""
        if context:
            context_str = f"\n\nAdditional Context:\n{json.dumps(context, indent=2)}"

        # Format historical data for readability
        recent_samples = historical_data[-20:]  # Last 20 data points
        historical_summary = self._format_historical_data(recent_samples)

        # Step 3: Ask Claude to analyze
        prompt = f"""Analyze this time-series metric for anomalies.

Metric: {metric_name}
Current Value: {current_value}

Statistical Analysis:
- Mean: {stats_context['mean']:.2f}
- Std Dev: {stats_context['std_dev']:.2f}
- Current is {stats_context['std_devs_from_mean']:.2f} standard deviations from mean
- Min (historical): {stats_context['min']:.2f}
- Max (historical): {stats_context['max']:.2f}
- 95th Percentile: {stats_context['p95']:.2f}

Recent Historical Data (last 20 samples):
{historical_summary}
{context_str}

Analyze and determine:
1. Is this current value genuinely anomalous? Consider:
   - Statistical deviation (already {stats_context['std_devs_from_mean']:.2f} σ)
   - Trend direction (increasing, decreasing, spike)
   - Seasonality patterns (time of day, day of week)
   - Business context (is this expected behavior?)

2. If anomalous, what severity level?
   - Low: Unusual but not concerning
   - Medium: Should investigate soon
   - High: Requires immediate attention
   - Critical: Production impact likely

3. What is the most likely root cause? Be specific.

4. Should we alert the on-call engineer? Consider alert fatigue.

5. What action should they take first?

Output ONLY valid JSON with this exact structure:
{{
  "is_anomalous": true/false,
  "confidence": 0.0-1.0,
  "severity": "low/medium/high/critical",
  "likely_cause": "brief explanation",
  "should_alert": true/false,
  "recommended_action": "specific next step",
  "explanation": "detailed reasoning for your determination"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse AI response
            ai_analysis = json.loads(response.content[0].text)

            # Combine statistical and AI analysis
            return AnomalyResult(
                metric_name=metric_name,
                timestamp=datetime.utcnow().isoformat(),
                current_value=current_value,
                is_anomalous=ai_analysis['is_anomalous'],
                confidence=ai_analysis['confidence'],
                severity=ai_analysis['severity'],
                deviation_magnitude=stats_context['std_devs_from_mean'],
                likely_cause=ai_analysis['likely_cause'],
                should_alert=ai_analysis['should_alert'],
                recommended_action=ai_analysis['recommended_action'],
                explanation=ai_analysis['explanation'],
                statistical_context=stats_context
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Anomaly detection failed: {e}")

    def detect_from_prometheus(
        self,
        query: str,
        lookback: str = "7d",
        context: Optional[Dict[str, Any]] = None
    ) -> AnomalyResult:
        """
        Fetch metric from Prometheus and analyze for anomalies.

        Args:
            query: PromQL query (e.g., 'http_requests_total{job="api"}')
            lookback: How far back to look for historical data (e.g., '7d', '24h')
            context: Additional context for analysis

        Returns:
            AnomalyResult
        """
        if not self.prom:
            raise RuntimeError("Prometheus connection not configured")

        # Fetch current value
        current_result = self.prom.custom_query(query=query)
        if not current_result:
            raise ValueError(f"No data returned for query: {query}")

        current_value = float(current_result[0]['value'][1])
        metric_name = query

        # Fetch historical data
        end_time = datetime.utcnow()
        start_time = end_time - self._parse_duration(lookback)

        historical_result = self.prom.custom_query_range(
            query=query,
            start_time=start_time,
            end_time=end_time,
            step='5m'  # 5-minute resolution
        )

        if not historical_result or 'values' not in historical_result[0]:
            raise ValueError(f"No historical data for query: {query}")

        # Format historical data
        historical_data = [
            {'timestamp': datetime.fromtimestamp(t).isoformat(), 'value': float(v)}
            for t, v in historical_result[0]['values']
        ]

        return self.detect_anomalies(
            metric_name=metric_name,
            current_value=current_value,
            historical_data=historical_data,
            context=context
        )

    def _calculate_statistics(self, values: List[float], current_value: float) -> Dict[str, float]:
        """Calculate statistical metrics for the data."""
        arr = np.array(values)
        mean = np.mean(arr)
        std_dev = np.std(arr)

        return {
            'mean': float(mean),
            'std_dev': float(std_dev),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'median': float(np.median(arr)),
            'p95': float(np.percentile(arr, 95)),
            'p99': float(np.percentile(arr, 99)),
            'std_devs_from_mean': float((current_value - mean) / std_dev) if std_dev > 0 else 0
        }

    def _format_historical_data(self, data: List[Dict[str, Any]], max_lines: int = 20) -> str:
        """Format historical data for display in prompt."""
        lines = []
        for d in data[-max_lines:]:
            ts = d.get('timestamp', 'unknown')
            val = d.get('value', 0)
            lines.append(f"  {ts}: {val}")
        return "\n".join(lines)

    def _parse_duration(self, duration_str: str) -> timedelta:
        """Parse duration string like '7d', '24h', '30m' into timedelta."""
        unit = duration_str[-1]
        value = int(duration_str[:-1])

        if unit == 'd':
            return timedelta(days=value)
        elif unit == 'h':
            return timedelta(hours=value)
        elif unit == 'm':
            return timedelta(minutes=value)
        else:
            raise ValueError(f"Invalid duration unit: {unit}")


def continuous_monitoring(
    detector: AIAnomalyDetector,
    query: str,
    check_interval: int = 60,
    lookback: str = "7d"
):
    """
    Run continuous anomaly monitoring.

    Args:
        detector: AIAnomalyDetector instance
        query: PromQL query to monitor
        check_interval: Seconds between checks
        lookback: Historical data window
    """
    print(f"🔍 Starting continuous monitoring of: {query}")
    print(f"   Check interval: {check_interval}s")
    print(f"   Historical lookback: {lookback}")
    print(f"   Press Ctrl+C to stop\n")

    consecutive_anomalies = 0

    try:
        while True:
            try:
                result = detector.detect_from_prometheus(
                    query=query,
                    lookback=lookback
                )

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if result.is_anomalous:
                    consecutive_anomalies += 1
                    icon = "🚨" if result.severity in ["high", "critical"] else "⚠️"
                    print(f"{icon} [{timestamp}] ANOMALY DETECTED")
                    print(f"   Value: {result.current_value:.2f} ({result.deviation_magnitude:.2f}σ)")
                    print(f"   Severity: {result.severity.upper()} (confidence: {result.confidence:.0%})")
                    print(f"   Cause: {result.likely_cause}")

                    if result.should_alert:
                        print(f"   🔔 ALERT: {result.recommended_action}")

                    if consecutive_anomalies >= 3:
                        print(f"   ⚠️  WARNING: {consecutive_anomalies} consecutive anomalies detected")
                else:
                    consecutive_anomalies = 0
                    print(f"✓ [{timestamp}] Normal - Value: {result.current_value:.2f} (within expected range)")

            except Exception as e:
                print(f"❌ Error during check: {e}")

            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")


def main():
    parser = argparse.ArgumentParser(
        description='AI-powered anomaly detection for Prometheus metrics'
    )
    parser.add_argument(
        '--prometheus',
        required=True,
        help='Prometheus server URL (e.g., http://localhost:9090)'
    )
    parser.add_argument(
        '--metric',
        help='PromQL query to analyze'
    )
    parser.add_argument(
        '--lookback',
        default='7d',
        help='Historical data window (e.g., 7d, 24h, 30m)'
    )
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Run in continuous monitoring mode'
    )
    parser.add_argument(
        '--check-interval',
        type=int,
        default=60,
        help='Seconds between checks in continuous mode'
    )
    parser.add_argument(
        '--output',
        help='Output file for results (JSON)'
    )

    args = parser.parse_args()

    # Get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    # Initialize detector
    detector = AIAnomalyDetector(
        anthropic_api_key=api_key,
        prometheus_url=args.prometheus
    )

    if args.continuous:
        # Continuous monitoring mode
        if not args.metric:
            print("❌ Error: --metric required for continuous monitoring")
            sys.exit(1)

        continuous_monitoring(
            detector=detector,
            query=args.metric,
            check_interval=args.check_interval,
            lookback=args.lookback
        )
    else:
        # Single analysis mode
        if not args.metric:
            print("❌ Error: --metric required")
            sys.exit(1)

        print(f"🔍 Analyzing metric: {args.metric}")
        print(f"   Lookback: {args.lookback}\n")

        result = detector.detect_from_prometheus(
            query=args.metric,
            lookback=args.lookback
        )

        # Display results
        print(f"{'='*70}")
        print(f"Anomaly Detection Results")
        print(f"{'='*70}")
        print(f"Metric: {result.metric_name}")
        print(f"Current Value: {result.current_value:.2f}")
        print(f"Statistical Deviation: {result.deviation_magnitude:.2f} standard deviations")
        print(f"\nAnomaly Detected: {'YES' if result.is_anomalous else 'NO'}")

        if result.is_anomalous:
            print(f"Confidence: {result.confidence:.0%}")
            print(f"Severity: {result.severity.upper()}")
            print(f"Likely Cause: {result.likely_cause}")
            print(f"\nShould Alert: {'YES' if result.should_alert else 'NO'}")
            print(f"Recommended Action: {result.recommended_action}")
            print(f"\nExplanation:\n{result.explanation}")
        else:
            print(f"The metric is within expected ranges.")

        print(f"{'='*70}")

        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(asdict(result), f, indent=2)
            print(f"\n✓ Results saved to: {args.output}")


if __name__ == '__main__':
    main()
