# Claude Code Quick Reference

**Essential Commands and Patterns for Daily Use**

---

## Installation & Setup

```bash
# Install Claude Code (macOS/Linux)
curl -fsSL https://cli.anthropic.com/install.sh | sh

# Install via package managers
brew install claude-code        # macOS
apt install claude-code        # Ubuntu/Debian
yum install claude-code        # RHEL/CentOS

# Authenticate
claude auth login

# Check installation
claude --version
claude doctor                  # Diagnose issues
```

---

## Basic Commands

```bash
# Start Claude Code (interactive mode)
claude

# Run single command
claude "what files are in this directory?"

# Execute with specific model
claude --model sonnet "review this code"
claude --model haiku "quick search for TODO comments"
claude --model opus "complex architectural decision needed"

# Background mode
claude &                      # Run in background
Ctrl+B                       # Background current operation
```

---

## Built-in Slash Commands

```bash
# Help & Information
/help                        # Show all commands
/commands                    # List available custom commands
/skills                      # List available skills
/doctor                      # Diagnose configuration issues

# Session Management
/clear                       # Clear conversation history
/reset                       # Reset session
/exit or /quit              # Exit Claude Code

# Configuration
/config                      # Open configuration editor
/model sonnet               # Switch to Sonnet model
/model haiku                # Switch to Haiku model
/model opus                 # Switch to Opus model

# File Operations
/read <file>                # Read file explicitly
/edit <file>                # Edit file
/create <file>              # Create new file

# Context Control
/compact                    # Manually trigger context compaction
/forget <topic>             # Remove specific context
```

---

## Essential Patterns

### Code Review

```bash
# Quick review
claude "review src/api/users.ts for security issues"

# Comprehensive review
claude "perform a thorough code review of src/auth/ checking for:
- Security vulnerabilities
- Performance issues
- Best practices compliance
- Test coverage gaps"
```

### File Operations

```bash
# Read and analyze
claude "read Dockerfile and suggest optimizations"

# Batch editing
claude "add logging to all functions in src/services/*.ts"

# Search and replace
claude "find all TODO comments and create GitHub issues"
```

### DevOps Tasks

```bash
# Infrastructure as Code
claude "generate Terraform for an AWS RDS PostgreSQL instance with:
- Multi-AZ deployment
- Automated backups
- Encryption at rest
- Parameter group for PostgreSQL 15"

# Kubernetes
claude "create K8s deployment for nginx with 3 replicas, health checks, and resource limits"

# CI/CD
claude "generate GitHub Actions workflow for:
- Lint and test on PR
- Build Docker image on merge
- Deploy to staging"
```

### Debugging

```bash
# Analyze errors
claude "analyze this error log and suggest fixes: $(cat error.log)"

# Investigate issues
claude "why is my pod crashlooping? Check deployment.yaml and recent logs"

# Performance analysis
claude "review this SQL query for optimization opportunities: $(cat slow_query.sql)"
```

---

## Configuration Files

### Main Configuration

**Location**: `~/.claude/config.json`

```json
{
  "model": "sonnet",
  "auto_approve": {
    "read": true,
    "write": false
  },
  "max_tokens": 4096,
  "temperature": 0.7
}
```

### Project Configuration

**Location**: `.claude/config.json` (project root)

```json
{
  "context": {
    "include": ["src/**/*.ts", "*.md"],
    "exclude": ["node_modules/**", "dist/**"]
  },
  "skills": ["kubernetes", "terraform", "devops"]
}
```

### CLAUDE.md

**Location**: `./CLAUDE.md` or `./.claude/CLAUDE.md`

```markdown
# Project Context for Claude

## Tech Stack
- Backend: Node.js 20, TypeScript 5.3
- Database: PostgreSQL 15
- Infrastructure: Kubernetes 1.28 on AWS EKS
- CI/CD: GitHub Actions

## Coding Standards
- Follow Airbnb TypeScript style guide
- All functions must have JSDoc comments
- Minimum 80% test coverage required
- Use async/await, never callbacks

## Deployment Process
1. PRs must pass all checks
2. Deploy to staging first
3. Run smoke tests
4. Manual approval for production
```

---

## Custom Commands

### Creating a Command

**Location**: `.claude/commands/review.md`

```markdown
---
name: review
description: Comprehensive code review
arguments:
  - name: file
    description: File to review
    required: true
---

Perform a comprehensive code review of {{file}}:

1. **Security Analysis**
   - Check for vulnerabilities
   - Verify input validation

2. **Performance Review**
   - Identify bottlenecks
   - Check for N+1 queries

3. **Code Quality**
   - Check naming conventions
   - Verify error handling

4. **Best Practices**
   - Framework-specific patterns
   - Project consistency
```

### Using Custom Commands

```bash
# List commands
/commands

# Run command
/review src/api/users.ts

# Run with arguments
/deploy-check staging
```

---

## Skills

### Using Built-in Skills

```bash
# Activate single skill
/skill kubernetes
/skill terraform
/skill docker

# Combine skills
/skill kubernetes terraform
```

### Creating Custom Skills

**Location**: `.claude/skills/company-standards.yaml`

```yaml
name: company-standards
description: Our company's coding and deployment standards

knowledge:
  - "We use AWS EKS for all Kubernetes deployments"
  - "All services must expose /metrics for Prometheus"
  - "Use DataDog for logging"
  - "Terraform must use internal module registry"

templates:
  deployment: |
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        team: "{{team}}"
    spec:
      replicas: {{replicas}}
      # ... template content
```

---

## Hooks

### Common Hook Patterns

**Location**: `.claude/hooks.yaml`

