# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### 🎮 Major Addition: DevOps Quest Gamification System

A complete interactive learning layer that transforms the guide into an engaging, hands-on experience.

### Added

#### Progress Tracker System
- **Progress Dashboard** with beautiful ASCII UI using Rich library
- **Achievement/Badge System** with 15 unlockable badges
- **Streak Tracking** for daily learning habits
- **Player Profiles** stored in `~/.ai-devops-quest/`
- **CLI Interface** for tracking completions and viewing stats
- **Achievement Logic** for automatic badge awarding based on conditions

#### Challenge System
- **Challenge 01: Prompt Dojo** - Token Minimization (⭐⭐)
  - Reduce prompt tokens by 75% while maintaining quality
  - Auto-grader with correctness, efficiency, and quality scoring
  - Progressive 3-hint system (costs points)
  - Reference solution with detailed analysis
  - Multiple difficulty modes (Normal, Hard, Nightmare)
- **Challenge 02: Token Detective** (⭐⭐⭐)
  - Audit and optimize 5 production prompts
  - 60% token reduction goal (8500 → 3400 tokens)
- **Challenge 03: CRAFT Master** (⭐⭐⭐)
  - Master the CRAFT framework for perfect code generation
  - Generate production-ready code on first try
- **Challenge 04: Claude Code Basics** (⭐)
  - First hands-on session with Claude Code
  - 5 fundamental tasks to complete
- **Token Counter Utility** (`challenges/lib/count-tokens.py`)
  - Accurate token counting using tiktoken
  - Challenge-specific feedback and scoring
- **Auto-Grader Framework** for instant feedback
- **Hint Systems** with progressive disclosure

#### Story Mode System
- **Chapter 6: "The Midnight Deployment Crisis"** 🚨
  - Immersive 450-line narrative experience
  - Production incident at 2:47 AM scenario
  - 30-minute time-pressured mission
  - Multiple difficulty levels (Novice, Normal, Hard, Nightmare)
  - Real-time event simulation
  - Success/failure outcomes with consequences
- **Interactive Launcher** (`story-mode/play.sh`)
  - Menu-driven chapter selection
  - Progress tracking integration

#### Sandbox Environment System
- **Incident 01: CrashLoopBackOff** (⭐⭐)
  - Full Docker Compose environment
  - Broken Flask API with intentional configuration bug
  - PostgreSQL database integration
  - Auto-grader with 4 test categories
  - 60-second stability check
  - Progressive hint system
  - Realistic production debugging scenario

#### Documentation
- `gamification/README.md` - Comprehensive system overview
- `gamification/TODO.md` - Detailed implementation roadmap (200+ items)
- `gamification/IMPLEMENTATION_SUMMARY.md` - Status and architecture
- `gamification/TEST_RESULTS.md` - Complete test report
- `gamification/COMPLETE.md` - Achievement summary
- Updated `CLAUDE.md` with gamification section

#### Repository Improvements
- **CLAUDE.md** - Added for Claude Code instances to understand repo
- **CHANGELOG.md** - This file (project changelog)
- Updated README.md structure in CLAUDE.md

### Changed
- **CLAUDE.md**: Added gamification system documentation
- **Repository Structure**: Added `gamification/` directory to structure

### Technical Details

**Files Added**: 39+
**Lines of Code**: 2,585+
**Languages**: Python, Bash, Markdown, YAML, Dockerfile
**Dependencies**: rich, click, pyyaml, python-dateutil, tiktoken

### Learning Paths

Three distinct paths for different learning styles:
- 🚀 **Speed Run** (20 hours) - Core challenges, minimum viable
- 🎓 **Knowledge Master** (40-60 hours) - Complete mastery
- ⚡ **Hybrid** (30-40 hours) - Balanced approach (recommended)

### Features

- **Token Economics Focus** - Real-world cost optimization skills
- **Multi-Difficulty Modes** - Same challenge, harder constraints
- **Progressive Hints** - Strategic help without solving
- **Realistic Scenarios** - Production-like environments
- **Auto-Grading** - Instant feedback on solutions
- **Visual Progress** - Beautiful terminal dashboards
- **Achievement System** - 15 badges to unlock
- **Streak Tracking** - Daily learning habit building

### Testing
- ✅ All Python syntax validated
- ✅ All shell scripts tested
- ✅ Integration tests passing
- ✅ End-to-end flow verified

### Breaking Changes
None - All additions, no modifications to existing content

---

## [0.1.1] - 2026-01-09

### Changed
- Updated guide with Claude Code 2.1.x changelog features
- Added hands-on practice references to Chapters 8 and 9
- Added Community Tools & Utilities section to Additional Resources
- Revised README for v1.1.0 updates and enhancements

### Fixed
- README formatting in Community Tools & Utilities section

---

## [0.1.0] - 2025-XX-XX

### Added
- Initial release of "AI and Claude Code: A Comprehensive Guide for DevOps Engineers"
- 10 comprehensive chapters covering AI fundamentals through advanced Claude Code usage
- Chapter 1: Introduction to AI
- Chapter 2: Understanding LLMs and Tokens
- Chapter 3: The Art of Prompting (CRAFT Framework)
- Chapter 4: AI Models Landscape
- Chapter 5: Introduction to Claude
- Chapter 6: Claude Code Fundamentals
- Chapter 7: Claude Code Intermediate
- Chapter 8: Claude Code Professional
- Chapter 9: MCP Deep Dive
- Chapter 10: AI for DevOps
- Marp presentation slides for all chapters
- Code examples for each chapter in `src/`
- GitHub Actions workflow for generating PowerPoint presentations
- CC BY-NC 4.0 License
- Contributing guidelines

---

## Upgrade Guide

### From v0.1.x to v1.0.0

**New Features Available**:
1. Initialize your gamification profile:
   ```bash
   cd gamification/progress-tracker
   pip install -r requirements.txt
   python tracker.py init
   ```

2. Try your first challenge:
   ```bash
   cd gamification/challenges/01-prompt-dojo
   ./start.sh
   ```

3. Experience story mode:
   ```bash
   cd gamification/story-mode
   ./play.sh
   ```

**No Breaking Changes**: All existing guide content remains unchanged.

---

## Links

- [Repository](https://github.com/michelabboud/ai-and-claude-code-intro)
- [License](./LICENSE)
- [Contributing](./CONTRIBUTING.md)
- [Gamification README](./gamification/README.md)

---

**Note**: Version 1.0.0 represents the first major milestone with the complete gamification system, making this guide production-ready for interactive learning.
