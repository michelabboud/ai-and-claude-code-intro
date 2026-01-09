# Chapter 7: Claude Code Intermediate

## Leveling Up Your Claude Code Skills

Now that you've mastered the basics, let's explore intermediate features that will make you more productive with Claude Code. This chapter covers configuration, custom commands, browser and IDE integration, and advanced workflows.

---

## 7.1 Configuration Deep Dive

### Configuration File Locations

```bash
# Claude Code looks for configuration in these locations (in order):

1. Project-level:  ./.claude/config.json       # Per-project settings
2. User-level:     ~/.claude/config.json       # User defaults
3. System-level:   /etc/claude/config.json     # System-wide (rare)

# Environment variables override all:
ANTHROPIC_API_KEY          # API authentication
CLAUDE_CODE_MODEL          # Default model
CLAUDE_CODE_MAX_TOKENS     # Max output tokens
```

### Configuration Options

```json
// ~/.claude/config.json - Full example with all options
{
  // Authentication
  "api_key": "sk-ant-...",       // Or use env var (recommended)

  // Model settings
  "model": "claude-sonnet-4-5-20250514",
  "max_tokens": 4096,

  // Behavior settings
  "auto_approve": {
    "read": true,           // Auto-approve file reads
    "write": false,         // Require approval for writes
    "execute": false        // Require approval for commands
  },

  // Context settings
  "context": {
    "max_files": 50,        // Max files to include automatically
    "exclude_patterns": [   // Files/dirs to ignore
      "node_modules",
      ".git",
      "*.log",
      "dist",
      "build",
      ".env*"
    ]
  },

  // Output preferences
  "output": {
    "color": true,
    "verbose": false,
    "show_tokens": true
  },

  // Safety settings
  "safety": {
    "confirm_destructive": true,    // Extra confirm for rm, git push --force
    "max_file_size": "1MB",         // Don't read files larger than this
    "blocked_commands": [           // Commands Claude cannot run
      "rm -rf /",
      "mkfs",
      "> /dev/sda"
    ]
  }
}
```

### Project-Specific Configuration

```json
// .claude/config.json in your project root
{
  // Project-specific model (maybe cheaper for simple projects)
  "model": "claude-haiku-4-5-20250514",

  // Project-specific excludes
  "context": {
    "exclude_patterns": [
      "vendor",
      "*.min.js",
      "coverage"
    ],
    "include_patterns": [
      "src/**/*",
      "tests/**/*",
      "*.yaml",
      "*.tf"
    ]
  },

  // Project instructions (system prompt addition)
  "project_instructions": """
    This is a Python Django project.
    Use Django 4.2 patterns.
    Follow PEP 8 style guide.
    All code must have type hints.
  """
}
```

### Environment-Based Configuration

```bash
# Different configs for different contexts

# Development
export CLAUDE_CODE_PROFILE=dev
# Uses ~/.claude/profiles/dev.json

# Production (more restrictive)
export CLAUDE_CODE_PROFILE=prod
# Uses ~/.claude/profiles/prod.json

# Example profile structure:
# ~/.claude/profiles/
# ├── dev.json       # Full access, auto-approve reads
# ├── prod.json      # Restricted, no auto-approve
# └── demo.json      # Limited features for demos
```

---

## 7.2 Custom Slash Commands

### Creating Custom Commands

Custom commands let you create reusable prompts for common tasks.

```markdown
// .claude/commands/review.md
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
   - Check for injection vulnerabilities
   - Verify input validation
   - Check for hardcoded secrets

2. **Performance Review**
   - Identify potential bottlenecks
   - Check for N+1 queries
   - Review memory usage patterns

3. **Code Quality**
   - Check naming conventions
   - Verify error handling
   - Assess test coverage needs

4. **Best Practices**
   - Framework-specific patterns
   - Project consistency
   - Documentation needs

Output format:
- List issues by severity (Critical, High, Medium, Low)
- Include line numbers
- Provide fix suggestions
```

```bash
# Usage
claude
> /review src/api/handlers.py
```

### More Custom Command Examples

```markdown
// .claude/commands/debug.md
---
name: debug
description: Debug an error with full context
---

I'm encountering this error. Please:

1. Analyze the error message and stack trace
2. Read relevant source files
3. Identify the root cause
4. Suggest fixes with code examples
5. Explain how to prevent similar issues

Be thorough and check related files that might be involved.
```

