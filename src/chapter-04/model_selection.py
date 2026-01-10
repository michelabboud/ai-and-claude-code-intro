#!/usr/bin/env python3
"""
Chapter 4: AI Models Landscape
Model Selection Guide for DevOps Engineers

This module helps select the right AI model for different DevOps tasks.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class TaskComplexity(Enum):
    """Task complexity levels."""
    SIMPLE = "simple"      # Formatting, simple Q&A
    MODERATE = "moderate"  # Code generation, analysis
    COMPLEX = "complex"    # Architecture, multi-step reasoning


class SpeedRequirement(Enum):
    """Response speed requirements."""
    REALTIME = "realtime"      # < 1 second
    FAST = "fast"              # < 5 seconds
    STANDARD = "standard"      # < 30 seconds
    BATCH = "batch"            # No time constraint


@dataclass
class ModelSpec:
    """Model specification."""
    name: str
    provider: str
    context_window: int  # tokens
    cost_per_1k_input: float  # USD
    cost_per_1k_output: float
    best_for: List[str]
    speed: SpeedRequirement
    complexity_level: TaskComplexity


# Model database (as of 2025 - prices and specs change frequently)
MODELS = {
    # Claude Models
    "claude-opus-4.5": ModelSpec(
        name="Claude Opus 4.5",
        provider="Anthropic",
        context_window=200000,
        cost_per_1k_input=0.005,
        cost_per_1k_output=0.025,
        best_for=["complex architecture", "nuanced analysis", "research"],
        speed=SpeedRequirement.STANDARD,
        complexity_level=TaskComplexity.COMPLEX,
    ),
    "claude-sonnet-4.5": ModelSpec(
        name="Claude Sonnet 4.5",
        provider="Anthropic",
        context_window=200000,
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        best_for=["code generation", "general DevOps", "documentation"],
        speed=SpeedRequirement.FAST,
        complexity_level=TaskComplexity.MODERATE,
    ),
    "claude-haiku-4.5": ModelSpec(
        name="Claude Haiku 4.5",
        provider="Anthropic",
        context_window=200000,
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.005,
        best_for=["quick queries", "simple formatting", "high volume"],
        speed=SpeedRequirement.REALTIME,
        complexity_level=TaskComplexity.SIMPLE,
    ),

    # GPT Models
    "gpt-4-turbo": ModelSpec(
        name="GPT-4 Turbo",
        provider="OpenAI",
        context_window=128000,
        cost_per_1k_input=0.01,
        cost_per_1k_output=0.03,
        best_for=["complex reasoning", "code generation"],
        speed=SpeedRequirement.FAST,
        complexity_level=TaskComplexity.COMPLEX,
    ),
    "gpt-3.5-turbo": ModelSpec(
        name="GPT-3.5 Turbo",
        provider="OpenAI",
        context_window=16000,
        cost_per_1k_input=0.0005,
        cost_per_1k_output=0.0015,
        best_for=["simple tasks", "high volume", "quick responses"],
        speed=SpeedRequirement.REALTIME,
        complexity_level=TaskComplexity.SIMPLE,
    ),
}


def recommend_model(
    task_type: str,
    complexity: TaskComplexity = TaskComplexity.MODERATE,
    speed_needed: SpeedRequirement = SpeedRequirement.STANDARD,
    budget_sensitive: bool = False,
) -> dict:
    """
    Recommend a model based on task requirements.

    Args:
        task_type: Type of task (code_review, infrastructure, troubleshooting, etc.)
        complexity: How complex is the task?
        speed_needed: How fast do you need responses?
        budget_sensitive: Prioritize cost over capability?

    Returns:
        Dictionary with recommendation and reasoning.
    """
    task_mappings = {
        "code_review": ["claude-sonnet-4.5", "gpt-4-turbo"],
        "infrastructure": ["claude-sonnet-4.5", "gpt-4-turbo"],
        "troubleshooting": ["claude-sonnet-4.5", "claude-opus-4.5"],
        "documentation": ["claude-sonnet-4.5", "gpt-4-turbo"],
        "quick_query": ["claude-haiku-4.5", "gpt-4-turbo"],
        "architecture": ["claude-opus-4.5", "gpt-4-turbo"],
        "security_audit": ["claude-opus-4.5", "claude-sonnet-4.5"],
        "log_analysis": ["claude-sonnet-4.5", "claude-haiku-4.5"],
    }

    candidates = task_mappings.get(task_type, ["claude-sonnet-4.5"])

    # Filter by complexity
    filtered = []
    for model_id in candidates:
        model = MODELS.get(model_id)
        if model and model.complexity_level.value >= complexity.value:
            filtered.append(model_id)

    if not filtered:
        filtered = candidates

    # Sort by cost if budget sensitive
    if budget_sensitive:
        filtered.sort(key=lambda m: MODELS[m].cost_per_1k_input)

    recommended = filtered[0] if filtered else "claude-sonnet-4.5"
    model = MODELS[recommended]

    return {
        "recommended_model": model.name,
        "model_id": recommended,
        "provider": model.provider,
        "reasoning": f"Best for {task_type} with {complexity.value} complexity",
        "cost_estimate": {
            "per_1k_input": f"${model.cost_per_1k_input}",
            "per_1k_output": f"${model.cost_per_1k_output}",
        },
        "alternatives": filtered[1:3] if len(filtered) > 1 else [],
    }


def estimate_monthly_cost(
    model_id: str,
    daily_input_tokens: int,
    daily_output_tokens: int,
    working_days: int = 22,
) -> dict:
    """Estimate monthly API costs."""
    model = MODELS.get(model_id)
    if not model:
        return {"error": f"Unknown model: {model_id}"}

    daily_input_cost = (daily_input_tokens / 1000) * model.cost_per_1k_input
    daily_output_cost = (daily_output_tokens / 1000) * model.cost_per_1k_output
    daily_total = daily_input_cost + daily_output_cost

    monthly_total = daily_total * working_days

    return {
        "model": model.name,
        "daily_cost": f"${daily_total:.2f}",
        "monthly_cost": f"${monthly_total:.2f}",
        "annual_cost": f"${monthly_total * 12:.2f}",
        "breakdown": {
            "input_cost_per_day": f"${daily_input_cost:.2f}",
            "output_cost_per_day": f"${daily_output_cost:.2f}",
        },
    }


# =============================================================================
# DECISION TREE FOR MODEL SELECTION
# =============================================================================

def model_decision_tree(
    needs_code: bool = True,
    needs_reasoning: bool = True,
    latency_sensitive: bool = False,
    budget_per_month: Optional[float] = None,
    daily_requests: int = 100,
) -> dict:
    """
    Decision tree for model selection.

    Returns recommendation with reasoning.
    """
    # Estimate tokens per request
    avg_input_tokens = 2000
    avg_output_tokens = 500

    recommendations = []

    # Check latency requirements
    if latency_sensitive:
        recommendations.append({
            "model": "claude-haiku-4.5",
            "reason": "Lowest latency for real-time use cases",
        })

    # Check budget constraints
    if budget_per_month:
        for model_id, model in MODELS.items():
            monthly = estimate_monthly_cost(
                model_id, avg_input_tokens * daily_requests,
                avg_output_tokens * daily_requests
            )
            if float(monthly["monthly_cost"].replace("$", "")) <= budget_per_month:
                recommendations.append({
                    "model": model_id,
                    "reason": f"Fits budget at {monthly['monthly_cost']}/month",
                })

    # Check capability requirements
    if needs_reasoning and needs_code:
        recommendations.append({
            "model": "claude-sonnet-4.5",
            "reason": "Best balance of code generation and reasoning",
        })
    elif needs_code and not needs_reasoning:
        recommendations.append({
            "model": "claude-haiku-4.5",
            "reason": "Fast and cost-effective for code tasks",
        })

    # Default recommendation
    if not recommendations:
        recommendations.append({
            "model": "claude-sonnet-4.5",
            "reason": "Best general-purpose model for DevOps",
        })

    return {
        "primary_recommendation": recommendations[0],
        "alternatives": recommendations[1:3] if len(recommendations) > 1 else [],
        "decision_factors": {
            "latency_sensitive": latency_sensitive,
            "needs_code": needs_code,
            "needs_reasoning": needs_reasoning,
            "budget_constraint": budget_per_month,
        },
    }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MODEL SELECTION EXAMPLES")
    print("=" * 60)

    # Example 1: Code review
    print("\n--- Recommendation for Code Review ---")
    rec = recommend_model("code_review", TaskComplexity.MODERATE)
    print(f"Model: {rec['recommended_model']}")
    print(f"Reasoning: {rec['reasoning']}")
    print(f"Cost: {rec['cost_estimate']}")

    # Example 2: Architecture decision
    print("\n--- Recommendation for Architecture ---")
    rec = recommend_model("architecture", TaskComplexity.COMPLEX)
    print(f"Model: {rec['recommended_model']}")
    print(f"Reasoning: {rec['reasoning']}")

    # Example 3: Quick queries (budget sensitive)
    print("\n--- Recommendation for Quick Queries (Budget) ---")
    rec = recommend_model("quick_query", budget_sensitive=True)
    print(f"Model: {rec['recommended_model']}")
    print(f"Cost: {rec['cost_estimate']}")

    # Example 4: Cost estimation
    print("\n--- Monthly Cost Estimation ---")
    cost = estimate_monthly_cost(
        "claude-3-sonnet",
        daily_input_tokens=50000,
        daily_output_tokens=10000,
    )
    print(f"Model: {cost['model']}")
    print(f"Monthly cost: {cost['monthly_cost']}")

    # Example 5: Decision tree
    print("\n--- Decision Tree Analysis ---")
    decision = model_decision_tree(
        needs_code=True,
        needs_reasoning=True,
        latency_sensitive=False,
        budget_per_month=100,
        daily_requests=100,
    )
    print(f"Recommended: {decision['primary_recommendation']}")
