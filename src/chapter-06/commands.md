# Chapter 6: Claude Code Commands Reference

## Basic Commands

### Starting Claude Code

```bash
# Start in current directory
claude

# Start with a specific prompt
claude "Review this codebase for security issues"

# Start in non-interactive mode
claude --non-interactive "Generate a README for this project"

# Start with a specific model
claude --model claude-opus-4-20250514

# Resume a previous session
claude --resume

# Print mode (single response, no interaction)
claude -p "Explain what this project does"
```

### Essential Slash Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show available commands | `/help` |
| `/clear` | Clear conversation history | `/clear` |
| `/model` | Switch AI model | `/model opus` |
| `/quit` | Exit Claude Code | `/quit` or `Ctrl+C` |
| `/compact` | Toggle compact mode | `/compact` |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Autocomplete file paths |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit Claude Code |
| `↑/↓` | Navigate command history |
| `Shift+Enter` | Multi-line input |

## Tool Categories

### File Operations

```bash
# These are internal tools Claude uses

Read:     # Read file contents
Write:    # Create or overwrite files
Edit:     # Make precise edits to files
Glob:     # Find files matching patterns
Grep:     # Search file contents
```

### Shell Operations

```bash
Bash:     # Execute shell commands
# Claude can run:
# - npm/yarn/pnpm commands
# - git operations
# - docker commands
# - kubectl commands
# - terraform commands
```

### Search Operations

```bash
WebSearch:  # Search the web
WebFetch:   # Fetch web page content
```

## DevOps Use Cases

### Code Review

```bash
claude
> Review the changes in my current branch for security issues

> Focus on the Terraform files and check for misconfigurations

> Summarize findings in a markdown table
```

### Troubleshooting

```bash
claude
> Analyze these logs and identify the root cause:
[paste logs]

> What kubectl commands should I run to debug further?

> Generate a fix for the issue
```

### Infrastructure Generation

```bash
claude
> Create a Terraform module for an ECS Fargate service with:
  - Application Load Balancer
  - Auto-scaling based on CPU
  - CloudWatch alarms
  - Proper IAM roles
```

### CI/CD Pipeline

```bash
claude
> Create a GitHub Actions workflow that:
  - Runs tests on PR
  - Builds and pushes Docker image on merge
  - Deploys to staging automatically
  - Requires approval for production
```

## Configuration Files

### Project-level: `.claude/config.json`

```json
{
  "model": "claude-sonnet-4-20250514",
  "allowedTools": ["Read", "Write", "Bash(npm:*)"],
  "contextFiles": ["README.md", "package.json"]
}
```

### User-level: `~/.claude/config.json`

```json
{
  "theme": "dark",
  "defaultModel": "claude-sonnet-4-20250514",
  "autoApprove": ["Read", "Glob", "Grep"]
}
```

## Custom Commands

Create in `.claude/commands/`:

### `.claude/commands/review-pr.md`

```markdown
Review the current PR changes:

1. Get the diff: `git diff origin/main...HEAD`
2. Focus on:
   - Security issues
   - Performance problems
   - Missing error handling
   - Test coverage gaps

3. Format findings as:
   - Critical: Must fix
   - Major: Should fix
   - Minor: Nice to have

Provide specific file:line references.
```

Usage:
```bash
claude
> /review-pr
```

### `.claude/commands/generate-tests.md`

```markdown
Generate tests for the specified file:

1. Read the file
2. Identify untested functions
3. Generate Jest tests covering:
   - Happy path
   - Edge cases
   - Error conditions

Follow the existing test patterns in the project.
```

Usage:
```bash
claude
> /generate-tests src/services/user.ts
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | API key for Claude | Required |
| `CLAUDE_MODEL` | Default model | claude-sonnet-4-20250514 |
| `CLAUDE_CODE_CONFIG` | Config file path | `.claude/config.json` |
| `CLAUDE_MAX_TOKENS` | Max response tokens | 4096 |

## Best Practices

### 1. Start with Context

```bash
# Bad
claude "fix the bug"

# Good
claude "There's a memory leak in the user service.
Looking at src/services/user.ts, the connection isn't
being released after queries. Fix it."
```

### 2. Be Specific About Format

```bash
# Request specific output
> Generate a Kubernetes deployment with:
  - Deployment with 3 replicas
  - Service (ClusterIP)
  - ConfigMap for environment
  - Output as separate YAML files
```

### 3. Iterate

```bash
> Generate initial Terraform module
> Add multi-AZ support
> Add monitoring alarms
> Optimize costs with spot instances
```

### 4. Verify Changes

```bash
> Before applying, run terraform plan
> Show me what will change
> If it looks good, apply
```

## Troubleshooting

### Common Issues

**"Cannot read file"**
- Check file permissions
- Ensure file exists
- Verify path is correct

**"Command not allowed"**
- Check `allowedTools` in config
- May need to approve the tool

**"Context too long"**
- Use `/clear` to reset
- Be more selective with file includes
- Summarize previous context

### Getting Help

```bash
# In-tool help
claude
> /help

# Specific command help
> /help review
```