```markdown
// .claude/commands/deploy-check.md
---
name: deploy-check
description: Pre-deployment verification
---

Before deploying, please verify:

1. **Tests**
   - Run the test suite
   - Report any failures

2. **Security**
   - Check for exposed secrets in code
   - Verify .gitignore is correct
   - Check for vulnerable dependencies

3. **Configuration**
   - Verify environment variables are documented
   - Check database migration status
   - Validate Kubernetes manifests

4. **Documentation**
   - Check if README is up to date
   - Verify API docs match implementation

Create a deployment readiness report.
```

```markdown
// .claude/commands/k8s-troubleshoot.md
---
name: k8s-troubleshoot
description: Kubernetes troubleshooting assistant
arguments:
  - name: resource
    description: Resource type (pod, deployment, service)
  - name: name
    description: Resource name
---

Troubleshoot Kubernetes {{resource}} named {{name}}:

1. Get resource status with kubectl describe
2. Check events for issues
3. If pod, check logs for errors
4. Check related resources (service, configmap, secrets)
5. Verify resource requests and limits
6. Check network policies if applicable

Provide diagnosis and remediation steps.
```

### Organizing Commands

```bash
# Project command structure
.claude/
└── commands/
    ├── review.md           # Code review
    ├── debug.md            # Debugging helper
    ├── deploy-check.md     # Pre-deployment
    ├── k8s/
    │   ├── troubleshoot.md
    │   ├── scale.md
    │   └── rollback.md
    ├── terraform/
    │   ├── plan.md
    │   ├── security-check.md
    │   └── cost-estimate.md
    └── git/
        ├── pr-create.md
        ├── commit.md
        └── branch.md

# List available commands
claude
> /commands

# Run nested command
> /k8s/troubleshoot pod api-server-xyz
```

---

## 7.3 Claude Code in the Browser

### Claude Code Web Interface

Claude Code is also available in browser at **claude.ai** with enhanced capabilities.

```
┌────────────────────────────────────────────────────────────────┐
│                CLAUDE CODE IN BROWSER                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Features:                                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Visual file explorer                                  │  │
│  │  • Syntax-highlighted code editing                       │  │
│  │  • Diff view for changes                                 │  │
│  │  • Project upload capability                             │  │
│  │  • No local installation required                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Access:                                                       │
│  1. Go to claude.ai                                            │
│  2. Start a new conversation                                   │
│  3. Upload project files or connect repository                 │
│  4. Use Claude Code features in the browser                    │
│                                                                │
│  Best for:                                                     │
│  • Quick tasks without local setup                             │
│  • Sharing sessions with team members                          │
│  • Working from machines without CLI access                    │
│  • Visual code review                                          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Browser vs CLI Comparison

```yaml
# When to use each

browser_claude_code:
  pros:
    - "No installation needed"
    - "Visual interface with syntax highlighting"
    - "Easy file upload"
    - "Shareable sessions"
    - "Works on any device"
  cons:
    - "Can't run local commands"
    - "Manual file sync needed"
    - "No direct git integration"
  best_for:
    - "Code review"
    - "Learning/exploration"
    - "Quick edits"
    - "Sharing with team"

cli_claude_code:
  pros:
    - "Direct file system access"
    - "Can execute commands"
    - "Git integration"
    - "Full automation capability"
    - "Works with local tools"
  cons:
    - "Requires installation"
    - "Terminal-only interface"
    - "Local machine needed"
  best_for:
    - "Active development"
    - "DevOps automation"
    - "CI/CD integration"
    - "Multi-file refactoring"
```

---

## 7.4 IDE Integration

### VS Code Integration

```bash
# Install the Claude Code VS Code extension
# Search for "Claude Code" in VS Code extensions

