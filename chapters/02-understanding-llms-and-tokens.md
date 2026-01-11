# Chapter 2: Understanding Large Language Models (LLMs) and Tokens

## The Technology Powering Modern AI Assistants

**📖 Reading time:** ~15 minutes | **⚙️ Hands-on time:** ~20 minutes
**🎯 Quick nav:** [What is an LLM?](#21-what-is-a-large-language-model) | [How LLMs Work](#22-how-llms-actually-work) | [Tokens](#23-understanding-tokens) | [Context Window](#24-the-context-window) | [Costs](#25-token-economics-understanding-costs) | [🏋️ Skip to Exercises](#29-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** LLMs are trained on vast amounts of text to predict the next word. They don't "think" - they're incredibly sophisticated pattern matchers. Understanding tokens (how LLMs count text) is crucial for managing costs and working within context limits.

**Key concepts:**
- **LLMs** = Massive neural networks trained to predict next tokens based on patterns (not databases, not search engines)
- **Tokens** ≈ 4 characters or ¾ of a word. "Hello DevOps!" = ~3 tokens, not 2 words
- **Context window** = Maximum tokens LLM can "remember" (Claude Sonnet 4.5 = 200K tokens ≈ 150K words)
- **Costs** = Charged per token: input tokens (what you send) + output tokens (what AI generates)
- **Optimization** = Shorter prompts = lower cost. But too short = worse results. Balance matters.

**Most important takeaway:** Tokens = money and memory. Every character counts. Understanding token economics helps you use AI effectively without blowing your budget. A 10K token prompt on Sonnet costs ~$0.30 - small, but adds up at scale.

**Hands-on:** [Jump to exercises](#29-hands-on-exercises) to practice token counting, plan context windows, and experiment with model behavior.

---

*💡 Want to understand the internals? Keep reading. Just need token basics? You're good - try the exercises!*

---

As a DevOps engineer, understanding how LLMs work will help you use them more effectively, estimate costs, troubleshoot issues, and make informed decisions about integrating AI into your workflows.

---

## 2.1 What is a Large Language Model?

### The Simple Explanation

A **Large Language Model (LLM)** is an AI system trained on massive amounts of text to predict what comes next in a sequence. That's it—at its core, it's a very sophisticated autocomplete.

```
Input:  "The capital of France is"
LLM:    "Paris" (predicted with high confidence)

Input:  "To check disk space in Linux, use the"
LLM:    "df command" (predicted based on patterns in training data)
```

### Why "Large"?

```
Model Size Comparison (Parameters)
═══════════════════════════════════════════════════════════════

GPT-2 (2019)          ██ 1.5 Billion
GPT-3 (2020)          ████████████████████████████████████ 175 Billion
Claude 4.5 (2025)     ████████████████████████████████████████ ~200B+ (estimated)
GPT-4 (2023)          ████████████████████████████████████████ ~1.7 Trillion (rumored)

For context:
- Human brain: ~86 billion neurons
- Parameters ≠ neurons, but gives sense of scale
```

### The Technical Definition

An LLM is a **neural network** with billions of **parameters** (learned weights) that has been trained on terabytes of text data to model the statistical relationships between words and concepts.

---

## 2.2 How LLMs Actually Work

### The Training Process

```
┌──────────────────────────────────────────────────────────────────┐
│                    LLM TRAINING PIPELINE                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Data Collection                                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ • Books (millions of them)                                  │ │
│  │ • Websites (Common Crawl - billions of pages)               │ │
│  │ • Wikipedia, academic papers                                │ │
│  │ • Code repositories (GitHub)                                │ │
│  │ • Documentation, forums, Q&A sites                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  Step 2: Preprocessing                                           │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ • Clean and filter data                                     │ │
│  │ • Remove duplicates, harmful content                        │ │
│  │ • Convert to tokens                                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  Step 3: Training (Self-Supervised Learning)                     │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Input: "The DevOps engineer deployed the"                   │ │
│  │ Target: "application"                                       │ │
│  │                                                             │ │
│  │ Model predicts → compares to actual → adjusts weights       │ │
│  │ Repeat trillions of times                                   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  Step 4: Fine-Tuning (Making it Useful)                          │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ • RLHF (Reinforcement Learning from Human Feedback)         │ │
│  │ • Human raters score responses                              │ │
│  │ • Model learns to be helpful, harmless, honest              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### The Transformer Architecture

LLMs use a architecture called **Transformers** (introduced in the famous "Attention is All You Need" paper, 2017).

```
┌────────────────────────────────────────────────────────────────┐
│                   TRANSFORMER ARCHITECTURE                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│    Input: "kubectl get pods -n"                                │
│                    ↓                                           │
│    ┌──────────────────────────────────────┐                    │
│    │         TOKENIZATION                 │                    │
│    │  "kubectl" "get" "pods" "-" "n"      │                    │
│    └──────────────────────────────────────┘                    │
│                    ↓                                           │
│    ┌──────────────────────────────────────┐                    │
│    │      EMBEDDING LAYER                 │                    │
│    │  Convert tokens to vectors           │                    │
│    │  [0.23, -0.45, 0.12, ...]            │                    │
│    └──────────────────────────────────────┘                    │
│                    ↓                                           │
│    ┌──────────────────────────────────────┐                    │
│    │      ATTENTION MECHANISM             │  ← The magic!      │
│    │  "Which words relate to which?"      │                    │
│    │                                      │                    │
│    │  "kubectl" pays attention to "pods"  │                    │
│    │  "-n" pays attention to "namespace"  │                    │
│    └──────────────────────────────────────┘                    │
│                    ↓                                           │
│    ┌──────────────────────────────────────┐                    │
│    │      FEED FORWARD LAYERS             │                    │
│    │  Process and transform               │                    │
│    └──────────────────────────────────────┘                    │
│                    ↓                                           │
│    ┌──────────────────────────────────────┐                    │
│    │      OUTPUT LAYER                    │                    │
│    │  Probability distribution over       │                    │
│    │  all possible next tokens            │                    │
│    │                                      │                    │
│    │  "production": 0.35                  │                    │
│    │  "default": 0.28                     │                    │
│    │  "kube-system": 0.22                 │                    │
│    │  ...                                 │                    │
│    └──────────────────────────────────────┘                    │
│                    ↓                                           │
│    Output: "production" (highest probability selected)         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### The Attention Mechanism (Simplified)

The key innovation is **self-attention**, which allows the model to weigh the importance of different parts of the input.

```
Example: "The server crashed because the database connection pool was exhausted"

Attention weights (which words relate to "crashed"):

"The"        ░░░░░░░░░░ 0.02
"server"     ████████░░ 0.75  ← High attention (subject of crash)
"crashed"    ██████████ 1.00  ← Self
"because"    ███░░░░░░░ 0.30  ← Indicates causation
"the"        ░░░░░░░░░░ 0.01
"database"   ██████░░░░ 0.55  ← Related to cause
"connection" █████░░░░░ 0.45  ← Related to cause
"pool"       ███████░░░ 0.65  ← Key technical detail
"was"        ░░░░░░░░░░ 0.03
"exhausted"  █████████░ 0.90  ← Root cause!

The model learns: "crashed" strongly relates to "server" and "exhausted"
This understanding is learned from seeing millions of similar patterns
```

---

## 2.3 Understanding Tokens

### What is a Token?

A **token** is the basic unit of text that LLMs process. It's NOT the same as a word.

```
Tokenization Examples (using GPT-style tokenization):

"Hello"           → ["Hello"]                    # 1 token
"Hello world"     → ["Hello", " world"]          # 2 tokens
"Kubernetes"      → ["Kub", "ernetes"]           # 2 tokens
"kubectl"         → ["kub", "ect", "l"]          # 3 tokens
"authentication"  → ["auth", "ent", "ication"]   # 3 tokens

# Special characters and numbers
"192.168.1.1"     → ["192", ".", "168", ".", "1", ".", "1"]  # 7 tokens
"#!/bin/bash"     → ["#!", "/", "bin", "/", "bash"]         # 5 tokens
```

### Why Tokens Instead of Words?

```
┌─────────────────────────────────────────────────────────────┐
│                 WHY TOKENIZATION?                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Problem with word-based:                                   │
│  • Vocabulary would be enormous (millions of words)         │
│  • Can't handle new words, typos, technical terms           │
│  • Different languages need different vocabularies          │
│                                                             │
│  Problem with character-based:                              │
│  • Sequences become very long                               │
│  • Loses semantic meaning                                   │
│  • Computationally expensive                                │
│                                                             │
│  Tokens = Best of both worlds:                              │
│  • Fixed vocabulary size (typically 50K-100K tokens)        │
│  • Can represent ANY text                                   │
│  • Captures meaningful subunits                             │
│  • Efficient computation                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Common Tokenization Algorithms

#### 1. **Byte-Pair Encoding (BPE)**
Used by GPT models, Claude, and others.

```python
# How BPE Works (Simplified)

# Starting with character-level vocabulary
vocab = ['a', 'b', 'c', ..., 'z', ' ', '.', ...]

# Find most common pair and merge
"the cat sat" → "th" "e " "ca" "t " "sa" "t"

# After training on billions of words:
# Common words become single tokens: "the", " is", " and"
# Rare words get split: "Kubernetes" → "Kub" + "ernetes"
```

#### 2. **WordPiece**
Used by BERT-based models.

```
"unhappiness" → ["un", "##happy", "##ness"]

# The ## indicates continuation of previous token
```

### Token Counting: DevOps Examples

```python
# Approximate token counts (varies by model)

# Simple text
"Hello, world!"
# Tokens: ~4 (Hello, ,, world, !)

# Kubernetes manifest
"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
"""
# Tokens: ~35

# A typical bash script (50 lines)
# Tokens: ~400-600

# A Python file (200 lines of code)
# Tokens: ~1,500-2,500

# Terraform module (100 lines)
# Tokens: ~800-1,200
```

### Rule of Thumb for Token Estimation

```
┌────────────────────────────────────────────────────────────┐
│              TOKEN ESTIMATION RULES                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  English text:                                             │
│  • ~4 characters per token                                 │
│  • ~0.75 words per token                                   │
│  • 1 page of text ≈ 500-700 tokens                         │
│                                                            │
│  Code:                                                     │
│  • More tokens per line (special characters, indentation)  │
│  • Python/JS: ~8-12 tokens per line                        │
│  • YAML/JSON: ~5-8 tokens per line                         │
│  • Variable names may be multiple tokens                   │
│                                                            │
│  Quick mental math:                                        │
│  • 1,000 words ≈ 1,300 tokens                              │
│  • 100 lines of code ≈ 1,000 tokens                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 2.4 The Context Window

### What is Context Window?

The **context window** is the maximum number of tokens an LLM can process at once (input + output combined).

```
┌────────────────────────────────────────────────────────────────┐
│                    CONTEXT WINDOW                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Your Input (Prompt)                    │   │
│  │  • Your question/request                                │   │
│  │  • Code you paste                                       │   │
│  │  • System instructions                                  │   │
│  │  • Conversation history                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           +                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Model Output                           │   │
│  │  • The response generated                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           =                                    │
│         Must fit within Context Window limit                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Context Window Sizes (2025)

```
Model Context Windows
═══════════════════════════════════════════════════════════════════

GPT-4 Turbo        ████████████████████  128K tokens (~100K words)
Claude Opus 4.5    ████████████████████  200K tokens (~150K words)
Claude Sonnet 4.5  ████████████████████  200K tokens
Claude Haiku 4.5   ████████████████████  200K tokens

Practical comparison:
├── 8K tokens   = ~20 pages of text
├── 32K tokens  = ~80 pages of text
├── 128K tokens = ~300 pages (a short book!)
└── 200K tokens = ~500 pages
```

### Why Context Window Matters for DevOps

```yaml
# Scenario: Debugging a complex issue

context_needed:
  - error_logs: "~2,000 tokens"
  - config_files: "~3,000 tokens"
  - recent_code_changes: "~4,000 tokens"
  - conversation_history: "~2,000 tokens"
  - system_prompt: "~500 tokens"
  total_input: "~11,500 tokens"

# With GPT-3.5 (16K window):
#   Input: 11,500 + Output room: 4,500 = OK

# With a smaller context window:
#   Would need to truncate logs or split the task
```

### Strategies for Working with Context Limits

```python
# Strategy 1: Summarize large files
# Instead of pasting 1000 lines of logs

bad_prompt = f"Here are all my logs: {giant_log_file}"  # May exceed limit

good_prompt = """
Here's a summary of my logs:
- 500 INFO messages (normal operation)
- 15 WARN messages (mostly about deprecation)
- 3 ERROR messages (pasted below)

Error 1: [timestamp] Connection refused...
Error 2: [timestamp] Timeout after 30s...
Error 3: [timestamp] Out of memory...

What's causing these errors?
"""

# Strategy 2: Focus on relevant sections
# Instead of entire codebase

bad_prompt = "Here's my entire application: {all_files}"

good_prompt = """
I'm having an issue with database connections.
Here's the relevant code:

database.py (connection handling):
{connection_code}

config.py (database settings):
{db_config}

The error occurs in database.py line 45.
"""

# Strategy 3: Iterative refinement
# Break large tasks into steps

step1 = "Analyze this error message: {error}"
step2 = "Based on the error, what files should I check?"
step3 = "Here's the relevant file. What's wrong?"
```

---

## 2.5 Token Economics: Understanding Costs

### How Pricing Works

```
┌────────────────────────────────────────────────────────────────┐
│                    LLM PRICING MODEL                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  You pay for:                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  INPUT TOKENS                                            │  │
│  │  • Your prompt                                           │  │
│  │  • System instructions                                   │  │
│  │  • Context you provide                                   │  │
│  │                                                          │  │
│  │  Usually cheaper (the model just reads)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           +                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  OUTPUT TOKENS                                           │  │
│  │  • The model's response                                  │  │
│  │  • Usually more expensive (computation intensive)        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Pricing Examples (Approximate, as of 2024)

```
Cost per 1 Million Tokens (USD) - 2025
═══════════════════════════════════════════════════════════════════

Model               Input        Output
─────────────────────────────────────────────────────────────────
Claude Haiku 4.5    $1.00        $5.00
Claude Sonnet 4.5   $3.00        $15.00
Claude Opus 4.5     $5.00        $25.00
GPT-4 Turbo         $10.00       $30.00

Note: Prices change frequently. Check current pricing.
```

### Real-World Cost Calculations

```python
# Example 1: Code Review Bot

# Input per review:
# - Code diff: ~500 tokens
# - Instructions: ~200 tokens
# - Context: ~300 tokens
# Total input: 1,000 tokens

# Output per review:
# - Feedback: ~400 tokens

# Using Claude Sonnet 4.5:
# Input cost: 1,000 / 1,000,000 * $3 = $0.003
# Output cost: 400 / 1,000,000 * $15 = $0.006
# Total per review: $0.009

# 100 PRs per day = $0.90/day = ~$27/month


# Example 2: Log Analysis Pipeline

# Input per analysis:
# - Log batch: ~5,000 tokens
# - System prompt: ~500 tokens
# Total input: 5,500 tokens

# Output:
# - Summary: ~300 tokens

# Using Claude Haiku 4.5 (cheaper for simple tasks):
# Input cost: 5,500 / 1,000,000 * $1 = $0.0055
# Output cost: 300 / 1,000,000 * $5 = $0.0015
# Total per analysis: $0.007

# 1,000 analyses per day = $7/day = ~$210/month


# Example 3: Interactive Debugging Session

# Average conversation:
# - 10 back-and-forth exchanges
# - ~2,000 tokens input per exchange (including history)
# - ~500 tokens output per exchange

# Using GPT-4 Turbo:
# Input: 20,000 tokens → $0.20
# Output: 5,000 tokens → $0.15
# Total per session: $0.35

# 50 sessions per month = $17.50/month
```

### Cost Optimization Tips

```yaml
# DevOps Cost Optimization for LLM Usage

1_use_appropriate_model:
  description: "Don't use Opus for simple tasks"
  examples:
    - simple_formatting: "Use Claude Haiku 4.5"
    - code_generation: "Use Claude Sonnet 4.5"
    - complex_reasoning: "Use Claude Opus 4.5"

2_minimize_context:
  description: "Only include what's necessary"
  before: |
    Here's my entire application with 50 files...
  after: |
    Here's the relevant error and the 2 files involved...

3_cache_common_patterns:
  description: "Don't re-ask the same questions"
  implementation:
    - hash: "Hash the prompt"
    - cache: "Store in Redis/DynamoDB"
    - ttl: "Set appropriate expiration"

4_batch_requests:
  description: "Combine multiple small requests"
  before: |
    Request 1: Review file1.py
    Request 2: Review file2.py
    Request 3: Review file3.py
  after: |
    Request 1: Review these 3 files: file1.py, file2.py, file3.py

5_use_streaming:
  description: "Stream responses for better UX without extra cost"
  benefit: "User sees response faster, same token cost"
```

---

## 2.6 How LLMs Generate Text

### The Generation Process

```
┌────────────────────────────────────────────────────────────────┐
│                  TEXT GENERATION PROCESS                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Input: "Write a bash script to"                               │
│                                                                │
│  Step 1: Process input tokens                                  │
│  ["Write", " a", " bash", " script", " to"]                    │
│                                                                │
│  Step 2: Predict next token                                    │
│  ┌───────────────────────────────────────┐                     │
│  │ Probability distribution:              │                    │
│  │ " check"     : 0.15                    │                    │
│  │ " backup"    : 0.12                    │                    │
│  │ " monitor"   : 0.10                    │                    │
│  │ " list"      : 0.08                    │                    │
│  │ " delete"    : 0.05                    │                    │
│  │ ...                                    │                    │
│  └───────────────────────────────────────┘                     │
│                                                                │
│  Step 3: Select token (based on sampling settings)             │
│  Selected: " backup"                                           │
│                                                                │
│  Step 4: Append and repeat                                     │
│  New context: "Write a bash script to backup"                  │
│  Predict next: " the" (0.25), " MySQL" (0.18), ...             │
│                                                                │
│  Continue until:                                               │
│  • End token generated                                         │
│  • Max length reached                                          │
│  • Stop sequence encountered                                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Key Generation Parameters

#### Temperature

```
Temperature: Controls randomness in selection

Temperature = 0.0 (Deterministic)
─────────────────────────────────────────────────
"backup"  ████████████████████ 0.25  ← Always picks this
"check"   ████████████░░░░░░░░ 0.20
"monitor" ████████░░░░░░░░░░░░ 0.15

Temperature = 0.7 (Balanced)
─────────────────────────────────────────────────
"backup"  ██████████████░░░░░░ 0.22  ← Usually this
"check"   ██████████████░░░░░░ 0.21  ← Sometimes this
"monitor" ████████████░░░░░░░░ 0.18  ← Occasionally this

Temperature = 1.5 (Creative/Random)
─────────────────────────────────────────────────
"backup"  ████████████░░░░░░░░ 0.18
"check"   ████████████░░░░░░░░ 0.17
"monitor" ████████████░░░░░░░░ 0.16  ← More variety
"analyze" ██████████░░░░░░░░░░ 0.14
"encrypt" ████████░░░░░░░░░░░░ 0.12

DevOps Use Cases:
• temp=0: Consistent code generation, deterministic outputs
• temp=0.7: General assistance, explanations
• temp=1.0+: Brainstorming, creative solutions
```

#### Top-P (Nucleus Sampling)

```
Top-P = 0.9: Only consider tokens in top 90% of probability mass

Example distribution:
Token        Probability  Cumulative  Included?
───────────────────────────────────────────────
"backup"     0.25         0.25        Yes ✓
"check"      0.20         0.45        Yes ✓
"monitor"    0.15         0.60        Yes ✓
"list"       0.12         0.72        Yes ✓
"delete"     0.10         0.82        Yes ✓
"create"     0.08         0.90        Yes ✓
"encrypt"    0.04         0.94        No ✗ (over 90%)
"hash"       0.03         0.97        No ✗
"pipe"       0.02         0.99        No ✗
"dance"      0.01         1.00        No ✗ (filtered out!)
```

#### Max Tokens

```python
# Control maximum response length

# Short response (save tokens/money)
response = client.generate(
    prompt="What's the kubectl command to get pods?",
    max_tokens=100  # Expect short answer
)

# Long response (detailed explanation)
response = client.generate(
    prompt="Explain Kubernetes networking in detail",
    max_tokens=2000  # Allow comprehensive response
)

# Code generation (needs more space)
response = client.generate(
    prompt="Write a complete Terraform module for EKS",
    max_tokens=4000  # Complex code needs room
)
```

---

## 2.7 Understanding Model Behavior

### Why LLMs Can Be "Wrong"

```
┌────────────────────────────────────────────────────────────────┐
│                 WHY LLMs MAKE MISTAKES                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. STATISTICAL PATTERNS, NOT TRUE UNDERSTANDING               │
│     • LLMs predict likely text, not factually correct text     │
│     • "Hallucinations" occur when patterns mislead             │
│                                                                │
│  2. TRAINING DATA CUTOFF                                       │
│     • Model doesn't know events after training date            │
│     • New tools, versions, APIs may be unknown                 │
│                                                                │
│  3. TRAINING DATA BIASES                                       │
│     • Reflects patterns in training data                       │
│     • Popular != correct                                       │
│                                                                │
│  4. CONTEXT LIMITATIONS                                        │
│     • Can lose track in very long conversations                │
│     • May "forget" earlier context                             │
│                                                                │
│  5. AMBIGUOUS PROMPTS                                          │
│     • Garbage in, garbage out                                  │
│     • Vague questions get vague answers                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Hallucination Examples

```yaml
# Example 1: Made-up CLI flags

prompt: "What's the kubectl command to restart a deployment?"

bad_response: |
  kubectl restart deployment nginx -n production
  # WRONG! 'restart' is not a kubectl command

correct_response: |
  kubectl rollout restart deployment nginx -n production
  # CORRECT! 'rollout restart' is the proper command


# Example 2: Invented package names

prompt: "What npm package monitors node memory?"

bad_response: |
  npm install node-memory-profiler-live
  # This package might not exist!

correct_response: |
  # There are several options:
  # - process.memoryUsage() (built-in)
  # - v8.getHeapStatistics() (built-in)
  # - heapdump package (for snapshots)
  # - clinic.js (comprehensive profiling)
  # Always verify packages on npmjs.com


# Example 3: Outdated information

prompt: "How do I set up a Kubernetes cluster?"

potentially_outdated: |
  Use kubernetes-the-hard-way with version 1.18...
  # Models may suggest older versions

best_practice: |
  "What's the current recommended way to set up Kubernetes
   clusters in 2024? Please note your training cutoff date."
```

### Verification Strategies for DevOps

```bash
# Always verify AI-generated commands before running!

# Strategy 1: Use --dry-run
kubectl apply -f ai-generated.yaml --dry-run=client

# Strategy 2: Use explain/help
kubectl explain deployment.spec.replicas
terraform plan  # Never apply without plan

# Strategy 3: Check documentation
man <command>
<command> --help

# Strategy 4: Test in isolation
docker run --rm -it ubuntu bash
# Test AI-suggested commands in container first

# Strategy 5: Version check
# AI might suggest deprecated syntax
kubectl version
terraform version
ansible --version
```

---

## 2.8 Practical Token Management

### Counting Tokens Programmatically

```python
# Using tiktoken (OpenAI's tokenizer)
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens for a given text and model."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Example usage
dockerfile = """
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
"""

tokens = count_tokens(dockerfile)
print(f"Dockerfile tokens: {tokens}")  # ~45 tokens

# For Claude, use Anthropic's tokenizer
from anthropic import Anthropic

client = Anthropic()
# Claude's API handles tokenization internally
# You can estimate ~4 chars per token for planning
```

### Token Budget Planning

```python
# Example: Building a code review system with token budgets

class CodeReviewBudget:
    def __init__(self, max_context=100000):  # Claude's context
        self.max_context = max_context
        self.reserved_output = 4000  # Reserve for response
        self.system_prompt = 500     # Fixed system instructions

    def available_for_code(self):
        return self.max_context - self.reserved_output - self.system_prompt

    def can_review(self, code: str) -> bool:
        code_tokens = len(code) // 4  # Rough estimate
        return code_tokens <= self.available_for_code()

    def split_for_review(self, code: str) -> list:
        """Split large codebases into reviewable chunks."""
        available = self.available_for_code()
        chars_per_chunk = available * 4  # Convert back to chars

        chunks = []
        for i in range(0, len(code), chars_per_chunk):
            chunks.append(code[i:i + chars_per_chunk])
        return chunks

# Usage
budget = CodeReviewBudget()
large_codebase = open("main.py").read()

if budget.can_review(large_codebase):
    review(large_codebase)
else:
    chunks = budget.split_for_review(large_codebase)
    for i, chunk in enumerate(chunks):
        print(f"Reviewing chunk {i+1}/{len(chunks)}")
        review(chunk)
```

---

## 2.9 Hands-On Exercises

### Exercise 1: Token Counting Practice

```markdown
## Token Estimation Exercise

Estimate the tokens for each, then verify with a tokenizer:

1. Your company's main README.md file
   Estimate: _______
   Actual: _______

2. A typical Kubernetes deployment manifest
   Estimate: _______
   Actual: _______

3. Your longest shell script
   Estimate: _______
   Actual: _______

4. The last error log you debugged
   Estimate: _______
   Actual: _______
```

### Exercise 2: Context Window Planning

```yaml
# Plan a conversation for debugging a production issue

Scenario: API returning 500 errors intermittently

Available context: 100,000 tokens

# Plan your token budget:
system_instructions:
  content: "You are a DevOps expert..."
  estimated_tokens: _____

error_logs:
  content: "Last 100 relevant log entries"
  estimated_tokens: _____

config_files:
  content: "Relevant YAML configs"
  estimated_tokens: _____

code_context:
  content: "Related source files"
  estimated_tokens: _____

conversation_history:
  content: "Previous Q&A in session"
  estimated_tokens: _____

reserved_for_response:
  estimated_tokens: _____

# Total: _____ / 100,000
```

### Exercise 3: Temperature Experiment

```markdown
## Temperature Effects on Code Generation

Try the same prompt with different temperatures:

Prompt: "Write a bash function to retry a command 3 times with backoff"

Temperature 0.0:
```
[Response here]
```

Temperature 0.7:
```
[Response here]
```

Temperature 1.2:
```
[Response here]
```

## Observations:
- Consistency at temp 0:
- Variation at temp 0.7:
- Creativity/Errors at temp 1.2:
```

---

## 2.10 Chapter Summary

### Key Takeaways

1. **LLMs are sophisticated pattern matchers** - They predict statistically likely text based on training data

2. **Tokens are the currency of LLMs** - Everything (input + output) is measured in tokens; ~4 characters per token

3. **Context window is your working memory** - Plan your prompts to fit within limits; larger windows enable more complex tasks

4. **Cost = Input tokens + Output tokens** - Use appropriate models for different tasks to optimize costs

5. **Temperature controls creativity vs. consistency** - Use low temperature for deterministic outputs, higher for brainstorming

6. **Always verify AI outputs** - LLMs can hallucinate; trust but verify, especially for commands and configurations

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│                    LLM QUICK REFERENCE                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Token Estimation:                                             │
│  • ~4 characters = 1 token                                     │
│  • ~0.75 words = 1 token                                       │
│  • 100 lines of code ≈ 1,000 tokens                            │
│                                                                │
│  Temperature Guide:                                            │
│  • 0.0 = Deterministic (code, configs)                         │
│  • 0.7 = Balanced (general use)                                │
│  • 1.0+ = Creative (brainstorming)                             │
│                                                                │
│  Context Windows (2025):                                       │
│  • GPT-4 Turbo: 128K tokens                                    │
│  • Claude 4.5: 200K tokens                                     │
│                                                                │
│  Verification Commands:                                        │
│  • kubectl --dry-run=client                                    │
│  • terraform plan                                              │
│  • shellcheck script.sh                                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: Introduction to AI](./01-introduction-to-ai.md) | [Next: The Art of Prompting →](./03-the-art-of-prompting.md)

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0
