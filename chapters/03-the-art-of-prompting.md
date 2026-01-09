# Chapter 3: The Art of Prompting

## Mastering the Skill of Communicating with AI

As a DevOps engineer, you already know that clear communication with machines (code, configs, scripts) is essential. Prompting is the same skill applied to AI—the better your input, the better your output.

---

## 3.1 What is a Prompt?

### Definition

A **prompt** is any text input you provide to an LLM. It's your way of telling the AI what you want.

```
┌────────────────────────────────────────────────────────────────┐
│                      ANATOMY OF A PROMPT                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    SYSTEM PROMPT                        │   │
│  │  (Sets the AI's role, personality, constraints)         │   │
│  │                                                         │   │
│  │  "You are a senior DevOps engineer specializing in      │   │
│  │   Kubernetes. Be concise and provide working examples." │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           +                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    USER PROMPT                          │   │
│  │  (Your actual question or request)                      │   │
│  │                                                         │   │
│  │  "How do I set up horizontal pod autoscaling for my     │   │
│  │   nginx deployment based on CPU usage?"                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           +                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    CONTEXT (Optional)                   │   │
│  │  (Additional information: code, logs, configs)          │   │
│  │                                                         │   │
│  │  "Here's my current deployment:                         │   │
│  │   apiVersion: apps/v1                                   │   │
│  │   kind: Deployment..."                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
│                           ↓                                    │
│                    AI RESPONSE                                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### The Prompt Quality Spectrum

```
Poor Prompt                                              Excellent Prompt
────────────────────────────────────────────────────────────────────────►

"fix this"          "my script         "This bash script    "Debug this bash
                    is broken"          fails with error     script that processes
                                        code 1"              log files. It fails
                                                            with 'file not found'
                                                            on line 23. I'm running
                                                            Ubuntu 22.04. Here's
                                                            the script: [code]
                                                            And here's the error:
                                                            [output]"
```

---

## 3.2 The CRAFT Framework for Effective Prompts

I've developed the **CRAFT** framework specifically for DevOps prompting:

```
┌────────────────────────────────────────────────────────────────┐
│                    THE CRAFT FRAMEWORK                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   C - CONTEXT                                                  │
│       Provide relevant background information                  │
│       Environment, versions, constraints                       │
│                                                                │
│   R - ROLE                                                     │
│       Define who the AI should be                              │
│       Expert level, perspective, focus area                    │
│                                                                │
│   A - ACTION                                                   │
│       Specify exactly what you want done                       │
│       Clear, actionable request                                │
│                                                                │
│   F - FORMAT                                                   │
│       Describe the desired output format                       │
│       Code, list, table, step-by-step                          │
│                                                                │
│   T - TARGET                                                   │
│       Define success criteria                                  │
│       What does "done" look like?                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### CRAFT Example: Complete Prompt

```markdown
# Bad Prompt
"Write a monitoring script"

# CRAFT Prompt

## Context
I'm running a Kubernetes cluster on AWS EKS (v1.28) with 20 microservices.
We use Prometheus for metrics and AlertManager for alerting.
Our team is on-call 24/7 and gets paged via PagerDuty.

## Role
Act as a senior SRE with expertise in Kubernetes monitoring and incident response.

## Action
Create a Python script that:
1. Queries Prometheus for pod restart counts in the last hour
2. Identifies pods with more than 3 restarts
3. Fetches the last 50 log lines from those pods
4. Sends a summary to our Slack webhook if issues are found

## Format
Provide:
- Complete, production-ready Python script
- Requirements.txt with dependencies
- Brief explanation of each function
- Example cron job for scheduling

## Target
The script should:
- Handle connection errors gracefully
- Support multiple namespaces (configurable via env var)
- Complete in under 60 seconds
- Be idempotent (safe to run multiple times)
```

---

## 3.3 Prompting Techniques

### Technique 1: Zero-Shot Prompting

Ask directly without examples.

```markdown
# Zero-Shot Example

**Prompt:**
Convert this JSON to YAML:
{
  "apiVersion": "v1",
  "kind": "ConfigMap",
  "metadata": {
    "name": "app-config"
  }
}

**Response:**
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
```

**Best for:** Simple, unambiguous tasks where the AI knows the format.

### Technique 2: One-Shot Prompting

Provide one example to guide the format.