# Or install via command line
code --install-extension anthropic.claude-code
```

```yaml
# VS Code settings.json configuration
{
  "claude-code.apiKey": "${env:ANTHROPIC_API_KEY}",
  "claude-code.model": "claude-3-5-sonnet-20241022",

  # Keybindings
  "claude-code.keybindings": {
    "openChat": "Ctrl+Shift+C",
    "explainSelection": "Ctrl+Shift+E",
    "fixSelection": "Ctrl+Shift+F",
    "generateTests": "Ctrl+Shift+T"
  },

  # Inline suggestions
  "claude-code.inlineSuggestions": true,
  "claude-code.suggestOnSave": false,

  # Context settings
  "claude-code.includeWorkspaceContext": true,
  "claude-code.maxContextFiles": 10
}
```

### VS Code Features

```
┌────────────────────────────────────────────────────────────────┐
│            VS CODE CLAUDE CODE FEATURES                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Side Panel Chat:                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Chat interface in sidebar                             │  │
│  │  • Workspace-aware context                               │  │
│  │  • File references with @file                            │  │
│  │  • Direct code insertion                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Inline Features:                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Select code → Right click → "Ask Claude"              │  │
│  │  • "Explain this code"                                   │  │
│  │  • "Fix this error"                                      │  │
│  │  • "Generate tests"                                      │  │
│  │  • "Add documentation"                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Commands (Ctrl+Shift+P):                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Claude: Open Chat                                     │  │
│  │  • Claude: Explain Selection                             │  │
│  │  • Claude: Fix Selection                                 │  │
│  │  • Claude: Generate Tests                                │  │
│  │  • Claude: Review File                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### JetBrains Integration

```bash
# Install from JetBrains Marketplace
# Settings → Plugins → Marketplace → Search "Claude"

# Or install via command line for IntelliJ
# Download from marketplace and install via:
# Settings → Plugins → Install from Disk
```

### Vim/Neovim Integration

```lua
-- Neovim configuration with Claude Code
-- ~/.config/nvim/lua/plugins/claude.lua

return {
  {
    "anthropics/claude.nvim",
    config = function()
      require("claude").setup({
        api_key = vim.env.ANTHROPIC_API_KEY,
        model = "claude-sonnet-4-5-20250514",
        keymaps = {
          chat = "<leader>cc",      -- Open chat
          explain = "<leader>ce",    -- Explain selection
          fix = "<leader>cf",        -- Fix selection
          review = "<leader>cr",     -- Review file
        },
        window = {
          position = "right",
          width = 60,
        },
      })
    end,
  },
}
```

```vim
" Traditional Vim configuration
" ~/.vimrc

" Use with vim-plug
Plug 'anthropics/claude.vim'

" Configuration
let g:claude_api_key = $ANTHROPIC_API_KEY
let g:claude_model = 'claude-sonnet-4-5-20250514'

" Keybindings
nnoremap <leader>cc :ClaudeChat<CR>
vnoremap <leader>ce :ClaudeExplain<CR>
vnoremap <leader>cf :ClaudeFix<CR>
```

---

## 7.5 Advanced Workflows

### Workflow 1: Multi-File Refactoring

```bash
# Large-scale refactoring with Claude Code

claude

# Step 1: Understand current state
> Analyze the user authentication code across the codebase.
  List all files involved and how they interact.

# Step 2: Plan the refactoring
> I want to refactor authentication to use JWT instead of sessions.
  Create a detailed plan showing:
  - Files that need changes
  - Order of changes
  - Potential breaking changes
  - Required new dependencies

# Step 3: Execute incrementally
> Let's start with step 1: Create the new JWT utility module.

> Now update the login endpoint to issue JWT tokens.

> Update the middleware to validate JWT tokens.

> Update all protected routes to use new middleware.

# Step 4: Verify
> Run the auth-related tests and show me any failures.

> Fix the failing tests.

# Step 5: Cleanup
> Remove the old session-based code that's no longer used.
```

### Workflow 2: Infrastructure Migration

```bash
# Migrating from one infrastructure pattern to another

claude

# Step 1: Document current state
> Analyze all Terraform files in infrastructure/ and create
  a diagram (ASCII) of the current AWS architecture.

# Step 2: Plan migration
> We need to migrate from EC2-based deployment to EKS.
  Create a migration plan that:
  - Minimizes downtime
  - Preserves data
  - Can be rolled back

# Step 3: Create new infrastructure
> Create the EKS Terraform module following our existing patterns.
  Include: VPC integration, node groups, IAM roles.

# Step 4: Create Kubernetes manifests
> Convert our current EC2 deployment scripts to Kubernetes manifests.
  Preserve all environment variables and secrets handling.

# Step 5: Test plan
> Create a testing checklist for validating the migration.
```

### Workflow 3: Automated Code Review Pipeline

