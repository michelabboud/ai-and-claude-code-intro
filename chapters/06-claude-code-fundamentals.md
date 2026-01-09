# Chapter 6: Claude Code Fundamentals

## Your AI Pair Programmer for the Terminal

Claude Code is Anthropic's command-line interface that brings Claude directly into your development workflow. Unlike web interfaces, Claude Code can read your files, execute commands, and make changes to your codebase.

---

## 6.1 What is Claude Code?

### Overview

**Claude Code** is an agentic AI coding tool that operates directly in your terminal. It can:

```
┌────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE CAPABILITIES                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  READ & UNDERSTAND                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Read files in your project                            │  │
│  │  • Understand codebase structure                         │  │
│  │  • Navigate directories                                  │  │
│  │  • Search for patterns across files                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  EXECUTE & MODIFY                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Run shell commands                                    │  │
│  │  • Edit existing files                                   │  │
│  │  • Create new files                                      │  │
│  │  • Run tests and builds                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  AUTOMATE & ASSIST                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Complete multi-step tasks autonomously                │  │
│  │  • Git operations (commit, branch, PR)                   │  │
│  │  • Debug issues with access to real data                 │  │
│  │  • Refactor code across multiple files                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### How Claude Code Differs from Claude.ai

```
┌────────────────────────────────────────────────────────────────────────────┐
│                CLAUDE.AI vs CLAUDE CODE                                    │
├────────────────────────────┬───────────────────────────────────────────────┤
│        Claude.ai           │              Claude Code                      │
├────────────────────────────┼───────────────────────────────────────────────┤
│ Web browser interface      │ Terminal/CLI interface                        │
│ Copy-paste code manually   │ Direct file system access                     │
│ You run commands yourself  │ Can execute commands for you                  │
│ Session-based only         │ Persistent project context                    │
│ Manual context management  │ Automatic codebase awareness                  │
│ Good for chat/exploration  │ Good for actual development work              │
├────────────────────────────┴───────────────────────────────────────────────┤
│                                                                            │
│  Example: "Add error handling to the database module"                      │
│                                                                            │
│  Claude.ai:                                                                │
│  1. You paste the file content                                             │
│  2. Claude suggests changes                                                │
│  3. You manually copy and apply changes                                    │
│  4. You run tests yourself                                                 │
│                                                                            │
│  Claude Code:                                                              │
│  1. Claude reads the database module directly                              │
│  2. Claude edits the file in place                                         │
│  3. Claude runs the tests                                                  │
│  4. Claude fixes any issues found                                          │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 6.2 Installation

### Prerequisites

```bash
# Required:
# - Node.js 18+ (for npm installation)
# - OR: Direct binary download available
# - Anthropic API key or Claude account

# Check Node.js version
node --version  # Should be v18.0.0 or higher

# Check npm version
npm --version
```

### Installation Methods

#### Method 1: npm (Recommended)

```bash
# Global installation
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

#### Method 2: Direct Download (No Node.js Required)

```bash
# macOS (Apple Silicon)
curl -fsSL https://claude.ai/download/claude-code/macos-arm64 -o claude
chmod +x claude
sudo mv claude /usr/local/bin/

# macOS (Intel)
curl -fsSL https://claude.ai/download/claude-code/macos-x64 -o claude
chmod +x claude
sudo mv claude /usr/local/bin/

# Linux (x64)
curl -fsSL https://claude.ai/download/claude-code/linux-x64 -o claude
chmod +x claude
sudo mv claude /usr/local/bin/
```

#### Method 3: Homebrew (macOS)

```bash
# Install via Homebrew
brew install claude-code

# Verify
claude --version
```

### Platform-Specific Notes

```yaml
# Platform Installation Notes

macos:
  native: "Full support, best experience"
  notes:
    - "Works natively on both Intel and Apple Silicon"
    - "May need to allow in Security & Privacy settings"
  terminal_recommendation: "iTerm2 or native Terminal"

