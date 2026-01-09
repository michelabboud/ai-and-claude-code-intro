/**
 * Chapter 9: MCP Deep Dive
 * Kubernetes MCP Server Implementation
 *
 * This server provides Kubernetes management capabilities to Claude Code.
 *
 * Installation:
 *   npm install @modelcontextprotocol/sdk @kubernetes/client-node
 *
 * Usage:
 *   Add to ~/.claude/mcp_servers.json:
 *   {
 *     "kubernetes": {
 *       "command": "npx",
 *       "args": ["tsx", "path/to/kubernetes-mcp-server.ts"]
 *     }
 *   }
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import * as k8s from "@kubernetes/client-node";

// Initialize Kubernetes client
const kc = new k8s.KubeConfig();
kc.loadFromDefault();
const coreApi = kc.makeApiClient(k8s.CoreV1Api);
const appsApi = kc.makeApiClient(k8s.AppsV1Api);

// Create MCP server
const server = new Server(
  {
    name: "kubernetes-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// =============================================================================
// TOOLS DEFINITION
// =============================================================================

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_pods",
      description: "List pods in a namespace with status information",
      inputSchema: {
        type: "object",
        properties: {
          namespace: {
            type: "string",
            description: "Kubernetes namespace",
            default: "default",
          },
          labelSelector: {
            type: "string",
            description: "Label selector (e.g., app=nginx)",
          },
        },
      },
    },
    {
      name: "get_pod_logs",
      description: "Get logs from a specific pod",
      inputSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "Pod name",
          },
          namespace: {
            type: "string",
            description: "Kubernetes namespace",
            default: "default",
          },
          container: {
            type: "string",
            description: "Container name (if pod has multiple containers)",
          },
          tailLines: {
            type: "number",
            description: "Number of lines to fetch from end",
            default: 100,
          },
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
          namespace: {
            type: "string",
            description: "Kubernetes namespace",
            default: "default",
          },
        },
      },
    },
    {
      name: "scale_deployment",
      description: "Scale a deployment to specified replicas",
      inputSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "Deployment name",
          },
          namespace: {
            type: "string",
            description: "Kubernetes namespace",
            default: "default",
          },
          replicas: {
            type: "number",
            description: "Desired number of replicas",
          },
        },
        required: ["name", "replicas"],
      },
    },
    {
      name: "describe_pod",
      description: "Get detailed information about a pod",
      inputSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "Pod name",
          },
          namespace: {
            type: "string",
            description: "Kubernetes namespace",
            default: "default",
          },
        },
        required: ["name"],
      },
    },
    {
      name: "get_events",
      description: "Get recent events in a namespace",
      inputSchema: {
        type: "object",
        properties: {
          namespace: {
            type: "string",
            description: "Kubernetes namespace",
            default: "default",
          },
          limit: {
            type: "number",
            description: "Maximum number of events to return",
            default: 20,
          },
        },
      },
    },
  ],
}));

// =============================================================================
// TOOLS IMPLEMENTATION
// =============================================================================

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "get_pods": {
      const namespace = (args?.namespace as string) || "default";
      const labelSelector = args?.labelSelector as string | undefined;

      const response = await coreApi.listNamespacedPod(
        namespace,
        undefined,
        undefined,
        undefined,
        undefined,
        labelSelector
      );

      const pods = response.body.items.map((pod) => ({
        name: pod.metadata?.name,
        namespace: pod.metadata?.namespace,
        status: pod.status?.phase,
        ready: pod.status?.conditions?.find((c) => c.type === "Ready")?.status,
        restarts: pod.status?.containerStatuses?.[0]?.restartCount || 0,
        age: pod.metadata?.creationTimestamp,
        ip: pod.status?.podIP,
        node: pod.spec?.nodeName,
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(pods, null, 2),
          },
        ],
      };
    }

    case "get_pod_logs": {
      const podName = args?.name as string;
      const namespace = (args?.namespace as string) || "default";
      const container = args?.container as string | undefined;
      const tailLines = (args?.tailLines as number) || 100;

      const response = await coreApi.readNamespacedPodLog(
        podName,
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
        content: [
          {
            type: "text",
            text: response.body,
          },
        ],
      };
    }

    case "get_deployments": {
      const namespace = (args?.namespace as string) || "default";

      const response = await appsApi.listNamespacedDeployment(namespace);

      const deployments = response.body.items.map((dep) => ({
        name: dep.metadata?.name,
        namespace: dep.metadata?.namespace,
        replicas: {
          desired: dep.spec?.replicas,
          ready: dep.status?.readyReplicas || 0,
          available: dep.status?.availableReplicas || 0,
        },
        strategy: dep.spec?.strategy?.type,
        age: dep.metadata?.creationTimestamp,
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(deployments, null, 2),
          },
        ],
      };
    }

    case "scale_deployment": {
      const deployName = args?.name as string;
      const namespace = (args?.namespace as string) || "default";
      const replicas = args?.replicas as number;

      const patch = { spec: { replicas } };

      await appsApi.patchNamespacedDeploymentScale(
        deployName,
        namespace,
        patch,
        undefined,
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
            text: `Successfully scaled deployment ${deployName} to ${replicas} replicas`,
          },
        ],
      };
    }

    case "describe_pod": {
      const podName = args?.name as string;
      const namespace = (args?.namespace as string) || "default";

      const response = await coreApi.readNamespacedPod(podName, namespace);
      const pod = response.body;

      const description = {
        name: pod.metadata?.name,
        namespace: pod.metadata?.namespace,
        labels: pod.metadata?.labels,
        annotations: pod.metadata?.annotations,
        status: {
          phase: pod.status?.phase,
          conditions: pod.status?.conditions,
          containerStatuses: pod.status?.containerStatuses,
        },
        spec: {
          nodeName: pod.spec?.nodeName,
          serviceAccount: pod.spec?.serviceAccountName,
          containers: pod.spec?.containers?.map((c) => ({
            name: c.name,
            image: c.image,
            ports: c.ports,
            resources: c.resources,
            env: c.env?.length || 0,
          })),
        },
      };

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(description, null, 2),
          },
        ],
      };
    }

    case "get_events": {
      const namespace = (args?.namespace as string) || "default";
      const limit = (args?.limit as number) || 20;

      const response = await coreApi.listNamespacedEvent(
        namespace,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        limit
      );

      const events = response.body.items
        .sort(
          (a, b) =>
            new Date(b.lastTimestamp || "").getTime() -
            new Date(a.lastTimestamp || "").getTime()
        )
        .slice(0, limit)
        .map((event) => ({
          type: event.type,
          reason: event.reason,
          message: event.message,
          object: `${event.involvedObject?.kind}/${event.involvedObject?.name}`,
          count: event.count,
          lastSeen: event.lastTimestamp,
        }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(events, null, 2),
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// =============================================================================
// RESOURCES DEFINITION
// =============================================================================

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
    {
      uri: "k8s://cluster-info",
      name: "Cluster Information",
      description: "General cluster information",
      mimeType: "application/json",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "k8s://namespaces") {
    const response = await coreApi.listNamespace();
    const namespaces = response.body.items.map((ns) => ({
      name: ns.metadata?.name,
      status: ns.status?.phase,
      age: ns.metadata?.creationTimestamp,
    }));

    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(namespaces, null, 2),
        },
      ],
    };
  }

  if (uri === "k8s://nodes") {
    const response = await coreApi.listNode();
    const nodes = response.body.items.map((node) => ({
      name: node.metadata?.name,
      status: node.status?.conditions?.find((c) => c.type === "Ready")?.status,
      capacity: node.status?.capacity,
      allocatable: node.status?.allocatable,
      version: node.status?.nodeInfo?.kubeletVersion,
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

  if (uri === "k8s://cluster-info") {
    const info = {
      context: kc.getCurrentContext(),
      cluster: kc.getCurrentCluster()?.name,
      server: kc.getCurrentCluster()?.server,
    };

    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(info, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// =============================================================================
// START SERVER
// =============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Kubernetes MCP server running");
}

main().catch(console.error);