```bash
# Create a code review automation

# .claude/commands/pr-review.md
---
name: pr-review
description: Automated PR review
---

# Step 1: Get changed files
Review the files changed in this branch compared to main.

# Step 2: Security review
For each changed file, check for:
- Injection vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure
- Insecure configurations

# Step 3: Code quality
Check for:
- Breaking changes to public APIs
- Missing error handling
- Performance issues
- Test coverage

# Step 4: Generate report
Create a markdown report with:
- Summary of changes
- Security findings (Critical/High/Medium/Low)
- Code quality suggestions
- Questions for the author

Save as PR_REVIEW.md
```

```bash
# Usage in CI/CD (GitHub Actions example)
# .github/workflows/claude-review.yaml

name: Claude Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --output pr-review.md "/pr-review"

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('pr-review.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review
            });
```

### Workflow 4: Incident Response Automation

```bash
# Incident response helper

# .claude/commands/incident.md
---
name: incident
description: Incident response assistant
arguments:
  - name: service
    description: Affected service name
---

Incident Response for {{service}}:

1. **Gather Information**
   - Check recent deployments (git log --oneline -10)
   - Check pod status if Kubernetes
   - Gather relevant logs

2. **Initial Assessment**
   - What's the user impact?
   - When did it start?
   - What changed recently?

3. **Diagnostic Steps**
   - Run health checks
   - Check dependencies
   - Verify configurations

4. **Recommended Actions**
   - Immediate mitigation options
   - Root cause investigation steps
   - Communication templates

Provide findings in incident report format.
```

---

## 7.6 Session Management

### Saving and Loading Sessions

```bash
# Save current session
claude
> /save my-feature-session

# Sessions are saved to ~/.claude/sessions/

# List saved sessions
> /sessions

# Load a previous session
> /load my-feature-session

# Export session for sharing
> /export my-session output.json
```

### Session Best Practices

```yaml
# Session management strategies

long_running_projects:
  pattern: "Daily saves with context"
  example: |
    # End of day
    > /save feature-auth-day3

    # Next day
    > /load feature-auth-day3
    > Where were we? What's left to do?

team_collaboration:
  pattern: "Export and share sessions"
  example: |
    # Developer A exports investigation
    > /export security-audit audit-session.json

    # Developer B imports and continues
    claude --import audit-session.json
    > Continue the security audit

context_preservation:
  pattern: "Save at key milestones"
  example: |
    # After completing major section
    > /save terraform-module-complete

    # After tests pass
    > /save feature-tested

    # Before risky changes
    > /save before-refactor
```

---

## 7.7 Error Handling and Troubleshooting

### Common Issues and Solutions

```yaml
# Troubleshooting guide

authentication_errors:
  symptom: "API key invalid or missing"
  solutions:
    - "Check ANTHROPIC_API_KEY is set: echo $ANTHROPIC_API_KEY"
    - "Verify key is valid at console.anthropic.com"
    - "Re-run: claude login"

rate_limiting:
  symptom: "Too many requests error"
  solutions:
    - "Wait and retry (automatic backoff)"
    - "Upgrade API tier for higher limits"
    - "Use caching for repeated queries"

context_too_large:
  symptom: "Context exceeds maximum length"
  solutions:
    - "Exclude unnecessary files in config"
    - "Be more specific about which files to include"
    - "Use /clear to reset context"

command_failures:
  symptom: "Command execution failed"
  solutions:
    - "Check command exists in PATH"
    - "Verify permissions"
    - "Run command manually first to test"

slow_responses:
  symptom: "Responses take very long"
  solutions:
    - "Use Claude Haiku 4.5 for simpler tasks"
    - "Reduce context size"
    - "Check network connection"
    - "Consider using streaming"
```

### Debug Mode

```bash
# Enable debug output
CLAUDE_DEBUG=1 claude

# Or in session
> /debug on

# Shows:
# - API requests/responses
# - Tool usage details
# - Token counts
# - Timing information
```

### Recovery from Bad State

```bash
# If Claude Code seems stuck or confused

# Option 1: Clear context
> /clear

# Option 2: Reset and start fresh
> /reset

# Option 3: Exit and restart
# Ctrl+C followed by new claude session

# Option 4: Specify fresh start
claude --no-history
```

---

## 7.8 Performance Optimization

### Reducing Token Usage