linux:
  native: "Full support"
  distributions:
    - "Ubuntu 20.04+: Full support"
    - "Debian 11+: Full support"
    - "RHEL/CentOS 8+: Full support"
    - "Arch: Full support"
  notes:
    - "Requires glibc 2.31+"
    - "Some features may need additional packages"

windows_wsl:
  support: "Full support via WSL2"
  setup: |
    # Install WSL2 first
    wsl --install

    # Inside WSL, install Node.js
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs

    # Install Claude Code
    npm install -g @anthropic-ai/claude-code
  notes:
    - "Use WSL2, not WSL1"
    - "Windows Terminal recommended"
    - "VS Code WSL extension works great"

windows_native:
  support: "Limited - WSL recommended"
  notes:
    - "PowerShell support is experimental"
    - "WSL provides better experience"
```

---

## 6.3 Authentication

### Setting Up Authentication

```bash
# Method 1: Interactive login (recommended)
claude login

# This opens a browser for Anthropic account authentication
# Your API key is stored securely

# Method 2: API key environment variable
export ANTHROPIC_API_KEY="your-api-key-here"

# Add to shell profile for persistence
echo 'export ANTHROPIC_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc

# Method 3: Configuration file
# Create ~/.claude/config.json
{
  "api_key": "your-api-key-here"
}
```

### Verifying Authentication

```bash
# Check authentication status
claude auth status

# Test with a simple query
claude "What model are you?"
```

### Enterprise Authentication (AWS Bedrock)

```bash
# Use Claude Code with AWS Bedrock
export CLAUDE_CODE_PROVIDER=bedrock
export AWS_REGION=us-east-1
export AWS_PROFILE=your-profile  # Or use IAM role

# Bedrock requires appropriate IAM permissions
# See AWS documentation for setup
```

---

## 6.4 Basic Usage

### Starting Claude Code

```bash
# Interactive mode (most common)
claude

# You'll see:
# ╭─────────────────────────────────────────────────────────╮
# │ Claude Code                                             │
# │ Type your message or /help for commands                 │
# ╰─────────────────────────────────────────────────────────╯
# >

# Single command mode
claude "explain this codebase"

# With specific file
claude "review this file" --file src/main.py

# Pipe input
cat error.log | claude "what caused this error?"
```

### The Interactive Interface

```
┌────────────────────────────────────────────────────────────────┐
│                  CLAUDE CODE INTERFACE                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ╭─────────────────────────────────────────────────────────╮   │
│  │ Claude Code v1.x.x                                      │   │
│  ╰─────────────────────────────────────────────────────────╯   │
│                                                                │
│  Status indicators:                                            │
│  🟢 Connected to Claude                                        │
│  📁 Working directory: /home/user/myproject                    │
│  🔧 Tools available: file, bash, edit, etc.                    │
│                                                                │
│  > [Your input here]                                           │
│                                                                │
│  Navigation:                                                   │
│  • Type message and press Enter to send                        │
│  • Use ↑/↓ arrows for history                                  │
│  • Tab for autocompletion                                      │
│  • Ctrl+C to cancel current operation                          │
│  • Type /help for commands                                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Essential Commands

```bash
# Help and information
/help                    # Show all commands
/model                   # Show/change current model
/cost                    # Show session token usage and cost

# File operations
/file path/to/file       # Add file to context
/tree                    # Show project structure

# Session management
/clear                   # Clear conversation history
/history                 # Show conversation history
/save                    # Save session
/load                    # Load previous session

# Control
/stop                    # Stop current operation
/exit or Ctrl+D          # Exit Claude Code
```

---

## 6.5 Core Workflows

### Workflow 1: Understanding a Codebase

```bash
# Start Claude Code in a project directory
cd /path/to/project
claude

# Ask Claude to explain the codebase
> explain the structure of this project

# Claude will:
# 1. Read key files (package.json, README, main entry points)
# 2. Identify frameworks and patterns
# 3. Summarize the architecture
# 4. Highlight important components

# Follow-up questions
> where is authentication handled?
> how does the database connection work?
> what are the main API endpoints?
```

### Workflow 2: Writing New Code

