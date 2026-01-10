#!/usr/bin/env python3
"""
Chapter 2: Understanding LLMs and Tokens
Tokenization Examples and Token Counting

This module demonstrates token concepts for DevOps engineers.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0
"""

from typing import List, Tuple


# =============================================================================
# SIMPLIFIED BPE TOKENIZATION CONCEPT
# =============================================================================

def demonstrate_bpe_concept():
    """
    Demonstrate the concept of Byte Pair Encoding (BPE).

    BPE works by:
    1. Starting with individual characters
    2. Finding most common adjacent pairs
    3. Merging them into new tokens
    4. Repeating until vocabulary size reached
    """
    text = "kubernetes"

    print("BPE Tokenization Concept:")
    print("-" * 40)
    print(f"Input: '{text}'")
    print()

    # Step 1: Character-level tokens
    char_tokens = list(text)
    print(f"Step 1 - Characters: {char_tokens}")

    # Step 2: Common pairs might merge
    # In reality, this is based on training corpus statistics
    example_merges = [
        ("k", "u", "ku"),
        ("b", "e", "be"),
        ("r", "n", "rn"),
    ]

    print("\nStep 2 - Example merges (based on corpus frequency):")
    for a, b, merged in example_merges:
        print(f"  '{a}' + '{b}' -> '{merged}'")

    # Step 3: Final tokens (simplified example)
    final_tokens = ["kuber", "net", "es"]
    print(f"\nStep 3 - Final tokens: {final_tokens}")
    print(f"Token count: {len(final_tokens)}")


# =============================================================================
# TOKEN COUNTING (WITHOUT EXTERNAL DEPENDENCIES)
# =============================================================================

def estimate_tokens(text: str) -> int:
    """
    Estimate token count without external libraries.

    Rule of thumb:
    - English: ~4 characters per token
    - Code: ~3 characters per token (more symbols)
    - With spaces: ~0.75 words per token
    """
    # Simple estimation based on words and characters
    words = len(text.split())
    chars = len(text)

    # Weighted estimate
    word_based = words * 1.3  # ~1.3 tokens per word average
    char_based = chars / 4  # ~4 chars per token

    return int((word_based + char_based) / 2)


def count_tokens_tiktoken(text: str, model: str = "gpt-4") -> int:
    """
    Count tokens using tiktoken library.

    Install: pip install tiktoken

    Note: This is a reference implementation. In production,
    use the appropriate tokenizer for your model.
    """
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except ImportError:
        print("tiktoken not installed. Using estimate.")
        return estimate_tokens(text)


# =============================================================================
# COST ESTIMATION
# =============================================================================

# Pricing as of 2025 (prices change frequently)
MODEL_PRICING = {
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},  # per 1K tokens
    "claude-opus-4.5": {"input": 0.005, "output": 0.025},
    "claude-sonnet-4.5": {"input": 0.003, "output": 0.015},
    "claude-haiku-4.5": {"input": 0.001, "output": 0.005},
}


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "claude-sonnet-4.5"
) -> dict:
    """
    Estimate API cost for a given number of tokens.
    """
    if model not in MODEL_PRICING:
        return {"error": f"Unknown model: {model}"}

    pricing = MODEL_PRICING[model]

    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": f"${input_cost:.6f}",
        "output_cost": f"${output_cost:.6f}",
        "total_cost": f"${total_cost:.6f}",
    }


# =============================================================================
# CODE REVIEW BUDGET PLANNING
# =============================================================================

def plan_code_review_budget(
    avg_file_lines: int = 200,
    files_per_pr: int = 5,
    prs_per_day: int = 10,
    model: str = "claude-sonnet-4.5"
) -> dict:
    """
    Plan budget for AI-assisted code review.

    Assumptions:
    - ~4 chars per line average
    - Include context (system prompt, instructions)
    - Output ~20% of input length
    """
    # Estimate tokens per file
    chars_per_file = avg_file_lines * 40  # ~40 chars per line
    tokens_per_file = chars_per_file // 4  # ~4 chars per token

    # Context overhead (system prompt, instructions)
    context_tokens = 500

    # Per PR calculation
    input_tokens_per_pr = (tokens_per_file * files_per_pr) + context_tokens
    output_tokens_per_pr = input_tokens_per_pr // 5  # ~20% for response

    # Daily calculation
    daily_input = input_tokens_per_pr * prs_per_day
    daily_output = output_tokens_per_pr * prs_per_day

    # Cost estimation
    cost = estimate_cost(daily_input, daily_output, model)

    # Monthly projection (22 working days)
    monthly_cost = float(cost["total_cost"].replace("$", "")) * 22

    return {
        "per_pr": {
            "input_tokens": input_tokens_per_pr,
            "output_tokens": output_tokens_per_pr,
        },
        "daily": {
            "prs": prs_per_day,
            "input_tokens": daily_input,
            "output_tokens": daily_output,
            "cost": cost["total_cost"],
        },
        "monthly": {
            "working_days": 22,
            "estimated_cost": f"${monthly_cost:.2f}",
        },
        "model": model,
    }


# =============================================================================
# CONTEXT WINDOW STRATEGIES
# =============================================================================

def demonstrate_context_strategies():
    """
    Show strategies for managing context windows.
    """
    strategies = {
        "chunking": {
            "description": "Split large documents into smaller pieces",
            "use_case": "Processing files larger than context window",
            "example": "Split a 10,000 line file into 1,000 line chunks",
        },
        "summarization": {
            "description": "Summarize previous context to preserve tokens",
            "use_case": "Long conversations or document analysis",
            "example": "Summarize first 3 file reviews, detail current one",
        },
        "sliding_window": {
            "description": "Keep recent context, drop older",
            "use_case": "Real-time log analysis",
            "example": "Always keep last 100 log lines in context",
        },
        "hierarchical": {
            "description": "High-level summary + detailed current section",
            "use_case": "Code architecture review",
            "example": "System overview + detailed current module",
        },
        "selective": {
            "description": "Include only relevant sections",
            "use_case": "Bug investigation",
            "example": "Include error stack + related functions only",
        },
    }

    print("\nContext Window Management Strategies:")
    print("=" * 50)
    for name, info in strategies.items():
        print(f"\n{name.upper()}")
        print(f"  Description: {info['description']}")
        print(f"  Use case: {info['use_case']}")
        print(f"  Example: {info['example']}")


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CHAPTER 2: TOKEN EXAMPLES")
    print("=" * 60)

    # BPE Concept
    print("\n")
    demonstrate_bpe_concept()

    # Token estimation
    print("\n" + "=" * 60)
    print("TOKEN ESTIMATION")
    print("-" * 40)
    sample_code = """
def process_request(request):
    if not request.is_valid():
        raise ValidationError("Invalid request")
    return handler.process(request)
"""
    estimated = estimate_tokens(sample_code)
    print(f"Sample code:\n{sample_code}")
    print(f"Estimated tokens: {estimated}")

    # Cost estimation
    print("\n" + "=" * 60)
    print("COST ESTIMATION")
    print("-" * 40)
    cost = estimate_cost(10000, 2000, "claude-sonnet-4.5")
    for key, value in cost.items():
        print(f"  {key}: {value}")

    # Budget planning
    print("\n" + "=" * 60)
    print("CODE REVIEW BUDGET PLANNING")
    print("-" * 40)
    budget = plan_code_review_budget()
    print(f"Daily cost: {budget['daily']['cost']}")
    print(f"Monthly cost: {budget['monthly']['estimated_cost']}")

    # Context strategies
    demonstrate_context_strategies()
