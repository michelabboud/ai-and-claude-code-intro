---
marp: true
theme: default
paginate: true
backgroundColor: #1e1e1e
color: #ffffff
---

<!-- _class: lead -->

# Chapters 21-22

# Resilient Agentic Systems

## Part 1: Resilience Patterns | Part 2: Production Deployment

### AI and Claude Code Guide for DevOps Engineers

---

## Chapter Overview

**Prevention > Detection**

- Chapter 20: **Detect** Ralph Wiggum loops when they happen
- Chapters 21-22: **Prevent** loops by designing resilient systems

**6 Resilience Patterns Across Two Chapters:**

**Chapter 21 (Core Patterns):**
1. Circuit Breaker
2. Idempotency
3. State Checkpointing

**Chapter 22 (Advanced Patterns):**
4. Exponential Backoff + Jitter
5. Graceful Degradation
6. Self-Healing

---

## The Problem: Cascading Failures

**Without resilience patterns:**

```python
async def fix_pod():
    status = await check_pod()      # ❌ Fails
    if status == "CrashLoopBackOff":
        await restart_pod()          # ❌ Fails
        await check_pod()            # ❌ Fails
        # Repeats forever... 💸
```

**Result:** $12K AWS bill from infinite retry loop

---

## Pattern 1: Circuit Breaker

**Prevent cascading failures**

### Three States

| State | Behavior |
|-------|----------|
| **CLOSED** | Normal operation, requests pass through |
| **OPEN** | Fail fast, reject requests immediately |
| **HALF_OPEN** | Test if service recovered |

**When to Open:** After N consecutive failures (e.g., 5)
**When to Close:** After N successful attempts in half-open (e.g., 2)

---

## Circuit Breaker Implementation

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.timeout = timeout  # Seconds before trying half-open

    async def call(self, func, *args):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Service unavailable")

        try:
            result = await func(*args)
            self._on_success()  # Reset failures
            return result
        except Exception:
            self._on_failure()  # Increment failures, maybe open
            raise
```

---

## Circuit Breaker: Real-World Example

**Netflix Hystrix Pattern:**

```python
# Protect external API calls
breaker = CircuitBreaker(failure_threshold=3, timeout=30)

async def call_payment_api():
    return await breaker.call(
        stripe_api.charge,
        amount=100,
        currency='usd'
    )
```

**Result:**
- Service down → Circuit opens after 3 failures
- Prevents 1000s of wasted API calls
- Automatic recovery testing after 30 seconds

---

## Pattern 2: Exponential Backoff + Jitter

**Retry without overwhelming the system**

### The Problem: Thundering Herd

**Without jitter:**
- 1000 clients fail at t=0
- All retry at t=5s → **Synchronized storm**
- All retry at t=10s → **Another storm**

**With exponential backoff + jitter:**
- Retries spread out randomly
- No synchronized traffic spikes
- Smooth recovery curve

---

## Exponential Backoff Implementation

```python
import random

async def retry_with_backoff(func, max_retries=5):
    base_delay = 1  # seconds
    max_delay = 32

    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt >= max_retries - 1:
                raise

            # Exponential backoff: 1, 2, 4, 8, 16, 32...
            exp_delay = min(base_delay * (2 ** attempt), max_delay)

            # Full jitter: random between 0 and exp_delay
            delay = random.uniform(0, exp_delay)

            await asyncio.sleep(delay)
```

---

## Jitter Types Comparison

| Type | Formula | Use Case |
|------|---------|----------|
| **None** | `delay` | ❌ Don't use (thundering herd) |
| **Full** | `random(0, delay)` | ✅ Best for high concurrency |
| **Equal** | `delay/2 + random(0, delay/2)` | Guarantees minimum wait |
| **Decorrelated** | `random(base, prev_delay * 3)` | Smooth growth |

**AWS Recommendation:** Use **full jitter** for most scenarios

---

## Pattern 3: Idempotency

**Safe to retry without side effects**

### Mathematical Definition

> f(f(x)) = f(x)

**Applying twice gives same result as applying once**

---

## Idempotency Examples

### ❌ Not Idempotent

```python
async def restart_pod(pod_name):
    current_pods = await get_pod_count()
    await create_pod(pod_name)  # Creates duplicate if retried!
```

### ✅ Idempotent

```python
async def restart_pod(pod_name):
    # Check if action already completed
    action_id = hash(f"restart:{pod_name}")
    if action_id in completed_actions:
        return completed_actions[action_id]

    # Set to desired state (idempotent)
    await set_pod_desired_count(pod_name, 1)
    completed_actions[action_id] = True
