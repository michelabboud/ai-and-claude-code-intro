"""
Fix navigation and footers for all chapters to match Chapter 23 standard.
"""

from pathlib import Path
import re

chapters_dir = Path("../chapters")

# Chapter information: (number, title, part, prev_num, next_num, filename)
chapters_info = [
    (1, "Introduction to AI", "Part 1: AI Fundamentals", None, 2, "01-introduction-to-ai.md"),
    (2, "Understanding LLMs and Tokens", "Part 1: AI Fundamentals", 1, 3, "02-understanding-llms-and-tokens.md"),
    (3, "The Art of Prompting", "Part 1: AI Fundamentals", 2, 4, "03-the-art-of-prompting.md"),
    (4, "AI Models Landscape", "Part 2: The AI Ecosystem", 3, 5, "04-ai-models-landscape.md"),
    (5, "Introduction to Claude", "Part 2: The AI Ecosystem", 4, 6, "05-introduction-to-claude.md"),
    (6, "Claude Code Fundamentals", "Part 3: Claude Code Mastery", 5, 7, "06-claude-code-fundamentals.md"),
    (7, "Claude Code Intermediate", "Part 3: Claude Code Mastery", 6, 8, "07-claude-code-intermediate.md"),
    (8, "Skills and Sub-Agents", "Part 3: Claude Code Mastery", 7, 9, "08-skills-and-subagents.md"),
    (9, "Hooks and Advanced Features", "Part 3: Claude Code Mastery", 8, 10, "09-hooks-and-advanced-features.md"),
    (10, "MCP Fundamentals", "Part 4: MCP Integration", 9, 11, "10-mcp-fundamentals.md"),
    (11, "MCP Server Development", "Part 4: MCP Integration", 10, 12, "11-mcp-server-development.md"),
    (12, "AI for DevOps", "Part 5: Workflow Automation", 11, 13, "12-ai-for-devops.md"),
    (13, "n8n Fundamentals", "Part 5: Workflow Automation", 12, 14, "13-n8n-fundamentals.md"),
    (14, "Advanced n8n Workflows", "Part 5: Workflow Automation", 13, 15, "14-n8n-advanced.md"),
    (15, "Multi-Agent Fundamentals", "Part 6: Multi-Agent Orchestration & AIOps", 14, 16, "15-multi-agent-fundamentals.md"),
    (16, "Advanced Multi-Agent Workflows", "Part 6: Multi-Agent Orchestration & AIOps", 15, 17, "16-multi-agent-advanced.md"),
    (17, "AIOps Fundamentals", "Part 6: Multi-Agent Orchestration & AIOps", 16, 18, "17-aiops-fundamentals.md"),
    (18, "Advanced AIOps", "Part 6: Multi-Agent Orchestration & AIOps", 17, 19, "18-aiops-advanced.md"),
    (19, "Team Transformation", "Part 7: Advanced Agentic Development & Leadership", 18, 20, "19-team-transformation.md"),
    (20, "Agent Loop Detection & Prevention", "Part 7: Advanced Agentic Development & Leadership", 19, 21, "20-agent-loop-detection.md"),
    (21, "Building Resilient Agentic Systems", "Part 7: Advanced Agentic Development & Leadership", 20, 22, "21-resilient-agentic-systems.md"),
    (22, "RAG Fundamentals", "Part 8: Advanced Agentic Development", 21, 23, "22-rag-fundamentals.md"),
    (23, "Advanced RAG Patterns", "Part 8: Advanced Agentic Development", 22, None, "23-advanced-rag-patterns.md"),
]

def get_chapter_filename(num):
    """Get chapter filename from number"""
    return chapters_info[num-1][5]

def create_nav_section(chapter_num, prev_num, next_num):
    """Create navigation section"""
    nav_parts = []

    if prev_num:
        prev_title = chapters_info[prev_num-1][1]
        prev_file = get_chapter_filename(prev_num)
        nav_parts.append(f"← Previous: [Chapter {prev_num}: {prev_title}](./{prev_file})")
    else:
        nav_parts.append("← Previous: [README](../README.md)")

    nav_parts.append(" | ")

    if next_num:
        next_title = chapters_info[next_num-1][1]
        next_file = get_chapter_filename(next_num)
        nav_parts.append(f"Next: [Chapter {next_num}: {next_title}](./{next_file}) →")
    else:
        nav_parts.append("Next: TBD →")

    return ''.join(nav_parts)

def fix_chapter(chapter_num):
    """Fix a single chapter's navigation and footer"""

    info = chapters_info[chapter_num - 1]
    num, title, part, prev_num, next_num, _ = info

    # Get filename
    filename = get_chapter_filename(num)
    filepath = chapters_dir / filename

    if not filepath.exists():
        print(f"❌ Chapter {num} not found: {filename}")
        return False

    print(f"Processing Chapter {num}: {title}...")

    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')

    # Check if already has navigation at top
    has_top_nav = any('## Navigation' in line for line in lines[:30])

    # Create top navigation
    nav_line = create_nav_section(num, prev_num, next_num)
    top_nav = f"""
**{part}**

---

## Navigation

{nav_line}

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---
"""

    # Create bottom navigation and footer
    bottom_nav = f"""
---

## Navigation

{nav_line}

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter {num}** | {title} | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
"""

    # Add top navigation if missing
    if not has_top_nav:
        # Find the first line starting with # (title)
        title_line_idx = next(i for i, line in enumerate(lines) if line.startswith('# Chapter'))

        # Insert after title
        lines.insert(title_line_idx + 1, top_nav)
        print(f"  ✅ Added top navigation")
    else:
        print(f"  ⏭️  Top navigation already exists")

    # Rejoin content
    content = '\n'.join(lines)

    # Remove existing footer patterns
    content = re.sub(r'\n---\n\n\*\*End of Chapter \d+\*\*.*?\n', '', content)
    content = re.sub(r'\n---\n\n\*\*Chapter \d+.*?Michel Abboud.*?\n', '', content)
    content = re.sub(r'\*Created with Claude AI.*?CC BY-NC.*?\n', '', content)

    # Add bottom navigation and footer
    content = content.rstrip() + '\n' + bottom_nav

    print(f"  ✅ Added/updated bottom navigation and footer")

    # Write back
    with open(filepath, 'w') as f:
        f.write(content)

    return True

if __name__ == "__main__":
    print("="*80)
    print("Fixing Navigation and Footers for All Chapters")
    print("="*80)

    success_count = 0
    for chapter_num in range(1, 24):
        if fix_chapter(chapter_num):
            success_count += 1
        print()

    print("="*80)
    print(f"✅ Successfully processed {success_count}/23 chapters")
    print("="*80)
