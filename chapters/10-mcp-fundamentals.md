# Chapter 10: MCP (Model Context Protocol) Fundamentals

## Connecting Claude Code to External Systems

**📖 Reading time:** ~9 minutes | **⚙️ Hands-on time:** ~30 minutes
**🎯 Quick nav:** [What is MCP?](#101-what-is-mcp) | [Architecture](#102-mcp-architecture) | [Using MCP](#103-using-mcp-in-claude-code) | [Use Cases](#104-mcp-use-cases-for-devops) | [Security](#105-security-considerations) | [🏋️ Skip to Exercises](#106-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** MCP is an open protocol that lets Claude Code connect to external tools and data sources (databases, AWS, Kubernetes, etc.) through a standardized interface. Instead of custom integrations, you build once and use everywhere.

**Key concepts:**
- **MCP = Universal adapter** for AI to access external systems
- **MCP servers** provide tools, resources, and prompts to Claude Code
- **Three main components:** Resources (read data), Tools (take actions), Prompts (templates)
- **Use existing servers** from the community or **build your own** (covered in Chapter 11)
- **Perfect for DevOps:** AWS management, K8s operations, database queries, monitoring integrations

**Most important takeaway:** MCP transforms Claude Code from a code editor into a complete DevOps automation platform by giving it access to your infrastructure.

**Hands-on:** [Jump to exercises](#106-hands-on-exercises) to install official MCP servers and start using external tools.

---

*💡 Need the full deep dive? Keep reading. Just need to get started? Jump to exercises!*

---

This chapter introduces the Model Context Protocol (MCP) and shows you how to use existing MCP servers to connect Claude Code to external systems.

---

**📖 Reading time:** ~18 minutes | **⚙️ Hands-on time:** ~45 minutes
**🎯 Quick nav:** [What is MCP?](#91-what-is-mcp) | [Architecture](#92-mcp-architecture) | [Using MCP](#93-using-mcp-in-claude-code) | [Building Servers](#94-building-custom-mcp-servers) | [🏋️ Skip to Exercises](#98-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** MCP is an open protocol that lets Claude Code connect to external tools and data sources (databases, AWS, Kubernetes, etc.) through a standardized interface. Instead of custom integrations, you build once and use everywhere.

**Key concepts:**
- **MCP = Universal adapter** for AI to access external systems
- **MCP servers** provide tools, resources, and prompts to Claude Code
- **Three main components:** Resources (read data), Tools (take actions), Prompts (templates)
- **Use existing servers** from the community or **build your own** in TypeScript/Python
- **Perfect for DevOps:** AWS management, K8s operations, database queries, monitoring integrations

**Most important takeaway:** MCP transforms Claude Code from a code editor into a complete DevOps automation platform by giving it access to your infrastructure.

**Hands-on:** [Jump to exercises](#98-hands-on-exercises) to install official MCP servers and build your first custom server.

---

*💡 Need the full deep dive? Keep reading. Just need the essentials? You're done – try the exercises!*

---

The **Model Context Protocol (MCP)** is one of the most powerful features of Claude Code. It's an open standard that allows AI systems to connect with external data sources and tools. This chapter provides a comprehensive exploration of MCP for DevOps professionals.

---

## 10.1 What is MCP?

### The Problem MCP Solves

```
┌────────────────────────────────────────────────────────────────┐
│                    BEFORE MCP                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│    ┌─────────────┐                                             │
│    │   AI App    │                                             │
│    │   (Claude)  │                                             │
│    └──────┬──────┘                                             │
│           │                                                    │
│           │  Custom integration for each data source           │
│           │                                                    │
│    ┌──────┼──────┬──────────┬──────────┬──────────┐            │
│    │      │      │          │          │          │            │
│    ▼      ▼      ▼          ▼          ▼          ▼            │
│  ┌───┐ ┌───┐ ┌─────┐   ┌───────┐  ┌─────┐  ┌──────┐            │
│  │Git│ │DB │ │Slack│   │Jira   │  │AWS  │  │K8s   │            │
│  └───┘ └───┘ └─────┘   └───────┘  └─────┘  └──────┘            │
│                                                                │
│  Problems:                                                     │
│  • Each integration is custom-built                            │
│  • Duplicated effort across AI applications                    │
│  • Inconsistent interfaces                                     │
│  • Hard to maintain and update                                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    WITH MCP                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     │
│    │  Claude     │     │  ChatGPT    │     │  Other AI   │     │
│    │  Code       │     │  Plugin     │     │  App        │     │
│    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     │
│           │                   │                   │            │
│           │    Standard MCP Protocol              │            │
│           │                   │                   │            │
│    ┌──────┴───────────────────┴───────────────────┴──────┐     │
│    │                    MCP LAYER                         │    │
│    │  (Unified protocol for all integrations)             │    │
│    └──────────────────────────┬───────────────────────────┘    │
│                               │                                │
│    ┌──────┬──────┬───────┬────┴───┬───────┬───────┐            │
│    │      │      │       │        │       │       │            │
│    ▼      ▼      ▼       ▼        ▼       ▼       ▼            │
│  ┌───┐ ┌───┐ ┌─────┐ ┌───────┐ ┌─────┐ ┌──────┐ ┌───┐          │
│  │Git│ │DB │ │Slack│ │Jira   │ │AWS  │ │K8s   │ │...│          │
│  │MCP│ │MCP│ │MCP  │ │MCP    │ │MCP  │ │MCP   │ │   │          │
│  └───┘ └───┘ └─────┘ └───────┘ └─────┘ └──────┘ └───┘          │
│                                                                │
│  Benefits:                                                     │
│  • Standard protocol for all integrations                      │
│  • Build once, use everywhere                                  │
│  • Consistent interface                                        │
│  • Community-maintained servers                                │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### MCP Definition

**MCP (Model Context Protocol)** is an open protocol that standardizes how AI applications connect to external data sources and tools.

```yaml
# MCP in simple terms

what_it_is:
  - "A standard way for AI to talk to external services"
  - "Like USB for AI integrations"
  - "Open source and community-driven"

components:
  mcp_server:
    description: "Provides capabilities to AI clients"
    examples:
      - "GitHub MCP server - provides Git/GitHub operations"
      - "PostgreSQL MCP server - provides database queries"
      - "Kubernetes MCP server - provides K8s management"

  mcp_client:
    description: "AI application that uses MCP servers"
    examples:
      - "Claude Code (built-in MCP client)"
      - "Claude Desktop"
      - "Other AI tools adopting MCP"

  protocol:
    description: "The standard communication format"
    transport: "JSON-RPC over stdio or HTTP"
    capabilities:
      - "Tools (functions the AI can call)"
      - "Resources (data the AI can read)"
      - "Prompts (templates for common tasks)"
```

---

## 10.2 MCP Architecture

### Core Components

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         MCP ARCHITECTURE                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                         MCP CLIENT                                 │    │
│  │                        (Claude Code)                               │    │
│  │                                                                    │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │    │
│  │  │ Server Manager  │  │ Protocol Handler│  │ Capability Cache│     │    │
│  │  │                 │  │                 │  │                 │     │    │
│  │  │ • Start servers │  │ • Send requests │  │ • Tools list    │     │    │
│  │  │ • Health check  │  │ • Handle resp.  │  │ • Resources     │     │    │
│  │  │ • Restart       │  │ • Error handle  │  │ • Prompts       │     │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │    │
│  └────────────────────────────────┬───────────────────────────────────┘    │
│                                   │                                        │
│                          JSON-RPC Protocol                                 │
│                        (stdio or HTTP/SSE)                                 │
│                                   │                                        │
│  ┌────────────────────────────────┼───────────────────────────────────┐    │
│  │                                │                                   │    │
│  │     ┌──────────────────────────┼───────────────────────────┐       │    │
│  │     │                          │                           │       │    │
│  │     ▼                          ▼                           ▼       │    │
│  │  ┌─────────────┐   ┌─────────────────────┐   ┌─────────────────┐   │    │
│  │  │ GitHub      │   │ Kubernetes          │   │ PostgreSQL      │   │    │
│  │  │ MCP Server  │   │ MCP Server          │   │ MCP Server      │   │    │
│  │  │             │   │                     │   │                 │   │    │
│  │  │ Tools:      │   │ Tools:              │   │ Tools:          │   │    │
│  │  │ • clone     │   │ • get_pods          │   │ • query         │   │    │
│  │  │ • commit    │   │ • get_deployments   │   │ • execute       │   │    │
│  │  │ • create_pr │   │ • apply_manifest    │   │ • list_tables   │   │    │
│  │  │ • list_prs  │   │ • scale             │   │ • describe      │   │    │
│  │  └─────────────┘   └─────────────────────┘   └─────────────────┘   │    │
│  │                                                                    │    │
│  │                         MCP SERVERS                                │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### The Three Primitives

```yaml
# MCP provides three types of capabilities

1_tools:
  description: "Functions that Claude can execute"
  characteristics:
    - "Take parameters"
    - "Perform actions"
    - "Return results"
  examples:
    - name: "create_file"
      parameters: ["path", "content"]
      description: "Creates a file at the specified path"

    - name: "run_query"
      parameters: ["sql", "database"]
      description: "Executes SQL query against database"

    - name: "kubectl_apply"
      parameters: ["manifest"]
      description: "Applies Kubernetes manifest"

2_resources:
  description: "Data that Claude can read"
  characteristics:
    - "URI-addressable"
    - "Read-only"
    - "Can be dynamic or static"
  examples:
    - uri: "file:///path/to/config.yaml"
      description: "Local file content"

    - uri: "postgres://db/users"
      description: "Database table contents"

    - uri: "k8s://namespace/pods"
      description: "Kubernetes resource list"

3_prompts:
  description: "Reusable prompt templates"
  characteristics:
    - "Parameterized templates"
    - "Best practices encoded"
    - "Server-provided workflows"
  examples:
    - name: "analyze_slow_query"
      parameters: ["query_text"]
      description: "Template for analyzing SQL performance"

    - name: "debug_pod"
      parameters: ["pod_name", "namespace"]
      description: "Template for debugging K8s pods"
```

---

## 10.3 Using MCP in Claude Code

### Configuring MCP Servers

```json
// Claude Code MCP configuration
// Location: ~/.claude/mcp_servers.json (or claude_desktop_config.json)

{
  "mcpServers": {
    // GitHub Server
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },

    // PostgreSQL Server
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    },

    // Filesystem Server
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    },

    // Kubernetes Server (custom)
    "kubernetes": {
      "command": "node",
      "args": ["/path/to/k8s-mcp-server/index.js"],
      "env": {
        "KUBECONFIG": "${HOME}/.kube/config"
      }
    },

    // Slack Server
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

### Using MCP Tools in Claude Code

```bash
# Start Claude Code (MCP servers start automatically)
claude

# Claude now has access to MCP tools
> List my GitHub repositories

# Claude uses mcp__github__list_repos tool
# Returns list of repos

> Show pods in the production namespace

# Claude uses mcp__kubernetes__get_pods tool
# Returns pod list

> Query the users table for admin accounts

# Claude uses mcp__postgres__run_query tool
# Returns query results
```

### Dynamic Tool Updates (New in 2.1)

MCP now supports `list_changed` notifications, allowing servers to dynamically update their available tools:

```yaml
# MCP servers can now:
- Add new tools at runtime
- Remove tools when no longer available
- Update tool schemas
- All without requiring reconnection or restart

# This is especially useful for:
- Database connections (new tables become queryable)
- Kubernetes (new CRDs become available)
- Dynamic service discovery
```

> **What Changed:** Previously, MCP tool lists were static after connection. Now servers can send `list_changed` notifications and Claude Code will refresh its understanding of available tools.

### Available MCP Servers (Official)

```yaml
# Official MCP servers maintained by Anthropic

filesystem:
  package: "@modelcontextprotocol/server-filesystem"
  description: "Read/write files in specified directories"
  tools:
    - read_file
    - write_file
    - list_directory
    - search_files

github:
  package: "@modelcontextprotocol/server-github"
  description: "GitHub operations"
  tools:
    - search_repositories
    - get_file_contents
    - create_or_update_file
    - push_files
    - create_issue
    - create_pull_request
    - list_commits
    - list_branches

postgres:
  package: "@modelcontextprotocol/server-postgres"
  description: "PostgreSQL database operations"
  tools:
    - query
    - list_tables
    - describe_table

sqlite:
  package: "@modelcontextprotocol/server-sqlite"
  description: "SQLite database operations"
  tools:
    - read_query
    - write_query
    - list_tables
    - describe_table

slack:
  package: "@modelcontextprotocol/server-slack"
  description: "Slack operations"
  tools:
    - list_channels
    - post_message
    - get_channel_history
    - search_messages

google_drive:
  package: "@modelcontextprotocol/server-gdrive"
  description: "Google Drive operations"
  tools:
    - search_files
    - get_file_content

memory:
  package: "@modelcontextprotocol/server-memory"
  description: "Persistent memory/knowledge storage"
  tools:
    - store_memory
    - retrieve_memory
    - search_memories

fetch:
  package: "@modelcontextprotocol/server-fetch"
  description: "Fetch web content"
  tools:
    - fetch_url
```

---

## 10.4 MCP Use Cases for DevOps

### Use Case 1: Multi-Cloud Management

```json
// Configuration for multi-cloud MCP servers
{
  "mcpServers": {
    "aws": {
      "command": "node",
      "args": ["./servers/aws-mcp/index.js"],
      "env": {
        "AWS_PROFILE": "production"
      }
    },
    "gcp": {
      "command": "node",
      "args": ["./servers/gcp-mcp/index.js"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "${HOME}/.gcp/credentials.json"
      }
    },
    "azure": {
      "command": "node",
      "args": ["./servers/azure-mcp/index.js"],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "${AZURE_SUB_ID}"
      }
    }
  }
}
```

```bash
# Now Claude can manage resources across clouds
claude

> List all running compute instances across AWS, GCP, and Azure

# Claude queries all three MCP servers
# Aggregates and presents unified view

> Find the most expensive resources across all clouds

> Scale down non-production resources across all clouds
```

### Use Case 2: Integrated Monitoring Stack

```json
// Monitoring-focused MCP configuration
{
  "mcpServers": {
    "prometheus": {
      "command": "node",
      "args": ["./servers/prometheus-mcp/index.js"],
      "env": {
        "PROMETHEUS_URL": "http://prometheus:9090"
      }
    },
    "grafana": {
      "command": "node",
      "args": ["./servers/grafana-mcp/index.js"],
      "env": {
        "GRAFANA_URL": "http://grafana:3000",
        "GRAFANA_API_KEY": "${GRAFANA_API_KEY}"
      }
    },
    "pagerduty": {
      "command": "node",
      "args": ["./servers/pagerduty-mcp/index.js"],
      "env": {
        "PAGERDUTY_API_KEY": "${PAGERDUTY_KEY}"
      }
    },
    "datadog": {
      "command": "node",
      "args": ["./servers/datadog-mcp/index.js"],
      "env": {
        "DD_API_KEY": "${DD_API_KEY}",
        "DD_APP_KEY": "${DD_APP_KEY}"
      }
    }
  }
}
```

```bash
# Integrated monitoring workflow
claude

> Show me the current alerts from PagerDuty

> Query Prometheus for the error rate of the payment service
  over the last hour

> Create a Grafana dashboard for the metrics we just looked at

> If the error rate exceeds 5%, create a PagerDuty incident
```

### Use Case 3: CI/CD Pipeline Management

```json
// CI/CD focused MCP servers
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "argocd": {
      "command": "node",
      "args": ["./servers/argocd-mcp/index.js"],
      "env": {
        "ARGOCD_SERVER": "argocd.example.com",
        "ARGOCD_TOKEN": "${ARGOCD_TOKEN}"
      }
    },
    "jenkins": {
      "command": "node",
      "args": ["./servers/jenkins-mcp/index.js"],
      "env": {
        "JENKINS_URL": "https://jenkins.example.com",
        "JENKINS_USER": "${JENKINS_USER}",
        "JENKINS_TOKEN": "${JENKINS_TOKEN}"
      }
    }
  }
}
```

```bash
# CI/CD workflow with MCP
claude

> Show me failed GitHub Actions runs from the last 24 hours

> For each failed run, get the error logs and summarize
  the root cause

> Check if there are any stuck ArgoCD applications

> Trigger a Jenkins build for the api-service project
```

### Use Case 4: Database Operations

```json
// Database MCP configuration
{
  "mcpServers": {
    "postgres_prod": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${PROD_DATABASE_URL}"
      }
    },
    "postgres_staging": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${STAGING_DATABASE_URL}"
      }
    },
    "redis": {
      "command": "node",
      "args": ["./servers/redis-mcp/index.js"],
      "env": {
        "REDIS_URL": "${REDIS_URL}"
      }
    }
  }
}
```

```bash
# Database operations with MCP
claude

> Compare the schema between staging and production databases

> Show me the slowest queries from the production database
  in the last hour

> Check Redis cache hit rate

> Generate a migration script for adding an index on users.email
```

---

## 10.5 Security Considerations

### MCP Security Best Practices

```yaml
# Security considerations for MCP

authentication:
  api_keys:
    - "Store in environment variables, never in config files"
    - "Use secrets management (HashiCorp Vault, AWS Secrets Manager)"
    - "Rotate regularly"

  example:
    # Bad - hardcoded
    env:
      GITHUB_TOKEN: "ghp_xxxxxxxxxxxx"

    # Good - from environment
    env:
      GITHUB_TOKEN: "${GITHUB_TOKEN}"

authorization:
  principle_of_least_privilege:
    - "MCP servers should only have permissions they need"
    - "Use read-only tokens where possible"
    - "Create service accounts with limited scope"

  examples:
    github:
      good: "Token with only 'repo:read' scope"
      bad: "Token with full 'admin' scope"

    kubernetes:
      good: "ServiceAccount with specific namespace access"
      bad: "cluster-admin token"

network_security:
  recommendations:
    - "Run MCP servers locally (stdio transport)"
    - "If using HTTP, use TLS"
    - "Firewall MCP server ports"
    - "Use VPN for remote resources"

data_protection:
  considerations:
    - "MCP servers can access sensitive data"
    - "Be careful what databases you connect"
    - "Audit MCP tool usage"
    - "Consider data masking for sensitive fields"

  example_masking: |
    // In your MCP server
    function maskSensitiveData(data) {
      return data.map(row => ({
        ...row,
        email: row.email.replace(/(.{2}).*(@.*)/, '$1***$2'),
        ssn: '***-**-' + row.ssn.slice(-4),
      }));
    }
```

### Audit Logging

```typescript
// Add audit logging to your MCP server

import { appendFileSync } from "fs";

function auditLog(action: string, details: any) {
  const entry = {
    timestamp: new Date().toISOString(),
    action,
    details,
    user: process.env.USER,
  };

  appendFileSync(
    "/var/log/mcp-audit.log",
    JSON.stringify(entry) + "\n"
  );

  // Also send to SIEM/logging system
  sendToSplunk(entry);
}

// In tool handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  // Audit all tool calls
  auditLog("tool_call", { tool: name, arguments: args });

  // ... handle the tool
});
```

---


---

## 10.6 Hands-On Exercises

### Exercise 1: Install and Use Official MCP Servers

```bash
# 1. Install official MCP servers
npx @modelcontextprotocol/create-server

# 2. Configure in ~/.claude/mcp_servers.json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem",
             "/path/to/allowed/directory"]
  },
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "your_token_here"
    }
  }
}

# 3. Test the servers
claude
> List files in the configured directory
> Show my GitHub issues
> Query database for recent users
```

### Exercise 2: Explore MCP Capabilities

```bash
# Try different MCP tools

# Database operations
> Query the users table for accounts created this week
> Show database schema

# Cloud operations (if AWS MCP server configured)
> List EC2 instances in us-east-1
> Show S3 buckets

# Kubernetes operations (if K8s MCP server configured)
> List all pods in production namespace
> Show deployment status for api-service
```

### Exercise 3: Security Review

```yaml
# Review your MCP configuration for security

# 1. Check permissions
# - Are MCP servers accessing only necessary resources?
# - Are credentials properly secured?
# - Are tokens scoped appropriately?

# 2. Test restrictions
# - Try accessing unauthorized resources
# - Verify error handling works
# - Confirm audit logging is active

# 3. Document security practices
# - Create runbook for MCP security
# - Share with team
```

---

## 10.7 Chapter Summary

### Key Takeaways

1. **MCP is a universal protocol** for connecting AI to external systems
   - Standardized interface replaces custom integrations
   - Build once, use with any MCP-compatible client
   - Growing ecosystem of community servers

2. **MCP has three main components**
   - **Resources**: Read-only data access (files, database queries)
   - **Tools**: Actions and operations (create, update, delete)
   - **Prompts**: Reusable templates with context

3. **Using MCP in Claude Code is simple**
   - Configure servers in ~/.claude/mcp_servers.json
   - Tools automatically available in conversations
   - Transparent integration - just ask naturally

4. **Security is built-in**
   - Explicit permissions and scoping
   - Credential isolation
   - Audit logging
   - Error handling

### Next Steps

- [Chapter 11: MCP Server Development](./11-mcp-server-development.md) - Build your own MCP servers
- Install official MCP servers from the exercises
- Experiment with different MCP tools
- Plan which custom servers you need for your workflow

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0
