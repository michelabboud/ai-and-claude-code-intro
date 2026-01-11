# Chapter 20: Agent Loop Detection & Prevention Fundamentals

**Part 7: Advanced Agentic Development & Leadership**

---

## Navigation

← Previous: [Chapter 19: Team Transformation](./19-team-transformation.md) | Next: [Chapter 21: Building Resilient Agentic Systems](./21-resilient-agentic-systems.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---


## Learning Objectives

By the end of this chapter, you will:

- **Understand Ralph Wiggum loops** and why they're critical to prevent in agentic systems
- **Identify 6 types of loops** that can occur in AI agent workflows
- **Build loop detection mechanisms** from scratch using Python
- **Debug agent loops** effectively using IDE tools and logging
- **Implement production-grade monitoring** for loop detection
- **Recognize security implications** of infinite loops (Denial of Wallet attacks)
- **Apply best practices** for safe agentic development

**Prerequisites:**
- Python 3.9+ installed
- Basic understanding of async/await in Python
- Familiarity with Claude Code from Chapters 6-9
- Text editor or IDE (VS Code recommended)

**Time to Complete:** 2-3 hours (including hands-on exercise)

---

## Introduction: The $12,000 AWS Bill

It was 3 AM when Sarah, a DevOps engineer at a fast-growing startup, received an urgent Slack message from AWS billing: **"Your account has exceeded $12,000 in API charges this month."**

The culprit? An AI agent designed to auto-remediate Kubernetes pod failures. The agent had gotten stuck in what we call a **"Ralph Wiggum loop"** — named after the iconic Simpsons character who famously said *"I'm in danger!"* while riding his bus in circles.

Here's what happened:

```python
# The problematic agent code
async def fix_pod(pod_name):
    if pod_status(pod_name) == "CrashLoopBackOff":
        restart_pod(pod_name)
        await asyncio.sleep(5)

        # Check if fixed
        if pod_status(pod_name) == "CrashLoopBackOff":
            # Still failing? Try again!
            await fix_pod(pod_name)  # 🚨 INFINITE RECURSION
```

**What went wrong:**
1. Pod was failing due to a missing ConfigMap (not fixable by restart)
2. Agent restarted pod → checked status → still failing → restarted again
3. No exit condition for "unfixable" scenarios
4. Each restart attempt called Claude API ($0.03 per call)
5. Agent ran for 72 hours = **400,000 API calls = $12,000**

This chapter teaches you how to **prevent these loops** before they happen, **detect them** when they do, and **recover gracefully** without human intervention.

---

## Section 1: What Are Ralph Wiggum Loops?

### Definition

A **Ralph Wiggum loop** (also called an infinite agentic loop) occurs when an AI agent:
1. Takes an action
2. Observes that the action didn't achieve the desired outcome
3. Repeats the exact same action (or a slight variation)
4. Fails to recognize it's stuck in a repetitive pattern
5. Continues indefinitely without making progress

### Why "Ralph Wiggum"?

In The Simpsons, Ralph Wiggum is riding his bus in circles while cheerfully exclaiming *"I'm in danger!"* — perfectly capturing the essence of an agent that:
- Thinks it's making progress (cheerful)
- Is actually going in circles (the bus loop)
- Doesn't realize the danger (lack of self-awareness)

### Real-World Impact

**Cost:**
- Claude Opus: $15 per 1M input tokens, $75 per 1M output tokens
- 1,000 loop iterations with 10K tokens each = $1,500 in API costs
- Production incidents can cost $10K-$50K before detection

**Service Disruption:**
- Agent monopolizes API quota, blocking legitimate requests
- Cascading failures if agent controls infrastructure
- Team loses trust in AI automation

**Why This Happens:**
1. **No state tracking:** Agent doesn't remember what it tried before
2. **No progress metrics:** Can't tell if it's getting closer to goal
3. **No timeout limits:** Runs indefinitely
4. **No human escalation:** Fails silently without alerting humans
5. **Overly optimistic:** Assumes every action will eventually succeed

---

## Section 2: Development Fundamentals — The 6 Types of Agent Loops

Understanding loop types is crucial for detection. Each requires different prevention strategies.

### Type 1: Infinite Retry Loop

**Description:** Agent retries the same failed action indefinitely.

**Example Scenario:** Agent tries to restart a pod that's crashing due to insufficient memory (restart won't fix it).

**Code Example:**
```python
# ❌ BAD: No retry limit
async def deploy_service(service_name):
    while True:
        result = await kubectl_apply(service_name)
        if result.success:
            break
        await asyncio.sleep(10)
        # Retries forever even if deployment config is invalid
```

**Why It Happens:**
- Missing retry counter
- No classification of "retryable" vs "permanent" failures
- Overly optimistic error handling

**Fix:**
```python
# ✅ GOOD: Retry limit + failure classification
async def deploy_service(service_name, max_retries=3):
    for attempt in range(max_retries):
        result = await kubectl_apply(service_name)

        if result.success:
            return result

        # Check if retryable
        if result.error in ["connection_timeout", "rate_limited"]:
            await asyncio.sleep(10 * (2 ** attempt))  # Exponential backoff
            continue
        else:
            # Permanent error (invalid YAML, RBAC denied, etc.)
            raise DeploymentFailed(f"Non-retryable error: {result.error}")

    raise MaxRetriesExceeded(f"Failed after {max_retries} attempts")
```

---

### Type 2: State Loop

**Description:** Agent returns to the same state repeatedly without recognizing it's been there before.

**Example Scenario:** Agent adjusts Kubernetes resource limits, but each adjustment triggers a pod restart, causing the agent to think there's a new issue.

**Visualization:**
```
State A (pod failing)
  → Action: increase memory
  → State B (pod restarting)
  → Action: wait for readiness
  → State A (pod failing again)
  → Agent thinks: "New issue!"
  → Action: increase memory
  → State B (pod restarting)
  ... loop continues
```

**Code Example:**
```python
# ❌ BAD: No state tracking
async def optimize_resources(pod_name):
    while True:
        status = await get_pod_status(pod_name)

        if status == "OOMKilled":
            await increase_memory(pod_name, by="100Mi")
            await asyncio.sleep(30)
            # Doesn't remember it already tried this!
```

**Fix with State Fingerprinting:**
```python
import hashlib
import json

class StateTracker:
    """Track visited states to detect loops"""

    def __init__(self, max_history=20):
        self.state_history = []
        self.max_history = max_history

    def fingerprint(self, state: dict) -> str:
        """Create unique hash of current state"""
        # Sort keys for consistent hashing
        state_json = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_json.encode()).hexdigest()

    def check_loop(self, state: dict) -> bool:
        """Returns True if we've been in this state before"""
        fp = self.fingerprint(state)

        # Check if fingerprint exists in recent history
        recent_fingerprints = [s['fingerprint'] for s in self.state_history[-10:]]

        if fp in recent_fingerprints:
            return True

        # Add to history
        self.state_history.append({
            'fingerprint': fp,
            'state': state,
            'timestamp': time.time()
        })

        # Trim history
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)

        return False

# ✅ GOOD: State loop detection
async def optimize_resources(pod_name):
    tracker = StateTracker()
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        status = await get_pod_status(pod_name)
        current_memory = await get_memory_limit(pod_name)

        # Create state representation
        state = {
            'pod_name': pod_name,
            'status': status,
            'memory_limit': current_memory,
            'cpu_limit': await get_cpu_limit(pod_name)
        }

        # Check for state loop
        if tracker.check_loop(state):
            raise StateLoopDetected(
                f"Returned to previously seen state: {state}"
            )

        if status == "OOMKilled":
            await increase_memory(pod_name, by="100Mi")
            await asyncio.sleep(30)
            attempts += 1
        elif status == "Running":
            return {"success": True, "final_memory": current_memory}

    raise MaxAttemptsExceeded(f"Could not optimize after {max_attempts} attempts")
```

---

### Type 3: Circular Dependency Loop

**Description:** Agent A calls Agent B, which calls Agent C, which calls Agent A.

**Example Scenario:**
- **Log Analyzer Agent:** Finds error in logs, delegates to Metrics Agent
- **Metrics Agent:** Sees high latency, delegates to Code Analyzer Agent
- **Code Analyzer Agent:** Finds recent deployment, delegates back to Log Analyzer
- Loop continues...

**Visualization:**
```
┌─────────────────┐
│  Log Analyzer   │────┐
└─────────────────┘    │
        ↑              ↓
        │      ┌─────────────────┐
        │      │ Metrics Analyzer│
        │      └─────────────────┘
        │              │
        │              ↓
        │      ┌─────────────────┐
        └──────│  Code Analyzer  │
               └─────────────────┘
```

**Code Example:**
```python
# ❌ BAD: No call stack tracking
class LogAnalyzer:
    async def analyze(self, incident_id):
        errors = await self.parse_logs(incident_id)
        if "latency" in errors:
            # Delegate to metrics
            return await metrics_agent.analyze(incident_id)

class MetricsAnalyzer:
    async def analyze(self, incident_id):
        metrics = await self.fetch_metrics(incident_id)
        if metrics['error_rate'] > 0.01:
            # Delegate to code analyzer
            return await code_agent.analyze(incident_id)

class CodeAnalyzer:
    async def analyze(self, incident_id):
        recent_changes = await self.get_recent_deploys()
        if recent_changes:
            # Delegate back to logs (loop!)
            return await log_agent.analyze(incident_id)
```

**Fix with Call Stack Tracking:**
```python
from typing import List, Optional

class AgentCallStack:
    """Prevents circular agent dependencies"""

    def __init__(self):
        self.stack: List[str] = []
        self.max_depth = 10

    def push(self, agent_name: str):
        """Add agent to call stack"""
        if agent_name in self.stack:
            raise CircularDependencyDetected(
                f"Circular call detected: {' -> '.join(self.stack)} -> {agent_name}"
            )

        if len(self.stack) >= self.max_depth:
            raise MaxCallDepthExceeded(
                f"Call stack too deep: {' -> '.join(self.stack)}"
            )

        self.stack.append(agent_name)

    def pop(self):
        """Remove agent from call stack"""
        if self.stack:
            self.stack.pop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pop()

# Global call stack (in production, use context variables)
call_stack = AgentCallStack()

# ✅ GOOD: Circular dependency prevention
class LogAnalyzer:
    async def analyze(self, incident_id, stack: Optional[AgentCallStack] = None):
        stack = stack or call_stack

        with stack:
            stack.push("LogAnalyzer")

            errors = await self.parse_logs(incident_id)
            if "latency" in errors:
                # Pass stack to child agent
                return await metrics_agent.analyze(incident_id, stack)

            return {"agent": "LogAnalyzer", "findings": errors}

class MetricsAnalyzer:
    async def analyze(self, incident_id, stack: Optional[AgentCallStack] = None):
        stack = stack or call_stack

        with stack:
            stack.push("MetricsAnalyzer")

            metrics = await self.fetch_metrics(incident_id)
            if metrics['error_rate'] > 0.01:
                return await code_agent.analyze(incident_id, stack)

            return {"agent": "MetricsAnalyzer", "findings": metrics}

class CodeAnalyzer:
    async def analyze(self, incident_id, stack: Optional[AgentCallStack] = None):
        stack = stack or call_stack

        with stack:
            stack.push("CodeAnalyzer")

            recent_changes = await self.get_recent_deploys()
            if recent_changes:
                # This will raise CircularDependencyDetected!
                return await log_agent.analyze(incident_id, stack)
```

