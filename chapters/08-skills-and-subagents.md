# Chapter 8: Skills and Sub-Agents

## Extending Claude Code with Custom Capabilities

**📖 Reading time:** ~9 minutes | **⚙️ Hands-on time:** ~40 minutes
**🎯 Quick nav:** [Agents](#81-understanding-agents-in-claude-code) | [Skills](#82-skills-system) | [Sub-Agents](#83-sub-agents-and-task-delegation) | [Workflows](#84-advanced-agentic-workflows) | [Task Tool](#85-the-task-tool-sub-agent-spawning) | [🏋️ Skip to Exercises](#86-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** Claude Code becomes exponentially more powerful when you extend it with skills (custom knowledge) and sub-agents (parallel specialized workers). This chapter teaches you to create reusable capabilities and orchestrate complex multi-agent workflows.

**Key concepts:**
- **Skills** = Custom knowledge/capabilities that teach Claude Code about your tech stack, company standards, and common patterns
- **Built-in skills** = kubernetes, terraform, docker, security (ready to use)
- **Custom skills** = Create your own for team-specific needs (hot-reload in v2.1.3)
- **Sub-agents** = Spawn specialized instances for parallel or isolated work
- **Context forking** = Run skills in isolated environments (prevents context pollution)
- **Task Tool** = Claude Code's mechanism for spawning and managing sub-agents

**Most important takeaway:** Skills teach Claude Code what to do, sub-agents let it do multiple things at once. Combined, they transform Claude Code from a helpful assistant into an autonomous DevOps platform.

**Hands-on:** [Jump to exercises](#86-hands-on-exercises) to build your first custom skill and orchestrate a multi-agent workflow.

---

*💡 Need the full guide? Keep reading. Ready to build? Jump to exercises!*

---

This chapter covers how to extend Claude Code with custom capabilities through skills and leverage sub-agents for complex autonomous workflows.

---

**📖 Reading time:** ~17 minutes | **⚙️ Hands-on time:** ~60 minutes
**🎯 Quick nav:** [Agents](#81-understanding-agents-in-claude-code) | [Skills](#82-skills-system) | [Sub-Agents](#83-sub-agents-and-task-delegation) | [Hooks](#86-hooks-system) | [🏋️ Skip to Exercises](#810-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** Claude Code isn't just an AI assistant – it's an autonomous agent that can plan, execute, and verify complex multi-step tasks. This chapter teaches you to extend its capabilities with skills, spawn sub-agents for parallel work, and automate workflows with hooks.

**Key concepts:**
- **Skills** = Custom knowledge/capabilities for specific domains (Kubernetes, AWS, your company's standards)
- **Sub-agents** = Spawn specialized instances for parallel or isolated work (e.g., security audit while you keep coding)
- **Hooks** = Automated triggers (run linters on save, validate configs before deployment, log all commands)
- **Context forking** = Run skills in isolated environments to prevent context pollution
- **Skills and commands are now unified** (v2.1.3) - same thing, simpler mental model

**Most important takeaway:** Transform Claude Code from a helpful assistant into a fully autonomous DevOps platform that knows your infrastructure, follows your standards, and works on multiple tasks simultaneously.

**Hands-on:** [Jump to exercises](#810-hands-on-exercises) to build a custom skill, set up hooks, and orchestrate multi-agent workflows.

---

*💡 Need the full mastery guide? Keep reading. Ready to build? Jump to exercises!*

---

This chapter covers the most powerful features of Claude Code: the agentic capabilities that enable autonomous task completion, specialized skills, and the ability to spawn sub-agents for complex workflows.

---

## 8.1 Understanding Agents in Claude Code

### What is an Agent?

In AI terminology, an **agent** is a system that can:
1. Perceive its environment (read files, understand context)
2. Make decisions (reason about what to do)
3. Take actions (execute commands, edit files)
4. Learn from feedback (adjust based on results)

```
┌────────────────────────────────────────────────────────────────┐
│                    AGENTIC BEHAVIOR MODEL                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│    ┌─────────────────────────────────────────────────────┐     │
│    │              YOUR REQUEST                           │     │
│    │   "Add caching to the user endpoint"                │     │
│    └──────────────────────┬──────────────────────────────┘     │
│                           │                                    │
│                           ▼                                    │
│    ┌─────────────────────────────────────────────────────┐     │
│    │              PERCEIVE                               │     │
│    │   • Read existing code                              │     │
│    │   • Understand project structure                    │     │
│    │   • Identify patterns used                          │     │
│    └──────────────────────┬──────────────────────────────┘     │
│                           │                                    │
│                           ▼                                    │
│    ┌─────────────────────────────────────────────────────┐     │
│    │              PLAN                                   │     │
│    │   • Decide on caching strategy                      │     │
│    │   • Identify files to modify                        │     │
│    │   • Plan implementation steps                       │     │
│    └──────────────────────┬──────────────────────────────┘     │
│                           │                                    │
│                           ▼                                    │
│    ┌─────────────────────────────────────────────────────┐     │
│    │              ACT                                    │     │
│    │   • Edit code files                                 │     │
│    │   • Add dependencies                                │     │
│    │   • Update configurations                           │     │
│    └──────────────────────┬──────────────────────────────┘     │
│                           │                                    │
│                           ▼                                    │
│    ┌─────────────────────────────────────────────────────┐     │
│    │              VERIFY                                 │     │
│    │   • Run tests                                       │     │
│    │   • Check for errors                                │     │
│    │   • Validate changes work                           │     │
│    └──────────────────────┬──────────────────────────────┘     │
│                           │                                    │
│                           ▼                                    │
│    ┌─────────────────────────────────────────────────────┐     │
│    │              ITERATE (if needed)                    │     │
│    │   • Fix any issues found                            │     │
│    │   • Refine implementation                           │     │
│    │   • Re-verify                                       │     │
│    └─────────────────────────────────────────────────────┘     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Claude Code as an Autonomous Agent

```yaml
# Claude Code's agentic capabilities

autonomous_actions:
  file_operations:
    - "Read any file in the project"
    - "Create new files"
    - "Edit existing files"
    - "Delete files (with approval)"

  shell_operations:
    - "Run any shell command"
    - "Install packages"
    - "Run tests"
    - "Execute scripts"

  reasoning:
    - "Understand complex codebases"
    - "Make architectural decisions"
    - "Debug issues systematically"
    - "Plan multi-step implementations"

  verification:
    - "Run tests to verify changes"
    - "Check for syntax errors"
    - "Validate configurations"
    - "Test API endpoints"

human_in_the_loop:
  always_asks: "Before executing commands or making changes"
  configurable: "Can auto-approve certain actions"
  override: "You can stop any operation with Ctrl+C"
```

---

## 8.2 Skills System

### What are Skills?

**Skills** are pre-built capabilities that extend Claude Code's functionality for specific domains or tasks.

> **New in v2.1.3 (January 2025):** Skills and slash commands are now **fully unified** - there's no conceptual difference between them anymore. This simplifies the mental model with no change in behavior. Any skill you create is automatically available as a command (e.g., `/skill-name`).
>
> **Skills placed in `~/.claude/skills` or `.claude/skills` are hot-reloaded** - they become available immediately without restarting Claude Code. You can also configure your preferred **release channel** (`stable` or `latest`) using `/config`.
>
> **Version Compatibility:** This guide covers features up to Claude Code v2.1.4 (January 2025).

```
┌────────────────────────────────────────────────────────────────┐
│                       SKILLS SYSTEM                            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   Skills = Specialized knowledge + Tools + Patterns            │
│                                                                │
│   ┌──────────────────┐  ┌────────────────────┐                 │
│   │  Kubernetes      │  │  Terraform         │                 │
│   │  Skill           │  │  Skill             │                 │
│   │                  │  │                    │                 │
│   │  • K8s manifests │  │  • AWS/GCP/Azure   │                 │
│   │  • Helm charts   │  │  • Module patterns │                 │
│   │  • kubectl cmds  │  │  • State mgmt      │                 │
│   │  • Debugging     │  │  • Best practices  │                 │
│   └──────────────────┘  └────────────────────┘                 │
│                                                                │
│   ┌──────────────────┐  ┌──────────────────┐                   │
│   │  Docker          │  │  CI/CD           │                   │
│   │  Skill           │  │  Skill           │                   │
│   │                  │  │                  │                   │
│   │  • Dockerfile    │  │  • GitHub Actions│                   │
│   │  • Compose       │  │  • GitLab CI     │                   │
│   │  • Optimization  │  │  • Jenkins       │                   │
│   │  • Security      │  │  • ArgoCD        │                   │
│   └──────────────────┘  └──────────────────┘                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Using Skills

```bash
# List available skills
claude
> /skills

# Activate a skill
> /skill kubernetes

# Claude now has enhanced K8s knowledge and will:
# - Use K8s best practices automatically
# - Understand kubectl commands better
# - Generate proper manifests
# - Debug K8s-specific issues

# Skills can be combined
> /skill kubernetes terraform
# Now Claude is optimized for K8s-on-Terraform workflows
```

### Built-in Skills for DevOps

```yaml
# Key skills for DevOps engineers

kubernetes:
  capabilities:
    - "Generate and validate K8s manifests"
    - "Debug pod issues"
    - "Optimize resource requests/limits"
    - "Helm chart generation"
    - "Network policy configuration"
  example_use: |
    /skill kubernetes
    > Create a deployment for nginx with:
      - 3 replicas
      - Rolling update strategy
      - Liveness and readiness probes
      - Resource limits

terraform:
  capabilities:
    - "Generate modules for AWS/GCP/Azure"
    - "State management best practices"
    - "Security hardening"
    - "Cost optimization"
  example_use: |
    /skill terraform
    > Create a module for an RDS instance with:
      - Multi-AZ deployment
      - Encryption at rest
      - Automated backups
      - Parameter groups for PostgreSQL

docker:
  capabilities:
    - "Optimize Dockerfiles"
    - "Multi-stage builds"
    - "Security scanning"
    - "Compose configurations"
  example_use: |
    /skill docker
    > Optimize this Dockerfile for production:
      [paste Dockerfile]

cicd:
  capabilities:
    - "GitHub Actions workflows"
    - "GitLab CI pipelines"
    - "Jenkins pipelines"
    - "ArgoCD applications"
  example_use: |
    /skill cicd
    > Create a GitHub Actions workflow for:
      - PR validation (lint, test, security)
      - Build and push to ECR on merge
      - Deploy to EKS staging

security:
  capabilities:
    - "Security scanning"
    - "Vulnerability assessment"
    - "Secret management patterns"
    - "Compliance checking"
  example_use: |
    /skill security
    > Audit this codebase for:
      - Hardcoded credentials
      - Injection vulnerabilities
      - Insecure configurations
```

### Creating Custom Skills

```yaml
# .claude/skills/my-company-standards.yaml

name: my-company-standards
description: Company-specific coding and deployment standards

knowledge:
  - "We use AWS EKS for all Kubernetes deployments"
  - "All services must have Prometheus metrics on /metrics"
  - "Use DataDog for logging via the dd-agent sidecar"
  - "All Terraform must use our internal module registry"
  - "Python code follows Black formatting"

templates:
  deployment: |
    # Standard deployment template
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        ad.datadoghq.com/tags: '{"team":"{{team}}"}'
    # ... rest of template

  service: |
    # Standard service template
    apiVersion: v1
    kind: Service
    # ...

commands:
  - name: "lint"
    command: "make lint"
  - name: "test"
    command: "make test"
  - name: "deploy"
    command: "make deploy ENV={{env}}"

patterns:
  error_handling: "Use structured logging with correlation IDs"
  api_versioning: "Always version APIs as /api/v1/, /api/v2/"
  database: "Use connection pooling with PgBouncer"
```

```bash
# Load custom skill
> /skill load .claude/skills/my-company-standards.yaml

# Now Claude follows your company standards automatically
```

### Sub-Agent Context Forking (New in 2.1)

Skills can now run in a **forked sub-agent context** using frontmatter:

```markdown
// .claude/skills/security-audit.md
---
name: security-audit
description: Run security audit in isolated context
context: fork    # NEW: Run in forked sub-agent context
---

Perform a comprehensive security audit...
```

With `context: fork`:
- The skill runs in an isolated sub-agent with its own context
- The main conversation context is preserved
- Useful for long-running or resource-intensive skills
- Results are returned to the main conversation when complete

> **What Changed:** Previously, all skills ran in the main conversation context, which could lead to context pollution for complex operations. Now you can isolate skill execution.

---

## 8.3 Sub-Agents and Task Delegation

### What are Sub-Agents?

**Sub-agents** are specialized instances that Claude Code can spawn to handle specific parts of a complex task.

```
┌────────────────────────────────────────────────────────────────┐
│                    SUB-AGENT ARCHITECTURE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│                    ┌─────────────────────┐                     │
│                    │   MAIN AGENT        │                     │
│                    │   (Coordinator)     │                     │
│                    └─────────┬───────────┘                     │
│                              │                                 │
│         ┌────────────────────┼────────────────────┐            │
│         │                    │                    │            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Sub-Agent:  │    │ Sub-Agent:  │    │ Sub-Agent:  │         │
│  │ Code Review │    │ Test Writer │    │ Docs Writer │         │
│  │             │    │             │    │             │         │
│  │ • Security  │    │ • Unit tests│    │ • README    │         │
│  │ • Quality   │    │ • Int tests │    │ • API docs  │         │
│  │ • Style     │    │ • E2E tests │    │ • Comments  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                    │                    │            │
│         └────────────────────┼────────────────────┘            │
│                              │                                 │
│                              ▼                                 │
│                    ┌─────────────────────┐                     │
│                    │   FINAL RESULT      │                     │
│                    │   (Aggregated)      │                     │
│                    └─────────────────────┘                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Using Sub-Agents

```bash
# Complex task that benefits from sub-agents
claude

> I need to prepare this service for production deployment.
  Please run these checks in parallel:
  1. Security audit of the codebase
  2. Performance analysis
  3. Test coverage assessment
  4. Documentation completeness

# Claude spawns sub-agents for parallel processing:
# [Sub-agent 1]: Security scanning...
# [Sub-agent 2]: Performance analysis...
# [Sub-agent 3]: Test coverage check...
# [Sub-agent 4]: Documentation review...

# Results are aggregated and presented together
```

### Sub-Agent Types

```yaml
# Available sub-agent specializations

explorer_agent:
  purpose: "Explore and understand codebases"
  capabilities:
    - "Fast file searching"
    - "Pattern recognition"
    - "Architecture mapping"
  use_case: "Finding where functionality is implemented"
  example: |
    > Where is authentication handled in this codebase?
    # Spawns explorer agent to efficiently search

planner_agent:
  purpose: "Create implementation plans"
  capabilities:
    - "Break down complex tasks"
    - "Identify dependencies"
    - "Estimate complexity"
  use_case: "Planning large features or refactors"
  example: |
    > Plan the migration from REST to GraphQL
    # Spawns planner agent to create detailed plan

code_writer_agent:
  purpose: "Write and modify code"
  capabilities:
    - "Generate new code"
    - "Refactor existing code"
    - "Follow patterns"
  use_case: "Implementing features"

test_agent:
  purpose: "Create and run tests"
  capabilities:
    - "Generate unit tests"
    - "Create integration tests"
    - "Run test suites"
  use_case: "Ensuring code quality"

reviewer_agent:
  purpose: "Review code for issues"
  capabilities:
    - "Security analysis"
    - "Performance review"
    - "Best practice checking"
  use_case: "Code review automation"
```

### Explicit Sub-Agent Control

```bash
# Manually spawn specific sub-agents

# Spawn an explorer agent
> @explorer Find all files that handle database connections

# Spawn a security-focused reviewer
> @security-reviewer Audit the authentication module

# Spawn multiple agents in parallel
> @parallel {
    @code-writer "Add input validation to all API endpoints"
    @test-writer "Create tests for the new validation"
    @doc-writer "Update API documentation"
  }
```

### Background Agents (New in 2.0.64)

Agents can now run asynchronously in the background:

```bash
# Start a long-running task in the background
# The agent will notify you when complete

# Use Ctrl+B to background all running foreground tasks
# This is a unified shortcut that works across all task types

# View running background tasks
> /tasks

# Background agents send wake-up messages when they complete,
# so you can continue working on other tasks
```

> **What Changed:** Previously, you had to wait for agents to complete. Now you can send tasks to the background with Ctrl+B and continue working. You'll be notified when they finish.

---

## 8.4 Advanced Agentic Workflows

### Workflow 1: Full Feature Implementation

```bash
# Let Claude autonomously implement a complete feature

claude

> Implement a rate limiting feature for our API:

Requirements:
- Use Redis for distributed rate limiting
- Limit: 100 requests per minute per API key
- Return 429 with retry-after header when exceeded
- Add bypass for internal services
- Include monitoring metrics
- Write comprehensive tests
- Update API documentation

You have permission to:
- Create new files
- Modify existing files
- Install dependencies
- Run tests

Please implement this completely and verify it works.

# Claude will:
# 1. Analyze existing codebase structure
# 2. Design the rate limiting solution
# 3. Create the rate limiter module
# 4. Integrate with existing middleware
# 5. Add Redis configuration
# 6. Write unit and integration tests
# 7. Run tests and fix any issues
# 8. Update documentation
# 9. Report completion with summary
```

### Workflow 2: Multi-Service Refactoring

```bash
# Refactoring across a microservices codebase

> We need to update our authentication across all services:

Current state:
- 5 microservices
- Each has its own JWT validation
- Want to centralize to auth-service

Tasks:
1. Create shared auth client library
2. Update each service to use the library
3. Add integration tests for auth flow
4. Update deployment configs for auth-service dependency
5. Create migration runbook

Work through each service methodically and ensure
all tests pass before moving to the next.

# Claude coordinates sub-agents:
# - Library writer for shared auth client
# - Per-service updater for each microservice
# - Test writer for integration tests
# - Doc writer for runbook
```

### Workflow 3: Incident Investigation

```bash
# Automated incident investigation

> Investigate why the payment service is failing:

Symptoms:
- 500 errors increased at 14:32 UTC
- Error rate: 23%
- Affected endpoint: POST /payments

I'm attaching:
- Last 1000 lines of application logs
- Recent git commits
- Current pod status

Please:
1. Analyze the logs for root cause
2. Check if recent commits could be related
3. Identify the specific failure point
4. Suggest immediate mitigation
5. Propose long-term fix

# Claude spawns sub-agents:
# - Log analyzer
# - Git commit reviewer
# - Code analyzer
# - Solution architect
```

### Workflow 4: Continuous Code Quality

```bash
# Set up autonomous code quality maintenance

> Create a code quality automation system:

1. On each git commit, run:
   - Linting
   - Type checking
   - Security scanning

2. On each PR, run:
   - Full test suite
   - Code coverage check (fail if < 80%)
   - AI code review

3. Weekly:
   - Dependency vulnerability scan
   - Dead code detection
   - Performance regression check

Create the necessary:
- Git hooks
- GitHub Actions workflows
- Configuration files
- Monitoring dashboards

# Claude creates complete automation infrastructure
```

---

## 8.5 The Task Tool (Sub-Agent Spawning)

### Understanding the Task Tool

The **Task Tool** is Claude Code's mechanism for spawning specialized sub-agents:

```yaml
# Task tool parameters

task_tool:
  description: "Launch a specialized sub-agent for complex tasks"

  parameters:
    subagent_type:
      description: "Type of specialized agent to spawn"
      options:
        - "general-purpose"     # Multi-step tasks
        - "Explore"            # Codebase exploration
        - "Plan"               # Implementation planning
        - "code-reviewer"      # Code review (if configured)

    prompt:
      description: "The task for the agent to perform"
      type: "string"

    model:
      description: "Model to use (optional)"
      options:
        - "sonnet"   # Default, balanced
        - "opus"     # Complex reasoning
        - "haiku"    # Fast, simple tasks

  behavior:
    - "Sub-agents run autonomously"
    - "Report back when complete"
    - "Can be run in parallel"
    - "Each has its own context"
```

### Task Tool Examples

```bash
# These are examples of how Claude Code uses sub-agents internally

# Example 1: Exploring codebase
# When you ask: "How does authentication work?"
# Claude may spawn:
Task(
  subagent_type="Explore",
  prompt="Find all authentication-related code and explain the flow"
)

# Example 2: Planning implementation
# When you ask: "Plan how to add caching"
# Claude may spawn:
Task(
  subagent_type="Plan",
  prompt="Design a caching strategy for the user API endpoints"
)

# Example 3: General multi-step task
# When you ask: "Update all tests to use new mocking"
# Claude may spawn:
Task(
  subagent_type="general-purpose",
  prompt="Find all test files, identify mocking patterns, update to new approach"
)
```

---


---

## 8.6 Hands-On Exercises

### Exercise 1: Build a Custom Skill

```yaml
# Create a skill for your team's workflow

# 1. Analyze your team's patterns
# - What frameworks do you use?
# - What standards do you follow?
# - What common tasks do you repeat?

# 2. Create skill file: .claude/skills/team-skill.yaml
name: my-team
description: Our team's standards and patterns

knowledge:
  # Add your team's knowledge
  - "We use AWS EKS for Kubernetes"
  - "All services must expose /metrics"
  - "Follow company coding standards"

templates:
  # Add your common templates
  deployment: |
    # Your deployment template

patterns:
  # Add your patterns
  error_handling: "Use structured logging"

# 3. Test the skill
# claude
# > /skill my-team
# > Create a new service following our standards
```

### Exercise 2: Multi-Agent Workflow

```bash
# Design and execute a multi-agent workflow

# Scenario: Prepare a service for production

# 1. Plan the workflow
# > Plan a comprehensive production readiness check for this service

# 2. Execute with sub-agents
# > Run these checks in parallel:
#   - Security audit (use security skill)
#   - Performance analysis
#   - Test coverage report
#   - Documentation review
#   - Dependency vulnerability scan

# 3. Generate report
# > Compile findings into a production readiness report

# 4. Document the process for repeatability
```

---

### 💡 Hands-On Practice

Ready to apply these concepts? The **[Claude Code Helper](https://github.com/michelabboud/claude-code-helper/tree/main/examples/agents)** repository provides 14+ production-ready agent examples including skills, sub-agents, and agentic workflows.

---

## 8.7 Chapter Summary

### Key Takeaways

1. **Skills extend Claude Code** with domain-specific knowledge and patterns
   - Use built-in skills (kubernetes, terraform, docker)
   - Create custom skills for your team's standards
   - Skills are now unified with commands (v2.1.3)
   - Hot-reload means instant availability

2. **Sub-agents enable parallel and isolated work**
   - Spawn specialized agents for complex tasks
   - Run multiple sub-agents in parallel
   - Context forking prevents context pollution
   - Task tool manages sub-agent lifecycle

3. **Agentic workflows automate complex processes**
   - Chain multiple skills and sub-agents
   - Claude Code orchestrates autonomous execution
   - Iterate on results until goals are achieved

4. **Professional usage requires customization**
   - Build skills for your tech stack
   - Create sub-agent workflows for common tasks
   - Use Task tool for complex multi-step operations

### Next Steps

- [Chapter 9: Hooks and Advanced Features](./09-hooks-and-advanced-features.md) - Automate with hooks, integrate CI/CD
- Try the hands-on exercises above
- Create your first custom skill
- Experiment with multi-agent workflows

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0
