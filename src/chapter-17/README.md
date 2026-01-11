# Chapter 17: AI-Powered Observability & AIOps

Code examples demonstrating AI-powered monitoring intelligence, anomaly detection, predictive alerting, and intelligent alert correlation.

## Directory Structure

```
chapter-17/
├── anomaly-detector/        # AI-powered anomaly detection
├── predictive-alerting/     # Forecasting and predictive alerts
├── alert-correlation/       # Intelligent alert grouping
└── monitoring-integration/  # Prometheus + Grafana integration
```

## Prerequisites

### Python Dependencies

```bash
pip install anthropic prometheus-api-client prophet pandas numpy scipy slack-sdk flask pyyaml
```

### API Keys

Set these environment variables:

```bash
export ANTHROPIC_API_KEY="your-key-here"
export SLACK_BOT_TOKEN="xoxb-your-token"  # Optional, for Slack alerts
```

### Prometheus Server

All examples require access to a Prometheus instance:

```bash
# Quick Prometheus setup with Docker
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  prom/prometheus
```

## Examples Overview

### 1. Anomaly Detector (`anomaly-detector/`)

AI-powered anomaly detection that goes beyond static thresholds.

**Features:**
- Statistical baseline calculation (mean, std dev, percentiles)
- AI analysis of deviations with contextual understanding
- Continuous monitoring mode
- Confidence scoring for anomalies

**Usage:**
```bash
cd anomaly-detector

# Analyze a metric once
python anomaly_detector.py \
  --prometheus http://localhost:9090 \
  --metric 'http_requests_total{job="api"}' \
  --lookback 7d

# Continuous monitoring
python anomaly_detector.py \
  --prometheus http://localhost:9090 \
  --metric 'node_memory_MemAvailable_bytes' \
  --continuous \
  --check-interval 60
```

### 2. Predictive Alerting (`predictive-alerting/`)

Forecast metric values using Prophet and alert BEFORE threshold breaches.

**Features:**
- Time-series forecasting with Facebook Prophet
- Seasonality detection (daily, weekly patterns)
- Breach prediction with time estimates
- Slack integration for proactive alerts

**Usage:**
```bash
cd predictive-alerting

# Forecast disk usage
python predictive_alerter.py \
  --prometheus http://localhost:9090 \
  --metric 'node_filesystem_avail_bytes{mountpoint="/"}' \
  --threshold 10737418240 \
  --forecast-hours 24

# Continuous forecasting with Slack alerts
python predictive_alerter.py \
  --prometheus http://localhost:9090 \
  --metric 'node_memory_MemAvailable_bytes' \
  --threshold 1073741824 \
  --forecast-hours 12 \
  --continuous \
  --alert-slack \
  --slack-channel #predictions
```

### 3. Alert Correlation (`alert-correlation/`)

Group related alerts and identify root causes using AI.

**Features:**
- Correlates concurrent alerts (5-minute window)
- Identifies root cause vs. symptoms
- Service topology awareness
- Webhook server for real-time processing

**Usage:**
```bash
cd alert-correlation

# Analyze alerts from file
python alert_correlator.py \
  --alerts alerts.json \
  --topology service-map.yaml

# Run as webhook server
python alert_correlator.py \
  --webhook \
  --port 5000 \
  --topology service-map.yaml \
  --slack-channel #incidents

# Process from stdin (for pipelines)
cat grafana-alerts.json | python alert_correlator.py --stdin
```

**Service Topology Format (`service-map.yaml`):**
```yaml
api-server:
  depends_on:
    - database
    - redis
    - auth-service

frontend:
  depends_on:
    - api-server
    - cdn

database:
  depends_on: []
```

### 4. Monitoring Integration (`monitoring-integration/`)

Direct integration with Prometheus and Grafana.

#### Prometheus AI (`prometheus_ai.py`)

Add AI analysis to any Prometheus metric.

