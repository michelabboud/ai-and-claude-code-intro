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

# Multi-Agent Orchestration

## Chapters 15-16: AI and Claude Code Guide

**For DevOps Engineers**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# Why Multiple Agents?

## Single Agent Limitations

| Problem | Example |
|---------|---------|
| **Sequential Processing** | Analyze logs → then metrics → then code |
| **Context Overload** | 50K token limit vs 500K token incident |
| **Token Costs** | Using Opus for everything ($150/incident) |
| **No Specialization** | Generalist vs security expert |

---

# Multi-Agent Benefits

```
┌─────────────────────────────────────────────────┐
│  SINGLE AGENT: 45 minutes, $1.50              │
│                                                 │
│  MULTI-AGENT SWARM: 6 minutes, $0.82          │
│                                                 │
│  - 87% faster                                   │
│  - 45% cheaper                                  │
│  - Parallel processing                          │
│  - Specialized expertise                        │
└─────────────────────────────────────────────────┘
```

---

# Agent Mesh Patterns

## 1. Coordinator Pattern
```
       [Coordinator]
      /      |      \
[Agent A] [Agent B] [Agent C]
```
- Central orchestrator delegates tasks
- Good for complex workflows

---

# Agent Mesh Patterns

## 2. Peer-to-Peer Pattern
```
[Agent A] ←→ [Agent B]
    ↕           ↕
[Agent C] ←→ [Agent D]
```
- Agents negotiate directly
- Good for dynamic collaboration

---

# Agent Mesh Patterns

## 3. Hierarchical Pattern
```
      [Manager]
     /    |    \
[TL 1] [TL 2] [TL 3]
  / \    / \    / \
[W1][W2][W3][W4][W5][W6]
```
- Multi-level delegation
- Good for enterprises

---

# Specialist Agent Types

| Agent | Responsibility | Model |
|-------|---------------|-------|
| **Log Analyzer** | Parse logs, find errors | Haiku ($) |
| **Metrics Agent** | Analyze Prometheus data | Haiku ($) |
| **Code Analyzer** | Recent changes, RCA | Sonnet ($$) |
| **Infrastructure Agent** | Check K8s, AWS resources | Sonnet ($$) |
| **Security Agent** | Vulnerability scanning | Opus ($$$) |
| **Communication Agent** | Write reports, update Slack | Haiku ($) |

---

# Communication Protocols

## 1. Message Queue (Redis/RabbitMQ)
```python
# Agent A publishes
redis.publish('incident:123', {
    'agent': 'log_analyzer',
    'findings': ['OOMKilled at 14:32']
})

# Agent B subscribes
redis.subscribe('incident:123')
```

---

# Communication Protocols

## 2. Shared Context (Database)
```python
# Agent writes findings
db.incidents.update({
    'id': 'INC-123',
    'log_analysis': {
        'errors': ['OOMKilled'],
        'confidence': 0.95
    }
})

# Coordinator reads all
findings = db.incidents.find_one({'id': 'INC-123'})
```

---

# Model Selection Strategy

```
┌──────────────┬─────────────────┬─────────────┐
│   Task       │   Model         │   Cost      │
├──────────────┼─────────────────┼─────────────┤
│ Log parsing  │ Haiku           │ $0.001      │
│ Metric check │ Haiku           │ $0.001      │
│ Code review  │ Sonnet          │ $0.03       │
│ Architecture │ Opus            │ $1.50       │
│ RCA synthesis│ Sonnet          │ $0.05       │
└──────────────┴─────────────────┴─────────────┘
Total per incident: ~$0.82
```

---

# Incident Response Swarm

## The Team

```
Coordinator (Sonnet)
     ↓
┌────────────────────────────────────────┐
│ [Log Analyzer]   [Metrics Analyzer]   │
│ [Code Analyzer]  [Infra Checker]      │
│ [Comms Handler]                        │
└────────────────────────────────────────┘
```

**Execution Time:** 6 minutes (parallel)
**Single Agent:** 45 minutes (sequential)

---

# Incident Response Swarm

## Workflow

```python
async def handle_incident(alert):
    # 1. Spawn specialist agents
    agents = await spawn_swarm([
        LogAnalyzer(model='haiku'),
        MetricsAnalyzer(model='haiku'),
        CodeAnalyzer(model='sonnet'),
        InfraChecker(model='sonnet'),
        CommsHandler(model='haiku')
    ])

    # 2. Run in parallel
    results = await asyncio.gather(*[
        agent.analyze(alert) for agent in agents
    ])

    # 3. Coordinator synthesizes
    rca = await coordinator.synthesize(results)
    return rca
```

---

# Code Review Pipeline

## The Team

```
┌──────────────────────────────────────────┐
│ [Security Scanner] → OWASP, CVEs        │
│ [Performance Profiler] → Complexity     │
│ [Style Checker] → Linting               │
│ [Test Analyzer] → Coverage              │
│ [Doc Validator] → Comments              │
└──────────────────────────────────────────┘
        ↓
   [Coordinator]
        ↓
  Comprehensive Review
```

---

# Code Review Pipeline

## Results

