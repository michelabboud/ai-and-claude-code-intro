#!/usr/bin/env python3
"""
Chapter 17: AI-Powered Observability & AIOps
Prometheus + Claude AI Integration

Adds AI-powered analysis to Prometheus metrics and alerts.
Automatically explains spikes, anomalies, and alert conditions.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install anthropic prometheus-api-client pandas

Usage:
    # Analyze why a metric is spiking
    python prometheus_ai.py \
        --prometheus http://localhost:9090 \
        --query 'rate(http_requests_total[5m])' \
        --explain-spike

    # Get AI insights on current metric value
    python prometheus_ai.py \
        --query 'container_memory_usage_bytes{pod="api-server"}' \
        --analyze

    # Compare two time periods
    python prometheus_ai.py \
        --query 'node_cpu_seconds_total' \
        --compare \
        --baseline '24h ago' \
        --current 'now'

    # Monitor for significant changes
    python prometheus_ai.py \
        --query 'database_query_duration_seconds' \
        --watch \
        --threshold-pct 20
"""

import anthropic
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
from prometheus_api_client import PrometheusConnect


class PrometheusAI:
    """
    AI-powered analysis of Prometheus metrics.

    Combines metric data with Claude's reasoning to provide
    human-readable explanations and recommendations.
    """

    def __init__(
        self,
        prometheus_url: str,
        anthropic_api_key: str,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        Initialize Prometheus AI analyzer.

        Args:
            prometheus_url: URL of Prometheus server
            anthropic_api_key: API key for Claude
            model: Claude model to use
        """
        self.prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.model = model

    def analyze_metric(
        self,
        query: str,
        lookback: str = "1h",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get AI analysis of a metric's current state.

        Args:
            query: PromQL query
            lookback: Historical window for context
            context: Additional context for AI

        Returns:
            Dict with analysis, insights, and recommendations
        """
        # Fetch current value
        current_result = self.prom.custom_query(query=query)
        if not current_result:
            raise ValueError(f"No data for query: {query}")

        current_value = float(current_result[0]['value'][1])
        labels = current_result[0]['metric']

        # Fetch recent history
        end_time = datetime.utcnow()
        start_time = end_time - self._parse_duration(lookback)

        history = self.prom.custom_query_range(
            query=query,
            start_time=start_time,
            end_time=end_time,
            step='1m'
        )

        if not history or 'values' not in history[0]:
            raise ValueError("No historical data available")

        # Calculate statistics
        values = [float(v) for t, v in history[0]['values']]
        stats = self._calculate_stats(values)

        # Ask Claude for analysis
        prompt = f"""Analyze this Prometheus metric:

Metric Query: {query}
Current Value: {current_value}

Labels: {json.dumps(labels, indent=2)}

Recent Statistics (last {lookback}):
- Mean: {stats['mean']:.2f}
- Std Dev: {stats['std_dev']:.2f}
- Min: {stats['min']:.2f}
- Max: {stats['max']:.2f}
- Trend: {stats['trend']}

Value Distribution:
- p50 (median): {stats['p50']:.2f}
- p95: {stats['p95']:.2f}
- p99: {stats['p99']:.2f}

{f"Additional Context: {context}" if context else ""}

Provide:
1. What does this metric measure? (in plain English for a non-expert)
2. Is the current value normal, concerning, or critical?
3. What might cause this metric to increase/decrease?
4. Any recommendations for optimization or investigation?

Output JSON:
{{
  "metric_explanation": "what this measures",
  "status": "normal/concerning/critical",
  "health_score": 0-100,
  "insights": ["insight 1", "insight 2"],
  "recommendations": ["recommendation 1", "recommendation 2"]
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = json.loads(response.content[0].text)

        return {
            "query": query,
            "current_value": current_value,
            "labels": labels,
            "statistics": stats,
            "ai_analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }

    def explain_spike(
        self,
        query: str,
        spike_threshold_pct: float = 50.0,
        lookback: str = "6h"
    ) -> Optional[Dict[str, Any]]:
        """
        Detect and explain metric spikes.

        Args:
            query: PromQL query
            spike_threshold_pct: Percentage increase to consider a spike
            lookback: Historical window

        Returns:
            Dict with spike analysis, or None if no spike detected
        """
        # Fetch data
        end_time = datetime.utcnow()
        start_time = end_time - self._parse_duration(lookback)

        history = self.prom.custom_query_range(
            query=query,
            start_time=start_time,
            end_time=end_time,
            step='1m'
        )

        if not history or 'values' not in history[0]:
            raise ValueError("No data available")

        values = [float(v) for t, v in history[0]['values']]
        timestamps = [datetime.fromtimestamp(t) for t, v in history[0]['values']]

        # Calculate baseline (first 80% of data)
        baseline_len = int(len(values) * 0.8)
        baseline_values = values[:baseline_len]
        recent_values = values[baseline_len:]

        baseline_mean = sum(baseline_values) / len(baseline_values)
        recent_mean = sum(recent_values) / len(recent_values)

        pct_change = ((recent_mean - baseline_mean) / baseline_mean) * 100

        if abs(pct_change) < spike_threshold_pct:
            return None  # No significant spike

        # Find peak value
        peak_value = max(recent_values)
        peak_index = values.index(peak_value)
        peak_time = timestamps[peak_index]

        # Ask Claude to explain
        prompt = f"""A significant spike has been detected in a Prometheus metric.

Metric Query: {query}

Spike Details:
- Baseline mean: {baseline_mean:.2f}
- Recent mean: {recent_mean:.2f}
- Change: {pct_change:+.1f}%
- Peak value: {peak_value:.2f} at {peak_time.strftime('%Y-%m-%d %H:%M:%S')}
- Duration: {lookback}

What are the most likely causes for this spike? Consider:
- Application issues (memory leaks, infinite loops, bad deployments)
- Infrastructure issues (CPU throttling, disk I/O, network)
- External factors (traffic surge, DDoS, scheduled jobs)
- Configuration changes

Output JSON:
{{
  "likely_causes": ["cause 1", "cause 2", "cause 3"],
  "severity": "low/medium/high/critical",
  "investigation_steps": ["step 1", "step 2"],
  "possible_fixes": ["fix 1", "fix 2"]
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        explanation = json.loads(response.content[0].text)

        return {
            "query": query,
            "spike_detected": True,
            "baseline_mean": baseline_mean,
            "recent_mean": recent_mean,
            "percent_change": pct_change,
            "peak_value": peak_value,
            "peak_time": peak_time.isoformat(),
            "explanation": explanation,
            "timestamp": datetime.utcnow().isoformat()
        }

    def compare_time_periods(
        self,
        query: str,
        period1_start: str,
        period1_end: str,
        period2_start: str,
        period2_end: str
    ) -> Dict[str, Any]:
        """
        Compare metric behavior across two time periods.

        Args:
            query: PromQL query
            period1_start: Start of baseline period
            period1_end: End of baseline period
            period2_start: Start of comparison period
            period2_end: End of comparison period

        Returns:
            Dict with comparison analysis
        """
        # Fetch both periods
        period1_data = self.prom.custom_query_range(
            query=query,
            start_time=self._parse_timestamp(period1_start),
            end_time=self._parse_timestamp(period1_end),
            step='5m'
        )

        period2_data = self.prom.custom_query_range(
            query=query,
            start_time=self._parse_timestamp(period2_start),
            end_time=self._parse_timestamp(period2_end),
            step='5m'
        )

        if not period1_data or not period2_data:
            raise ValueError("Insufficient data for comparison")

        values1 = [float(v) for t, v in period1_data[0]['values']]
        values2 = [float(v) for t, v in period2_data[0]['values']]

        stats1 = self._calculate_stats(values1)
        stats2 = self._calculate_stats(values2)

        # Calculate differences
        mean_diff = stats2['mean'] - stats1['mean']
        pct_diff = (mean_diff / stats1['mean']) * 100 if stats1['mean'] != 0 else 0

        prompt = f"""Compare these two time periods for a Prometheus metric.

Metric: {query}

Period 1 ({period1_start} to {period1_end}):
- Mean: {stats1['mean']:.2f}
- Std Dev: {stats1['std_dev']:.2f}
- Min/Max: {stats1['min']:.2f} / {stats1['max']:.2f}
- p95: {stats1['p95']:.2f}

Period 2 ({period2_start} to {period2_end}):
- Mean: {stats2['mean']:.2f}
- Std Dev: {stats2['std_dev']:.2f}
- Min/Max: {stats2['min']:.2f} / {stats2['max']:.2f}
- p95: {stats2['p95']:.2f}

Change: {pct_diff:+.1f}%

What explains this change? Is it expected behavior or concerning?

Output JSON:
{{
  "change_explanation": "explanation",
  "is_concerning": true/false,
  "recommendations": ["rec 1", "rec 2"]
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = json.loads(response.content[0].text)

        return {
            "query": query,
            "period1": {"start": period1_start, "end": period1_end, "stats": stats1},
            "period2": {"start": period2_start, "end": period2_end, "stats": stats2},
            "percent_change": pct_diff,
            "ai_analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _calculate_stats(self, values: List[float]) -> Dict[str, Any]:
        """Calculate statistical summary."""
        import numpy as np

        arr = np.array(values)
        return {
            "mean": float(np.mean(arr)),
            "std_dev": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "p50": float(np.percentile(arr, 50)),
            "p95": float(np.percentile(arr, 95)),
            "p99": float(np.percentile(arr, 99)),
            "trend": "increasing" if arr[-1] > arr[0] else "decreasing"
        }

    def _parse_duration(self, duration_str: str) -> timedelta:
        """Parse duration like '1h', '6h', '24h'."""
        unit = duration_str[-1]
        value = int(duration_str[:-1])

        if unit == 'h':
            return timedelta(hours=value)
        elif unit == 'd':
            return timedelta(days=value)
        elif unit == 'm':
            return timedelta(minutes=value)
        else:
            raise ValueError(f"Invalid duration: {duration_str}")

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp like 'now', '24h ago', '2024-01-15T10:00:00'."""
        if timestamp_str == 'now':
            return datetime.utcnow()
        elif timestamp_str.endswith(' ago'):
            duration = timestamp_str.replace(' ago', '')
            return datetime.utcnow() - self._parse_duration(duration)
        else:
            return datetime.fromisoformat(timestamp_str)


def main():
    parser = argparse.ArgumentParser(description='AI-powered Prometheus analysis')
    parser.add_argument('--prometheus', required=True, help='Prometheus URL')
    parser.add_argument('--query', required=True, help='PromQL query')
    parser.add_argument('--analyze', action='store_true', help='Analyze current state')
    parser.add_argument('--explain-spike', action='store_true', help='Detect and explain spikes')
    parser.add_argument('--compare', action='store_true', help='Compare time periods')
    parser.add_argument('--lookback', default='1h', help='Historical window')
    parser.add_argument('--threshold-pct', type=float, default=50, help='Spike threshold %')
    parser.add_argument('--baseline', help='Baseline period for comparison')
    parser.add_argument('--current', default='now', help='Current period for comparison')
    parser.add_argument('--output', help='Output file (JSON)')

    args = parser.parse_args()

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)

    prom_ai = PrometheusAI(
        prometheus_url=args.prometheus,
        anthropic_api_key=api_key
    )

    if args.analyze:
        print(f"🔍 Analyzing: {args.query}\n")
        result = prom_ai.analyze_metric(query=args.query, lookback=args.lookback)

        print(f"Current Value: {result['current_value']:.2f}")
        print(f"Status: {result['ai_analysis']['status'].upper()}")
        print(f"Health Score: {result['ai_analysis']['health_score']}/100")
        print(f"\nWhat it measures:\n{result['ai_analysis']['metric_explanation']}")
        print(f"\nInsights:")
        for insight in result['ai_analysis']['insights']:
            print(f"  • {insight}")
        print(f"\nRecommendations:")
        for rec in result['ai_analysis']['recommendations']:
            print(f"  • {rec}")

    elif args.explain_spike:
        print(f"🔍 Checking for spikes: {args.query}\n")
        result = prom_ai.explain_spike(
            query=args.query,
            spike_threshold_pct=args.threshold_pct,
            lookback=args.lookback
        )

        if result:
            print(f"🚨 SPIKE DETECTED")
            print(f"Change: {result['percent_change']:+.1f}%")
            print(f"Peak: {result['peak_value']:.2f} at {result['peak_time']}")
            print(f"Severity: {result['explanation']['severity'].upper()}")
            print(f"\nLikely Causes:")
            for cause in result['explanation']['likely_causes']:
                print(f"  • {cause}")
            print(f"\nInvestigation Steps:")
            for step in result['explanation']['investigation_steps']:
                print(f"  {step}")
        else:
            print("✓ No significant spike detected")

    elif args.compare:
        if not args.baseline:
            print("❌ --baseline required for comparison")
            sys.exit(1)

        # Parse time periods (simplified for example)
        period1_end = datetime.utcnow() - prom_ai._parse_duration(args.baseline)
        period1_start = period1_end - prom_ai._parse_duration(args.lookback)

        period2_end = datetime.utcnow()
        period2_start = period2_end - prom_ai._parse_duration(args.lookback)

        result = prom_ai.compare_time_periods(
            query=args.query,
            period1_start=period1_start.isoformat(),
            period1_end=period1_end.isoformat(),
            period2_start=period2_start.isoformat(),
            period2_end=period2_end.isoformat()
        )

        print(f"📊 Comparison: {args.query}")
        print(f"Change: {result['percent_change']:+.1f}%")
        print(f"Concerning: {'YES' if result['ai_analysis']['is_concerning'] else 'NO'}")
        print(f"\n{result['ai_analysis']['change_explanation']}")

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n✓ Saved to: {args.output}")


if __name__ == '__main__':
    main()
