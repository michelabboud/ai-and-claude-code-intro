#!/bin/bash
# Auto-grader for prompt-dojo-01
# Grades solution based on token efficiency and output quality

set -e

SOLUTION_DIR="${1:-my-solution}"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║              🎓 AUTO-GRADER: PROMPT DOJO 01              ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check solution directory exists
if [ ! -d "$SOLUTION_DIR" ]; then
    echo "❌ Solution directory not found: $SOLUTION_DIR"
    echo ""
    echo "Expected structure:"
    echo "  $SOLUTION_DIR/"
    echo "  ├── optimized-prompt.txt"
    echo "  └── generated-dockerfile (optional)"
    echo ""
    exit 1
fi

# Check required files
if [ ! -f "$SOLUTION_DIR/optimized-prompt.txt" ]; then
    echo "❌ Missing: $SOLUTION_DIR/optimized-prompt.txt"
    exit 1
fi

echo "📁 Grading solution in: $SOLUTION_DIR"
echo ""

# Initialize scores
CORRECTNESS_SCORE=0
EFFICIENCY_SCORE=0
QUALITY_SCORE=0
BONUS_POINTS=0
PENALTY_POINTS=0

# ===================================================================
# 1. TOKEN EFFICIENCY (40% of grade)
# ===================================================================
echo "─────────────────────────────────────────────────────────────"
echo "1️⃣  EFFICIENCY CHECK (40 points)"
echo "─────────────────────────────────────────────────────────────"
echo ""

if command -v python3 &> /dev/null && python3 -c "import tiktoken" 2>/dev/null; then
    # Count tokens using Python tool
    TOKEN_OUTPUT=$(python3 ../lib/count-tokens.py "$SOLUTION_DIR/optimized-prompt.txt" 2>&1 | grep "🎫 Tokens:")
    TOKEN_COUNT=$(echo "$TOKEN_OUTPUT" | grep -oP '\d{1,5}' | head -1)

    echo "🎫 Token count: $TOKEN_COUNT"
    echo ""

    # Score based on token count
    if [ "$TOKEN_COUNT" -le 200 ]; then
        EFFICIENCY_SCORE=40
        BONUS_POINTS=$((BONUS_POINTS + 100))
        echo "   💀 NIGHTMARE MODE: ≤200 tokens"
        echo "   ✅ Efficiency: 40/40"
        echo "   🏆 Bonus: +100 points (Nightmare mode)"
    elif [ "$TOKEN_COUNT" -le 300 ]; then
        EFFICIENCY_SCORE=40
        BONUS_POINTS=$((BONUS_POINTS + 50))
        echo "   💪 HARD MODE: ≤300 tokens"
        echo "   ✅ Efficiency: 40/40"
        echo "   🏆 Bonus: +50 points (Hard mode)"
    elif [ "$TOKEN_COUNT" -le 500 ]; then
        EFFICIENCY_SCORE=40
        BONUS_POINTS=$((BONUS_POINTS + 20))
        echo "   ✅ NORMAL MODE: ≤500 tokens"
        echo "   ✅ Efficiency: 40/40"
        echo "   🏆 Bonus: +20 points (Extreme efficiency)"
    elif [ "$TOKEN_COUNT" -le 600 ]; then
        EFFICIENCY_SCORE=30
        PENALTY_POINTS=$((PENALTY_POINTS - 5))
        echo "   ⚠️  Over target: 501-600 tokens"
        echo "   ⚠️  Efficiency: 30/40"
        echo "   ⚠️  Penalty: -5 points"
    else
        EFFICIENCY_SCORE=20
        PENALTY_POINTS=$((PENALTY_POINTS - 10))
        echo "   ❌ Over limit: >600 tokens"
        echo "   ❌ Efficiency: 20/40"
        echo "   ❌ Penalty: -10 points"
    fi
else
    echo "⚠️  Cannot count tokens (tiktoken not installed)"
    echo "   Install: pip install tiktoken"
    echo "   Assuming pass for now..."
    EFFICIENCY_SCORE=35
fi

echo ""

# ===================================================================
# 2. CORRECTNESS CHECK (40% of grade)
# ===================================================================
echo "─────────────────────────────────────────────────────────────"
echo "2️⃣  CORRECTNESS CHECK (40 points)"
echo "─────────────────────────────────────────────────────────────"
echo ""

# Check for key requirements in prompt
PROMPT_TEXT=$(cat "$SOLUTION_DIR/optimized-prompt.txt" | tr '[:upper:]' '[:lower:]')

REQUIREMENTS_MET=0
REQUIREMENTS_TOTAL=7

