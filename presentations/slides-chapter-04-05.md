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
---

# AI Models & Claude

## Chapters 4-5: The AI Ecosystem

**Navigating Models and Meeting Claude**

---

# Major AI Companies

| Company | Focus | Models |
|---------|-------|--------|
| **Anthropic** | AI Safety | Claude family |
| **OpenAI** | General AI | GPT family |
| **Google** | Research + Products | Gemini |
| **Meta** | Open Source | LLaMA |
| **Mistral** | Efficient AI | Mistral, Mixtral |

---

# Model Comparison

| Model | Context | Best For |
|-------|---------|----------|
| Claude 3 Opus | 200K | Complex reasoning |
| Claude 3.5 Sonnet | 200K | Balanced (recommended) |
| Claude 3 Haiku | 200K | Speed + Cost |
| GPT-4 Turbo | 128K | General purpose |
| GPT-3.5 | 16K | Simple tasks |

---

# Proprietary vs Open Source

## Proprietary (Claude, GPT-4)
- Best performance
- No infrastructure to manage
- Pay per token
- Vendor lock-in risk

## Open Source (LLaMA, Mistral)
- Data stays local
- No per-token cost
- Need GPU infrastructure
- Requires ML expertise

---

# When to Use What

```
NEED BEST QUALITY?
→ Claude 3 Opus, GPT-4

NEED BALANCE?
→ Claude 3.5 Sonnet, GPT-4 Turbo

NEED LOW COST?
→ Claude 3 Haiku, GPT-3.5

NEED PRIVACY?
→ LLaMA 2, Mistral (self-hosted)

NEED ENTERPRISE?
→ AWS Bedrock, Azure OpenAI
```

---

# What is Claude?

## Anthropic's AI Assistant

**Designed to be:**
- **H**elpful - Genuinely useful
- **H**armless - Safe outputs
- **H**onest - Transparent about limitations

---

# The Claude 3 Family

```
┌────────────────────────────────────────┐
│  CLAUDE 3.5 SONNET - "The Sweet Spot" │
│  Best balance of intelligence & speed  │
│  Excellent for code, most DevOps tasks │
├────────────────────────────────────────┤
│  CLAUDE 3 OPUS - "The Powerhouse"     │
│  Most capable, complex reasoning       │
│  Best for architecture decisions       │
├────────────────────────────────────────┤
│  CLAUDE 3 HAIKU - "The Speed Demon"   │
│  Fastest, most cost-effective          │
│  Great for simple tasks at scale       │
└────────────────────────────────────────┘
```

---

# Claude Pricing

## Per 1M Tokens

| Model | Input | Output |
|-------|-------|--------|
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

---

# Access Methods

```
┌─────────────────────────────────────────┐
│  1. CLAUDE.AI (Web Interface)           │
│     Quick questions, exploration        │
│                                         │
│  2. API (api.anthropic.com)            │
│     Automation, integration             │
│                                         │
│  3. AWS BEDROCK                         │
│     Enterprise, VPC integration         │
│                                         │
│  4. CLAUDE CODE (CLI)                   │
│     Development, DevOps tasks           │
└─────────────────────────────────────────┘
```

---

# Claude's Capabilities

## Excellent At:
- Code generation & review
- Debugging & troubleshooting
- Documentation
- Long context (200K tokens!)
- Following complex instructions

## Cannot:
- Access real-time data
- Execute code (except Claude Code)
- Remember between sessions
- Access your systems directly

---

# Vision Capabilities

Claude 3 models can analyze images!

```python
# Send screenshot for analysis
message = client.messages.create(
    model="claude-3-5-sonnet",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {...}},
            {"type": "text", "text": "What error is shown?"}
        ]
    }]
)
```

Use for: dashboard screenshots, error images, architecture diagrams

---

# Model Selection Guide

| Task | Model |
|------|-------|
| Code generation | Claude 3.5 Sonnet |
| Complex debugging | Claude 3 Opus |
| Log analysis | Claude 3.5 Sonnet |
| Chatbot/automation | Claude 3 Haiku |
| Architecture design | Claude 3 Opus |

---

# Quick Reference

```
┌─────────────────────────────────────────┐
│  Model Selection:                       │
│  • Most tasks → Sonnet                  │
│  • Complex → Opus                       │
│  • Simple/volume → Haiku                │
│                                         │
│  Access:                                │
│  • Quick tasks → claude.ai              │
│  • Automation → API                     │
│  • Enterprise → Bedrock/Vertex          │
│  • Coding → Claude Code CLI             │
│                                         │
│  Context: 200K tokens                   │
│  (~500 pages, entire codebases!)        │
└─────────────────────────────────────────┘
```

---

# Next: Chapter 6-8

## Claude Code Mastery

- Installation and setup
- Basic to professional usage
- Configuration and customization
- Agents, skills, sub-agents

---

# Questions?

## Resources

- Chapter 4: [ai-models-landscape.md](../chapters/04-ai-models-landscape.md)
- Chapter 5: [introduction-to-claude.md](../chapters/05-introduction-to-claude.md)
- Claude: [claude.ai](https://claude.ai)
