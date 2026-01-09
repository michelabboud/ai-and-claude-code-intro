#!/usr/bin/env python3
"""
Chapter 5: Introduction to Claude
Claude API Usage Examples for DevOps

Examples of using Claude API directly for automation.
"""

from typing import Optional, List
from dataclasses import dataclass
import json


@dataclass
class ClaudeConfig:
    """Configuration for Claude API usage."""
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.7


def select_claude_model(
    task: str,
    speed: str = "standard",
    cost: str = "moderate"
) -> str:
    """
    Select the appropriate Claude model for a task.

    Args:
        task: Type of task (code, analysis, quick_answer)
        speed: Required speed (fast, standard, slow_ok)
        cost: Budget (low, moderate, high)

    Returns:
        Model identifier string.
    """
    # Model selection matrix
    if task in ["architecture", "complex_analysis", "security_audit"]:
        if cost == "high":
            return "claude-opus-4-20250514"
        return "claude-sonnet-4-20250514"

    if task in ["quick_answer", "formatting", "simple_query"]:
        if speed == "fast":
            return "claude-3-5-haiku-20241022"
        return "claude-3-5-sonnet-20241022"

    if task in ["code_generation", "code_review", "documentation"]:
        return "claude-sonnet-4-20250514"

    # Default to Sonnet for balanced performance
    return "claude-sonnet-4-20250514"


# =============================================================================
# ANTHROPIC DIRECT API EXAMPLE
# =============================================================================

def anthropic_api_example():
    """
    Example of using Anthropic's Python SDK.

    Install: pip install anthropic
    """
    example_code = '''
import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key"  # Or set ANTHROPIC_API_KEY env var
)

# Simple message
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Analyze this Kubernetes deployment for issues: ..."
        }
    ]
)

print(message.content[0].text)

# With system prompt for DevOps context
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system="""You are a senior DevOps engineer with expertise in:
- Kubernetes and container orchestration
- Cloud infrastructure (AWS, GCP, Azure)
- CI/CD pipelines and GitOps
- Infrastructure as Code (Terraform, Pulumi)
- Monitoring and observability

When analyzing code or configurations:
1. Check for security issues first
2. Identify performance problems
3. Suggest best practices
4. Provide actionable fixes with code examples""",
    messages=[
        {
            "role": "user",
            "content": "Review this Terraform module for security issues: ..."
        }
    ]
)

print(message.content[0].text)
'''
    return example_code


# =============================================================================
# AWS BEDROCK EXAMPLE
# =============================================================================

def aws_bedrock_example():
    """
    Example of using Claude via AWS Bedrock.

    Install: pip install boto3
    """
    example_code = '''
import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"  # Or your region
)

# Prepare request
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "user",
            "content": "Generate a CloudFormation template for a VPC with public and private subnets"
        }
    ],
    "system": "You are an AWS solutions architect. Provide production-ready templates."
})

# Call Claude via Bedrock
response = bedrock.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    body=body,
    contentType="application/json",
    accept="application/json"
)

# Parse response
result = json.loads(response["body"].read())
print(result["content"][0]["text"])
'''
    return example_code


# =============================================================================
# GOOGLE CLOUD VERTEX AI EXAMPLE
# =============================================================================

def gcp_vertex_ai_example():
    """
    Example of using Claude via Google Cloud Vertex AI.

    Install: pip install google-cloud-aiplatform anthropic[vertex]
    """
    example_code = '''
from anthropic import AnthropicVertex

# Initialize client
client = AnthropicVertex(
    region="us-east5",  # Or your region
    project_id="your-gcp-project-id"
)

# Create message
message = client.messages.create(
    model="claude-sonnet-4@20250514",  # Vertex AI model name format
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Create a GKE cluster Terraform module with best practices"
        }
    ]
)

print(message.content[0].text)
'''
    return example_code


# =============================================================================
# VISION CAPABILITIES
# =============================================================================

def vision_example():
    """
    Example of using Claude's vision capabilities.

    Useful for:
    - Analyzing architecture diagrams
    - Reading screenshots of errors
    - Understanding monitoring dashboards
    """
    example_code = '''
import anthropic
import base64

client = anthropic.Anthropic()

# Read image file
with open("architecture-diagram.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

# Analyze the image
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
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
                    "text": """Analyze this architecture diagram and:
1. Identify potential single points of failure
2. Suggest improvements for high availability
3. Note any security concerns with the design
4. Recommend monitoring points"""
                }
            ],
        }
    ],
)

print(message.content[0].text)
'''
    return example_code


# =============================================================================
# STREAMING FOR LONG RESPONSES
# =============================================================================

def streaming_example():
    """
    Example of streaming responses for long outputs.

    Useful for:
    - Long code generation
    - Detailed analysis
    - Real-time feedback in CLI tools
    """
    example_code = '''
import anthropic

client = anthropic.Anthropic()

# Stream the response
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=8192,
    messages=[
        {
            "role": "user",
            "content": "Generate a comprehensive CI/CD pipeline for a microservices application"
        }
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # Final newline
'''
    return example_code


# =============================================================================
# DEVOPS PROMPT PATTERNS
# =============================================================================

DEVOPS_PROMPTS = {
    "code_review": {
        "system": """You are a senior DevOps engineer reviewing code.
Focus on: security, performance, error handling, and best practices.
Always provide specific line numbers and code examples for fixes.""",
        "temperature": 0.3,  # Lower for more consistent reviews
    },

    "troubleshooting": {
        "system": """You are an SRE investigating a production incident.
Approach systematically: gather data, form hypotheses, test, and verify.
Provide specific commands and explain your reasoning.""",
        "temperature": 0.5,
    },

    "infrastructure": {
        "system": """You are a cloud architect designing infrastructure.
Prioritize: security, cost-efficiency, scalability, and maintainability.
Always include proper tagging, monitoring, and documentation.""",
        "temperature": 0.7,  # More creative for architecture
    },

    "documentation": {
        "system": """You are a technical writer creating DevOps documentation.
Write clearly, include examples, and anticipate common questions.
Format with proper markdown and code blocks.""",
        "temperature": 0.6,
    },
}


def get_devops_config(task_type: str) -> dict:
    """Get the recommended configuration for a DevOps task type."""
    return DEVOPS_PROMPTS.get(task_type, DEVOPS_PROMPTS["infrastructure"])


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CLAUDE API EXAMPLES FOR DEVOPS")
    print("=" * 60)

    print("\n--- Model Selection ---")
    print(f"Code review: {select_claude_model('code_review')}")
    print(f"Quick answer: {select_claude_model('quick_answer', speed='fast')}")
    print(f"Architecture: {select_claude_model('architecture', cost='high')}")

    print("\n--- DevOps Config ---")
    config = get_devops_config("code_review")
    print(f"System prompt: {config['system'][:100]}...")
    print(f"Temperature: {config['temperature']}")

    print("\n--- API Examples ---")
    print("See the example functions for complete API usage patterns:")
    print("- anthropic_api_example()")
    print("- aws_bedrock_example()")
    print("- gcp_vertex_ai_example()")
    print("- vision_example()")
    print("- streaming_example()")
