# Chapter 5: Introduction to Claude

## Meet Your AI Colleague

Claude is Anthropic's family of AI assistants, designed to be helpful, harmless, and honest. In this chapter, we'll explore what makes Claude unique and how to use it effectively for DevOps tasks.

---

## 5.1 What is Claude?

### The Basics

**Claude** is a family of large language models created by **Anthropic**, an AI safety company founded in 2021 by former members of OpenAI.

```
┌────────────────────────────────────────────────────────────────┐
│                    CLAUDE AT A GLANCE                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Creator: Anthropic                                            │
│  Founded: 2021                                                 │
│  Mission: AI safety research                                   │
│                                                                │
│  Key Differentiators:                                          │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  • Constitutional AI - trained with safety principles     │ │
│  │  • Honest about limitations and uncertainties             │ │
│  │  • 200K token context window (one of the largest)         │ │
│  │  • Strong reasoning and analysis capabilities             │ │
│  │  • Excellent at following complex instructions            │ │
│  │  • Natural, conversational communication style            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  Available Via:                                                │
│  • claude.ai (web interface)                                   │
│  • API (api.anthropic.com)                                     │
│  • AWS Bedrock                                                 │
│  • Google Cloud Vertex AI                                      │
│  • Claude Code (CLI tool)                                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Claude's Design Philosophy

```yaml
# The Three H's of Claude

helpful:
  description: "Claude aims to be genuinely useful"
  examples:
    - "Provides working code, not just theory"
    - "Asks clarifying questions when needed"
    - "Suggests alternatives when requests are unclear"
    - "Explains reasoning behind recommendations"

harmless:
  description: "Claude is designed to avoid harmful outputs"
  examples:
    - "Won't help with malicious hacking"
    - "Refuses to generate dangerous content"
    - "Considers security implications in code"
    - "Points out potential risks in approaches"

honest:
  description: "Claude is transparent about its limitations"
  examples:
    - "Admits when it doesn't know something"
    - "Acknowledges uncertainty in responses"
    - "Won't make up information to seem helpful"
    - "Distinguishes between fact and opinion"
```

---

## 5.2 The Claude Model Family

### Current Claude 3 Models

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       CLAUDE 3 MODEL FAMILY                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ╔═══════════════════════════════════════════════════════════════════╗    │
│  ║  CLAUDE 3.5 SONNET                                                ║    │
│  ║  "The Sweet Spot"                                                 ║    │
│  ║                                                                   ║    │
│  ║  • Best balance of intelligence, speed, and cost                  ║    │
│  ║  • Excellent for code generation and analysis                     ║    │
│  ║  • Great at complex reasoning                                     ║    │
│  ║  • Recommended for most DevOps tasks                              ║    │
│  ║  • 200K context window                                            ║    │
│  ║  • Vision capabilities (can analyze images)                       ║    │
│  ╚═══════════════════════════════════════════════════════════════════╝    │
│                                                                            │
│  ╔═══════════════════════════════════════════════════════════════════╗    │
│  ║  CLAUDE 3 OPUS                                                    ║    │
│  ║  "The Powerhouse"                                                 ║    │
│  ║                                                                   ║    │
│  ║  • Most capable model                                             ║    │
│  ║  • Best for complex analysis and reasoning                        ║    │
│  ║  • Excellent for architecture decisions                           ║    │
│  ║  • Higher cost per token                                          ║    │
│  ║  • Use when quality matters most                                  ║    │
│  ╚═══════════════════════════════════════════════════════════════════╝    │
│                                                                            │
│  ╔═══════════════════════════════════════════════════════════════════╗    │
│  ║  CLAUDE 3 HAIKU                                                   ║    │
│  ║  "The Speed Demon"                                                ║    │
│  ║                                                                   ║    │
│  ║  • Fastest response times                                         ║    │
│  ║  • Most cost-effective                                            ║    │
│  ║  • Great for simple tasks at scale                                ║    │
│  ║  • Perfect for chatbots and quick queries                         ║    │
│  ║  • Ideal for high-volume automation                               ║    │
│  ╚═══════════════════════════════════════════════════════════════════╝    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Model Selection for DevOps Tasks

```python
# Choosing the right Claude model for your task