```

---

## Idempotency Patterns

### Pattern 1: Check-Then-Act

```python
if not await exists():
    await create()
```

### Pattern 2: Absolute Values (Not Relative)

```python
# ✅ Good
await set_replicas(pod_name, 3)

# ❌ Bad
await increase_replicas(pod_name, +1)
```

### Pattern 3: Idempotency Keys

```python
await payment_api.charge(
    amount=100,
    idempotency_key='order-12345'  # Same key = same result
)
```

---

## Pattern 4: State Checkpointing

**Resume workflows after crashes**

### The Problem

```python
async def long_workflow():
    await step_1()  # Completes ✓
    await step_2()  # Completes ✓
    await step_3()  # 💥 CRASH
    # On restart: Re-runs step_1 and step_2 (wasted work)
```

### The Solution: Checkpoints

```python
async def long_workflow_with_checkpoints():
    checkpoint = load_checkpoint()

    if checkpoint.step < 1:
        await step_1()
        save_checkpoint(step=1)

    if checkpoint.step < 2:
        await step_2()
        save_checkpoint(step=2)

    if checkpoint.step < 3:
        await step_3()
        save_checkpoint(step=3)
```

---

## Checkpointing Implementation

```python
@dataclass
class Checkpoint:
    workflow_id: str
    step: int
    state: Dict[str, Any]
    timestamp: datetime

class CheckpointedAgent:
    def save_checkpoint(self, step: int):
        checkpoint = Checkpoint(
            workflow_id=self.workflow_id,
            step=step,
            state=self.state.copy(),
            timestamp=datetime.now()
        )
        # Save to disk/database
        with open(f'.checkpoint-{self.workflow_id}.json', 'w') as f:
            json.dump(asdict(checkpoint), f)

    def load_checkpoint(self) -> Optional[Checkpoint]:
        # Load from disk/database
        try:
            with open(f'.checkpoint-{self.workflow_id}.json', 'r') as f:
                data = json.load(f)
                return Checkpoint(**data)
        except FileNotFoundError:
            return None
```

---

## Pattern 5: Graceful Degradation

**Provide reduced functionality instead of complete failure**

### Philosophy

> "80% functionality with 100% uptime
> is better than
> 100% functionality with 80% uptime"

---

## Graceful Degradation Levels

| Level | Description | Example |
|-------|-------------|---------|
| **0: Full** | All features working | Fresh data from all services |
| **1: Slight** | Minor degradation | Some cached responses |
| **2: Moderate** | Partial functionality | Read-only mode |
| **3: Minimal** | Critical only | Static content |
| **4: Failed** | Unavoidable | Error page with status |

**Goal:** Never drop from level 0 directly to level 4

---

## Graceful Degradation Example

### ❌ All-or-Nothing

```python
async def get_incident_details(incident_id):
    metrics = await metrics_service.get(incident_id)  # ❌ Fails
    logs = await logs_service.get(incident_id)        # Never reached
    alerts = await alerts_service.get(incident_id)    # Never reached

    return {'metrics': metrics, 'logs': logs, 'alerts': alerts}
```

**If metrics service is down → Get NOTHING**

---

## Graceful Degradation Example

### ✅ Degraded Gracefully

```python
async def get_incident_details_graceful(incident_id):
    result = {'status': 'full', 'degraded_components': []}

    # Try metrics (with fallback to cache)
    try:
        result['metrics'] = await metrics_service.get(incident_id)
    except Exception:
        result['metrics'] = cache.get('metrics') or {'error': 'unavailable'}
        result['degraded_components'].append('metrics')
        result['status'] = 'degraded'

    # Try logs (fail gracefully)
    try:
        result['logs'] = await logs_service.get(incident_id)
    except Exception:
        result['logs'] = {'error': 'unavailable'}
        result['degraded_components'].append('logs')

    return result  # Still get what's available!
```

---

## Netflix Example: Graceful Degradation

**Recommendation Engine Fails:**

❌ **Bad:** Show error, user can't watch anything
✅ **Netflix:** Show "Popular Now" and "Recently Watched"

**Users barely notice the issue**

**Production Stats:**
- Monolithic: 99.9% uptime (8.7 hours downtime/year)
- Gracefully degraded: 99.99% uptime (52 minutes downtime/year)
- **10x reduction in revenue loss**

---

## Pattern 6: Self-Healing

**Automatically detect and recover from failures**

### Google Borg Example

**Automatic actions:**
- Pod crashes → Restart automatically
- Node fails → Reschedule pods to healthy nodes
- Health checks fail → Replace unhealthy instances
- Resource exhaustion → Evict low-priority workloads

**Result:** Millions of containers with minimal manual intervention

---

## Self-Healing Patterns

### Pattern 1: Health Checks + Auto-Restart

```python
async def agent_with_self_healing():
    consecutive_failures = 0
    max_failures = 5

    while True:
        if not await health_check():
            await self_heal()
            consecutive_failures += 1

            if consecutive_failures >= max_failures:
                await alert_humans()
                break
        else:
            consecutive_failures = 0  # Reset on success

        await process_work()
