# Chapter 13: n8n Fundamentals

## Low-Code Workflow Automation for DevOps

**📖 Reading time:** ~14 minutes | **⚙️ Hands-on time:** ~45 minutes
**🎯 Quick nav:** [What is n8n?](#131-what-is-n8n) | [Installation](#132-installation--setup) | [Core Concepts](#133-core-concepts) | [First Workflow](#134-building-your-first-workflow) | [Essential Nodes](#135-essential-nodes-for-devops) | [Examples](#136-devops-workflow-examples) | [🏋️ Skip to Exercises](#138-hands-on-exercises)

---

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** n8n is a powerful open-source workflow automation tool that lets you connect different services and automate tasks without writing extensive code. Think of it as "Zapier for DevOps" but self-hosted, extendable, and perfect for technical users.

**Key concepts:**
- **n8n** = Low-code workflow automation platform (node-based visual builder)
- **Self-hosted** = Full control, no vendor lock-in, unlimited executions
- **Workflows** = Connected nodes that trigger on events and perform actions
- **Nodes** = Pre-built integrations (300+ available: GitHub, Slack, AWS, databases, etc.)
- **Perfect for DevOps** = Incident response, deployment automation, monitoring alerts, PR workflows

**Most important takeaway:** n8n bridges the gap between manual DevOps tasks and full custom development. Automate in hours what would take days to code, while maintaining full control and flexibility.

**Hands-on:** [Jump to exercises](#138-hands-on-exercises) to install n8n and build your first three DevOps workflows.

---

*💡 Want the complete guide? Keep reading. Ready to automate? Jump to exercises!*

---

This chapter introduces n8n and teaches you to build practical workflow automations for DevOps tasks.

---

## 13.1 What is n8n?

### The Automation Gap

DevOps engineers face a common challenge:

```
┌────────────────────────────────────────────────────────────────┐
│                    THE AUTOMATION GAP                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Manual Tasks                                                  │
│  ├── Time-consuming                                            │
│  ├── Error-prone                                               │
│  ├── Not scalable                                              │
│  └── Example: Manually checking GitHub, updating Jira,        │
│               posting to Slack for every incident              │
│                                                                │
│  vs.                                                           │
│                                                                │
│  Custom Scripts                                                │
│  ├── Requires development time                                 │
│  ├── Needs maintenance                                         │
│  ├── Hard to share/modify                                      │
│  └── Example: Writing Python scripts with API clients,        │
│               error handling, logging, etc.                    │
│                                                                │
│  ↓↓↓ n8n fills this gap ↓↓↓                                    │
│                                                                │
│  n8n Workflows                                                 │
│  ├── Visual, low-code automation                              │
│  ├── Pre-built integrations (300+ services)                    │
│  ├── Easy to create, modify, share                            │
│  ├── Full code when needed (JavaScript/Python nodes)          │
│  └── Example: Drag-and-drop workflow in 10 minutes            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### What is n8n?

**n8n** (short for "nodemation" - **n**ode autom**ation**) is an open-source workflow automation tool that connects different services and automates tasks through a visual, node-based interface.

```yaml
# n8n in simple terms

what_it_is:
  description: "Visual workflow automation platform"
  model: "Low-code with full code escape hatches"
  architecture: "Node-based workflows"

key_features:
  - "300+ pre-built integrations (nodes)"
  - "Self-hosted (Docker, K8s, npm)"
  - "Open source (Apache 2.0 license)"
  - "Fair-code model (free for most uses)"
  - "Visual workflow editor"
  - "Code nodes for custom logic"
  - "API access for everything"

why_for_devops:
  control: "Self-hosted = full data control"
  flexibility: "Extend with custom nodes"
  cost: "Unlimited executions (vs. SaaS limits)"
  integration: "API-first design, works with everything"
  transparency: "Open source = audit, modify, contribute"
```

### n8n vs. Alternatives

| Feature | n8n | Zapier | Make (Integromat) | Custom Scripts |
|---------|-----|--------|-------------------|----------------|
| **Self-hosted** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Open source** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Cost** | 💰 Free (self-hosted) | 💰💰💰 Expensive | 💰💰 Moderate | 💰 Server costs only |
| **Execution limits** | ♾️ Unlimited | ⚠️ Limited by plan | ⚠️ Limited by plan | ♾️ Unlimited |
| **Code access** | ✅ Full | ❌ Limited | ❌ Limited | ✅ Full |
| **Visual editor** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Pre-built nodes** | 300+ | 5000+ | 1000+ | 0 (DIY) |
| **Learning curve** | 📚 Moderate | 📖 Easy | 📚 Moderate | 📚📚 Steep |
| **DevOps friendly** | ✅✅✅ | ✅ | ✅✅ | ✅✅✅ |

**Bottom line**: n8n gives you the best of both worlds - visual automation like SaaS tools, with the control and flexibility of custom scripts.

---

## 13.2 Installation & Setup

### Deployment Options

n8n offers multiple deployment methods:

#### Option 1: Docker (Recommended for Testing)

```bash
# Quick start with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Access at: http://localhost:5678
```

#### Option 2: Docker Compose (Recommended for Production)

```yaml
# docker-compose.yml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=change_this_password
      - N8N_HOST=n8n.yourdomain.com
      - N8N_PROTOCOL=https
      - NODE_ENV=production
      - WEBHOOK_URL=https://n8n.yourdomain.com/
      - GENERIC_TIMEZONE=America/New_York
    volumes:
      - ./n8n_data:/home/node/.n8n
      - ./local_files:/files
    # Optional: Use PostgreSQL for production
    # depends_on:
    #   - postgres

  # Optional: PostgreSQL database
  # postgres:
  #   image: postgres:15-alpine
  #   restart: unless-stopped
  #   environment:
  #     - POSTGRES_USER=n8n
  #     - POSTGRES_PASSWORD=n8n
  #     - POSTGRES_DB=n8n
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data

# volumes:
#   postgres_data:
```

```bash
# Start n8n
docker-compose up -d

# View logs
docker-compose logs -f n8n
```

#### Option 3: Kubernetes (Production)

```yaml
# n8n-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n
  namespace: automation
spec:
  replicas: 1
  selector:
    matchLabels:
      app: n8n
  template:
    metadata:
      labels:
        app: n8n
    spec:
      containers:
      - name: n8n
        image: n8nio/n8n:latest
        ports:
        - containerPort: 5678
        env:
        - name: N8N_BASIC_AUTH_ACTIVE
          value: "true"
        - name: N8N_BASIC_AUTH_USER
          valueFrom:
            secretKeyRef:
              name: n8n-auth
              key: username
        - name: N8N_BASIC_AUTH_PASSWORD
          valueFrom:
            secretKeyRef:
              name: n8n-auth
              key: password
        volumeMounts:
        - name: n8n-data
          mountPath: /home/node/.n8n
      volumes:
      - name: n8n-data
        persistentVolumeClaim:
          claimName: n8n-data-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: n8n-service
  namespace: automation
spec:
  selector:
    app: n8n
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5678
  type: LoadBalancer
```

```bash
# Deploy to Kubernetes
kubectl apply -f n8n-deployment.yaml
```

#### Option 4: n8n Cloud

For teams who want hosted n8n with zero infrastructure management:

```
Visit: https://n8n.cloud
- Managed hosting
- Automatic updates
- Built-in SSL
- Starts at $20/month
```

### Initial Configuration

Once n8n is running:

1. **Access the interface**: `http://localhost:5678`
2. **Create owner account**: First user becomes the owner
3. **Configure credentials**: Set up API keys for services you'll use
4. **Test connection**: Create a simple test workflow

---

## 13.3 Core Concepts

### Workflows

A **workflow** is a connected series of nodes that automate a process.

```
┌────────────────────────────────────────────────────────────────┐
│                     WORKFLOW ANATOMY                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   TRIGGER   │──────>│   PROCESS    │──────>│    ACTION    │  │
│  │             │      │              │      │              │  │
│  │  • Webhook  │      │  • Filter    │      │  • Slack     │  │
│  │  • Schedule │      │  • Transform │      │  • Email     │  │
│  │  • Manual   │      │  • Condition │      │  • API Call  │  │
│  └─────────────┘      └──────────────┘      └──────────────┘  │
│                                                                │
│  Example: "When GitHub webhook fires, check if it's a PR,     │
│            then post message to Slack"                         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Nodes

**Nodes** are the building blocks of workflows:

```yaml
node_types:
  trigger_nodes:
    description: "Start workflow execution"
    examples:
      - "Webhook: Receive HTTP requests"
      - "Schedule: Cron-based triggers"
      - "Manual: Click to start"
      - "On Error: Trigger on workflow errors"

  action_nodes:
    description: "Perform operations"
    examples:
      - "HTTP Request: Call APIs"
      - "Slack: Send messages"
      - "Email: Send emails"
      - "GitHub: Create issues, PRs"
      - "AWS: Manage resources"
      - "Kubernetes: Deploy, scale"

  logic_nodes:
    description: "Control flow and transformation"
    examples:
      - "IF: Conditional branching"
      - "Switch: Multi-way branching"
      - "Code: JavaScript/Python execution"
      - "Function: Data transformation"
      - "Merge: Combine multiple inputs"

  data_nodes:
    description: "Data storage and retrieval"
    examples:
      - "PostgreSQL: Database operations"
      - "MongoDB: Document queries"
      - "Redis: Caching"
      - "Spreadsheet: Google Sheets, Excel"
```

### Credentials

n8n securely manages API keys and authentication:

```yaml
# Credential types

oauth2:
  services: ["GitHub", "Google", "Slack"]
  setup: "OAuth flow in n8n UI"

api_key:
  services: ["AWS", "DataDog", "PagerDuty"]
  setup: "Paste API key in n8n"

basic_auth:
  services: ["Custom APIs", "Jenkins"]
  setup: "Username + password"

custom:
  services: ["Any service"]
  setup: "Define custom credential schema"
```

**Security**: Credentials are encrypted at rest and never exposed in workflow exports.

### Executions

An **execution** is a single run of a workflow:

```yaml
execution_model:
  trigger: "Workflow starts from trigger node"
  flow: "Data passes node-to-node"
  completion: "All nodes execute or error occurs"

execution_data:
  stored: "Input/output data for each node"
  retention: "Configurable (default: all executions)"
  debugging: "View data at each step"
```

---

## 13.4 Building Your First Workflow

### Example: GitHub PR → Slack Notification

Let's build a practical workflow that sends Slack notifications when pull requests are opened.

#### Step 1: Create New Workflow

1. Click **"+ Add workflow"** in n8n
2. Name it: "GitHub PR to Slack"

#### Step 2: Add Trigger (Webhook)

```yaml
# Add Webhook node

1. Search for "Webhook" node
2. Add to canvas
3. Configure:
   - HTTP Method: POST
   - Path: github-pr-webhook
   - Authentication: None (GitHub signs webhooks)
4. Note the webhook URL: https://your-n8n.com/webhook/github-pr-webhook
```

#### Step 3: Filter PR Events

```yaml
# Add IF node to filter only "opened" PRs

1. Add "IF" node
2. Connect from Webhook
3. Configure condition:
   - Value 1: {{$json["action"]}}
   - Operation: Equal
   - Value 2: opened
4. Connect "true" output to next node
```

#### Step 4: Extract PR Data

```yaml
# Add Function node to format data

1. Add "Function" node
2. Connect from IF (true branch)
3. Add JavaScript code:

// Extract PR information
const pr = $input.first().json.pull_request;
const repo = $input.first().json.repository;

return {
  title: pr.title,
  author: pr.user.login,
  url: pr.html_url,
  repo: repo.full_name,
  branch: pr.head.ref
};
```

#### Step 5: Send to Slack

```yaml
# Add Slack node

1. Add "Slack" node
2. Connect from Function
3. Configure credentials (OAuth2)
4. Set up message:
   - Channel: #pull-requests
   - Message:
     🔔 New Pull Request in {{$json["repo"]}}

     *{{$json["title"]}}*
     Author: @{{$json["author"]}}
     Branch: {{$json["branch"]}}

     View PR: {{$json["url"]}}
```

#### Step 6: Test

```bash
# Test with curl
curl -X POST https://your-n8n.com/webhook/github-pr-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "action": "opened",
    "pull_request": {
      "title": "Fix authentication bug",
      "user": {"login": "engineer123"},
      "html_url": "https://github.com/company/repo/pull/42",
      "head": {"ref": "fix-auth"}
    },
    "repository": {
      "full_name": "company/repo"
    }
  }'
```

#### Step 7: Connect to GitHub

```bash
# In GitHub repository settings:
# Settings → Webhooks → Add webhook

Payload URL: https://your-n8n.com/webhook/github-pr-webhook
Content type: application/json
Events: Pull requests
Active: ✓
```

**Done!** Your first automation is live. Every time a PR is opened, your team gets notified in Slack.

---

## 13.5 Essential Nodes for DevOps

### 1. HTTP Request

The Swiss Army knife of n8n - call any API:

```yaml
use_cases:
  - "Trigger deployments (Jenkins, ArgoCD)"
  - "Query monitoring systems (Prometheus, DataDog)"
  - "Update tickets (Jira, Linear)"
  - "Call custom internal APIs"

example_config:
  method: POST
  url: https://jenkins.company.com/job/deploy/build
  authentication: Basic Auth
  body:
    branch: {{$json["branch"]}}
    environment: staging
```

### 2. Schedule Trigger

Cron-based automation:

```yaml
use_cases:
  - "Daily health checks"
  - "Weekly cost reports"
  - "Hourly log cleanup"
  - "Monthly compliance scans"

example_config:
  trigger_times: "0 9 * * 1-5"  # 9 AM weekdays
  timezone: "America/New_York"
```

### 3. Code Node

Full JavaScript/Python for complex logic:

```javascript
// JavaScript example: Analyze log data
const logs = $input.all();

const errors = logs.filter(log =>
  log.json.level === 'ERROR'
);

const errorsByService = errors.reduce((acc, log) => {
  const service = log.json.service;
  acc[service] = (acc[service] || 0) + 1;
  return acc;
}, {});

// Alert if any service has >10 errors
const alerts = Object.entries(errorsByService)
  .filter(([service, count]) => count > 10)
  .map(([service, count]) => ({
    service,
    error_count: count,
    severity: 'high'
  }));

return alerts;
```

### 4. IF/Switch Nodes

Conditional branching:

```yaml
IF_examples:
  - "If error rate > 5%, page on-call"
  - "If deployment succeeded, update status"
  - "If PR from external contributor, require review"

Switch_examples:
  - "Route by environment: dev/staging/prod"
  - "Route by severity: low/medium/high/critical"
  - "Route by service: api/frontend/database"
```

### 5. Wait Node

Delays and polling:

```yaml
use_cases:
  - "Wait for deployment to complete"
  - "Poll API until job finishes"
  - "Rate limit API calls"
  - "Implement retry with backoff"

example:
  resume_on_webhook: true
  webhook_url: "Call this when deployment done"
  timeout: "30 minutes"
```

---

## 13.6 DevOps Workflow Examples

### Example 1: Automated Incident Response

```
┌─────────────────────────────────────────────────────────────┐
│        INCIDENT DETECTION & RESPONSE WORKFLOW               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. [Webhook Trigger]                                       │
│     ↓ (Alert from Prometheus/DataDog)                      │
│  2. [Code Node] Parse alert data                            │
│     ↓                                                       │
│  3. [IF Node] Is severity critical?                         │
│     ↓ true                                                  │
│  4. [PagerDuty] Create incident                             │
│     ↓                                                       │
│  5. [Slack] Post to #incidents channel                      │
│     ↓                                                       │
│  6. [Jira] Create ticket automatically                      │
│     ↓                                                       │
│  7. [HTTP Request] Trigger automated remediation            │
│     ↓                                                       │
│  8. [Wait] Poll for resolution                              │
│     ↓                                                       │
│  9. [Slack] Post resolution update                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Example 2: PR Review Workflow

```
┌─────────────────────────────────────────────────────────────┐
│           PULL REQUEST AUTOMATION WORKFLOW                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. [GitHub Trigger] PR opened                              │
│     ↓                                                       │
│  2. [IF Node] Is external contributor?                      │
│     ↓ true                                                  │
│  3. [GitHub] Add "needs-review" label                       │
│     ↓                                                       │
│  4. [GitHub] Request review from team                       │
│     ↓                                                       │
│  5. [Slack] Notify reviewers                                │
│     ↓                                                       │
│  6. [Wait] Wait for approval webhook                        │
│     ↓ approved                                              │
│  7. [HTTP Request] Trigger CI/CD pipeline                   │
│     ↓                                                       │
│  8. [Wait] Poll build status                                │
│     ↓ success                                               │
│  9. [GitHub] Merge PR                                       │
│     ↓                                                       │
│ 10. [Slack] Post merge notification                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Example 3: Cost Monitoring

```yaml
# Daily AWS cost report workflow

trigger: Schedule (daily at 9 AM)

steps:
  1. [AWS Cost Explorer] Get yesterday's costs
  2. [Code] Calculate cost by service
  3. [Code] Compare to budget
  4. [IF] Did any service exceed budget?
     true:
       5a. [Slack] Alert #finops channel
       5b. [Email] Send detailed report
     false:
       5c. [Slack] Post summary to #devops
  6. [Google Sheets] Append to cost tracking sheet
```

---

## 13.7 Best Practices

### Error Handling

```yaml
error_handling_strategies:

  1_try_catch:
    description: "Use Error Trigger workflow"
    setup:
      - "Create separate workflow"
      - "Trigger: On workflow error"
      - "Actions: Log, alert, retry"

  2_retries:
    description: "Configure node retry settings"
    config:
      retry_on_fail: true
      max_tries: 3
      wait_between_tries: 5000  # ms

  3_error_output:
    description: "Connect error outputs"
    setup: "Use 'On Error' connection to handle failures"

  4_monitoring:
    description: "Set up execution monitoring"
    tools:
      - "Email on workflow failure"
      - "Slack alerts for errors"
      - "Log to external monitoring"
```

### Workflow Organization

```yaml
best_practices:
  naming:
    - "Use descriptive names: 'GitHub-PR-to-Slack'"
    - "Add prefixes for grouping: 'PROD-' for production"
    - "Include version if iterating: 'Deployment-v2'"

  tags:
    - "Tag by category: 'incident', 'deployment', 'monitoring'"
    - "Tag by environment: 'production', 'staging'"
    - "Tag by team: 'platform', 'backend'"

  folders:
    - "Use n8n's workflow folders feature"
    - "Group by: team, function, or criticality"

  documentation:
    - "Add notes to complex nodes"
    - "Document credentials needed"
    - "Include example test data"
```

### Security Considerations

```yaml
security_best_practices:

  credentials:
    - "Use n8n credential system (never hardcode)"
    - "Scope credentials minimally"
    - "Rotate API keys regularly"
    - "Audit credential access"

  webhooks:
    - "Enable webhook authentication when possible"
    - "Validate incoming data"
    - "Rate limit webhook endpoints"
    - "Log all webhook calls"

  access_control:
    - "Use n8n's user roles (owner, member, viewer)"
    - "Limit production workflow editing"
    - "Enable 2FA for all users"

  data:
    - "Don't log sensitive data"
    - "Configure execution data retention"
    - "Encrypt data at rest (use PostgreSQL with encryption)"
```

### Testing & Debugging

```yaml
testing_workflow:

  1_manual_execution:
    - "Use 'Execute Workflow' button"
    - "Inspect node output at each step"
    - "Verify data transformations"

  2_test_data:
    - "Use 'Set' node to inject test data"
    - "Create test workflows before production"

  3_debugging:
    - "Check execution history"
    - "View node input/output"
    - "Enable verbose logging"

  4_staging:
    - "Run separate n8n instance for testing"
    - "Use test credentials/endpoints"
    - "Mirror production workflows"
```

---

## 13.8 Hands-On Exercises

### Exercise 1: GitHub to Slack Workflow

```yaml
# Build the workflow from section 13.4

Goal: Send Slack notification when PR is opened

Requirements:
  - GitHub webhook trigger
  - Filter for "opened" action
  - Format message nicely
  - Send to Slack channel

Test:
  - Open a test PR
  - Verify Slack message appears
  - Check formatting and data

Bonus:
  - Add different messages for draft vs ready PRs
  - Include CI status in message
  - Add reaction buttons for quick actions
```

### Exercise 2: Deployment Status Tracker

```yaml
# Build a deployment monitoring workflow

Goal: Track deployment status and notify team

Workflow:
  1. Webhook receives deployment start notification
  2. Post "🚀 Deployment started" to Slack
  3. Wait for deployment completion webhook
  4. If successful:
     - Post "✅ Deployment succeeded" to Slack
     - Update status page
  5. If failed:
     - Post "❌ Deployment failed" to Slack
     - Create PagerDuty incident
     - Notify on-call engineer

Test:
  - Trigger with sample webhook data
  - Verify both success and failure paths
  - Check timing and notifications
```

### Exercise 3: Daily Cost Report

```yaml
# Automate daily infrastructure cost reporting

Goal: Send daily AWS cost summary

Workflow:
  1. Schedule: Run daily at 9 AM
  2. AWS Cost Explorer: Get yesterday's costs
  3. Code node: Calculate totals by service
  4. Code node: Compare to budget
  5. Google Sheets: Log costs
  6. Slack: Post summary
  7. If over budget: Email alert to management

Test:
  - Run manually first
  - Verify calculations
  - Check Google Sheets append
  - Confirm Slack formatting

Bonus:
  - Add trend analysis (week-over-week)
  - Visualize costs in Slack message
  - Include cost optimization recommendations
```

---

## 13.9 Chapter Summary

### Key Takeaways

1. **n8n is powerful workflow automation for DevOps**
   - Self-hosted, open source, unlimited executions
   - 300+ pre-built integrations
   - Visual builder with code escape hatches
   - Perfect for DevOps automation

2. **Core concepts are simple**
   - Workflows connect trigger → process → action
   - Nodes are building blocks (triggers, actions, logic)
   - Credentials securely manage API keys
   - Executions show full data flow for debugging

3. **Essential nodes for DevOps**
   - HTTP Request (call any API)
   - Webhook (receive events)
   - Schedule (cron triggers)
   - Code (JavaScript/Python)
   - IF/Switch (conditional logic)

4. **Best practices ensure reliability**
   - Implement error handling
   - Organize workflows logically
   - Secure credentials properly
   - Test before production deployment

### Next Steps

- [Chapter 14: Advanced n8n Workflows](./14-n8n-advanced.md) - AI integration, complex patterns, production deployment
- Install n8n using Docker Compose
- Complete all three hands-on exercises
- Build your first production workflow

### External Resources

**Official Documentation**
- n8n Documentation: https://docs.n8n.io
- n8n Community Forum: https://community.n8n.io
- n8n Workflow Templates: https://n8n.io/workflows

**Learning Resources**
- n8n YouTube Channel: Tutorials and walkthroughs
- n8n Blog: Best practices and case studies
- GitHub: https://github.com/n8n-io/n8n

**DevOps-Specific**
- n8n for DevOps Guide: https://docs.n8n.io/use-cases/devops/
- Workflow Template Library: Search "DevOps", "monitoring", "deployment"
- Community Workflows: Share and discover on n8n.io

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
**Copyright**: © 2026 Michel Abboud. All rights reserved.
**License**: CC BY-NC 4.0
