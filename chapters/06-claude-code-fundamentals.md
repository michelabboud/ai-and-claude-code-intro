# Chapter 6: Claude Code Fundamentals

**Part 3: Claude Code Mastery**

---

## Navigation

← Previous: [Chapter 5: Introduction to Claude](./05-introduction-to-claude.md) | Next: [Chapter 7: Claude Code Intermediate](./07-claude-code-intermediate.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---


## Your AI Pair Programmer for the Terminal

**📖 Reading time:** ~13 minutes | **⚙️ Hands-on time:** ~30 minutes
**🎯 Quick nav:** [What is Claude Code?](#61-what-is-claude-code) | [Installation](#62-installation) | [Basic Usage](#64-basic-usage) | [Core Workflows](#65-core-workflows) | [DevOps Examples](#66-devops-examples)

---

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

#### Method 4: Windows Package Manager (winget)

```bash
# Install via winget on Windows
winget install Anthropic.ClaudeCode

# Verify installation
claude --version

# Claude Code auto-detects winget and provides
# update instructions when new versions are available
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
  support: "Improved - winget installation available"
  notes:
    - "Install via winget: winget install Anthropic.ClaudeCode"
    - "PowerShell support improved"
    - "WSL still provides best Unix-like experience"
    - "Windows ARM64 supported via x64 emulation"
```

### Installation Method Selection: Which One Should You Use?

Choosing the right installation method depends on your environment, team needs, and update preferences. Here's how to decide.

#### Decision Matrix: Installation Methods

| Scenario | Best Method | Why | Trade-offs |
|----------|-------------|-----|------------|
| **Individual developer, Node.js already installed** | npm install | Easiest updates (`npm update -g`), integrates with existing Node.js workflow | Requires Node.js 18+ |
| **Mac user without Node.js** | Homebrew | Native package manager, automatic updates via `brew upgrade` | macOS only |
| **Windows user** | winget | Native Windows package manager, integrates with Windows updates | Windows 11 or recent Windows 10 only |
| **Team standardization** | npm install | Consistent across all platforms, can version-lock in package.json | Everyone needs Node.js |
| **Air-gapped/restricted environment** | Direct download | No package manager needed, works offline | Manual updates required |
| **Docker/containerized** | Direct download | Smallest footprint, no runtime dependencies | Must manage binaries yourself |

#### Common Installation Issues and Fixes

##### Issue 1: "command not found: claude" (After npm install)

**Symptom**:
```bash
$ npm install -g @anthropic-ai/claude-code
# Installation succeeds but...
$ claude
command not found: claude
```

**Cause**: npm global bin directory not in PATH

**Solution**:
```bash
# Find where npm installs global packages
npm config get prefix  # Example output: /usr/local

# Add to PATH (bash)
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Add to PATH (zsh)
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
claude --version
```

**Alternative**: Use npx (no PATH configuration needed)
```bash
npx @anthropic-ai/claude-code
```

##### Issue 2: npm Permission Errors (EACCES)

**Symptom**:
```bash
$ npm install -g @anthropic-ai/claude-code
npm ERR! code EACCES
npm ERR! syscall mkdir
npm ERR! path /usr/local/lib/node_modules
npm ERR! errno -13
```

**Cause**: Insufficient permissions for global npm directory

**Solutions**:

**Option 1: Fix npm permissions** (Recommended)
```bash
# Create a directory for global packages in your home
mkdir ~/.npm-global

# Configure npm to use the new directory
npm config set prefix '~/.npm-global'

# Add to PATH
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Now install (no sudo needed)
npm install -g @anthropic-ai/claude-code
```

**Option 2: Use sudo** (Not recommended - security risk)
```bash
sudo npm install -g @anthropic-ai/claude-code
# This can cause permission issues later
```

**Option 3: Use a different method** (Easiest)
```bash
# macOS: Use Homebrew instead
brew install claude-code

# Windows: Use winget instead
winget install Anthropic.ClaudeCode

# Linux: Download binary directly
curl -fsSL https://claude.ai/download/claude-code/linux-x64 -o claude
chmod +x claude && sudo mv claude /usr/local/bin/
```

##### Issue 3: Node.js Version Mismatch

**Symptom**:
```bash
$ npm install -g @anthropic-ai/claude-code
npm ERR! engine Unsupported engine
npm ERR! engine Node.js version 16.x not supported
npm ERR! Required: >=18.0.0
```

**Solution**: Upgrade Node.js
```bash
# Using nvm (Node Version Manager) - Recommended
nvm install 20
nvm use 20
nvm alias default 20

# Using Homebrew (macOS)
brew upgrade node

# Using apt (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version  # Should show v20.x.x or v18.x.x
```

##### Issue 4: Antivirus/Security Software Blocks Installation (Windows)

**Symptom**: Installation hangs or fails with cryptic errors on Windows

**Cause**: Windows Defender or enterprise antivirus blocking executable download

**Solution**:
```powershell
# Temporarily disable real-time protection (run as Administrator)
Set-MpPreference -DisableRealtimeMonitoring $true

# Install
winget install Anthropic.ClaudeCode

# Re-enable protection
Set-MpPreference -DisableRealtimeMonitoring $false

# OR: Add exception for npm cache directory
# Windows Defender > Virus & threat protection > Manage settings > Exclusions
# Add: C:\Users\YourName\AppData\Local\npm-cache
```

##### Issue 5: Firewall Blocks Download

**Symptom**: Installation times out or fails with network errors

**Common in**: Corporate environments with restrictive firewalls

**Solution**:
```bash
# Check if you can reach npm registry
curl https://registry.npmjs.org/@anthropic-ai/claude-code

# If blocked, configure npm to use corporate proxy
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# Or download binary manually and transfer
# On machine with internet:
curl -fsSL https://claude.ai/download/claude-code/linux-x64 -o claude

# Transfer via USB/internal network
# On target machine:
chmod +x claude && sudo mv claude /usr/local/bin/
```

#### Update Strategies by Installation Method

| Method | Update Command | Auto-update? | Check for Updates |
|--------|---------------|--------------|-------------------|
| **npm** | `npm update -g @anthropic-ai/claude-code` | No | `npm outdated -g` |
| **Homebrew** | `brew upgrade claude-code` | No | `brew update && brew outdated` |
| **winget** | `winget upgrade Anthropic.ClaudeCode` | No | `winget list --upgrade-available` |
| **Direct download** | Re-download and replace binary | No | Check release notes manually |

**Pro tip**: Set up a weekly reminder to check for updates:
```bash
# Add to cron (Linux/macOS)
# Check for updates every Monday at 9am
0 9 * * 1 npm outdated -g | grep claude-code && echo "Claude Code update available!"

# Or create an alias for quick checks
echo 'alias claude-update="npm update -g @anthropic-ai/claude-code && claude --version"' >> ~/.bashrc
```

#### Team Installation Best Practices

**For Small Teams (2-10 developers)**:
- Use npm installation for consistency
- Document in README: "Requires Node.js 18+, install with `npm install -g @anthropic-ai/claude-code`"
- Create onboarding script:
```bash
#!/bin/bash
# setup-dev-environment.sh

# Check Node.js version
if ! node --version | grep -E "v(18|19|20|21|22)" > /dev/null; then
    echo "Error: Node.js 18+ required"
    exit 1
fi

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Verify
claude --version || {
    echo "Installation failed. Check PATH configuration."
    exit 1
}

echo "✓ Claude Code installed successfully"
```

**For Large Teams/Enterprise**:
- Consider hosting binaries internally (air-gapped environments)
- Use configuration management (Ansible, Chef, Puppet) to deploy
- Example Ansible playbook:
```yaml
# deploy-claude-code.yml
- name: Install Claude Code on developer workstations
  hosts: developers
  tasks:
    - name: Download Claude Code binary
      get_url:
        url: https://internal-repo.company.com/tools/claude-code-linux-x64
        dest: /usr/local/bin/claude
        mode: '0755'

    - name: Verify installation
      command: claude --version
      register: claude_version

    - name: Print version
      debug:
        msg: "Claude Code {{ claude_version.stdout }} installed"
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

### Authentication Security Best Practices

Understanding authentication methods and their security implications is critical for DevOps teams. Here's what you need to know.

#### Security Comparison: Authentication Methods

| Method | Security Level | Use Case | Risk Profile |
|--------|---------------|----------|--------------|
| **Interactive Login** (`claude login`) | ★★★★★ High | Individual developers | Low - Tokens stored encrypted, automatic refresh |
| **API Key in Environment Variable** | ★★★☆☆ Medium | CI/CD pipelines, automation | Medium - Visible in process list, logged in shell history |
| **API Key in Config File** | ★★☆☆☆ Low | Not recommended | High - Plaintext file, easy to accidentally commit |
| **AWS Bedrock (IAM Roles)** | ★★★★★ High | Enterprise production | Very Low - No long-lived credentials, AWS manages rotation |

#### Method 1: Interactive Login (Recommended for Developers)

**How it works**:
```bash
claude login
# Opens browser → Authenticate with Anthropic → Token stored securely
```

**What happens under the hood**:
1. Creates OAuth token tied to your Anthropic account
2. Stores in system keychain (macOS: Keychain, Linux: Secret Service, Windows: Credential Manager)
3. Token automatically refreshes before expiration
4. Can be revoked from Anthropic console

**Security benefits**:
- ✅ Token never visible in shell history
- ✅ Encrypted at rest in system keychain
- ✅ Automatic expiration and rotation
- ✅ Can revoke from Anthropic dashboard
- ✅ Tied to your account (audit trail)

**When to use**: Default choice for human developers working on their local machines

#### Method 2: Environment Variable (For Automation)

**How to set securely**:
```bash
# DON'T do this (exposed in shell history):
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# DO this instead (prompt for key):
read -s ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY

# Or load from secure store:
export ANTHROPIC_API_KEY=$(aws secretsmanager get-secret-value \
    --secret-id prod/anthropic/api-key \
    --query SecretString \
    --output text)
```

**Security implications**:
- ⚠️ **Visible in process list**: Anyone with access can see it via `ps aux | grep ANTHROPIC`
- ⚠️ **Logged in shell history**: `history | grep ANTHROPIC_API_KEY` exposes it
- ⚠️ **Inherited by child processes**: Any script/command inherits the variable
- ⚠️ **May appear in error logs**: Stack traces can expose environment variables

**When to use**: CI/CD pipelines where interactive login isn't possible

**Mitigation strategies**:
```bash
# 1. Load from secrets manager (best practice)
export ANTHROPIC_API_KEY=$(kubectl get secret anthropic-key -o jsonpath='{.data.key}' | base64 -d)

# 2. Use dedicated service account API keys (not your personal key)
# Create service account key at https://console.anthropic.com

# 3. Restrict key permissions (read-only for production)
# Configure in Anthropic console: API Key → Permissions → Read Only

# 4. Rotate keys regularly
# Set reminder to rotate every 90 days

# 5. Never log the variable
set +x  # Disable bash debugging before loading secrets
export ANTHROPIC_API_KEY=$(get-secret)
set -x  # Re-enable after loading
```

#### Method 3: Configuration File (NOT RECOMMENDED)

**Why it's risky**:
```bash
# ~/.claude/config.json
{
  "api_key": "sk-ant-api03-..."  # ← Plaintext, easy to leak
}
```

**Common leak scenarios**:
1. **Accidental git commit**:
   ```bash
   git add . && git commit -m "update config"
   # Oops, just committed API key to GitHub
   ```

2. **Backup/sync tools**:
   ```bash
   # Dropbox, Google Drive sync entire home directory
   # Your API key is now in the cloud
   ```

3. **File permissions**:
   ```bash
   ls -la ~/.claude/config.json
   # -rw-r--r-- ← Other users can read this!
   ```

**If you must use config file** (please don't):
```bash
# At minimum, restrict permissions
chmod 600 ~/.claude/config.json  # Only you can read/write

# Add to .gitignore BEFORE creating
echo ".claude/config.json" >> ~/.gitignore

# Better: Use placeholder and load at runtime
cat > ~/.claude/config.json <<EOF
{
  "api_key_path": "/secure/secrets/anthropic-key"
}
EOF
```

#### Method 4: AWS Bedrock with IAM Roles (Best for Production)

**How it works**:
```bash
# No API key needed! Uses AWS IAM
export CLAUDE_CODE_PROVIDER=bedrock
export AWS_REGION=us-east-1

# Claude Code uses your AWS credentials
# (IAM role, instance profile, or AWS_PROFILE)
```

**Security benefits**:
- ✅ No long-lived API keys to manage
- ✅ AWS handles credential rotation automatically
- ✅ Fine-grained IAM permissions
- ✅ CloudTrail audit log of all API calls
- ✅ Can restrict by IP, VPC, time of day

**Example IAM policy** (least privilege):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-5-*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": ["10.0.0.0/8"]  // Only from internal network
        },
        "DateGreaterThan": {
          "aws:CurrentTime": "2025-01-01T00:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2025-12-31T23:59:59Z"
        }
      }
    }
  ]
}
```

**When to use**: Production environments, enterprise teams, compliance requirements

#### Common Authentication Mistakes

##### Mistake 1: Using Personal API Key in CI/CD

**Problem**:
```yaml
# .github/workflows/ci.yml
env:
  ANTHROPIC_API_KEY: sk-ant-api03-your-personal-key  # ← Bad!
```

**Why it's bad**:
- Tied to individual's account (what if they leave?)
- Hard to rotate (need to update everywhere)
- No separation of permissions (same key for dev and prod)
- Audit trails show individual's name, not service

**Solution**: Use service account API keys
```yaml
# .github/workflows/ci.yml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_SERVICE_ACCOUNT_KEY }}

# Create service account at https://console.anthropic.com
# Name it clearly: "github-actions-prod" or "ci-cd-pipeline"
```

##### Mistake 2: Committing API Keys to Git

**Symptoms**: You pushed a commit and realized seconds later your API key is in the history

**Immediate action**:
```bash
# 1. REVOKE THE KEY IMMEDIATELY
# Go to https://console.anthropic.com/api-keys → Revoke

# 2. Remove from git history (if just pushed)
git reset --hard HEAD~1
git push --force  # Only if no one else pulled yet

# 3. If others already pulled or it's been a while:
# Use BFG Repo Cleaner or git-filter-repo
# See: https://rtyley.github.io/bfg-repo-cleaner/

# 4. Generate new API key
# Go to Anthropic console → Create New Key

# 5. Add proper .gitignore
echo ".env" >> .gitignore
echo ".claude/config.json" >> .gitignore
git add .gitignore && git commit -m "prevent api key leaks"
```

**Prevention**: Use pre-commit hooks
```bash
# Install pre-commit framework
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install hook
pre-commit install

# Now commits with API keys are blocked!
```

##### Mistake 3: Storing Keys in Docker Images

**Problem**:
```dockerfile
# Dockerfile
FROM node:20
ENV ANTHROPIC_API_KEY=sk-ant-api03-...  # ← Baked into image!
```

**Why it's bad**:
- Anyone with access to image can extract the key
- Key persists even if you change it later
- Image layers are cached and reused

**Solution**: Pass secrets at runtime
```dockerfile
# Dockerfile (correct)
FROM node:20
# NO API KEY HERE!

# At runtime:
docker run -e ANTHROPIC_API_KEY=$(get-secret) myimage

# Or use Docker secrets (Swarm/Kubernetes)
kubectl create secret generic anthropic-key --from-literal=key=$(get-secret)

# In pod spec:
env:
  - name: ANTHROPIC_API_KEY
    valueFrom:
      secretKeyRef:
        name: anthropic-key
        key: key
```

#### Team Authentication Strategy

**For Development Environments**:
```bash
# Each developer uses their own account
claude login

# Benefits:
# - Individual audit trails
# - Easy to revoke if developer leaves
# - No shared credentials to manage
```

**For Staging/Production**:
```bash
# Use AWS Bedrock with IAM roles (best)
export CLAUDE_CODE_PROVIDER=bedrock

# OR: Use service account API keys
# Stored in secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
```

**For CI/CD Pipelines**:
```yaml
# GitHub Actions example
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Claude Code
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_CI_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code
          claude "run tests"

# Key best practices:
# 1. Use GitHub Secrets (encrypted at rest)
# 2. Limit secret access to specific workflows
# 3. Rotate keys quarterly
# 4. Use different keys for different environments
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
│  • Shift+Enter for multi-line input (iTerm2, WezTerm,          │
│    Ghostty, Kitty)                                             │
│  • Use ↑/↓ arrows for history                                  │
│  • Tab for autocompletion                                      │
│  • Ctrl+C to cancel current operation                          │
│  • Ctrl+T to toggle theme/syntax highlighting                  │
│  • Ctrl+B to background running tasks                          │
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
/stats                   # Usage statistics, graphs, and streaks
/config                  # Access configuration settings
/doctor                  # Diagnose issues (permission rules, etc.)

# File operations
/file path/to/file       # Add file to context
/tree                    # Show project structure

# Session management
/clear                   # Clear conversation history
/history                 # Show conversation history
/rename <name>           # Name current session for easy recall
/resume <name>           # Resume a named session
/save                    # Save session
/load                    # Load previous session

# Control
/stop                    # Stop current operation
/exit or Ctrl+D          # Exit Claude Code

# Remote features (for claude.ai subscribers)
/teleport                # Connect to remote environment
/remote-env              # Remote environment management
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
│  /stats   - Usage statistics and graphs                        │
│  /config  - Access settings                                    │
│  /doctor  - Diagnose configuration issues                      │
│  /rename  - Name session for easy resume                       │
│  /resume  - Resume named session                               │
│  /stop    - Stop current operation                             │
│  /exit    - Exit Claude Code                                   │
│                                                                │
│  Keyboard Shortcuts:                                           │
│  Ctrl+C   - Cancel current operation                           │
│  Ctrl+T   - Toggle theme/syntax highlighting                   │
│  Ctrl+B   - Background running tasks                           │
│  Shift+Enter - Multi-line input (modern terminals)             │
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

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0

---

## Navigation

← Previous: [Chapter 5: Introduction to Claude](./05-introduction-to-claude.md) | Next: [Chapter 7: Claude Code Intermediate](./07-claude-code-intermediate.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 6** | Claude Code Fundamentals | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
