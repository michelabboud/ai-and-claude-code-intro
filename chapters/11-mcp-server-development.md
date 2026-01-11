# Chapter 11: MCP Server Development

**Part 4: MCP Integration**

---

## Navigation

← Previous: [Chapter 10: MCP Fundamentals](./10-mcp-fundamentals.md) | Next: [Chapter 12: AI for DevOps](./12-ai-for-devops.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---


## Building Custom Integrations for Your Tools

**📖 Reading time:** ~9 minutes | **⚙️ Hands-on time:** ~60 minutes
**🎯 Quick nav:** [Building Servers](#111-building-custom-mcp-servers) | [Complete Examples](#112-building-a-complete-mcp-server) | [🏋️ Skip to Exercises](#113-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** Building custom MCP servers lets you integrate Claude Code with ANY tool or data source your team uses. This chapter teaches you to create production-ready MCP servers in TypeScript or Python.

**Key concepts:**
- **MCP servers** = Simple Node/Python apps that expose tools and resources
- **Development** = Use @modelcontextprotocol/sdk (TS) or mcp package (Python)
- **Structure** = Initialize server → Define tools/resources → Handle requests → Return results
- **Testing** = Use MCP inspector and local testing before deployment
- **Examples provided** = Kubernetes MCP server, AWS MCP server (complete working code)

**Most important takeaway:** You're not limited to pre-built servers. Build custom integrations for your internal tools, databases, APIs - give Claude Code access to your entire infrastructure.

**Hands-on:** [Jump to exercises](#113-hands-on-exercises) to build your first MCP server for a tool you actually use.

---

*💡 Want to build custom integrations? Keep reading!*

---

This chapter teaches you to build custom MCP servers, turning any tool or system into a Claude Code integration.

---

## 11.1 Building Custom MCP Servers

### When to Build a Custom MCP Server

Understanding when to build custom vs use existing servers saves significant development time. Here's the decision framework.

#### Decision Matrix: Build vs Use Existing

| Factor | Use Existing Server | Build Custom Server |
|--------|-------------------|---------------------|
| **Tool has public server** | Yes (github.com/modelcontextprotocol/servers) | N/A |
| **Tool is popular** | Likely exists, search first | Only if no match |
| **Internal/proprietary tool** | N/A | Required |
| **Specific workflow** | Existing might not fit | Tailored to your needs |
| **Team resources** | Low dev time | 4-8 hours initial + maintenance |
| **Security requirements** | Trust third-party code | Full control |
| **Complexity** | Tool has 20+ operations | Tool has 3-5 operations |

#### Real-World Decision Examples

**Example 1: GitHub Integration**

```yaml
Situation: Need GitHub PR review capabilities

Decision: USE EXISTING
Reason:
  - Official @modelcontextprotocol/server-github exists
  - Well-maintained by Anthropic
  - Handles authentication, rate limiting
  - Covers 90% of use cases

Action:
  npm install @modelcontextprotocol/server-github
  # Configure in claude_desktop_config.json

Time saved: 8-12 hours development
```

**Example 2: Internal Deployment System**

```yaml
Situation: Your company's custom deployment tool ("DeployMaster")

Decision: BUILD CUSTOM
Reason:
  - No public server exists (internal tool)
  - Specific to your workflows
  - Needs company SSO integration
  - Only 5 operations needed: deploy, rollback, status, logs, approve

Action:
  - Create MCP server (4-6 hours)
  - Expose 5 tools
  - Connect to DeployMaster API

Time investment: 6 hours initial, 1 hour/month maintenance
Value: Team of 10 saves 30 min/week each = 130 hours/year saved
```

**Example 3: Kubernetes Management**

```yaml
Situation: Need Kubernetes cluster operations

Decision: EVALUATE THEN DECIDE

Step 1: Check existing servers
  - Search: github.com/modelcontextprotocol/servers
  - Search: "kubernetes mcp server" on GitHub
  - Result: Maybe community servers exist

Step 2: Evaluate existing vs custom
  Existing server pros:
    ✅ Saves development time
    ❌ May not have your specific operations
    ❌ Might not follow your security model

  Custom server pros:
    ✅ Exactly the operations you need
    ✅ Integrates with your auth system
    ❌ Takes time to build and maintain

Step 3: Make informed decision
  If existing covers 80%+ of needs → Use existing
  If custom workflows critical → Build custom
```

#### The "Minimum Viable MCP Server" Approach

Don't build everything at once. Start small and expand based on actual usage.

```yaml
Phase 1: Core Operations (Week 1)
  Build 3-5 most common operations
  Example for AWS:
    - list_ec2_instances
    - describe_instance
    - get_cloudwatch_metrics

  Goal: Usable, not complete
  Time: 4-6 hours

Phase 2: Feedback & Expansion (Weeks 2-4)
  Track what team asks AI to do
  Add operations for frequent requests
  Example additions:
    - start_instance
    - stop_instance
    - update_tags

  Goal: Cover 90% of use cases
  Time: 2-3 hours per addition

Phase 3: Polish (Month 2+)
  Add error handling edge cases
  Improve response formatting
  Add caching for expensive operations
  Documentation

  Goal: Production-ready
  Time: 4-8 hours
```

#### Common Mistakes in Server Development

**Mistake 1: Building Too Much Upfront**

```yaml
❌ Bad approach:
  "I'll build a complete AWS management server with all services!"

  Result:
    - 3 weeks of development
    - 50+ tools implemented
    - Team only uses 5 of them
    - Maintenance burden

✅ Good approach:
  "I'll build tools for the AWS services we actually use daily"

  Result:
    - 1 day of development
    - 5 carefully chosen tools
    - High adoption
    - Easy to maintain
```

**Mistake 2: Not Considering Existing Solutions**

```yaml
❌ Bad approach:
  Jump straight to building custom server

✅ Good approach:
  1. Search for existing servers (5 minutes)
  2. Test if existing meets 80%+ of needs (30 minutes)
  3. If yes: use existing, contribute improvements if needed
  4. If no: build custom for the gaps

Time saved: Hours to days
```

**Mistake 3: No Security Consideration**

```yaml
❌ Dangerous:
  MCP server with full AWS admin permissions
  No audit logging
  No input validation

✅ Secure:
  MCP server with least-privilege IAM role
  All operations logged
  Input validated and sanitized
  Read-only operations by default
  Write operations require confirmation

Security is not optional for production!
```

#### Quick Decision Flowchart

```
Need tool integration?
│
├─ Popular tool (GitHub, GitLab, Jira)?
│  └─ Search existing servers → Likely exists → USE EXISTING
│
├─ Internal/proprietary tool?
│  └─ Must BUILD CUSTOM
│
└─ Standard tool (AWS, Kubernetes, Docker)?
   ├─ Check community servers
   ├─ Evaluate fit
   └─ If 80%+ match → USE/EXTEND EXISTING
      If <80% match → BUILD CUSTOM
```

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

## 11.2 Building a Complete MCP Server

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


---

## 11.3 Hands-On Exercises

### Exercise 1: Build a Simple MCP Server

```typescript
// Create a basic MCP server for a custom tool

// 1. Set up project
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk

// 2. Create server (server.ts)
// See Chapter 11 §11.1 for complete code example

// 3. Test locally
npx tsx server.ts

// 4. Configure in Claude Code
// Add to ~/.claude/mcp_servers.json
{
  "my-tool": {
    "command": "npx",
    "args": ["tsx", "/path/to/my-mcp-server/server.ts"]
  }
}

// 5. Use in Claude Code
claude
> Use my custom tool
```

### Exercise 2: Build a DevOps MCP Server

```typescript
// Create an MCP server for your infrastructure

// Choose one to implement:
// A) Internal API integration
// B) Custom database queries  
// C) Monitoring system integration
// D) Deployment automation tools

// Follow the patterns in Chapter 11 §11.2
// - Kubernetes MCP Server example
// - AWS MCP Server example

// Add features like:
// - List resources
// - Query status
// - Execute operations (with safety checks)
// - Health monitoring
```

### Exercise 3: Publish and Share

```bash
# Package your MCP server for sharing

# 1. Add proper error handling
# 2. Write documentation (README.md)
# 3. Add examples and tests
# 4. Publish to npm (optional)
npm publish

# 5. Share configuration with team
# Document in team wiki or README
```

---

## 11.4 Chapter Summary

### Key Takeaways

1. **Building MCP servers is straightforward**
   - Use @modelcontextprotocol/sdk (TypeScript) or mcp (Python)
   - Implement handlers for tools and resources
   - Return structured responses
   - Test locally before deploying

2. **MCP servers unlock infinite possibilities**
   - Integrate any tool or API
   - Access internal databases
   - Control infrastructure
   - Automate workflows

3. **Complete examples provided**
   - Kubernetes MCP server (production-ready)
   - AWS MCP server (full implementation)
   - Copy, adapt, extend for your needs

4. **Best practices matter**
   - Implement proper error handling
   - Add authentication/authorization
   - Log operations for audit
   - Test thoroughly

### Next Steps

- [Chapter 12: AI for DevOps](./12-ai-for-devops.md) - Real-world applications
- Build an MCP server for your most-used tool
- Share with your team
- Contribute to the MCP ecosystem

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0

---

## Navigation

← Previous: [Chapter 10: MCP Fundamentals](./10-mcp-fundamentals.md) | Next: [Chapter 12: AI for DevOps](./12-ai-for-devops.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 11** | MCP Server Development | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
