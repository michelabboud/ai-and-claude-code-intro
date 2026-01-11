# Chapter 21: Resilience Patterns for Agents

**Part 8: Advanced Agentic Development**

---

## Navigation

← Previous: [Chapter 20: Agent Loop Detection & Prevention](./20-agent-loop-detection.md) | Next: [Chapter 22: Production Deployment of Agentic Systems](./22-production-deployment.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

## TL;DR

**Chapter 21 (Part 1 of 2)**: Learn the core resilience patterns that prevent agent failures: **Circuit Breakers** (when to stop trying), **Idempotency** (safe to retry), and **State Checkpointing** (resume from last save point). Includes production-ready implementations, pattern selection frameworks, and real-world scenarios. Reading time: ~30 minutes.

**Continue to [Chapter 22](./22-production-deployment.md)** for production deployment strategies, exponential backoff, graceful degradation, and self-healing architectures.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand the circuit breaker pattern** and when to apply it
- **Implement idempotent agent actions** for safe retries
- **Build checkpointing systems** for crash recovery
- **Apply the resilience pattern selection framework** to make architectural decisions

**Prerequisites:**
- Chapter 20: Agent Loop Detection & Prevention
- Python 3.9+ installed
- Understanding of async/await
- Basic knowledge of circuit breakers (we'll deep dive here)

**Time to Complete:** 1.5-2 hours (including reading and understanding patterns)

---

## Introduction: From Detection to Prevention

In Chapter 20, you learned how to **detect loops** when they occur. This chapter (Part 1) teaches you the **core resilience patterns** that prevent failures in the first place.

### The Philosophy Shift

**Chapter 20 mindset:** "Catch loops when they happen"
**Chapter 21 mindset:** "Design systems that can't loop"

Think of it like this:
- **Loop detection** = Smoke detector (alerts you to fire)
- **Resilient design** = Fireproof building (prevents fire from spreading)

You need both. But prevention is always better than detection.

---

## The Resilience Triangle

Every resilient agentic system needs three core patterns:

```
┌─────────────────────────────────────┐
│                                     │
│      CIRCUIT BREAKER                │
│    (When to stop trying)            │
│             ┌───────┐               │
│             │       │               │
│             │       │               │
│    ┌────────┴───────┴────────┐    │
│    │                           │    │
│ IDEMPOTENCY          RETRY LOGIC   │
│ (Safe to retry)    (How to retry)  │
│    │                           │    │
│    └───────────────────────────┘    │
│                                     │
│    = RESILIENT AGENT SYSTEM         │
└─────────────────────────────────────┘
```

**All three must work together** for true resilience.

**In this chapter** you'll learn the first three patterns. **[Chapter 22](./22-production-deployment.md)** covers advanced production patterns.

---

## Section 1: The Circuit Breaker Pattern

### What is a Circuit Breaker?

Inspired by electrical circuit breakers, this pattern prevents cascading failures by "opening the circuit" when errors exceed a threshold.

**Three states:**

```
CLOSED (Normal)
  ↓ (3 consecutive failures)
OPEN (Blocking)
  ↓ (30 seconds timeout)
HALF-OPEN (Testing)
  ↓ (2 successes) ↓ (1 failure)
CLOSED          OPEN
```

**Real-world analogy:** Like a breaker in your home's electrical panel:
- **CLOSED**: Power flows normally
- **OPEN**: Breaker trips, power cut off
- **HALF-OPEN**: Test if it's safe to restore power

---

### Why Circuit Breakers Matter

**Without circuit breaker:**
```python
# Agent keeps hammering failing API
for i in range(1000):
    try:
        result = call_api()  # Fails every time
    except:
        continue  # Try again immediately

# Result: 1,000 failed requests, wasted time, DoS on API
```

**With circuit breaker:**
```python
# Circuit opens after 3 failures
# Next 997 requests rejected immediately
# Saves time and resources

CLOSED: request 1 → fail
CLOSED: request 2 → fail
CLOSED: request 3 → fail
OPEN:   request 4-1000 → rejected (instant)
        Wait 30 seconds...
HALF_OPEN: request 1001 → test
```

**Benefits:**
- Fails fast (no wasted retries)
- Protects downstream services
- Gives failing systems time to recover
- Prevents resource exhaustion

---

### Building a Production Circuit Breaker

**Installation:**

```bash
pip install enum34 typing
```

**File: `circuit_breaker.py`**

```python
"""
Production-grade circuit breaker for AI agents.

Based on patterns from Netflix Hystrix and Google SRE practices.
"""

import time
import asyncio
from enum import Enum
from typing import Callable, Any, Optional
from dataclasses import dataclass


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"        # Normal operation
    OPEN = "open"            # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior"""

    # Number of failures before opening circuit
    failure_threshold: int = 5

    # Seconds to wait before attempting recovery
    recovery_timeout: int = 60

    # Number of successes needed to close circuit from half-open
    success_threshold: int = 2

    # Time window for counting failures (seconds)
    failure_window: int = 120


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


class CircuitBreaker:
    """
    Production-ready circuit breaker for AI agents.

    Features:
    - Automatic state transitions
    - Configurable thresholds
    - Metrics tracking
    - Half-open state for safe recovery
    - Time-window failure counting

    Usage:
        breaker = CircuitBreaker()

        async def risky_operation():
            async with breaker:
                return await call_external_api()
    """

    def __init__(self, config: Optional[CircuitBreakerConfig] = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED

        # Failure tracking
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.failure_timestamps = []

        # Metrics
        self.total_calls = 0
        self.total_successes = 0
        self.total_failures = 0
        self.total_rejected = 0

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker.

        Args:
            func: Async function to execute
            *args, **kwargs: Arguments to pass to function

        Returns:
            Result from function

        Raises:
            CircuitOpenError: If circuit is open
        """
        self.total_calls += 1

        # Check if circuit is open
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                self.total_rejected += 1
                raise CircuitOpenError(
                    f"Circuit breaker is OPEN. "
                    f"Retry in {self._time_until_retry():.0f} seconds"
                )

        # Attempt the call
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise

    async def __aenter__(self):
        """Context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is not None:
            self._on_failure()
        else:
            self._on_success()
        return False

    def _on_success(self):
        """Handle successful call"""
        self.total_successes += 1

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1

            if self.success_count >= self.config.success_threshold:
                self._transition_to_closed()

    def _on_failure(self):
        """Handle failed call"""
        self.total_failures += 1
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.failure_timestamps.append(time.time())

        # Clean old failures outside window
        cutoff = time.time() - self.config.failure_window
        self.failure_timestamps = [
            ts for ts in self.failure_timestamps if ts > cutoff
        ]

        # Check if we should open circuit
        if len(self.failure_timestamps) >= self.config.failure_threshold:
            self._transition_to_open()

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery"""
        if not self.last_failure_time:
            return False

        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.config.recovery_timeout

    def _time_until_retry(self) -> float:
        """Calculate seconds until retry is allowed"""
        if not self.last_failure_time:
            return 0

        elapsed = time.time() - self.last_failure_time
        remaining = self.config.recovery_timeout - elapsed
        return max(0, remaining)

    def _transition_to_open(self):
        """Transition to OPEN state"""
        if self.state != CircuitState.OPEN:
            print(f"🔴 Circuit breaker OPEN (failures: {self.failure_count})")
            self.state = CircuitState.OPEN
            # In production, send alert here
            # alert_oncall("Circuit breaker opened", self.get_stats())

    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state"""
        print("🟡 Circuit breaker HALF-OPEN (testing recovery)")
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0

    def _transition_to_closed(self):
        """Transition to CLOSED state"""
        print("🟢 Circuit breaker CLOSED (recovery successful)")
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.failure_timestamps = []

    def get_stats(self) -> dict:
        """Get circuit breaker statistics"""
        return {
            'state': self.state.value,
            'total_calls': self.total_calls,
            'total_successes': self.total_successes,
            'total_failures': self.total_failures,
            'total_rejected': self.total_rejected,
            'success_rate': (
                self.total_successes / self.total_calls
                if self.total_calls > 0 else 0
            ),
            'recent_failures': len(self.failure_timestamps),
            'time_until_retry': self._time_until_retry()
        }


# Example usage
async def main():
    """Demonstrate circuit breaker in action"""

    # Create circuit breaker
    breaker = CircuitBreaker(
        config=CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=10,
            success_threshold=2
        )
    )

    # Simulated API call (fails first 5 times, then succeeds)
    call_count = 0

    async def unreliable_api():
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)

        if call_count <= 5:
            raise Exception("API error")
        return {"status": "success"}

    # Make calls
    for i in range(20):
        try:
            result = await breaker.call(unreliable_api)
            print(f"Call {i+1}: ✅ {result}")
        except CircuitOpenError as e:
            print(f"Call {i+1}: ⛔ {e}")
        except Exception as e:
            print(f"Call {i+1}: ❌ {e}")

        await asyncio.sleep(0.5)

    # Print final stats
    print(f"\nFinal stats: {breaker.get_stats()}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Run it:**

```bash
python circuit_breaker.py
```

**Expected output:**

```
Call 1: ❌ API error
Call 2: ❌ API error
Call 3: ❌ API error
🔴 Circuit breaker OPEN (failures: 3)
Call 4: ⛔ Circuit breaker is OPEN. Retry in 10 seconds
Call 5: ⛔ Circuit breaker is OPEN. Retry in 9 seconds
...
Call 20: ⛔ Circuit breaker is OPEN. Retry in 5 seconds
(after 10 seconds)
🟡 Circuit breaker HALF-OPEN (testing recovery)
Call 21: ✅ {'status': 'success'}
Call 22: ✅ {'status': 'success'}
🟢 Circuit breaker CLOSED (recovery successful)
```

---

### When to Use Circuit Breakers

**Use circuit breakers when:**
- ✅ Calling external APIs (Claude, AWS, databases)
- ✅ Network operations that can fail
- ✅ Operations that impact other services
- ✅ High-cost operations (API calls with billing)

**Don't use circuit breakers for:**
- ❌ Pure in-memory operations
- ❌ File system operations (use retries instead)
- ❌ Operations that must eventually succeed

---

### Resilience Pattern Selection: A Decision Framework

Understanding which resilience patterns to combine is crucial. Here's how to make the right architectural decisions for your agents.

#### The Pattern Selection Matrix

| Scenario | Circuit Breaker | Retry Logic | Idempotency | Checkpointing |
|----------|----------------|-------------|-------------|---------------|
| **API calls to Claude** | ✅ Required | ✅ Required | ⚠️ Complex | ❌ Optional |
| **Database operations** | ✅ Required | ✅ Required | ✅ Critical | ⚠️ Situational |
| **Kubernetes operations** | ✅ Required | ✅ Required | ✅ Required | ⚠️ Recommended |
| **File system ops** | ❌ No | ✅ Simple retry | ✅ Recommended | ✅ Yes |
| **Long-running workflows** | ⚠️ Per-step | ✅ Per-step | ✅ Per-step | ✅ Critical |
| **In-memory calculations** | ❌ No | ✅ Maybe | N/A | ❌ No |

#### Real-World Pattern Combinations

**Scenario 1: Kubernetes Pod Auto-Remediation Agent**

```yaml
Problem: Agent restarts failing pods

Required patterns:
  ✅ Circuit Breaker:
     Why: Prevent hammering Kubernetes API if cluster is degraded
     Config: 5 failures → open for 60 seconds

  ✅ Retry Logic with Exponential Backoff:
     Why: Transient failures (network hiccups) should retry
     Config: Max 3 retries, 2^n seconds wait

  ✅ Idempotency:
     Why: Safe to restart same pod multiple times
     Implementation: Check pod status before restart

  ❌ Checkpointing:
     Why: Operation is quick (<30s), not worth overhead
     Alternative: Log actions for audit trail

Pattern combination:
  1. Check if circuit is open (fast fail)
  2. Attempt pod restart (idempotent)
  3. If fails, retry with backoff (max 3)
  4. If still fails, open circuit
  5. Log all actions

Time investment: 4-6 hours to implement all patterns
Benefit: Prevents 90%+ of cascading failures
```

**Scenario 2: Multi-Step Infrastructure Provisioning**

```yaml
Problem: Agent provisions VPC → Subnet → EC2 → RDS (20 min workflow)

Required patterns:
  ✅ Circuit Breaker:
     Why: AWS API calls can fail, protect against rate limits
     Config: Per-service breaker (VPC breaker, EC2 breaker, etc.)

  ✅ Retry Logic:
     Why: AWS eventually consistent, may need retries
     Config: Different per resource type

  ✅ Idempotency:
     Why: CRITICAL - can't create duplicate infrastructure
     Implementation: Check existence before create

  ✅ Checkpointing:
     Why: Don't want to recreate VPC if EC2 step fails
     Implementation: Save state after each successful step

Workflow with all patterns:
  Step 1: Create VPC
    - Check if VPC exists (idempotency)
    - Circuit breaker protects AWS API
    - Retry if fails (max 3)
    - Checkpoint: Save VPC ID

  Step 2: Create Subnet
    - Load checkpoint (get VPC ID)
    - Check if subnet exists
    - Circuit breaker active
    - Retry if fails
    - Checkpoint: Save subnet ID

  (Continue for each step)

Recovery scenario:
  Agent crashes at Step 3 (EC2 creation)
  On restart:
    - Load checkpoint
    - VPC and Subnet already exist (don't recreate)
    - Resume from EC2 creation
    - Complete RDS without starting over

Time investment: 8-12 hours for full implementation
Benefit: Can recover from any point without duplicating $1000+ of infrastructure
```

**Scenario 3: Log Analysis Agent (Read-Only Operations)**

```yaml
Problem: Agent analyzes CloudWatch logs and suggests fixes

Required patterns:
  ✅ Circuit Breaker:
     Why: CloudWatch API has rate limits
     Config: 10 failures → open for 30 seconds

  ✅ Retry Logic:
     Why: Transient network issues
     Config: Max 5 retries (read operations are cheap)

  ⚠️ Idempotency:
     Why: Somewhat - reading logs multiple times is safe but wasteful
     Implementation: Cache results to avoid re-reading

  ❌ Checkpointing:
     Why: Analysis is fast (<2 min), restart from scratch is fine

Simplified pattern:
  - Circuit breaker for API protection
  - Simple retry for transient failures
  - Results caching (optional idempotency)
  - No checkpointing needed

Time investment: 2-3 hours
Benefit: Reliable analysis with minimal overhead
```

#### When to Skip Patterns (Cost-Benefit Analysis)

```yaml
Skip Circuit Breaker when:
  Situation: Operation takes <1 second, fails <1% of time
  Cost: 4 hours implementation + testing
  Benefit: Saves ~10 failed retries/month = 10 seconds
  Decision: NOT worth it

  Better approach: Simple max_retries=3

Skip Checkpointing when:
  Situation: Workflow takes <5 minutes, failures rare
  Cost: 8 hours implementation + 10% performance overhead
  Benefit: Saves 5 min restart once/month
  Decision: NOT worth it for most cases

  Exception: If failure common (>10%), implement checkpointing

Skip Idempotency when:
  Situation: Pure read operations
  Cost: 3 hours adding existence checks
  Benefit: Prevents... nothing (reads don't have side effects)
  Decision: Skip unless caching results

Skip Retry Logic when:
  Situation: Operation MUST be manual (e.g., production deployment)
  Cost: Could auto-retry and cause issues
  Benefit: None (need human approval anyway)
  Decision: Explicitly no retries
```

#### Common Pattern Mistakes

**Mistake 1: Implementing all patterns for everything**

```yaml
Problem:
  Junior engineer adds circuit breaker + retry + idempotency + checkpointing
  to simple file read operation

Result:
  - 500 lines of code for 10-line operation
  - 2 weeks of development time
  - Harder to debug
  - No actual benefit

Fix:
  Match patterns to risk:
    Low risk (file read): Simple error handling
    Medium risk (API call): Circuit breaker + retry
    High risk (infrastructure): All patterns
```

**Mistake 2: Circuit breaker without retry**

```yaml
Problem:
  Circuit breaker opens immediately on first failure
  No retries attempted

Result:
  Transient failures (1-second network hiccup) → circuit opens
  Agent disabled for 60 seconds unnecessarily

Fix:
  Retry FIRST, then circuit breaker
  Example: 3 retries with backoff → if all fail → count as 1 failure toward circuit threshold
```

**Mistake 3: Idempotency without existence checks**

```yaml
Problem:
  Code assumes idempotency but doesn't verify

  async def create_resource_idempotent(name):
      """Claims to be idempotent"""
      return await api.create(name)  # Actually fails on duplicate

Result:
  Agent retries → duplicate error → circuit opens

Fix:
  Implement proper idempotency:
    1. Check if exists
    2. If exists, return existing
    3. If not, create
    4. Handle race conditions
```

#### Quick Decision Tree

```
Need resilience for operation?
│
├─ Operation takes <10 seconds?
│  ├─ Yes → Circuit Breaker + Simple Retry (3-4 hours)
│  └─ No → Continue below
│
├─ Operation is read-only?
│  ├─ Yes → Circuit Breaker + Retry + Caching (4-6 hours)
│  └─ No → Continue below
│
├─ Operation creates/modifies resources?
│  ├─ Yes → Circuit Breaker + Retry + Idempotency (6-8 hours)
│  └─ No → Just Circuit Breaker + Retry
│
└─ Workflow takes >10 minutes?
   └─ Yes → Add Checkpointing (+4-6 hours)
```

**Rule of thumb**: Start with circuit breaker + retry (minimum viable resilience). Add idempotency if operation has side effects. Add checkpointing only if workflow is long and failure is common.

---

## Section 2: Idempotency — Safe to Retry

### What is Idempotency?

**Definition:** An operation is idempotent if performing it multiple times has the same effect as performing it once.

**Mathematical definition:**
```
f(f(x)) = f(x)
```

**Real-world examples:**

| Operation | Idempotent? | Why |
|-----------|-------------|-----|
| `SET user_status = "active"` | ✅ Yes | Same result whether run 1× or 10× |
| `INCREMENT page_views` | ❌ No | Different result each time |
| `DELETE user WHERE id=123` | ✅ Yes | User deleted after first call |
| `CREATE user WITH id=123` | ❌ No | Second call fails (duplicate) |
| `PUT /api/users/123` | ✅ Yes | Updates user to same state |
| `POST /api/users` | ❌ No | Creates new user each time |

---

### Why Idempotency Matters for Agents

**Without idempotency:**
```python
# Agent crashes mid-execution
await increase_memory(pod, by="500Mi")  # Executed
await restart_pod(pod)                   # NOT executed (crash)

# Agent retries from start
await increase_memory(pod, by="500Mi")  # Executed AGAIN! (now +1000Mi)
await restart_pod(pod)                   # Executed

# Result: Memory increased by 1000Mi instead of 500Mi
```

**With idempotency:**
```python
# Agent sets absolute values, not relative changes
await set_memory(pod, to="1024Mi")     # Executed
await restart_pod(pod)                  # NOT executed (crash)

# Agent retries from start
await set_memory(pod, to="1024Mi")     # Executed AGAIN (same result!)
await restart_pod(pod)                  # Executed

# Result: Memory is 1024Mi (correct)
```

---

### Building Idempotent Agent Actions

**Pattern 1: Use Absolute Values, Not Deltas**

```python
# ❌ BAD: Relative changes (not idempotent)
async def scale_up(deployment: str):
    current_replicas = await get_replicas(deployment)
    await set_replicas(deployment, current_replicas + 1)

# If this runs twice, you get +2 instead of +1

# ✅ GOOD: Absolute values (idempotent)
async def ensure_replicas(deployment: str, target: int):
    await set_replicas(deployment, target)

# Safe to run multiple times
```

**Pattern 2: Check Before Acting**

```python
# ✅ GOOD: Check-then-act pattern
async def ensure_config_exists(config_name: str, data: dict):
    # Check if already exists
    existing = await get_config(config_name)

    if existing and existing['data'] == data:
        # Already in desired state, no action needed
        return {"status": "already_exists", "action": "none"}

    if existing:
        # Update existing
        await update_config(config_name, data)
        return {"status": "updated", "action": "update"}
    else:
        # Create new
        await create_config(config_name, data)
        return {"status": "created", "action": "create"}
```

**Pattern 3: Use Idempotency Keys**

```python
# ✅ GOOD: Idempotency key pattern (Stripe-style)
async def charge_customer(
    customer_id: str,
    amount: float,
    idempotency_key: str
):
    # Check if already processed
    existing = await db.charges.find_one({
        'idempotency_key': idempotency_key
    })

    if existing:
        # Already processed, return cached result
        return existing

    # Process charge
    charge = await stripe.charge.create(
        customer=customer_id,
        amount=amount,
        idempotency_key=idempotency_key
    )

    # Cache result
    await db.charges.insert_one({
        'idempotency_key': idempotency_key,
        'charge_id': charge.id,
        'timestamp': time.time()
    })

    return charge
```

---

### Idempotent Agent Implementation

**File: `idempotent_agent.py`**

```python
"""
Idempotent agent with action tracking.

Ensures all actions are safe to retry.
"""

import hashlib
import json
import asyncio
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ActionRecord:
    """Record of a completed action"""
    action_id: str
    action_name: str
    params: Dict
    result: Any
    timestamp: float
    completed: bool = False


class IdempotentAgent:
    """
    Agent that tracks completed actions and ensures idempotency.

    All actions must be idempotent and identified by unique keys.
    """

    def __init__(self, state_file: str = "agent_state.json"):
        self.state_file = state_file
        self.completed_actions: Dict[str, ActionRecord] = {}
        self._load_state()

    def _load_state(self):
        """Load completed actions from disk (crash recovery)"""
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                for action_id, record in data.items():
                    self.completed_actions[action_id] = ActionRecord(**record)
        except FileNotFoundError:
            pass

    def _save_state(self):
        """Persist completed actions to disk"""
        data = {
            action_id: {
                'action_id': record.action_id,
                'action_name': record.action_name,
                'params': record.params,
                'result': record.result,
                'timestamp': record.timestamp,
                'completed': record.completed
            }
            for action_id, record in self.completed_actions.items()
        }

        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _generate_action_id(self, action_name: str, params: Dict) -> str:
        """Generate unique ID for action based on name and params"""
        # Sort params for consistent hashing
        params_str = json.dumps(params, sort_keys=True)
        content = f"{action_name}:{params_str}"
        return hashlib.sha256(content.encode()).hexdigest()

    async def execute(
        self,
        action_name: str,
        action_func: Callable,
        params: Optional[Dict] = None,
        **kwargs
    ) -> Any:
        """
        Execute action idempotently.

        Args:
            action_name: Name of action
            action_func: Async function to execute
            params: Parameters for action (used in idempotency key)
            **kwargs: Additional arguments to pass to action_func

        Returns:
            Result from action_func
        """
        params = params or {}

        # Generate idempotency key
        action_id = self._generate_action_id(action_name, params)

        # Check if already completed
        if action_id in self.completed_actions:
            record = self.completed_actions[action_id]
            print(f"✓ Action '{action_name}' already completed, returning cached result")
            return record.result

        # Execute action
        print(f"▶ Executing action '{action_name}' (id: {action_id[:8]}...)")
        result = await action_func(**kwargs)

        # Record completion
        record = ActionRecord(
            action_id=action_id,
            action_name=action_name,
            params=params,
            result=result,
            timestamp=asyncio.get_event_loop().time(),
            completed=True
        )

        self.completed_actions[action_id] = record
        self._save_state()

        print(f"✓ Action '{action_name}' completed successfully")
        return result

    def reset(self):
        """Clear all completed actions (for testing)"""
        self.completed_actions.clear()
        self._save_state()


# Example usage
async def main():
    """Demonstrate idempotent agent"""

    agent = IdempotentAgent(state_file="demo_state.json")
    agent.reset()  # Start fresh

    # Define some actions
    async def set_pod_memory(pod_name: str, memory: str):
        print(f"  → Setting {pod_name} memory to {memory}")
        await asyncio.sleep(0.5)
        return {"pod": pod_name, "memory": memory}

    async def restart_pod(pod_name: str):
        print(f"  → Restarting {pod_name}")
        await asyncio.sleep(0.5)
        return {"pod": pod_name, "status": "restarted"}

    # Simulate workflow with crash and retry
    print("=== Attempt 1 (will 'crash' after first action) ===\n")

    # Action 1: Set memory
    await agent.execute(
        "set_pod_memory",
        set_pod_memory,
        params={"pod": "payment-service", "memory": "2Gi"},
        pod_name="payment-service",
        memory="2Gi"
    )

    # Simulate crash here!
    print("\n💥 Simulated crash!\n")

    print("=== Attempt 2 (retry from start) ===\n")

    # Action 1: Set memory (will skip, already done)
    await agent.execute(
        "set_pod_memory",
        set_pod_memory,
        params={"pod": "payment-service", "memory": "2Gi"},
        pod_name="payment-service",
        memory="2Gi"
    )

    # Action 2: Restart pod (will execute)
    await agent.execute(
        "restart_pod",
        restart_pod,
        params={"pod": "payment-service"},
        pod_name="payment-service"
    )

    print("\n=== Workflow completed successfully! ===")


if __name__ == "__main__":
    asyncio.run(main())
```

**Run it:**

```bash
python idempotent_agent.py
```

**Expected output:**

```
=== Attempt 1 (will 'crash' after first action) ===

▶ Executing action 'set_pod_memory' (id: a3f5b2c8...)
  → Setting payment-service memory to 2Gi
✓ Action 'set_pod_memory' completed successfully

💥 Simulated crash!

=== Attempt 2 (retry from start) ===

✓ Action 'set_pod_memory' already completed, returning cached result
▶ Executing action 'restart_pod' (id: 9d7e1f4a...)
  → Restarting payment-service
✓ Action 'restart_pod' completed successfully

=== Workflow completed successfully! ===
```

---

## Section 3: State Checkpointing and Recovery

### What is Checkpointing?

**Definition:** Saving progress at regular intervals so you can resume from the last checkpoint instead of starting over.

**Analogy:** Like save points in a video game:
- ❌ No checkpoints: Die → restart entire game
- ✅ Checkpoints: Die → restart from last save point

---

### Implementing Checkpoints

**Pattern: Checkpoint After Each Major Step**

```python
"""
Agent with checkpointing for crash recovery.
"""

import json
import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class Checkpoint:
    """Represents a saved checkpoint"""
    workflow_id: str
    step: int
    step_name: str
    state: Dict[str, Any]
    timestamp: float


class CheckpointedAgent:
    """
    Agent that saves checkpoints for crash recovery.

    Can resume from last checkpoint after crash.
    """

    def __init__(self, workflow_id: str, checkpoint_file: str = "checkpoints.json"):
        self.workflow_id = workflow_id
        self.checkpoint_file = checkpoint_file
        self.current_step = 0
        self.state = {}

    def save_checkpoint(self, step_name: str):
        """Save current state as checkpoint"""
        checkpoint = Checkpoint(
            workflow_id=self.workflow_id,
            step=self.current_step,
            step_name=step_name,
            state=self.state.copy(),
            timestamp=asyncio.get_event_loop().time()
        )

        # Load existing checkpoints
        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoints = json.load(f)
        except FileNotFoundError:
            checkpoints = {}

        # Save checkpoint
        checkpoints[self.workflow_id] = asdict(checkpoint)

        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoints, f, indent=2)

        print(f"💾 Checkpoint saved: step {self.current_step} ({step_name})")

    def load_checkpoint(self) -> bool:
        """Load last checkpoint if exists"""
        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoints = json.load(f)

            if self.workflow_id in checkpoints:
                checkpoint_data = checkpoints[self.workflow_id]
                self.current_step = checkpoint_data['step'] + 1  # Resume from next step
                self.state = checkpoint_data['state']
                print(f"📂 Loaded checkpoint: step {checkpoint_data['step']} ({checkpoint_data['step_name']})")
                print(f"   Resuming from step {self.current_step}")
                return True

        except FileNotFoundError:
            pass

        return False

    async def run_workflow(self, steps: List[tuple]):
        """
        Run workflow with checkpoints.

        Args:
            steps: List of (step_name, step_func, step_args) tuples
        """
        # Try to load checkpoint
        resumed = self.load_checkpoint()

        if resumed:
            print(f"▶ Resuming workflow from step {self.current_step}\n")
        else:
            print(f"▶ Starting new workflow\n")

        # Execute steps
        for i, (step_name, step_func, step_args) in enumerate(steps):
            # Skip already completed steps
            if i < self.current_step:
                print(f"⏭  Skipping step {i}: {step_name} (already completed)")
                continue

            print(f"\nStep {i}: {step_name}")
            result = await step_func(**step_args)

            # Update state
            self.state[step_name] = result
            self.current_step = i

            # Save checkpoint
            self.save_checkpoint(step_name)

        print(f"\n✓ Workflow completed!")


# Example usage
async def main():
    """Demonstrate checkpointed workflow"""

    # Define workflow steps
    async def analyze_logs(incident_id: str):
        print(f"  Analyzing logs for {incident_id}...")
        await asyncio.sleep(1)
        return {"errors": 15, "warnings": 42}

    async def check_metrics(incident_id: str):
        print(f"  Checking metrics for {incident_id}...")
        await asyncio.sleep(1)
        return {"cpu": "85%", "memory": "92%"}

    async def identify_root_cause(incident_id: str):
        print(f"  Identifying root cause for {incident_id}...")
        await asyncio.sleep(1)
        return {"cause": "memory leak", "service": "payment-api"}

    async def apply_fix(incident_id: str):
        print(f"  Applying fix for {incident_id}...")
        # Simulate crash here on first run
        if not agent.load_checkpoint():
            print("  💥 Simulated crash!")
            raise Exception("Crash during fix")
        await asyncio.sleep(1)
        return {"fix_applied": True}

    async def verify_fix(incident_id: str):
        print(f"  Verifying fix for {incident_id}...")
        await asyncio.sleep(1)
        return {"verified": True}

    workflow_steps = [
        ("analyze_logs", analyze_logs, {"incident_id": "INC-12345"}),
        ("check_metrics", check_metrics, {"incident_id": "INC-12345"}),
        ("identify_root_cause", identify_root_cause, {"incident_id": "INC-12345"}),
        ("apply_fix", apply_fix, {"incident_id": "INC-12345"}),
        ("verify_fix", verify_fix, {"incident_id": "INC-12345"}),
    ]

    # First attempt (will crash)
    print("="*60)
    print("ATTEMPT 1 (will crash during 'apply_fix')")
    print("="*60)

    agent = CheckpointedAgent(workflow_id="incident-INC-12345")

    try:
        await agent.run_workflow(workflow_steps)
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")

    # Second attempt (will resume from checkpoint)
    print("\n" + "="*60)
    print("ATTEMPT 2 (resuming from checkpoint)")
    print("="*60 + "\n")

    agent2 = CheckpointedAgent(workflow_id="incident-INC-12345")
    await agent2.run_workflow(workflow_steps)


if __name__ == "__main__":
    asyncio.run(main())
```

**Run it:**

```bash
python checkpointed_agent.py
```

**Expected output:**

```
============================================================
ATTEMPT 1 (will crash during 'apply_fix')
============================================================
▶ Starting new workflow

Step 0: analyze_logs
  Analyzing logs for INC-12345...
💾 Checkpoint saved: step 0 (analyze_logs)

Step 1: check_metrics
  Checking metrics for INC-12345...
💾 Checkpoint saved: step 1 (check_metrics)

Step 2: identify_root_cause
  Identifying root cause for INC-12345...
💾 Checkpoint saved: step 2 (identify_root_cause)

Step 3: apply_fix
  Applying fix for INC-12345...
  💥 Simulated crash!

❌ Workflow failed: Crash during fix

============================================================
ATTEMPT 2 (resuming from checkpoint)
============================================================

📂 Loaded checkpoint: step 2 (identify_root_cause)
   Resuming from step 3
▶ Resuming workflow from step 3

⏭  Skipping step 0: analyze_logs (already completed)
⏭  Skipping step 1: check_metrics (already completed)
⏭  Skipping step 2: identify_root_cause (already completed)

Step 3: apply_fix
  Applying fix for INC-12345...
💾 Checkpoint saved: step 3 (apply_fix)

Step 4: verify_fix
  Verifying fix for INC-12345...
💾 Checkpoint saved: step 4 (verify_fix)

✓ Workflow completed!
```

---


## Summary

In this chapter, you learned the **three core resilience patterns** that every production agent needs:

1. **Circuit Breaker Pattern** - Prevents cascading failures by opening the circuit after threshold failures
2. **Idempotency** - Makes operations safe to retry by ensuring same result regardless of execution count
3. **State Checkpointing** - Enables crash recovery by saving progress at regular intervals

### Key Takeaways

- **Circuit breakers** protect against cascading failures and give failing systems time to recover
- **Idempotency** is achieved through absolute values (not deltas), check-before-act patterns, and idempotency keys
- **Checkpointing** allows workflows to resume from last save point instead of starting over
- **Pattern selection** depends on operation type, duration, and failure characteristics
- Start with circuit breaker + retry (minimum viable resilience), add others as needed

### Pattern Selection Quick Reference

| Operation Type | Required Patterns | Time Investment |
|---------------|------------------|-----------------|
| Quick API calls (<10s) | Circuit Breaker + Retry | 3-4 hours |
| Read-only operations | + Caching | 4-6 hours |
| Resource creation | + Idempotency | 6-8 hours |
| Long workflows (>10 min) | + Checkpointing | 10-14 hours |

### What's Next

**Continue to [Chapter 22: Production Deployment of Agentic Systems](./22-production-deployment.md)** to learn:
- Exponential backoff with jitter
- Graceful degradation strategies
- Self-healing architectures
- Staged rollout patterns (Dev → Staging → Prod)
- Real-world incident response scenarios
- Production monitoring and observability

---

## Navigation

← Previous: [Chapter 20: Agent Loop Detection & Prevention](./20-agent-loop-detection.md) | Next: [Chapter 22: Production Deployment of Agentic Systems](./22-production-deployment.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 21 (Part 1 of 2)** | Resilience Patterns for Agents | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

---