def select_claude_model(task: dict) -> str:
    """
    Returns the recommended Claude model based on task requirements.
    """

    # Complex reasoning, architecture decisions, critical code review
    if task.get("complexity") == "high":
        return "claude-3-opus-20240229"

    # Most DevOps tasks: code generation, debugging, documentation
    if task.get("needs_code_quality"):
        return "claude-3-5-sonnet-20241022"

    # High volume, simple tasks, chatbots
    if task.get("high_volume") or task.get("simple"):
        return "claude-3-haiku-20240307"

    # Default: Sonnet is the best general choice
    return "claude-3-5-sonnet-20241022"


# Examples
print(select_claude_model({"complexity": "high"}))  # opus
print(select_claude_model({"needs_code_quality": True}))  # sonnet
print(select_claude_model({"high_volume": True}))  # haiku
```

### Pricing Comparison

```
Claude Model Pricing (per 1M tokens, as of 2024)
═══════════════════════════════════════════════════════════════════

Model              │ Input      │ Output     │ Best For
───────────────────┼────────────┼────────────┼──────────────────────
Claude 3 Opus      │ $15.00     │ $75.00     │ Complex analysis
Claude 3.5 Sonnet  │ $3.00      │ $15.00     │ Most tasks (default)
Claude 3 Haiku     │ $0.25      │ $1.25      │ High-volume simple

Cost Example: 100 code reviews per day
─────────────────────────────────────────────────────────────────────
Average: 2,000 input tokens, 500 output tokens per review
Monthly: 3,000 reviews

Opus:     Input: $90 + Output: $112.50 = $202.50/month
Sonnet:   Input: $18 + Output: $22.50  = $40.50/month
Haiku:    Input: $1.50 + Output: $1.87 = $3.37/month
```

---

## 5.3 Claude's Capabilities

### What Claude Excels At

```yaml
# Claude's Strengths for DevOps

code_generation:
  capability: "Excellent"
  examples:
    - "Generate Terraform modules from requirements"
    - "Write Kubernetes manifests"
    - "Create CI/CD pipelines"
    - "Build monitoring scripts"

code_review:
  capability: "Excellent"
  examples:
    - "Identify security vulnerabilities"
    - "Suggest performance improvements"
    - "Check for best practices"
    - "Explain complex code"

debugging:
  capability: "Excellent"
  examples:
    - "Analyze error messages and logs"
    - "Trace issues through stack traces"
    - "Suggest fixes based on symptoms"
    - "Explain root causes"

documentation:
  capability: "Excellent"
  examples:
    - "Generate README files"
    - "Create API documentation"
    - "Write runbooks"
    - "Document architecture decisions"

analysis:
  capability: "Excellent"
  examples:
    - "Compare architecture options"
    - "Risk assessment"
    - "Cost analysis"
    - "Security audit"

long_context:
  capability: "Industry-leading"
  window: "200K tokens"
  examples:
    - "Analyze entire log files"
    - "Review large codebases"
    - "Process extensive documentation"
```

### What Claude Cannot Do

```yaml
# Understanding Claude's Limitations

cannot_do:
  real_time_data:
    description: "Claude doesn't have access to current data"
    workaround: "Provide current data in your prompt"
    example: |
      # Don't ask: "What's the current AWS pricing?"
      # Instead: "Based on this pricing data [paste], which instance is cheapest?"

  execute_code:
    description: "Claude generates code but doesn't run it"
    workaround: "Use Claude Code or copy-paste to execute"
    exception: "Claude Code CAN execute code in your terminal"

  access_internet:
    description: "Claude can't browse the web during conversation"
    workaround: "Paste relevant content into your prompt"
    exception: "Some interfaces provide web access tools"

  remember_between_sessions:
    description: "Each conversation starts fresh"
    workaround: "Provide context at the start of each session"
    tip: "Save important prompts and context for reuse"

  access_your_systems:
    description: "Claude can't directly SSH to your servers"
    workaround: "Copy outputs for Claude to analyze"
    exception: "Claude Code can access local files and run commands"

knowledge_cutoff:
  description: "Training data has a cutoff date"
  impact:
    - "May not know newest tool versions"
    - "Recent security advisories might be missing"
    - "New cloud services might be unknown"
  workaround: "Provide documentation for new features"
