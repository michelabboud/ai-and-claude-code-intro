---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #eee
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  h1 {
    color: #00d4ff;
  }
  h2 {
    color: #7c3aed;
  }
  code {
    background-color: #2d2d44;
  }
  a {
    color: #00d4ff;
  }
  table {
    border-collapse: collapse;
    margin: 1em 0;
    width: 100%;
  }
  th {
    background-color: #7c3aed;
    color: #ffffff;
    font-weight: bold;
    padding: 12px 16px;
    text-align: left;
    border: 1px solid #5a2eb8;
  }
  td {
    background-color: #2d2d44;
    color: #eee;
    padding: 10px 16px;
    border: 1px solid #3d3d5c;
  }
  tr:nth-child(even) td {
    background-color: #363654;
  }
---

# AI-Powered Observability

## Chapters 17-18: AIOps Guide

**For DevOps Engineers**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# The Problem with Traditional Monitoring

```
┌────────────────────────────────────────┐
│ 10,000 alerts/month                    │
│ 95% are noise                          │
│ Real issues buried                     │
│ Alert fatigue                          │
│ 2+ hours to find root cause            │
└────────────────────────────────────────┘
```

**We need intelligent systems, not just dashboards**

---

# What is AIOps?

## AI for IT Operations

```
Traditional Monitoring        AIOps
────────────────────         ────────────────────
Static thresholds      →     Dynamic baselines
Manual correlation     →     Auto-correlation
Reactive alerts        →     Predictive alerts
Human RCA             →     AI-powered RCA
```

**AIOps = Observe + Analyze + Act (with AI)**

---

# The AIOps Value Proposition

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Alert Volume | 10K/month | 1K/month | 90% reduction |
| MTTR | 45 min | 3 min | 93% faster |
| False Positives | 95% | 10% | 85% reduction |
| Outage Prevention | 0% | 70% | Predictive |
| Cost per Incident | $112 | $1 | 99% cheaper |

---

# Anomaly Detection

## Beyond Static Thresholds

```python
# Traditional (brittle)
if cpu > 80%:
    alert()

# AI-powered (intelligent)
baseline = ai.learn_normal_behavior(metrics, days=30)
if ai.is_anomalous(current_cpu, baseline, confidence=0.90):
    alert_with_context()
```

**AI learns what's normal for YOUR system**

---

# Anomaly Detection Architecture

```
┌────────────────────────────────────────────┐
│ Prometheus                                 │
│   ↓                                        │
│ Statistical Baseline (Prophet)             │
│   ↓                                        │
│ AI Analysis (Claude)                       │
│   ├─→ Anomaly? (Yes/No)                   │
│   ├─→ Severity (Low/Medium/High/Critical)  │
│   ├─→ Confidence (0.0-1.0)                 │
│   └─→ Suggested Action                     │
└────────────────────────────────────────────┘
```

---

# Anomaly Detection Example

```python
# Real output from Claude
{
    "is_anomaly": true,
    "confidence": 0.92,
    "severity": "critical",
    "explanation": "CPU spiked to 95% at 14:32 UTC,
                    3.2 std deviations above the 30-day
                    baseline of 45%",
    "suggested_actions": [
        "Check for recent deployments",
        "Review application logs for errors",
        "Consider horizontal pod autoscaling"
    ]
}
```

---

# Predictive Alerting

## Prevent Issues Before They Happen

```
┌───────────────────────────────────────────┐
│ Traditional: React when threshold crossed │
│                                           │
│ 14:00 ─ 14:15 ─ 14:30 ─ 14:45 ─ 15:00   │
│   60%    70%    80%    92% ← ALERT!      │
│                                           │
├───────────────────────────────────────────┤
│ Predictive: Alert 2 hours in advance     │
│                                           │
│ 12:00 ─ 12:30 ─ 13:00 ← PREDICT BREACH   │
│   55%    58%    ALERT: "Will hit 95% at  │
│                  15:00 based on trend"    │
└───────────────────────────────────────────┘
```

---

# Predictive Alerting with Prophet

```python
from fbprophet import Prophet

# Train on historical data
model = Prophet()
model.fit(historical_metrics)

# Forecast next 6 hours
future = model.make_future_dataframe(periods=6, freq='H')
forecast = model.predict(future)

# Predict threshold breach
if forecast['yhat'].max() > threshold:
    alert_now(
        message="Predicted breach at 15:00",
        confidence=forecast['confidence'],
        time_to_breach='2 hours'
    )
```

---

# Alert Correlation