---

### Type 4: Escalation Loop

**Description:** Error handling creates new errors, which trigger more error handling.

**Example Scenario:** Agent encounters API timeout → retries → hits rate limit → retries faster → permanent ban → retries → account suspended.

**Code Example:**
```python
# ❌ BAD: Escalating error handling
async def fetch_data(url):
    try:
        return await http_client.get(url, timeout=5)
    except TimeoutError:
        # Retry faster (wrong!)
        return await http_client.get(url, timeout=2)
    except RateLimitError:
        # Retry immediately (wrong!)
        return await http_client.get(url)
    except BannedError:
        # Create new account (very wrong!)
        new_account = await create_account()
        return await http_client.get(url, auth=new_account)
```

**Fix:**
```python
# ✅ GOOD: De-escalation pattern
async def fetch_data(url, retry_count=0, max_retries=3):
    if retry_count >= max_retries:
        raise MaxRetriesExceeded("All retry strategies exhausted")

    try:
        return await http_client.get(url, timeout=5)

    except TimeoutError:
        # Increase timeout, don't decrease
        longer_timeout = 5 * (2 ** retry_count)
        return await http_client.get(url, timeout=longer_timeout)

    except RateLimitError as e:
        # Respect rate limit, wait longer
        wait_time = e.retry_after or (60 * (2 ** retry_count))
        await asyncio.sleep(wait_time)
        return await fetch_data(url, retry_count + 1, max_retries)

    except BannedError:
        # Don't retry, escalate to humans
        await alert_humans("Account banned", {"url": url, "account": current_account})
        raise PermanentFailure("Account banned, human intervention required")
```

---

### Type 5: Token Threshold Loop

**Description:** Agent hits context window limit, restarts from scratch, hits limit again.

**Example Scenario:** Agent analyzing 500K tokens of logs, hits 200K context limit, truncates and retries, hits limit again.

**Code Example:**
```python
# ❌ BAD: No token budget tracking
async def analyze_logs(log_files):
    all_logs = ""
    for file in log_files:
        all_logs += read_file(file)  # Could be 1M+ tokens

    # Send to Claude (will hit context limit)
    response = await claude.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": all_logs}]
    )
```

**Fix with Token Budget:**
```python
import tiktoken

class TokenBudgetManager:
    """Manage token usage to prevent context limit loops"""

    def __init__(self, model="claude-3-5-sonnet-20241022"):
        self.model = model
        self.encoder = tiktoken.encoding_for_model("gpt-4")  # Close enough
        self.context_limit = 200_000  # Claude 3.5 Sonnet limit
        self.safety_margin = 0.8  # Use 80% of limit

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoder.encode(text))

    def truncate_to_budget(self, text: str, budget: int) -> str:
        """Truncate text to fit token budget"""
        tokens = self.encoder.encode(text)
        if len(tokens) <= budget:
            return text

        # Truncate and decode
        truncated = tokens[:budget]
        return self.encoder.decode(truncated)

# ✅ GOOD: Token budget management
async def analyze_logs(log_files):
    budget_manager = TokenBudgetManager()
    max_tokens = int(budget_manager.context_limit * budget_manager.safety_margin)

    # Collect logs within budget
    logs_to_analyze = ""
    tokens_used = 0

    for file in log_files:
        content = read_file(file)
        content_tokens = budget_manager.count_tokens(content)

        if tokens_used + content_tokens > max_tokens:
            # Would exceed budget, truncate
            remaining_budget = max_tokens - tokens_used
            content = budget_manager.truncate_to_budget(content, remaining_budget)
            logs_to_analyze += content
            break

        logs_to_analyze += content
        tokens_used += content_tokens

    print(f"Analyzing {tokens_used:,} tokens (under {max_tokens:,} budget)")

    response = await claude.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": logs_to_analyze}]
    )

    return response.content[0].text
```

---

### Type 6: Spawn Loop

**Description:** Agent creates child agents, which create more agents, exponentially.

**Example Scenario:** Incident response agent spawns specialist agents, each spawns sub-agents, system runs out of memory.

**Visualization:**
```
Coordinator
    ├─ LogAgent
    │    ├─ ErrorParser
    │    └─ StackTraceAnalyzer
    │         ├─ CodeSearcher
    │         └─ GitBlamer
    │              ├─ CommitAnalyzer (too deep!)
    │              └─ ...
    ├─ MetricsAgent
    │    ├─ PrometheusQuery
    │    └─ ...
    ...
```

**Code Example:**
```python
# ❌ BAD: Unconstrained agent spawning
async def coordinate_incident(incident_id):
    # Spawn specialists
    log_agent = await spawn_agent("LogAnalyzer", incident_id)
    metrics_agent = await spawn_agent("MetricsAnalyzer", incident_id)
    code_agent = await spawn_agent("CodeAnalyzer", incident_id)

    # Each agent spawns more agents...
    # No limit on total agent count!
```

**Fix with Agent Pool:**
```python
import asyncio
from typing import Optional

class AgentPool:
    """Limit total number of concurrent agents"""

    def __init__(self, max_agents=10):
        self.max_agents = max_agents
        self.active_agents = 0
        self.semaphore = asyncio.Semaphore(max_agents)

    async def spawn_agent(self, agent_class, *args, **kwargs):
        """Spawn agent with pool limit"""
        async with self.semaphore:
            if self.active_agents >= self.max_agents:
                raise AgentPoolExhausted(
                    f"Cannot spawn more agents (limit: {self.max_agents})"
                )

            self.active_agents += 1
            try:
                agent = agent_class(*args, **kwargs)
                result = await agent.execute()
                return result
            finally:
                self.active_agents -= 1

# ✅ GOOD: Limited agent pool
agent_pool = AgentPool(max_agents=10)

async def coordinate_incident(incident_id):
    try:
        # Spawn with limit
        results = await asyncio.gather(
            agent_pool.spawn_agent(LogAnalyzer, incident_id),
            agent_pool.spawn_agent(MetricsAnalyzer, incident_id),
            agent_pool.spawn_agent(CodeAnalyzer, incident_id),
            return_exceptions=True
        )

        return synthesize_results(results)

    except AgentPoolExhausted as e:
        # Fall back to sequential execution
        print(f"Pool exhausted, running sequentially: {e}")
        return await run_sequential_analysis(incident_id)
```

---

### Diagnosing Loop Types: A Practical Decision Framework

When you encounter an agent loop in production, quick diagnosis is critical. Here's how to identify which type you're dealing with and respond appropriately.

#### The 3-Step Diagnosis Process

**Step 1: Observe the Pattern** (30 seconds)

```yaml
Look at logs and answer:

Question 1: Is the agent repeating the EXACT same action?
  Yes → Likely Type 1 (Infinite Retry)
  No → Continue to Question 2

Question 2: Are states repeating in the logs (A → B → A → B)?
  Yes → Type 2 (State Loop)
  No → Continue to Question 3

Question 3: Do you see cascading agent spawns in logs?
  Yes → Type 6 (Spawn Loop) - CRITICAL, kill immediately
  No → Continue to Question 4

Question 4: Are multiple agents blocking each other?
  Yes → Type 3 (Circular Dependency)
  No → Continue to Question 5

Question 5: Are requests failing then immediately retrying with higher privileges?
  Yes → Type 4 (Escalation Loop)
  No → Type 5 (Token Threshold) - check token counts
```

**Step 2: Check Key Metrics** (1 minute)

```python
# Quick diagnostic script
import json

def diagnose_loop(log_file):
    """Analyze agent logs to identify loop type"""

    with open(log_file) as f:
        logs = [json.loads(line) for line in f]

    # Metric 1: Action repetition rate
    actions = [log['action'] for log in logs if 'action' in log]
    unique_actions = set(actions)
    repetition_rate = (len(actions) - len(unique_actions)) / len(actions)

    if repetition_rate > 0.8:
        return "Type 1: Infinite Retry (80%+ same action)"

    # Metric 2: State fingerprint collisions
    states = [log.get('state_fingerprint') for log in logs if 'state_fingerprint' in log]
    if len(states) > len(set(states)) * 2:
        return "Type 2: State Loop (state revisited multiple times)"

    # Metric 3: Agent spawn rate
    spawns = [log for log in logs if log.get('event') == 'agent_spawned']
    if len(spawns) > 10 and (logs[-1]['timestamp'] - logs[0]['timestamp']) < 60:
        return "Type 6: Spawn Loop (>10 spawns/minute) - CRITICAL!"

    # Metric 4: Dependency wait events
    waits = [log for log in logs if 'waiting_for' in log]
    if len(waits) > len(logs) * 0.5:
        return "Type 3: Circular Dependency (50%+ of time waiting)"

    return "Type 4 or 5: Check token usage and escalation patterns"

# Usage
diagnosis = diagnose_loop('/var/log/agent.jsonl')
print(f"Diagnosis: {diagnosis}")
```

**Step 3: Apply Appropriate Fix** (5-30 minutes)

```yaml
Type 1 - Infinite Retry:
  Immediate: Kill agent, add max_retries parameter
  Long-term: Implement retryable vs permanent error classification
  Time: 5 minutes

Type 2 - State Loop:
  Immediate: Kill agent, add StateTracker
  Long-term: Implement state fingerprinting in all agents
  Time: 15 minutes

Type 3 - Circular Dependency:
  Immediate: Kill all dependent agents, restart in correct order
  Long-term: Implement dependency graph validation at startup
  Time: 30 minutes

Type 4 - Escalation Loop:
  Immediate: Revoke escalation permissions, kill agent
  Long-term: Implement escalation approval workflow
  Time: 20 minutes

Type 5 - Token Threshold:
  Immediate: Increase token limit or reduce context
  Long-term: Implement context pruning strategy
  Time: 10 minutes

Type 6 - Spawn Loop:
  Immediate: KILL ALL AGENTS IMMEDIATELY (cascading failure)
  Long-term: Implement spawn rate limiting at pool level
  Time: 5 minutes + 30 minutes recovery
```

#### Common Diagnostic Mistakes

**Mistake 1: Treating all loops as Type 1**

```yaml
Problem:
  "It's retrying, so I'll just add max_retries=3"

Why it fails:
  - Type 2 loops will still repeat (different states, same outcome)
  - Type 6 spawns will continue (retries don't stop spawns)
  - Type 3 will deadlock (agents waiting for each other)

Correct approach:
  1. Diagnose the specific type
  2. Apply type-specific fix
  3. Add comprehensive loop detection
```

**Mistake 2: Not checking costs before investigating**

```yaml
Scenario: Agent loop detected at 2 PM

❌ Bad response:
  2:00 PM: Notice loop in logs
  2:05 PM: Start debugging
  2:30 PM: Identify root cause
  2:45 PM: Deploy fix
  3:00 PM: Check AWS bill → $8,000 in 1 hour

✅ Good response:
  2:00 PM: Notice loop
  2:01 PM: KILL AGENT IMMEDIATELY
  2:02 PM: Check API usage → stopped at $50
  2:05 PM: Start debugging safely
  2:30 PM: Deploy fix with safeguards

Rule: Always kill first, debug second.
Cost of 1 hour investigation during loop: $1,000-$10,000
Cost of killing agent prematurely: $0 (just restart after fix)
```