```

---

## Self-Healing Implementation

```python
class SelfHealingAgent:
    async def _health_check(self) -> HealthStatus:
        # Check memory, connections, response time, queue depth
        checks = {
            'memory': memory_percent < 90,
            'connectivity': await test_connectivity(),
            'response_time': avg_response_time < 1.0,
            'queue_depth': queue_size < 1000
        }

        if all(checks.values()):
            return HealthStatus.HEALTHY
        elif sum(checks.values()) >= len(checks) * 0.75:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.UNHEALTHY

    async def _attempt_self_heal(self):
        # Clear caches
        cache.clear()
        # Reset connections
        await db_pool.reset_all()
        # Reload configuration
        config.reload()
```

---

## Self-Healing: Production Stats

**Recovery Times:**

| Approach | MTTR (Mean Time To Recovery) |
|----------|------------------------------|
| Manual | 30 minutes |
| Semi-automated | 5 minutes |
| Fully self-healing | **30 seconds** |

**Cost Impact:**
- 60x faster recovery = 60x less downtime cost
- Reduced on-call burden
- Fewer human errors during recovery

---

## Combining All 6 Patterns

### Real-World Production Example

```python
class ProductionIncidentAgent:
    def __init__(self):
        # Pattern 1: Circuit breakers for external services
        self.datadog_circuit = CircuitBreaker()
        self.pagerduty_circuit = CircuitBreaker()

        # Pattern 2: Retry strategy with exponential backoff
        self.retry_strategy = RetryStrategy(jitter_type=JitterType.FULL)

        # Pattern 3: Idempotency tracking
        self.completed_actions = {}

        # Pattern 4: State checkpointing
        self.checkpoints = {}

        # Pattern 5: Graceful degradation caches
        self.metrics_cache = {}

        # Pattern 6: Self-healing state
        self.consecutive_failures = 0
```

---

## Production Workflow Example

```python
async def handle_incident(context):
    # Step 1: Gather context (graceful degradation)
    context.metrics = await self._get_metrics_with_fallback(context)

    # Step 2: Analyze (retry with backoff)
    context.logs = await self._retry_with_backoff(
        self._call_with_circuit_breaker,  # Circuit breaker
        self.datadog_circuit,
        self._fetch_logs
    )

    # Step 3: Apply fix (idempotent)
    await self._execute_idempotent(
        "restart_pods",
        context,
        self._restart_pods
    )

    # Save checkpoint after each step
    self._save_checkpoint(context)

    # Self-heal if failures accumulate
    if self.consecutive_failures >= 5:
        await self._self_heal()
```

---

## Hands-On Exercise

### Build a Database Migration Agent

**Requirements:**
1. Execute migrations idempotently
2. Checkpoint progress for crash recovery
3. Retry database connection failures
4. Degrade gracefully when monitoring unavailable
5. Circuit breaker for database connections
6. Self-heal when connection pool exhausted

**Starter code provided in chapter materials**

---

## Key Architectural Decisions

### Circuit Breaker Placement

✅ **Do:** Wrap ALL external service calls
- API calls (Datadog, PagerDuty, AWS)
- Database connections
- Network file operations

❌ **Don't:** Use for local operations
- File reads from local disk
- In-memory calculations
- Local function calls

---

## Production Configuration

### Circuit Breaker Tuning

```python
# Standard configuration
CircuitBreakerConfig(
    failure_threshold=5,      # Open after 5 failures
    success_threshold=2,       # Close after 2 successes
    timeout=60.0              # Try recovery after 60s
)

# High-traffic API
CircuitBreakerConfig(
    failure_threshold=10,     # More tolerance
    timeout=30.0              # Faster recovery attempts
)

# Critical service
CircuitBreakerConfig(
    failure_threshold=3,      # Fail fast
    timeout=120.0             # Conservative recovery
)
```

---

## Retry Strategy Tuning

```python
# User-facing operations (keep it fast)
RetryConfig(
    base_delay=0.5,
    max_delay=5.0,
    max_retries=2,
    max_total_wait_time=10.0  # Don't make users wait
)

