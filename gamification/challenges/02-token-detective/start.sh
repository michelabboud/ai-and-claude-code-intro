#!/bin/bash
# Quick start script for token-detective-01 challenge
#
# Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
# Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
# Copyright: © 2026 Michel Abboud. All rights reserved.
# License: CC BY-NC 4.0

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║   🥋 PROMPT DOJO 01: TOKEN MINIMIZATION                  ║"
echo "║                                                           ║"
echo "║   Challenge: Reduce token usage by 75%                   ║"
echo "║   Difficulty: ⭐⭐ Apprentice                              ║"
echo "║   Time Limit: 15 minutes                                 ║"
echo "║   Points: 20 (base) + bonuses                            ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if user has initialized profile
if [ ! -f "$HOME/.ai-devops-quest/profile.json" ]; then
    echo "⚠️  No quest profile found!"
    echo ""
    echo "Please initialize your profile first:"
    echo "  cd ../../progress-tracker"
    echo "  python tracker.py init"
    echo ""
    exit 1
fi

# Create solution directory
if [ ! -d "my-solution" ]; then
    echo "📁 Creating solution directory..."
    mkdir -p my-solution
    echo "✓ Created: my-solution/"
    echo ""
fi

# Show mission brief
echo "📋 MISSION BRIEF:"
echo "─────────────────────────────────────────────────────────────"
cat << 'EOF'

Your startup's API costs are out of control! A colleague wrote
a prompt that works but uses 2,000 tokens.

Your mission: Rewrite it to use ≤500 tokens while maintaining
the same quality output.

EOF
echo "─────────────────────────────────────────────────────────────"
echo ""

# Offer to show inefficient prompt
read -p "View the inefficient prompt? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "INEFFICIENT PROMPT (2000+ tokens):"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    cat starter/inefficient-prompt.txt | head -20
    echo ""
    echo "... (truncated, see starter/inefficient-prompt.txt for full)"
    echo ""
fi

# Show next steps
echo "🎯 YOUR TASK:"
echo ""
echo "1. Create your optimized prompt:"
echo "   Edit: my-solution/optimized-prompt.txt"
echo ""
echo "2. Test it with Claude to generate Dockerfile"
echo ""
echo "3. Count tokens in your prompt:"
echo "   python ../lib/count-tokens.py my-solution/optimized-prompt.txt"
echo ""
echo "4. Grade your solution:"
echo "   ./test-suite/grade.sh"
echo ""

# Offer to start timer
echo "───────────────────────────────────────────────────────────"
read -p "Start 15-minute timer now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    START_TIME=$(date +%s)
    echo "$START_TIME" > my-solution/.start-time
    echo ""
    echo "⏱️  Timer started! You have 15 minutes."
    echo ""

    # Optional: terminal notification at 15 min (Linux only)
    if command -v notify-send &> /dev/null; then
        (sleep 900 && notify-send "DevOps Quest" "Time's up! 15 minutes elapsed." &) 2>/dev/null
    fi
fi

# Show helpful reminders
echo "💡 TIPS:"
echo "  • Need hints? Run: ./hints.sh list"
echo "  • Each hint costs -5 points"
echo "  • Focus on clarity over cleverness"
echo "  • Trust Claude's expertise"
echo ""

# Open editor if available
if [ -n "$EDITOR" ]; then
    read -p "Open editor for optimized-prompt.txt? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        touch my-solution/optimized-prompt.txt
        $EDITOR my-solution/optimized-prompt.txt
    fi
fi

echo ""
echo "Good luck! 🚀"
echo ""