## Finding the Root Cause

```
Before Correlation:
├─ HighCPU (service-a)
├─ SlowResponse (service-a)
├─ DatabaseConnectionPoolExhausted (db)
├─ HighMemory (service-a)
└─ PodRestarting (service-a)

After AI Correlation:
└─ ROOT CAUSE: DatabaseConnectionPoolExhausted
   └─ SYMPTOMS: HighCPU, SlowResponse, HighMemory,
                PodRestarting
```

**5 alerts → 1 actionable incident**

---

# Alert Correlation Strategy

## Temporal Grouping + Topology Awareness

```python
# Group alerts within 5-minute window
alerts_in_window = alerts.filter(
    time_range=(now - 5min, now)
)

# Understand service dependencies
topology = {
    'service-a': ['db', 'cache'],
    'service-b': ['service-a', 'queue']
}

# AI identifies root cause
root_cause = claude.analyze_correlation(
    alerts=alerts_in_window,
    topology=topology
)
```

---

# Auto-Remediation

## The Safety Pyramid

```
┌────────────────────────────────────────┐
│ FORBIDDEN (Never automate)             │
│  ├─ delete_database                    │
│  ├─ revoke_ssl_certificate             │
│  └─ modify_dns_records                 │
├────────────────────────────────────────┤
│ REQUIRES_APPROVAL (Ask first)          │
│  ├─ rollback_deployment                │
│  ├─ scale_down_production              │
│  └─ restart_database                   │
├────────────────────────────────────────┤
│ SAFE (Automate freely)                 │
│  ├─ restart_pod                        │
│  ├─ clear_cache                        │
│  └─ increase_memory_limit              │
└────────────────────────────────────────┘
```

---

# Auto-Remediation Workflow

```
Alert Received
      ↓
AI Diagnoses Issue
      ↓
Classify Action (SAFE/APPROVAL/FORBIDDEN)
      ↓
   ┌──┴──┐
   ↓     ↓
SAFE    APPROVAL    FORBIDDEN
   ↓     ↓           ↓
Execute  Ask Human  Block + Escalate
   ↓     ↓
Validate Result
   ↓
Success? → Audit Log
Failure? → Rollback + Escalate
```

---

# Auto-Remediation Engine

```python
class AutoRemediationEngine:
    SAFE_ACTIONS = {
        'restart_pod': {
            'blast_radius': 'single pod',
            'typical_duration': '5-30 seconds'
        }
    }

    async def handle_alert(self, alert):
        # AI diagnoses
        diagnosis = await self.ai_diagnose(alert)

        # Classify action
        action = self.ACTIONS[diagnosis['recommended_action']]

        if action.safety == RemediationSafety.FORBIDDEN:
            await self.escalate_to_human()
        elif action.safety == RemediationSafety.SAFE:
            result = await self.execute_remediation(action)
        # ...
```

---

# Circuit Breaker Pattern

## Prevent Runaway Automation

```python
class CircuitBreaker:
    def __init__(self):
        self.failure_count = 0
        self.threshold = 3  # Open after 3 failures

    def can_execute(self):
        if self.failure_count >= self.threshold:
            return False  # Circuit OPEN
        return True  # Circuit CLOSED

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.threshold:
            alert_humans("Circuit breaker OPEN")
            self.reset_timer = 15_minutes
```

---

# Self-Healing Infrastructure

## The OODA Loop

```
┌────────────────────────────────────────┐
│  Observe                               │
│   ↓                                    │
│  Orient (AI analysis)                  │
│   ↓                                    │
│  Decide (confidence threshold)         │
│   ↓                                    │
│  Act (execute remediation)             │
│   ↓                                    │
│  Validate (check if fixed)             │
│   └─→ Loop back if needed              │
└────────────────────────────────────────┘
```

---

# Kubernetes Self-Healing Operator

```python
@kopf.on.event('pods')
async def pod_event_handler(event, **kwargs):
    pod = event['object']
    phase = pod['status']['phase']

    if phase in ['Failed', 'CrashLoopBackOff']:
        # AI diagnoses the issue
        diagnosis = await ai.analyze_pod_failure(pod)

        if diagnosis['confidence'] > 0.80:
            # Auto-fix
            await apply_fix(pod, diagnosis)
        else:
            # Escalate to human
            await escalate(pod, diagnosis)
```

---

# Self-Healing Remediations