```markdown
# One-Shot Example

**Prompt:**
I need to document my bash functions in a specific format.

Example:
Function: backup_database
Purpose: Creates a timestamped backup of the PostgreSQL database
Parameters:
  - $1: Database name
  - $2: Output directory
Returns: 0 on success, 1 on failure
Example: backup_database myapp /var/backups

Now document this function:
```bash
deploy_app() {
  local env=$1
  local version=$2
  kubectl set image deployment/app app=myapp:$version -n $env
  kubectl rollout status deployment/app -n $env
}
```

**Response:**
Function: deploy_app
Purpose: Deploys a new version of the application to a specified environment
Parameters:
  - $1: Environment name (e.g., staging, production)
  - $2: Application version/tag to deploy
Returns: Exit code from kubectl rollout status
Example: deploy_app staging v1.2.3
```

**Best for:** When you need consistent formatting or style.

### Technique 3: Few-Shot Prompting

Provide multiple examples for complex patterns.

```markdown
# Few-Shot Example for Log Parsing

**Prompt:**
Parse these log lines into structured JSON.

Example 1:
Input: 2024-01-15 10:23:45 ERROR [auth-service] Failed login attempt for user john@example.com from IP 192.168.1.100
Output: {"timestamp": "2024-01-15 10:23:45", "level": "ERROR", "service": "auth-service", "message": "Failed login attempt", "user": "john@example.com", "ip": "192.168.1.100"}

Example 2:
Input: 2024-01-15 10:24:01 INFO [api-gateway] Request processed in 234ms - endpoint=/api/users method=GET status=200
Output: {"timestamp": "2024-01-15 10:24:01", "level": "INFO", "service": "api-gateway", "message": "Request processed", "duration_ms": 234, "endpoint": "/api/users", "method": "GET", "status": 200}

Example 3:
Input: 2024-01-15 10:24:15 WARN [db-connector] Connection pool at 80% capacity - active=40 max=50
Output: {"timestamp": "2024-01-15 10:24:15", "level": "WARN", "service": "db-connector", "message": "Connection pool at 80% capacity", "active_connections": 40, "max_connections": 50}

Now parse this:
Input: 2024-01-15 10:25:00 ERROR [payment-service] Transaction failed for order #12345 - reason=insufficient_funds amount=99.99
```

**Best for:** Complex patterns, consistent output format, domain-specific parsing.

### Technique 4: Chain-of-Thought (CoT) Prompting

Ask the AI to think step-by-step.

```markdown
# Chain-of-Thought Example

**Prompt:**
I'm seeing high latency on my API endpoint. Think through this step-by-step:

Current situation:
- Endpoint: GET /api/products
- Average latency: 2.5 seconds (should be <200ms)
- Database: PostgreSQL RDS
- Cache: Redis (ElastiCache)
- No recent deployments

Walk me through how you would diagnose this issue, explaining your reasoning at each step.

**Response:**
Let me think through this systematically:

**Step 1: Identify where the time is spent**
Reasoning: 2.5s is 10x our target. First, I need to determine if the delay is in:
- Network (unlikely for internal services)
- Application code (business logic)
- Database queries
- Cache operations
- External service calls

Action: Check application traces/APM data for timing breakdown.

**Step 2: Check database performance**
Reasoning: PostgreSQL is often the bottleneck. With no recent deployments, this could be:
- Query plan changes (statistics drift)
- Table bloat requiring VACUUM
- Lock contention
- Connection pool exhaustion

Action: Run `SELECT * FROM pg_stat_activity WHERE state != 'idle'` and check for slow queries.

**Step 3: Verify cache effectiveness**
Reasoning: If Redis cache miss rate increased, every request hits the database.
Action: Check Redis hit rate: `redis-cli info stats | grep keyspace`
If hit rate dropped, investigate:
- Key expiration settings
- Memory eviction (check maxmemory-policy)
- Network latency to Redis

... [continues with structured reasoning]
```

**Best for:** Debugging, architecture decisions, complex problem-solving.

### Technique 5: Role-Based Prompting

Assign a specific expert role.

