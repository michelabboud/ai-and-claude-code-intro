#!/bin/bash
# Progressive hints system for prompt-dojo-01
# Each hint costs -5 points
#
# Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
# Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
# Copyright: © 2026 Michel Abboud. All rights reserved.
# License: CC BY-NC 4.0

HINT_FILE="$HOME/.ai-devops-quest/hints-prompt-dojo-01.txt"

show_hint() {
    local hint_num=$1

    case $hint_num in
        1)
            echo "═══════════════════════════════════════════════════════"
            echo "💡 HINT 1: High-Level Strategy (-5 points)"
            echo "═══════════════════════════════════════════════════════"
            echo ""
            echo "The inefficient prompt has three major problems:"
            echo ""
            echo "1. 🗣️  Unnecessary conversation and small talk"
            echo "   - Greetings, pleasantries, thank yous"
            echo "   - Explanations of what Docker/Flask are"
            echo "   - Claude already knows this!"
            echo ""
            echo "2. 📝 Verbose structure"
            echo "   - Full paragraphs instead of bullet points"
            echo "   - Repetitive phrasing"
            echo "   - 'First, Second, Third' format"
            echo ""
            echo "3. 🔍 Over-specification"
            echo "   - Listing every Docker best practice"
            echo "   - Explaining WHY (Claude understands)"
            echo "   - Multiple examples for simple things"
            echo ""
            echo "Your strategy:"
            echo "✓ Remove ALL conversational fluff"
            echo "✓ Use bullet points, not paragraphs"
            echo "✓ Trust Claude's expertise"
            echo ""
            ;;
        2)
            echo "═══════════════════════════════════════════════════════"
            echo "💡 HINT 2: Specific Techniques (-5 points)"
            echo "═══════════════════════════════════════════════════════"
            echo ""
            echo "Token-saving techniques to apply:"
            echo ""
            echo "1. Start with direct action:"
            echo "   Bad:  'Hello! I need help with...'"
            echo "   Good: 'Create a Dockerfile for...'"
            echo ""
            echo "2. List requirements with bullets:"
            echo "   Bad:  'First, use Python 3.11. Second, create...'"
            echo "   Good: '- Python 3.11'"
            echo "         '- Non-root user'"
            echo ""
            echo "3. Combine related requirements:"
            echo "   Bad:  'We have requirements.txt. Use pip install...'"
            echo "   Good: 'Install from requirements.txt'"
            echo ""
            echo "4. Use shorthand:"
            echo "   Bad:  'The entry point should start the Flask application'"
            echo "   Good: 'Entry: python app.py'"
            echo ""
            echo "5. Delegate details:"
            echo "   Bad:  'Use specific tags, minimize layers, order...'"
            echo "   Good: 'Follow Docker best practices'"
            echo ""
            echo "Target structure:"
            echo "  - 1-2 sentence context"
            echo "  - Bullet list of requirements"
            echo "  - One line for best practices"
            echo ""
            ;;
        3)
            echo "═══════════════════════════════════════════════════════"
            echo "💡 HINT 3: Near-Solution Template (-5 points)"
            echo "═══════════════════════════════════════════════════════"
            echo ""
            echo "Here's a template structure (fill in the details):"
            echo ""
            echo "┌─────────────────────────────────────────────────┐"
            echo "│ Create a [CONTEXT] Dockerfile for [APP TYPE]:  │"
            echo "│                                                 │"
            echo "│ Requirements:                                   │"
            echo "│ - [BASE IMAGE + VERSION]                        │"
            echo "│ - [SECURITY REQUIREMENT]                        │"
            echo "│ - [HEALTH CHECK DETAILS]                        │"
            echo "│ - [DEPENDENCY MANAGEMENT]                       │"
            echo "│ - [ENTRY POINT]                                 │"
            echo "│ - [PORT]                                        │"
            echo "│ - [OPTIONAL FEATURE]                            │"
            echo "│                                                 │"
            echo "│ [QUALITY STATEMENT]                             │"
            echo "└─────────────────────────────────────────────────┘"
            echo ""
            echo "Token budget per section:"
            echo "  - Context line: 15-20 tokens"
            echo "  - Each requirement: 10-15 tokens"
            echo "  - Quality statement: 10 tokens"
            echo "  - Total: ~250-300 tokens"
            echo ""
            echo "Remember:"
            echo "  - Be specific about WHAT (versions, endpoints)"
            echo "  - Be vague about HOW (let Claude decide)"
            echo "  - NO explanations or justifications"
            echo "  - NO examples unless critical"
            echo ""
            ;;
        list)
            echo ""
            echo "Available hints for prompt-dojo-01:"
            echo ""
            echo "  Hint 1: High-level strategy (costs -5 pts)"
            echo "  Hint 2: Specific techniques (costs -5 pts)"
            echo "  Hint 3: Near-solution template (costs -5 pts)"
            echo ""
            echo "Usage: ./hints.sh [1|2|3]"
            echo ""
            return
            ;;
        *)
            echo "Invalid hint number. Use: ./hints.sh [1|2|3|list]"
            return 1
            ;;
    esac

    # Track hint usage
    mkdir -p "$(dirname "$HINT_FILE")"
    echo "$(date): Hint $hint_num used" >> "$HINT_FILE"

    echo ""
    echo "───────────────────────────────────────────────────────"
    echo "⚠️  Remember: Each hint costs -5 points!"
    echo "───────────────────────────────────────────────────────"
    echo ""
}

# Main
if [ $# -eq 0 ]; then
    show_hint list
else
    show_hint "$1"
fi
