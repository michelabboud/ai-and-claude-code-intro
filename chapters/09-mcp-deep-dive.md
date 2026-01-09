# Chapter 9: MCP (Model Context Protocol) Deep Dive

## The Universal Connector for AI Applications

The **Model Context Protocol (MCP)** is one of the most powerful features of Claude Code. It's an open standard that allows AI systems to connect with external data sources and tools. This chapter provides a comprehensive exploration of MCP for DevOps professionals.

---

## 9.1 What is MCP?

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

## 9.2 MCP Architecture

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

## 9.3 Using MCP in Claude Code

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

## 9.4 Building Custom MCP Servers

### MCP Server Anatomy

```typescript
// Basic MCP server structure (TypeScript)

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create server instance
const server = new Server(
  {
    name: "my-devops-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},       // We provide tools
      resources: {},   // We provide resources
    },
  }
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "check_service_health",
        description: "Check health of a service endpoint",
        inputSchema: {
          type: "object",
          properties: {
            url: {
              type: "string",
              description: "The health check URL",
            },
            timeout: {
              type: "number",
              description: "Timeout in milliseconds",
              default: 5000,
            },
          },
          required: ["url"],
        },
      },
      {
        name: "get_metrics",
        description: "Get Prometheus metrics for a service",
        inputSchema: {
          type: "object",
          properties: {
            service: {
              type: "string",
              description: "Service name",
            },
            metric: {
              type: "string",
              description: "Metric name",
            },
          },
          required: ["service", "metric"],
        },
      },
    ],
  };
});

// Implement tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "check_service_health": {
      const { url, timeout = 5000 } = args;
      try {
        const response = await fetch(url, {
          signal: AbortSignal.timeout(timeout),
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                status: response.ok ? "healthy" : "unhealthy",
                statusCode: response.status,
                responseTime: Date.now() - start,
              }),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                status: "error",
                error: error.message,
              }),
            },
          ],
        };
      }
    }

    case "get_metrics": {
      // Implementation for metrics retrieval
      // ...
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### DevOps MCP Server Example: Kubernetes

```typescript
// kubernetes-mcp-server/src/index.ts

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import * as k8s from "@kubernetes/client-node";

// Initialize Kubernetes client
const kc = new k8s.KubeConfig();
kc.loadFromDefault();
const k8sApi = kc.makeApiClient(k8s.CoreV1Api);
const k8sAppsApi = kc.makeApiClient(k8s.AppsV1Api);

const server = new Server(
  { name: "kubernetes-mcp", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_pods",
      description: "List pods in a namespace",
      inputSchema: {
        type: "object",
        properties: {
          namespace: { type: "string", default: "default" },
          labelSelector: { type: "string", description: "Label selector" },
        },
      },
    },
    {
      name: "get_pod_logs",
      description: "Get logs from a pod",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Pod name" },
          namespace: { type: "string", default: "default" },
          container: { type: "string", description: "Container name" },
          tailLines: { type: "number", default: 100 },
        },
        required: ["name"],
      },
    },
    {
      name: "get_deployments",
      description: "List deployments in a namespace",
      inputSchema: {
        type: "object",
        properties: {
          namespace: { type: "string", default: "default" },
        },
      },
    },
    {
      name: "scale_deployment",
      description: "Scale a deployment to specified replicas",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Deployment name" },
          namespace: { type: "string", default: "default" },
          replicas: { type: "number", description: "Desired replicas" },
        },
        required: ["name", "replicas"],
      },
    },
    {
      name: "apply_manifest",
      description: "Apply a Kubernetes manifest",
      inputSchema: {
        type: "object",
        properties: {
          manifest: { type: "string", description: "YAML manifest content" },
        },
        required: ["manifest"],
      },
    },
    {
      name: "describe_pod",
      description: "Get detailed information about a pod",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string" },
          namespace: { type: "string", default: "default" },
        },
        required: ["name"],
      },
    },
  ],
}));