```markdown
# Role-Based Examples

**Security Focus:**
You are a senior security engineer conducting a code review.
Analyze this Dockerfile for security vulnerabilities and suggest fixes:

FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl wget
COPY . /app
RUN chmod 777 /app
USER root
CMD ["python", "/app/server.py"]


**Performance Focus:**
You are a performance engineer specializing in container optimization.
Review this Dockerfile for performance issues and optimization opportunities:

[same Dockerfile]


**Cost Optimization Focus:**
You are a FinOps engineer focused on cloud cost optimization.
Analyze this Dockerfile and suggest ways to reduce compute costs:

[same Dockerfile]
```

Each role will provide different, valuable perspectives!

### Technique 6: Constraint-Based Prompting

Define boundaries and limitations.

```markdown
# Constraint-Based Example

**Prompt:**
Write a bash script to clean up old Docker images.

**Constraints:**
- Must work on Ubuntu 20.04 and 22.04
- Cannot use any external tools (only bash built-ins and standard coreutils)
- Must preserve images used in the last 7 days
- Must require confirmation before deletion
- Must log all actions to /var/log/docker-cleanup.log
- Script must complete in under 60 seconds
- Must handle the case where Docker daemon is not running
- Must be idempotent

**Do NOT:**
- Use `docker system prune` (too aggressive)
- Delete images with specific tags: latest, stable, prod-*
- Run as root (use sudo only where necessary)
```

**Best for:** Production code, security-sensitive tasks, compliance requirements.

---

## 3.4 DevOps-Specific Prompting Patterns

### Pattern 1: The Troubleshooting Template

```markdown
## Issue Description
[Brief description of the problem]

## Environment
- OS: [Ubuntu 22.04 / Amazon Linux 2 / etc.]
- Tool versions:
  - Docker: [version]
  - Kubernetes: [version]
  - Other relevant tools: [versions]
- Infrastructure: [AWS/GCP/Azure/on-prem]
- Time when issue started: [timestamp]

## What I've Already Tried
1. [First thing you tried]
2. [Second thing you tried]
3. [etc.]

## Relevant Logs/Output
```
[Paste error messages, logs, command output]
```

## Expected Behavior
[What should happen]

## Actual Behavior
[What is actually happening]

## Questions
1. What could be causing this?
2. What additional information should I gather?
3. What are the next steps to resolve this?
```

### Pattern 2: The Code Review Request

```markdown
## Code Review Request

### Context
- Purpose: [What this code does]
- Language/Tool: [Python/Bash/Terraform/etc.]
- Criticality: [High/Medium/Low]
- Runs in: [Production/Staging/Development]

### Code to Review
```[language]
[Your code here]
```

### Specific Concerns
- [ ] Security vulnerabilities
- [ ] Performance issues
- [ ] Error handling
- [ ] Best practices
- [ ] Documentation

### Please Provide
1. Critical issues that must be fixed
2. Improvements that should be made
3. Nice-to-have suggestions
4. Revised code with fixes applied
```

### Pattern 3: The Infrastructure Generation Request

```markdown
## Infrastructure Request

### Overview
Generate [Terraform/CloudFormation/Pulumi] code for [description].

### Requirements
- Cloud provider: [AWS/GCP/Azure]
- Region: [specific region]
- Environment: [dev/staging/prod]

### Components Needed
1. [Component 1 with specifications]
2. [Component 2 with specifications]
3. [etc.]

### Constraints
- Budget: [monthly budget if relevant]
- Compliance: [HIPAA/SOC2/PCI-DSS/none]
- Network: [VPC requirements]
- Security: [specific security requirements]

### Expected Outputs
- [ ] Main infrastructure code
- [ ] Variables file with descriptions
- [ ] Example tfvars for each environment
- [ ] README with usage instructions
```

### Pattern 4: The Migration Planning Request

```markdown
## Migration Planning Request

### Current State
- Source: [Current system/tool/platform]
- Version: [Current version]
- Scale: [Number of users/requests/data size]
- Dependencies: [List of integrations]

### Target State
- Destination: [New system/tool/platform]
- Version: [Target version]
- Timeline: [Desired completion]

### Constraints
- Maximum downtime: [X hours/minutes]
- Budget: [If relevant]
- Team size: [Number of engineers available]

### Risk Tolerance
- Data loss tolerance: [None/Minimal/Some acceptable]
- Rollback requirement: [Must be possible/Nice to have/Not needed]

### Please Provide
1. Step-by-step migration plan
2. Risk assessment for each step
3. Rollback procedures
4. Testing checklist
5. Communication template for stakeholders
```

---

