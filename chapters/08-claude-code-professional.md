# Chapter 8: Claude Code Professional

## Mastering Agents, Skills, Sub-Agents, and Advanced Features

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

## 8.6 Hooks System

### What are Hooks?

**Hooks** allow you to run custom commands at specific points in Claude Code's workflow.

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

## 8.7 Memory and Context Management

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

## 8.8 CI/CD Integration Patterns

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

## 8.9 Best Practices for Professional Use

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

### Efficiency Tips

```yaml
# Getting the most out of Claude Code

model_selection:
  exploration: "Use Haiku 4.5 for quick searches"
  implementation: "Use Sonnet 4.5 for most coding tasks"
  architecture: "Use Opus 4.5 for complex decisions"

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

## 8.10 Hands-On Exercises

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

## 8.11 Chapter Summary

### Key Takeaways

1. **Claude Code is an autonomous agent** - Can perceive, plan, act, and verify

2. **Skills extend capabilities** - Pre-built and custom skills for specialized tasks

3. **Sub-agents enable parallel work** - Complex tasks split across specialized agents

4. **Hooks automate workflows** - Run commands at key points in the workflow

5. **Professional use requires safety practices** - Verify, restrict, audit

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│           PROFESSIONAL CLAUDE CODE REFERENCE                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Skills:                                                       │
│  /skills              - List available skills                  │
│  /skill <name>        - Activate a skill                       │
│  /skill load <file>   - Load custom skill                      │
│                                                                │
│  Sub-Agents:                                                   │
│  @explorer            - Codebase exploration                   │
│  @planner             - Implementation planning                │
│  @security-reviewer   - Security analysis                      │
│  @parallel { }        - Run agents in parallel                 │
│                                                                │
│  Hooks:                                                        │
│  .claude/hooks.yaml   - Hook configuration                     │
│  pre_edit, post_edit  - File modification hooks                │
│  pre_command          - Command execution hooks                │
│                                                                │
│  Memory:                                                       │
│  .claude/memory.yaml  - Persistent project facts               │
│  .claude/context.yaml - Context prioritization                 │
│                                                                │
│  CI/CD:                                                        │
│  --non-interactive    - Run without prompts                    │
│  --output <file>      - Save output to file                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: Claude Code Intermediate](./07-claude-code-intermediate.md) | [Next: MCP Deep Dive →](./09-mcp-deep-dive.md)
