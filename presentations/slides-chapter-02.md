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

# Understanding LLMs and Tokens

## Chapter 2: AI and Claude Code Guide

**The Technology Behind Modern AI**

---

# What is an LLM?

## Large Language Model

A neural network trained on massive text data to predict what comes next.

```
Input:  "The capital of France is"
LLM:    "Paris" (predicted with high confidence)

Input:  "To check disk space in Linux, use the"
LLM:    "df command" (learned from patterns)
```

At its core: **Very sophisticated autocomplete**

---

# Why "Large"?

## Model Size Comparison

```
GPT-2 (2019)      ██ 1.5 Billion parameters
GPT-3 (2020)      ████████████████████ 175 Billion
Claude 3 (2024)   ████████████████████████ ~200B+
GPT-4 (2023)      ████████████████████████████ ~1.7T

Human brain: ~86 billion neurons
```

---

# The Training Process

```
1. DATA COLLECTION
   Books, websites, code, documentation
              ↓
2. PREPROCESSING
   Clean, filter, tokenize
              ↓
3. TRAINING
   Predict next token, adjust weights
   Repeat trillions of times
              ↓
4. FINE-TUNING (RLHF)
   Human feedback makes it helpful
```

---

# The Transformer Architecture

## Self-Attention: The Magic Ingredient

```
"The server crashed because the database pool was exhausted"

Attention weights for "crashed":
  "server"     ████████ 0.75 (subject)
  "exhausted"  █████████ 0.90 (root cause!)
  "pool"       ███████ 0.65 (key detail)
  "the"        █ 0.02 (not important)
```

The model learns: **Which words relate to which**

---

# What is a Token?

## The Basic Unit of LLM Processing

```
"Hello world"    → ["Hello", " world"]       # 2 tokens
"Kubernetes"     → ["Kub", "ernetes"]        # 2 tokens
"kubectl"        → ["kub", "ect", "l"]       # 3 tokens
"192.168.1.1"    → 7 tokens (each part)
```

**Tokens ≠ Words**

---

# Token Estimation Rules

## Quick Mental Math

```
┌─────────────────────────────────────────┐
│  ~4 characters = 1 token                │
│  ~0.75 words = 1 token                  │
│  1 page of text ≈ 500-700 tokens        │
│  100 lines of code ≈ 1,000 tokens       │
└─────────────────────────────────────────┘
```

---

# The Context Window

## Maximum Tokens (Input + Output)

```
┌─────────────────────────────────┐
│  YOUR INPUT                     │
│  • Your question                │
│  • Code you paste               │
│  • Conversation history         │
└─────────────────────────────────┘
              +
┌─────────────────────────────────┐
│  MODEL OUTPUT                   │
│  • The response generated       │
└─────────────────────────────────┘
              =
    Must fit in Context Window
```

---

# Context Window Sizes (2024)

| Model | Context | Equivalent |
|-------|---------|------------|
| GPT-3.5 | 16K | ~40 pages |
| GPT-4 Turbo | 128K | ~300 pages |
| **Claude 3** | **200K** | **~500 pages** |
| Gemini | 1M+ | A short book! |

---

# Token Economics

## How Pricing Works

```
┌────────────────────────────────────────────┐
│  You pay for:                              │
│                                            │
│  INPUT TOKENS (cheaper)                    │
│  Your prompt, context, instructions        │
│                                            │
│  OUTPUT TOKENS (more expensive)            │
│  The model's response                      │
└────────────────────────────────────────────┘
```

---

# Pricing Examples

## Per 1M Tokens (Approximate)

| Model | Input | Output |
|-------|-------|--------|
| Claude 3 Haiku | $0.25 | $1.25 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |
| GPT-4 Turbo | $10.00 | $30.00 |

---

# Real Cost Example

## Code Review Bot

```python
# Per review:
# Input: 2,000 tokens, Output: 500 tokens

# Using Claude 3.5 Sonnet:
# Input:  2,000 / 1M × $3  = $0.006
# Output: 500 / 1M × $15  = $0.0075
# Total per review: ~$0.01

# 100 PRs/day = $1/day = ~$30/month
```

---

# Temperature Parameter

## Controls Randomness

```
Temperature = 0.0 (Deterministic)
  → Always picks highest probability
  → Best for code, consistent output

Temperature = 0.7 (Balanced)
  → Some variation
  → Good for explanations

Temperature = 1.0+ (Creative)
  → More random choices
  → Best for brainstorming
```

---

# Why LLMs Make Mistakes

1. **Statistical patterns, not understanding**
2. **Training data cutoff** (doesn't know recent events)
3. **Hallucinations** (confidently wrong)
4. **Context limitations** (can "forget")
5. **Ambiguous prompts** (garbage in, garbage out)

---

# Verification is Essential

## Always Verify AI Outputs!

```bash
# Before running AI-generated commands:
kubectl apply -f ai-generated.yaml --dry-run=client
terraform plan  # Never apply without plan
shellcheck ai-script.sh
```

---

# Key Takeaways

1. **LLMs predict statistically likely text**
2. **Tokens are the currency** (~4 chars each)
3. **Context window is your working memory**
4. **Cost = Input + Output tokens**
5. **Temperature controls creativity**
6. **Always verify critical outputs**

---

# Quick Reference

```
┌─────────────────────────────────────────┐
│  Token Estimation:                      │
│  • ~4 characters = 1 token              │
│  • 100 lines of code ≈ 1,000 tokens     │
│                                         │
│  Temperature:                           │
│  • 0.0 = Deterministic (code)           │
│  • 0.7 = Balanced (general)             │
│  • 1.0+ = Creative (brainstorming)      │
│                                         │
│  Context Windows:                       │
│  • Claude 3: 200K tokens                │
│  • GPT-4 Turbo: 128K tokens             │
└─────────────────────────────────────────┘
```

---

# Next: Chapter 3

## The Art of Prompting

- CRAFT Framework
- Prompting techniques
- DevOps-specific patterns
- Building a prompt library

---

# Questions?

## Resources

- Full chapter: [chapters/02-understanding-llms-and-tokens.md](../chapters/02-understanding-llms-and-tokens.md)
- Token counter: tiktoken library
