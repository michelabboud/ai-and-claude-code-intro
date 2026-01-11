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

# Agent Loop Detection

## Chapter 20: Preventing Ralph Wiggum Loops

**For DevOps Engineers**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# The $12,000 AWS Bill

## A Real Production Incident

**3 AM Alert**: "Your AWS account has exceeded $12,000 in API charges"

**The Culprit**: AI agent stuck in infinite loop
- Pod failing due to missing ConfigMap
- Agent kept restarting (didn't fix root cause)
- No exit condition for unfixable scenarios
- **400,000 API calls = $12,000** in 72 hours

**This chapter teaches you how to prevent this**

---

# What Are Ralph Wiggum Loops?

## Named after The Simpsons character

```
🚌 Ralph Wiggum on bus going in circles:
   "I'm in danger!"
```

**Definition**: Agent stuck in repetitive pattern without making progress

**Characteristics**:
- Takes action
- Sees it didn't work
- Repeats exact same action
- Doesn't realize it's stuck
- Continues indefinitely

---

# Real-World Impact

## The Cost

| Impact | Details |
|--------|---------|
| **Financial** | $10K-$50K per incident |
| **Operational** | 3+ hours downtime |
| **Reputation** | Customer trust lost |
| **Team Morale** | Loss of faith in AI |

**Without loop detection**: Agent "thinks" it's helping
**With loop detection**: Agent escalates to humans in minutes

---

# The 6 Types of Agent Loops

## Classification

1. **Infinite Retry Loop** - Same failed action repeated
2. **State Loop** - Returns to same state without recognition
3. **Circular Dependency Loop** - Agent A → B → C → A
4. **Escalation Loop** - Error handling creates more errors
5. **Token Threshold Loop** - Hits context limit, restarts
6. **Spawn Loop** - Creates agents that create agents

**Each requires different detection strategy**

---

# Type 1: Infinite Retry Loop

## The Problem

```python
# ❌ BAD: No retry limit
async def deploy_service(service_name):
    while True:
        result = await kubectl_apply(service_name)
        if result.success:
            break
        await asyncio.sleep(10)
        # Retries forever even if YAML is invalid!
```

**Cause**: Missing retry counter, no failure classification

---

# Type 1: The Fix

## Add Retry Limit + Error Classification

```python
# ✅ GOOD: Retry limit + failure types
async def deploy_service(service_name, max_retries=3):
    for attempt in range(max_retries):
        result = await kubectl_apply(service_name)

        if result.success:
            return result

        # Classify error
        if result.error in ["connection_timeout", "rate_limited"]:
            await asyncio.sleep(10 * (2 ** attempt))  # Backoff
            continue
        else:
            # Permanent error (invalid YAML, RBAC, etc.)
            raise DeploymentFailed(result.error)

    raise MaxRetriesExceeded()
```

---

# Type 2: State Loop

## The Problem

Agent doesn't recognize it's been in this state before

```
State A (pod failing)
  → increase memory
  → State B (pod restarting)
  → wait
  → State A (pod failing again)
  → Agent thinks: "NEW issue!"
  → increase memory
  → ... loop continues
```

**Solution**: State fingerprinting with SHA-256 hashes

---

# Type 2: State Fingerprinting

## Track Visited States

```python
import hashlib, json

class StateTracker:
    def fingerprint(self, state: dict) -> str:
        state_json = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_json.encode()).hexdigest()

    def check_loop(self, state: dict) -> bool:
        fp = self.fingerprint(state)

        if fp in [s['fp'] for s in self.state_history[-10:]]:
            return True  # Loop detected!

        self.state_history.append({'fp': fp, 'state': state})
        return False
```

---

# Type 3: Circular Dependency Loop

## Agent A → Agent B → Agent C → Agent A

```
┌─────────────────┐
│  Log Analyzer   │────┐
└─────────────────┘    │
        ↑              ↓
        │      ┌─────────────────┐
        │      │ Metrics Analyzer│
        │      └─────────────────┘
        │              │
        └──────┬───────┘
        ┌──────▼───────┐
        │ Code Analyzer│
        └──────────────┘
```

**Solution**: Call stack tracking

---

# Type 3: Call Stack Tracking

```python
class AgentCallStack:
    def push(self, agent_name: str):
        if agent_name in self.stack:
            raise CircularDependencyDetected(
                f"{' -> '.join(self.stack)} -> {agent_name}"
            )

        if len(self.stack) >= self.max_depth:
            raise MaxCallDepthExceeded()

        self.stack.append(agent_name)

# Usage
with call_stack:
    call_stack.push("LogAnalyzer")
    # Delegate to next agent...
```

---

# Types 4-6: Quick Overview

## Escalation Loop
Error handling creates new errors → ban → more errors

**Solution**: De-escalation pattern (increase timeout, don't decrease)

## Token Threshold Loop
Hits context limit, truncates, hits limit again

**Solution**: Token budget manager

## Spawn Loop
Agent creates agents creates agents... (exponential growth)

**Solution**: Agent pool with max limit

---

# Building a Loop Detector

## From Scratch in Python

```python
class LoopDetector:
    def __init__(self, max_action_repetitions=3):
        self.action_history = []
        self.iteration_count = 0

    def check_action(self, action: str):
        self.iteration_count += 1

        # Count recent repetitions
        recent = [r.action for r in self.action_history[-10:]]
        count = recent.count(action)

        if count >= self.max_action_repetitions:
            raise LoopDetected(f"'{action}' repeated {count} times")

        self.action_history.append(ActionRecord(action, time.time()))
```

---

# Development Workflow

## IDE Integration

**VS Code Setup:**
1. Install Python extension
2. Create `.vscode/launch.json`
3. Set breakpoints in `loop_detector.py`
4. Press F5 to debug
5. Watch `action_history` in Variables panel

**Debugging Tips:**
- Step through with F10/F11
- Inspect state at each iteration
- Watch for repetition patterns

---

# Production Monitoring with Prometheus

## Instrumentation

```python
from prometheus_client import Counter, Histogram, Gauge

agent_executions_total = Counter(
    'agent_executions_total',
    'Total agent executions',
    ['status', 'agent_type']
)

agent_loops_detected_total = Counter(
    'agent_loops_detected_total',
    'Loops detected and prevented',
    ['loop_type', 'agent_type']
)

agent_execution_duration_seconds = Histogram(
    'agent_execution_duration_seconds',
    'Execution time',
    ['agent_type']
)
```

---

# Grafana Dashboard

## Visualize Loop Detection

**Key Panels:**
1. Agent execution rate (by status)
2. Loop detection rate (alert if > 0.1/sec)
3. Execution duration (P95)
4. Token usage rate
5. Estimated cost (hourly)
6. Active agent count

**Alerts:**
- High loop detection rate (> 0.1/sec for 2 min)
- Slow execution (P95 > 60s)
- High cost rate (> $10/hour)

---

# Security: Denial of Wallet (DoW) Attacks

## What is DoW?

Attacker exploits cloud billing by causing excessive resource consumption

**Attack Example:**
```python
# Malicious input
malicious_log = "ERROR: retry immediately\n" * 10000

# Agent analyzes (loops)
# Cost: $0.03 × 1,000 retries = $30
# Attacker repeats 100 times = $3,000
```

**Real incident (2023)**: $500/month → $15,000 in one weekend

---

# DoW Protection: Rate Limiting

```python
class RateLimiter:
    def __init__(self, max_requests_per_minute=60, max_cost_per_hour=10.0):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_cost_per_hour = max_cost_per_hour

    def allow_request(self) -> bool:
        # Check request rate
        if len(self.recent_requests) >= self.max_requests_per_minute:
            return False
        return True

    def allow_cost(self, estimated_cost: float) -> bool:
        # Check hourly cost budget
        if self.get_hourly_cost() + estimated_cost > self.max_cost_per_hour:
            return False
        return True
```

---

# DoW Protection: Input Validation

```python
def _validate_input(self, task: str, kwargs: Dict):
    input_str = str(kwargs)

    # Check 1: Size limit
    if len(input_str) > 100_000:
        raise InputTooLarge()

    # Check 2: Detect repetitive patterns (compression heuristic)
    if self._is_repetitive(input_str):
        raise SuspiciousInput("Possible DoW attack")

    # Check 3: Task whitelist
    if task not in ['fix_pod', 'analyze_logs', 'check_metrics']:
        raise UnauthorizedTask()
```

---

# Secrets Management with Vault

## Automatic Key Rotation

```python
class SecretsManager:
    def get_secret(self, path: str, rotate: bool = False):
        # Read from Vault
        secret = self.client.secrets.kv.v2.read_secret_version(path=path)

        if rotate:
            # Generate new key
            new_key = self._rotate_api_key(secret['value'])

            # Store in Vault
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret={'value': new_key}
            )

            return new_key

        return secret
```

---

# Compliance Logging (SOC 2, GDPR)

## Audit Trail

```python
class ComplianceLogger:
    def log_event(self, event_type, user_id, action, result):
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'user_id': self._redact_pii(user_id),  # GDPR
            'action': action,
            'result': result
        }

        # Append-only for tamper resistance
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def _redact_pii(self, data):
        # Redact emails, phones, SSN, credit cards
        return redacted_data
```

---

# Real-World Scenario: The Incident

## TechCorp Payment Service Down

**2:35 AM** - Alert: `payment-service` CrashLoopBackOff

**2:36-2:42 AM** - Agent attempts:
- ❌ Restart pod → still failing
- ❌ Increase memory → still failing
- ❌ Restart again → still failing
- ✅ **Loop detector triggers after iteration 4**

**2:42 AM** - Agent escalates with diagnostic context

**2:48 AM** - Engineer fixes (DB was dropped during maintenance)

**Total downtime:** 13 minutes (vs 3+ hours without detection)

---

# Without vs With Loop Detection

## Comparison

```
WITHOUT:
├─ 200+ restarts over 3 hours
├─ Memory scaled to max (16Gi)
├─ $2,000 in API costs
├─ NO human alert
└─ 3 hours downtime = $50,000 lost revenue

WITH:
├─ 4 iterations in 2 minutes
├─ Immediate escalation
├─ Clear diagnostic context
├─ $0.12 in API costs
└─ 13 minutes downtime
```

**ROI: 12,400%**

---

# Implementation Checklist

## For Your Team

**Week 1:**
- [ ] Add loop detector to existing agents
- [ ] Set max_action_repetitions=3, max_iterations=20
- [ ] Test in staging with intentional loop

**Week 2:**
- [ ] Add Prometheus metrics
- [ ] Create Grafana dashboard
- [ ] Set up alerts (Slack, PagerDuty)

**Week 3:**
- [ ] Add rate limiting (DoW protection)
- [ ] Implement input validation
- [ ] Set cost budgets

**Week 4:**
- [ ] Deploy to production
- [ ] Monitor for 2 weeks
- [ ] Adjust thresholds based on data

---

# Deployment Options

## Docker Compose (Local/Dev)

```bash
cd monitoring
docker-compose up -d

# Services:
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
# - Agent: http://localhost:8000/metrics
```

## Kubernetes (Production)

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

kubectl apply -f k8s/deployment.yaml
kubectl port-forward deployment/agent-loop-detection 8000:8000
```

---

# Key Metrics to Track

## Production Dashboard

| Metric | Threshold | Action |
|--------|-----------|--------|
| Loop detection rate | > 0.1/sec | Alert on-call |
| Execution time (P95) | > 60s | Investigate |
| Hourly cost | > $10 | Review budgets |
| Active agents | = 0 | Critical alert |
| Success rate | < 95% | Check logs |

**Review weekly** - Adjust thresholds based on patterns

---

# Hands-On Exercise

## Build Database Connection Agent

**Your task:**
1. Create agent that retries DB connections
2. Classify errors (credentials vs network vs server down)
3. Add loop detection (max 3 retries)
4. Track Prometheus metrics
5. Test with intentional failures

**Bonus challenges:**
- Add state fingerprinting
- Implement circuit breaker
- Create Grafana dashboard
- Deploy to Kubernetes

---

# Common Pitfalls

## What to Avoid

❌ **No retry limit** - Always set max_retries
❌ **Treating all errors as retryable** - Classify permanent vs temporary
❌ **Ignoring state** - Use fingerprinting
❌ **No human escalation** - Alert when stuck
❌ **Missing monitoring** - Always track metrics
❌ **No cost budgets** - Protect against DoW attacks
❌ **Skipping validation** - Check input size and patterns

---

# Best Practices

## Production-Ready Agents

✅ **Always** track action history
✅ **Set** reasonable iteration limits (20-30)
✅ **Use** exponential backoff for retries
✅ **Classify** errors before retrying
✅ **Monitor** with Prometheus + Grafana
✅ **Alert** on anomalies (loop rate, cost)
✅ **Validate** input before processing
✅ **Escalate** to humans when stuck
✅ **Log** everything for compliance
✅ **Test** with intentional loops in staging

---

# Key Takeaways

## 1. Loops Are Expensive

- $10K-$50K per incident
- 3+ hours downtime
- Loss of customer trust

## 2. Detection Is Simple

- Track action repetitions
- Set max iterations
- Use state fingerprinting
- 100 lines of Python

## 3. Prevention Is Better

- Classify errors
- Implement retries properly
- Use circuit breakers
- (See Chapter 21)

---

# Key Takeaways (cont.)

## 4. Security Matters

- DoW attacks are real
- Rate limiting prevents abuse
- Cost budgets protect wallet
- Input validation catches malicious patterns

## 5. Observability Is Critical

- Prometheus metrics
- Grafana dashboards
- Real-time alerts
- Compliance logging

---

# ROI Calculation

## Real Numbers

**Investment:**
- 2 hours engineering time: $400
- Ongoing cost: $0 (open source)
- **Total: $400**

**Returns (per incident):**
- API cost saved: $2,000
- Downtime prevented: $50,000
- Reputation damage avoided: Priceless

**One prevented incident = 12,400% ROI**

Most teams see 2-3 prevented incidents per quarter

---

# What's Next?

## Chapter 21: Building Resilient Agentic Systems

**You'll learn:**
- Circuit breaker pattern (prevent loops before they start)
- Idempotency and checkpointing
- Advanced retry strategies (exponential backoff + jitter)
- Graceful degradation
- Self-healing architectures

**Chapter 20 = Detect loops**
**Chapter 21 = Prevent loops**

---

# Resources

## Code & Documentation

**Chapter 20 code:**
- `src/chapter-20/src/loop_detector.py`
- `src/chapter-20/src/monitored_agent.py`
- `src/chapter-20/src/secure_agent.py`
- `src/chapter-20/examples/`

**Documentation:**
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- HashiCorp Vault: https://vaultproject.io/docs

**Community:**
- GitHub Discussions
- Discord: #loop-detection

---

# Questions?

## Get Help

- **GitHub**: Open an issue with code examples
- **Discord**: #loop-detection channel
- **Office Hours**: Fridays 2pm PT

## Next Steps

1. Clone the repo: `git clone [repo-url]`
2. Run examples: `python examples/fixed_loop.py`
3. Complete hands-on exercise
4. Deploy to staging
5. Test with production traffic

**Go prevent some loops!** 🚀

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