| Metric | Before | After |
|--------|--------|-------|
| Review Time | 60 min | 8 min |
| Security Issues Found | 3/10 | 9/10 |
| False Positives | 40% | 5% |
| Developer Satisfaction | 6/10 | 9/10 |

---

# Multi-Cloud Cost Optimization

## The Squad

```
┌──────────────────────────────────────────┐
│ [AWS Analyzer] → EC2, RDS, S3           │
│ [GCP Analyzer] → Compute, Storage        │
│ [Azure Analyzer] → VMs, Databases       │
│ [Right-Sizer] → Recommendations         │
│ [Savings Planner] → Reserved instances  │
└──────────────────────────────────────────┘
        ↓
   [Coordinator]
        ↓
  Prioritized by ROI
```

**Result:** $47K → $18K/month (62% savings)

---

# Monitoring Agent Performance

## Key Metrics

```python
# Prometheus metrics
agent_execution_time_seconds{agent="log_analyzer"}
agent_token_usage_total{agent="metrics_analyzer"}
agent_success_rate{agent="code_analyzer"}
agent_cost_dollars{agent="coordinator"}

# Dashboard tracks:
- Execution times (P50, P95, P99)
- Token usage per agent
- Success/failure rates
- Cost per incident
```

---

# Implementation with n8n

## Multi-Agent Workflow

```
Webhook (Alert) →
   ├─→ HTTP: Spawn Log Agent
   ├─→ HTTP: Spawn Metrics Agent
   ├─→ HTTP: Spawn Code Agent
   └─→ HTTP: Spawn Infra Agent
       ↓
   Merge Results →
       ↓
   HTTP: Coordinator Synthesis →
       ↓
   Slack: Post RCA
```

---

# Best Practices

## ✅ DO

- Use Haiku for simple, high-volume tasks
- Run agents in parallel when possible
- Set timeouts (30s per agent)
- Cache common queries
- Monitor token usage

## ❌ DON'T

- Use Opus for everything
- Create circular dependencies
- Spawn unlimited agents
- Forget error handling
- Skip monitoring

---

# When NOT to Use Multiple Agents

## Single Agent is Better When:

1. **Simple tasks** - "Parse this log file"
2. **Low latency required** - <1 second response
3. **Tight context needed** - All info fits in 10K tokens
4. **Budget constrained** - <$10/month
5. **Learning phase** - Master single agent first

---

# Common Pitfalls

## 1. Token Budget Explosion
```
5 agents × $0.05 × 100 incidents/day = $25/day = $750/month
```
**Solution:** Use Haiku for simple tasks, cache results

## 2. Circular Dependencies
```
Agent A → needs Agent B → needs Agent C → needs Agent A ❌
```
**Solution:** Clear dependency graph, coordinator pattern

---

# Common Pitfalls

## 3. No Conflict Resolution
```
Agent A: "Restart pod"
Agent B: "Increase memory"
Agent C: "Rollback deployment"
```
**Solution:** Confidence scoring + coordinator arbitration

## 4. Ignoring Failures
**Solution:** Circuit breakers, retry logic, human escalation

---

# Load Balancing Strategies

## Agent Pool Management

```python
# Dynamic agent pool
class AgentPool:
    def __init__(self, max_agents=10):
        self.pool = []
        self.max_agents = max_agents

    async def get_agent(self, agent_type):
        if len(self.pool) >= self.max_agents:
            await self.wait_for_slot()

        agent = Agent(type=agent_type)
        self.pool.append(agent)
        return agent
```

---

# Cost Optimization

## Real-World Example

```
Startup (40 incidents/month):
├─ Single Opus agent: $60/month
├─ Mixed strategy: $33/month
└─ Savings: 45% + 87% faster

Enterprise (500 incidents/month):
├─ Single Opus agent: $750/month
├─ Multi-agent swarm: $410/month
└─ Savings: 45% + parallel processing
```

---

# Hands-On Exercise

## Build Your First Swarm

1. **Deploy code review pipeline** (Chapter 16 code)
2. **Test with a PR** from your project
3. **Monitor execution** with Prometheus
4. **Measure time savings** vs manual review
5. **Optimize costs** by model selection

**Goal:** <10 min review time, <$0.50/PR

---

# Key Takeaways

1. **Multi-agent = parallel processing** (87% faster)
2. **Specialist agents = better results** (higher accuracy)
3. **Model selection = cost optimization** (45% cheaper)
4. **Coordinator pattern** works for most use cases
5. **Monitor everything** (token usage, costs, time)

---

# Next Up: Chapters 17-18

## AI-Powered Observability (AIOps)

- Anomaly detection with AI
- Predictive alerting
- Auto-remediation workflows
- Self-healing infrastructure
- Production deployment

---

# Questions?

## Resources

- Chapter 15: [chapters/15-multi-agent-fundamentals.md](../chapters/15-multi-agent-fundamentals.md)
- Chapter 16: [chapters/16-multi-agent-advanced.md](../chapters/16-multi-agent-advanced.md)
- Code Examples: [src/chapter-15/](../src/chapter-15/)
- Code Examples: [src/chapter-16/](../src/chapter-16/)

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