```

---

## 5.4 How to Access Claude

### Option 1: Claude.ai Web Interface

```
┌────────────────────────────────────────────────────────────────┐
│                    CLAUDE.AI WEB INTERFACE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  URL: https://claude.ai                                        │
│                                                                │
│  Access Tiers:                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  FREE TIER                                                │ │
│  │  • Limited messages per day                               │ │
│  │  • Access to Claude 3.5 Sonnet                           │ │
│  │  • Good for learning and light usage                     │ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  CLAUDE PRO ($20/month)                                   │ │
│  │  • 5x more messages                                       │ │
│  │  • Priority access during peak times                      │ │
│  │  • Access to Claude 3 Opus                               │ │
│  │  • Early access to new features                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  CLAUDE TEAM ($25/user/month)                             │ │
│  │  • Everything in Pro                                      │ │
│  │  • Team collaboration features                            │ │
│  │  • Admin controls                                         │ │
│  │  • Higher usage limits                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  Best For:                                                     │
│  • Quick questions and exploration                             │
│  • One-off tasks                                               │
│  • Learning and experimentation                                │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Option 2: Anthropic API

```python
# Direct API access for programmatic use

# Installation
# pip install anthropic

import anthropic

# Initialize client
client = anthropic.Anthropic(
    api_key="your-api-key"  # Or set ANTHROPIC_API_KEY env var
)

# Simple message
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a Dockerfile for a Python Flask app"}
    ]
)

print(message.content[0].text)

# With system prompt
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a DevOps expert specializing in Kubernetes. Be concise.",
    messages=[
        {"role": "user", "content": "What's a good health check for nginx?"}
    ]
)

print(message.content[0].text)
```

### Option 3: AWS Bedrock

```python
# Claude via AWS Bedrock - Enterprise option

import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # or your preferred region
)

# Make request
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "Write a CloudFormation template for an S3 bucket with versioning"
            }
        ]
    })
)

# Parse response
result = json.loads(response['body'].read())
print(result['content'][0]['text'])
```

```yaml
# AWS Bedrock Benefits for Enterprise
benefits:
  - "VPC endpoints - data stays in your network"
  - "IAM integration - use existing access controls"
  - "CloudTrail logging - audit all AI usage"
  - "No separate API keys to manage"
  - "Consolidated billing through AWS"
  - "Compliance certifications"
```

### Option 4: Google Cloud Vertex AI

```python
# Claude via Google Cloud Vertex AI

from anthropic import AnthropicVertex

# Initialize with GCP project
client = AnthropicVertex(
    project_id="your-project-id",
    region="us-east5"  # Claude available regions
)

message = client.messages.create(
    model="claude-3-5-sonnet@20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain GKE Autopilot vs Standard mode"}
    ]
)

print(message.content[0].text)
```

### Option 5: Claude Code CLI (Covered in Next Chapters)

```bash
# The most powerful way to use Claude for DevOps

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Start interactive session
claude

# Or run single command
claude "Review my Dockerfile for security issues"
```

---

## 5.5 Using Claude Effectively

### Best Practices for DevOps Prompts

```yaml
# Effective prompting strategies for Claude

1_be_specific:
  bad: "Write a script"
  good: |
    Write a bash script that:
    - Runs on Ubuntu 22.04
    - Backs up PostgreSQL database named 'production'
    - Compresses with gzip
    - Uploads to S3 bucket 'my-backups'
    - Retains last 7 days of backups
    - Logs to syslog

2_provide_context:
  bad: "Why is my pod crashing?"
  good: |
    My Kubernetes pod is crashing with CrashLoopBackOff.

    Environment:
    - EKS 1.28, namespace: production
    - Pod: api-server-5d4f7b8c9-x2k3j

    Here's kubectl describe output:
    [paste output]

    And the logs:
    [paste logs]

    What's causing this and how do I fix it?

3_specify_format:
  bad: "List monitoring tools"
  good: |
    Compare Prometheus, Datadog, and New Relic in a table with columns:
    | Feature | Prometheus | Datadog | New Relic |

    Include: pricing model, Kubernetes support, alert capabilities,
    learning curve, and best use case.

4_iterative_refinement:
  approach: "Start simple, add requirements as needed"
  example:
    prompt_1: "Write a Terraform module for EC2"
    prompt_2: "Add auto-scaling based on CPU"
    prompt_3: "Add CloudWatch alarms for the scaling events"
    prompt_4: "Make the instance type configurable via variable"

5_use_system_prompts:
  purpose: "Set Claude's behavior for the entire conversation"
  example: |
    System: You are a senior SRE with 10 years of experience.
    Focus on reliability, observability, and security.
    Always consider failure modes and suggest monitoring.
    Prefer battle-tested solutions over cutting-edge.
```

