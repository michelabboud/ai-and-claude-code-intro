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

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

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
| Claude Opus 4.5 | 200K | Complex reasoning |
| Claude Sonnet 4.5 | 200K | Balanced (recommended) |
| Claude Haiku 4.5 | 200K | Speed + Cost |
| GPT-4 Turbo | 128K | General purpose |

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
→ Claude Opus 4.5, GPT-4

NEED BALANCE?
→ Claude Sonnet 4.5, GPT-4 Turbo

NEED LOW COST?
→ Claude Haiku 4.5

NEED PRIVACY?
→ LLaMA 3, Mistral (self-hosted)

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

# The Claude 4.5 Family

```
┌────────────────────────────────────────┐
│  CLAUDE SONNET 4.5 - "The Sweet Spot" │
│  Best balance of intelligence & speed  │
│  Excellent for code, most DevOps tasks │
├────────────────────────────────────────┤
│  CLAUDE OPUS 4.5 - "The Powerhouse"   │
│  Most capable, complex reasoning       │
│  Best for architecture decisions       │
├────────────────────────────────────────┤
│  CLAUDE HAIKU 4.5 - "The Speed Demon" │
│  Fastest, most cost-effective          │
│  Great for simple tasks at scale       │
└────────────────────────────────────────┘
```

---

# Claude Pricing

## Per 1M Tokens (2025)

| Model | Input | Output |
|-------|-------|--------|
| Claude Opus 4.5 | $5.00 | $25.00 |
| Claude Sonnet 4.5 | $3.00 | $15.00 |
| Claude Haiku 4.5 | $1.00 | $5.00 |

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

Claude 4.5 models can analyze images!

```python
# Send screenshot for analysis
message = client.messages.create(
    model="claude-sonnet-4-5-20250514",
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
| Code generation | Claude Sonnet 4.5 |
| Complex debugging | Claude Opus 4.5 |
| Log analysis | Claude Sonnet 4.5 |
| Chatbot/automation | Claude Haiku 4.5 |
| Architecture design | Claude Opus 4.5 |

---

# Quick Reference

```
┌─────────────────────────────────────────┐
│  Model Selection:                       │
│  • Most tasks → Sonnet 4.5              │
│  • Complex → Opus 4.5                   │
│  • Simple/volume → Haiku 4.5            │
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

---

# Credits

**Author:** Michel Abboud
**Created with:** Claude AI (Anthropic)

**License:** CC BY-NC 4.0 | © 2026 Michel Abboud