// Implement tools
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "get_pods": {
      const { namespace = "default", labelSelector } = args;
      const response = await k8sApi.listNamespacedPod(
        namespace,
        undefined,
        undefined,
        undefined,
        undefined,
        labelSelector
      );

      const pods = response.body.items.map((pod) => ({
        name: pod.metadata?.name,
        status: pod.status?.phase,
        ready: pod.status?.conditions?.find((c) => c.type === "Ready")?.status,
        restarts: pod.status?.containerStatuses?.[0]?.restartCount || 0,
        age: pod.metadata?.creationTimestamp,
      }));

      return {
        content: [{ type: "text", text: JSON.stringify(pods, null, 2) }],
      };
    }

    case "get_pod_logs": {
      const { name, namespace = "default", container, tailLines = 100 } = args;
      const response = await k8sApi.readNamespacedPodLog(
        name,
        namespace,
        container,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        tailLines
      );

      return {
        content: [{ type: "text", text: response.body }],
      };
    }

    case "scale_deployment": {
      const { name, namespace = "default", replicas } = args;
      const patch = { spec: { replicas } };

      await k8sAppsApi.patchNamespacedDeploymentScale(
        name,
        namespace,
        patch,
        undefined,
        undefined,
        undefined,
        undefined,
        { headers: { "Content-Type": "application/merge-patch+json" } }
      );

      return {
        content: [
          {
            type: "text",
            text: `Scaled deployment ${name} to ${replicas} replicas`,
          },
        ],
      };
    }

    // ... other tool implementations
  }
});