**Mistake 3: Fixing the symptom, not the cause**

```yaml
Symptom fix:
  "Agent retries 100 times, I'll add max_retries=3"

Result:
  - Agent fails after 3 retries
  - Still doesn't know WHY it's failing
  - Issue repeats with next similar scenario

Root cause fix:
  1. Why is it retrying? (Pod won't start)
  2. Why won't pod start? (Missing ConfigMap)
  3. Can agent detect missing ConfigMap? (Add check)
  4. Can agent create ConfigMap? (Add capability)
  5. If can't create, escalate to human (Add escalation)

Time investment:
  - Symptom fix: 5 minutes (repeats weekly)
  - Root cause fix: 30 minutes (prevents all future occurrences)
```

#### Production Triage Checklist

When a loop is detected in production:

```yaml
[ ] 1. STOP THE BLEEDING (30 seconds)
      - Kill the looping agent(s)
      - Disable auto-restart if configured
      - Block API key if costs are spiking

[ ] 2. ASSESS DAMAGE (2 minutes)
      - Check API usage costs
      - Check if infrastructure was modified
      - Check if data was corrupted
      - Alert stakeholders if needed

[ ] 3. DIAGNOSE TYPE (3 minutes)
      - Run diagnostic script
      - Check recent deployments
      - Review agent configuration changes

[ ] 4. APPLY QUICK FIX (10 minutes)
      - Add appropriate loop detection
      - Patch critical vulnerability
      - Test in dev environment

[ ] 5. DEPLOY FIX (5 minutes)
      - Deploy with extra monitoring
      - Watch for loop recurrence
      - Document incident

[ ] 6. ROOT CAUSE ANALYSIS (later)
      - Why did existing detection fail?
      - What safeguard was missing?
      - Update all agents with learnings
```

#### When to Redesign vs Patch

```yaml
Patch the existing agent when:
  ✅ Loop is Type 1 or 5 (simple fix: max_retries or token limit)
  ✅ Agent logic is sound, just missing safeguard
  ✅ Occurs in <10% of scenarios
  ✅ Fix can be deployed in <30 minutes

Redesign the agent when:
  🔄 Loop is Type 2, 3, or 6 (architectural issue)
  🔄 Multiple loop types occurring
  🔄 Agent has no state tracking (foundational problem)
  🔄 Occurs in >50% of scenarios
  🔄 Team has lost confidence in agent

Example decision:
  Scenario: Kubernetes pod restart agent loops 60% of the time

  Patch approach: Add max_retries=3
    - Stops infinite loops ✅
    - Still fails 60% of the time ❌
    - Band-aid on broken design ❌

  Redesign approach: Add pod failure classification
    - Classify failures: retryable vs permanent
    - Add ConfigMap/Secret validation before restart
    - Escalate truly unfixable scenarios to humans
    - Stops loops AND increases success rate ✅
    - Takes 2 hours vs 15 minutes ✅ (saves time long-term)
```

**Rule of thumb**: If the same agent loops twice in a week, redesign it. Patches aren't working.

---

## Section 3: Development Workflow — Debugging Agent Loops

Now that we understand loop types, let's build practical debugging skills.

### Setting Up Your Development Environment

**Installation Instructions:**

```bash
# 1. Create project directory
mkdir agent-loop-detection
cd agent-loop-detection

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install anthropic asyncio aiohttp tiktoken pytest pytest-asyncio

# 4. Create project structure
mkdir -p src tests
touch src/__init__.py tests/__init__.py

# 5. Set up environment variables
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

**Project Structure:**
```
agent-loop-detection/
├── .env                    # API keys (never commit!)
├── requirements.txt        # Dependencies
├── src/
│   ├── __init__.py
│   ├── loop_detector.py    # Core detection logic
│   ├── state_tracker.py    # State fingerprinting
│   └── agent_pool.py       # Agent pool management
├── tests/
│   ├── __init__.py
│   └── test_loop_detector.py
└── examples/
    ├── basic_loop.py       # Intentional loop for testing
    └── fixed_loop.py       # Same logic with detection
```

---

### Building a Basic Loop Detector

Let's build a minimal loop detector from scratch.

**File: `src/loop_detector.py`**

```python
"""
Basic loop detection for AI agents.

This module provides simple loop detection mechanisms suitable for
development and testing. For production use, see Chapter 21.
"""

import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class LoopDetectionConfig:
    """Configuration for loop detection behavior"""

    # Maximum times same action can repeat
    max_action_repetitions: int = 3

    # Maximum total iterations before forced stop
    max_total_iterations: int = 20

    # Time window for action repetition (seconds)
    repetition_window: int = 60

    # Enable debug output
    debug: bool = False


@dataclass
class ActionRecord:
    """Record of a single agent action"""

    action: str
    timestamp: float
    metadata: Dict = field(default_factory=dict)


class LoopDetector:
    """
    Simple loop detector for development and debugging.

    Tracks agent actions and raises exceptions when loops are detected.

    Usage:
        detector = LoopDetector(debug=True)

        for action in agent_actions:
            detector.check_action(action)  # Raises LoopDetected if loop found
            perform_action(action)
    """

    def __init__(self, config: Optional[LoopDetectionConfig] = None):
        self.config = config or LoopDetectionConfig()
        self.action_history: List[ActionRecord] = []
        self.iteration_count = 0

    def check_action(self, action: str, metadata: Optional[Dict] = None) -> None:
        """
        Check if action would create a loop.

        Args:
            action: Name of action to perform
            metadata: Optional context (pod name, service, etc.)

        Raises:
            LoopDetected: If action would create a loop
            MaxIterationsExceeded: If too many total iterations
        """
        self.iteration_count += 1
        current_time = time.time()

        # Check 1: Max iterations
        if self.iteration_count > self.config.max_total_iterations:
            raise MaxIterationsExceeded(
                f"Exceeded {self.config.max_total_iterations} total iterations"
            )

        # Check 2: Action repetition
        self._check_repetition(action, current_time)

        # Record action
        record = ActionRecord(
            action=action,
            timestamp=current_time,
            metadata=metadata or {}
        )
        self.action_history.append(record)

        if self.config.debug:
            print(f"[LoopDetector] Action {self.iteration_count}: {action}")
            print(f"[LoopDetector] Recent history: {self._get_recent_actions(5)}")

    def _check_repetition(self, action: str, current_time: float) -> None:
        """Check if action repeats too many times"""
        # Get recent actions within time window
        cutoff_time = current_time - self.config.repetition_window
        recent_actions = [
            record for record in self.action_history
            if record.timestamp >= cutoff_time
        ]

        # Count how many times this action appears
        repetition_count = sum(
            1 for record in recent_actions
            if record.action == action
        )

        if repetition_count >= self.config.max_action_repetitions:
            raise LoopDetected(
                f"Action '{action}' repeated {repetition_count} times "
                f"within {self.config.repetition_window}s window"
            )

    def _get_recent_actions(self, count: int) -> List[str]:
        """Get last N actions for debugging"""
        recent = self.action_history[-count:] if len(self.action_history) >= count else self.action_history
        return [record.action for record in recent]

    def reset(self) -> None:
        """Reset detector state (useful for testing)"""
        self.action_history.clear()
        self.iteration_count = 0

    def get_stats(self) -> Dict:
        """Get detection statistics"""
        return {
            'total_iterations': self.iteration_count,
            'unique_actions': len(set(r.action for r in self.action_history)),
            'total_actions': len(self.action_history),
            'recent_actions': self._get_recent_actions(10)
        }


class LoopDetected(Exception):
    """Raised when a loop is detected"""
    pass


class MaxIterationsExceeded(Exception):
    """Raised when iteration limit is reached"""
    pass


# Example usage
if __name__ == "__main__":
    # Create detector with debug mode
    detector = LoopDetector(
        config=LoopDetectionConfig(
            max_action_repetitions=3,
            max_total_iterations=10,
            debug=True
        )
    )

    try:
        # Simulate agent actions
        detector.check_action("check_logs")
        detector.check_action("check_metrics")
        detector.check_action("restart_pod")
        detector.check_action("check_logs")
        detector.check_action("restart_pod")
        detector.check_action("restart_pod")
        detector.check_action("restart_pod")  # This will raise LoopDetected

    except LoopDetected as e:
        print(f"\n❌ Loop detected: {e}")
        print(f"Stats: {detector.get_stats()}")
```

---

### Using the Loop Detector

**File: `examples/basic_loop.py` (Intentionally broken)**

```python
"""
Example of an agent with an infinite loop (for educational purposes).
This demonstrates what NOT to do.
"""

import asyncio
import random


async def check_pod_status(pod_name: str) -> str:
    """Simulate checking pod status"""
    await asyncio.sleep(0.1)
    # Always return failing status (simulates unfixable issue)
    return "CrashLoopBackOff"


async def restart_pod(pod_name: str) -> None:
    """Simulate pod restart"""
    print(f"🔄 Restarting pod: {pod_name}")
    await asyncio.sleep(0.5)


async def fix_pod_without_detection(pod_name: str):
    """
    ❌ BAD: This will loop forever!

    Problem: Pod is crashing due to missing ConfigMap, which restart
    cannot fix. Agent will retry indefinitely.
    """
    print(f"Starting agent for pod: {pod_name}\n")

    iteration = 0
    while True:
        iteration += 1
        print(f"Iteration {iteration}")

        status = await check_pod_status(pod_name)
        print(f"  Status: {status}")

        if status == "CrashLoopBackOff":
            await restart_pod(pod_name)
            await asyncio.sleep(2)

            # Check again
            new_status = await check_pod_status(pod_name)
            if new_status == "Running":
                print("✅ Pod is now running!")
                break
            else:
                print("  Still failing, retrying...\n")
                # Infinite loop! No escape condition!


if __name__ == "__main__":
    print("="*60)
    print("DEMO: Agent without loop detection (will run forever)")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")

    try:
        asyncio.run(fix_pod_without_detection("my-app-pod"))
    except KeyboardInterrupt:
        print("\n\n⚠️  Agent stopped manually. In production, this would run")
        print("   indefinitely, racking up costs!")
