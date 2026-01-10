#!/usr/bin/env python3
"""
Token Counter Utility
Counts tokens in prompts using tiktoken (same as Claude)

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0
"""

import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("❌ Error: tiktoken not installed")
    print("Install with: pip install tiktoken")
    sys.exit(1)


def count_tokens(text: str, model: str = "claude-3-5-sonnet-20241022") -> int:
    """
    Count tokens in text using Claude's tokenizer approximation.

    Note: We use cl100k_base encoding which is a good approximation
    for Claude's tokenizer (actual numbers may vary slightly)
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def analyze_file(file_path: Path):
    """Analyze token usage in a file"""
    try:
        text = file_path.read_text()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    token_count = count_tokens(text)
    char_count = len(text)
    word_count = len(text.split())

    # Calculate cost (Claude Sonnet 4.5 rates)
    cost_per_million = 3.00  # Input tokens
    cost = (token_count / 1_000_000) * cost_per_million

    # Show results
    print()
    print("═" * 60)
    print(f" 📊 TOKEN ANALYSIS: {file_path.name}")
    print("═" * 60)
    print()
    print(f"  📝 Characters:  {char_count:,}")
    print(f"  📖 Words:       {word_count:,}")
    print(f"  🎫 Tokens:      {token_count:,}")
    print()
    print(f"  💰 Cost:        ${cost:.6f} (Claude Sonnet 4.5 input)")
    print()

    # Efficiency rating
    chars_per_token = char_count / token_count if token_count > 0 else 0
    print(f"  📏 Efficiency:  {chars_per_token:.2f} chars/token")
    print()

    # Challenge-specific feedback
    if "prompt-dojo" in str(file_path):
        print("─" * 60)
        print(" 🎯 CHALLENGE TARGETS:")
        print("─" * 60)
        print()

        if token_count <= 200:
            print("  🏆 NIGHTMARE MODE: ✅ ≤200 tokens")
            print("     Bonus: +100 points!")
        elif token_count <= 300:
            print("  💀 HARD MODE: ✅ ≤300 tokens")
            print("     Bonus: +50 points!")
        elif token_count <= 500:
            print("  ✅ NORMAL MODE: ✅ ≤500 tokens")
            print("     Extreme Efficiency bonus: +20 points!")
        elif token_count <= 600:
            print("  ⚠️  OVER TARGET: 501-600 tokens")
            print("     Penalty: -5 points")
        else:
            print("  ❌ OVER LIMIT: >600 tokens")
            print("     Penalty: -10 points")
        print()

    print("═" * 60)
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python count-tokens.py <file>")
        print()
        print("Example:")
        print("  python count-tokens.py my-solution/optimized-prompt.txt")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    analyze_file(file_path)


if __name__ == "__main__":
    main()