// Resources: expose cluster information
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "k8s://namespaces",
      name: "Kubernetes Namespaces",
      description: "List of all namespaces in the cluster",
      mimeType: "application/json",
    },
    {
      uri: "k8s://nodes",
      name: "Kubernetes Nodes",
      description: "List of all nodes in the cluster",
      mimeType: "application/json",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "k8s://namespaces") {
    const response = await k8sApi.listNamespace();
    const namespaces = response.body.items.map((ns) => ns.metadata?.name);
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(namespaces),
        },
      ],
    };
  }

  if (uri === "k8s://nodes") {
    const response = await k8sApi.listNode();
    const nodes = response.body.items.map((node) => ({
      name: node.metadata?.name,
      status: node.status?.conditions?.find((c) => c.type === "Ready")?.status,
      capacity: node.status?.capacity,
    }));
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(nodes, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Kubernetes MCP server running");
```

### DevOps MCP Server Example: AWS

```typescript
// aws-mcp-server/src/index.ts

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  EC2Client,
  DescribeInstancesCommand,
  StartInstancesCommand,
  StopInstancesCommand,
} from "@aws-sdk/client-ec2";
import {
  S3Client,
  ListBucketsCommand,
  ListObjectsV2Command,
} from "@aws-sdk/client-s3";
import {
  CloudWatchClient,
  GetMetricDataCommand,
} from "@aws-sdk/client-cloudwatch";

const ec2 = new EC2Client({});
const s3 = new S3Client({});
const cloudwatch = new CloudWatchClient({});

const server = new Server(
  { name: "aws-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_ec2_instances",
      description: "List EC2 instances with their status",
      inputSchema: {
        type: "object",
        properties: {
          filters: {
            type: "array",
            items: {
              type: "object",
              properties: {
                Name: { type: "string" },
                Values: { type: "array", items: { type: "string" } },
              },
            },
          },
        },
      },
    },
    {
      name: "start_ec2_instance",
      description: "Start an EC2 instance",
      inputSchema: {
        type: "object",
        properties: {
          instanceId: { type: "string" },
        },
        required: ["instanceId"],
      },
    },
    {
      name: "stop_ec2_instance",
      description: "Stop an EC2 instance",
      inputSchema: {
        type: "object",
        properties: {
          instanceId: { type: "string" },
        },
        required: ["instanceId"],
      },
    },
    {
      name: "list_s3_buckets",
      description: "List S3 buckets",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "get_cloudwatch_metric",
      description: "Get CloudWatch metrics",
      inputSchema: {
        type: "object",
        properties: {
          namespace: { type: "string", description: "e.g., AWS/EC2" },
          metricName: { type: "string", description: "e.g., CPUUtilization" },
          dimensions: {
            type: "array",
            items: {
              type: "object",
              properties: {
                Name: { type: "string" },
                Value: { type: "string" },
              },
            },
          },
          period: { type: "number", default: 300 },
          hoursBack: { type: "number", default: 1 },
        },
        required: ["namespace", "metricName"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "list_ec2_instances": {
      const command = new DescribeInstancesCommand({
        Filters: args.filters,
      });
      const response = await ec2.send(command);

      const instances = response.Reservations?.flatMap((r) =>
        r.Instances?.map((i) => ({
          instanceId: i.InstanceId,
          state: i.State?.Name,
          type: i.InstanceType,
          publicIp: i.PublicIpAddress,
          privateIp: i.PrivateIpAddress,
          name: i.Tags?.find((t) => t.Key === "Name")?.Value,
        }))
      );

      return {
        content: [
          { type: "text", text: JSON.stringify(instances, null, 2) },
        ],
      };
    }

    case "start_ec2_instance": {
      const command = new StartInstancesCommand({
        InstanceIds: [args.instanceId],
      });
      await ec2.send(command);
      return {
        content: [
          { type: "text", text: `Started instance ${args.instanceId}` },
        ],
      };
    }

    case "get_cloudwatch_metric": {
      const endTime = new Date();
      const startTime = new Date(
        endTime.getTime() - args.hoursBack * 60 * 60 * 1000
      );

      const command = new GetMetricDataCommand({
        StartTime: startTime,
        EndTime: endTime,
        MetricDataQueries: [
          {
            Id: "m1",
            MetricStat: {
              Metric: {
                Namespace: args.namespace,
                MetricName: args.metricName,
                Dimensions: args.dimensions,
              },
              Period: args.period,
              Stat: "Average",
            },
          },
        ],
      });

      const response = await cloudwatch.send(command);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(response.MetricDataResults, null, 2),
          },
        ],
      };
    }

    // ... other tools
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 9.5 MCP Use Cases for DevOps

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

## 9.6 Security Considerations

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

## 9.7 Building a Complete MCP Server

### Project Structure

```bash
# Complete MCP server project structure

my-devops-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts           # Main entry point
│   ├── server.ts          # Server setup
│   ├── tools/
│   │   ├── index.ts       # Tool registry
│   │   ├── kubernetes.ts  # K8s tools
│   │   ├── aws.ts         # AWS tools
│   │   └── monitoring.ts  # Monitoring tools
│   ├── resources/
│   │   ├── index.ts       # Resource registry
│   │   └── cluster-info.ts
│   ├── prompts/
│   │   ├── index.ts       # Prompt registry
│   │   └── debug-pod.ts
│   └── utils/
│       ├── auth.ts        # Authentication helpers
│       ├── logging.ts     # Audit logging
│       └── validation.ts  # Input validation
├── tests/
│   ├── tools.test.ts
│   └── integration.test.ts
└── README.md
```

### Package Configuration

```json
// package.json
{
  "name": "my-devops-mcp-server",
  "version": "1.0.0",
  "description": "DevOps MCP server for Claude Code",
  "main": "dist/index.js",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts",
    "test": "vitest"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "@kubernetes/client-node": "^0.20.0",
    "@aws-sdk/client-ec2": "^3.0.0",
    "@aws-sdk/client-s3": "^3.0.0",
    "@aws-sdk/client-cloudwatch": "^3.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "tsx": "^4.0.0",
    "vitest": "^1.0.0"
  }
}
```

### Complete Server Implementation

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerTools } from "./tools/index.js";
import { registerResources } from "./resources/index.js";
import { registerPrompts } from "./prompts/index.js";
import { setupAuditLogging } from "./utils/logging.js";

async function main() {
  // Create server
  const server = new Server(
    {
      name: "devops-mcp-server",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: {},
        resources: {},
        prompts: {},
      },
    }
  );

  // Setup audit logging
  setupAuditLogging(server);

  // Register all capabilities
  registerTools(server);
  registerResources(server);
  registerPrompts(server);

  // Connect via stdio
  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error("DevOps MCP server started");
}

main().catch(console.error);
```

```typescript
// src/tools/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { kubernetesTools, handleKubernetes } from "./kubernetes.js";
import { awsTools, handleAWS } from "./aws.js";
import { monitoringTools, handleMonitoring } from "./monitoring.js";