### Example DevOps Conversations

#### Example 1: Debugging with Claude

```markdown
**You:** My nginx container keeps getting OOMKilled in Kubernetes. Here's the pod spec:

```yaml
containers:
- name: nginx
  image: nginx:1.24
  resources:
    limits:
      memory: "128Mi"
    requests:
      memory: "64Mi"
```

And this error from kubectl describe:
```
Last State: Terminated
Reason: OOMKilled
Exit Code: 137
```

What's wrong and how do I fix it?

**Claude:** The issue is that your memory limit of 128Mi is too low for nginx under your workload. Here's what's happening:

1. **Exit Code 137** = Container killed by SIGKILL (128 + 9)
2. **OOMKilled** = Kubernetes killed the container because it exceeded its memory limit

**Diagnosis steps:**
```bash
# Check actual memory usage before it crashes
kubectl top pod <pod-name>

# Check nginx worker processes and connections
kubectl exec -it <pod-name> -- nginx -T | grep worker
```

**Solutions (from least to most change):**

1. **Quick fix - Increase memory limit:**
```yaml
resources:
  limits:
    memory: "256Mi"  # Start here
  requests:
    memory: "128Mi"
```

2. **Better - Optimize nginx configuration:**
```nginx
# Add to nginx.conf
worker_processes 1;  # Reduce if you have multiple
worker_connections 512;  # Reduce from default 1024

# Disable unused modules, reduce buffers
client_body_buffer_size 8k;
client_header_buffer_size 1k;
```

3. **Best - Profile and right-size:**
```bash
# Monitor actual usage over time
kubectl top pod <pod-name> --containers
```
Then set requests to P50 usage and limits to P99 + 20% buffer.

Would you like me to help profile your nginx configuration?
```

#### Example 2: Generating Infrastructure Code

```markdown
**You:** Create a Terraform module for an AWS ALB that:
- Has HTTPS listener on 443
- Redirects HTTP to HTTPS
- Uses ACM certificate (provided as variable)
- Has health check on /health
- Outputs the ALB DNS name

**Claude:** Here's a complete Terraform module:

```hcl
# modules/alb/variables.tf
variable "name" {
  description = "Name prefix for ALB resources"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where ALB will be created"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for ALB (minimum 2 AZs)"
  type        = list(string)
}

variable "certificate_arn" {
  description = "ACM certificate ARN for HTTPS"
  type        = string
}

variable "target_group_port" {
  description = "Port on which targets receive traffic"
  type        = number
  default     = 80
}

variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/health"
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

# modules/alb/main.tf
resource "aws_lb" "main" {
  name               = "${var.name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.subnet_ids

  tags = merge(var.tags, {
    Name = "${var.name}-alb"
  })
}

resource "aws_security_group" "alb" {
  name        = "${var.name}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP (redirects to HTTPS)"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}

resource "aws_lb_target_group" "main" {
  name     = "${var.name}-tg"
  port     = var.target_group_port
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = var.health_check_path
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }

  tags = var.tags
}

# HTTPS Listener
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}

# HTTP to HTTPS redirect
resource "aws_lb_listener" "http_redirect" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# modules/alb/outputs.tf
output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ARN of the ALB"
  value       = aws_lb.main.arn
}

output "target_group_arn" {
  description = "ARN of the target group"
  value       = aws_lb_target_group.main.arn
}

output "security_group_id" {
  description = "Security group ID of the ALB"
  value       = aws_security_group.alb.id
}
```

**Usage:**
```hcl
module "alb" {
  source = "./modules/alb"

  name            = "my-app"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.public_subnet_ids
  certificate_arn = aws_acm_certificate.main.arn

  tags = {
    Environment = "production"
  }
}
```

Want me to add WAF integration or additional features?
```

---

## 5.6 Claude's Vision Capabilities

Claude 3 models can analyze images, which is useful for DevOps:

```python
# Using Claude's vision for DevOps tasks

import anthropic
import base64

client = anthropic.Anthropic()

# Read image file
with open("error_screenshot.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "This is a screenshot of an error from my monitoring dashboard. What does it indicate and how should I respond?"
                }
            ],
        }
    ],
)

print(message.content[0].text)
```

