#!/usr/bin/env python3
"""
Chapter 3: The Art of Prompting
CRAFT Framework Implementation

A Python module for building well-structured prompts.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Tone(Enum):
    """Tone options for prompts."""
    TECHNICAL = "technical and precise"
    FRIENDLY = "friendly and approachable"
    FORMAL = "formal and professional"
    CONCISE = "brief and to the point"
    EDUCATIONAL = "explanatory and educational"


class OutputFormat(Enum):
    """Output format options."""
    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    TABLE = "markdown table"
    BULLETS = "bullet points"
    NUMBERED = "numbered list"
    CODE = "code with comments"


@dataclass
class CRAFTPrompt:
    """
    Build prompts using the CRAFT framework.

    CRAFT stands for:
    - Context: Background information
    - Role: Who should the AI be?
    - Action: What should be done?
    - Format: How should output be structured?
    - Tone: What communication style?
    """

    # Required
    action: str

    # Optional with defaults
    context: str = ""
    role: str = ""
    output_format: OutputFormat = OutputFormat.MARKDOWN
    tone: Tone = Tone.TECHNICAL

    # Additional details
    constraints: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)

    def build(self) -> str:
        """Build the complete prompt string."""
        parts = []

        # Role (if specified)
        if self.role:
            parts.append(f"You are {self.role}.")

        # Context
        if self.context:
            parts.append(f"\n## Context\n{self.context}")

        # Action (always required)
        parts.append(f"\n## Task\n{self.action}")

        # Constraints
        if self.constraints:
            parts.append("\n## Constraints")
            for constraint in self.constraints:
                parts.append(f"- {constraint}")

        # Examples
        if self.examples:
            parts.append("\n## Examples")
            for example in self.examples:
                parts.append(f"```\n{example}\n```")

        # Format and Tone
        parts.append(f"\n## Output Requirements")
        parts.append(f"- Format: {self.output_format.value}")
        parts.append(f"- Tone: {self.tone.value}")

        return "\n".join(parts)


# =============================================================================
# PREDEFINED PROMPT BUILDERS
# =============================================================================

def build_troubleshooting_prompt(
    service: str,
    symptoms: str,
    logs: str,
    tried: Optional[List[str]] = None
) -> str:
    """Build a troubleshooting prompt."""
    tried_text = ""
    if tried:
        tried_text = "I've already tried:\n" + "\n".join(f"- {t}" for t in tried)

    prompt = CRAFTPrompt(
        role="a senior SRE with expertise in distributed systems and incident response",
        context=f"""
Service: {service}
Symptoms: {symptoms}
{tried_text}

Logs:
```
{logs}
```
""",
        action="""
Analyze this issue and provide:
1. Most likely root cause
2. Additional diagnostic steps to confirm
3. Recommended fix with specific commands
4. Prevention measures for the future
""",
        output_format=OutputFormat.MARKDOWN,
        tone=Tone.TECHNICAL,
        constraints=[
            "Focus on actionable solutions",
            "Include exact commands where applicable",
            "Consider impact before suggesting changes",
        ]
    )
    return prompt.build()


def build_code_review_prompt(
    code: str,
    language: str,
    focus_areas: Optional[List[str]] = None
) -> str:
    """Build a code review prompt."""
    if focus_areas is None:
        focus_areas = ["security", "performance", "error handling", "best practices"]

    prompt = CRAFTPrompt(
        role="a senior software engineer conducting a thorough code review",
        context=f"""
Language: {language}

Code to review:
```{language}
{code}
```
""",
        action=f"""
Review this code focusing on: {', '.join(focus_areas)}

For each issue found, provide:
- Severity (Critical/Major/Minor)
- Location (line number if possible)
- Description
- Suggested fix with code example
""",
        output_format=OutputFormat.MARKDOWN,
        tone=Tone.TECHNICAL,
        constraints=[
            "Prioritize security issues first",
            "Be specific about what's wrong and why",
            "Provide working code examples for fixes",
        ]
    )
    return prompt.build()


def build_infrastructure_prompt(
    description: str,
    cloud_provider: str,
    requirements: List[str],
    iac_tool: str = "terraform"
) -> str:
    """Build an infrastructure generation prompt."""
    prompt = CRAFTPrompt(
        role=f"a cloud architect specializing in {cloud_provider} and {iac_tool}",
        context=f"""
Cloud Provider: {cloud_provider}
IaC Tool: {iac_tool}
Project: {description}

Requirements:
{chr(10).join(f'- {r}' for r in requirements)}
""",
        action=f"""
Create production-ready {iac_tool} code that:
1. Implements all stated requirements
2. Follows {cloud_provider} best practices
3. Includes proper security configurations
4. Has sensible defaults with variable overrides
5. Includes comments explaining key decisions
""",
        output_format=OutputFormat.CODE,
        tone=Tone.TECHNICAL,
        constraints=[
            "Use modules where appropriate",
            "Include variable definitions with descriptions",
            "Add outputs for important resource attributes",
            "Follow security best practices (encryption, least privilege)",
        ]
    )
    return prompt.build()


def build_documentation_prompt(
    subject: str,
    doc_type: str,
    audience: str,
    source_material: str = ""
) -> str:
    """Build a documentation generation prompt."""
    prompt = CRAFTPrompt(
        role="a technical writer with deep DevOps expertise",
        context=f"""
Documentation Type: {doc_type}
Subject: {subject}
Target Audience: {audience}

Source Material:
{source_material if source_material else "Based on best practices and common patterns"}
""",
        action=f"""
Create comprehensive {doc_type} documentation that:
1. Is appropriate for the target audience
2. Includes practical examples
3. Covers common use cases and edge cases
4. Has clear structure with navigation
5. Includes troubleshooting section if applicable
""",
        output_format=OutputFormat.MARKDOWN,
        tone=Tone.EDUCATIONAL,
        constraints=[
            "Use clear, jargon-free language where possible",
            "Include code examples that actually work",
            "Add warnings for common pitfalls",
            "Structure with clear headings and sections",
        ]
    )
    return prompt.build()


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CRAFT FRAMEWORK EXAMPLES")
    print("=" * 60)

    # Example 1: Troubleshooting
    print("\n--- TROUBLESHOOTING PROMPT ---\n")
    troubleshooting = build_troubleshooting_prompt(
        service="payment-api",
        symptoms="Response times increased from 100ms to 2s",
        logs="2024-01-15 10:00:00 WARN Connection pool exhausted\n2024-01-15 10:00:01 ERROR Timeout waiting for connection",
        tried=["Increased connection pool size", "Restarted pods"]
    )
    print(troubleshooting)

    # Example 2: Code Review
    print("\n--- CODE REVIEW PROMPT ---\n")
    code_review = build_code_review_prompt(
        code='''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
''',
        language="python",
        focus_areas=["security", "error handling"]
    )
    print(code_review)

    # Example 3: Infrastructure
    print("\n--- INFRASTRUCTURE PROMPT ---\n")
    infrastructure = build_infrastructure_prompt(
        description="Web application with database",
        cloud_provider="AWS",
        requirements=[
            "ECS Fargate for containers",
            "RDS PostgreSQL with Multi-AZ",
            "Application Load Balancer",
            "VPC with public and private subnets",
        ]
    )
    print(infrastructure)
