#!/usr/bin/env python3
"""
Chapter 17: AI-Powered Observability & AIOps
Predictive Alerting System

Forecasts metric values using Prophet and alerts BEFORE threshold breaches.
Prevents incidents by predicting problems hours in advance.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install prophet anthropic prometheus-api-client pandas slack-sdk

Usage:
    # Forecast disk usage and predict when it will breach
    python predictive_alerter.py \
        --prometheus http://localhost:9090 \
        --metric 'node_filesystem_avail_bytes{mountpoint="/"}' \
        --threshold 10737418240 \
        --forecast-hours 24 \
        --alert-slack

    # Monitor memory usage with 12-hour forecast
    python predictive_alerter.py \
        --metric 'node_memory_MemAvailable_bytes' \
        --threshold 1073741824 \
        --forecast-hours 12 \
        --continuous

    # Batch forecasting for multiple metrics
    python predictive_alerter.py \
        --config forecasts.yaml \
        --output predictions.json
"""

import anthropic
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import pandas as pd
from prophet import Prophet
from prometheus_api_client import PrometheusConnect
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


@dataclass
class ForecastResult:
    """Result of predictive analysis."""
    metric_name: str
    timestamp: str
    current_value: float
    threshold: float
    forecast_hours: int
    will_breach: bool
    breach_time: Optional[str]
    hours_until_breach: Optional[float]
    breach_value: Optional[float]
    confidence_interval: Dict[str, float]
    severity: str  # info, warning, critical
    recommended_action: str
    ai_analysis: str


