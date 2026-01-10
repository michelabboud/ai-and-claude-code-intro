#!/bin/bash
# Progressive hints for incident-01-crashloop
#
# Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
# Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
# Copyright: © 2026 Michel Abboud. All rights reserved.
# License: CC BY-NC 4.0

show_hint() {
    case $1 in
        1)
            echo "═══════════════════════════════════════════════════════"
            echo "💡 HINT 1: Where to Look (-5 points)"
            echo "═══════════════════════════════════════════════════════"
            echo ""
            echo "The app is crashing on STARTUP, not during runtime."
            echo ""
            echo "Key questions:"
            echo "  • What does the app need to start successfully?"
            echo "  • Where is configuration provided?"
            echo "  • What do the logs say?"
            echo ""
            echo "Commands to try:"
            echo "  docker-compose logs app"
            echo "  docker-compose exec app env | grep DATABASE"
            echo ""
            ;;
        2)
            echo "═══════════════════════════════════════════════════════"
            echo "💡 HINT 2: The Specific Problem (-5 points)"
            echo "═══════════════════════════════════════════════════════"
            echo ""
            echo "The issue is an ENVIRONMENT VARIABLE mismatch."
            echo ""
            echo "Look at:"
            echo "  • app/app.py - What variable does it expect?"
            echo "  • docker-compose.yml - What variable is set?"
            echo ""
            echo "The names don't match! ❌"
            echo ""
            ;;
        3)
            echo "═══════════════════════════════════════════════════════"
            echo "💡 HINT 3: The Solution (-5 points)"
            echo "═══════════════════════════════════════════════════════"
            echo ""
            echo "In docker-compose.yml, change:"
            echo ""
            echo "  FROM:"
            echo "    DB_URL: postgresql://..."
            echo ""
            echo "  TO:"
            echo "    DATABASE_URL: postgresql://..."
            echo ""
            echo "Then rebuild:"
            echo "  docker-compose down"
            echo "  docker-compose up -d"
            echo ""
            ;;
        *)
            echo "Usage: ./hints.sh [1|2|3]"
            ;;
    esac
}

if [ $# -eq 0 ]; then
    echo "Available hints:"
    echo "  ./hints.sh 1  # High-level hint"
    echo "  ./hints.sh 2  # Specific problem"
    echo "  ./hints.sh 3  # Solution"
else
    show_hint $1
fi