```

**File: `examples/fixed_loop.py` (With detection)**

```python
"""
Example of the same agent WITH loop detection.
This demonstrates proper safeguards.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.loop_detector import LoopDetector, LoopDetectionConfig, LoopDetected, MaxIterationsExceeded


async def check_pod_status(pod_name: str) -> str:
    """Simulate checking pod status"""
    await asyncio.sleep(0.1)
    return "CrashLoopBackOff"


async def restart_pod(pod_name: str) -> None:
    """Simulate pod restart"""
    print(f"🔄 Restarting pod: {pod_name}")
    await asyncio.sleep(0.5)


async def alert_humans(message: str, context: dict) -> None:
    """Simulate alerting on-call engineer"""
    print(f"\n🚨 ALERT TO HUMANS: {message}")
    print(f"   Context: {context}")


async def fix_pod_with_detection(pod_name: str):
    """
    ✅ GOOD: Same logic but with loop detection.

    Agent will detect it's stuck and escalate to humans instead
    of running indefinitely.
    """
    print(f"Starting agent for pod: {pod_name}\n")

    # Create loop detector
    detector = LoopDetector(
        config=LoopDetectionConfig(
            max_action_repetitions=3,
            max_total_iterations=10,
            debug=True
        )
    )

    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\nIteration {iteration}")

            # Check action BEFORE performing it
            detector.check_action("check_pod_status", metadata={'pod': pod_name})
            status = await check_pod_status(pod_name)
            print(f"  Status: {status}")

            if status == "CrashLoopBackOff":
                # Check action BEFORE performing it
                detector.check_action("restart_pod", metadata={'pod': pod_name})
                await restart_pod(pod_name)
                await asyncio.sleep(2)

                # Check again
                detector.check_action("check_pod_status", metadata={'pod': pod_name})
                new_status = await check_pod_status(pod_name)

                if new_status == "Running":
                    print("✅ Pod is now running!")
                    break
                else:
                    print("  Still failing, will retry...")

            elif status == "Running":
                print("✅ Pod is running!")
                break

    except LoopDetected as e:
        print(f"\n❌ Loop detected: {e}")
        print(f"\nAgent stats: {detector.get_stats()}")

        # Escalate to humans instead of continuing
        await alert_humans(
            "Agent stuck in loop while fixing pod",
            {
                'pod': pod_name,
                'stats': detector.get_stats(),
                'error': str(e)
            }
        )

        print("\n✅ Agent stopped safely and alerted humans")

    except MaxIterationsExceeded as e:
        print(f"\n⚠️  Max iterations exceeded: {e}")
        print(f"\nAgent stats: {detector.get_stats()}")

        await alert_humans(
            "Agent exceeded max iterations",
            {
                'pod': pod_name,
                'stats': detector.get_stats()
            }
        )

        print("\n✅ Agent stopped safely after iteration limit")


if __name__ == "__main__":
    print("="*60)
    print("DEMO: Agent WITH loop detection")
    print("="*60 + "\n")

    asyncio.run(fix_pod_with_detection("my-app-pod"))
```

**Run the examples:**

```bash
# This will loop forever (press Ctrl+C to stop)
python examples/basic_loop.py

# This will detect the loop and stop safely
python examples/fixed_loop.py
```

**Expected Output (fixed_loop.py):**

```
============================================================
DEMO: Agent WITH loop detection
============================================================

Starting agent for pod: my-app-pod

Iteration 1
[LoopDetector] Action 1: check_pod_status
[LoopDetector] Recent history: ['check_pod_status']
  Status: CrashLoopBackOff
[LoopDetector] Action 2: restart_pod
[LoopDetector] Recent history: ['check_pod_status', 'restart_pod']
🔄 Restarting pod: my-app-pod
[LoopDetector] Action 3: check_pod_status
[LoopDetector] Recent history: ['check_pod_status', 'restart_pod', 'check_pod_status']
  Still failing, will retry...

Iteration 2
[LoopDetector] Action 4: check_pod_status
[LoopDetector] Recent history: ['check_pod_status', 'restart_pod', 'check_pod_status', 'check_pod_status']
  Status: CrashLoopBackOff
[LoopDetector] Action 5: restart_pod
[LoopDetector] Recent history: ['restart_pod', 'check_pod_status', 'check_pod_status', 'restart_pod']
🔄 Restarting pod: my-app-pod
[LoopDetector] Action 6: check_pod_status
[LoopDetector] Recent history: ['check_pod_status', 'check_pod_status', 'restart_pod', 'check_pod_status']
  Still failing, will retry...

Iteration 3
[LoopDetector] Action 7: check_pod_status

❌ Loop detected: Action 'check_pod_status' repeated 3 times within 60s window

Agent stats: {'total_iterations': 7, 'unique_actions': 2, 'total_actions': 7, 'recent_actions': ['check_pod_status', 'restart_pod', 'check_pod_status', 'check_pod_status', 'restart_pod', 'check_pod_status', 'check_pod_status']}

🚨 ALERT TO HUMANS: Agent stuck in loop while fixing pod
   Context: {'pod': 'my-app-pod', 'stats': {...}, 'error': '...'}

✅ Agent stopped safely and alerted humans
```

---

### IDE Integration and Debugging

**VS Code Setup:**

1. **Install Python extension**
   - Open VS Code
   - Install "Python" extension by Microsoft

2. **Create debug configuration**

**File: `.vscode/launch.json`**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Agent Loop Detection",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/examples/fixed_loop.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Debug Broken Agent",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/examples/basic_loop.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

3. **Set breakpoints**
   - Open `src/loop_detector.py`
   - Click left margin on line 85 (`def _check_repetition`)
   - Click left margin on line 103 (where `LoopDetected` is raised)

4. **Debug workflow**
   - Press F5 to start debugging
   - Step through code with F10 (step over) or F11 (step into)
   - Inspect `self.action_history` in Variables panel
   - Watch loop detection logic execute in real-time

**Debugging Tips:**

```python
# Add this to your agent code for detailed logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('agent_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# In your agent
logger.debug(f"Action history: {detector.action_history}")
logger.info(f"Iteration {iteration}, status: {status}")
logger.warning(f"Pod still failing after {retry_count} retries")
```

---

## Section 4: DevOps Detection Strategies — Production Monitoring

Development loop detection is great for testing, but production systems need real-time monitoring and alerting. Let's build production-grade observability.

### Installing Prometheus and Grafana

**Prometheus** is the industry standard for metrics collection in Kubernetes and cloud environments.

**Installation Instructions:**

```bash
# Option 1: Docker Compose (quickest for local testing)
mkdir monitoring
cd monitoring

# Create docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus

  # Your agent application
  agent-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:
EOF

# Create Prometheus config
cat > prometheus.yml <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'agent-app'
    static_configs:
      - targets: ['agent-app:8000']
EOF

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

**Option 2: Kubernetes (production)**

```bash
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus + Grafana
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=admin

# Port-forward to access
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

**Access the services:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

---

### Instrumenting Your Agent with Prometheus Metrics

**Installation:**

```bash
pip install prometheus-client
```

**File: `src/monitored_agent.py`**

```python
"""
Production agent with Prometheus metrics.