# Background jobs (can wait longer)
RetryConfig(
    base_delay=2.0,
    max_delay=120.0,
    max_retries=5,
    exponential_base=3  # Grow faster: 2, 6, 18, 54s
)
```

---

## Monitoring Resilience Patterns

### Key Metrics to Track

```python
# Circuit breaker state
prometheus.gauge('circuit_breaker_state',
                 labels=['service'])

# Retry attempts
prometheus.counter('retry_attempts_total',
                    labels=['service', 'success'])

# Degradation level
prometheus.gauge('system_degradation_level')

# Self-healing actions
prometheus.counter('self_heal_attempts_total',
                    labels=['action', 'success'])

# Checkpoint saves
prometheus.counter('checkpoints_saved_total')
```

---

## Common Pitfalls

### 1. Circuit Breaker Stuck Open

**Problem:** Never closes even after service recovers

**Fix:**
- Reduce `timeout` value
- Lower `success_threshold`
- Improve health check accuracy

### 2. Excessive Retries

**Problem:** Overwhelming the system with retries

**Fix:**
- Add exponential backoff
- Set `max_retries` limit
- Implement retry budgets

---

## Common Pitfalls (cont.)

### 3. Non-Idempotent Operations

**Problem:** Retries create duplicates

**Fix:**
- Use absolute values (not relative)
- Implement check-then-act pattern
- Add idempotency keys

### 4. Stale Cached Data

**Problem:** Graceful degradation serving outdated info

**Fix:**
- Set appropriate cache TTL
- Display "cached data" warnings
- Implement cache invalidation

---

## Testing Resilience Patterns

### Chaos Engineering

**Netflix Chaos Monkey:**
- Randomly kills production instances
- Injects network latency
- Simulates service failures
- Verifies auto-recovery works

**Tools:**
- Chaos Monkey (AWS)
- Gremlin (multi-cloud)
- Pumba (Docker)
- Toxiproxy (network conditions)

---

## Testing Strategies

### 1. Unit Tests

```python
def test_circuit_opens_after_threshold():
    breaker = CircuitBreaker(failure_threshold=3)

    for i in range(3):
        with pytest.raises(ConnectionError):
            await breaker.call(failing_function)

    # Circuit should now be OPEN
    with pytest.raises(CircuitOpenError):
        await breaker.call(failing_function)
```

### 2. Integration Tests

- Test patterns working together
- Simulate real failure scenarios
- Verify recovery paths

---

## Summary: When to Use Each Pattern

| Situation | Recommended Pattern |
|-----------|-------------------|
| External API call | Circuit Breaker |
| Transient network failure | Exponential Backoff + Jitter |
| Database update | Idempotency |
| Long-running workflow | State Checkpointing |
| Multi-service system | Graceful Degradation |
| Production deployment | Self-Healing |

**Best Practice:** Use multiple patterns together for defense in depth

---

## Key Takeaways

1. **Prevention > Detection**
   - Design systems that can't loop
   - Chapter 20 = detect, Chapter 21 = prevent

2. **Defense in Depth**
   - Use multiple patterns together
   - Each pattern handles different failure modes

3. **Fail Gracefully**
   - Better to provide reduced functionality than complete failure
   - Netflix example: 99.99% uptime

4. **Human Escalation**
   - Always have a path to escalate
   - Set limits on automatic recovery

5. **Test Regularly**
   - Use chaos engineering
   - Verify resilience patterns work

---

## Next Steps

1. **Review Chapter 20** for loop detection techniques
2. **Complete the hands-on exercise**
   - Build database migration agent
   - Implement all 6 patterns

3. **Study production incidents**
   - Learn from real-world failures
   - AWS, Netflix, Google postmortems

4. **Implement in your agents**
   - Start with circuit breakers
   - Add patterns incrementally

5. **Set up monitoring**
   - Track all resilience metrics
   - Alert on pattern failures

---

## Resources

**Books:**
- *Release It!* by Michael Nygard
- *Site Reliability Engineering* by Google
- *Chaos Engineering* by Casey Rosenthal

**Articles:**
- AWS: Exponential Backoff and Jitter
- Netflix: Hystrix Documentation
- Google: Handling Overload

**Code:**
- `src/chapter-21/` - Core pattern implementations
- `chapters/22-production-deployment.md` - Advanced patterns
- Hands-on exercise starter code

---

<!-- _class: lead -->

# Questions?

## Chapters 21-22: Resilient Agentic Systems

### Ready to build production-ready AI agents that never loop!

---

<!-- _class: lead -->

# Thank You!

**Next:** Continue to advanced chapters or practice with hands-on exercises

**Feedback:** Help us improve this guide

**Connect:** Share your resilient agent implementations!