export function registerTools(server: Server) {
  // List all tools
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      ...kubernetesTools,
      ...awsTools,
      ...monitoringTools,
    ],
  }));

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    // Route to appropriate handler
    if (name.startsWith("k8s_")) {
      return handleKubernetes(name, args);
    }
    if (name.startsWith("aws_")) {
      return handleAWS(name, args);
    }
    if (name.startsWith("mon_")) {
      return handleMonitoring(name, args);
    }

    throw new Error(`Unknown tool: ${name}`);
  });
}
```

---

## 9.8 Hands-On Exercises

### Exercise 1: Set Up Official MCP Servers

```bash
# Configure and test official MCP servers

# 1. Create MCP configuration
mkdir -p ~/.claude
cat > ~/.claude/mcp_servers.json << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp/mcp-test"]
    }
  }
}
EOF

# 2. Create test directory
mkdir -p /tmp/mcp-test
echo "Hello MCP" > /tmp/mcp-test/test.txt

# 3. Start Claude Code and test
claude
> List files in the MCP filesystem
> Read the test.txt file
> Create a new file called hello.txt with content "MCP works!"

# 4. Verify the file was created
cat /tmp/mcp-test/hello.txt
```

### Exercise 2: Build a Simple MCP Server

```typescript
// Create a simple "system info" MCP server

// 1. Create project
// mkdir system-info-mcp && cd system-info-mcp
// npm init -y
// npm install @modelcontextprotocol/sdk

// 2. Create src/index.ts with these tools:
// - get_cpu_usage: Returns current CPU usage
// - get_memory_usage: Returns memory stats
// - get_disk_usage: Returns disk space
// - get_uptime: Returns system uptime

// 3. Test with Claude Code:
// - Add to mcp_servers.json
// - Start Claude and ask about system info

// Starter code:
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { execSync } from "child_process";
import os from "os";

const server = new Server(
  { name: "system-info", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Implement the tools...
// Your code here
```

### Exercise 3: Create a DevOps MCP Server

```markdown
# Build a complete DevOps MCP server

## Requirements:
1. Tools:
   - check_port: Check if a port is open
   - ping_host: Ping a hostname
   - get_docker_containers: List Docker containers
   - get_docker_logs: Get container logs
   - check_ssl_cert: Check SSL certificate expiry

2. Resources:
   - system://info: System information
   - docker://stats: Docker statistics

3. Prompts:
   - debug_connectivity: Template for debugging network issues

## Steps:
1. Create project structure
2. Implement each tool
3. Add to Claude Code configuration
4. Test all functionality
5. Add audit logging
```

---

## 9.9 Chapter Summary

### Key Takeaways

1. **MCP is a universal protocol** - Standardizes how AI connects to external services

2. **Three primitives** - Tools (actions), Resources (data), Prompts (templates)

3. **Claude Code has built-in MCP client** - Just configure servers in JSON

4. **Build custom servers** - Extend Claude's capabilities for your infrastructure

5. **Security matters** - Follow least privilege, audit logs, protect credentials

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│                    MCP QUICK REFERENCE                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Configuration:                                                │
│  ~/.claude/mcp_servers.json                                    │
│                                                                │
│  Official Servers:                                             │
│  @modelcontextprotocol/server-filesystem                       │
│  @modelcontextprotocol/server-github                           │
│  @modelcontextprotocol/server-postgres                         │
│  @modelcontextprotocol/server-slack                            │
│                                                                │
│  Building Servers:                                             │
│  npm install @modelcontextprotocol/sdk                         │
│                                                                │
│  Key Concepts:                                                 │
│  • Tools = Functions Claude can call                           │
│  • Resources = Data Claude can read                            │
│  • Prompts = Templates for common tasks                        │
│                                                                │
│  Transport:                                                    │
│  • stdio (recommended for local)                               │
│  • HTTP/SSE (for remote servers)                               │
│                                                                │
│  Security:                                                     │
│  • Use environment variables for secrets                       │
│  • Apply least privilege principle                             │
│  • Enable audit logging                                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: Claude Code Professional](./08-claude-code-professional.md) | [Next: AI for DevOps →](./10-ai-for-devops.md)
