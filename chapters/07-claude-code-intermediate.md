# Chapter 7: Claude Code Intermediate

**Part 3: Claude Code Mastery**

---

## Navigation

← Previous: [Chapter 6: Claude Code Fundamentals](./06-claude-code-fundamentals.md) | Next: [Chapter 8: Skills and Sub-Agents](./08-skills-and-subagents.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---


## Leveling Up Your Claude Code Skills

**📖 Reading time:** ~15 minutes | **⚙️ Hands-on time:** ~40 minutes
**🎯 Quick nav:** [Configuration](#71-configuration-deep-dive) | [Custom Commands](#72-custom-slash-commands-skills) | [IDE Integration](#74-ide-integration) | [Workflows](#75-advanced-workflows) | [🏋️ Skip to Exercises](#79-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** Beyond basic usage, Claude Code becomes exponentially more powerful when you customize it for your workflow. This chapter teaches configuration, creating reusable commands, integrating with your IDE/browser, and building automated review pipelines.

**Key concepts:**
- **Custom commands/skills** = Reusable prompt templates for common tasks (unified system as of v2.1.3)
- **Configuration** = Fine-tune behavior, permissions, auto-approve patterns, model selection
- **IDE integration** = Use Claude Code inside VS Code, Cursor, IntelliJ with full context
- **Browser mode** = claude.ai for lightweight access (no local commands, but great for quick questions)
- **Automated workflows** = PR reviews, incident response, deployment checks

**Most important takeaway:** The difference between "using Claude Code" and "mastering Claude Code" is customization. Create commands for your team's workflows, configure permissions for safety, and integrate into your existing tools.

**Hands-on:** [Jump to exercises](#79-hands-on-exercises) to create custom DevOps commands, integrate with your IDE, and build an automated review pipeline.

---

*💡 Need configuration details? Keep reading. Ready to customize? Jump to exercises!*

---

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

  // Language preference (new in 2.1)
  "language": "english",     // Or: "japanese", "spanish", etc.

  // Release channel (toggle in /config)
  "release_channel": "stable",  // Or: "latest" for newest features

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

### Configuration Decision Framework

Understanding which configuration to use and when is critical for both productivity and security. Here's how to make informed configuration decisions.

#### When to Use Each Configuration Level

**Project-level configuration** (.claude/config.json):
- Settings that are specific to this project's needs
- Team-shared standards (commit all team members)
- Project-specific model requirements (e.g., Haiku for a simple project)
- Custom exclude patterns for project structure
- When onboarding should automatically apply settings

Example: A Python Django project might specify `"model": "claude-haiku-4-5-20250514"` for cost savings, while a complex distributed system might use Sonnet for better reasoning.

**User-level configuration** (~/.claude/config.json):
- Personal preferences that apply across projects
- Your API authentication
- Your preferred output format and verbosity
- Your default auto-approve settings for personal safety level
- Settings you don't want to share with the team

Example: You prefer `"show_tokens": true` to monitor costs, but your teammate doesn't care about tokens.

**Environment variables** (temporary overrides):
- Testing different models without changing config files
- CI/CD pipelines with different authentication
- Temporary debugging settings
- Demo/presentation modes (IS_DEMO=true)

Example: `CLAUDE_CODE_MODEL=claude-opus-4-5 claude` to temporarily use Opus for a complex task without changing your config.

#### Security Implications of Configuration

**Auto-approval settings** - Critical security consideration:

```yaml
Low Risk (Development Environment):
  auto_approve:
    read: true      # Safe - reading files is non-destructive
    write: false    # Controlled - you review each file change
    execute: false  # Controlled - you approve each command

Medium Risk (Personal Projects):
  auto_approve:
    read: true
    write: true     # Faster but risky - Claude can modify any file
    execute: false  # You still control command execution

High Risk (Production/Shared Systems):
  auto_approve:
    read: false     # You review even file reads (audit trail)
    write: false    # Every change requires approval
    execute: false  # Every command requires approval
```

**Real-world security example**: A developer with `write: true` auto-approve asked Claude to "clean up the config files." Claude interpreted this as deleting unused configs, including a critical `.env.production` file. The file was recovered from git, but it demonstrates why write approval matters.

**Blocked commands** for safety:
```json
{
  "safety": {
    "blocked_commands": [
      "rm -rf /",           // Catastrophic system damage
      "mkfs",               // Filesystem formatting
      "> /dev/sda",         // Direct disk writes
      "dd if=/dev/zero",    // Disk wiping
      "chmod -R 777",       // Security hole
      "git push --force origin main"  // Dangerous for shared repos
    ]
  }
}
```

#### Cost and Performance Impact of Settings

**Model selection** has the biggest cost impact:

```
Scenario: Reviewing 50 files/day (average 500 lines each)

Claude Opus 4.5:
  Input:  (50 × 500 × 4 chars/token ÷ 1M) × $15  = ~$1.50/day
  Output: (50 × 100 tokens ÷ 1M) × $75            = ~$0.38/day
  Total: ~$1.88/day (~$40/month) ✓ High quality but expensive

Claude Sonnet 4.5:
  Input:  (50 × 500 × 4 chars/token ÷ 1M) × $3   = ~$0.30/day
  Output: (50 × 100 tokens ÷ 1M) × $15            = ~$0.075/day
  Total: ~$0.38/day (~$8/month) ✓ Best balance

Claude Haiku 4.5:
  Input:  (50 × 500 × 4 chars/token ÷ 1M) × $1   = ~$0.10/day
  Output: (50 × 100 tokens ÷ 1M) × $5             = ~$0.025/day
  Total: ~$0.13/day (~$3/month) ✓ Cheapest
```

**Decision**: For code review, Sonnet provides 90% of Opus quality at 20% of the cost. Reserve Opus for architecture decisions and complex debugging.

**Context settings** affect both cost and performance:

```yaml
max_files: 10 (Small Context):
  pros: Fast responses, lower token costs, focused answers
  cons: May miss relevant code, requires manual file mentions
  best_for: Small projects, specific tasks, tight budgets

max_files: 50 (Medium Context):
  pros: Balanced performance, good project understanding
  cons: Moderate cost, occasional irrelevant files included
  best_for: Most projects, general development work

max_files: 200 (Large Context):
  pros: Comprehensive understanding, finds related code
  cons: Slow responses, high token costs, can overwhelm context
  best_for: Large refactoring, architectural analysis, debugging
```

**Exclude patterns** significantly impact performance:

```json
Without excludes:
  - Claude reads node_modules (50MB, 10,000 files)
  - 5-10 second delay before each response
  - Wastes tokens on dependencies

With proper excludes:
  - Claude reads only source (5MB, 200 files)
  - <1 second indexing
  - Focuses tokens on your code
```

**Recommended baseline** for most DevOps projects:
```json
{
  "model": "claude-sonnet-4-5-20250514",
  "auto_approve": {
    "read": true,
    "write": false,
    "execute": false
  },
  "context": {
    "max_files": 50,
    "exclude_patterns": [
      "node_modules", "vendor", ".git", "dist", "build",
      "*.log", "*.lock", "coverage", ".terraform"
    ]
  },
  "safety": {
    "confirm_destructive": true
  }
}
```

This balances speed ($8-15/month for typical usage), safety (you review all changes), and effectiveness (good project understanding).

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

  // Control @-mention file picker behavior
  "respectGitignore": true,  // Respect .gitignore in file picker

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

### Important Environment Variables

```bash
# Core configuration
ANTHROPIC_API_KEY              # API authentication
CLAUDE_CODE_MODEL              # Default model override
CLAUDE_CODE_MAX_TOKENS         # Max output tokens
CLAUDE_CODE_SHELL              # Override shell detection

# File handling
CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS  # File read token limit

# UI and display
IS_DEMO=true                   # Hide email/org from UI (for streaming/recording)

# Plugin management
FORCE_AUTOUPDATE_PLUGINS=true  # Control plugin auto-updates

# Network
CLAUDE_CODE_PROXY_RESOLVES_HOSTS  # DNS resolution opt-in

# Enterprise (AWS Bedrock)
ANTHROPIC_BEDROCK_BASE_URL     # Bedrock endpoint override
```

---

## 7.2 Custom Slash Commands (Skills)

### Understanding the Unified System

As of **version 2.1.3** (January 2025), Claude Code has **fully merged slash commands and skills** into a unified system. This simplified mental model means:

- Custom commands and skills work the same way - **no conceptual difference**
- Both are loaded from `.claude/commands/` or `.claude/skills/` directories
- Both support the same frontmatter options (arguments, context forking, etc.)
- Skills in `~/.claude/skills` or `.claude/skills` are **hot-reloaded** - available immediately without restarting Claude Code
- You can configure your preferred **release channel** (`stable` or `latest`) using `/config`

> **What Changed:** Previously, slash commands and skills were separate concepts with different behaviors. Slash commands were simpler prompt templates, while skills had additional capabilities. Now they are unified - you can use either directory and both support all features including context forking and hot-reload.
>
> **Version Compatibility:** This guide covers features up to Claude Code v2.1.4 (January 2025).

### Creating Custom Commands

Custom commands let you create reusable prompts for common tasks.

### Anatomy of Effective Custom Commands

Creating truly useful custom commands requires understanding what makes them effective versus just "nice to have." Here are the principles and patterns that separate production-quality commands from simple prompt templates.

#### Principles of Good Command Design

**1. Single Responsibility Principle**

Each command should do ONE thing well. Don't create a "do-everything" command.

```yaml
Bad Command Example:
  name: devops
  purpose: "Handle all DevOps tasks"
  problem: Too vague, Claude won't know what you want

Good Command Examples:
  - name: k8s-scale
    purpose: "Scale a specific Kubernetes deployment"
  - name: log-analysis
    purpose: "Analyze application logs for errors"
  - name: terraform-cost
    purpose: "Estimate cost changes from Terraform plan"
```

**2. Context Over Instructions**

Good commands provide context and constraints, not step-by-step instructions. Let Claude reason, don't script it.

```markdown
❌ Bad: Prescriptive and rigid
---
name: review
---
First, read the file.
Then, check for errors on line 1.
Then, check line 2.
Then, check line 3.
...

✅ Good: Context-driven and flexible
---
name: review
---
You are a senior DevOps engineer reviewing infrastructure code.

Our standards:
- All Terraform must use remote state
- Security groups must never allow 0.0.0.0/0 on SSH (22)
- Resources must have Name tags with project-service-env format

Review {{file}} and flag any violations of these standards.
Also suggest improvements for maintainability and cost.
```

**3. Reusability Through Arguments**

Commands should be parameterized, not hardcoded.

```markdown
❌ Bad: Hardcoded values
---
name: check-api-prod
---
Check if the production API at https://api.example.com is healthy

✅ Good: Parameterized and reusable
---
name: check-api
arguments:
  - name: environment
    description: Environment to check (dev, staging, prod)
    required: true
  - name: service
    description: Service name
    required: false
    default: api
---
Check if the {{service}} service in {{environment}} is healthy.

For production, also verify:
- Response time < 200ms
- Error rate < 0.1%
- Certificate expiry > 30 days
```

Now you can use: `/check-api prod`, `/check-api staging`, `/check-api dev api`, etc.

**4. Output Format Specification**

Always specify the desired output format. This ensures consistency and makes results parseable.

```markdown
Bad: Vague output expectations
---
Tell me about the security issues

Good: Structured output specification
---
Output format:
## Security Review for {{file}}

### Critical Issues (Must Fix)
- [Line X] Issue description
  Fix: Specific remediation

### High Priority (Should Fix)
- [Line Y] Issue description
  Fix: Specific remediation

### Recommendations (Consider)
- General improvement suggestions

### Summary
- Total issues found: N
- Estimated fix time: X hours
```

#### Common Mistakes to Avoid

**Mistake 1: Commands That Are Just Conversation Starters**

```markdown
❌ This doesn't need to be a command:
---
name: help
---
Can you help me with my code?

Just ask Claude directly in conversation!
```

**When NOT to create a command:**
- One-time questions
- Exploratory conversations
- When the context is obvious from your message
- When you need back-and-forth clarification

**When TO create a command:**
- You ask the same type of question 3+ times per week
- Your team needs consistent outputs
- The context is complex and takes >5 minutes to explain
- You want standardized formatting

**Mistake 2: Over-Constraining Claude**

```markdown
❌ Too rigid - doesn't let Claude think:
---
name: terraform-review
---
Read main.tf.
Count the resources.
If >10, say "too many".
If <=10, say "OK".

✅ Better - lets Claude analyze:
---
name: terraform-review
---
Review the Terraform configuration.

Check for:
- Resource count (>10 may indicate need for modules)
- Security misconfigurations
- Cost optimization opportunities
- Best practice violations

Provide analysis with specific recommendations.
```

**Mistake 3: No Error Handling Guidance**

```markdown
❌ Doesn't handle edge cases:
---
name: deploy-check
---
Run the tests and report if they pass.

✅ Better - handles various scenarios:
---
name: deploy-check
---
Pre-deployment verification:

1. Run the test suite
   - If tests fail, identify which tests and why
   - If tests don't exist, warn and suggest creating them
   - If test command not found, show available scripts

2. Check for uncommitted changes
   - If found, list them and ask if they should be committed

3. Verify environment variables are documented
   - Compare .env.example with code usage
   - Flag any undocumented required variables

4. Check for TODO or FIXME comments added in this branch
   - List them for review before deployment

Provide a deployment readiness report with go/no-go recommendation.
```

**Mistake 4: Not Providing Examples**

Commands with examples in their prompts are more reliable:

```markdown
✅ Command with examples:
---
name: commit-message
---
Generate a conventional commit message for the staged changes.

Format: <type>(<scope>): <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation only
- refactor: Code change that neither fixes a bug nor adds a feature
- perf: Performance improvement
- test: Adding tests

Examples:
- feat(auth): add JWT token refresh endpoint
- fix(api): prevent null pointer in user lookup
- docs(readme): update installation instructions
- refactor(db): simplify query builder interface

Review staged changes and suggest an appropriate commit message.
```

#### Reusability Patterns

**Pattern 1: Nested Commands for Related Tasks**

```bash
.claude/commands/
├── k8s/
│   ├── debug-pod.md      # /k8s/debug-pod
│   ├── scale.md          # /k8s/scale
│   ├── rollback.md       # /k8s/rollback
│   └── cost-report.md    # /k8s/cost-report
└── terraform/
    ├── security.md       # /terraform/security
    ├── cost.md           # /terraform/cost
    └── compliance.md     # /terraform/compliance
```

**Pattern 2: Composable Commands**

Create small, focused commands that can be chained:

```bash
# Instead of one giant "deploy" command, create:
/pre-deploy-check   # Verifies tests, config, etc.
/deploy staging     # Deploys to staging
/verify staging     # Runs smoke tests
/deploy prod        # Promotes to production
```

**Pattern 3: Team Standards Command**

Create a command that encodes your team's conventions:

```markdown
// .claude/commands/team-standards.md
---
name: team-standards
context: fork  # Runs in separate context to avoid pollution
---
When writing code for this project, always follow these standards:

**Python**
- Use type hints on all functions
- Maximum line length: 100 characters
- Use Black formatter
- pytest for tests with >80% coverage

**Infrastructure**
- Terraform 1.5+ required
- All resources must have tags: Environment, Project, Owner, CostCenter
- Use AWS Secrets Manager, never environment variables for secrets
- Document all security group rules

**Git**
- Branch naming: feature/TICKET-description, fix/TICKET-description
- Conventional commits: type(scope): description
- Squash commits before merging to main

Apply these standards when reviewing or generating code.
```

Now every team member gets consistent guidance by running `/team-standards` before asking Claude to write code.

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
│  │  • Chat interface in sidebar or secondary sidebar        │  │
│  │    (VS Code 1.97+)                                       │  │
│  │  • Workspace-aware context                               │  │
│  │  • File references with @file                            │  │
│  │  • Direct code insertion                                 │  │
│  │  • Streaming message support                             │  │
│  │  • Copy-to-clipboard on code blocks                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Tab Icon Badges:                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Blue badge: Pending permission requests               │  │
│  │  • Orange badge: Unread task completions                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Permission Requests:                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Clickable destination selector for permissions:       │  │
│  │    - Save to project                                     │  │
│  │    - Save to all projects                                │  │
│  │    - Share with team                                     │  │
│  │    - Session only                                        │  │
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
│  Platform Support:                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Windows ARM64 supported via x64 emulation             │  │
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

### Claude Code Built-in Vim Mode

Claude Code's input field has enhanced Vim-like editing support (as of 2.1):

```
Vim Motions and Commands:
• ; and , for repeat f/F/t/T motions
• y operator with yy/Y for yank
• p/P for paste
• >> and << for indent/dedent
• J for join lines

Text Objects:
• iw, aw (inner/around word)
• iW, aW (inner/around WORD)
• i", a", i', a' (quoted strings)
• i(, a(, i[, a[, i{, a{ (brackets)
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

### Named Sessions (New in 2.0.64)

Named sessions make it easier to organize and resume your work:

```bash
# Name your current session
claude
> /rename my-feature-work

# Later, resume by name (instead of searching through session IDs)
> /resume my-feature-work

# This replaces the older /save and /load workflow
# Sessions are now automatically saved, you just need to name them
```

> **What Changed:** Previously, you had to manually save sessions with `/save` and remember session filenames. Now sessions are automatically persisted, and `/rename` lets you give them memorable names that you can use with `/resume`.

### Legacy Save/Load (Still Supported)

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
│  Custom Commands (Skills):                                     │
│  .claude/commands/*.md     - Custom commands (hot-reloaded)    │
│  .claude/skills/*.md       - Same as commands (unified)        │
│  /commands                 - List available commands           │
│  /command-name             - Run a command                     │
│                                                                │
│  Session Management:                                           │
│  /rename <name>            - Name session for easy resume      │
│  /resume <name>            - Resume named session              │
│  /save <name>              - Save session (legacy)             │
│  /load <name>              - Load session (legacy)             │
│  /sessions                 - List saved sessions               │
│  /stats                    - Usage stats, graphs, streaks      │
│                                                                │
│  New Settings:                                                 │
│  language: "japanese"      - UI language preference            │
│  release_channel: "latest" - Get newest features               │
│  respectGitignore: true    - @-mention respects .gitignore     │
│  IS_DEMO=true              - Hide email/org for streaming      │
│                                                                │
│  Debug:                                                        │
│  CLAUDE_DEBUG=1 claude     - Enable debug mode                 │
│  /debug on                 - In-session debug                  │
│  /doctor                   - Diagnose permission rules         │
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

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0

---

## Navigation

← Previous: [Chapter 6: Claude Code Fundamentals](./06-claude-code-fundamentals.md) | Next: [Chapter 8: Skills and Sub-Agents](./08-skills-and-subagents.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 7** | Claude Code Intermediate | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
