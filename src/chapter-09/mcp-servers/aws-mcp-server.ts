/**
 * Chapters 10-11: MCP (Model Context Protocol)
 * AWS MCP Server Implementation
 *
 * This server provides AWS management capabilities to Claude Code.
 *
 * Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
 * Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
 * Copyright: © 2026 Michel Abboud. All rights reserved.
 * License: CC BY-NC 4.0
 *
 * Installation:
 *   npm install @modelcontextprotocol/sdk @aws-sdk/client-ec2 @aws-sdk/client-s3 @aws-sdk/client-cloudwatch
 *
 * Usage:
 *   Add to ~/.claude/mcp_servers.json:
 *   {
 *     "aws": {
 *       "command": "npx",
 *       "args": ["tsx", "path/to/aws-mcp-server.ts"],
 *       "env": {
 *         "AWS_PROFILE": "production"
 *       }
 *     }
 *   }
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import {
  EC2Client,
  DescribeInstancesCommand,
  StartInstancesCommand,
  StopInstancesCommand,
  DescribeSecurityGroupsCommand,
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

// Initialize AWS clients
const ec2 = new EC2Client({});
const s3 = new S3Client({});
const cloudwatch = new CloudWatchClient({});

// Create MCP server
const server = new Server(
  {
    name: "aws-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// =============================================================================
// TOOLS DEFINITION
// =============================================================================

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    // EC2 Tools
    {
      name: "list_ec2_instances",
      description: "List EC2 instances with their status",
      inputSchema: {
        type: "object",
        properties: {
          filters: {
            type: "array",
            description: "Filters to apply (e.g., tag:Environment=production)",
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
      description: "Start a stopped EC2 instance",
      inputSchema: {
        type: "object",
        properties: {
          instanceId: {
            type: "string",
            description: "EC2 instance ID (e.g., i-1234567890abcdef0)",
          },
        },
        required: ["instanceId"],
      },
    },
    {
      name: "stop_ec2_instance",
      description: "Stop a running EC2 instance",
      inputSchema: {
        type: "object",
        properties: {
          instanceId: {
            type: "string",
            description: "EC2 instance ID",
          },
        },
        required: ["instanceId"],
      },
    },
    {
      name: "list_security_groups",
      description: "List security groups and their rules",
      inputSchema: {
        type: "object",
        properties: {
          vpcId: {
            type: "string",
            description: "VPC ID to filter by",
          },
        },
      },
    },

    // S3 Tools
    {
      name: "list_s3_buckets",
      description: "List all S3 buckets",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
    {
      name: "list_s3_objects",
      description: "List objects in an S3 bucket",
      inputSchema: {
        type: "object",
        properties: {
          bucket: {
            type: "string",
            description: "Bucket name",
          },
          prefix: {
            type: "string",
            description: "Object prefix filter",
          },
          maxKeys: {
            type: "number",
            description: "Maximum number of objects to return",
            default: 100,
          },
        },
        required: ["bucket"],
      },
    },

    // CloudWatch Tools
    {
      name: "get_cloudwatch_metric",
      description: "Get CloudWatch metrics for analysis",
      inputSchema: {
        type: "object",
        properties: {
          namespace: {
            type: "string",
            description: "CloudWatch namespace (e.g., AWS/EC2, AWS/RDS)",
          },
          metricName: {
            type: "string",
            description: "Metric name (e.g., CPUUtilization)",
          },
          dimensions: {
            type: "array",
            description: "Dimensions to filter by",
            items: {
              type: "object",
              properties: {
                Name: { type: "string" },
                Value: { type: "string" },
              },
            },
          },
          period: {
            type: "number",
            description: "Period in seconds",
            default: 300,
          },
          hoursBack: {
            type: "number",
            description: "How many hours of data to fetch",
            default: 1,
          },
        },
        required: ["namespace", "metricName"],
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
    // EC2 Tools
    case "list_ec2_instances": {
      const command = new DescribeInstancesCommand({
        Filters: args?.filters as any[],
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
          launchTime: i.LaunchTime,
          availabilityZone: i.Placement?.AvailabilityZone,
        }))
      );

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(instances, null, 2),
          },
        ],
      };
    }

    case "start_ec2_instance": {
      const instanceId = args?.instanceId as string;
      const command = new StartInstancesCommand({
        InstanceIds: [instanceId],
      });
      await ec2.send(command);

      return {
        content: [
          {
            type: "text",
            text: `Started instance ${instanceId}. It may take a few minutes to become available.`,
          },
        ],
      };
    }

    case "stop_ec2_instance": {
      const instanceId = args?.instanceId as string;
      const command = new StopInstancesCommand({
        InstanceIds: [instanceId],
      });
      await ec2.send(command);

      return {
        content: [
          {
            type: "text",
            text: `Stopping instance ${instanceId}.`,
          },
        ],
      };
    }

    case "list_security_groups": {
      const filters = args?.vpcId
        ? [{ Name: "vpc-id", Values: [args.vpcId as string] }]
        : undefined;

      const command = new DescribeSecurityGroupsCommand({ Filters: filters });
      const response = await ec2.send(command);

      const groups = response.SecurityGroups?.map((sg) => ({
        groupId: sg.GroupId,
        groupName: sg.GroupName,
        description: sg.Description,
        vpcId: sg.VpcId,
        inboundRules: sg.IpPermissions?.length || 0,
        outboundRules: sg.IpPermissionsEgress?.length || 0,
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(groups, null, 2),
          },
        ],
      };
    }

    // S3 Tools
    case "list_s3_buckets": {
      const command = new ListBucketsCommand({});
      const response = await s3.send(command);

      const buckets = response.Buckets?.map((b) => ({
        name: b.Name,
        creationDate: b.CreationDate,
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(buckets, null, 2),
          },
        ],
      };
    }

    case "list_s3_objects": {
      const bucket = args?.bucket as string;
      const prefix = args?.prefix as string | undefined;
      const maxKeys = (args?.maxKeys as number) || 100;

      const command = new ListObjectsV2Command({
        Bucket: bucket,
        Prefix: prefix,
        MaxKeys: maxKeys,
      });
      const response = await s3.send(command);

      const objects = response.Contents?.map((obj) => ({
        key: obj.Key,
        size: obj.Size,
        lastModified: obj.LastModified,
        storageClass: obj.StorageClass,
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                bucket,
                count: objects?.length || 0,
                isTruncated: response.IsTruncated,
                objects,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    // CloudWatch Tools
    case "get_cloudwatch_metric": {
      const namespace = args?.namespace as string;
      const metricName = args?.metricName as string;
      const dimensions = args?.dimensions as
        | { Name: string; Value: string }[]
        | undefined;
      const period = (args?.period as number) || 300;
      const hoursBack = (args?.hoursBack as number) || 1;

      const endTime = new Date();
      const startTime = new Date(endTime.getTime() - hoursBack * 60 * 60 * 1000);

      const command = new GetMetricDataCommand({
        StartTime: startTime,
        EndTime: endTime,
        MetricDataQueries: [
          {
            Id: "m1",
            MetricStat: {
              Metric: {
                Namespace: namespace,
                MetricName: metricName,
                Dimensions: dimensions,
              },
              Period: period,
              Stat: "Average",
            },
          },
        ],
      });

      const response = await cloudwatch.send(command);

      const result = {
        metric: `${namespace}/${metricName}`,
        period,
        startTime: startTime.toISOString(),
        endTime: endTime.toISOString(),
        dataPoints: response.MetricDataResults?.[0]?.Timestamps?.map(
          (ts, i) => ({
            timestamp: ts,
            value: response.MetricDataResults?.[0]?.Values?.[i],
          })
        ),
      };

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// =============================================================================
// START SERVER
// =============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("AWS MCP server running");
}

main().catch(console.error);
