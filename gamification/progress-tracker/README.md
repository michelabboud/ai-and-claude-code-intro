# Progress Tracker

Visual dashboard tracking your AI and Claude Code learning journey.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize your profile
python tracker.py init

# View dashboard
python tracker.py

# Quick stats
python tracker.py summary
```

## Usage

```bash
# Mark completions
python tracker.py complete-chapter 6
python tracker.py complete-challenge prompt-dojo-01 --time 300 --tokens 450
python tracker.py complete-sandbox incident-01

# View badges
python tracker.py badges
```

## Implementation Status

✅ Core structure complete
✅ Profile management
✅ Progress tracking
✅ Dashboard rendering
✅ Streak calculation
⚠️ **Achievement checking logic** - Ready for YOUR implementation!

See `tracker.py` lines 150-200 for the TODO sections.

## Your Implementation Task

Complete the achievement checking system in `AchievementChecker` class:

### 1. `_check_condition()` method
Implement logic to check if achievement conditions are met.

### 2. `_compare()` method
Handle comparison operators: `>=`, `<=`, `==`, `<`, `>`

See inline comments in `tracker.py` for guidance!
