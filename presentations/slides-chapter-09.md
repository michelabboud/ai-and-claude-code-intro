---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #eee
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  h1 {
    color: #00d4ff;
  }
  h2 {
    color: #7c3aed;
  }
  code {
    background-color: #2d2d44;
  }
---

# MCP Deep Dive

## Chapter 9: Model Context Protocol

**The Universal Connector for AI**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# What is MCP?

## Model Context Protocol

An open standard for connecting AI to external data sources and tools.

> Like **USB for AI integrations**
> Build once, use everywhere

---

# The Problem MCP Solves

## Before MCP

```
AI App ──custom integration──► GitHub
AI App ──custom integration──► Database
AI App ──custom integration──► Slack
AI App ──custom integration──► Kubernetes

Each integration: custom code, duplicated effort
```

---

# With MCP

```
┌──────────────────────────────────────────┐
│           MCP PROTOCOL LAYER             │
│     (Standard for all integrations)      │
└────────────────┬─────────────────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ GitHub  │ │ K8s     │ │ Postgres│
│ MCP     │ │ MCP     │ │ MCP     │
│ Server  │ │ Server  │ │ Server  │
└─────────┘ └─────────┘ └─────────┘
```

Build server once, any AI can use it!

---

# MCP Components

```
MCP CLIENT (Claude Code)
    │
    │  JSON-RPC Protocol
    │
    ▼
MCP SERVER (GitHub, K8s, etc.)
    │
    │  Native API/SDK
    │
    ▼
EXTERNAL SYSTEM
```

---

# The Three Primitives

## 1. Tools
Functions Claude can execute

```json
{
  "name": "get_pods",
  "parameters": {"namespace": "production"}
}
```

## 2. Resources
Data Claude can read

## 3. Prompts
Reusable templates

---

# Configuration

## ~/.claude/mcp_servers.json

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@mcp/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

---

# Official MCP Servers

| Server | What it Does |
|--------|--------------|
| **filesystem** | Read/write files |
| **github** | Repos, PRs, issues |
| **postgres** | Database queries |
| **slack** | Messages, channels |
| **sqlite** | Local databases |

Install: `npx @modelcontextprotocol/server-*`

---

# Using MCP in Claude Code

```bash
claude

# Claude now has MCP tools available
> List my GitHub repositories
# Uses mcp__github__list_repos

> Show pods in production namespace
# Uses mcp__kubernetes__get_pods

> Query users table
# Uses mcp__postgres__run_query
```

---

# DevOps MCP Example: K8s

```typescript
const tools = [
  {
    name: "get_pods",
    description: "List pods in namespace",
    inputSchema: {
      type: "object",
      properties: {
        namespace: { type: "string" }
      }
    }
  },
  { name: "get_pod_logs" },
  { name: "scale_deployment" },
  { name: "apply_manifest" }
];
```

---

# Multi-Cloud Setup

```json
{
  "mcpServers": {
    "aws": { "command": "node", "args": ["aws-mcp"] },
    "gcp": { "command": "node", "args": ["gcp-mcp"] },
    "azure": { "command": "node", "args": ["azure-mcp"] }
  }
}
```

```bash
> List compute instances across all clouds
# Queries all three providers!
```

---

# Monitoring Stack

```json
{
  "mcpServers": {
    "prometheus": { ... },
    "grafana": { ... },
    "pagerduty": { ... }
  }
}
```

```bash
> Show current PagerDuty alerts
> Query error rate from Prometheus
> Create Grafana dashboard
```

---

# Building MCP Servers

## Project Structure

```
my-mcp-server/
├── package.json
├── src/
│   ├── index.ts      # Entry point
│   ├── tools/        # Tool implementations
│   └── resources/    # Resource handlers
```

---

# MCP Server Code

```typescript
import { Server } from "@modelcontextprotocol/sdk";

const server = new Server({
  name: "my-devops-server",
  version: "1.0.0"
});

// Register tools
server.setRequestHandler(ListToolsRequestSchema, () => ({
  tools: [{ name: "check_health", ... }]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, request => {
  // Implementation
});
```

---

# Security Considerations

## Best Practices

```yaml
authentication:
  - Store API keys in environment variables
  - Never hardcode secrets
  - Rotate keys regularly

authorization:
  - Use read-only tokens when possible
  - Apply least privilege
  - Separate tokens for CI vs interactive

audit:
  - Log all MCP tool calls
  - Monitor for unusual patterns
```

---

# MCP Use Cases for DevOps

| Use Case | MCP Servers |
|----------|-------------|
| Multi-cloud management | aws, gcp, azure |
| Monitoring | prometheus, grafana, datadog |
| CI/CD | github, argocd, jenkins |
| Databases | postgres, redis, mongodb |
| Communication | slack, teams |

---

# Quick Start

```bash
# 1. Create config
mkdir -p ~/.claude
cat > ~/.claude/mcp_servers.json << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@mcp/server-filesystem", "/tmp"]
    }
  }
}
EOF

# 2. Start Claude Code
claude

# 3. Use MCP tools
> List files in the MCP filesystem
```

---

# Key Takeaways

1. **MCP standardizes AI integrations**
2. **Three primitives**: Tools, Resources, Prompts
3. **Claude Code has built-in MCP client**
4. **Build custom servers** for your tools
5. **Security matters**: least privilege, audit logs

---

# Quick Reference

```
┌─────────────────────────────────────────┐
│  Config: ~/.claude/mcp_servers.json     │
│                                         │
│  Official servers:                      │
│  @modelcontextprotocol/server-*         │
│                                         │
│  Build servers with:                    │
│  @modelcontextprotocol/sdk              │
│                                         │
│  Primitives:                            │
│  • Tools = Functions to call            │
│  • Resources = Data to read             │
│  • Prompts = Templates                  │
│                                         │
│  Transport: stdio (local) or HTTP       │
└─────────────────────────────────────────┘
```

---

# Next: Chapter 10

## AI for DevOps

- Practical workflows
- Real-world examples
- Tips and tricks
- Building AI-first culture

---

# Questions?

## Resources

- Full chapter: [chapters/09-mcp-deep-dive.md](../chapters/09-mcp-deep-dive.md)
- MCP Spec: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- Official servers: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

---

# Credits

**Author:** Michel Abboud
**Created with:** Claude AI (Anthropic)

**License:** CC BY-NC 4.0 | © 2026 Michel Abboud
