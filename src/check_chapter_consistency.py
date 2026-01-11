"""
Check all chapters for consistent navigation and footer format.
"""

from pathlib import Path
import re

chapters_dir = Path("../chapters")
chapters = sorted(chapters_dir.glob("*.md"), key=lambda x: x.name)

print("="*80)
print("Chapter Consistency Check")
print("="*80)

# Expected patterns
nav_top_pattern = r"##\s+Navigation"
nav_bottom_pattern = r"←\s+Previous:|Next:\s+"
footer_pattern = r"\*\*Copyright\*\*:|©\s+\d{4}\s+Michel\s+Abboud"

issues = []

for chapter_file in chapters:
    chapter_name = chapter_file.name
    print(f"\n[{chapter_name}]")

    with open(chapter_file, 'r') as f:
        content = f.read()
        lines = content.split('\n')

    # Check for navigation at top (within first 30 lines)
    top_section = '\n'.join(lines[:30])
    has_nav_top = bool(re.search(nav_top_pattern, top_section))

    # Check for navigation at bottom (within last 30 lines)
    bottom_section = '\n'.join(lines[-30:])
    has_nav_bottom = bool(re.search(nav_bottom_pattern, bottom_section))

    # Check for footer
    has_footer = bool(re.search(footer_pattern, content))

    # Report
    print(f"  Navigation (top):    {'✅' if has_nav_top else '❌'}")
    print(f"  Navigation (bottom): {'✅' if has_nav_bottom else '❌'}")
    print(f"  Footer:              {'✅' if has_footer else '❌'}")

    if not has_nav_top:
        issues.append((chapter_name, "Missing navigation at top"))
    if not has_nav_bottom:
        issues.append((chapter_name, "Missing navigation at bottom"))
    if not has_footer:
        issues.append((chapter_name, "Missing or incomplete footer"))

# Summary
print("\n" + "="*80)
print("Summary")
print("="*80)

if issues:
    print(f"\nFound {len(issues)} issues:\n")
    for chapter, issue in issues:
        print(f"  • {chapter}: {issue}")

    # Group by issue type
    nav_top_missing = [c for c, i in issues if "top" in i]
    nav_bottom_missing = [c for c, i in issues if "bottom" in i]
    footer_missing = [c for c, i in issues if "footer" in i]

    print(f"\nIssue breakdown:")
    print(f"  Missing top navigation: {len(nav_top_missing)} chapters")
    print(f"  Missing bottom navigation: {len(nav_bottom_missing)} chapters")
    print(f"  Missing/incomplete footer: {len(footer_missing)} chapters")
else:
    print("\n✅ All chapters have consistent navigation and footers!")

print("\n" + "="*80)