## 3.5 Advanced Prompting Techniques

### Technique: Prompt Chaining

Break complex tasks into connected prompts.

```markdown
## Prompt Chain: Building a CI/CD Pipeline

### Prompt 1: Architecture Design
"Design a CI/CD pipeline architecture for a Python microservices application.
We use GitHub for code, need to deploy to Kubernetes on AWS.
Output: Architecture diagram in ASCII and list of required components."

### Prompt 2: GitHub Actions Workflow (uses output from Prompt 1)
"Based on this architecture:
[paste Prompt 1 output]

Create the GitHub Actions workflow file for the CI portion (build and test)."

### Prompt 3: Kubernetes Manifests (continues the chain)
"Now create the Kubernetes deployment manifests that the workflow will use.
Consider the artifacts produced by this workflow:
[paste Prompt 2 output]"

### Prompt 4: Security Review (validates the chain)
"Review this complete CI/CD setup for security issues:
Architecture: [Prompt 1 output]
Workflow: [Prompt 2 output]
Manifests: [Prompt 3 output]"
```

### Technique: Self-Correction Prompting

Ask the AI to verify its own output.

```markdown
## Self-Correction Example

**Initial Prompt:**
Write a Terraform configuration for an AWS Lambda function with API Gateway.

**Follow-up Prompt:**
Now review the Terraform code you just wrote:
1. Does it follow AWS best practices?
2. Are there any security issues?
3. Will it actually work if I run `terraform apply`?
4. What's missing that I'll need to add?

Please provide a corrected version with any issues fixed.
```

### Technique: Comparative Analysis Prompting

```markdown
## Comparative Analysis Example

**Prompt:**
Compare these three approaches for implementing blue-green deployments on Kubernetes:

Approach A: Using Kubernetes native deployments with service switching
Approach B: Using Istio service mesh traffic splitting
Approach C: Using Argo Rollouts

For each approach, analyze:
1. Implementation complexity (1-10)
2. Operational overhead (1-10)
3. Rollback speed
4. Resource requirements
5. Best use cases
6. Potential pitfalls

Present the comparison in a table, then provide a recommendation based on:
- Team of 3 DevOps engineers
- 20 microservices
- Moderate traffic (10K requests/minute)
- Limited Kubernetes experience
```

### Technique: Adversarial Prompting (for Security)

```markdown
## Adversarial Prompt Example

**Prompt:**
You are a red team security expert. Review this Kubernetes deployment manifest
and identify every possible security vulnerability and attack vector:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: DB_PASSWORD
          value: "supersecret123"
        securityContext:
          privileged: true
```

For each vulnerability:
1. Explain the risk
2. Provide the attack scenario
3. Show the remediation
4. Rate severity (Critical/High/Medium/Low)
```

---

## 3.6 Common Prompting Mistakes

### Mistake 1: Being Too Vague

```markdown
# Bad
"How do I deploy?"

# Good
"How do I deploy a Dockerized Python Flask application to AWS EKS using GitHub Actions?"
```

### Mistake 2: Not Providing Context

```markdown
# Bad
"Why is my pod crashing?"

# Good
"My Kubernetes pod is in CrashLoopBackOff status.

Environment: EKS 1.28, namespace: production
Pod name: api-server-5d4f7b8c9-x2k3j

Here are the recent events:
```
kubectl describe pod api-server-5d4f7b8c9-x2k3j
[paste output]
```

And the logs:
```
kubectl logs api-server-5d4f7b8c9-x2k3j --previous
[paste output]
```

What's causing the crash and how do I fix it?"
```

### Mistake 3: Asking for Too Much at Once

```markdown
# Bad (Too much at once)
"Create a complete CI/CD pipeline with testing, security scanning, multi-environment
deployment, rollback capabilities, monitoring integration, and documentation."

# Good (Broken into steps)
"Let's build a CI/CD pipeline step by step.

Step 1: Create the basic GitHub Actions workflow that:
- Triggers on push to main
- Runs Python unit tests
- Builds a Docker image

I'll share the repo structure:
[paste structure]

We can add more features after this works."
```

### Mistake 4: Not Specifying the Output Format

```markdown
# Bad
"List some Kubernetes monitoring tools."

# Good
"List Kubernetes monitoring tools in a comparison table with columns:
| Tool | Type | Pros | Cons | Best For | License |

