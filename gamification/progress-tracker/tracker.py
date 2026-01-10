#!/usr/bin/env python3
"""
DevOps Quest Progress Tracker
Tracks learning progress, achievements, and streaks for the AI and Claude Code guide.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich import box

console = Console()

# Configuration
HOME_DIR = Path.home()
QUEST_DIR = HOME_DIR / ".ai-devops-quest"
PROFILE_FILE = QUEST_DIR / "profile.json"
ACHIEVEMENTS_FILE = Path(__file__).parent / "achievements.json"

# Total counts for progress calculation
TOTAL_CHAPTERS = 10
TOTAL_CHALLENGES = 30  # Will be updated as challenges are added
TOTAL_SANDBOXES = 10
TOTAL_BOSS_BATTLES = 5


class QuestProfile:
    """Manages user profile and progress data"""

    def __init__(self, profile_path: Path = PROFILE_FILE):
        self.profile_path = profile_path
        self.data = self._load_profile()

    def _load_profile(self) -> Dict:
        """Load profile from disk or create new"""
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return self._create_default_profile()

    def _create_default_profile(self) -> Dict:
        """Create a new profile with default values"""
        return {
            "username": "Anonymous DevOps Engineer",
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "settings": {
                "difficulty": "journeyman",
                "enable_story_mode": True,
                "enable_leaderboards": False,
                "hint_penalty": -5,
                "speed_bonus_threshold": 0.25,
                "local_only": True
            },
            "progress": {
                "chapters_completed": [],
                "challenges_completed": [],
                "sandboxes_completed": [],
                "boss_battles_completed": [],
                "story_mode_completed": [],
                "mcp_servers_built": 0
            },
            "achievements": {
                "earned": [],
                "points": 0
            },
            "stats": {
                "total_time_minutes": 0,
                "min_tokens_used": float('inf'),
                "challenges_by_time": {},  # challenge_id: completion_time_seconds
                "activity_dates": [],  # List of ISO dates when active
                "current_streak": 0,
                "longest_streak": 0
            }
        }

    def save(self):
        """Save profile to disk"""
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        self.data["last_active"] = datetime.now().isoformat()
        with open(self.profile_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def update_activity(self):
        """Update last active date and streak"""
        today = datetime.now().date().isoformat()
        activity_dates = self.data["stats"]["activity_dates"]

        if today not in activity_dates:
            activity_dates.append(today)
            self._calculate_streak()
            self.save()

    def _calculate_streak(self):
        """Calculate current and longest streak"""
        dates = sorted([datetime.fromisoformat(d).date() for d in self.data["stats"]["activity_dates"]])
        if not dates:
            return

        current_streak = 1
        longest_streak = 1
        temp_streak = 1

        for i in range(len(dates) - 1):
            diff = (dates[i + 1] - dates[i]).days
            if diff == 1:
                temp_streak += 1
                current_streak = temp_streak
                longest_streak = max(longest_streak, temp_streak)
            elif diff > 1:
                temp_streak = 1

        self.data["stats"]["current_streak"] = current_streak
        self.data["stats"]["longest_streak"] = longest_streak

    def mark_chapter_complete(self, chapter_num: int):
        """Mark a chapter as completed"""
        if chapter_num not in self.data["progress"]["chapters_completed"]:
            self.data["progress"]["chapters_completed"].append(chapter_num)
            self.update_activity()
            self.save()
            console.print(f"✅ Chapter {chapter_num} marked as complete!", style="bold green")

    def mark_challenge_complete(self, challenge_id: str, time_seconds: Optional[int] = None, tokens_used: Optional[int] = None):
        """Mark a challenge as completed"""
        if challenge_id not in self.data["progress"]["challenges_completed"]:
            self.data["progress"]["challenges_completed"].append(challenge_id)

            if time_seconds:
                self.data["stats"]["challenges_by_time"][challenge_id] = time_seconds

            if tokens_used:
                self.data["stats"]["min_tokens_used"] = min(
                    self.data["stats"]["min_tokens_used"],
                    tokens_used
                )

            self.update_activity()
            self.save()
            console.print(f"✅ Challenge '{challenge_id}' complete!", style="bold green")

    def mark_sandbox_complete(self, sandbox_id: str):
        """Mark a sandbox incident as resolved"""
        if sandbox_id not in self.data["progress"]["sandboxes_completed"]:
            self.data["progress"]["sandboxes_completed"].append(sandbox_id)
            self.update_activity()
            self.save()
            console.print(f"✅ Sandbox '{sandbox_id}' resolved!", style="bold green")

    def get_completion_percentage(self) -> float:
        """Calculate overall completion percentage"""
        total_items = TOTAL_CHAPTERS + TOTAL_CHALLENGES + TOTAL_SANDBOXES
        completed_items = (
            len(self.data["progress"]["chapters_completed"]) +
            len(self.data["progress"]["challenges_completed"]) +
            len(self.data["progress"]["sandboxes_completed"])
        )
        return (completed_items / total_items) * 100 if total_items > 0 else 0


class AchievementChecker:
    """Checks and awards achievements"""

    def __init__(self, profile: QuestProfile):
        self.profile = profile
        self.achievements = self._load_achievements()

    def _load_achievements(self) -> List[Dict]:
        """Load achievement definitions"""
        with open(ACHIEVEMENTS_FILE, 'r') as f:
            data = json.load(f)
        return data["achievements"]

    def check_achievements(self) -> List[Dict]:
        """Check for newly earned achievements"""
        newly_earned = []
        earned_ids = self.profile.data["achievements"]["earned"]

        for achievement in self.achievements:
            if achievement["id"] in earned_ids:
                continue

            if self._check_condition(achievement["condition"]):
                self._award_achievement(achievement)
                newly_earned.append(achievement)

        return newly_earned

    def _check_condition(self, condition: Dict) -> bool:
        """
        Check if an achievement condition is met.

        Args:
            condition: Dict with 'type', 'operator', 'value'

        Returns:
            bool: True if condition is met
        """
        condition_type = condition["type"]
        operator = condition["operator"]
        target_value = condition["value"]

        progress = self.profile.data["progress"]
        stats = self.profile.data["stats"]

        # Simple count conditions
        if condition_type == "challenges_completed":
            actual = len(progress["challenges_completed"])
            return self._compare(actual, operator, target_value)

        elif condition_type == "chapters_completed":
            actual = len(progress["chapters_completed"])
            return self._compare(actual, operator, target_value)

        elif condition_type == "sandboxes_completed":
            actual = len(progress["sandboxes_completed"])
            return self._compare(actual, operator, target_value)

        elif condition_type == "boss_battles_completed":
            actual = len(progress["boss_battles_completed"])
            if target_value == "all":
                return actual == TOTAL_BOSS_BATTLES
            return self._compare(actual, operator, target_value)

        # Token efficiency
        elif condition_type == "min_tokens_used":
            actual = stats["min_tokens_used"]
            if actual == float('inf'):
                return False  # No challenges completed yet
            return self._compare(actual, operator, target_value)

        # Streak tracking
        elif condition_type == "streak_days":
            actual = stats["current_streak"]
            return self._compare(actual, operator, target_value)

        # Completion percentage
        elif condition_type == "completion_percentage":
            actual = self.profile.get_completion_percentage()
            return self._compare(actual, operator, target_value)

        # Challenge series completion
        elif condition_type == "challenge_series_completed":
            series_name = target_value
            series_challenges = [c for c in progress["challenges_completed"]
                                if c.startswith(series_name)]
            # For now, check if at least 3 challenges from series completed
            return len(series_challenges) >= 3

        # Chapter challenges completion
        elif condition_type == "chapter_challenges_completed":
            # Check if all challenges in a specific chapter are done
            # This is a placeholder - would need challenge-to-chapter mapping
            return False

        # MCP servers built
        elif condition_type == "mcp_servers_built":
            actual = progress.get("mcp_servers_built", 0)
            return self._compare(actual, operator, target_value)

        # Time-based percentile (for speed bonus)
        elif condition_type == "completion_time_percentile":
            # This requires historical data - for now, skip
            return False

        # Hard mode boss battles
        elif condition_type == "hard_mode_boss_completed":
            # Track this in progress when we implement boss battles
            return False

        return False

    def _compare(self, actual, operator: str, target) -> bool:
        """Helper to compare values with operator"""
        if operator == ">=":
            return actual >= target
        elif operator == "<=":
            return actual <= target
        elif operator == "==":
            return actual == target
        elif operator == "<":
            return actual < target
        elif operator == ">":
            return actual > target
        else:
            return False

    def _award_achievement(self, achievement: Dict):
        """Award an achievement to the user"""
        self.profile.data["achievements"]["earned"].append(achievement["id"])
        self.profile.data["achievements"]["points"] += achievement["points"]
        self.profile.save()

        console.print()
        console.print(Panel(
            f"[bold yellow]🎉 NEW ACHIEVEMENT UNLOCKED! 🎉[/bold yellow]\n\n"
            f"{achievement['icon']} [bold]{achievement['name']}[/bold]\n"
            f"{achievement['description']}\n\n"
            f"[green]+{achievement['points']} points[/green]",
            border_style="yellow",
            box=box.DOUBLE
        ))
        console.print()


def render_dashboard(profile: QuestProfile):
    """Render the main progress dashboard"""
    progress_data = profile.data["progress"]
    stats = profile.data["stats"]
    achievements_data = profile.data["achievements"]

    # Header
    console.print()
    console.print(Panel(
        "[bold cyan]YOUR AI DEVOPS MASTERY JOURNEY[/bold cyan]",
        border_style="cyan",
        box=box.DOUBLE
    ))
    console.print()

    # Progress bars
    chapters_pct = (len(progress_data["chapters_completed"]) / TOTAL_CHAPTERS) * 100
    challenges_pct = (len(progress_data["challenges_completed"]) / TOTAL_CHALLENGES) * 100
    sandboxes_pct = (len(progress_data["sandboxes_completed"]) / TOTAL_SANDBOXES) * 100

    progress_table = Table(show_header=False, box=None, padding=(0, 2))
    progress_table.add_column(style="bold")
    progress_table.add_column()

    # Create progress bars
    chapters_bar = _create_progress_bar(chapters_pct)
    challenges_bar = _create_progress_bar(challenges_pct)
    sandboxes_bar = _create_progress_bar(sandboxes_pct)

    progress_table.add_row(
        "📚 CHAPTERS:",
        f"{chapters_bar} {chapters_pct:.0f}% ({len(progress_data['chapters_completed'])}/{TOTAL_CHAPTERS})"
    )
    progress_table.add_row(
        "🏆 CHALLENGES:",
        f"{challenges_bar} {challenges_pct:.0f}% ({len(progress_data['challenges_completed'])}/{TOTAL_CHALLENGES})"
    )
    progress_table.add_row(
        "🛠️  SANDBOXES:",
        f"{sandboxes_bar} {sandboxes_pct:.0f}% ({len(progress_data['sandboxes_completed'])}/{TOTAL_SANDBOXES})"
    )

    console.print(progress_table)
    console.print()

    # Stats
    stats_table = Table(show_header=False, box=None, padding=(0, 2))
    stats_table.add_column(style="bold")
    stats_table.add_column()

    earned_badges = achievements_data["earned"]
    badge_icons = _get_badge_icons(earned_badges)

    stats_table.add_row("🎖️  BADGES:", badge_icons if badge_icons else "None yet")
    stats_table.add_row("📊 SCORE:", f"{achievements_data['points']:,} points")
    stats_table.add_row("⏱️  TIME:", f"{stats['total_time_minutes'] // 60}h {stats['total_time_minutes'] % 60}m")
    stats_table.add_row("🔥 STREAK:", f"{stats['current_streak']} days")

    console.print(stats_table)
    console.print()

    # Next milestones
    _render_next_milestones(profile)

    # Recent achievements
    if earned_badges:
        console.print("[bold]Recent Achievements:[/bold]")
        # Show last 3 achievements
        for badge_id in earned_badges[-3:]:
            badge_info = _get_achievement_info(badge_id)
            if badge_info:
                console.print(f"  ✨ {badge_info['icon']} {badge_info['name']}")
        console.print()

    # Motivational message
    completion = profile.get_completion_percentage()
    message = _get_motivational_message(completion)
    console.print(f"[italic]{message}[/italic]")
    console.print()


def _create_progress_bar(percentage: float, width: int = 10) -> str:
    """Create an ASCII progress bar"""
    filled = int((percentage / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty


def _get_badge_icons(badge_ids: List[str]) -> str:
    """Get emoji icons for earned badges"""
    with open(ACHIEVEMENTS_FILE, 'r') as f:
        achievements = json.load(f)["achievements"]

    icons = []
    for achievement in achievements:
        if achievement["id"] in badge_ids:
            icons.append(achievement["icon"])

    return " ".join(icons)


def _get_achievement_info(badge_id: str) -> Optional[Dict]:
    """Get achievement information by ID"""
    with open(ACHIEVEMENTS_FILE, 'r') as f:
        achievements = json.load(f)["achievements"]

    for achievement in achievements:
        if achievement["id"] == badge_id:
            return achievement
    return None


def _render_next_milestones(profile: QuestProfile):
    """Show next achievable milestones"""
    console.print("[bold]NEXT MILESTONES:[/bold]")

    chapters_left = TOTAL_CHAPTERS - len(profile.data["progress"]["chapters_completed"])
    if chapters_left > 0:
        next_chapter = len(profile.data["progress"]["chapters_completed"]) + 1
        console.print(f"  ├─ Complete Chapter {next_chapter}")

    challenges_left = TOTAL_CHALLENGES - len(profile.data["progress"]["challenges_completed"])
    if challenges_left > 0:
        console.print(f"  ├─ Finish {min(3, challenges_left)} more challenge{'s' if challenges_left != 1 else ''}")

    if profile.data["stats"]["current_streak"] < 7:
        days_to_7 = 7 - profile.data["stats"]["current_streak"]
        console.print(f"  └─ Maintain streak for {days_to_7} more day{'s' if days_to_7 != 1 else ''} → Streak Master 🔥")

    console.print()


def _get_motivational_message(completion: float) -> str:
    """Get motivational message based on completion"""
    if completion == 0:
        return "🚀 Every expert was once a beginner. Let's start your journey!"
    elif completion < 25:
        return "💪 Great start! Keep the momentum going!"
    elif completion < 50:
        return "🎯 You're making solid progress. Stay focused!"
    elif completion < 75:
        return "⭐ Over halfway there! You're doing amazing!"
    elif completion < 100:
        return "🔥 So close to mastery! Finish strong!"
    else:
        return "👑 Congratulations! You've achieved complete mastery!"


# CLI Commands

@click.group()
def cli():
    """DevOps Quest Progress Tracker"""
    pass


@cli.command()
@click.option('--username', prompt='Enter your name', help='Your username')
def init(username):
    """Initialize your quest profile"""
    QUEST_DIR.mkdir(parents=True, exist_ok=True)

    profile = QuestProfile()
    profile.data["username"] = username
    profile.save()

    console.print()
    console.print(Panel(
        f"[bold green]Welcome to DevOps Quest, {username}! 🎮[/bold green]\n\n"
        f"Your quest profile has been created at:\n"
        f"[cyan]{PROFILE_FILE}[/cyan]\n\n"
        f"Ready to begin your AI mastery journey?\n"
        f"Run [bold]python tracker.py[/bold] to see your dashboard.",
        border_style="green"
    ))
    console.print()


@cli.command()
def dashboard():
    """Show your progress dashboard (default)"""
    if not PROFILE_FILE.exists():
        console.print("[red]No profile found. Run: python tracker.py init[/red]")
        return

    profile = QuestProfile()
    profile.update_activity()

    # Check for new achievements
    checker = AchievementChecker(profile)
    newly_earned = checker.check_achievements()

    render_dashboard(profile)


@cli.command()
@click.argument('chapter_num', type=int)
def complete_chapter(chapter_num):
    """Mark a chapter as completed"""
    if not PROFILE_FILE.exists():
        console.print("[red]No profile found. Run: python tracker.py init[/red]")
        return

    profile = QuestProfile()
    profile.mark_chapter_complete(chapter_num)

    # Check achievements
    checker = AchievementChecker(profile)
    checker.check_achievements()


@cli.command()
@click.argument('challenge_id')
@click.option('--time', type=int, help='Completion time in seconds')
@click.option('--tokens', type=int, help='Tokens used')
def complete_challenge(challenge_id, time, tokens):
    """Mark a challenge as completed"""
    if not PROFILE_FILE.exists():
        console.print("[red]No profile found. Run: python tracker.py init[/red]")
        return

    profile = QuestProfile()
    profile.mark_challenge_complete(challenge_id, time, tokens)

    # Check achievements
    checker = AchievementChecker(profile)
    checker.check_achievements()


@cli.command()
@click.argument('sandbox_id')
def complete_sandbox(sandbox_id):
    """Mark a sandbox incident as resolved"""
    if not PROFILE_FILE.exists():
        console.print("[red]No profile found. Run: python tracker.py init[/red]")
        return

    profile = QuestProfile()
    profile.mark_sandbox_complete(sandbox_id)

    # Check achievements
    checker = AchievementChecker(profile)
    checker.check_achievements()


@cli.command()
def badges():
    """Show all available and earned badges"""
    if not PROFILE_FILE.exists():
        console.print("[red]No profile found. Run: python tracker.py init[/red]")
        return

    profile = QuestProfile()
    earned_ids = profile.data["achievements"]["earned"]

    with open(ACHIEVEMENTS_FILE, 'r') as f:
        achievements = json.load(f)["achievements"]

    console.print()
    console.print("[bold cyan]🎖️  ACHIEVEMENT BADGES[/bold cyan]\n")

    for achievement in achievements:
        is_earned = achievement["id"] in earned_ids
        status = "✅" if is_earned else "🔒"
        style = "green" if is_earned else "dim"

        console.print(
            f"{status} {achievement['icon']} [bold {style}]{achievement['name']}[/bold {style}] "
            f"[{style}]({achievement['points']} pts)[/{style}]"
        )
        console.print(f"   [italic {style}]{achievement['description']}[/italic {style}]\n")


@cli.command()
def summary():
    """Quick stats summary"""
    if not PROFILE_FILE.exists():
        console.print("[red]No profile found. Run: python tracker.py init[/red]")
        return

    profile = QuestProfile()
    data = profile.data

    console.print(f"\n📊 [bold]{data['username']}[/bold]")
    console.print(f"   Chapters: {len(data['progress']['chapters_completed'])}/{TOTAL_CHAPTERS}")
    console.print(f"   Challenges: {len(data['progress']['challenges_completed'])}/{TOTAL_CHALLENGES}")
    console.print(f"   Sandboxes: {len(data['progress']['sandboxes_completed'])}/{TOTAL_SANDBOXES}")
    console.print(f"   Score: {data['achievements']['points']} points")
    console.print(f"   Streak: {data['stats']['current_streak']} days 🔥\n")


if __name__ == "__main__":
    # Default to dashboard if no command given
    import sys
    if len(sys.argv) == 1:
        sys.argv.append('dashboard')
    cli()