**Usage:**
```bash
cd monitoring-integration

# Analyze current metric state
python prometheus_ai.py \
  --prometheus http://localhost:9090 \
  --query 'rate(http_requests_total[5m])' \
  --analyze

# Explain metric spikes
python prometheus_ai.py \
  --prometheus http://localhost:9090 \
  --query 'container_memory_usage_bytes{pod="api"}' \
  --explain-spike \
  --threshold-pct 50

# Compare time periods
python prometheus_ai.py \
  --prometheus http://localhost:9090 \
  --query 'node_cpu_seconds_total' \
  --compare \
  --baseline '24h ago' \
  --current 'now'
```

#### Grafana Webhook (`grafana_webhook.py`)

Enrich Grafana alerts with AI explanations.

**Usage:**
```bash
# Start webhook server
python grafana_webhook.py \
  --port 5000 \
  --slack-channel #alerts \
  --runbooks runbooks.yaml
```

**Configure in Grafana:**
1. Go to **Alerting → Contact Points**
2. Add new contact point
3. Type: **Webhook**
4. URL: `http://your-server:5000/webhook/grafana`
5. Method: **POST**

**Runbook Configuration (`runbooks.yaml`):**
```yaml
# Map alert names to runbook URLs
"High Memory Usage": "https://wiki.company.com/runbooks/memory"
"Database Connection Failed": "https://wiki.company.com/runbooks/db"

# Or by service
api-server: "https://wiki.company.com/runbooks/api"
database: "https://wiki.company.com/runbooks/postgres"
```

## Real-World Deployment

### Production Checklist

- [ ] Set up Prometheus with retention appropriate for forecasting (7+ days)
- [ ] Configure alerts in Grafana with proper severity labels
- [ ] Create service topology YAML for alert correlation
- [ ] Document runbooks and link them in configuration
- [ ] Set up Slack workspace and bot with permissions
- [ ] Run webhook handlers as systemd services
- [ ] Monitor API costs (Claude usage) with budget alerts
- [ ] Test failover behavior when AI API is unavailable

### systemd Service Example

```ini
[Unit]
Description=Grafana Alert AI Webhook
After=network.target

[Service]
Type=simple
User=monitoring
WorkingDirectory=/opt/monitoring/chapter-17/monitoring-integration
Environment=ANTHROPIC_API_KEY=your-key
Environment=SLACK_BOT_TOKEN=your-token
ExecStart=/usr/bin/python3 grafana_webhook.py --port 5000 --slack-channel #alerts
Restart=always

[Install]
WantedBy=multi-user.target
```

### Cost Optimization

**Typical Costs (Claude Sonnet 3.5):**
- Anomaly detection: ~$0.02 per analysis
- Predictive alerting: ~$0.03 per forecast
- Alert correlation: ~$0.05 per incident
- **Monthly (medium-sized team):** $50-200

**Optimization Tips:**
- Use Haiku for simple explanations ($0.25 vs $3.00 per MTok input)
- Cache analysis results for 5-10 minutes
- Batch related alerts before correlating
- Set minimum severity thresholds (skip P4 alerts)

## Expected Results

### Anomaly Detection
- **Alert volume reduction:** 80-90% (500/day → 50/day)
- **False positive rate:** <5%
- **Mean time to detect (MTTD):** <2 minutes

### Predictive Alerting
- **Prevented incidents:** 60-80% of threshold breaches
- **Advanced warning time:** 4-12 hours average
- **Forecast accuracy:** >85% for 24-hour window

### Alert Correlation
- **Incident investigation time:** 5.6× faster (45 min → 8 min)
- **Root cause accuracy:** >90%
- **On-call alert fatigue:** Reduced by 75%

## Troubleshooting

### "No data returned for query"
- Check Prometheus URL is correct
- Verify metric exists: `http://localhost:9090/graph`
- Ensure time range includes data points

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Insufficient data for forecasting"
Prophet requires at least 48 hours of historical data. Adjust `--lookback-days` or use more frequent scraping.

### "AI analysis failed: rate limit"
You've hit Claude API rate limits. Implement exponential backoff or upgrade to higher tier.

## Next Steps

1. **Chapter 18:** Advanced AIOps (auto-remediation, self-healing)
2. **Production Deployment:** See Chapter 17 main content for case studies
3. **Integration:** Combine with n8n workflows (Chapter 14)

## License

© 2026 Michel Abboud. CC BY-NC 4.0 License.
Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
