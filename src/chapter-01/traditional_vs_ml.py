#!/usr/bin/env python3
"""
Chapter 1: Introduction to AI
Traditional Programming vs Machine Learning Approaches

This example demonstrates the difference between traditional
rule-based programming and machine learning for spam detection.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0
"""

# =============================================================================
# TRADITIONAL APPROACH: Rule-based spam detection
# =============================================================================

def is_spam_traditional(email_text: str) -> bool:
    """
    Traditional rule-based spam detection.

    Problems with this approach:
    - Spammers easily evade rules (e.g., "FR3E" instead of "FREE")
    - Must manually update rules as spam evolves
    - Doesn't learn from new patterns
    """
    spam_keywords = ["FREE", "WINNER", "CLICK NOW", "LIMITED TIME"]

    for keyword in spam_keywords:
        if keyword.lower() in email_text.lower():
            return True
    return False


# =============================================================================
# ML APPROACH: Learn patterns from data
# =============================================================================

def is_spam_ml(email_text: str, model) -> bool:
    """
    Machine Learning approach to spam detection.

    Advantages:
    - Model learns patterns from millions of examples
    - Adapts to new spam tactics automatically
    - Catches sophisticated evasion attempts
    - Improves with more data
    """
    # Extract features (simplified - real implementations use more)
    features = extract_features(email_text)

    # Model predicts based on learned patterns
    prediction = model.predict(features)

    return prediction == "spam"


def extract_features(email_text: str) -> dict:
    """Extract features from email for ML model."""
    return {
        "length": len(email_text),
        "has_urgent_words": any(w in email_text.lower() for w in ["urgent", "asap", "now"]),
        "has_links": "http" in email_text.lower(),
        "uppercase_ratio": sum(1 for c in email_text if c.isupper()) / max(len(email_text), 1),
        "exclamation_count": email_text.count("!"),
    }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    test_emails = [
        "Congratulations! You've won a FREE vacation! CLICK NOW!",
        "Hi, can we reschedule our meeting to 3pm tomorrow?",
        "FR33 M0NEY! Act n0w!!!", # Traditional approach might miss this
    ]

    print("Traditional Spam Detection Results:")
    print("-" * 40)
    for email in test_emails:
        result = is_spam_traditional(email)
        print(f"Spam: {result} - {email[:50]}...")

    print("\nNote: ML approach would require a trained model.")
    print("The ML approach can catch evasion tactics like 'FR33' -> 'FREE'")