This agent exposes metrics for monitoring loop detection,
execution times, token usage, and costs in real-time.
"""

import time
import asyncio
from typing import Dict, Optional
from prometheus_client import Counter, Histogram, Gauge, Info, start_http_server

from loop_detector import LoopDetector, LoopDetectionConfig, LoopDetected


# Define Prometheus metrics
# =========================

# Counter: Monotonically increasing values
agent_executions_total = Counter(
    'agent_executions_total',
    'Total number of agent executions',
    ['status', 'agent_type']  # Labels for filtering
)

agent_loops_detected_total = Counter(
    'agent_loops_detected_total',
    'Total loops detected and prevented',
    ['loop_type', 'agent_type']
)

agent_token_usage_total = Counter(
    'agent_tokens_used_total',
    'Total tokens consumed',
    ['model', 'token_type']  # token_type: input/output
)

agent_cost_dollars_total = Counter(
    'agent_cost_dollars_total',
    'Total estimated cost in USD',
    ['model']
)

# Histogram: Track distribution of values
agent_execution_duration_seconds = Histogram(
    'agent_execution_duration_seconds',
    'Time spent executing agent tasks',
    ['agent_type'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 120.0]
)

agent_iteration_count = Histogram(
    'agent_iteration_count',
    'Number of iterations before completion or loop detection',
    ['agent_type'],
    buckets=[1, 3, 5, 10, 15, 20, 30, 50, 100]
)

# Gauge: Values that can go up or down
agent_active_count = Gauge(
    'agent_active_count',
    'Number of currently active agents',
    ['agent_type']
)

agent_queue_length = Gauge(
    'agent_queue_length',
    'Number of tasks waiting in queue'
)

# Info: Metadata about the agent
agent_info = Info(
    'agent_version',
    'Agent version and configuration'
)

# Set agent info once at startup
agent_info.info({
    'version': '1.0.0',
    'python': '3.11',
    'loop_detection': 'enabled'
})


class MonitoredAgent:
    """
    Production agent with comprehensive Prometheus monitoring.

    Tracks:
    - Execution times and counts
    - Loop detection events
    - Token usage and costs
    - Active agent count
    """

    def __init__(
        self,
        agent_type: str = "pod_fixer",
        model: str = "claude-3-5-sonnet-20241022"
    ):
        self.agent_type = agent_type
        self.model = model
        self.loop_detector = LoopDetector(
            config=LoopDetectionConfig(
                max_action_repetitions=3,
                max_total_iterations=20,
                debug=False  # Disable debug in production
            )
        )

        # Token pricing (as of 2024)
        self.token_prices = {
            'claude-3-5-sonnet-20241022': {
                'input': 3.00 / 1_000_000,   # $3 per 1M tokens
                'output': 15.00 / 1_000_000   # $15 per 1M tokens
            },
            'claude-3-opus-20240229': {
                'input': 15.00 / 1_000_000,
                'output': 75.00 / 1_000_000
            }
        }

    async def execute(self, task: str, **kwargs) -> Dict:
        """
        Execute agent task with full monitoring.

        Args:
            task: Task to perform (e.g., "fix_pod", "analyze_logs")
            **kwargs: Task-specific parameters

        Returns:
            Result dictionary with status and details
        """
        # Track active agents
        agent_active_count.labels(agent_type=self.agent_type).inc()

        # Start execution timer
        start_time = time.time()

        try:
            # Execute task
            result = await self._execute_task(task, **kwargs)

            # Record success
            agent_executions_total.labels(
                status='success',
                agent_type=self.agent_type
            ).inc()

            # Record token usage and cost
            if 'tokens' in result:
                self._record_tokens(result['tokens'])

            return result

        except LoopDetected as e:
            # Record loop detection
            agent_loops_detected_total.labels(
                loop_type='action_repetition',
                agent_type=self.agent_type
            ).inc()

            agent_executions_total.labels(
                status='loop_detected',
                agent_type=self.agent_type
            ).inc()

            # Re-raise for handling upstream
            raise

        except Exception as e:
            # Record failure
            agent_executions_total.labels(
                status='error',
                agent_type=self.agent_type
            ).inc()

            raise

        finally:
            # Record execution time
            duration = time.time() - start_time
            agent_execution_duration_seconds.labels(
                agent_type=self.agent_type
            ).observe(duration)

            # Record iteration count
            agent_iteration_count.labels(
                agent_type=self.agent_type
            ).observe(self.loop_detector.iteration_count)

            # Track active agents
            agent_active_count.labels(agent_type=self.agent_type).dec()

    async def _execute_task(self, task: str, **kwargs) -> Dict:
        """
        Internal task execution logic.

        This is where your actual agent logic goes.
        """
        if task == "fix_pod":
            return await self._fix_pod(kwargs.get('pod_name'))
        elif task == "analyze_logs":
            return await self._analyze_logs(kwargs.get('log_file'))
        else:
            raise ValueError(f"Unknown task: {task}")

    async def _fix_pod(self, pod_name: str) -> Dict:
        """Example task: Fix failing pod"""
        iteration = 0
        max_iterations = 10

        while iteration < max_iterations:
            iteration += 1

            # Check action before performing
            self.loop_detector.check_action("check_pod_status")

            # Simulate checking pod
            status = await self._check_pod_status(pod_name)

            if status == "Running":
                return {
                    'status': 'success',
                    'message': f'Pod {pod_name} is running',
                    'iterations': iteration,
                    'tokens': {'input': 1000, 'output': 500}
                }

            # Check action before performing
            self.loop_detector.check_action("restart_pod")

            # Simulate restart
            await self._restart_pod(pod_name)
            await asyncio.sleep(2)

        return {
            'status': 'failed',
            'message': f'Could not fix pod after {max_iterations} attempts',
            'iterations': iteration
        }

    async def _check_pod_status(self, pod_name: str) -> str:
        """Simulate Kubernetes API call"""
        await asyncio.sleep(0.1)
        # In real implementation, call K8s API
        return "CrashLoopBackOff"  # Always failing for demo

    async def _restart_pod(self, pod_name: str) -> None:
        """Simulate pod restart"""
        await asyncio.sleep(0.5)
        # In real implementation, kubectl delete pod

    async def _analyze_logs(self, log_file: str) -> Dict:
        """Example task: Analyze logs"""
        # Implementation here
        pass

    def _record_tokens(self, tokens: Dict[str, int]):
        """Record token usage and cost"""
        input_tokens = tokens.get('input', 0)
        output_tokens = tokens.get('output', 0)

        # Record token counts
        agent_token_usage_total.labels(
            model=self.model,
            token_type='input'
        ).inc(input_tokens)

        agent_token_usage_total.labels(
            model=self.model,
            token_type='output'
        ).inc(output_tokens)

        # Calculate and record cost
        if self.model in self.token_prices:
            prices = self.token_prices[self.model]
            cost = (
                input_tokens * prices['input'] +
                output_tokens * prices['output']
            )

            agent_cost_dollars_total.labels(model=self.model).inc(cost)


# Main application
async def main():
    """Run agent with Prometheus metrics server"""

    # Start Prometheus metrics HTTP server
    # Metrics will be available at http://localhost:8000/metrics
    start_http_server(8000)
    print("✅ Prometheus metrics server started on http://localhost:8000/metrics")

    # Create agent
    agent = MonitoredAgent(agent_type="pod_fixer")

    # Simulate work
    print("\nSimulating agent work...")
    for i in range(5):
        print(f"\n--- Task {i+1} ---")
        try:
            result = await agent.execute("fix_pod", pod_name=f"my-app-{i}")
            print(f"Result: {result['status']}")
        except LoopDetected as e:
            print(f"❌ Loop detected: {e}")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(1)

    # Keep server running for scraping
    print("\n✅ Agent work complete. Metrics server still running...")
    print("   View metrics: http://localhost:8000/metrics")
    print("   Press Ctrl+C to stop")

    try:
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\n\nShutting down...")


if __name__ == "__main__":
    asyncio.run(main())
```

**Run the monitored agent:**

```bash
python src/monitored_agent.py
```

**View metrics in browser:**

Navigate to http://localhost:8000/metrics and you'll see:

```
# HELP agent_executions_total Total number of agent executions
# TYPE agent_executions_total counter
agent_executions_total{agent_type="pod_fixer",status="success"} 2.0
agent_executions_total{agent_type="pod_fixer",status="loop_detected"} 1.0

# HELP agent_loops_detected_total Total loops detected and prevented
# TYPE agent_loops_detected_total counter
agent_loops_detected_total{agent_type="pod_fixer",loop_type="action_repetition"} 1.0

# HELP agent_execution_duration_seconds Time spent executing agent tasks
# TYPE agent_execution_duration_seconds histogram
agent_execution_duration_seconds_bucket{agent_type="pod_fixer",le="0.1"} 0.0
agent_execution_duration_seconds_bucket{agent_type="pod_fixer",le="0.5"} 0.0
agent_execution_duration_seconds_bucket{agent_type="pod_fixer",le="1.0"} 0.0
agent_execution_duration_seconds_bucket{agent_type="pod_fixer",le="2.0"} 1.0
agent_execution_duration_seconds_bucket{agent_type="pod_fixer",le="5.0"} 3.0
agent_execution_duration_seconds_sum{agent_type="pod_fixer"} 12.5
agent_execution_duration_seconds_count{agent_type="pod_fixer"} 3.0

# HELP agent_cost_dollars_total Total estimated cost in USD
# TYPE agent_cost_dollars_total counter
agent_cost_dollars_total{model="claude-3-5-sonnet-20241022"} 0.0225
```

---

### Creating Grafana Dashboards

Now let's visualize these metrics in Grafana.

**Step 1: Add Prometheus Data Source**

1. Open Grafana: http://localhost:3000
2. Login (admin/admin)
3. Go to Configuration → Data Sources
4. Click "Add data source"
5. Select "Prometheus"
6. URL: `http://prometheus:9090` (or `http://localhost:9090` if running locally)
7. Click "Save & Test"

**Step 2: Import Dashboard**

Create a file `grafana-dashboard.json`:

```json
{
  "dashboard": {
    "title": "Agent Loop Detection Dashboard",
    "tags": ["agent", "loops", "monitoring"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Agent Execution Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [{
          "expr": "rate(agent_executions_total[5m])",
          "legendFormat": "{{status}} - {{agent_type}}"
        }],
        "yaxes": [{
          "format": "ops",
          "label": "Executions/sec"
        }]
      },
      {
        "id": 2,
        "title": "Loop Detection Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [{
          "expr": "rate(agent_loops_detected_total[5m])",
          "legendFormat": "{{loop_type}} - {{agent_type}}"
        }],
        "yaxes": [{
          "format": "ops",
          "label": "Loops/sec"
        }],
        "alert": {
          "name": "High Loop Detection Rate",
          "conditions": [{
            "evaluator": {"params": [0.1], "type": "gt"},
            "query": {"params": ["A", "5m", "now"]},
            "reducer": {"type": "avg"},
            "type": "query"
          }],
          "frequency": "60s",
          "handler": 1,
          "message": "Loop detection rate is abnormally high",
          "noDataState": "no_data",
          "executionErrorState": "alerting"
        }
      },
      {
        "id": 3,
        "title": "Execution Duration (P95)",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [{
          "expr": "histogram_quantile(0.95, rate(agent_execution_duration_seconds_bucket[5m]))",
          "legendFormat": "P95 - {{agent_type}}"
        }],
        "yaxes": [{
          "format": "s",
          "label": "Duration"
        }]
      },
      {
        "id": 4,
        "title": "Token Usage Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [{
          "expr": "rate(agent_tokens_used_total[5m])",
          "legendFormat": "{{token_type}} - {{model}}"
        }],
        "yaxes": [{
          "format": "short",
          "label": "Tokens/sec"
        }]
      },
      {
        "id": 5,
        "title": "Estimated Cost (Hourly Rate)",
        "type": "singlestat",
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 16},
        "targets": [{
          "expr": "rate(agent_cost_dollars_total[1h]) * 3600"
        }],
        "format": "currencyUSD",
        "prefix": "$",
        "postfix": "/hour"
      },
      {
        "id": 6,
        "title": "Active Agents",
        "type": "gauge",
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 16},
        "targets": [{
          "expr": "agent_active_count"
        }],
        "thresholds": "10,20,30"
      }
    ]
  }
}
```

**Import the dashboard:**
1. Grafana → Create → Import
2. Upload `grafana-dashboard.json`
3. Select Prometheus data source
4. Click "Import"

---

### Setting Up Alerts

**File: `prometheus-alerts.yml`**

```yaml
groups:
  - name: agent_loop_alerts
    interval: 30s
    rules:
      # Alert when loop detection rate is high
      - alert: HighLoopDetectionRate
        expr: rate(agent_loops_detected_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High loop detection rate"
          description: "Agent {{$labels.agent_type}} is detecting loops at {{$value}} loops/sec"

      # Alert when execution time is abnormally high
      - alert: SlowAgentExecution
        expr: histogram_quantile(0.95, rate(agent_execution_duration_seconds_bucket[5m])) > 60
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow agent execution"
          description: "P95 execution time is {{$value}}s for {{$labels.agent_type}}"

      # Alert when cost rate is high
      - alert: HighCostRate
        expr: rate(agent_cost_dollars_total[1h]) * 3600 > 10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "High API cost rate"
          description: "Agent costs are ${{$value}}/hour"

      # Alert when no agents are running (might indicate crash)
      - alert: NoActiveAgents
        expr: sum(agent_active_count) == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "No active agents"
          description: "All agents appear to be down"
```

**Update `prometheus.yml` to include alerts:**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

# Load alert rules
rule_files:
  - 'prometheus-alerts.yml'

# Configure Alertmanager (optional)
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: 'agent-app'
    static_configs:
      - targets: ['agent-app:8000']
```

**Reload Prometheus config:**

```bash
# If using Docker Compose
docker-compose restart prometheus

# If using Kubernetes
kubectl rollout restart -n monitoring statefulset/prometheus-monitoring-kube-prometheus-prometheus
```

### Cost-Benefit Analysis: How Much Monitoring Is Enough?

Production monitoring has costs (infrastructure, maintenance, alert fatigue). Here's how to right-size your monitoring investment.

#### The Monitoring ROI Formula

```
Monitoring Value = (Cost of Undetected Loop) × (Loop Probability) - (Monitoring Cost)

Example calculation:
  Undetected loop cost: $10,000 average
  Loop probability: 5% per month (based on historical data)
  Expected loss without monitoring: $10,000 × 0.05 = $500/month

  Monitoring costs:
    Prometheus + Grafana: $50/month (hosted)
    Setup time: 8 hours × $150/hr = $1,200 (one-time)
    Maintenance: 2 hours/month × $150/hr = $300/month

  Break-even analysis:
    Month 1: -$1,200 - $350 + $500 = -$1,050 (investment)
    Month 2: -$350 + $500 = +$150 (positive ROI)
    Month 3+: +$150/month ongoing savings

  Decision: Implement monitoring (pays for itself in 2 months)
```

#### Monitoring Tiers: What to Implement When

**Tier 1: Minimum Viable Monitoring** (Free, 2 hours setup)

```yaml
What you get:
  - Basic loop detection in code (StateTracker)
  - Log-based alerts (grep for "loop detected")
  - Manual cost checks (AWS/Anthropic dashboards)

When sufficient:
  - Development/staging environments
  - Low-stakes agents (documentation, code review)
  - Budget: $0-$100/month in agent costs

Implementation:
  ✅ Add StateTracker to all agents
  ✅ Set up daily log review
  ✅ Configure cost alerts in billing dashboard
```

**Tier 2: Production Monitoring** ($50-200/month, 8 hours setup)

```yaml
What you add:
  - Prometheus metrics collection
  - Grafana dashboards
  - Automated alerting (PagerDuty/Slack)
  - Cost tracking per agent

When necessary:
  - Production agents handling infrastructure
  - Budget: $500-$5,000/month in agent costs
  - Team size: 3+ engineers

Implementation:
  ✅ Deploy Prometheus + Grafana
  ✅ Instrument agents with metrics
  ✅ Create 3-5 key dashboards
  ✅ Set up alerting rules
```

**Tier 3: Enterprise Monitoring** ($500-2,000/month, 40 hours setup)

```yaml
What you add:
  - Distributed tracing (Jaeger/DataDog)
  - Advanced anomaly detection (ML-based)
  - Cost forecasting and budgets
  - Multi-region monitoring
  - Compliance and audit logging

When necessary:
  - Critical production agents (payment, security)
  - Budget: $10,000+/month in agent costs
  - Team size: 10+ engineers
  - Regulatory requirements (SOC 2, HIPAA)

Implementation:
  ✅ Full observability stack (Datadog/New Relic)
  ✅ Custom anomaly detection models
  ✅ Integration with incident management
  ✅ Automated remediation workflows
```

#### Common Monitoring Mistakes

**Mistake 1: Over-monitoring in development**

```yaml
Problem:
  Team spends 40 hours setting up full Prometheus stack for dev environment
  Agents only cost $50/month
  Time investment: 40 hrs × $150 = $6,000
  ROI: Never (overkill)

Better approach:
  Use Tier 1 monitoring (2 hours)
  Graduate to Tier 2 when agent costs hit $500/month
```

**Mistake 2: Alert fatigue from unnecessary alerts**

```yaml
Problem:
  Alert on EVERY loop detection
  Dev environment triggers 50 alerts/day
  Team starts ignoring alerts
  Real production loop goes unnoticed

Better approach:
  Tier alerts by severity:
    - CRITICAL: Production loop or cost >$100/hour
    - WARNING: Staging loop or cost >$10/hour
    - INFO: Dev loop (log only, no alert)

  Alert routing:
    - Critical: PagerDuty (wakes on-call)
    - Warning: Slack (during business hours)
    - Info: Log aggregation only
```

**Mistake 3: Monitoring but not acting**

```yaml
Scenario:
  Grafana dashboard shows agent loops increasing
  Week 1: 5 loops
  Week 2: 12 loops
  Week 3: 25 loops
  Week 4: Production incident

Problem: Saw the trend, didn't act

Solution: Automated response thresholds
  - 5 loops/week: Team review (30 min meeting)
  - 10 loops/week: Mandatory fix sprint
  - 15 loops/week: Disable agent until fixed

Monitoring without action = expensive dashboard art
```

#### Decision Framework: When to Upgrade Monitoring

```
Current State: Tier 1 (Basic)
Evaluate monthly:

Upgrade to Tier 2 if ANY of:
  ✅ Agent costs >$500/month
  ✅ 3+ loop incidents in past month
  ✅ Team size >3 engineers
  ✅ Agents in production (not just dev)
  ✅ Loop caused >$1,000 in costs

Upgrade to Tier 3 if ANY of:
  ✅ Agent costs >$10,000/month
  ✅ Critical infrastructure automation
  ✅ Regulatory compliance requirements
  ✅ Multi-team/multi-region deployment
  ✅ Loop caused service outage
```

#### Real-World Cost Example

**Startup: TechCorp (30 engineers, 5 production agents)**

```yaml
Monitoring evolution:

Month 1 (Tier 1 - Basic):
  Setup: 2 hours
  Cost: $0
  Agent spend: $150
  Loops detected: 0
  Status: ✅ Appropriate

Month 3 (Tier 1):
  Agent spend: $800
  Loops detected: 2 (caught by StateTracker)
  Costs avoided: ~$2,000
  Status: ✅ Still appropriate

Month 6 (Agent costs hit $2,500/month):
  Decision: Upgrade to Tier 2
  Setup: 8 hours over 2 weeks
  Monthly cost: $100 (Grafana Cloud)
  Benefit: Real-time detection vs daily log review

Month 12:
  Agent spend: $6,000/month
  Monitoring prevented 3 major loops
  Estimated savings: $15,000
  Monitoring ROI: ($15,000 - $1,400) / $1,400 = 971% ROI
```

**Key insight**: Monitoring investment scales with agent usage. Don't over-invest early, but don't delay when agents reach production scale.

---

## Section 5: DevSecOps — Security Implications of Agent Loops

Agent loops aren't just operational problems—they're security vulnerabilities. Let's explore the security implications and mitigation strategies.

### Denial of Wallet (DoW) Attacks

**What is a DoW attack?**

A Denial of Wallet attack exploits cloud billing models by causing your system to consume excessive resources, resulting in massive bills.

**Attack Scenario:**

```python
# Malicious input designed to trigger loop
malicious_log_entry = """
ERROR: Failed to process request
CAUSE: Unknown
SOLUTION: Retry immediately
""" * 10000  # 10,000 repetitions

# Agent analyzes this log
# Claude API costs $0.03 per analysis
# Agent retries 1,000 times = $30
# Attacker repeats 100 times = $3,000 in bills
```

**Real-World Example:**

In 2023, a researcher demonstrated a DoW attack against an AI-powered customer support system:
1. Attacker sent specially crafted queries
2. AI agent entered infinite loop trying to "understand" the query
3. Company's Claude API bill went from $500/month to $15,000 in one weekend
4. Attack cost attacker: $0 (free tier account)

**Mitigation Strategy:**

**File: `src/secure_agent.py`**

```python
"""
Security-hardened agent with DoW protection.
"""

import time
import asyncio
from typing import Dict, Optional
from prometheus_client import Counter

# Security metrics
dow_attempts_blocked = Counter(
    'dow_attempts_blocked_total',
    'Denial of Wallet attempts blocked'
)

rate_limit_exceeded = Counter(
    'rate_limit_exceeded_total',
    'Rate limit exceeded events'
)


class RateLimiter:
    """
    Token bucket rate limiter to prevent DoW attacks.

    Limits both requests per second and total cost per hour.
    """

    def __init__(
        self,
        max_requests_per_minute: int = 60,
        max_cost_per_hour: float = 10.0
    ):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_cost_per_hour = max_cost_per_hour

        # Sliding window for requests
        self.request_timestamps = []

        # Cost tracking
        self.hourly_costs = []

    def allow_request(self) -> bool:
        """Check if request is allowed under rate limit"""
        current_time = time.time()

        # Clean old requests (older than 1 minute)
        cutoff = current_time - 60
        self.request_timestamps = [
            ts for ts in self.request_timestamps if ts > cutoff
        ]

        # Check rate limit
        if len(self.request_timestamps) >= self.max_requests_per_minute:
            rate_limit_exceeded.inc()
            return False

        # Allow request
        self.request_timestamps.append(current_time)
        return True

    def record_cost(self, cost: float):
        """Record API cost"""
        current_time = time.time()

        # Clean old costs (older than 1 hour)
        cutoff = current_time - 3600
        self.hourly_costs = [
            (ts, c) for ts, c in self.hourly_costs if ts > cutoff
        ]

        # Add new cost
        self.hourly_costs.append((current_time, cost))

    def get_hourly_cost(self) -> float:
        """Get total cost in last hour"""
        return sum(cost for _, cost in self.hourly_costs)

    def allow_cost(self, estimated_cost: float) -> bool:
        """Check if cost is allowed"""
        current_hourly_cost = self.get_hourly_cost()

        if current_hourly_cost + estimated_cost > self.max_cost_per_hour:
            dow_attempts_blocked.inc()
            return False

        return True


class SecureAgent:
    """
    Security-hardened agent with DoW protection,
    rate limiting, and audit logging.
    """

    def __init__(self):
        self.rate_limiter = RateLimiter(
            max_requests_per_minute=60,  # 1 req/sec average
            max_cost_per_hour=10.0        # $10/hour max
        )
        self.audit_log = []

    async def execute(self, task: str, **kwargs) -> Dict:
        """Execute task with security checks"""

        # Security check 1: Rate limiting
        if not self.rate_limiter.allow_request():
            self._audit_log('rate_limit_exceeded', task, kwargs)
            raise RateLimitExceeded(
                f"Rate limit exceeded: {self.rate_limiter.max_requests_per_minute} req/min"
            )

        # Security check 2: Cost budget
        estimated_cost = self._estimate_cost(task, kwargs)
        if not self.rate_limiter.allow_cost(estimated_cost):
            self._audit_log('cost_limit_exceeded', task, kwargs)
            raise CostLimitExceeded(
                f"Cost limit exceeded: ${self.rate_limiter.max_cost_per_hour}/hour"
            )

        # Security check 3: Input validation
        self._validate_input(task, kwargs)

        # Execute task
        try:
            result = await self._execute_task(task, **kwargs)

            # Record actual cost
            actual_cost = result.get('cost', estimated_cost)
            self.rate_limiter.record_cost(actual_cost)

            self._audit_log('success', task, kwargs, result)
            return result

        except Exception as e:
            self._audit_log('error', task, kwargs, error=str(e))
            raise

    def _estimate_cost(self, task: str, kwargs: Dict) -> float:
        """
        Estimate API cost before execution.

        Prevents expensive operations from starting if budget exhausted.
        """
        # Estimate tokens based on input size
        input_size = len(str(kwargs))
        estimated_input_tokens = input_size * 0.75  # Rough estimate

        # Assume 2:1 output ratio
        estimated_output_tokens = estimated_input_tokens * 2

        # Claude 3.5 Sonnet pricing
        cost = (
            estimated_input_tokens * (3.00 / 1_000_000) +
            estimated_output_tokens * (15.00 / 1_000_000)
        )

        return cost

    def _validate_input(self, task: str, kwargs: Dict):
        """
        Validate input to prevent injection attacks and DoW.
        """
        # Check 1: Input size limit (prevent massive token usage)
        input_str = str(kwargs)
        if len(input_str) > 100_000:  # 100KB limit
            raise InputTooLarge(f"Input size {len(input_str)} exceeds 100KB limit")

        # Check 2: Detect repetitive patterns (DoW indicator)
        if self._is_repetitive(input_str):
            dow_attempts_blocked.inc()
            raise SuspiciousInput("Input contains repetitive patterns (possible DoW attack)")

        # Check 3: Task whitelist
        allowed_tasks = ['fix_pod', 'analyze_logs', 'check_metrics']
        if task not in allowed_tasks:
            raise UnauthorizedTask(f"Task '{task}' not in whitelist")

    def _is_repetitive(self, text: str, threshold: float = 0.8) -> bool:
        """
        Detect if text is suspiciously repetitive.

        Uses simple compression ratio heuristic:
        If zlib compresses text by >80%, it's highly repetitive.
        """
        import zlib

        compressed = zlib.compress(text.encode())
        compression_ratio = len(compressed) / len(text.encode())

        return compression_ratio < (1 - threshold)

    def _audit_log(self, event: str, task: str, kwargs: Dict, result: Optional[Dict] = None, error: Optional[str] = None):
        """
        Audit log for security compliance (SOC 2, GDPR, etc.)
        """
        log_entry = {
            'timestamp': time.time(),
            'event': event,
            'task': task,
            'input_size': len(str(kwargs)),
            'result': result,
            'error': error
        }

        self.audit_log.append(log_entry)

        # In production, send to logging system (Splunk, ELK, etc.)
        print(f"[AUDIT] {event}: {task}")

    async def _execute_task(self, task: str, **kwargs) -> Dict:
        """Execute the actual task"""
        # Implementation here
        pass


class RateLimitExceeded(Exception):
    pass


class CostLimitExceeded(Exception):
    pass


class InputTooLarge(Exception):
    pass


class SuspiciousInput(Exception):
    pass


class UnauthorizedTask(Exception):
    pass
```

**Testing DoW Protection:**

```python
# Test script
async def test_dow_protection():
    agent = SecureAgent()

    # Test 1: Normal operation
    print("Test 1: Normal operation")
    try:
        result = await agent.execute("fix_pod", pod_name="my-app")
        print(f"✅ Success: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # Test 2: Rate limiting
    print("\nTest 2: Rate limiting (61 requests in 1 minute)")
    for i in range(65):
        try:
            await agent.execute("fix_pod", pod_name=f"pod-{i}")
        except RateLimitExceeded as e:
            print(f"✅ Rate limit kicked in at request {i+1}: {e}")
            break

    # Test 3: Repetitive input (DoW attempt)
    print("\nTest 3: Repetitive input detection")
    malicious_input = "ERROR: retry immediately\n" * 10000
    try:
        await agent.execute("analyze_logs", log_data=malicious_input)
    except SuspiciousInput as e:
        print(f"✅ DoW attempt blocked: {e}")

    # Test 4: Input too large
    print("\nTest 4: Input size limit")
    massive_input = "x" * 200_000  # 200KB
    try:
        await agent.execute("analyze_logs", log_data=massive_input)
    except InputTooLarge as e:
        print(f"✅ Large input blocked: {e}")


if __name__ == "__main__":
    asyncio.run(test_dow_protection())
```

---

### Secrets Management and Rotation

Agent loops can expose API keys in logs and error messages. Let's implement secure secrets management.

**Installing HashiCorp Vault (for local development):**

```bash
# Option 1: Docker
docker run -d --name=vault --cap-add=IPC_LOCK \
  -p 8200:8200 \
  -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' \
  vault:latest

# Set environment variables
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='myroot'

# Verify
docker exec vault vault status
```

**File: `src/secrets_manager.py`**

```python
"""
Secure secrets management with HashiCorp Vault.