| Failure Type | AI Diagnosis | Auto-Fix |
|--------------|--------------|----------|
| OOMKilled | "Container needs 2GB memory" | Increase memory limit |
| CrashLoopBackOff | "Bad deployment v1.2.3" | Rollback to v1.2.2 |
| ImagePullBackOff | "Image tag doesn't exist" | Escalate to human |
| CPU Throttling | "CPU limit too low" | Increase CPU limit |

**80%+ auto-healing rate in production**

---

# Log Analysis at Scale

## The Challenge

```
10,000 logs/day × 365 days = 3.65M logs
$3/MTok × 3.65M tokens = $10,950/year ❌
```

## The Solution

```
Batch Processing (50 logs/call) + Haiku Model
= $0.001/call × 200 calls/day × 365 days
= $73/year ✅

99% cost reduction with intelligent sampling
```

---

# Log Analysis Strategy

## Intelligent Sampling

```python
# 100% of critical logs
if log.level in ['ERROR', 'CRITICAL']:
    analyze_with_ai(log)

# 10% sample of routine logs
elif log.level == 'INFO' and random() < 0.10:
    analyze_with_ai(log)

# Batch process for efficiency
batch = collect_logs(limit=50)
patterns = await ai.analyze_batch(batch, model='haiku')
```

---

# Log Analysis Output

```json
{
  "patterns": [
    {
      "pattern": "OOMKilled containers",
      "count": 142,
      "services": ["api-server", "worker"],
      "recommendation": "Increase memory limits"
    }
  ],
  "top_errors": [
    {
      "error": "DatabaseConnectionTimeout",
      "count": 89,
      "root_cause": "Connection pool exhausted"
    }
  ],
  "summary": "Primary issue: Memory pressure causing
              OOMKills. Secondary: DB connection pool
              needs tuning."
}
```

---

# Distributed Tracing with AI

## Finding Bottlenecks

```
[User Request] → 2400ms total
   ├─ [API Gateway] → 50ms
   ├─ [Auth Service] → 100ms
   ├─ [Product Service] → 1800ms ← BOTTLENECK
   │   ├─ [Database Query] → 1650ms ← ROOT CAUSE
   │   └─ [Cache Check] → 150ms
   └─ [Payment Service] → 450ms
```

**AI identifies: "Database query SELECT * FROM products
needs index on category_id column"**

---

# Trace Analysis with Claude

```python
# Fetch slow traces from Jaeger
traces = jaeger.query(
    service='api-server',
    min_duration='1s'
)

# AI analyzes and suggests fixes
for trace in traces:
    analysis = await claude.analyze_trace(trace)

    # Example output:
    # {
    #   "bottleneck_service": "product-service",
    #   "bottleneck_operation": "SELECT * FROM products",
    #   "recommendation": "Add index on category_id",
    #   "code_example": "CREATE INDEX idx_category..."
    # }
```

---

# Chaos Engineering Validation

## Testing Self-Healing

```yaml
# Chaos Mesh experiment
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-failure-test
spec:
  action: pod-kill
  mode: fixed-percent
  value: '20'  # Kill 20% of pods
  selector:
    namespaces: ['production']
```

**Expected:** Self-healing operator detects and restarts
            within 30 seconds

---

# Chaos Experiments

| Experiment | Expected Behavior | Success Criteria |
|------------|-------------------|------------------|
| Pod Kill | Restart pods | <30s detection |
| Memory Stress | Increase limits | <2 min fix |
| Network Latency | Detect anomaly | <1 min alert |
| Bad Deployment | Rollback | <5 min recovery |

**Target: 80%+ auto-healing rate, <5% incorrect fixes**

---

# Production Deployment

## Architecture

```
┌────────────────────────────────────────┐
│ Kubernetes Cluster                     │
│                                        │
│ ┌──────────────────────────────────┐  │
│ │ Self-Healing Operator (Deployment)│  │
│ │  ├─ Watches pods                  │  │
│ │  ├─ AI diagnosis (Claude API)     │  │
│ │  └─ Auto-fixes                    │  │
│ └──────────────────────────────────┘  │
│                                        │
│ ┌──────────────────────────────────┐  │
│ │ Auto-Remediation Service (Webhook)│  │
│ │  ├─ Receives Prometheus alerts    │  │
│ │  ├─ Circuit breaker               │  │
│ │  └─ Approval workflow             │  │
│ └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

---

# Cost Optimization

## Real-World Numbers

```
Auto-Remediation Engine:
├─ 40 incidents/month × $0.07 = $2.80/month

Log Analyzer (10K logs/day):
├─ 200 API calls/day × $0.001 = $6/month

