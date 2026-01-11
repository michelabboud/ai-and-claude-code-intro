"""
Analyze all chapters: word count, code count, and code-to-text ratio.
"""

from pathlib import Path
import re

chapters_dir = Path("../chapters")
chapters = sorted(chapters_dir.glob("*.md"), key=lambda x: x.name)

print("="*100)
print("Chapter Analysis: Word Count and Code-to-Text Ratio")
print("="*100)

# Data collection
chapter_data = []

for chapter_file in chapters:
    chapter_name = chapter_file.stem

    with open(chapter_file, 'r') as f:
        content = f.read()

    # Extract code blocks
    code_blocks = re.findall(r'```[\s\S]*?```', content)
    code_text = '\n'.join(code_blocks)

    # Remove code blocks from content to get pure text
    text_content = re.sub(r'```[\s\S]*?```', '', content)

    # Count words (split by whitespace)
    total_words = len(content.split())
    code_words = len(code_text.split())
    text_words = len(text_content.split())

    # Calculate ratio
    if text_words > 0:
        code_ratio = (code_words / text_words) * 100
    else:
        code_ratio = 0

    # Count code blocks
    num_code_blocks = len(code_blocks)

    # Character counts
    total_chars = len(content)

    chapter_data.append({
        'name': chapter_name,
        'total_words': total_words,
        'text_words': text_words,
        'code_words': code_words,
        'code_ratio': code_ratio,
        'num_code_blocks': num_code_blocks,
        'total_chars': total_chars
    })

# Sort by chapter number
chapter_data.sort(key=lambda x: x['name'])

# Print table
print(f"\n{'Chapter':<40} {'Words':<10} {'Code %':<10} {'Code Blocks':<12} {'Chars':<12}")
print("-" * 100)

total_words = 0
total_code_words = 0
total_text_words = 0
total_blocks = 0
total_chars = 0

for data in chapter_data:
    # Extract chapter number and title
    match = re.match(r'(\d+)-(.+)', data['name'])
    if match:
        num, title = match.groups()
        title = title.replace('-', ' ').title()
        display_name = f"Ch {num}: {title[:25]}"
    else:
        display_name = data['name'][:40]

    print(f"{display_name:<40} {data['total_words']:<10,} {data['code_ratio']:<9.1f}% {data['num_code_blocks']:<12} {data['total_chars']:<12,}")

    total_words += data['total_words']
    total_code_words += data['code_words']
    total_text_words += data['text_words']
    total_blocks += data['num_code_blocks']
    total_chars += data['total_chars']

# Calculate overall ratio
overall_code_ratio = (total_code_words / total_text_words * 100) if total_text_words > 0 else 0

print("-" * 100)
print(f"{'TOTAL':<40} {total_words:<10,} {overall_code_ratio:<9.1f}% {total_blocks:<12} {total_chars:<12,}")
print("=" * 100)

# Statistics
print(f"\nStatistics:")
print(f"  Total chapters: {len(chapter_data)}")
print(f"  Total words: {total_words:,}")
print(f"  Text words: {total_text_words:,}")
print(f"  Code words: {total_code_words:,}")
print(f"  Overall code-to-text ratio: {overall_code_ratio:.1f}%")
print(f"  Total code blocks: {total_blocks:,}")
print(f"  Total characters: {total_chars:,}")
print(f"  Average words per chapter: {total_words // len(chapter_data):,}")

# Find extremes
max_words_chapter = max(chapter_data, key=lambda x: x['total_words'])
min_words_chapter = min(chapter_data, key=lambda x: x['total_words'])
max_code_chapter = max(chapter_data, key=lambda x: x['code_ratio'])
min_code_chapter = min(chapter_data, key=lambda x: x['code_ratio'])

print(f"\nExtremes:")
print(f"  Longest chapter: {max_words_chapter['name']} ({max_words_chapter['total_words']:,} words)")
print(f"  Shortest chapter: {min_words_chapter['name']} ({min_words_chapter['total_words']:,} words)")
print(f"  Most code: {max_code_chapter['name']} ({max_code_chapter['code_ratio']:.1f}%)")
print(f"  Least code: {min_code_chapter['name']} ({min_code_chapter['code_ratio']:.1f}%)")

print("\n" + "="*100)

# Export table in markdown format
print("\n## Markdown Table for Documentation\n")
print("| Chapter | Words | Code/Text Ratio | Code Blocks | Characters |")
print("|---------|-------|----------------|-------------|------------|")

for data in chapter_data:
    match = re.match(r'(\d+)-(.+)', data['name'])
    if match:
        num, title = match.groups()
        title = title.replace('-', ' ').title()
        display_name = f"{num}. {title}"
    else:
        display_name = data['name']

    print(f"| {display_name} | {data['total_words']:,} | {data['code_ratio']:.1f}% | {data['num_code_blocks']} | {data['total_chars']:,} |")

print(f"| **TOTAL** | **{total_words:,}** | **{overall_code_ratio:.1f}%** | **{total_blocks}** | **{total_chars:,}** |")

print("\n" + "="*100)
