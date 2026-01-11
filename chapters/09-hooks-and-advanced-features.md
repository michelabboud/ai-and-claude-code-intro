# Chapter 9: Hooks and Advanced Features

**Part 3: Claude Code Mastery**

---

## Navigation

← Previous: [Chapter 8: Skills and Sub-Agents](./08-skills-and-subagents.md) | Next: [Chapter 10: MCP Fundamentals](./10-mcp-fundamentals.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---


## Automation, CI/CD Integration, and Professional Best Practices

**📖 Reading time:** ~9 minutes | **⚙️ Hands-on time:** ~45 minutes
**🎯 Quick nav:** [Hooks](#91-hooks-system) | [Memory](#92-memory-and-context-management) | [CI/CD](#93-cicd-integration-patterns) | [Best Practices](#94-best-practices-for-professional-use) | [🏋️ Skip to Exercises](#95-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** Hooks automate actions at specific points in Claude Code's workflow (format on save, validate before deploy). Combined with memory management and CI/CD patterns, you can build production-grade AI-powered DevOps workflows.

**Key concepts:**
- **Hooks** = Automated triggers that run at workflow events (pre_edit, post_edit, pre_command, session_start, etc.)
- **Hook timeout** = 10 minutes (v2.1.3), enough for complex validation
- **Memory management** = Long-term context that persists across sessions
- **CI/CD integration** = Use Claude Code in GitHub Actions, GitLab CI, etc.
- **Best practices** = Safety guidelines, environment variables, wildcard permissions

**Most important takeaway:** Hooks turn Claude Code from interactive tool to automation platform. Set up once, benefit forever - auto-format, security scan, validate configs, log actions.

**Hands-on:** [Jump to exercises](#95-hands-on-exercises) to set up hooks and build an automated workflow. See [Hooks Cookbook](../references/hooks-cookbook.md) for 20+ ready-to-use examples.

---

*💡 Need the automation guide? Keep reading. Want hook examples? Jump to [Hooks Cookbook](../references/hooks-cookbook.md)!*

---

This chapter covers automation through hooks, context management, CI/CD integration, and professional best practices for using Claude Code at scale.

---

## 9.1 Hooks System

### What are Hooks?

**Hooks** allow you to run custom commands at specific points in Claude Code's workflow.

> **New in v2.1.3:** Tool hook execution timeout has been increased from 60 seconds to **10 minutes**. This allows for more complex validation and processing in hooks without timeout failures.

```yaml
# .claude/hooks.yaml

hooks:
  # Before any file is modified
  pre_edit:
    - command: "cp {{file}} {{file}}.backup"
      description: "Create backup before editing"

  # After files are modified
  post_edit:
    - command: "prettier --write {{file}}"
      condition: "{{file}} matches *.js or *.ts"
      description: "Format JavaScript/TypeScript files"

    - command: "black {{file}}"
      condition: "{{file}} matches *.py"
      description: "Format Python files"

  # Before commands are executed
  pre_command:
    - command: "echo 'Running: {{command}}' >> ~/.claude/command.log"
      description: "Log all commands"

  # After tests are run
  post_test:
    - command: "coverage report --fail-under=80"
      description: "Check coverage threshold"

  # On session start
  session_start:
    - command: "git status"
      description: "Show git status on start"

  # On session end
  session_end:
    - command: "git diff --stat"
      description: "Show changes made in session"
```

### Hook Use Cases for DevOps

```yaml
# DevOps-specific hooks

infrastructure_safety:
  pre_command:
    - command: |
        if echo "{{command}}" | grep -q "terraform destroy"; then
          echo "WARNING: Destructive terraform command detected!"
          read -p "Are you sure? (yes/no): " confirm
          [ "$confirm" = "yes" ] || exit 1
        fi
      description: "Confirm destructive terraform commands"

kubernetes_validation:
  post_edit:
    - command: "kubeval {{file}}"
      condition: "{{file}} matches k8s/*.yaml"
      description: "Validate Kubernetes manifests"

security_scanning:
  post_edit:
    - command: "gitleaks detect --source={{file}} --no-git"
      description: "Scan for secrets in modified files"

docker_linting:
  post_edit:
    - command: "hadolint {{file}}"
      condition: "{{file}} matches *Dockerfile*"
      description: "Lint Dockerfiles"

terraform_formatting:
  post_edit:
    - command: "terraform fmt {{file}}"
      condition: "{{file}} matches *.tf"
      description: "Format Terraform files"
```

---

## 9.2 Memory and Context Management

### Long-Term Memory

```yaml
# .claude/memory.yaml

# Project-specific facts Claude should remember
facts:
  - "This project uses Django 4.2 with PostgreSQL"
  - "We follow GitFlow branching strategy"
  - "Production deployments require two approvals"
  - "The main API is versioned at /api/v2/"
  - "Legacy code in /src/legacy is being deprecated"

# Key contacts and responsibilities
team:
  - "Backend: backend-team@company.com"
  - "DevOps: @devops-team in Slack"
  - "Security: security@company.com for vulnerabilities"

# Important patterns and conventions
conventions:
  naming:
    - "Use snake_case for Python files and functions"
    - "Use kebab-case for Kubernetes resources"
    - "Prefix internal services with 'internal-'"

  architecture:
    - "All external calls go through the gateway service"
    - "Use Redis for caching, with 1-hour default TTL"
    - "Database migrations must be backward compatible"

# Things to avoid
anti_patterns:
  - "Don't use print() for logging, use the logger module"
  - "Never commit to main directly"
  - "Don't hardcode environment-specific values"
```

### Context Prioritization

```yaml
# .claude/context.yaml

# Files Claude should always be aware of
priority_files:
  high:
    - "README.md"
    - "CONTRIBUTING.md"
    - "src/config/*.py"
    - "k8s/*.yaml"

  medium:
    - "docs/*.md"
    - "scripts/*.sh"

# Directories to deeply understand
focus_directories:
  - "src/api/"       # Main API code
  - "src/services/"  # Business logic
  - "tests/"         # Test patterns

# Files to ignore even if relevant
ignore_patterns:
  - "*.min.js"
  - "*.map"
  - "coverage/*"
  - "*.lock"
  - "dist/*"
```

---

## 9.3 CI/CD Integration Patterns

### GitHub Actions Integration

```yaml
# .github/workflows/claude-automation.yaml

name: Claude Code Automation

on:
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:
    inputs:
      task:
        description: 'Task for Claude to perform'
        required: true

jobs:
  claude-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Get changed files
          CHANGED_FILES=$(git diff --name-only origin/${{ github.base_ref }}...)

          # Run Claude review
          claude --non-interactive --output review.md "
            Review these changed files for:
            1. Security issues
            2. Performance problems
            3. Best practices

            Changed files:
            $CHANGED_FILES

            Provide a structured report.
          "

      - name: Post Review
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '## Claude Code Review\n\n' + review
            });

  claude-task:
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'
    steps:
      - uses: actions/checkout@v4

      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Execute Task
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --non-interactive "${{ github.event.inputs.task }}"

      - name: Create PR with changes
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Claude Code: ${{ github.event.inputs.task }}"
          body: "Automated changes by Claude Code"
          branch: "claude-automated-$(date +%s)"
```

### GitLab CI Integration

```yaml
# .gitlab-ci.yml

variables:
  ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY

stages:
  - review
  - deploy

claude-code-review:
  stage: review
  image: node:20
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      claude --non-interactive --output review.md "
        Review the changes in this merge request:
        $(git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD)

        Focus on:
        1. Security vulnerabilities
        2. Code quality issues
        3. Test coverage
      "
  artifacts:
    paths:
      - review.md
  only:
    - merge_requests

claude-generate-docs:
  stage: deploy
  image: node:20
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      claude --non-interactive "
        Update the API documentation in docs/api.md
        based on the current codebase.
      "
    - git add docs/
    - git commit -m "docs: Auto-update API documentation" || true
    - git push
  only:
    - main
  when: manual
```

---

## 9.4 Best Practices for Professional Use

### Safety Guidelines

```yaml
# Professional safety practices

always_verify:
  - "Review generated infrastructure code before applying"
  - "Test in non-production environments first"
  - "Use dry-run modes when available"
  - "Have rollback plans ready"

restrict_permissions:
  - "Use separate API keys for CI/CD vs interactive use"
  - "Limit auto-approve to read operations"
  - "Block destructive commands in hooks"

audit_trail:
  - "Log all Claude Code sessions"
  - "Track changes made by automation"
  - "Review AI-generated code in PRs"

secret_management:
  - "Never include secrets in prompts"
  - "Use environment variables"
  - "Exclude .env files from context"
```

### Environment Variables (New in 2.1.x)

```bash
# Control Claude Code behavior via environment variables

# Disable background tasks (New in v2.1.4)
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1
# Prevents:
# - Auto-backgrounding of long-running commands
# - Ctrl+B backgrounding shortcut
# Useful for: CI/CD environments, demos, teaching scenarios

# Demo mode - hides sensitive information (v2.1.0)
export IS_DEMO=1
# Use when: Recording screencasts, live demos, sharing logs

# Force plugin updates (v2.1.2)
export FORCE_AUTOUPDATE_PLUGINS=1
# Forces: Immediate plugin/skill reload without cache
```

### Wildcard Bash Permissions (New in 2.1)

You can now configure granular bash command permissions using wildcards:

```yaml
# Permission patterns with wildcards
permissions:
  bash:
    allow:
      - "npm *"           # Allow all npm commands
      - "* install"       # Allow any install command
      - "git * main"      # Allow git commands on main branch
      - "docker build *"  # Allow docker build with any args
      - "kubectl get *"   # Allow kubectl get operations

    deny:
      - "rm -rf *"        # Block recursive force delete
      - "* --force"       # Block force flags
```

> **What Changed:** Previously, bash permissions were exact matches only. Now wildcards (`*`) allow flexible permission patterns that cover families of related commands.

### Efficiency Tips

```yaml
# Getting the most out of Claude Code

model_selection:
  exploration: "Use Haiku 4.5 for quick searches"
  implementation: "Use Sonnet 4.5 for most coding tasks"
  architecture: "Use Opus 4.5 for complex decisions"
  note: "Opus 4.5 has thinking mode enabled by default for deeper reasoning"

parallel_processing:
  approach: "Break large tasks into parallel sub-tasks"
  example: |
    > @parallel {
        @agent Review security of src/auth/
        @agent Review security of src/api/
        @agent Review security of src/db/
      }

context_management:
  tip: "Start sessions in the right directory"
  tip: "Use .claude/context.yaml to prioritize files"
  tip: "Clear context between unrelated tasks"

automation_boundaries:
  automate: "Repetitive, well-defined tasks"
  human_review: "Security-critical changes"
  human_decision: "Architecture choices"
```

---

## 9.5 Hands-On Exercises

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
  - ""
  - ""

templates:
  # Add your common templates
  deployment: |
    # Your deployment template

patterns:
  # Add your patterns

# 3. Test the skill
# claude
# > /skill load .claude/skills/team-skill.yaml
# > Create a new service following our standards
```

### Exercise 2: Set Up Hooks

```yaml
# Create a comprehensive hooks setup

# 1. Create .claude/hooks.yaml with:
# - Pre-edit backup
# - Post-edit formatting
# - Pre-command logging
# - Security scanning

# 2. Test each hook:
# - Make an edit, verify backup created
# - Edit a Python file, verify Black ran
# - Run a command, check the log
# - Add a test secret, verify scanner catches it

# 3. Document your hooks for the team
```

### Exercise 3: Multi-Agent Workflow

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

Ready to apply these concepts? The **[Claude Code Helper](https://github.com/michelabboud/claude-code-helper/tree/main/examples/agents)** repository provides 14+ production-ready agent examples:

- **Android Development** - Kotlin/Java, Jetpack Compose, Room database
- **Database Operations** - SQL, PostgreSQL, migrations, optimization
- **REST API Development** - Authentication, testing, documentation
- **Git Workflows** - Branch strategies, commit patterns, automation
- **Performance Optimization** - Bundle analysis, caching, profiling

Each agent includes real-world patterns and comprehensive documentation to complement the exercises above.

---

## 9.6 Chapter Summary

---

## 9.5 Hands-On Exercises

### Exercise 1: Set Up Essential Hooks

```yaml
# Create a comprehensive hooks setup

# 1. Create .claude/hooks.yaml with:
hooks:
  # Session management
  session_start:
    - command: "git status"
      description: "Show git status"

  # File operations
  pre_edit:
    - command: "cp {{file}} {{file}}.backup"
      description: "Backup before edit"

  post_edit:
    # Security scanning
    - command: "gitleaks detect --source={{file}} --no-git || true"
      description: "Scan for secrets"

    # Auto-formatting
    - command: "black {{file}}"
      condition: "{{file}} matches *.py"
      description: "Format Python"

    - command: "terraform fmt {{file}}"
      condition: "{{file}} matches *.tf"
      description: "Format Terraform"

  # Command safety
  pre_command:
    - command: |
        if echo "{{command}}" | grep -qE "destroy|delete.*prod"; then
          echo "🚨 DESTRUCTIVE COMMAND!"
          read -p "Type 'confirm': " response
          [ "$response" = "confirm" ] || exit 1
        fi
      description: "Protect against destructive commands"

# 2. Test each hook:
# - Make an edit, verify backup created
# - Edit a Python file, verify Black ran
# - Try a destructive command, verify protection

# 3. Document your hooks for the team
```

### Exercise 2: CI/CD Integration

```bash
# Integrate Claude Code into your CI/CD pipeline

# 1. Add Claude Code to GitHub Actions
# See Chapter 9 §9.3 for complete workflow example

# 2. Use Claude Code for:
# - Automated code review on PRs
# - Generate test cases for new code
# - Update documentation automatically
# - Analyze performance regressions

# 3. Test locally first:
# claude "review the changes in this PR"
# claude "generate tests for src/api/users.ts"
```

### Exercise 3: Production Safety Setup

```yaml
# Implement production safety measures

# 1. Configure wildcard permissions
permissions:
  bash:
    allow:
      - "kubectl get *"
      - "aws * list*"
      - "terraform plan *"
    deny:
      - "kubectl delete *"
      - "terraform destroy *"
      - "rm -rf *"

# 2. Set up environment variables
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1  # For CI/CD
export IS_DEMO=1  # For presentations

# 3. Create incident response runbook
# Document how to use Claude Code safely in production
```

---

### 💡 Hands-On Practice

**Hook Examples**: See [Hooks Cookbook](../references/hooks-cookbook.md) for 20+ production-ready hook configurations covering:
- File operations
- Security scanning
- Infrastructure validation
- Code quality
- DevOps workflows

---

## 9.6 Chapter Summary

### Key Takeaways

1. **Hooks automate workflows**
   - Run commands at specific workflow events
   - 10-minute timeout for complex operations (v2.1.3)
   - Use for formatting, validation, security, logging
   - See [Hooks Cookbook](../references/hooks-cookbook.md) for examples

2. **Memory management preserves context**
   - Long-term memory across sessions
   - Project-specific facts and patterns
   - Improves Claude Code's understanding

3. **CI/CD integration enables automation**
   - Run Claude Code in pipelines
   - Automated code review
   - Test generation
   - Documentation updates

4. **Best practices ensure safety**
   - Environment variables for control
   - Wildcard permissions for granular access
   - Security scanning in hooks
   - Production safety measures

### Next Steps

- [Chapter 10: MCP Fundamentals](./10-mcp-fundamentals.md) - Connect Claude Code to external systems
- Implement hooks from the [Hooks Cookbook](../references/hooks-cookbook.md)
- Integrate Claude Code into your CI/CD pipeline
- Document your team's standards and workflows

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0

---

## Navigation

← Previous: [Chapter 8: Skills and Sub-Agents](./08-skills-and-subagents.md) | Next: [Chapter 10: MCP Fundamentals](./10-mcp-fundamentals.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 9** | Hooks and Advanced Features | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