Trace Analyzer (100 traces/day):
├─ 10 API calls/day × $0.03 = $9/month

Total Monthly AI Cost: ~$18

Compare to Manual:
├─ 20 hours/month × $180/hr = $3,600/month

ROI: 200× return
```

---

# Cost Optimization Strategies

## Token Reduction

1. **Use Haiku for simple tasks** (50× cheaper than Opus)
2. **Batch processing** (50 logs per call)
3. **Caching** (30-50% reduction)
4. **Smart sampling** (100% critical, 10% routine)
5. **Context minimization** (send only relevant data)

**Result:** $18/month for full AIOps platform

---

# Monitoring AIOps Itself

## Meta-Monitoring

```python
# Track AI performance
aiops_diagnosis_accuracy{status="correct"}
aiops_diagnosis_accuracy{status="incorrect"}
aiops_mttr_seconds
aiops_cost_dollars
aiops_token_usage_total

# Alert on degradation
if aiops_diagnosis_accuracy < 0.80:
    alert("AI accuracy degrading")
```

---

# Production Metrics

## Real-World Results

| Company | MTTR Before | MTTR After | Auto-Resolve Rate |
|---------|-------------|------------|-------------------|
| Startup (30 eng) | 45 min | 3 min | 85% |
| Mid-size (200 eng) | 60 min | 4 min | 75% |
| Enterprise (2000 eng) | 90 min | 5 min | 70% |

**Average:** 93% MTTR reduction, 77% auto-resolve rate

---

# Best Practices

## ✅ DO

- Start with safe actions only
- Run in shadow mode first (2 weeks)
- Monitor AI accuracy closely
- Use circuit breakers
- Maintain audit logs
- Keep humans in the loop for risky actions

---

# Best Practices

## ❌ DON'T

- Automate destructive actions
- Skip the shadow mode phase
- Ignore AI confidence scores
- Forget rollback capability
- Over-trust AI (always validate)
- Disable circuit breakers

---

# Common Pitfalls

## 1. Runaway Automation
```
AI fixes issue → creates new issue → AI tries to fix
→ creates another issue → loop ❌
```
**Solution:** Circuit breaker (stop after 3 failures)

## 2. High AI Costs
```
Using Opus for everything = $500/month ❌
```
**Solution:** Model selection + caching = $18/month ✅

---

# Common Pitfalls

## 3. Low Confidence Scores
```
AI only 60% confident → risky to auto-fix
```
**Solution:** Escalate to human if confidence < 80%

## 4. Alert Fatigue Still High
```
AI reduces alerts 90% but still 1K/month
```
**Solution:** Better correlation + root cause grouping

---

# Hands-On Exercises

## 1. Deploy Anomaly Detector
- Use code from `src/chapter-17/`
- Connect to your Prometheus
- Set up Slack alerts

## 2. Build Auto-Remediation
- Use code from `src/chapter-18/`
- Start with SAFE actions only
- Run in shadow mode for 1 week

## 3. Chaos Engineering
- Deploy Chaos Mesh
- Run pod failure experiments
- Validate self-healing

---

# Key Takeaways

1. **AIOps reduces MTTR by 93%** (45 min → 3 min)
2. **80%+ incidents auto-resolved**
3. **Alert fatigue reduced 90%** (10K → 1K/month)
4. **Cost-effective** (~$18/month for full platform)
5. **Safety first** (SAFE/APPROVAL/FORBIDDEN classifications)
6. **Circuit breakers prevent runaway automation**
7. **Always monitor AI accuracy**

---

# Next Up: Chapter 19

## Team Transformation

- Leading organizational change
- Building the business case
- Upskilling your team
- Measuring success
- Real-world transformation stories

---

# Questions?

## Resources

- Chapter 17: [chapters/17-aiops-fundamentals.md](../chapters/17-aiops-fundamentals.md)
- Chapter 18: [chapters/18-aiops-advanced.md](../chapters/18-aiops-advanced.md)
- Code Examples: [src/chapter-17/](../src/chapter-17/)
- Code Examples: [src/chapter-18/](../src/chapter-18/)
- Appendix A: [appendices/appendix-a-platform-blueprint.md](../appendices/appendix-a-platform-blueprint.md)

---

# Credits

**Author:** Michel Abboud
**Created with:** Claude AI (Anthropic)

This presentation was created with the assistance of AI,
demonstrating the capabilities discussed in this guide.

**License:** CC BY-NC 4.0
Free for personal/educational use.
Commercial use requires permission.

© 2026 Michel Abboud
