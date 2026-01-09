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

# Claude Code

## Chapters 6-8: From Basics to Professional

**Your AI Pair Programmer for the Terminal**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# What is Claude Code?

## An Agentic AI Coding Tool

Claude Code can:
- **Read** files in your project
- **Execute** shell commands
- **Edit** existing files
- **Create** new files
- **Run** tests and builds
- **Git** operations

All from your terminal!

---

# Claude.ai vs Claude Code

| Claude.ai | Claude Code |
|-----------|-------------|
| Web browser | Terminal/CLI |
| Copy-paste code | Direct file access |
| You run commands | Executes for you |
| Session-based | Project context |
| Chat/exploration | Development work |

---

# Installation

```bash
# Via npm (recommended)
npm install -g @anthropic-ai/claude-code

# Verify
claude --version

# Authenticate
claude login

# Start using
cd your-project
claude
```

---

# Basic Usage

```bash
# Interactive mode
claude

# Single command
claude "explain this codebase"

# With specific file
claude "review this" --file src/main.py

# Pipe input
cat error.log | claude "what caused this?"
```

---

# Essential Commands

```bash
/help          # Show all commands
/model         # Show/change model
/cost          # Token usage

/clear         # Clear conversation
/save          # Save session
/load          # Load session

/stop          # Stop operation
/exit          # Exit (Ctrl+D)
```

---

# The Approval Flow

```
┌───────────────────────────────────────┐
│  I'll run this command:               │
│  $ npm install express                │
│                                       │
│  [y]es / [n]o / [e]xplain            │
└───────────────────────────────────────┘

You always approve before execution!
```

---

# Core Workflows

## 1. Understanding Codebases

```bash
> explain the structure of this project
> where is authentication handled?
> how does the database connection work?
```

## 2. Writing New Code

```bash
> create a new endpoint POST /api/users
  that validates email and hashes password
```

---

# Core Workflows (cont.)

## 3. Debugging

```bash
> I'm getting this error:
  TypeError: Cannot read property 'map'
  at UserList (/src/UserList.jsx:15)

  Fix this error.
```

## 4. Git Operations

```bash
> commit these changes with a good message
> create a feature branch for auth work
```

---

# DevOps Examples

## Create K8s Manifests

```bash
> Create Kubernetes manifests for this app:
  - Deployment with 3 replicas
  - Service with ClusterIP
  - Health checks on /health
  - Resource limits
```

---

# DevOps Examples

## CI/CD Pipeline

```bash
> Create GitHub Actions workflow that:
  - Runs on push to main
  - Runs npm test
  - Builds Docker image
  - Pushes to ECR
  - Deploys to EKS staging
```

---

# Configuration

## ~/.claude/config.json

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "auto_approve": {
    "read": true,
    "write": false,
    "execute": false
  },
  "context": {
    "exclude_patterns": ["node_modules", ".git"]
  }
}
```

---

# Custom Commands

## .claude/commands/review.md

```markdown
---
name: review
description: Code review
---

Review {{file}} for:
1. Security vulnerabilities
2. Performance issues
3. Error handling
4. Best practices

Output by severity: Critical/High/Medium/Low
```

Usage: `/review src/api.py`

---

# Skills System

## Pre-built Capabilities

```bash
# Activate skills
> /skill kubernetes
> /skill terraform
> /skill docker

# Now Claude has enhanced knowledge
# for these specific domains
```

---

# Sub-Agents

## Parallel Task Processing

```bash
> Run these checks in parallel:
  1. Security audit
  2. Performance analysis
  3. Test coverage
  4. Documentation review

# Claude spawns specialized agents
# for each task
```

---

# Hooks

## .claude/hooks.yaml

```yaml
hooks:
  post_edit:
    - command: "prettier --write {{file}}"
      condition: "{{file}} matches *.js"
    - command: "black {{file}}"
      condition: "{{file}} matches *.py"

  pre_command:
    - command: "echo '{{command}}' >> ~/.claude/log"
```

---

# IDE Integration

## VS Code

- Side panel chat
- Select code → "Ask Claude"
- "Explain this code"
- "Generate tests"

## Terminal + tmux

- Editor on left
- Claude Code on right
- Best of both worlds

---

# Tips for DevOps

## 1. Start in Project Root
Claude understands context better

## 2. Be Specific
```bash
# Good
> Create Python script following patterns
  from src/utils/logger.py
```

## 3. Iterate on Complex Tasks
Break into steps, refine each

---

# Quick Reference

```
┌─────────────────────────────────────────┐
│  Install: npm install -g claude-code    │
│  Start: cd project && claude            │
│                                         │
│  Commands:                              │
│  /help /clear /save /load /exit        │
│                                         │
│  Approval: y=yes n=no e=explain        │
│                                         │
│  Config: ~/.claude/config.json          │
│  Commands: .claude/commands/*.md        │
│  Hooks: .claude/hooks.yaml              │
│                                         │
│  Skills: /skill kubernetes terraform    │
└─────────────────────────────────────────┘
```

---

# Basic → Intermediate → Pro

| Level | Features |
|-------|----------|
| Basic | Commands, workflows, approval |
| Intermediate | Config, custom commands, IDE |
| Professional | Skills, sub-agents, hooks, MCP |

---

# Next: Chapter 9

## MCP Deep Dive

- Model Context Protocol
- Connecting to external systems
- Building custom MCP servers
- DevOps integrations

---

# Questions?

## Resources

- Chapter 6: [claude-code-fundamentals.md](../chapters/06-claude-code-fundamentals.md)
- Chapter 7: [claude-code-intermediate.md](../chapters/07-claude-code-intermediate.md)
- Chapter 8: [claude-code-professional.md](../chapters/08-claude-code-professional.md)

---

# Credits

**Author:** Michel Abboud
**Created with:** Claude AI (Anthropic)

**License:** CC BY-NC 4.0 | © 2026 Michel Abboud
