# Chapter 14: Advanced n8n Workflows

**Part 5: Workflow Automation**

---

## Navigation

← Previous: [Chapter 13: n8n Fundamentals](./13-n8n-fundamentals.md) | Next: [Chapter 15: Multi-Agent Fundamentals](./15-multi-agent-fundamentals.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

## AI Integration and Production DevOps Automation

**📖 Reading time:** ~17 minutes | **⚙️ Hands-on time:** ~90 minutes
**🎯 Quick nav:** [Advanced Patterns](#141-advanced-workflow-patterns) | [AI Integration](#142-integrating-n8n-with-ai-services) | [AI Within Workflows](#143-using-ai-within-n8n-workflows) | [Complex Automations](#144-complex-devops-automations) | [Claude Code Integration](#145-n8n--claude-code-integration) | [State Management](#146-database--state-management) | [Production](#147-production-considerations) | [Case Studies](#148-real-world-case-studies) | [🏋️ Skip to Exercises](#149-hands-on-exercises)

## 📋 TL;DR (5-Minute Version)

**What you'll learn:** Advanced n8n capabilities transform simple automations into intelligent, production-grade DevOps systems. This chapter covers AI integration (Claude API, GPT), advanced patterns (sub-workflows, parallel execution), complex automations (CI/CD, drift detection), and production deployment strategies.

**Key concepts:**
- **Sub-workflows & modularity**: Break complex automations into reusable components
- **AI-powered decisions**: Use Claude/GPT for log analysis, runbook generation, intelligent alerting
- **n8n + Claude Code**: Bidirectional integration for autonomous DevOps workflows
- **State management**: PostgreSQL/Redis for workflow data persistence
- **Production scaling**: Queue mode, HA setup, monitoring with Prometheus

**Why it matters for DevOps:** n8n becomes your DevOps orchestration brain—analyzing incidents with AI, auto-generating Terraform, executing remediation workflows, and coordinating complex multi-system automations that would require thousands of lines of traditional code.

**Time investment:** 17 min reading + 90 min hands-on = **~2 hours to production-grade n8n mastery**

---

## 14.1 Advanced Workflow Patterns

### 14.1.1 Sub-Workflows and Modularity

Sub-workflows allow you to create reusable automation components, critical for maintaining complex DevOps systems.

**Example: Modular Incident Response**

```yaml
# Parent Workflow: Incident Detection
1. Webhook Trigger (PagerDuty/Datadog)
2. IF Node: Severity check
   - Critical: Execute Sub-Workflow "critical-incident-response"
   - Warning: Execute Sub-Workflow "warning-incident-response"
3. Execute Workflow Node → Link to sub-workflow ID
```

**Creating the Sub-Workflow:**

```yaml
# Sub-Workflow: critical-incident-response
Name: Critical Incident Response
Description: Standard response for P0/P1 incidents

Steps:
1. Input: incident_id, service_name, severity, description
2. Slack Node: Alert #incidents channel
3. PagerDuty Node: Page on-call engineer
4. GitHub Node: Create incident issue
5. Jira Node: Create high-priority ticket
6. AWS Node: Scale up affected service (auto-remediation)
7. Slack Node: Post timeline update
8. Output: incident_response_summary
```

**Benefits:**
- **Reusability**: One sub-workflow used by 10+ parent workflows
- **Maintainability**: Update incident response in one place
- **Testing**: Test sub-workflows independently
- **Clarity**: Parent workflows stay clean and readable

### 14.1.2 Parallel Execution and Fan-Out Patterns

Execute multiple operations simultaneously to reduce workflow execution time.

**Example: Multi-Cloud Status Check**

```yaml
# Parallel health checks across cloud providers
1. Schedule Trigger (every 5 minutes)
2. Split In Batches Node → Mode: "Each item separately"
3. Fan-out to parallel branches:

   Branch A: AWS Health Check
   - HTTP Request → AWS Status API
   - Parse response

   Branch B: GCP Health Check
   - HTTP Request → GCP Status API
   - Parse response

   Branch C: Azure Health Check
   - HTTP Request → Azure Status API
   - Parse response

   Branch D: Datadog Metrics
   - HTTP Request → Datadog API (last 5 min)
   - Calculate averages

4. Merge Node → Wait for all branches
5. Code Node → Aggregate results
6. IF Node → Any issues?
   - Yes: Trigger alert workflow
   - No: Update status dashboard
```

**Performance Impact:**
- Sequential: 4 API calls × 2s each = **8 seconds**
- Parallel: max(2s, 2s, 2s, 2s) = **2 seconds** (4× faster)

### 14.1.3 Error Workflows and Graceful Degradation

Handle failures intelligently with dedicated error workflows.

**Example: Deployment Pipeline with Fallback**

```yaml
# Main Workflow: Deploy to Production
1. GitHub Trigger: Push to main branch
2. Execute Workflow: "run-test-suite"
   - On Success: Continue
   - On Error: Trigger "deployment-failure-handler"
3. Execute Workflow: "deploy-to-staging"
   - On Success: Continue
   - On Error: Trigger "deployment-failure-handler"
4. Wait Node: 5 minutes (smoke test period)
5. Execute Workflow: "deploy-to-production"
   - On Success: Send success notification
   - On Error: Execute "rollback-deployment" + "deployment-failure-handler"

# Error Workflow: deployment-failure-handler
1. Input: workflow_name, error_message, commit_sha
2. Slack: Post to #deployments with @here
3. PagerDuty: Page deployment team
4. GitHub: Add comment to commit
5. Datadog: Create deployment failure event
6. Execute Workflow: "capture-logs-and-artifacts"
7. Jira: Auto-create bug ticket with logs attached
```

**Error Handling Best Practices:**
- **Always set error workflows** on critical Execute Workflow nodes
- **Capture context**: Pass error details, timestamps, related data
- **Implement retries**: Use Loop node with retry logic for transient failures
- **Graceful degradation**: Fall back to manual processes when automation fails

---

## 14.2 Integrating n8n with AI Services

### 14.2.1 Claude API Integration

Connect n8n to Anthropic's Claude API for intelligent decision-making.

**Setup: Claude API Credentials in n8n**

```yaml
Credentials → Add Credential → HTTP Request
Name: Claude API
Authentication: Generic Credential Type
- Header Auth:
  - Name: x-api-key
  - Value: sk-ant-api03-xxx (your Anthropic API key)
  - Name: anthropic-version
  - Value: 2023-06-01
```

**Example: AI-Powered Log Analysis**

```yaml
Workflow: Analyze Application Errors

1. Webhook Trigger: Receives error logs from application
   Input: { "error_message": "...", "stack_trace": "...", "timestamp": "..." }

2. Code Node: Prepare Claude prompt
   ```javascript
   const errorData = $json;

   const prompt = `You are a senior DevOps engineer analyzing application errors.

   Error Message: ${errorData.error_message}
   Stack Trace: ${errorData.stack_trace}
   Timestamp: ${errorData.timestamp}

   Please analyze this error and provide:
   1. Root cause analysis
   2. Severity assessment (Critical/High/Medium/Low)
   3. Recommended remediation steps
   4. Whether this requires immediate human attention (Yes/No)

   Format your response as JSON with keys: root_cause, severity, remediation_steps, requires_human_attention`;

   return {
     json: {
       model: "claude-3-5-sonnet-20241022",
       max_tokens: 1024,
       messages: [
         {
           role: "user",
           content: prompt
         }
       ]
     }
   };
   ```

3. HTTP Request Node: Call Claude API
   - Method: POST
   - URL: https://api.anthropic.com/v1/messages
   - Authentication: Use "Claude API" credential
   - Body: {{ $json }}

4. Code Node: Parse Claude response
   ```javascript
   const response = $json;
   const analysis = JSON.parse(response.content[0].text);

   return {
     json: {
       ...analysis,
       original_error: $node["Webhook"].json
     }
   };
   ```

5. IF Node: Requires human attention?
   - Condition: {{ $json.requires_human_attention }} equals "Yes"

   TRUE branch:
   6a. Slack Node: Alert #oncall channel with analysis
   7a. PagerDuty Node: Create incident

   FALSE branch:
   6b. GitHub Node: Create issue with "auto-analyzed" label
   7b. Slack Node: Post to #dev-notifications (no page)

8. Database Node: Store analysis in PostgreSQL
   - Table: error_analyses
   - Columns: error_id, root_cause, severity, remediation_steps, analyzed_at
```

**Benefits:**
- **Intelligent triage**: AI determines severity and urgency
- **Root cause insights**: Claude analyzes stack traces humans might miss
- **Reduced alert fatigue**: Only page for critical issues
- **Knowledge capture**: Store AI analysis for pattern recognition

### 14.2.2 OpenAI GPT Integration

Similar pattern for OpenAI's GPT models.

**Example: Auto-Generate Runbooks**

```yaml
Workflow: Generate Incident Runbook

1. Manual Trigger: Operator provides incident description
   Input: { "incident_type": "database_connection_failure", "service": "payment-api" }

2. HTTP Request: Call OpenAI API
   - URL: https://api.openai.com/v1/chat/completions
   - Headers: { "Authorization": "Bearer sk-xxx" }
   - Body:
     ```json
     {
       "model": "gpt-4",
       "messages": [
         {
           "role": "system",
           "content": "You are a DevOps expert creating detailed incident runbooks. Format output as markdown with clear steps."
         },
         {
           "role": "user",
           "content": "Create a runbook for: {{ $json.incident_type }} affecting {{ $json.service }}"
         }
       ],
       "max_tokens": 2000
     }
     ```

3. Code Node: Format runbook
4. GitHub Node: Create runbook file in /docs/runbooks/
5. Slack Node: Share runbook link with team
6. Notion Node: Add to runbook database
```

---

## 14.3 Using AI Within n8n Workflows

### 14.3.1 Intelligent Log Analysis

**Example: Detect Anomalies in CloudWatch Logs**

```yaml
Workflow: CloudWatch Log Anomaly Detection

1. Schedule Trigger: Every 10 minutes

2. AWS Node: Fetch CloudWatch Logs
   - Log Group: /aws/lambda/production-api
   - Time Range: Last 10 minutes
   - Filter: errors, warnings, timeouts

3. Code Node: Prepare log summary
   ```javascript
   const logs = $json.logEvents.map(e => e.message).join('\n');

   return {
     json: {
       log_count: $json.logEvents.length,
       log_sample: logs
     }
   };
   ```

4. HTTP Request: Claude API
   - Prompt: "Analyze these logs for anomalies, security issues, or performance degradation. Provide: 1) Are there any anomalies? (Yes/No), 2) If yes, describe the issue and severity"

5. IF Node: Anomalies detected?
   - Condition: Claude response contains "Anomalies: Yes"

   TRUE:
   6. Execute Workflow: "incident-response"
   7. Datadog Node: Create event with AI analysis

   FALSE:
   6. Database: Log "healthy" status
```

### 14.3.2 AI-Powered Intelligent Alerting

Reduce alert noise by letting AI filter false positives.

**Example: Smart Disk Space Alerts**

```yaml
Workflow: Intelligent Disk Space Monitoring

1. Schedule Trigger: Every 5 minutes

2. HTTP Request: Prometheus query
   - Query: node_filesystem_avail_bytes / node_filesystem_size_bytes
   - Returns: Disk usage % for all servers

3. Code Node: Filter servers >80% usage
   ```javascript
   const highUsage = $json.result.filter(r => {
     const usage = 100 - (r.value[1] * 100);
     return usage > 80;
   });

   return highUsage.map(server => ({
     json: {
       server: server.metric.instance,
       usage_percent: 100 - (server.value[1] * 100),
       timestamp: new Date().toISOString()
     }
   }));
   ```

4. Loop Over Items

5. HTTP Request: Claude API
   - For each high-usage server, ask Claude:
   ```
   Server {{ $json.server }} has {{ $json.usage_percent }}% disk usage.

   Historical context: This server typically runs at 70-75% usage.
   Recent events: Deployed new version 2 hours ago.
   Server type: Log aggregation server (Elasticsearch).

   Is this concerning and requires immediate action? Consider:
   - Normal usage patterns for this server type
   - Recent deployments
   - Whether this is steady-state or rapidly growing

   Respond with: ACTION (page oncall) or MONITOR (log only) and brief reasoning.
   ```

6. IF Node: Claude says "ACTION"
   TRUE: Create PagerDuty incident
   FALSE: Log to monitoring dashboard only
```

**Result:** 70% reduction in false-positive disk alerts.

### 14.3.3 Auto-Generate Infrastructure Code

**Example: AI Writes Terraform from Requirements**

```yaml
Workflow: Generate Terraform from Specs

1. Slack Command Trigger: /terraform-generate
   User provides: "Create an RDS PostgreSQL 14 database with read replica, 100GB storage, t3.medium instance"

2. HTTP Request: Claude API
   - Prompt:
   ```
   Generate production-ready Terraform code for AWS based on these requirements:
   {{ $json.text }}

   Include:
   - Main resource definitions
   - Variables file
   - Outputs
   - Best practices (encryption, backup, tags)

   Format as proper HCL code with comments.
   ```

3. Code Node: Split response into files
   ```javascript
   const claudeResponse = $json.content[0].text;

   // Extract code blocks
   const mainTf = claudeResponse.match(/```hcl\n([\s\S]*?)```/)[1];
   const variablesTf = claudeResponse.match(/# variables.tf\n```hcl\n([\s\S]*?)```/)[1];

   return [
     { json: { filename: "main.tf", content: mainTf } },
     { json: { filename: "variables.tf", content: variablesTf } }
   ];
   ```

4. GitHub Node: Create PR with generated Terraform
   - Branch: auto-generated/rds-{{ Date.now() }}
   - Files: main.tf, variables.tf, outputs.tf
   - PR Description: "Auto-generated by AI from Slack request"

5. Slack Node: Reply with PR link for review
```

---

## 14.4 Complex DevOps Automations

### 14.4.1 Multi-Stage CI/CD Pipeline

**Example: Complete Deployment Pipeline**

```yaml
Workflow: Full CI/CD Pipeline with Approvals

1. GitHub Trigger: Pull request merged to main

2. Set Variable: deployment_id = {{ $json.sha }}-{{ Date.now() }}

3. Execute Workflow: "run-test-suite"
   - Pass: deployment_id, repo_name, commit_sha
   - Wait for completion
   - On Error: Stop and notify

4. Execute Workflow: "build-docker-image"
   - Build image: myapp:{{ $json.sha }}
   - Push to ECR
   - Scan with Trivy for vulnerabilities

5. IF Node: Vulnerabilities found?
   TRUE: Execute "security-review-workflow", wait for approval
   FALSE: Continue

6. Execute Workflow: "deploy-to-staging"
   - Update ECS service
   - Run smoke tests
   - Wait 10 minutes

7. Execute Workflow: "run-integration-tests"
   - Selenium tests
   - API contract tests
   - Performance tests with k6

8. Wait for Approval Node (Custom implementation):
   - Send Slack message to #deployments
   - Include buttons: "Approve to Production" / "Reject"
   - Wait for webhook callback
   - Timeout: 2 hours

9. IF Node: Approved?
   TRUE:
     10. Execute Workflow: "deploy-to-production"
         - Blue-green deployment
         - Health check validation
         - Route 53 traffic shift
     11. Execute Workflow: "smoke-tests-production"
     12. IF Node: Tests pass?
         TRUE: Mark deployment success
         FALSE: Execute "rollback-deployment"

   FALSE:
     10. Slack: Notify deployment cancelled
     11. GitHub: Add comment to PR

13. Datadog: Send deployment event with outcome
14. Jira: Update deployment ticket status
```

### 14.4.2 Infrastructure Drift Detection

**Example: Terraform State vs. Actual Resources**

```yaml
Workflow: Detect Infrastructure Drift

1. Schedule Trigger: Daily at 2 AM

2. Bash Command Node: Run terraform plan
   ```bash
   cd /terraform/production
   terraform plan -detailed-exitcode -out=plan.tfplan
   terraform show -json plan.tfplan > plan.json
   ```
   - Exit code 0: No changes
   - Exit code 2: Drift detected

3. IF Node: Drift detected? (exit code == 2)

   TRUE branch:
   4. Read File Node: Load plan.json

   5. HTTP Request: Claude API
      - Prompt: "Analyze this Terraform drift. Explain what changed outside of Terraform, why it might have happened, and severity level."

   6. Code Node: Parse drift details
      ```javascript
      const driftedResources = $json.resource_changes
        .filter(r => r.change.actions.includes('update'))
        .map(r => ({
          resource: r.address,
          changes: r.change.after
        }));

      return { json: { drifted_resources: driftedResources } };
      ```

   7. GitHub Node: Create issue
      - Title: "🚨 Infrastructure Drift Detected - {{ Date.now() }}"
      - Body: Include AI analysis + resource list
      - Labels: ["infrastructure", "drift", "needs-review"]

   8. Slack Node: Alert #infrastructure channel

   9. Jira Node: Create high-priority ticket

   FALSE branch:
   4. Database: Log "no drift" status
   5. Update monitoring dashboard
```

### 14.4.3 Security Compliance Automation

**Example: Automated Security Audit**

```yaml
Workflow: Weekly Security Compliance Check

1. Schedule Trigger: Every Monday 9 AM

2. Parallel Execution:

   Branch A: AWS Security
   - List all S3 buckets
   - Check public access settings
   - Verify encryption enabled
   - Check bucket policies

   Branch B: IAM Audit
   - List users with access keys >90 days old
   - Find users with no MFA
   - Check for overly permissive policies

   Branch C: EC2 Security Groups
   - Find rules with 0.0.0.0/0 access
   - Check for unused security groups

   Branch D: RDS Encryption
   - List RDS instances
   - Verify encryption at rest
   - Check public accessibility

3. Merge: Wait for all branches

4. Code Node: Aggregate findings
   ```javascript
   const findings = {
     critical: [],
     high: [],
     medium: [],
     low: []
   };

   // Categorize issues by severity
   $input.all().forEach(item => {
     if (item.json.issue_type === 'public_s3_bucket') {
       findings.critical.push(item.json);
     }
     // ... more categorization logic
   });

   return { json: findings };
   ```

5. HTTP Request: Claude API
   - Prompt: "Generate an executive summary of these security findings. Include: 1) Risk overview, 2) Top 3 priorities, 3) Recommended timeline for remediation"

6. Code Node: Generate HTML report
7. Send Email: Security team + management
8. Jira: Create tickets for each critical/high finding
9. Slack: Post summary to #security
10. S3: Store full report for compliance records
```

---

## 14.5 n8n + Claude Code Integration

### 14.5.1 Trigger n8n from Claude Code

**Use Case:** Claude Code detects issue → n8n orchestrates remediation

**Setup:**

1. **Create n8n webhook workflow:**
```yaml
Workflow: Claude Code Remediation Trigger

1. Webhook Node
   - Method: POST
   - Path: claude-code-trigger
   - Authentication: Header Auth (Bearer token)

2. Code Node: Parse Claude Code request
   Input expected:
   {
     "trigger_type": "code_quality_issue",
     "repository": "myapp",
     "file_path": "src/api/users.js",
     "issue_description": "SQL injection vulnerability detected",
     "severity": "critical"
   }

3. Switch Node: Based on trigger_type

   Case "code_quality_issue":
   - Create GitHub issue
   - Run SAST scan with Semgrep
   - Notify security team

   Case "deployment_needed":
   - Execute deployment workflow

   Case "incident_detected":
   - Execute incident response workflow
```

2. **Create Claude Code hook to call n8n:**

```yaml
# ~/.config/claude/hooks.yaml
hooks:
  post_edit:
    - command: |
        # Check if edited file contains SQL queries
        if grep -q "SELECT.*FROM\|INSERT INTO\|UPDATE.*SET" {{file}}; then
          # Trigger n8n workflow for security review
          curl -X POST https://n8n.yourcompany.com/webhook/claude-code-trigger \
            -H "Authorization: Bearer YOUR_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{
              "trigger_type": "code_quality_issue",
              "repository": "'$(basename $(git rev-parse --show-toplevel))'",
              "file_path": "{{file}}",
              "issue_description": "SQL query detected, requires security review",
              "severity": "high"
            }'
        fi
      description: "Trigger n8n security review for SQL code"
```

**Result:** Any SQL code edited by Claude Code automatically triggers security review workflow in n8n.

### 14.5.2 n8n Calls Claude Code

**Use Case:** n8n detects issue → Claude Code fixes it automatically

**Setup:**

1. **n8n workflow detects problem:**
```yaml
Workflow: Auto-Fix Code Issues

1. GitHub Webhook: New issue labeled "auto-fixable"

2. Code Node: Prepare Claude Code command
   ```javascript
   const issue = $json.issue;

   // Parse issue for file and description
   const fileMatch = issue.body.match(/File: (.+)/);
   const descMatch = issue.body.match(/Issue: (.+)/);

   return {
     json: {
       file_path: fileMatch[1],
       issue_description: descMatch[1],
       repo_name: $json.repository.name,
       issue_number: issue.number
     }
   };
   ```

3. SSH Node: Connect to CI server

4. Execute Command Node:
   ```bash
   cd /repos/{{ $json.repo_name }}

   # Use Claude Code CLI to fix issue
   claude code --prompt "Fix the following issue in {{ $json.file_path }}: {{ $json.issue_description }}" --auto-commit

   # Create PR
   git checkout -b auto-fix/issue-{{ $json.issue_number }}
   git push origin auto-fix/issue-{{ $json.issue_number }}

   gh pr create --title "Auto-fix: {{ $json.issue_description }}" \
     --body "Automatically generated by n8n + Claude Code to resolve #{{ $json.issue_number }}"
   ```

5. GitHub Node: Add comment to original issue
   - Comment: "🤖 Auto-fix PR created: [link]"

6. Slack Node: Notify team for review
```

**Result:** Certain GitHub issues automatically trigger Claude Code to create fix PRs.

---

## 14.6 Database & State Management

### 14.6.1 PostgreSQL for Workflow Data

Store workflow state, execution history, and analytics.

**Setup PostgreSQL Credential:**
```yaml
Credentials → PostgreSQL
- Host: db.yourcompany.com
- Port: 5432
- Database: n8n_workflows
- User: n8n_user
- Password: [secure password]
- SSL: Enabled
```

**Example: Track Deployment History**

```yaml
Workflow: Record Deployment

[... deployment steps ...]

Final Step: PostgreSQL Node
- Operation: Insert
- Table: deployments
- Columns:
  - deployment_id: {{ $json.deployment_id }}
  - service_name: {{ $json.service }}
  - version: {{ $json.version }}
  - environment: {{ $json.environment }}
  - deployed_by: {{ $json.github_user }}
  - deployed_at: {{ $now }}
  - status: {{ $json.deployment_status }}
  - rollback_version: {{ $json.previous_version }}
```

**Query Deployment History:**
```sql
-- Recent deployments by service
SELECT service_name, version, environment, deployed_at, status
FROM deployments
WHERE deployed_at > NOW() - INTERVAL '7 days'
ORDER BY deployed_at DESC;

-- Deployment frequency
SELECT service_name, COUNT(*) as deployment_count
FROM deployments
WHERE deployed_at > NOW() - INTERVAL '30 days'
GROUP BY service_name
ORDER BY deployment_count DESC;
```

### 14.6.2 Redis for Caching and Rate Limiting

Use Redis for fast state checks and rate limiting.

**Example: Rate-Limit Webhook Calls**

```yaml
Workflow: Webhook with Rate Limiting

1. Webhook Trigger

2. Redis Node: Check rate limit
   - Operation: GET
   - Key: rate_limit:{{ $json.source_ip }}

3. IF Node: Rate limit exceeded?
   - Condition: {{ $json.request_count }} > 100

   TRUE:
   - Stop and error
   - HTTP Response: 429 Too Many Requests

   FALSE:
   - Continue to next step

4. Redis Node: Increment counter
   - Operation: INCR
   - Key: rate_limit:{{ $json.source_ip }}
   - TTL: 3600 (1 hour)

5. [Continue with actual workflow logic...]
```

---

## 14.7 Production Considerations

### 14.7.1 Queue Mode for Scaling

Standard n8n runs workflows in the main process. Queue mode uses Redis for job distribution across multiple workers.

**Setup:**

```yaml
# docker-compose.yml for Queue Mode
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  n8n-master:
    image: n8nio/n8n:latest
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - N8N_PROTOCOL=https
      - N8N_HOST=n8n.yourcompany.com
      - WEBHOOK_URL=https://n8n.yourcompany.com/
    ports:
      - "5678:5678"
    depends_on:
      - redis
      - postgres
    volumes:
      - n8n_data:/home/node/.n8n

  n8n-worker-1:
    image: n8nio/n8n:latest
    command: worker
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
    depends_on:
      - redis
      - postgres
    volumes:
      - n8n_data:/home/node/.n8n

  n8n-worker-2:
    image: n8nio/n8n:latest
    command: worker
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
    depends_on:
      - redis
      - postgres
    volumes:
      - n8n_data:/home/node/.n8n

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  redis_data:
  postgres_data:
```

**Benefits:**
- **Horizontal scaling**: Add more workers for higher throughput
- **Resource isolation**: Heavy workflows don't block the UI
- **Reliability**: Worker crashes don't affect master/UI

### 14.7.2 High Availability Setup

**Architecture:**

```
                   ┌─────────────┐
                   │   Load      │
                   │  Balancer   │
                   │  (nginx)    │
                   └──────┬──────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
    │ n8n      │    │ n8n      │    │ n8n      │
    │ Instance │    │ Instance │    │ Instance │
    │    1     │    │    2     │    │    3     │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │                │                │
         └────────────────┼────────────────┘
                          │
                   ┌──────▼──────┐
                   │  PostgreSQL │
                   │   Primary   │
                   │ (RDS Multi-AZ)│
                   └─────────────┘
```

**Kubernetes Deployment:**

```yaml
# n8n-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n
  namespace: automation
spec:
  replicas: 3
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
        env:
        - name: DB_TYPE
          value: "postgresdb"
        - name: DB_POSTGRESDB_HOST
          valueFrom:
            secretKeyRef:
              name: n8n-db
              key: host
        - name: DB_POSTGRESDB_DATABASE
          value: "n8n"
        - name: DB_POSTGRESDB_USER
          valueFrom:
            secretKeyRef:
              name: n8n-db
              key: username
        - name: DB_POSTGRESDB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: n8n-db
              key: password
        - name: N8N_ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: n8n-secrets
              key: encryption-key
        - name: EXECUTIONS_MODE
          value: "queue"
        - name: QUEUE_BULL_REDIS_HOST
          value: "redis-service"
        ports:
        - containerPort: 5678
        livenessProbe:
          httpGet:
            path: /healthz
            port: 5678
          initialDelaySeconds: 30
          periodSeconds: 10
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: n8n-service
  namespace: automation
spec:
  type: LoadBalancer
  ports:
  - port: 443
    targetPort: 5678
  selector:
    app: n8n
```

### 14.7.3 Monitoring and Observability

**Prometheus Metrics:**

Enable metrics endpoint in n8n:
```bash
# Environment variables
N8N_METRICS=true
N8N_METRICS_INCLUDE_DEFAULT_METRICS=true
N8N_METRICS_INCLUDE_WORKFLOW_ID_LABEL=true
```

**Key Metrics to Track:**

```yaml
# Prometheus scrape config
scrape_configs:
  - job_name: 'n8n'
    static_configs:
      - targets: ['n8n:5678']
    metrics_path: '/metrics'

# Important metrics:
# - n8n_workflow_executions_total (counter)
# - n8n_workflow_execution_duration_seconds (histogram)
# - n8n_workflow_execution_status (gauge)
# - n8n_webhook_calls_total (counter)
# - n8n_trigger_errors_total (counter)
```

**Grafana Dashboard:**

```json
{
  "dashboard": {
    "title": "n8n Production Monitoring",
    "panels": [
      {
        "title": "Workflow Execution Rate",
        "targets": [
          {
            "expr": "rate(n8n_workflow_executions_total[5m])"
          }
        ]
      },
      {
        "title": "Workflow Success Rate",
        "targets": [
          {
            "expr": "sum(rate(n8n_workflow_executions_total{status='success'}[5m])) / sum(rate(n8n_workflow_executions_total[5m]))"
          }
        ]
      },
      {
        "title": "Average Execution Duration",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(n8n_workflow_execution_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Failed Workflows (Last Hour)",
        "targets": [
          {
            "expr": "sum(increase(n8n_workflow_executions_total{status='error'}[1h]))"
          }
        ]
      }
    ]
  }
}
```

**Alerting Rules:**

```yaml
# prometheus-alerts.yaml
groups:
  - name: n8n_alerts
    interval: 30s
    rules:
      - alert: N8nHighFailureRate
        expr: |
          (
            sum(rate(n8n_workflow_executions_total{status="error"}[5m]))
            /
            sum(rate(n8n_workflow_executions_total[5m]))
          ) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "n8n workflow failure rate above 10%"
          description: "{{ $value | humanizePercentage }} of workflows failing"

      - alert: N8nWorkflowExecutionSlow
        expr: |
          histogram_quantile(0.95,
            rate(n8n_workflow_execution_duration_seconds_bucket[5m])
          ) > 300
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "n8n workflows executing slowly"
          description: "P95 execution time is {{ $value }}s"

      - alert: N8nDown
        expr: up{job="n8n"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "n8n instance is down"
```

---

## 14.8 Real-World Case Studies

### 14.8.1 Case Study: Automated Incident Response System

**Company:** E-commerce platform, 50M+ users
**Challenge:** Mean time to response (MTTR) of 45 minutes for production incidents
**Solution:** n8n + Claude + PagerDuty + Kubernetes

**Implementation:**

```yaml
Workflow: Intelligent Incident Response

1. PagerDuty Trigger: New high-priority incident

2. Parallel Data Collection (60 seconds):
   - Kubernetes: Pod status, logs for affected service
   - Datadog: Metrics (CPU, memory, latency) for last 30 min
   - AWS: CloudWatch logs, ALB metrics
   - GitHub: Recent deployments (last 24 hours)
   - Database: Query slow log, connection count

3. Merge: Aggregate all data

4. HTTP Request: Claude API
   - Prompt: "Analyze this incident data. Provide: 1) Most likely root cause, 2) Suggested remediation steps, 3) If auto-remediation is safe (Yes/No)"
   - Input: All collected data + incident description

5. Code Node: Parse Claude response
   - Extract: root_cause, remediation_steps, safe_to_auto_remediate

6. Slack: Post AI analysis to #incidents channel

7. IF Node: Safe to auto-remediate?

   TRUE:
   - Execute remediation steps automatically
   - Examples:
     * Scale up pods (kubectl scale)
     * Restart failing service
     * Clear cache
     * Rotate database connections
   - Monitor for 5 minutes
   - IF Node: Issue resolved?
     * Yes: Close PagerDuty incident, post success
     * No: Page oncall engineer with context

   FALSE:
   - Page oncall engineer immediately
   - Provide Claude's analysis + raw data
   - Create detailed incident ticket in Jira

8. Database: Record incident + response actions
```

**Results:**
- **MTTR reduced** from 45 min → 8 min (82% improvement)
- **40% of incidents** auto-remediated without human intervention
- **Engineer satisfaction** increased (less trivial pages at 3 AM)
- **Cost savings**: ~$120K/year in reduced downtime

### 14.8.2 Case Study: Intelligent Cost Optimization

**Company:** SaaS startup, AWS infrastructure
**Challenge:** AWS bill growing 15% month-over-month without visibility
**Solution:** n8n + Claude + AWS Cost Explorer + Terraform

**Implementation:**

```yaml
Workflow: Daily Cost Analysis & Optimization

1. Schedule Trigger: Daily at 8 AM

2. AWS Cost Explorer Node: Get yesterday's costs by service

3. Code Node: Compare to historical average
   - Query PostgreSQL for 30-day average
   - Calculate anomalies (>20% increase)

4. IF Node: Anomalies detected?

   TRUE:
   5. Parallel Investigation:
      - AWS: List resources for expensive services
      - CloudWatch: Analyze usage patterns
      - Terraform: Check if resources match IaC

   6. HTTP Request: Claude API
      - Prompt: "Analyze these AWS costs. Identify: 1) Unused resources, 2) Right-sizing opportunities, 3) Potential misconfigurations, 4) Safe-to-delete resources"

   7. Code Node: Generate Terraform changes
      - For right-sizing: Update instance types
      - For unused: Add to deletion list

   8. GitHub: Create PR with Terraform changes
      - Title: "💰 Cost Optimization - Estimated savings: $XXX/month"
      - Body: Include Claude's analysis

   9. Slack: Post to #finops channel
      - Summary of findings
      - Link to PR for review
      - Estimated monthly savings

   10. Wait for Approval (webhook callback)

   11. IF Approved:
       - Apply Terraform changes
       - Monitor for 24 hours
       - Report actual savings

   FALSE:
   5. Database: Log "costs normal"
```

**Results:**
- **$18K/month saved** (22% cost reduction)
- **Automated detection** of 47 unused resources in first week
- **Right-sized** 120+ over-provisioned instances
- **ROI**: n8n setup paid for itself in 3 days

---

## 14.9 Hands-On Exercises

### Exercise 1: Build an AI-Powered Error Analyzer

**Goal:** Create a workflow that analyzes application errors with Claude and creates categorized GitHub issues.

**Requirements:**
1. Webhook trigger that accepts error payloads
2. Claude API integration for error analysis
3. Automatic severity classification
4. Create GitHub issues with appropriate labels
5. Slack notifications for critical errors

**Starter template:**
```yaml
1. Webhook Trigger
   Expected input: { "error_message": "", "stack_trace": "", "app_name": "" }

2. [YOUR CODE: Prepare Claude prompt]

3. [YOUR CODE: Call Claude API]

4. [YOUR CODE: Parse response and categorize]

5. [YOUR CODE: Create GitHub issue]

6. [YOUR CODE: Conditional Slack alert for critical issues]
```

**Success criteria:**
- Claude provides actionable analysis
- Issues are correctly labeled by severity
- Critical errors trigger immediate Slack alerts
- Non-critical errors logged without alerting

### Exercise 2: Multi-Cloud Cost Reporter

**Goal:** Build a daily cost report that fetches data from AWS, GCP, and Azure, then generates an executive summary with Claude.

**Requirements:**
1. Parallel API calls to AWS Cost Explorer, GCP Billing, Azure Cost Management
2. Aggregate costs by service and cloud provider
3. Claude generates executive summary with insights
4. Email report to finance team
5. Store data in PostgreSQL for trend analysis

**Bonus challenges:**
- Add cost anomaly detection (>15% day-over-day increase)
- Generate cost forecast for end of month
- Create visualization with Chart.js

### Exercise 3: Intelligent Deployment Pipeline

**Goal:** Build a complete CI/CD pipeline with AI-powered code review and automated testing.

**Requirements:**
1. GitHub trigger on PR merge to main
2. Run test suite, build Docker image
3. Claude reviews code changes for potential issues
4. Deploy to staging with health checks
5. Wait for manual approval (Slack button)
6. Blue-green deploy to production
7. Automated rollback if health checks fail

**Advanced features:**
- Terraform plan validation with Claude
- Security scan with Trivy + Claude analysis
- Performance testing with k6
- Datadog deployment event tracking

---

## 14.10 Chapter Summary

### What You've Learned

This chapter covered the transformation of n8n from a simple automation tool into a production-grade DevOps orchestration platform:

**Advanced Workflow Patterns:**
- Sub-workflows for modular, reusable automation components
- Parallel execution patterns for 4× performance improvements
- Error workflows for graceful degradation and intelligent failure handling

**AI Integration:**
- Claude and GPT API integration for intelligent decision-making
- AI-powered log analysis, alert filtering, and incident triage
- Auto-generation of runbooks, Terraform code, and documentation

**Complex DevOps Automations:**
- Multi-stage CI/CD pipelines with approvals and rollbacks
- Infrastructure drift detection with AI analysis
- Security compliance automation across cloud providers

**Production Readiness:**
- Queue mode with Redis for horizontal scaling
- High availability with Kubernetes and load balancing
- Comprehensive monitoring with Prometheus and Grafana

**Real-World Impact:**
- 82% reduction in MTTR with automated incident response
- 22% cost savings through AI-powered optimization
- 40% of incidents resolved without human intervention

### Key Takeaways

1. **n8n + AI = Force Multiplier**: Combining workflow automation with AI reasoning creates systems that approach human-level DevOps decision-making

2. **Start Simple, Scale Smart**: Begin with basic workflows, add complexity only when needed, and always plan for production from day one

3. **Observability is Critical**: Monitor workflow execution, track failures, measure business impact—you can't improve what you don't measure

4. **Security and State Management**: Production workflows require proper credential management, database persistence, and audit trails

5. **Bidirectional Integration**: n8n calling Claude Code AND Claude Code calling n8n creates a powerful autonomous DevOps ecosystem

### Next Steps

**Immediate (This Week):**
1. Set up n8n in queue mode with PostgreSQL backend
2. Implement one AI-powered workflow from this chapter
3. Create Prometheus/Grafana monitoring dashboard

**Short-term (This Month):**
1. Migrate 3-5 manual DevOps processes to n8n workflows
2. Integrate with your primary incident management system
3. Build custom sub-workflows for your team's common patterns

**Long-term (This Quarter):**
1. Deploy n8n in HA configuration on Kubernetes
2. Create organization-wide workflow library
3. Measure and report on automation ROI

### Additional Resources

**Official n8n Documentation:**
- Advanced workflows: https://docs.n8n.io/courses/level-two/
- Queue mode setup: https://docs.n8n.io/hosting/scaling/queue-mode/
- Security best practices: https://docs.n8n.io/hosting/security/

**AI Integration:**
- Anthropic Claude API: https://docs.anthropic.com/
- OpenAI GPT API: https://platform.openai.com/docs/
- AI prompt engineering for automation: https://www.promptingguide.ai/

**DevOps Automation:**
- n8n + Terraform workflows: https://n8n.io/integrations/terraform/
- n8n + Kubernetes monitoring: https://n8n.io/integrations/kubernetes/
- GitOps with n8n: https://n8n.io/workflows/gitops/

**Production Deployment:**
- n8n Kubernetes Helm chart: https://github.com/8gears/n8n-helm-chart
- n8n monitoring with Prometheus: https://docs.n8n.io/hosting/environment-variables/deployment/#metrics
- n8n HA reference architecture: https://community.n8n.io/t/high-availability-setup/

**Community Resources:**
- n8n Community Forum: https://community.n8n.io/
- n8n Workflow Templates: https://n8n.io/workflows/
- n8n GitHub Discussions: https://github.com/n8n-io/n8n/discussions

---

**🎉 Congratulations!** You've completed the advanced n8n chapter and now have the knowledge to build production-grade, AI-powered DevOps automation systems. You're equipped to transform manual processes into intelligent, self-healing workflows that save time, reduce errors, and scale with your organization.

**Next Chapter:** [Chapter 15: Future of AI in DevOps] (coming soon) - Explore emerging trends, predictive infrastructure management, and the evolution of autonomous DevOps systems.

---

**📚 Navigation:**
- [← Previous: Chapter 13 - n8n Fundamentals](13-n8n-fundamentals.md)
- [↑ Back to Main Index](../README.md)
- [→ Next: Chapter 15 - Future of AI in DevOps](#) (coming soon)

---

*This chapter is part of "AI and Claude Code: A Comprehensive Guide for DevOps Engineers"*
*Author: Michel Abboud | License: CC BY-NC 4.0*
*Learn more: https://github.com/michelabboud/ai-and-claude-code-intro*

---

## Navigation

← Previous: [Chapter 13: n8n Fundamentals](./13-n8n-fundamentals.md) | Next: [Chapter 15: Multi-Agent Fundamentals](./15-multi-agent-fundamentals.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 14** | Advanced n8n Workflows | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