Rotates API keys automatically during circuit breaker recovery.
"""

import hvac
import os
from typing import Dict, Optional


class SecretsManager:
    """
    Manage secrets with Vault.

    Features:
    - Automatic rotation
    - Audit logging
    - Lease management
    """

    def __init__(
        self,
        vault_addr: Optional[str] = None,
        vault_token: Optional[str] = None
    ):
        self.vault_addr = vault_addr or os.getenv('VAULT_ADDR', 'http://localhost:8200')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN')

        self.client = hvac.Client(
            url=self.vault_addr,
            token=self.vault_token
        )

        if not self.client.is_authenticated():
            raise ValueError("Vault authentication failed")

    def get_secret(self, path: str, rotate: bool = False) -> Dict:
        """
        Retrieve secret from Vault.

        Args:
            path: Secret path (e.g., 'secret/claude/api-key')
            rotate: If True, rotate secret after retrieval

        Returns:
            Secret data dictionary
        """
        # Read current secret
        secret = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point='secret'
        )

        secret_data = secret['data']['data']

        if rotate:
            # Generate new API key (implementation depends on provider)
            new_value = self._rotate_api_key(secret_data['value'])

            # Write new secret
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret={'value': new_value},
                mount_point='secret'
            )

            return {'value': new_value}

        return secret_data

    def _rotate_api_key(self, current_key: str) -> str:
        """
        Rotate API key with provider.

        In production, this would call Anthropic API to generate
        new key and revoke old one.
        """
        # Placeholder: In real implementation, call provider API
        print(f"Rotating API key (current: {current_key[:8]}...)")
        return f"sk-ant-new-key-{os.urandom(16).hex()}"


# Integration with SecureAgent
class VaultIntegratedAgent(SecureAgent):
    """Agent with Vault secrets integration"""

    def __init__(self):
        super().__init__()
        self.secrets = SecretsManager()

    async def execute(self, task: str, **kwargs) -> Dict:
        """Execute with fresh API key from Vault"""

        # Get fresh API key
        secret = self.secrets.get_secret('claude/api-key')
        api_key = secret['value']

        # Use API key in request
        # ... implementation ...

        return await super().execute(task, **kwargs)
```

---

### Audit Logging for Compliance

**File: `src/compliance_logger.py`**

```python
"""
Compliance-grade audit logging for SOC 2, GDPR, PCI-DSS.