check_requirement() {
    local name="$1"
    local pattern="$2"

    if echo "$PROMPT_TEXT" | grep -q "$pattern"; then
        echo "   ✅ $name"
        return 0
    else
        echo "   ❌ $name (not found: $pattern)"
        return 1
    fi
}

echo "Checking for required elements in prompt:"
echo ""

check_requirement "Python 3.11 specified" "python.*3\.11\|3\.11.*python" && REQUIREMENTS_MET=$((REQUIREMENTS_MET + 1))
check_requirement "Non-root user mentioned" "non-root\|user\|appuser" && REQUIREMENTS_MET=$((REQUIREMENTS_MET + 1))
check_requirement "Health check specified" "health" && REQUIREMENTS_MET=$((REQUIREMENTS_MET + 1))
check_requirement "Dependencies mentioned" "requirements\.txt\|dependencies\|install" && REQUIREMENTS_MET=$((REQUIREMENTS_MET + 1))
check_requirement "Entry point specified" "entry\|run\|start\|app\.py\|flask run" && REQUIREMENTS_MET=$((REQUIREMENTS_MET + 1))
check_requirement "Port mentioned" "port\|5000\|expose" && REQUIREMENTS_MET=$((REQUIREMENTS_MET + 1))
check_requirement "Dockerfile intent clear" "dockerfile" && REQUIREMENTS_MET=$((REQUIREMENTS_MET + 1))

echo ""
CORRECTNESS_PCT=$((REQUIREMENTS_MET * 100 / REQUIREMENTS_TOTAL))
CORRECTNESS_SCORE=$((REQUIREMENTS_MET * 40 / REQUIREMENTS_TOTAL))

echo "   Requirements met: $REQUIREMENTS_MET/$REQUIREMENTS_TOTAL ($CORRECTNESS_PCT%)"
echo "   Correctness score: $CORRECTNESS_SCORE/40"
echo ""

# ===================================================================
# 3. QUALITY CHECK (20% of grade)
# ===================================================================
echo "─────────────────────────────────────────────────────────────"
echo "3️⃣  QUALITY CHECK (20 points)"
echo "─────────────────────────────────────────────────────────────"
echo ""

QUALITY_ISSUES=0

# Check for common issues
if echo "$PROMPT_TEXT" | grep -q "hello\|hi\|thanks\|please\|sorry"; then
    echo "   ⚠️  Contains unnecessary pleasantries"
    QUALITY_ISSUES=$((QUALITY_ISSUES + 1))
fi

if echo "$PROMPT_TEXT" | grep -q "first,\|second,\|third,"; then
    echo "   ⚠️  Uses verbose enumeration (use bullets)"
    QUALITY_ISSUES=$((QUALITY_ISSUES + 1))
fi

SENTENCE_COUNT=$(echo "$PROMPT_TEXT" | grep -o '\.' | wc -l)
if [ "$SENTENCE_COUNT" -gt 20 ]; then
    echo "   ⚠️  Too many sentences (use bullet points)"
    QUALITY_ISSUES=$((QUALITY_ISSUES + 1))
fi

# Check for good practices
if echo "$PROMPT_TEXT" | grep -q "^-\|^*\|^•"; then
    echo "   ✅ Uses bullet points"
else
    echo "   ⚠️  No bullet points detected"
    QUALITY_ISSUES=$((QUALITY_ISSUES + 1))
fi

if echo "$PROMPT_TEXT" | grep -q "best practice"; then
    echo "   ✅ Delegates to model expertise"
fi

# Calculate quality score
if [ "$QUALITY_ISSUES" -eq 0 ]; then
    QUALITY_SCORE=20
    echo ""
    echo "   ✅ Quality: 20/20 (excellent)"
elif [ "$QUALITY_ISSUES" -le 2 ]; then
    QUALITY_SCORE=15
    echo ""
    echo "   ✅ Quality: 15/20 (good)"
else
    QUALITY_SCORE=10
    echo ""
    echo "   ⚠️  Quality: 10/20 (needs improvement)"
fi

echo ""

# ===================================================================
# 4. TIME BONUS (if tracked)
# ===================================================================
if [ -f "$SOLUTION_DIR/.start-time" ]; then
    echo "─────────────────────────────────────────────────────────────"
    echo "4️⃣  TIME BONUS"
    echo "─────────────────────────────────────────────────────────────"
    echo ""

    START_TIME=$(cat "$SOLUTION_DIR/.start-time")
    END_TIME=$(date +%s)
    ELAPSED=$((END_TIME - START_TIME))
    MINUTES=$((ELAPSED / 60))

    echo "   ⏱️  Time elapsed: ${MINUTES} minutes"

    if [ "$MINUTES" -le 10 ]; then
        BONUS_POINTS=$((BONUS_POINTS + 10))
        echo "   🏆 Speed bonus: +10 points (under 10 minutes)"
    elif [ "$MINUTES" -le 15 ]; then
        echo "   ✅ Within time limit (15 minutes)"
    else
        PENALTY_POINTS=$((PENALTY_POINTS - 10))
        echo "   ⚠️  Over time limit"
        echo "   ⚠️  Penalty: -10 points"
    fi
    echo ""
