# Source Code Examples

This directory contains all code examples and configurations from the guide, organized by chapter.

## Directory Structure

```
src/
├── chapter-01/                    # Introduction to AI
│   ├── traditional_vs_ml.py       # Traditional vs ML programming comparison
│   ├── aiops_examples.py          # AIOps patterns and examples
│   └── dockerfile_optimization.md # Dockerfile optimization examples
│
├── chapter-02/                    # Understanding LLMs and Tokens
│   └── token_examples.py          # Token counting, cost estimation, context management
│
├── chapter-03/                    # The Art of Prompting
│   ├── craft_framework.py         # CRAFT framework implementation
│   └── prompt_templates.md        # Reusable prompt templates for DevOps
│
├── chapter-04/                    # AI Models Landscape
│   └── model_selection.py         # Model selection guide and cost calculator
│
├── chapter-05/                    # Introduction to Claude
│   └── claude_api_examples.py     # Claude API usage examples (Anthropic, AWS, GCP)
│
├── chapter-06/                    # Claude Code Fundamentals
│   ├── claude_code_config.json    # Example configuration file
│   └── commands.md                # Command reference and usage guide
│
├── chapter-07/                    # Claude Code Intermediate
│   ├── project_config.json        # Project-level configuration
│   ├── custom-commands/           # Custom command templates
│   │   ├── review-pr.md           # PR review command
│   │   └── generate-tests.md      # Test generation command
│   └── github-actions/
│       └── claude-review.yaml     # GitHub Actions CI integration
│
├── chapter-08/                    # Claude Code Professional
│   ├── skills/
│   │   └── my-company-standards.yaml  # Custom skills definition
│   ├── hooks/
│   │   └── hooks.yaml             # Hooks configuration
│   └── memory/
│       └── memory.yaml            # Long-term memory configuration
│
├── chapter-09/                    # MCP Deep Dive
│   ├── mcp-config/
│   │   └── mcp_servers.json       # MCP server configuration
│   └── mcp-servers/
│       ├── kubernetes-mcp-server.ts   # Kubernetes MCP server
│       └── aws-mcp-server.ts          # AWS MCP server
│
└── chapter-10/                    # AI for DevOps
    ├── shell-aliases.sh           # Shell aliases and functions
    └── prompts/
        ├── incident-response.md   # Incident response templates
        └── prometheus-alerts.yaml # Prometheus alerting rules
```

## Usage

### Python Examples

Most Python examples can be run directly:

```bash
cd src/chapter-01
python traditional_vs_ml.py
```

For examples requiring dependencies:

```bash
pip install anthropic tiktoken  # For API and token examples
```

### TypeScript Examples (MCP Servers)

```bash
cd src/chapter-09/mcp-servers

# Install dependencies
npm init -y
npm install @modelcontextprotocol/sdk @kubernetes/client-node @aws-sdk/client-ec2

# Run with tsx
npx tsx kubernetes-mcp-server.ts
```

### Shell Aliases

Add to your shell configuration:

```bash
source src/chapter-10/shell-aliases.sh
```

### Configuration Files

Copy and customize for your projects:

```bash
# Claude Code config
cp src/chapter-06/claude_code_config.json ~/.claude/config.json

# MCP servers
cp src/chapter-09/mcp-config/mcp_servers.json ~/.claude/mcp_servers.json

# Project config
mkdir -p .claude
cp src/chapter-07/project_config.json .claude/config.json
```

## Chapter Overview

| Chapter | Topic | Key Examples |
|---------|-------|--------------|
| 01 | AI Fundamentals | Traditional vs ML, AIOps patterns |
| 02 | LLMs & Tokens | Token counting, cost estimation |
| 03 | Prompting | CRAFT framework, templates |
| 04 | AI Models | Model selection, cost calculation |
| 05 | Claude Intro | API usage across platforms |
| 06 | Claude Code Basics | Configuration, commands |
| 07 | Claude Code Intermediate | Custom commands, CI integration |
| 08 | Claude Code Professional | Skills, hooks, memory |
| 09 | MCP Deep Dive | Custom MCP servers |
| 10 | AI for DevOps | Shell helpers, incident response |

## Quick Start by Use Case

### Code Review

```bash
# Use the PR review command
cp src/chapter-07/custom-commands/review-pr.md .claude/commands/

# Or use shell alias
source src/chapter-10/shell-aliases.sh
ai-review-pr
```

### Infrastructure Generation

Use the prompts from chapter 03 and 10 for:
- Terraform modules
- Kubernetes manifests
- Ansible playbooks

### Incident Response

Copy the incident response template:
```bash
cat src/chapter-10/prompts/incident-response.md
```

### MCP Integration

Set up custom MCP servers:
```bash
# Configure servers
cp src/chapter-09/mcp-config/mcp_servers.json ~/.claude/

# Build custom servers
cd src/chapter-09/mcp-servers
npm install
```

## Contributing

Feel free to submit PRs with:
- Bug fixes for examples
- Additional use cases
- Improved documentation
- New language implementations

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

This code is part of the AI and Claude Code Guide for DevOps Engineers.
See the main [LICENSE](../LICENSE) file for terms.

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0
