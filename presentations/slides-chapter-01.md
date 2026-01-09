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

# Introduction to AI

## Chapter 1: AI and Claude Code Guide

**For DevOps Engineers**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# What is AI?

## The Simple Definition

> AI is software that can **learn from data**, **recognize patterns**, and **make decisions** — rather than just following pre-programmed rules.

---

# Traditional vs AI Approach

| Traditional Script | AI-Powered System |
|-------------------|-------------------|
| `if cpu > 80% then scale_up()` | Predicts when to scale BEFORE CPU spikes |
| Fixed rules for log parsing | Learns what "normal" looks like |
| Hardcoded deployment schedules | Learns optimal deployment windows |

---

# AI Timeline

```
1950s - The Dream Begins (Turing Test)
         ↓
1980s - Expert Systems Era
         ↓
1990s - Machine Learning Rise (Deep Blue)
         ↓
2010s - Deep Learning Revolution (AlphaGo)
         ↓
2020s - The LLM Era (ChatGPT, Claude)
         ↓
NOW - AI as a Daily Tool
```

---

# Types of AI

## By Capability

**Narrow AI (What we have today)**
- Excellent at specific tasks
- ChatGPT, Claude, GitHub Copilot, Tesla Autopilot

**Artificial General Intelligence (AGI)**
- Human-level across all tasks
- Theoretical / Not yet achieved

---

# Machine Learning Approaches

```
┌─────────────────────────────────────────────┐
│  MACHINE LEARNING                           │
│  └── Learns from data                       │
│                                             │
│  DEEP LEARNING                              │
│  └── Neural networks with many layers       │
│                                             │
│  REINFORCEMENT LEARNING                     │
│  └── Trial and error with rewards           │
│                                             │
│  LLMs (Large Language Models)               │
│  └── Trained on text, generates language    │
└─────────────────────────────────────────────┘
```

---

# Key AI Terms for DevOps

| Term | Definition | DevOps Analogy |
|------|------------|----------------|
| **Model** | Trained AI system | Compiled binary |
| **Training** | Teaching with data | CI/CD pipeline |
| **Inference** | Using the model | Running the app |
| **Prompt** | Your input | API request |

---

# AI Task Types

## Natural Language Processing
- Text classification, sentiment, generation
- "Analyze this error log"

## Generative AI
- Creating new content
- "Write a Terraform module"

## Computer Vision
- Understanding images
- "What does this dashboard show?"

---

# AIOps: AI for IT Operations

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Monitoring  │ → │  Analysis    │ → │  Action      │
│              │   │              │   │              │
│  Collect     │   │  AI finds    │   │  Auto-fix    │
│  logs,       │   │  patterns,   │   │  or alert    │
│  metrics     │   │  anomalies   │   │  humans      │
└──────────────┘   └──────────────┘   └──────────────┘
```

---

# DevOps + AI Examples

## Intelligent Alerting
```yaml
# AI-Enhanced: Only alerts when behavior is unusual
- alert: AnomalousCPU
  model: trained_on_historical_patterns
```

## Log Analysis
```bash
ai_analyze_logs /var/log/app.log \
  --find "root cause of the spike at 3pm"
```

---

# The 80/20 Rule

## AI Excels At (80%):
- Repetitive pattern recognition
- Processing large data volumes
- Generating boilerplate code

## You Excel At (20%):
- Strategic decisions
- Business context
- Security judgment
- Final verification

---

# Common Misconceptions

| Myth | Reality |
|------|---------|
| "AI understands like humans" | Recognizes patterns, doesn't "understand" |
| "AI will replace DevOps" | AI augments your capabilities |
| "AI is always right" | Can be confidently wrong |
| "AI is magic" | Math + statistics + data |

---

# Key Takeaways

1. **AI is pattern recognition at scale**
2. **We're in the Narrow AI era**
3. **AI augments, not replaces**
4. **Context is everything**
5. **Always verify AI outputs**

---

# Next Up: Chapter 2

## Understanding LLMs and Tokens

- How LLMs actually work
- What tokens are and why they matter
- Context windows
- Cost calculations

---

# Questions?

## Resources

- Full guide: [chapters/01-introduction-to-ai.md](../chapters/01-introduction-to-ai.md)
- Anthropic: [anthropic.com](https://anthropic.com)
- Claude: [claude.ai](https://claude.ai)

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