class PredictiveAlerter:
    """
    Forecast metric values and alert before threshold breaches.

    Uses Facebook Prophet for time-series forecasting combined with
    Claude AI for contextual recommendations.
    """

    def __init__(
        self,
        anthropic_api_key: str,
        prometheus_url: Optional[str] = None,
        slack_token: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        Initialize the predictive alerter.

        Args:
            anthropic_api_key: API key for Claude
            prometheus_url: URL of Prometheus server
            slack_token: Slack bot token for alerts
            model: Claude model to use
        """
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.model = model
        self.prom = PrometheusConnect(url=prometheus_url) if prometheus_url else None
        self.slack = WebClient(token=slack_token) if slack_token else None

    def forecast_metric(
        self,
        historical_data: pd.DataFrame,
        hours_ahead: int = 24
    ) -> pd.DataFrame:
        """
        Forecast metric values using Prophet.

        Args:
            historical_data: DataFrame with 'ds' (datetime) and 'y' (value) columns
            hours_ahead: Number of hours to forecast

        Returns:
            DataFrame with forecast including yhat, yhat_lower, yhat_upper
        """
        if len(historical_data) < 48:
            raise ValueError("Need at least 48 hours of historical data for reliable forecasting")

        # Configure Prophet model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05,  # Flexibility of trend changes
            seasonality_prior_scale=10.0,   # Strength of seasonality
            interval_width=0.95              # 95% confidence interval
        )

        # Fit model
        model.fit(historical_data)

        # Generate future dataframe
        future = model.make_future_dataframe(periods=hours_ahead, freq='H')

        # Make predictions
        forecast = model.predict(future)

        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    def check_for_breach(
        self,
        metric_name: str,
        current_value: float,
        forecast: pd.DataFrame,
        threshold: float,
        breach_direction: str = "above"  # or "below"
    ) -> ForecastResult:
        """
        Check if forecast predicts a threshold breach.

        Args:
            metric_name: Name of the metric
            current_value: Current metric value
            forecast: Forecast DataFrame from Prophet
            threshold: Threshold value to check against
            breach_direction: Whether we alert when going "above" or "below" threshold

        Returns:
            ForecastResult with breach prediction and recommendations
        """
        now = datetime.utcnow()

        # Find breaches in forecast
        if breach_direction == "above":
            breaches = forecast[forecast['yhat'] > threshold]
        else:
            breaches = forecast[forecast['yhat'] < threshold]

        will_breach = not breaches.empty
        breach_time = None
        hours_until_breach = None
        breach_value = None
        severity = "info"

        if will_breach:
            first_breach = breaches.iloc[0]
            breach_time = first_breach['ds']
            hours_until_breach = (breach_time - now).total_seconds() / 3600
            breach_value = first_breach['yhat']

            # Determine severity based on time remaining
            if hours_until_breach < 2:
                severity = "critical"
            elif hours_until_breach < 6:
                severity = "high"
            elif hours_until_breach < 12:
                severity = "medium"
            else:
                severity = "low"

        # Get AI recommendations
        ai_analysis = self._get_ai_recommendations(
            metric_name=metric_name,
            current_value=current_value,
            threshold=threshold,
            will_breach=will_breach,
            hours_until_breach=hours_until_breach,
            breach_value=breach_value,
            forecast_data=forecast.tail(24)  # Next 24 hours
        )

        return ForecastResult(
            metric_name=metric_name,
            timestamp=now.isoformat(),
            current_value=current_value,
            threshold=threshold,
            forecast_hours=len(forecast) - len(forecast[forecast['ds'] <= now]),
            will_breach=will_breach,
            breach_time=breach_time.isoformat() if breach_time else None,
            hours_until_breach=hours_until_breach,
            breach_value=breach_value,
            confidence_interval={
                'lower': float(forecast.iloc[-1]['yhat_lower']),
                'upper': float(forecast.iloc[-1]['yhat_upper'])
            },
            severity=severity,
            recommended_action=ai_analysis['recommended_action'],
            ai_analysis=ai_analysis['explanation']
        )

    def forecast_from_prometheus(
        self,
        query: str,
        threshold: float,
        forecast_hours: int = 24,
        lookback_days: int = 7,
        breach_direction: str = "above"
    ) -> ForecastResult:
        """
        Fetch data from Prometheus, forecast, and check for breaches.

        Args:
            query: PromQL query
            threshold: Threshold value
            forecast_hours: Hours to forecast ahead
            lookback_days: Days of historical data to use
            breach_direction: "above" or "below"

        Returns:
            ForecastResult
        """
        if not self.prom:
            raise RuntimeError("Prometheus connection not configured")

        # Fetch current value
        current_result = self.prom.custom_query(query=query)
        if not current_result:
            raise ValueError(f"No data for query: {query}")

        current_value = float(current_result[0]['value'][1])

        # Fetch historical data
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=lookback_days)

        historical_result = self.prom.custom_query_range(
            query=query,
            start_time=start_time,
            end_time=end_time,
            step='1h'  # Hourly data for forecasting
        )

        if not historical_result or 'values' not in historical_result[0]:
            raise ValueError(f"No historical data for query: {query}")

        # Format for Prophet (needs 'ds' and 'y' columns)
        data = []
        for timestamp, value in historical_result[0]['values']:
            data.append({
                'ds': datetime.fromtimestamp(timestamp),
                'y': float(value)
            })

        df = pd.DataFrame(data)

        # Generate forecast
        forecast = self.forecast_metric(df, hours_ahead=forecast_hours)

        # Check for breach
        return self.check_for_breach(
            metric_name=query,
            current_value=current_value,
            forecast=forecast,
            threshold=threshold,
            breach_direction=breach_direction
        )

    def _get_ai_recommendations(
        self,
        metric_name: str,
        current_value: float,
        threshold: float,
        will_breach: bool,
        hours_until_breach: Optional[float],
        breach_value: Optional[float],
        forecast_data: pd.DataFrame
    ) -> Dict[str, str]:
        """Get AI-powered recommendations for the forecast."""

        forecast_summary = "\n".join([
            f"  {row['ds'].strftime('%Y-%m-%d %H:%M')}: {row['yhat']:.2f} "
            f"(range: {row['yhat_lower']:.2f} - {row['yhat_upper']:.2f})"
            for _, row in forecast_data.iterrows()
        ])

        if will_breach:
            prompt = f"""A predictive alert has been triggered for a production metric.

Metric: {metric_name}
Current Value: {current_value:.2f}
Threshold: {threshold:.2f}

FORECAST: Threshold breach predicted in {hours_until_breach:.1f} hours
Predicted breach value: {breach_value:.2f}

Next 24 hours forecast:
{forecast_summary}

Provide:
1. What immediate action should the team take to PREVENT this breach?
2. What is the likely root cause of this trend?
3. Should we auto-scale, clear cache, optimize queries, or other action?

Output JSON with:
{{
  "recommended_action": "Specific preventive action to take now",
  "explanation": "Why this is happening and why your recommendation will help"
}}"""
        else:
            prompt = f"""Forecast analysis for production metric.

Metric: {metric_name}
Current Value: {current_value:.2f}
Threshold: {threshold:.2f}

FORECAST: No breach predicted in next {len(forecast_data)} hours

Next 24 hours forecast:
{forecast_summary}

Provide:
{{
  "recommended_action": "Any proactive optimizations recommended, or 'No action needed'",
  "explanation": "Brief assessment of metric health"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            return json.loads(response.content[0].text)

        except Exception as e:
            return {
                "recommended_action": "Manual review recommended",
                "explanation": f"AI analysis failed: {e}"
            }

    def send_slack_alert(self, result: ForecastResult, channel: str = "#alerts"):
        """Send predictive alert to Slack."""
        if not self.slack:
            raise RuntimeError("Slack client not configured")

        if result.will_breach:
            color = "danger" if result.severity in ["critical", "high"] else "warning"
            title = f"⚠️ Predictive Alert: {result.metric_name}"
            message = (
                f"*Threshold breach predicted in {result.hours_until_breach:.1f} hours*\n\n"
                f"• Current: {result.current_value:.2f}\n"
                f"• Threshold: {result.threshold:.2f}\n"
                f"• Predicted breach: {result.breach_value:.2f}\n"
                f"• Breach time: {result.breach_time}\n\n"
                f"*Recommended Action:*\n{result.recommended_action}\n\n"
                f"*Analysis:*\n{result.ai_analysis}"
            )
        else:
            color = "good"
            title = f"✅ Forecast OK: {result.metric_name}"
            message = (
                f"No threshold breach predicted in next {result.forecast_hours} hours.\n\n"
                f"• Current: {result.current_value:.2f}\n"
                f"• Threshold: {result.threshold:.2f}\n"
                f"• {result.ai_analysis}"
            )

        try:
            self.slack.chat_postMessage(
                channel=channel,
                text=title,
                attachments=[{
                    "color": color,
                    "title": title,
                    "text": message,
                    "footer": "Predictive Alerting System",
                    "ts": int(datetime.utcnow().timestamp())
                }]
            )
        except SlackApiError as e:
            print(f"❌ Slack alert failed: {e.response['error']}")


def continuous_forecasting(
    alerter: PredictiveAlerter,
    query: str,
    threshold: float,
    forecast_hours: int,
    check_interval: int,
    breach_direction: str = "above",
    slack_channel: Optional[str] = None
):
    """Run continuous predictive monitoring."""
    print(f"🔮 Starting predictive monitoring: {query}")
    print(f"   Threshold: {threshold}")
    print(f"   Forecast window: {forecast_hours} hours")
    print(f"   Check interval: {check_interval} seconds")
    print(f"   Press Ctrl+C to stop\n")

    last_alert_time = None

    try:
        while True:
            try:
                result = alerter.forecast_from_prometheus(
                    query=query,
                    threshold=threshold,
                    forecast_hours=forecast_hours,
                    breach_direction=breach_direction
                )

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if result.will_breach:
                    print(f"⚠️  [{timestamp}] BREACH PREDICTED")
                    print(f"   Time until breach: {result.hours_until_breach:.1f} hours")
                    print(f"   Predicted value: {result.breach_value:.2f} (threshold: {result.threshold:.2f})")
                    print(f"   Severity: {result.severity.upper()}")
                    print(f"   Action: {result.recommended_action}\n")

                    # Send Slack alert (but not more than once per hour)
                    if slack_channel:
                        if not last_alert_time or (datetime.utcnow() - last_alert_time).seconds > 3600:
                            alerter.send_slack_alert(result, channel=slack_channel)
                            last_alert_time = datetime.utcnow()
                else:
                    print(f"✓ [{timestamp}] Forecast OK - No breach predicted")
                    print(f"   Current: {result.current_value:.2f}, Threshold: {result.threshold:.2f}\n")

            except Exception as e:
                print(f"❌ Error: {e}\n")

            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n🛑 Forecasting stopped")


def main():
    parser = argparse.ArgumentParser(
        description='Predictive alerting with time-series forecasting'
    )
    parser.add_argument('--prometheus', required=True, help='Prometheus URL')
    parser.add_argument('--metric', help='PromQL query')
    parser.add_argument('--threshold', type=float, help='Threshold value')
    parser.add_argument('--forecast-hours', type=int, default=24, help='Hours to forecast')
    parser.add_argument('--lookback-days', type=int, default=7, help='Days of historical data')
    parser.add_argument('--breach-direction', choices=['above', 'below'], default='above')
    parser.add_argument('--continuous', action='store_true', help='Continuous monitoring')
    parser.add_argument('--check-interval', type=int, default=300, help='Seconds between checks')
    parser.add_argument('--alert-slack', action='store_true', help='Send Slack alerts')
    parser.add_argument('--slack-channel', default='#alerts', help='Slack channel')
    parser.add_argument('--output', help='Output file (JSON)')

    args = parser.parse_args()

    # Get API keys
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    slack_token = os.getenv('SLACK_BOT_TOKEN') if args.alert_slack else None

    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)

    # Initialize
    alerter = PredictiveAlerter(
        anthropic_api_key=anthropic_key,
        prometheus_url=args.prometheus,
        slack_token=slack_token
    )

    if args.continuous:
        continuous_forecasting(
            alerter=alerter,
            query=args.metric,
            threshold=args.threshold,
            forecast_hours=args.forecast_hours,
            check_interval=args.check_interval,
            breach_direction=args.breach_direction,
            slack_channel=args.slack_channel if args.alert_slack else None
        )
    else:
        # Single forecast
        result = alerter.forecast_from_prometheus(
            query=args.metric,
            threshold=args.threshold,
            forecast_hours=args.forecast_hours,
            lookback_days=args.lookback_days,
            breach_direction=args.breach_direction
        )

        # Display results
        print(f"{'='*70}")
        print("Predictive Forecast Results")
        print(f"{'='*70}")
        print(f"Metric: {result.metric_name}")
        print(f"Current Value: {result.current_value:.2f}")
        print(f"Threshold: {result.threshold:.2f}")
        print(f"\nBreach Predicted: {'YES' if result.will_breach else 'NO'}")

        if result.will_breach:
            print(f"Time Until Breach: {result.hours_until_breach:.1f} hours")
            print(f"Breach Time: {result.breach_time}")
            print(f"Predicted Value: {result.breach_value:.2f}")
            print(f"Severity: {result.severity.upper()}")
            print(f"\nRecommended Action:\n{result.recommended_action}")
            print(f"\nAI Analysis:\n{result.ai_analysis}")
        else:
            print("Metric is forecasted to remain within threshold.")
            print(f"\n{result.ai_analysis}")

        print(f"{'='*70}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(asdict(result), f, indent=2)
            print(f"\n✓ Saved to: {args.output}")

        if args.alert_slack and result.will_breach:
            alerter.send_slack_alert(result, channel=args.slack_channel)
            print(f"✓ Slack alert sent to {args.slack_channel}")


if __name__ == '__main__':
    main()