Logs all agent actions, detections, and security events.
"""

import json
import time
from typing import Dict, Any
from pathlib import Path


class ComplianceLogger:
    """
    Audit logger for security compliance.

    Features:
    - Tamper-evident logging
    - PII redaction
    - Retention policies
    - Export for audits
    """

    def __init__(self, log_dir: str = "./audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        self.current_log_file = self.log_dir / f"audit-{int(time.time())}.jsonl"

    def log_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        action: Optional[str] = None,
        result: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Log compliance event.

        Args:
            event_type: Event category (execution, loop_detected, error, security_alert)
            user_id: User who triggered agent (if applicable)
            agent_id: Agent identifier
            action: Action performed
            result: success/failure/loop_detected
            metadata: Additional context
        """
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'user_id': self._redact_pii(user_id),
            'agent_id': agent_id,
            'action': action,
            'result': result,
            'metadata': metadata or {}
        }

        # Write to log file (append-only for tamper resistance)
        with open(self.current_log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def _redact_pii(self, data: Optional[str]) -> Optional[str]:
        """
        Redact Personally Identifiable Information.

        Required for GDPR compliance.
        """
        if not data:
            return None

        # Redact email addresses
        import re
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        data = re.sub(email_pattern, '[REDACTED_EMAIL]', data)

        # Redact phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        data = re.sub(phone_pattern, '[REDACTED_PHONE]', data)

        return data

    def export_logs(self, start_time: float, end_time: float) -> str:
        """
        Export logs for audit.

        Returns path to export file.
        """
        export_file = self.log_dir / f"export-{int(time.time())}.jsonl"

        with open(export_file, 'w') as out:
            for log_file in self.log_dir.glob("audit-*.jsonl"):
                with open(log_file) as f:
                    for line in f:
                        event = json.loads(line)
                        if start_time <= event['timestamp'] <= end_time:
                            out.write(line)

        return str(export_file)
```

---

## Section 6: Real-World Scenario — Kubernetes Pod Restart Loop

Let's apply everything we've learned to a real production incident.

### The Incident

**Company:** TechCorp (200-person SaaS startup)
**Date:** March 15, 2024, 2:35 AM
**Incident:** Payment processing service down

**Timeline:**

**2:35 AM** - PagerDuty alert: `payment-service` pod in `CrashLoopBackOff`

**2:36 AM** - AI agent activates automatically (no human intervention yet)

**2:36-2:42 AM** - Agent attempts remediation:
- Iteration 1: Restart pod → still crash looping
- Iteration 2: Increase memory from 512Mi to 1Gi → still crash looping
- Iteration 3: Restart pod again → still crash looping
- **Iteration 4: Loop detector triggers** ✅

**2:42 AM** - Agent escalates to on-call engineer:
```
🚨 ALERT: Agent stuck in loop
Pod: payment-service-7d4f9c8b5-xk2m9
Actions attempted: restart_pod (3×), increase_memory (1×)
Root cause: NOT a resource issue
Recommendation: Check application logs for startup errors
Incident link: https://dashboard.techcorp.com/incidents/INC-9127
```

**2:45 AM** - Engineer investigates logs, finds:
```
ERROR: Database connection failed
Could not connect to postgres://payments-db:5432
Reason: database "payments" does not exist
```

**2:48 AM** - Engineer realizes: Database was accidentally dropped during maintenance
- Restores from backup
- Pod starts successfully

**Total downtime:** 13 minutes (vs 3+ hours without loop detection)

---

### How Loop Detection Saved the Day

**Without loop detection:**
```
Agent would have:
├─ Restarted pod 200+ times over 3 hours
├─ Increased memory to maximum (16Gi)
├─ Scaled replicas thinking it's a load issue
├─ Cost company $2,000 in API calls
└─ NOT alerted humans (thinks it's "handling it")

Engineer would wake up at 6 AM to:
├─ 3 hours of downtime
├─ Angry customers
├─ Lost revenue: ~$50,000
└─ Reputation damage
```

**With loop detection:**
```
Agent:
├─ Detected loop after 4 iterations (2 minutes)
├─ Immediately escalated to human
├─ Provided diagnostic context
└─ Cost: $0.12 in API calls

Engineer:
├─ Woke up at 2:42 AM (7 min after incident)
├─ Had clear context from agent
├─ Fixed root cause in 6 minutes
└─ Total downtime: 13 minutes
```

**ROI Calculation:**
```
Lost revenue prevented: $50,000
API cost saved: $1,999.88
Reputation damage avoided: Priceless

Investment in loop detection:
├─ 2 hours of engineering time: $400
└─ Ongoing cost: $0 (open source)

ROI: 12,400%
```

---

### Implementing This for Your Team

**Step 1: Clone the example code**

```bash
git clone https://github.com/your-repo/agent-loop-detection
cd agent-loop-detection
```

**Step 2: Configure for your environment**

**File: `config.yaml`**

```yaml
# Loop detection configuration
loop_detection:
  enabled: true
  max_action_repetitions: 3
  max_total_iterations: 20
  repetition_window_seconds: 60

# Rate limiting (DoW protection)
rate_limiting:
  enabled: true
  max_requests_per_minute: 60
  max_cost_per_hour: 10.0

# Monitoring
monitoring:
  prometheus:
    enabled: true
    port: 8000
  grafana:
    enabled: true
    dashboard_file: ./grafana-dashboard.json

# Alerting
alerting:
  slack:
    enabled: true
    webhook_url: ${SLACK_WEBHOOK_URL}
  pagerduty:
    enabled: true
    integration_key: ${PAGERDUTY_KEY}

# Security
security:
  vault:
    enabled: true
    address: http://localhost:8200
  audit_logging:
    enabled: true
    log_dir: ./audit_logs
  input_validation:
    max_input_size_bytes: 100000
    detect_repetitive_patterns: true
```

**Step 3: Deploy to Kubernetes**

```bash
# Build Docker image
docker build -t agent-loop-detection:v1.0.0 .

# Push to registry
docker tag agent-loop-detection:v1.0.0 your-registry/agent-loop-detection:v1.0.0
docker push your-registry/agent-loop-detection:v1.0.0

# Deploy
kubectl apply -f k8s/deployment.yaml

# Verify
kubectl get pods -n agents
kubectl logs -n agents deployment/agent-loop-detection --follow
```

**Step 4: Test in staging**

```bash
# Trigger intentional loop in staging
kubectl apply -f test/intentional-loop-scenario.yaml

# Watch agent detect and escalate
kubectl logs -n agents deployment/agent-loop-detection --follow

# Expected output:
# [2024-03-15 14:32:15] INFO: Starting agent for incident INC-TEST-001
# [2024-03-15 14:32:17] INFO: Iteration 1: restart_pod
# [2024-03-15 14:32:22] INFO: Iteration 2: restart_pod
# [2024-03-15 14:32:27] INFO: Iteration 3: restart_pod
# [2024-03-15 14:32:32] ERROR: Loop detected (action 'restart_pod' repeated 3 times)
# [2024-03-15 14:32:32] INFO: Escalating to humans via Slack and PagerDuty
# [2024-03-15 14:32:33] INFO: ✅ Loop detection working correctly
```

**Step 5: Monitor in production**

```bash
# Open Grafana dashboard
open http://localhost:3000/d/agent-loops

# Watch Prometheus metrics
open http://localhost:9090/graph?g0.expr=agent_loops_detected_total

# Check audit logs
cat audit_logs/audit-*.jsonl | jq '.event_type' | sort | uniq -c
```

---

## Section 7: Hands-On Exercise

Time to apply what you've learned! Complete this exercise to solidify your understanding.

### Exercise: Build a Self-Healing Database Connection Agent

**Objective:** Create an agent that automatically fixes database connection issues, with loop detection to prevent infinite retries.

**Scenario:** Your application's database connection sometimes fails due to:
1. Temporary network issues (retryable)
2. Wrong credentials (not retryable)
3. Database server down (retryable up to a point)
4. Connection pool exhausted (retryable)

**Requirements:**
1. Agent must detect and handle all 4 failure types
2. Loop detection must trigger after 3 retry attempts
3. Agent must escalate permanent failures immediately
4. Agent must track and expose Prometheus metrics

---

### Exercise Steps

**Step 1: Set up project**

```bash
mkdir db-connection-agent
cd db-connection-agent
python3 -m venv venv
source venv/bin/activate
pip install asyncio asyncpg prometheus-client pytest pytest-asyncio

mkdir src tests
touch src/__init__.py tests/__init__.py
```

**Step 2: Implement the agent (src/db_agent.py)**

```python
"""
Database connection agent with loop detection.

Your task: Complete the TODOs below.
"""

import asyncio
import asyncpg
from loop_detector import LoopDetector, LoopDetectionConfig, LoopDetected
from prometheus_client import Counter, start_http_server


# TODO 1: Define Prometheus metrics
# Hint: You need counters for:
# - Total connection attempts
# - Successful connections
# - Failed connections (by error type)
# - Loops detected

connection_attempts_total = Counter(
    'db_connection_attempts_total',
    'Total database connection attempts',
    ['status']
)

# TODO: Add more metrics here


class DatabaseConnectionError(Exception):
    """Base class for database connection errors"""
    pass


class CredentialsError(DatabaseConnectionError):
    """Wrong username/password - NOT retryable"""
    pass


class NetworkError(DatabaseConnectionError):
    """Network issue - retryable"""
    pass


class ServerDownError(DatabaseConnectionError):
    """Database server down - retryable"""
    pass


class PoolExhaustedError(DatabaseConnectionError):
    """Connection pool full - retryable"""
    pass


class DBConnectionAgent:
    """
    Agent that automatically handles database connection failures.
    """

    def __init__(
        self,
        db_host: str,
        db_port: int,
        db_name: str,
        db_user: str,
        db_password: str
    ):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

        # TODO 2: Initialize loop detector
        # Hint: Max 3 retries, 20 total iterations
        self.loop_detector = None  # Replace with LoopDetector()

    async def connect(self) -> asyncpg.Connection:
        """
        Connect to database with automatic retry and loop detection.

        Returns:
            Database connection

        Raises:
            LoopDetected: If agent gets stuck in loop
            CredentialsError: If credentials are wrong (not retryable)
        """
        # TODO 3: Implement connection logic with loop detection
        # Steps:
        # 1. Check action with loop detector
        # 2. Try to connect
        # 3. If failure, classify error type
        # 4. Retry if retryable, raise if not
        # 5. Record metrics

        pass  # Replace with implementation

    async def _attempt_connection(self) -> asyncpg.Connection:
        """
        Single connection attempt.

        Raises appropriate error type based on failure reason.
        """
        try:
            conn = await asyncpg.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                timeout=5.0
            )
            return conn

        except asyncpg.InvalidPasswordError:
            raise CredentialsError("Wrong username or password")

        except asyncio.TimeoutError:
            raise NetworkError("Connection timeout")

        except asyncpg.CannotConnectNowError:
            raise ServerDownError("Database server is down")

        except asyncpg.TooManyConnectionsError:
            raise PoolExhaustedError("Connection pool exhausted")

    def _classify_error(self, error: Exception) -> str:
        """
        Classify error as retryable or not.

        Returns:
            "retryable" or "permanent"
        """
        # TODO 4: Implement error classification
        # Hint: CredentialsError is permanent, others are retryable
        pass


async def main():
    """Test the agent"""

    # Start Prometheus metrics server
    start_http_server(8000)
    print("✅ Metrics server: http://localhost:8000/metrics\n")

    # Create agent
    agent = DBConnectionAgent(
        db_host="localhost",
        db_port=5432,
        db_name="testdb",
        db_user="postgres",
        db_password="wrong_password"  # Intentionally wrong!
    )

    # Try to connect
    try:
        conn = await agent.connect()
        print("✅ Connected successfully!")
        await conn.close()
    except LoopDetected as e:
        print(f"❌ Loop detected: {e}")
    except CredentialsError as e:
        print(f"❌ Credentials error (not retryable): {e}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Step 3: Write tests (tests/test_db_agent.py)**

```python
"""
Tests for database connection agent.

Your task: Complete the TODOs below.
"""

import pytest
from src.db_agent import DBConnectionAgent, LoopDetected, CredentialsError


@pytest.mark.asyncio
async def test_successful_connection():
    """Test that agent connects successfully when credentials are correct"""
    # TODO 5: Implement this test
    # Hint: Use a test database or mock
    pass


@pytest.mark.asyncio
async def test_loop_detection_on_network_error():
    """Test that loop detector triggers after 3 network errors"""
    # TODO 6: Implement this test
    # Hint: Mock the connection to always raise NetworkError
    pass


@pytest.mark.asyncio
async def test_immediate_failure_on_credentials_error():
    """Test that agent doesn't retry on credentials error"""
    # TODO 7: Implement this test
    # Hint: Wrong credentials should raise CredentialsError immediately
    pass


# TODO 8: Add more tests for:
# - ServerDownError (should retry)
# - PoolExhaustedError (should retry)
# - Metrics recording
```

**Step 4: Run tests**

```bash
pytest tests/ -v

# Expected output:
# tests/test_db_agent.py::test_successful_connection PASSED
# tests/test_db_agent.py::test_loop_detection_on_network_error PASSED
# tests/test_db_agent.py::test_immediate_failure_on_credentials_error PASSED
```

---

### Solution (Don't Peek!)

<details>
<summary>Click to reveal solution</summary>

```python
# Complete implementation of DBConnectionAgent

class DBConnectionAgent:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

        self.loop_detector = LoopDetector(
            config=LoopDetectionConfig(
                max_action_repetitions=3,
                max_total_iterations=20
            )
        )

    async def connect(self) -> asyncpg.Connection:
        retry_count = 0
        max_retries = 5

        while retry_count < max_retries:
            # Check action with loop detector
            self.loop_detector.check_action("attempt_connection")

            try:
                connection_attempts_total.labels(status='attempt').inc()

                conn = await self._attempt_connection()

                connection_attempts_total.labels(status='success').inc()
                return conn

            except CredentialsError as e:
                # Permanent error - don't retry
                connection_attempts_total.labels(status='credentials_error').inc()
                raise

            except (NetworkError, ServerDownError, PoolExhaustedError) as e:
                # Retryable error
                error_type = type(e).__name__
                connection_attempts_total.labels(status=error_type).inc()

                retry_count += 1
                wait_time = 2 ** retry_count  # Exponential backoff
                print(f"Retry {retry_count}/{max_retries} after {wait_time}s...")
                await asyncio.sleep(wait_time)

        raise MaxRetriesExceeded(f"Failed after {max_retries} attempts")

    def _classify_error(self, error: Exception) -> str:
        if isinstance(error, CredentialsError):
            return "permanent"
        return "retryable"
```

</details>

---

### Bonus Challenges

Once you complete the basic exercise:

1. **Add state fingerprinting:** Track database state (connection count, active queries) to detect state loops

2. **Implement circuit breaker:** After 3 consecutive failures, open circuit for 60 seconds before trying again

3. **Add connection pooling:** Maintain a pool of connections, detect when pool is getting exhausted

4. **Create Grafana dashboard:** Visualize connection attempts, failures, and loop detection rate

5. **Deploy to Kubernetes:** Run the agent in K8s with real database, test with chaos engineering (kill DB pod)

---

## Key Takeaways

Congratulations! You've completed Chapter 20. Here's what you've learned:

### Core Concepts ✅
1. **Ralph Wiggum loops:** Agent stuck in repetitive patterns without making progress
2. **6 loop types:** Infinite retry, state loop, circular dependency, escalation, token threshold, spawn loop
3. **Detection strategies:** Action repetition tracking, state fingerprinting, call stack tracking, token budgeting

### Development Skills ✅
4. **Built loop detector from scratch:** Python implementation with configurable thresholds
5. **IDE integration:** VS Code debugging with breakpoints and variable inspection
6. **Test-driven approach:** Unit tests for loop detection logic

### Production Skills ✅
7. **Prometheus monitoring:** Comprehensive metrics for executions, loops, costs, and durations
8. **Grafana dashboards:** Visual monitoring with alerts
9. **DevOps best practices:** Docker Compose and Kubernetes deployment

### Security Skills ✅
10. **DoW attack prevention:** Rate limiting, input validation, cost budgets
11. **Secrets management:** HashiCorp Vault integration with rotation
12. **Compliance logging:** SOC 2 / GDPR-compliant audit trails

### Business Impact ✅
13. **Real ROI:** 12,400% return on investment in loop detection
14. **Cost savings:** $2,000 in API costs prevented per incident
15. **Downtime reduction:** 3 hours → 13 minutes (93% faster resolution)

---

## What's Next?

In **Chapter 21: Building Resilient Agentic Systems**, you'll learn:

- **Circuit breaker pattern** for production agents
- **Idempotency** and state checkpointing
- **Graceful degradation** strategies
- **Advanced retry logic** with exponential backoff and jitter
- **Self-healing architectures** that recover without human intervention

The patterns in Chapter 20 detect loops. Chapter 21 teaches you how to **prevent** them in the first place.

---

## Additional Resources

### Code Examples
- All code from this chapter: `src/chapter-20/`
- Working examples: `examples/`
- Test suite: `tests/chapter-20/`

### Documentation
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- HashiCorp Vault: https://www.vaultproject.io/docs

### Community
- GitHub Discussions: Ask questions about loop detection
- Discord: #loop-detection channel
- Office Hours: Weekly Q&A sessions (Fridays 2pm PT)

*Created with Claude AI | © 2026 Michel Abboud | CC BY-NC 4.0*

---

## Navigation

← Previous: [Chapter 19: Team Transformation](./19-team-transformation.md) | Next: [Chapter 21: Building Resilient Agentic Systems](./21-resilient-agentic-systems.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 20** | Agent Loop Detection & Prevention | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