```yaml
hooks:
  # Auto-format on save
  post_edit:
    - command: "prettier --write {{file}}"
      condition: "{{file}} matches *.ts"
      description: "Format TypeScript"

  # Validate before deploy
  pre_command:
    - command: |
        if echo "{{command}}" | grep -q "kubectl apply"; then
          kubectl apply --dry-run=client -f deployment.yaml
        fi
      description: "Dry-run K8s deployments"

  # Security scanning
  post_edit:
    - command: "gitleaks detect --source={{file}}"
      description: "Scan for secrets"
```

---

## MCP Servers

### Configuration

**Location**: `~/.claude/mcp_servers.json`

```json
{
  "kubernetes": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-kubernetes"],
    "env": {
      "KUBECONFIG": "/path/to/kubeconfig"
    }
  },
  "aws": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-aws"],
    "env": {
      "AWS_PROFILE": "production"
    }
  }
}
```

### Using MCP Tools

```bash
# MCP tools are automatically available
claude "list all pods in the production namespace"
claude "show me EC2 instances in us-east-1"
claude "query the database for users created this week"
```

---

## Environment Variables

```bash
# Disable background tasks (useful for CI/CD, demos)
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1

# Demo mode - hide sensitive information
export IS_DEMO=1

# Force plugin updates
export FORCE_AUTOUPDATE_PLUGINS=1

# Set default model
export CLAUDE_MODEL=sonnet

# API key (if not using auth login)
export ANTHROPIC_API_KEY=your_key_here
```

---

## Productivity Tips

### 1. Use CLAUDE.md

Create a `CLAUDE.md` file in your project root with:
- Tech stack details
- Coding standards
- Common commands
- Deployment procedures

Claude Code reads this automatically for every session.

### 2. Create Project-Specific Commands

Build a library of commands for your team's common workflows:
- `/review-pr`
- `/generate-tests`
- `/deploy-staging`
- `/incident-response`

### 3. Leverage Model Selection

- **Haiku**: Quick searches, simple edits (`--model haiku`)
- **Sonnet**: Most coding tasks (default)
- **Opus**: Complex architecture decisions (`--model opus`)

### 4. Use Context Efficiently

```bash
# Be specific about file scope
claude "review only src/api/users.ts, ignore other files"

# Reference specific sections
claude "optimize the getUserById function in src/api/users.ts:45-67"

# Clear context when switching tasks
/clear
```

### 5. Combine with Shell Tools

```bash
# Pipe to Claude
cat error.log | claude "analyze these errors and suggest fixes"

# Use with find
find . -name "*.ts" | xargs claude "add JSDoc comments to all exported functions"

# Git integration
git diff | claude "review these changes before I commit"
```

---

## Common Workflows

### Incident Response

```bash
# 1. Gather information
claude "read logs/error.log and identify the root cause"

# 2. Analyze impact
claude "check all services that depend on user-api"

# 3. Generate fix
claude "create a hotfix for the connection pool exhaustion issue"

# 4. Deployment
claude "generate rollback procedure if this fix fails"
```

### Feature Development

```bash
# 1. Planning
claude "design the API for user profile updates, considering:
- Input validation
- Database schema changes
- Backward compatibility
- Test requirements"

# 2. Implementation
claude "implement the user profile update endpoint"

# 3. Testing
claude "generate comprehensive tests for the profile update feature"

# 4. Documentation
claude "write API documentation for the new endpoint"
```

### Code Review Automation

```bash
# Create command: .claude/commands/auto-review.md
# Then:
/auto-review src/api/users.ts
```

---

## Troubleshooting

### Common Issues

```bash
# Claude Code not finding files
claude doctor                           # Check configuration
ls -la ~/.claude/                      # Verify setup

# Permission denied
chmod +x ~/.claude/commands/*.md       # Fix permissions

# MCP server not working
cat ~/.claude/mcp_servers.json         # Check configuration
claude "test MCP connection"           # Verify connectivity

# Context too large
/compact                               # Manually compact
/clear                                 # Clear and restart

# Slow performance
claude --model haiku "quick task"      # Use faster model
# Or optimize CLAUDE.md (keep it < 5000 words)
```

---

## Keyboard Shortcuts

```bash
Ctrl+C          # Stop current operation
Ctrl+D          # Exit Claude Code
Ctrl+B          # Background current operation (v2.1.0+)
Ctrl+L          # Clear screen (terminal)
Shift+Enter     # New line in prompt (iTerm2, WezTerm, Kitty)
```

---

## Best Practices

### 1. Security

```yaml
# Never auto-approve writes in production
auto_approve:
  read: true
  write: false      # Always review writes

# Use hooks for security scanning
hooks:
  post_edit:
    - command: "gitleaks detect --source={{file}}"
```

### 2. Context Management

- Keep CLAUDE.md focused (< 5000 words)
- Use `.claudeignore` to exclude large files
- Clear context between unrelated tasks
- Use specific file paths to limit scope

### 3. Performance

- Use Haiku for quick tasks
- Batch similar operations
- Background long-running operations (Ctrl+B)
- Optimize prompts (shorter = faster)

### 4. Team Collaboration

- Share `.claude/` directory in git
- Document custom commands in README
- Use consistent naming for skills
- Review hooks before merging

---

## Additional Resources

- **Official Docs**: https://docs.anthropic.com/claude-code
- **CHANGELOG**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- **MCP Spec**: https://modelcontextprotocol.io
- **This Guide**: [Full chapters](../chapters/)

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
**Copyright**: © 2026 Michel Abboud. All rights reserved.
**License**: CC BY-NC 4.0