```yaml
# Strategies for token efficiency

1_exclude_unnecessary_files:
  config: |
    "context": {
      "exclude_patterns": [
        "node_modules", "vendor", "dist",
        "*.log", "*.lock", "coverage"
      ]
    }

2_be_specific:
  bad: "Review the codebase"
  good: "Review src/api/auth.py for security issues"

3_use_appropriate_model:
  complex_reasoning: "claude-opus-4.5 (expensive)"
  most_tasks: "claude-sonnet-4.5 (balanced)"
  simple_tasks: "claude-haiku-4.5 (cheapest)"

4_reuse_context:
  tip: "Keep sessions alive for related tasks"
  example: |
    # Don't start new session for each question
    # Keep conversation going in same session

5_summarize_large_inputs:
  instead_of: "Here are 10,000 lines of logs"
  do_this: "Here are the 50 error lines from the logs"
```

### Speeding Up Responses

```bash
# Use streaming for immediate feedback
claude --stream

# Use Haiku for quick tasks
claude --model claude-haiku-4-5-20250514

# Pre-warm with project context
# Start Claude Code before you need it
# Let it index while you prepare your question

# Use specific file references
> Review @src/main.py  # Faster than "review the main file"
```

---

## 7.9 Hands-On Exercises

### Exercise 1: Create Custom Commands

```bash
# Create a set of DevOps custom commands

# 1. Create command directory
mkdir -p .claude/commands

# 2. Create these commands:

# .claude/commands/security-scan.md
# - Scans for common security issues
# - Checks for secrets in code
# - Reviews dependencies

# .claude/commands/perf-check.md
# - Identifies performance bottlenecks
# - Checks database queries
# - Reviews caching opportunities

# .claude/commands/deploy-prep.md
# - Pre-deployment checklist
# - Tests verification
# - Config validation

# 3. Test your commands
claude
> /commands
> /security-scan
```

### Exercise 2: IDE Integration

```markdown
# Set up Claude Code in your IDE

## Option A: VS Code
1. Install the Claude Code extension
2. Configure your API key
3. Try these features:
   - Open chat panel (Ctrl+Shift+C)
   - Select code and "Ask Claude"
   - Use "Generate tests" on a function

## Option B: Terminal + tmux
1. Create a tmux layout:
   - Left pane: Your editor
   - Right pane: Claude Code

2. Test the workflow:
   - Edit code in left pane
   - Ask questions in right pane
   - Apply suggestions

Document your setup and workflow.
```

### Exercise 3: Automated Review Pipeline

```yaml
# Build a GitHub Actions workflow that:
# 1. Runs on PR creation
# 2. Uses Claude Code to review changes
# 3. Posts review as PR comment
# 4. Fails if critical issues found

# Create: .github/workflows/claude-review.yaml

# Requirements:
# - Set up ANTHROPIC_API_KEY secret
# - Create review output parsing
# - Handle rate limiting
# - Add status checks

# Test with a sample PR
```

---

## 7.10 Chapter Summary

### Key Takeaways

1. **Configuration is powerful** - Customize Claude Code for your project and team

2. **Custom commands save time** - Create reusable prompts for common tasks

3. **Browser and IDE options** - Use the interface that fits your workflow

4. **Advanced workflows** - Multi-file refactoring, infrastructure migration, automated reviews

5. **Performance matters** - Optimize token usage and choose appropriate models

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│           INTERMEDIATE CLAUDE CODE REFERENCE                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Configuration:                                                │
│  ~/.claude/config.json     - User defaults                     │
│  .claude/config.json       - Project settings                  │
│                                                                │
│  Custom Commands:                                              │
│  .claude/commands/*.md     - Your custom commands              │
│  /commands                 - List available commands           │
│  /command-name             - Run a command                     │
│                                                                │
│  Session Management:                                           │
│  /save <name>              - Save session                      │
│  /load <name>              - Load session                      │
│  /sessions                 - List saved sessions               │
│  /export <file>            - Export session                    │
│                                                                │
│  Debug:                                                        │
│  CLAUDE_DEBUG=1 claude     - Enable debug mode                 │
│  /debug on                 - In-session debug                  │
│                                                                │
│  Optimization:                                                 │
│  --model claude-haiku-4-5-*  - Fast/cheap model                │
│  --stream                  - Stream responses                  │
│  /clear                    - Reset context                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: Claude Code Fundamentals](./06-claude-code-fundamentals.md) | [Next: Claude Code Professional →](./08-claude-code-professional.md)