Include: Prometheus, Datadog, New Relic, Grafana, Elastic APM"
```

### Mistake 5: Ignoring the AI's Limitations

```markdown
# Bad (Asking for real-time data)
"What's the current price of AWS m5.large instances?"

# Good (Acknowledging limitations)
"What was the approximate pricing structure for AWS m5.large instances
as of your knowledge cutoff? I'll verify current prices on AWS.

Also, what factors affect EC2 pricing that I should consider?"
```

---

## 3.7 Prompting Tips and Tricks

### Tip 1: Use Delimiters for Clarity

```markdown
# Use clear separators for different sections

---
CONTEXT:
Running on Ubuntu 22.04, Kubernetes 1.28, Helm 3.12
---
CURRENT CONFIGURATION:
```yaml
apiVersion: v1
kind: ConfigMap
# ... config here
```
---
PROBLEM:
The ConfigMap isn't being picked up by pods after update
---
QUESTION:
How do I make pods automatically reload when ConfigMap changes?
---
```

### Tip 2: Specify What NOT to Do

```markdown
# Tell the AI what to avoid

"Write a bash script to clean up log files.

Do NOT:
- Delete files from the last 24 hours
- Use rm -rf
- Require root privileges
- Affect files in /var/log/audit

DO:
- Only target *.log files
- Use find with -mtime
- Create a dry-run mode
- Log all deletions"
```

### Tip 3: Request Explanations with Code

```markdown
"Write the Terraform code for an RDS instance.

For each resource block, include a comment explaining:
- What the resource does
- Why each important attribute is set
- What would happen if it were omitted

This is for training junior engineers."
```

### Tip 4: Use Personas for Different Perspectives

```markdown
# Get multiple viewpoints on the same problem

"Evaluate this architecture decision from three perspectives:

1. As a DEVELOPER: Focus on usability and development experience
2. As an SRE: Focus on reliability and operational burden
3. As a SECURITY ENGINEER: Focus on attack surface and vulnerabilities

The decision: Moving from REST APIs to gRPC for internal microservice communication"
```

### Tip 5: Iterate and Refine

```markdown
# First attempt
"Write a script to backup databases"

# After seeing output, refine
"Good start. Now modify the script to:
- Add error handling for connection failures
- Include progress output
- Compress backups with gzip
- Verify backup integrity after creation"

# Further refinement
"Perfect. One more change:
- Add support for multiple databases from a config file
- Send a Slack notification when complete"
```

### Tip 6: Use Markdown Formatting in Prompts

````markdown
The AI understands markdown, so use it!

```
### Request
I need help with **Kubernetes networking**.

### Specifically:
1. How does `kube-proxy` work?
2. What's the difference between:
   - `ClusterIP`
   - `NodePort`
   - `LoadBalancer`

### Format
- Use code blocks for examples
- Include diagrams if possible (ASCII)
- Highlight **important** concepts
```
````

---

## 3.8 Building a Prompt Library

### Create Reusable Prompt Templates

```yaml
# ~/.ai-prompts/devops-templates.yaml

incident_response:
  template: |
    ## Incident Analysis Request

    **Severity:** {severity}
    **Service Affected:** {service}
    **Start Time:** {start_time}
    **Duration:** {duration}

    ### Symptoms
    {symptoms}

    ### Error Messages
    ```
    {error_logs}
    ```

    ### Timeline of Events
    {timeline}

    ### Questions
    1. What is the likely root cause?
    2. What immediate actions should we take?
    3. What should we check to confirm?
    4. How do we prevent this in the future?

code_review:
  template: |
    ## Code Review: {file_type}

    **Purpose:** {purpose}
    **Risk Level:** {risk_level}

    ```{language}
    {code}
    ```

    Review for:
    - [ ] Security vulnerabilities
    - [ ] Performance issues
    - [ ] Error handling
    - [ ] Best practices for {language}

terraform_request:
  template: |
    ## Terraform Request

    **Provider:** {provider}
    **Module Name:** {module_name}

    ### Resources Needed
    {resources}

    ### Variables Required
    {variables}

    ### Constraints
    {constraints}

    Generate production-ready Terraform code with:
    - Proper variable definitions
    - Output values
    - Data sources where appropriate
    - Tags for cost allocation
```

### Shell Function for Quick Prompts

```bash
# Add to ~/.bashrc or ~/.zshrc

