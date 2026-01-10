#!/bin/bash
# Story Mode Launcher

set -e

show_menu() {
    clear
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║              📖 STORY MODE: SELECT CHAPTER               ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Available Stories:"
    echo ""
    echo "  6) The Midnight Deployment Crisis 🚨"
    echo "     Chapter 6: Claude Code Fundamentals"
    echo "     Difficulty: ⭐⭐⭐ | Time: 30 min"
    echo ""
    echo "  7) The Toxic Legacy Codebase 🐉 [Coming Soon]"
    echo "  8) Multi-Team Coordination Disaster 🌪️ [Coming Soon]"
    echo "  9) Building the Integration Bridge 🌉 [Coming Soon]"
    echo "  10) The Perfect Storm ⚡ [Coming Soon]"
    echo ""
    echo "  0) Exit"
    echo ""
}

play_story() {
    local chapter=$1
    local story_file="stories/chapter-$chapter.txt"

    if [ ! -f "$story_file" ]; then
        echo "❌ Story not found: $story_file"
        echo ""
        read -p "Press ENTER to return to menu..."
        return
    fi

    clear
    cat "$story_file"
    echo ""
    read -p "Press ENTER to return to menu..."
}

# Main loop
while true; do
    show_menu
    read -p "Select chapter (0-10): " choice

    case $choice in
        6)
            play_story "06"
            ;;
        7|8|9|10)
            echo ""
            echo "📝 This story is coming soon!"
            echo "   Check back after more chapters are written."
            echo ""
            read -p "Press ENTER to continue..."
            ;;
        0)
            echo ""
            echo "Thanks for playing! 🎮"
            echo ""
            exit 0
            ;;
        *)
            echo ""
            echo "Invalid choice. Please select 0-10."
            echo ""
            read -p "Press ENTER to continue..."
            ;;
    esac
done