### Vision Use Cases for DevOps

```yaml
# Practical vision applications

architecture_diagrams:
  use_case: "Upload architecture diagram, get Terraform code"
  prompt: "Convert this architecture diagram to Terraform modules"

error_screenshots:
  use_case: "Analyze monitoring dashboard screenshots"
  prompt: "What does this Grafana dashboard show? Any concerns?"

log_images:
  use_case: "When logs are in image format (shared via Slack)"
  prompt: "Transcribe this log screenshot and identify the error"

network_diagrams:
  use_case: "Analyze network topology"
  prompt: "Review this network diagram for security concerns"

ui_testing:
  use_case: "Verify deployment results"
  prompt: "Does this screenshot show the expected application state?"
```

---

## 5.7 Hands-On Exercises

### Exercise 1: Explore Claude.ai

```markdown
## Exercise: Getting Started with Claude.ai

1. Go to https://claude.ai and create an account
2. Try these DevOps prompts:

### Prompt 1: Simple Code Generation
```
Write a bash function that checks if a service is running
and restarts it if not. Include logging.
```

### Prompt 2: Troubleshooting
```
Explain possible causes for this error:
"Error: ETIMEOUT: connect ETIMEDOUT 10.0.0.5:5432"

Context: This happens when my Kubernetes pod tries to connect
to PostgreSQL RDS. It works sometimes but fails intermittently.
```

### Prompt 3: Code Review
```
Review this Dockerfile for security and optimization:

FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD ["python3", "app.py"]
```

### Observations:
- Response quality:
- Response time:
- Useful suggestions:
- Any limitations noticed:
```

### Exercise 2: API Exploration

```python
# Exercise: Use the Claude API

# 1. Get an API key from console.anthropic.com
# 2. Install the SDK: pip install anthropic
# 3. Run this code:

import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Task: Modify this code to:
# 1. Add a system prompt for DevOps expertise
# 2. Ask Claude to generate a specific script
# 3. Save the response to a file

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ]
)

print(message.content[0].text)
```

### Exercise 3: Model Comparison

```markdown
## Exercise: Compare Claude Models

Use the same prompt with different models and compare:

### Prompt:
```
Write a Python script that:
1. Connects to AWS using boto3
2. Lists all EC2 instances across all regions
3. Identifies instances without required tags (Name, Environment, Owner)
4. Outputs results as JSON
```

### Test with:
- Claude 3.5 Sonnet
- Claude 3 Haiku
- Claude 3 Opus (if available)

### Comparison:

| Aspect | Sonnet | Haiku | Opus |
|--------|--------|-------|------|
| Code Quality | | | |
| Error Handling | | | |
| Comments | | | |
| Response Time | | | |
| Edge Cases | | | |
```

---

## 5.8 Chapter Summary

### Key Takeaways

1. **Claude is Anthropic's AI assistant** - Designed to be helpful, harmless, and honest

2. **Three main models**: Opus (most capable), Sonnet (balanced), Haiku (fastest/cheapest)

3. **Multiple access options**: Web interface, API, AWS Bedrock, GCP Vertex AI, Claude Code

4. **200K token context window** - Can process large codebases and log files

5. **Vision capabilities** - Can analyze images for DevOps use cases

6. **Effective prompting matters** - Be specific, provide context, specify format

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│                    CLAUDE QUICK REFERENCE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Model Selection:                                              │
│  • Complex reasoning → Claude 3 Opus                          │
│  • General DevOps → Claude 3.5 Sonnet (default)               │
│  • High volume/simple → Claude 3 Haiku                        │
│                                                                │
│  Access Methods:                                               │
│  • Quick tasks → claude.ai                                    │
│  • Automation → API (api.anthropic.com)                       │
│  • Enterprise → AWS Bedrock or GCP Vertex AI                  │
│  • Coding → Claude Code CLI                                   │
│                                                                │
│  Best Practices:                                               │
│  • Be specific with requirements                               │
│  • Provide relevant context                                    │
│  • Specify output format                                       │
│  • Iterate and refine                                          │
│                                                                │
│  Context Window: 200K tokens                                   │
│  • ~150,000 words                                              │
│  • ~500 pages of text                                          │
│  • Entire codebases at once                                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: AI Models Landscape](./04-ai-models-landscape.md) | [Next: Claude Code Fundamentals →](./06-claude-code-fundamentals.md)