# Quick prompt helper for DevOps tasks
ai_prompt() {
    local task_type=$1
    shift

    case $task_type in
        "debug")
            echo "## Debug Request

Environment: $(uname -a)

Issue: $*

Please:
1. Identify potential causes
2. Suggest diagnostic commands
3. Provide solution steps"
            ;;

        "review")
            echo "## Code Review Request

Please review this for:
- Security issues
- Performance problems
- Best practices
- Error handling

Code:
\`\`\`
$(cat $1)
\`\`\`"
            ;;

        "explain")
            echo "## Explanation Request

Explain this in DevOps context:

Topic: $*

Cover:
1. What it is
2. Why it matters
3. Practical example
4. Common pitfalls"
            ;;

        *)
            echo "Usage: ai_prompt [debug|review|explain] [args]"
            ;;
    esac
}

# Usage:
# ai_prompt debug "My pods are getting OOMKilled"
# ai_prompt review deployment.yaml
# ai_prompt explain "Kubernetes service mesh"
```

---

## 3.9 Hands-On Exercises

### Exercise 1: Prompt Improvement Practice

```markdown
## Improve These Prompts

Transform each bad prompt into a good one using CRAFT:

### Prompt 1 (Bad)
"Help me with Docker"

Your improved version:
```
[Write your improved prompt here]
```

### Prompt 2 (Bad)
"Write a script"

Your improved version:
```
[Write your improved prompt here]
```

### Prompt 3 (Bad)
"My server is slow"

Your improved version:
```
[Write your improved prompt here]
```
```

### Exercise 2: Build Your Prompt Template

```markdown
## Create Your Own Template

Think of a task you do frequently and create a reusable prompt template:

### Task: ____________________

### Template:
```
## [Task Name]

### Context
- Environment:
- Current situation:

### Goal
[What you want to achieve]

### Constraints
- Must:
- Must not:

### Expected Output
[Describe the format and content]

### Additional Information
[Space for variable details]
```

### Example Usage:
[Show how you would fill in the template]
```

### Exercise 3: Prompt Chain Design

```markdown
## Design a Prompt Chain

Task: Create a prompt chain for migrating a monolithic application to microservices.

### Chain Step 1: Analysis
Prompt:
```
[Your prompt to analyze the monolith]
```

### Chain Step 2: Service Identification
Prompt (uses Step 1 output):
```
[Your prompt to identify microservice boundaries]
```

### Chain Step 3: Architecture Design
Prompt (uses Step 2 output):
```
[Your prompt to design the microservices architecture]
```

### Chain Step 4: Implementation Plan
Prompt (uses Step 3 output):
```
[Your prompt to create the migration plan]
```
```

---

## 3.10 Chapter Summary

### Key Takeaways

1. **Good prompts = Good outputs** - The quality of your input directly affects the response quality

2. **Use the CRAFT framework** - Context, Role, Action, Format, Target

3. **Choose the right technique** - Zero-shot for simple, few-shot for patterns, chain-of-thought for complex reasoning

4. **Be specific and provide context** - Include versions, environments, constraints

5. **Build a prompt library** - Create reusable templates for common tasks

6. **Iterate and refine** - Rarely is the first prompt perfect; improve based on results

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│              PROMPTING QUICK REFERENCE                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  CRAFT Framework:                                              │
│  C - Context (environment, versions, constraints)              │
│  R - Role (who should the AI be)                               │
│  A - Action (what to do)                                       │
│  F - Format (how to output)                                    │
│  T - Target (success criteria)                                 │
│                                                                │
│  Techniques:                                                   │
│  • Zero-shot: Direct question                                  │
│  • One-shot: One example                                       │
│  • Few-shot: Multiple examples                                 │
│  • Chain-of-thought: Step-by-step reasoning                    │
│  • Role-based: Expert persona                                  │
│  • Constraint-based: Define boundaries                         │
│                                                                │
│  Common Mistakes:                                              │
│  ✗ Too vague                                                   │
│  ✗ Missing context                                             │
│  ✗ Asking too much at once                                     │
│  ✗ Not specifying format                                       │
│  ✗ Ignoring limitations                                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: Understanding LLMs and Tokens](./02-understanding-llms-and-tokens.md) | [Next: AI Models Landscape →](./04-ai-models-landscape.md)