fi

# ===================================================================
# 5. HINT PENALTY
# ===================================================================
HINT_FILE="$HOME/.ai-devops-quest/hints-prompt-dojo-01.txt"
if [ -f "$HINT_FILE" ]; then
    HINTS_USED=$(wc -l < "$HINT_FILE")
    if [ "$HINTS_USED" -gt 0 ]; then
        echo "─────────────────────────────────────────────────────────────"
        echo "5️⃣  HINT PENALTY"
        echo "─────────────────────────────────────────────────────────────"
        echo ""
        echo "   ℹ️  Hints used: $HINTS_USED"
        echo "   ⚠️  Penalty: -$((HINTS_USED * 5)) points"
        PENALTY_POINTS=$((PENALTY_POINTS - (HINTS_USED * 5)))
        echo ""
    fi
fi

# ===================================================================
# FINAL SCORE
# ===================================================================
echo "═════════════════════════════════════════════════════════════"
echo " 📊 FINAL SCORE"
echo "═════════════════════════════════════════════════════════════"
echo ""

BASE_SCORE=$((CORRECTNESS_SCORE + EFFICIENCY_SCORE + QUALITY_SCORE))
TOTAL_SCORE=$((BASE_SCORE + BONUS_POINTS + PENALTY_POINTS))

if [ "$TOTAL_SCORE" -lt 0 ]; then
    TOTAL_SCORE=0
fi

echo "  Correctness:      ${CORRECTNESS_SCORE}/40"
echo "  Efficiency:       ${EFFICIENCY_SCORE}/40"
echo "  Quality:          ${QUALITY_SCORE}/20"
echo "  ────────────────────────"
echo "  Base Score:       ${BASE_SCORE}/100"
echo ""

if [ "$BONUS_POINTS" -gt 0 ]; then
    echo "  Bonuses:          +${BONUS_POINTS}"
fi

if [ "$PENALTY_POINTS" -lt 0 ]; then
    echo "  Penalties:        ${PENALTY_POINTS}"
fi

if [ "$BONUS_POINTS" -gt 0 ] || [ "$PENALTY_POINTS" -lt 0 ]; then
    echo "  ────────────────────────"
fi

echo "  TOTAL SCORE:      ${TOTAL_SCORE} points"
echo ""

# Performance rating
if [ "$TOTAL_SCORE" -ge 90 ]; then
    echo "  🏆 RATING: MASTER (90+)"
    echo "     Outstanding work! You've mastered token optimization."
elif [ "$TOTAL_SCORE" -ge 75 ]; then
    echo "  ⭐ RATING: EXPERT (75-89)"
    echo "     Excellent! You understand token efficiency well."
elif [ "$TOTAL_SCORE" -ge 60 ]; then
    echo "  ✅ RATING: PROFICIENT (60-74)"
    echo "     Good job! You're on the right track."
elif [ "$TOTAL_SCORE" -ge 40 ]; then
    echo "  ⚠️  RATING: DEVELOPING (40-59)"
    echo "     Keep practicing. Review the reference solution."
else
    echo "  ❌ RATING: NEEDS WORK (<40)"
    echo "     Review chapter 3 and try again."
fi

echo ""
echo "═════════════════════════════════════════════════════════════"
echo ""

# Update progress tracker
echo "📝 Next steps:"
echo ""
echo "  1. Review solutions/ directory for alternative approaches"
echo "  2. Update your progress tracker:"
echo "     cd ../../progress-tracker"
if [ -f "$SOLUTION_DIR/.start-time" ]; then
    echo "     python tracker.py complete-challenge prompt-dojo-01 --time $ELAPSED --tokens ${TOKEN_COUNT:-0}"
else
    echo "     python tracker.py complete-challenge prompt-dojo-01 --tokens ${TOKEN_COUNT:-0}"
fi
echo ""

# Save score for tracking
echo "$TOTAL_SCORE" > "$SOLUTION_DIR/.score"

if [ "$TOTAL_SCORE" -ge 60 ]; then
    echo "✅ Challenge complete! Well done! 🎉"
else
    echo "Keep practicing! You can retry unlimited times."
fi
echo ""
