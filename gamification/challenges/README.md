# 🏆 DevOps Quest Challenges

Progressive missions to master AI and Claude Code skills.

## Challenge Structure

Each challenge includes:
- `README.md` - Mission brief and instructions
- `challenge.yaml` - Configuration (difficulty, points, time limits)
- `starter/` - Starting templates and files
- `solutions/` - Reference solutions and alternatives
- `test-suite/` - Auto-grader scripts
- `start.sh` - Quick launch script

## Available Challenges

### 📚 Chapter 3: Prompt Engineering

| ID | Challenge | Difficulty | Points | Time Limit |
|----|-----------|------------|--------|------------|
| prompt-dojo-01 | Token Minimization | ⭐⭐ | 20 | 15 min |
| prompt-dojo-02 | CRAFT Framework Mastery | ⭐⭐⭐ | 30 | 20 min |
| prompt-dojo-03 | Context Compression | ⭐⭐⭐ | 40 | 20 min |

### 🔧 Chapter 6-7: Claude Code Basics

| ID | Challenge | Difficulty | Points | Time Limit |
|----|-----------|------------|--------|------------|
| claude-basics-01 | First Session | ⭐ | 10 | 10 min |
| claude-basics-02 | File Navigation | ⭐⭐ | 15 | 10 min |
| claude-basics-03 | Custom Command | ⭐⭐⭐ | 25 | 20 min |

### 🔌 Chapters 10-11: MCP Servers

| ID | Challenge | Difficulty | Points | Time Limit |
|----|-----------|------------|--------|------------|
| mcp-quickstart | Build Your First Server | ⭐⭐⭐ | 30 | 20 min |
| mcp-custom-tool | Add Custom Tool | ⭐⭐⭐⭐ | 40 | 25 min |
| mcp-speedrun | Full Server in 15min | ⭐⭐⭐⭐⭐ | 100 | 15 min |

### 🐉 Boss Battles

| ID | Challenge | Difficulty | Points | Time Limit |
|----|-----------|------------|--------|------------|
| boss-legacy-monolith | The Legacy Monolith | ⭐⭐⭐⭐⭐ | 150 | 30 min |
| boss-toxic-codebase | The Toxic Codebase | ⭐⭐⭐⭐⭐ | 150 | 30 min |
| boss-integration | The Integration Nightmare | ⭐⭐⭐⭐⭐ | 200 | 45 min |

## Quick Start

```bash
# Start a challenge
cd challenges/01-prompt-dojo
./start.sh

# Or manual start
cat README.md  # Read mission brief
# ... complete the challenge ...

# Check your solution
./test-suite/grade.sh
```

## Learning Paths

### 🚀 Speed Run Path
Focus: Time-based completion, minimum viable solutions
- Skip optional challenges
- Use hints liberally
- Focus on getting it working
**Target**: 20 hours total

### 🎓 Knowledge Master Path
Focus: Deep understanding, explore all alternatives
- Complete all challenges
- Study all solution approaches
- Master theory before practice
**Target**: 40-60 hours total

### ⚡ Hybrid Path (Recommended)
Focus: Balance speed with understanding
- Complete core challenges
- Review 2-3 solution approaches
- Skip only truly optional content
**Target**: 30-40 hours total

## Challenge Difficulty Levels

| Stars | Level | Description |
|-------|-------|-------------|
| ⭐ | Novice | Guided, clear instructions |
| ⭐⭐ | Apprentice | Some autonomy required |
| ⭐⭐⭐ | Journeyman | Real-world complexity |
| ⭐⭐⭐⭐ | Expert | Multi-step, minimal guidance |
| ⭐⭐⭐⭐⭐ | Master | Boss battles, time pressure |

## Scoring System

### Base Points
Awarded for challenge completion (see table above)

### Bonuses
- **Speed Bonus**: +10-50 pts (complete in top 25% time)
- **Efficiency Bonus**: +20 pts (optimal token usage)
- **No Hints Bonus**: +10 pts (complete without hints)
- **First Try Bonus**: +5 pts (no failed attempts)

### Penalties
- **Hint Usage**: -5 pts per hint
- **Excessive Time**: -10 pts (>2x time limit)
- **Multiple Attempts**: -5 pts per retry

## Hint System

Each challenge has 3 progressive hints:

```bash
# View available hints
./hints.sh list

# Get a hint (costs 5 points)
./hints.sh 1
./hints.sh 2
./hints.sh 3
```

Hints are designed to unblock, not solve. Use wisely!

## Auto-Grader

Challenges are auto-graded on:
- **Correctness**: Does it work?
- **Efficiency**: Token usage, time taken
- **Quality**: Code style, best practices
- **Completeness**: All requirements met

```bash
# Run grader
./test-suite/grade.sh

# Sample output:
# ✅ Correctness: 100% (all tests pass)
# ⚡ Efficiency: 90% (520 tokens, target: 500)
# 🎨 Quality: 85% (minor style issues)
# 📊 Overall Score: 92/100
```

## Submitting Solutions

Share your approach with the community:

```bash
# Export your solution
../lib/export-solution.sh prompt-dojo-01

# Creates: solutions/community/prompt-dojo-01-{username}.md
```

## Creating Custom Challenges

Want to contribute? See `CHALLENGE_TEMPLATE/` for the structure:

```bash
cp -r CHALLENGE_TEMPLATE/ my-custom-challenge/
# Edit files...
# Submit PR!
```

## Tips for Success

### 🎯 Before Starting
1. Read the mission brief carefully
2. Check time limit and difficulty
3. Review related chapter content
4. Set a timer (optional, for realism)

### 💪 During Challenge
1. Start with a plan (don't dive in)
2. Test incrementally
3. Use hints if stuck >5 minutes
4. Time management over perfection

### 🏆 After Completion
1. Check your score
2. Review solution alternatives
3. Update your progress tracker
4. Reflect: What did you learn?

## Common Issues

### "Auto-grader not working"
```bash
# Ensure scripts are executable
chmod +x test-suite/*.sh
chmod +x *.sh
```

### "Can't start challenge"
```bash
# Check you're in the challenge directory
cd challenges/01-prompt-dojo
pwd  # Should show: .../challenges/01-prompt-dojo
```

### "Dependencies missing"
```bash
# Install challenge dependencies
pip install -r requirements.txt  # If Python challenge
npm install  # If Node/TypeScript challenge
```

## Challenge Status

Track which challenges you've completed:

```bash
# In progress tracker
cd ../../progress-tracker
python tracker.py summary
```

---

**Ready to prove your skills? Choose your first challenge and begin! 🚀**

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0