```bash
# Example: Creating a new feature
> create a new endpoint POST /api/users that:
  - validates email and password
  - hashes the password with bcrypt
  - stores in the users table
  - returns user id on success

# Claude will:
# 1. Identify existing patterns in your codebase
# 2. Create the endpoint following your style
# 3. Add necessary imports
# 4. Create tests if you have a test structure

# Review what Claude proposes
> before making changes, show me the plan

# Claude shows the proposed changes

> go ahead with the changes
```

### Workflow 3: Debugging

```bash
# Paste or pipe error output
> I'm getting this error:
  TypeError: Cannot read property 'map' of undefined
  at UserList (/src/components/UserList.jsx:15)

# Claude will:
# 1. Read the relevant file
# 2. Analyze the error context
# 3. Identify the root cause
# 4. Suggest a fix

# Let Claude fix it
> fix this error

# Or ask for explanation first
> explain why this is happening and show me how to fix it
```

### Workflow 4: Refactoring

```bash
# Example: Refactoring a large function
> the function processOrder in src/orders.py is too long.
  Refactor it into smaller, testable functions.

# Claude will:
# 1. Analyze the function
# 2. Identify logical groupings
# 3. Extract helper functions
# 4. Update all call sites
# 5. Ensure tests still pass

# You can guide the refactoring
> also add type hints to the new functions
> make sure error handling is preserved
```

### Workflow 5: Git Operations

```bash
# Create a commit with Claude's help
> commit these changes with a descriptive message

# Claude will:
# 1. Run git status to see changes
# 2. Run git diff to understand changes
# 3. Compose an appropriate commit message
# 4. Execute git commit (with your approval)

# Create a branch
> create a feature branch for this user authentication work

# Prepare a PR
> create a pull request description for these changes
```

---

## 6.6 DevOps Examples

### Example 1: Creating Kubernetes Manifests

```bash
# Start Claude Code in your project
claude

> Create Kubernetes manifests for deploying this Node.js application.
  Requirements:
  - Deployment with 3 replicas
  - Service with ClusterIP
  - ConfigMap for environment variables
  - Health checks on /health endpoint
  - Resource limits appropriate for a Node.js app

# Claude reads package.json, Dockerfile, etc. and creates:
# - k8s/deployment.yaml
# - k8s/service.yaml
# - k8s/configmap.yaml

# Follow up
> add a HorizontalPodAutoscaler that scales based on CPU

# Claude adds k8s/hpa.yaml
```

### Example 2: Writing a CI/CD Pipeline

```bash
> Create a GitHub Actions workflow that:
  - Runs on push to main and PRs
  - Runs npm test
  - Builds Docker image
  - Pushes to ECR if on main branch
  - Deploys to EKS staging if on main branch

# Claude creates .github/workflows/ci-cd.yaml

# Iterate
> add a step for security scanning with trivy
> add Slack notification on failure
```

### Example 3: Infrastructure as Code

```bash
> Review the Terraform files in the infrastructure/ directory
  and identify any security issues or improvements

# Claude reads all .tf files and provides analysis

> Add a WAF rule to the ALB module that blocks SQL injection

# Claude modifies the relevant Terraform files

> Now generate documentation for these Terraform modules
# Claude creates README.md files with inputs/outputs docs
```

### Example 4: Log Analysis

```bash
# Pipe logs directly to Claude
kubectl logs deployment/api-server --tail=500 | claude "analyze these logs and identify any issues"

# Or reference a log file
> analyze the errors in /var/log/app/error.log
  and suggest fixes for the top 3 most common issues
```

### Example 5: Script Automation

```bash
> Create a bash script that:
  - Backs up all PostgreSQL databases
  - Compresses with gzip
  - Uploads to S3 with server-side encryption
  - Deletes local copies older than 24 hours
  - Sends notification to Slack on completion
  - Handles errors gracefully with proper exit codes

# Claude creates scripts/backup-databases.sh

> make it executable and add it to cron for 2am daily
```

---

## 6.7 Understanding Claude Code's Actions

### Tools Claude Code Uses

