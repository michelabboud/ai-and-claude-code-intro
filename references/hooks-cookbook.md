# Claude Code Hooks Cookbook

**Quick Reference for Hook Patterns**

This reference guide provides ready-to-use hook configurations for common DevOps scenarios. Copy and adapt these patterns for your `.claude/hooks.yaml` configuration.

---

## Table of Contents

- [File Operations](#file-operations)
- [Security & Safety](#security--safety)
- [Infrastructure Validation](#infrastructure-validation)
- [Code Quality](#code-quality)
- [Session Management](#session-management)
- [DevOps Workflows](#devops-workflows)

---

## File Operations

### Automatic Backup Before Edit

```yaml
hooks:
  pre_edit:
    - command: "cp {{file}} {{file}}.backup"
      description: "Create backup before editing"
```

### Auto-Format on Save

```yaml
hooks:
  post_edit:
    # JavaScript/TypeScript
    - command: "prettier --write {{file}}"
      condition: "{{file}} matches *.js or *.ts or *.jsx or *.tsx"
      description: "Format JavaScript/TypeScript files"

    # Python
    - command: "black {{file}}"
      condition: "{{file}} matches *.py"
      description: "Format Python files"

    # Go
    - command: "gofmt -w {{file}}"
      condition: "{{file}} matches *.go"
      description: "Format Go files"
```

---

## Security & Safety

### Scan for Secrets

```yaml
hooks:
  post_edit:
    - command: "gitleaks detect --source={{file}} --no-git"
      description: "Scan for secrets in modified files"

  pre_command:
    - command: |
        if echo "{{command}}" | grep -q "\.env\|credentials\|secrets"; then
          echo "⚠️  WARNING: Command may expose secrets!"
          read -p "Continue? (yes/no): " confirm
          [ "$confirm" = "yes" ] || exit 1
        fi
      description: "Warn on potential secret exposure"
```

### Destructive Command Protection

```yaml
hooks:
  pre_command:
    # Terraform destroy protection
    - command: |
        if echo "{{command}}" | grep -q "terraform destroy"; then
          echo "🚨 DESTRUCTIVE: terraform destroy detected!"
          read -p "Type 'destroy' to confirm: " confirm
          [ "$confirm" = "destroy" ] || exit 1
        fi
      description: "Confirm destructive terraform commands"

    # Force push protection
    - command: |
        if echo "{{command}}" | grep -q "git push.*--force"; then
          echo "⚠️  Force push detected!"
          read -p "Are you sure? (yes/no): " confirm
          [ "$confirm" = "yes" ] || exit 1
        fi
      description: "Confirm force pushes"

    # Production deletion protection
    - command: |
        if echo "{{command}}" | grep -qE "kubectl.*delete.*prod|aws.*delete.*production"; then
          echo "🚨 PRODUCTION DELETION DETECTED!"
          exit 1
        fi
      description: "Block production deletions"
```

---

## Infrastructure Validation

### Kubernetes Manifest Validation

```yaml
hooks:
  post_edit:
    - command: "kubeval {{file}}"
      condition: "{{file}} matches k8s/*.yaml or **/kubernetes/*.yaml"
      description: "Validate Kubernetes manifests"

    - command: "kubectl apply --dry-run=client -f {{file}}"
      condition: "{{file}} matches k8s/*.yaml"
      description: "Dry-run K8s manifest"
```

### Terraform Validation

```yaml
hooks:
  post_edit:
    - command: "terraform fmt {{file}}"
      condition: "{{file}} matches *.tf"
      description: "Format Terraform files"

    - command: "terraform validate"
      condition: "{{file}} matches *.tf"
      description: "Validate Terraform configuration"

    - command: "tflint {{file}}"
      condition: "{{file}} matches *.tf"
      description: "Lint Terraform files"
```

### Docker Linting

```yaml
hooks:
  post_edit:
    - command: "hadolint {{file}}"
      condition: "{{file}} matches *Dockerfile*"
      description: "Lint Dockerfiles"
```

### Ansible Linting

```yaml
hooks:
  post_edit:
    - command: "ansible-lint {{file}}"
      condition: "{{file}} matches *.yml and {{file}} contains 'playbook'"
      description: "Lint Ansible playbooks"
```

---

## Code Quality

### Linting

```yaml
hooks:
  post_edit:
    # Python linting
    - command: "pylint {{file}}"
      condition: "{{file}} matches *.py"
      description: "Lint Python files"

    # JavaScript linting
    - command: "eslint --fix {{file}}"
      condition: "{{file}} matches *.js or *.jsx"
      description: "Lint and fix JavaScript files"

    # Go linting
    - command: "golangci-lint run {{file}}"
      condition: "{{file}} matches *.go"
      description: "Lint Go files"
```

### Testing

```yaml
hooks:
  post_edit:
    # Run tests for modified files
    - command: "pytest {{file}}"
      condition: "{{file}} matches *_test.py or test_*.py"
      description: "Run Python tests"

  post_test:
    - command: "coverage report --fail-under=80"
      description: "Check coverage threshold"
```

---

## Session Management

### Session Start

```yaml
hooks:
  session_start:
    - command: "git status"
      description: "Show git status on start"

    - command: |
        echo "🚀 Claude Code session started"
        echo "Branch: $(git branch --show-current)"
        echo "Last commit: $(git log -1 --oneline)"
      description: "Show session info"
```

### Session End

```yaml
hooks:
  session_end:
    - command: "git diff --stat"
      description: "Show changes made in session"

    - command: |
        echo "📊 Session Summary:"
        echo "Files changed: $(git diff --name-only | wc -l)"
        echo "Lines added: $(git diff --numstat | awk '{s+=$1} END {print s}')"
        echo "Lines removed: $(git diff --numstat | awk '{s+=$2} END {print s}')"
      description: "Session statistics"
```

---

## DevOps Workflows

### CI/CD Validation

```yaml
hooks:
  post_edit:
    # GitHub Actions validation
    - command: "actionlint {{file}}"
      condition: "{{file}} matches .github/workflows/*.yml"
      description: "Validate GitHub Actions workflows"

    # GitLab CI validation
    - command: "gitlab-ci-lint {{file}}"
      condition: "{{file}} matches .gitlab-ci.yml"
      description: "Validate GitLab CI configuration"
```

### Command Logging

```yaml
hooks:
  pre_command:
    - command: |
        echo "$(date '+%Y-%m-%d %H:%M:%S') - {{command}}" >> ~/.claude/command.log
      description: "Log all commands"
```

### Deployment Safety

```yaml
hooks:
  pre_command:
    - command: |
        if echo "{{command}}" | grep -qE "kubectl apply|helm install|terraform apply"; then
          echo "🚀 Deployment command detected"
          echo "Command: {{command}}"
          read -p "Proceed with deployment? (yes/no): " confirm
          [ "$confirm" = "yes" ] || exit 1
        fi
      description: "Confirm deployment commands"
```

---

## Advanced Patterns

### Conditional Hooks Based on Environment

```yaml
hooks:
  pre_command:
    - command: |
        if [ "$ENVIRONMENT" = "production" ]; then
          echo "🔴 PRODUCTION ENVIRONMENT"
          echo "Extra caution required!"
          sleep 2
        fi
      description: "Production environment warning"
```

### Multi-Step Post-Edit Hook

```yaml
hooks:
  post_edit:
    - command: |
        set -e
        echo "1️⃣  Formatting..."
        black {{file}}
        echo "2️⃣  Linting..."
        pylint {{file}}
        echo "3️⃣  Type checking..."
        mypy {{file}}
        echo "✅ All checks passed!"
      condition: "{{file}} matches *.py"
      description: "Complete Python validation pipeline"
```

### Notification on Long-Running Commands

```yaml
hooks:
  post_command:
    - command: |
        if [ $COMMAND_DURATION -gt 300 ]; then
          echo "⏰ Command took ${COMMAND_DURATION}s"
          # Optional: Send notification (osascript on macOS, notify-send on Linux)
        fi
      description: "Notify on slow commands"
```

---

## Best Practices

### Hook Design Guidelines

1. **Keep hooks fast** - Hooks block execution; aim for <2 seconds
2. **Fail gracefully** - Use `|| true` for non-critical hooks
3. **Use conditions** - Only run hooks when relevant (file patterns, command patterns)
4. **Log important actions** - Help debug issues later
5. **Test hooks independently** - Run commands manually before adding as hooks
6. **Document your hooks** - Use clear descriptions

### Performance Optimization

```yaml
# ❌ Bad: Runs for every file
post_edit:
  - command: "npm test"  # Slow, runs full test suite

# ✅ Good: Only runs for test files
post_edit:
  - command: "npm test -- {{file}}"
    condition: "{{file}} matches *.test.js"
```

### Error Handling

```yaml
# Allow hook to fail without blocking
post_edit:
  - command: "prettier --write {{file}} || true"
    description: "Format if prettier is available"

# Require hook to succeed
post_edit:
  - command: "terraform validate"
    condition: "{{file}} matches *.tf"
    description: "Must pass validation"
```

---

## Full Example Configuration

```yaml
# .claude/hooks.yaml - Complete DevOps configuration

hooks:
  # Session lifecycle
  session_start:
    - command: "git status"
      description: "Show git status"

  session_end:
    - command: "git diff --stat"
      description: "Show session changes"

  # File operations
  pre_edit:
    - command: "cp {{file}} {{file}}.backup"
      description: "Backup before edit"

  post_edit:
    # Security
    - command: "gitleaks detect --source={{file}} --no-git"
      description: "Scan for secrets"

    # Infrastructure
    - command: "terraform fmt {{file}}"
      condition: "{{file}} matches *.tf"
      description: "Format Terraform"

    - command: "kubeval {{file}}"
      condition: "{{file}} matches k8s/*.yaml"
      description: "Validate K8s manifests"

    # Code quality
    - command: "black {{file}}"
      condition: "{{file}} matches *.py"
      description: "Format Python"

    - command: "prettier --write {{file}}"
      condition: "{{file}} matches *.js or *.ts"
      description: "Format JavaScript/TypeScript"

  # Command safety
  pre_command:
    # Log all commands
    - command: "echo '$(date) - {{command}}' >> ~/.claude/audit.log"
      description: "Audit log"

    # Destructive command protection
    - command: |
        if echo "{{command}}" | grep -qE "destroy|delete.*prod|rm -rf /"; then
          echo "🚨 DESTRUCTIVE COMMAND!"
          read -p "Type 'confirm' to proceed: " response
          [ "$response" = "confirm" ] || exit 1
        fi
      description: "Protect against destructive commands"
```

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
**Copyright**: © 2026 Michel Abboud. All rights reserved.
**License**: CC BY-NC 4.0
