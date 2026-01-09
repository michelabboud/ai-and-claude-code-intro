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

# The Art of Prompting

## Chapter 3: AI and Claude Code Guide

**Mastering AI Communication**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# What is a Prompt?

## Any text input to an LLM

```
┌─────────────────────────────────┐
│  SYSTEM PROMPT                  │
│  "You are a DevOps expert..."   │
└─────────────────────────────────┘
              +
┌─────────────────────────────────┐
│  USER PROMPT                    │
│  "How do I set up HPA?"         │
└─────────────────────────────────┘
              +
┌─────────────────────────────────┐
│  CONTEXT                        │
│  "Here's my deployment..."      │
└─────────────────────────────────┘
```

---

# Prompt Quality Spectrum

```
Poor                                    Excellent
─────────────────────────────────────────────────►

"fix this"     "my script      "Debug this bash
               is broken"      script that processes
                              logs. Error on line 23.
                              Ubuntu 22.04. Here's
                              the code: [...]
                              And the error: [...]"
```

---

# The CRAFT Framework

## A DevOps Prompting System

- **C**ontext - Environment, versions, constraints
- **R**ole - Who should the AI be?
- **A**ction - What to do specifically
- **F**ormat - Desired output structure
- **T**arget - Success criteria

---

# CRAFT Example

```markdown
## Context
Python microservice on AWS EKS (v1.28)

## Role
Act as a senior SRE specializing in K8s

## Action
Create a script that:
1. Queries Prometheus for pod restarts
2. Fetches logs from problem pods
3. Sends summary to Slack

## Format
Python script with comments

## Target
Script should complete in <60 seconds
```

---

# Prompting Techniques

## Zero-Shot
Direct question, no examples

## One-Shot
One example to guide format

## Few-Shot
Multiple examples for patterns

## Chain-of-Thought
Step-by-step reasoning

---

# Zero-Shot Example

```markdown
**Prompt:**
Convert this JSON to YAML:
{"apiVersion": "v1", "kind": "ConfigMap"}

**Response:**
apiVersion: v1
kind: ConfigMap
```

Best for: **Simple, unambiguous tasks**

---

# Few-Shot Example

```markdown
Parse logs to JSON:

Example 1:
Input: "2024-01-15 ERROR [auth] Login failed"
Output: {"timestamp": "...", "level": "ERROR", ...}

Example 2:
Input: "2024-01-15 INFO [api] Request completed"
Output: {"timestamp": "...", "level": "INFO", ...}

Now parse this:
Input: "2024-01-15 WARN [db] Pool at 80%"
```

Best for: **Consistent formatting, complex patterns**

---

# Chain-of-Thought Example

```markdown
**Prompt:**
API latency is 2.5s (should be <200ms). Think step-by-step:
- Database: PostgreSQL RDS
- Cache: Redis ElastiCache
- No recent deployments

Walk me through diagnosing this issue.
```

Best for: **Debugging, complex problem-solving**

---

# Role-Based Prompting

## Get Different Perspectives

```markdown
**Security Focus:**
"You are a security engineer. Review this
Dockerfile for vulnerabilities..."

**Performance Focus:**
"You are a performance engineer. Review
this Dockerfile for optimization..."

**Cost Focus:**
"You are a FinOps engineer. Analyze this
Dockerfile for cost reduction..."
```

---

# DevOps Troubleshooting Template

```markdown
## Issue Description
[Brief description]

## Environment
- OS: Ubuntu 22.04
- K8s: 1.28, Docker: 24.0
- Cloud: AWS EKS

## What I've Tried
1. Checked logs
2. Verified network

## Relevant Output
[paste logs/errors]

## Questions
1. What's causing this?
2. How do I fix it?
```

---

# Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too vague | "How do I deploy?" → "Deploy Python Flask to EKS using GitHub Actions" |
| No context | Add environment, versions, constraints |
| Too much at once | Break into steps |
| No format | Specify: table, code, steps |

---

# Prompting Tips

## 1. Use Delimiters
```markdown
---
CONTEXT: Ubuntu 22.04, K8s 1.28
---
PROBLEM: Pods are crashing
---
QUESTION: What's wrong?
---
```

## 2. Specify What NOT to Do
```markdown
Do NOT use rm -rf
Do NOT require root
```

---

# Building a Prompt Library

## Save Effective Prompts

```yaml
# ~/.ai-prompts/devops-templates.yaml

code_review:
  template: |
    Review {{file}} for:
    - Security issues
    - Performance
    - Error handling
    Output as: Critical/High/Medium/Low

incident_response:
  template: |
    Analyze incident for {{service}}:
    Symptoms: {{symptoms}}
    Logs: {{logs}}
```

---

# Shell Function for Quick Prompts

```bash
# Add to ~/.bashrc

ai_debug() {
    claude "Debug this error: $*

    Please:
    1. Identify potential causes
    2. Suggest diagnostic commands
    3. Provide solution steps"
}

# Usage:
ai_debug "Connection refused to port 5432"
```

---

# Iterate and Refine

## Start Simple, Then Improve

```markdown
# First attempt
"Write a backup script"

# After seeing output
"Add error handling for network failures"

# Further refinement
"Also add Slack notifications"
```

---

# Key Takeaways

1. **Good prompts = Good outputs**
2. **Use the CRAFT framework**
3. **Choose right technique** (zero/few-shot, CoT)
4. **Be specific, provide context**
5. **Build a prompt library**
6. **Iterate and refine**

---

# Quick Reference

```
┌─────────────────────────────────────────┐
│  CRAFT Framework:                       │
│  C - Context (environment, versions)    │
│  R - Role (who should AI be)            │
│  A - Action (what to do)                │
│  F - Format (output structure)          │
│  T - Target (success criteria)          │
│                                         │
│  Techniques:                            │
│  • Zero-shot: Direct question           │
│  • Few-shot: Multiple examples          │
│  • Chain-of-thought: Step reasoning     │
│  • Role-based: Expert perspective       │
└─────────────────────────────────────────┘
```

---

# Next: Chapter 4-5

## AI Models & Claude Introduction

- Major AI providers
- Model comparison
- Introduction to Claude
- Claude model family

---

# Questions?

## Resources

- Full chapter: [chapters/03-the-art-of-prompting.md](../chapters/03-the-art-of-prompting.md)

---

# Credits

**Author:** Michel Abboud
**Created with:** Claude AI (Anthropic)

**License:** CC BY-NC 4.0 | © 2026 Michel Abboud
