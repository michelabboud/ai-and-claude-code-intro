# Incident Response Prompt Template

Use this template when investigating production incidents.

## Quick Start

Copy and paste this template, filling in the bracketed sections:

```
I have a production incident. Help me analyze:

## Symptoms
- Service: [SERVICE NAME]
- Error type: [500 errors / latency / availability / etc.]
- Started at: [TIME in UTC]
- Percentage affected: [X% of requests]
- User impact: [DESCRIPTION]

## Current Metrics
- Error rate: [X%]
- Latency p99: [Xms]
- CPU usage: [X%]
- Memory usage: [X%]

## Recent Changes
[List any deployments, config changes, or infrastructure changes in last 24h]

## Logs
```
[PASTE RELEVANT LOGS HERE - last 50-100 lines of errors]
```

## What I've Tried
1. [ACTION] - [RESULT]
2. [ACTION] - [RESULT]

## Questions
1. What is the most likely root cause?
2. What additional data should I collect?
3. What are the immediate mitigation options?
4. What's the recommended fix?
```

---

## Detailed Template

For complex incidents, use this expanded version:

```
# Incident Investigation Request

## 1. Incident Summary
**Severity**: [P1 - Critical / P2 - High / P3 - Medium / P4 - Low]
**Status**: [Investigating / Identified / Monitoring / Resolved]
**Service(s)**: [Affected services]
**Started**: [YYYY-MM-DD HH:MM UTC]
**Duration**: [How long has it been ongoing]

## 2. Impact Assessment
- **Users affected**: [Number or percentage]
- **Functionality impact**: [What's not working]
- **Business impact**: [Revenue, SLAs, etc.]
- **Downstream effects**: [Other services affected]

## 3. Symptoms
- Primary symptom: [DESCRIPTION]
- Secondary symptoms:
  - [SYMPTOM 1]
  - [SYMPTOM 2]

## 4. Timeline of Events
| Time (UTC) | Event |
|------------|-------|
| HH:MM | [First symptom observed] |
| HH:MM | [Alert fired] |
| HH:MM | [Action taken] |

## 5. Metrics Snapshot
### Error Rates
- Current: X%
- Normal baseline: X%
- Trend: [Increasing / Stable / Decreasing]

### Latency
- p50: Xms (normal: Xms)
- p95: Xms (normal: Xms)
- p99: Xms (normal: Xms)

### Resources
- CPU: X% (normal: X%)
- Memory: X% (normal: X%)
- Disk I/O: [Normal / Elevated]
- Network: [Normal / Elevated]

## 6. Recent Changes (Last 48h)
### Deployments
| Time | Service | Version | Change Description |
|------|---------|---------|-------------------|
| | | | |

### Configuration Changes
| Time | System | Change |
|------|--------|--------|
| | | |

### Infrastructure Changes
| Time | Change |
|------|--------|
| | |

## 7. Logs and Traces

### Error Logs (Last 100 lines)
```
[PASTE ERROR LOGS]
```

### Stack Traces
```
[PASTE RELEVANT STACK TRACES]
```

### Distributed Traces
- Trace ID: [ID]
- Observations: [What the trace shows]

## 8. Diagnostics Already Run

| Check | Command | Result |
|-------|---------|--------|
| Pod status | kubectl get pods | [RESULT] |
| Pod logs | kubectl logs [pod] | [SUMMARY] |
| DB connections | [command] | [RESULT] |
| External deps | [command] | [RESULT] |

## 9. Hypotheses
Based on the data, potential causes:
1. [HYPOTHESIS 1] - Evidence: [WHY YOU THINK THIS]
2. [HYPOTHESIS 2] - Evidence: [WHY YOU THINK THIS]

## 10. Questions for AI Analysis

1. **Root Cause Analysis**
   - What does the log pattern suggest?
   - Which hypothesis is most likely correct?
   - What correlations should we investigate?

2. **Immediate Actions**
   - What's the fastest way to restore service?
   - Should we rollback the recent deployment?
   - Do we need to scale resources?

3. **Additional Diagnostics**
   - What other logs/metrics should we check?
   - What commands would help narrow down the cause?

4. **Mitigation Options**
   - Option A: [IDEA] - Pros/Cons?
   - Option B: [IDEA] - Pros/Cons?

5. **Prevention**
   - How do we prevent this from recurring?
   - What monitoring would have caught this earlier?
```

---

## Example Filled Template

```
I have a production incident. Help me analyze:

## Symptoms
- Service: payment-api
- Error type: 503 Service Unavailable
- Started at: 2024-01-15 14:32 UTC
- Percentage affected: ~30% of payment requests
- User impact: Users unable to complete checkout

## Current Metrics
- Error rate: 28% (normal: <1%)
- Latency p99: 12000ms (normal: 500ms)
- CPU usage: 45% (normal)
- Memory usage: 78% (elevated from 60%)

## Recent Changes
- 14:15 UTC: Deployed payment-api v2.4.1 (added new payment provider)
- No infrastructure changes
- No config changes

## Logs
```
2024-01-15 14:32:01 ERROR Connection pool exhausted - max connections: 50
2024-01-15 14:32:01 ERROR Timeout waiting for connection after 10000ms
2024-01-15 14:32:02 ERROR Failed to process payment: connection timeout
2024-01-15 14:32:03 WARN Queue depth: 847 (threshold: 100)
2024-01-15 14:32:05 ERROR Circuit breaker OPEN for payment-provider-api
```

## What I've Tried
1. Restarted pods - No improvement, errors returned after 2 minutes
2. Increased replicas from 3 to 5 - Slight improvement but still 20% errors

## Questions
1. What is the most likely root cause?
2. What additional data should I collect?
3. What are the immediate mitigation options?
4. What's the recommended fix?
```

---

## Follow-up Prompts

After initial analysis, use these follow-up prompts:

```
# Dive deeper into specific area
"Analyze the connection pool exhaustion issue in more detail.
What would cause this after the v2.4.1 deployment?"
```

```
# Get specific commands
"What kubectl commands should I run to investigate the
connection pool issue on the payment-api pods?"
```

```
# Generate fix
"Generate a fix for the connection pool configuration.
Current settings are in this ConfigMap: [PASTE CONFIG]"
```

```
# Create runbook entry
"Based on this incident, create a runbook entry for
'Payment API Connection Pool Exhaustion' with:
- Symptoms to identify
- Diagnostic steps
- Resolution steps
- Prevention measures"
```

```
# Draft incident summary
"Draft a customer-facing incident summary for this issue.
Include: what happened, impact, resolution, prevention."
```