```yaml
# Claude Code has access to various tools

file_operations:
  read_file:
    purpose: "Read contents of files"
    example: "Reading src/main.py..."
  write_file:
    purpose: "Create or overwrite files"
    example: "Creating k8s/deployment.yaml..."
  edit_file:
    purpose: "Modify specific parts of files"
    example: "Editing src/config.js lines 15-20..."
  list_directory:
    purpose: "See directory contents"
    example: "Listing contents of src/..."

shell_operations:
  execute_command:
    purpose: "Run shell commands"
    example: "Running: npm test"
    security: "You approve before execution"

search_operations:
  grep:
    purpose: "Search for patterns in files"
    example: "Searching for 'TODO' across codebase..."
  glob:
    purpose: "Find files matching patterns"
    example: "Finding all *.py files..."
```

### Approval Flow

```
┌────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE APPROVAL FLOW                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Claude proposes an action:                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ I'll run this command:                                   │  │
│  │ $ npm install express                                    │  │
│  │                                                          │  │
│  │ [y]es / [n]o / [e]xplain                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Your options:                                                 │
│  • y (yes) - Execute the command                               │
│  • n (no) - Skip this command                                  │
│  • e (explain) - Ask Claude to explain why                     │
│                                                                │
│  For file edits:                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ I'll make these changes to src/app.js:                   │  │
│  │                                                          │  │
│  │ - const port = 3000;                                     │  │
│  │ + const port = process.env.PORT || 3000;                 │  │
│  │                                                          │  │
│  │ [y]es / [n]o / [e]xplain / [d]iff                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Security tip:                                                 │
│  • Always review commands before approving                     │
│  • Be cautious with destructive operations                     │
│  • Use /stop if Claude is doing something unexpected           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Auto-Approve Mode (Use Carefully!)

```bash
# For trusted, repetitive operations
claude --auto-approve "format all Python files with black"

# This skips confirmation for each action
# Only use in controlled environments!

# Better alternative: approve categories
claude
> /settings
> auto_approve_read: true    # Auto-approve file reads
> auto_approve_write: false  # Still confirm writes
```

---

## 6.8 Tips for DevOps Workflows

### Tip 1: Project Context Matters

```bash
# Claude Code works best when started in your project root
cd /path/to/your/project
claude

# It will read:
# - .git/ for project history
# - package.json, pyproject.toml, etc. for dependencies
# - README files for context
# - Existing code patterns
```

### Tip 2: Be Specific About Standards

```bash
# Good: Specific requirements
> Create a Python script following our patterns:
  - Use the existing logger from src/utils/logger.py
  - Follow our error handling pattern from src/utils/errors.py
  - Add type hints (we use Python 3.10+)
  - Write tests in tests/ using pytest

# Less effective: Vague request
> Create a Python script
```

### Tip 3: Use File References

```bash
# Reference specific files for context
> Using the pattern from src/services/user_service.py,
  create a new order_service.py with similar structure

> The error is in src/handlers/webhook.py, the logs show
  [paste error]. What's wrong?
```

### Tip 4: Iterate on Complex Tasks

```bash
# Break down large tasks
> First, show me the current structure of our Terraform modules

> Now suggest how to refactor for better module reusability

> Implement the changes to the VPC module first

> Now update the EKS module to use the refactored VPC
```

### Tip 5: Save Useful Sessions

```bash
# Save sessions for future reference
/save infra-refactor-session

# Load when you need to continue
/load infra-refactor-session
```

---

## 6.9 Common Use Cases for DevOps

### Use Case Matrix

```yaml
daily_tasks:
  - task: "Review and fix CI pipeline failures"
    prompt: "The CI is failing, check .github/workflows/ and fix the issue"

  - task: "Update dependencies"
    prompt: "Update all npm dependencies and fix any breaking changes"

  - task: "Add monitoring"
    prompt: "Add Prometheus metrics to our Express endpoints"

infrastructure:
  - task: "IaC generation"
    prompt: "Create Terraform for a new S3 bucket with encryption and versioning"

  - task: "K8s manifests"
    prompt: "Generate Kubernetes manifests for the services in docker-compose.yaml"

  - task: "Security hardening"
    prompt: "Review our Dockerfile and K8s manifests for security issues"

troubleshooting:
  - task: "Analyze logs"
    prompt: "Here are the last 100 error logs, identify patterns"

  - task: "Debug performance"
    prompt: "Our API is slow, analyze the code and suggest optimizations"

  - task: "Fix deployment"
    prompt: "Pods are CrashLoopBackOff, here's kubectl describe output"

documentation:
  - task: "Generate runbooks"
    prompt: "Create a runbook for deploying to production"

  - task: "API docs"
    prompt: "Generate OpenAPI spec from our Express routes"

  - task: "Architecture docs"
    prompt: "Document the system architecture based on the codebase"
```

---

## 6.10 Hands-On Exercises

### Exercise 1: First Steps with Claude Code

```bash
# Exercise: Get familiar with Claude Code

# 1. Install Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Authenticate
claude login

# 3. Create a test project
mkdir claude-test && cd claude-test
npm init -y
touch index.js

# 4. Start Claude Code
claude

# 5. Try these commands:
> explain what files are in this directory
> create a simple Express server in index.js
> add a /health endpoint
> create a Dockerfile for this application
> what's the project structure now?

# 6. Document your experience:
# - What worked well?
# - Any surprises?
# - How does it compare to Claude.ai?
```

### Exercise 2: DevOps Automation

```bash
# Exercise: Create a deployment pipeline

# Setup
mkdir deployment-exercise && cd deployment-exercise
git init
claude

# Tasks (try each one):

# Task 1: Create project structure
> Create a simple Python Flask API with:
  - GET /health endpoint
  - GET /api/items endpoint (mock data)
  - tests using pytest

# Task 2: Add containerization
> Add a Dockerfile following best practices
> Add docker-compose.yaml for local development

# Task 3: Add CI/CD
> Create a GitHub Actions workflow that:
  - Runs tests on PR
  - Builds Docker image on merge to main
  - Add code quality checks

# Task 4: Add Kubernetes deployment
> Create Kubernetes manifests in k8s/ directory:
  - Deployment
  - Service
  - ConfigMap
  - HorizontalPodAutoscaler
```

### Exercise 3: Codebase Analysis

```bash
# Exercise: Analyze an existing project

# Clone a sample project
git clone https://github.com/gothinkster/node-express-realworld-example-app
cd node-express-realworld-example-app

# Start Claude Code
claude

# Try these analysis prompts:
> Explain the architecture of this application
> What frameworks and patterns are used?
> Identify potential security issues
> What improvements would you suggest?
> How would you add rate limiting to this API?
```

---

## 6.11 Chapter Summary

### Key Takeaways

1. **Claude Code is an AI agent** - It can read, write, and execute in your development environment

2. **It works in your terminal** - Full integration with your existing workflow

3. **Approval flow keeps you in control** - You decide what gets executed

4. **Project context matters** - Start in your project root for best results

5. **Perfect for DevOps** - IaC, CI/CD, K8s manifests, troubleshooting

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│              CLAUDE CODE QUICK REFERENCE                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Installation:                                                 │
│  $ npm install -g @anthropic-ai/claude-code                    │
│                                                                │
│  Start:                                                        │
│  $ cd /your/project                                            │
│  $ claude                                                      │
│                                                                │
│  Essential Commands:                                           │
│  /help    - Show all commands                                  │
│  /clear   - Clear conversation                                 │
│  /cost    - Show token usage                                   │
│  /stop    - Stop current operation                             │
│  /exit    - Exit Claude Code                                   │
│                                                                │
│  Approval:                                                     │
│  y - Yes, execute                                              │
│  n - No, skip                                                  │
│  e - Explain why                                               │
│                                                                │
│  Best Practices:                                               │
│  • Start in project root                                       │
│  • Be specific about requirements                              │
│  • Review before approving                                     │
│  • Break complex tasks into steps                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: Introduction to Claude](./05-introduction-to-claude.md) | [Next: Claude Code Intermediate →](./07-claude-code-intermediate.md)
