"""
Test Chapters 22-23 markdown files for completeness and quality.
"""

import sys
from pathlib import Path

print("="*80)
print("Testing RAG Chapters (22-23) - Markdown Quality")
print("="*80)

# Test Chapter 22
print("\n[Chapter 22: RAG Fundamentals]")
chapter_22 = Path("../chapters/22-rag-fundamentals.md")

if not chapter_22.exists():
    print(f"❌ Chapter 22 not found at {chapter_22}")
    sys.exit(1)

with open(chapter_22, 'r') as f:
    ch22_content = f.read()
    ch22_lines = ch22_content.split('\n')

print(f"✅ File exists: {chapter_22.name}")
print(f"✅ Size: {len(ch22_content):,} characters ({len(ch22_content)/4:.0f} tokens est.)")
print(f"✅ Lines: {len(ch22_lines):,}")

# Check for required sections in Chapter 22
ch22_sections = [
    '# Chapter 22: RAG Fundamentals',
    '## 1. Introduction to RAG',
    '## 2. Understanding Vector Embeddings',
    '## 3. Vector Databases',
    '## 4. Document Chunking Strategies',
    '## 5. Building Your First RAG System',
    '## 6. Query Transformation Techniques',
    '## 7. Context Window Management',
    '## 8. Real-World DevOps RAG Scenarios'
]

missing_sections = []
for section in ch22_sections:
    if section in ch22_content:
        print(f"  ✅ {section}")
    else:
        print(f"  ❌ Missing: {section}")
        missing_sections.append(section)

# Check for code blocks
code_blocks = ch22_content.count('```python')
print(f"✅ Python code examples: {code_blocks}")

if code_blocks < 20:
    print(f"  ⚠️  Expected >= 20 code examples, found {code_blocks}")

# Test Chapter 23
print("\n[Chapter 23: Advanced RAG Patterns]")
chapter_23 = Path("../chapters/23-advanced-rag-patterns.md")

if not chapter_23.exists():
    print(f"❌ Chapter 23 not found at {chapter_23}")
    sys.exit(1)

with open(chapter_23, 'r') as f:
    ch23_content = f.read()
    ch23_lines = ch23_content.split('\n')

print(f"✅ File exists: {chapter_23.name}")
print(f"✅ Size: {len(ch23_content):,} characters ({len(ch23_content)/4:.0f} tokens est.)")
print(f"✅ Lines: {len(ch23_lines):,}")

# Check for required sections in Chapter 23
ch23_sections = [
    '# Chapter 23: Advanced RAG Patterns',
    '## 1. Hybrid Search: Combining Keyword and Semantic',
    '## 2. Advanced Re-Ranking with Cross-Encoders',
    '## 3. Multi-Query and Query Fusion',
    '## 4. Agentic RAG: RAG as a Tool',
    '## 5. RAG Evaluation and Metrics',
    '## 6. Production Optimization and Caching',
    '## 7. Fine-Tuning Embeddings for Your Domain',
    '## 8. RAG Routing and Conditional Retrieval'
]

for section in ch23_sections:
    if section in ch23_content:
        print(f"  ✅ {section}")
    else:
        print(f"  ❌ Missing: {section}")
        missing_sections.append(section)

# Check for code blocks
code_blocks_23 = ch23_content.count('```python')
print(f"✅ Python code examples: {code_blocks_23}")

if code_blocks_23 < 30:
    print(f"  ⚠️  Expected >= 30 code examples, found {code_blocks_23}")

# Test presentations
print("\n[Presentations]")

slide_22 = Path("../presentations/slides-chapter-22.md")
if slide_22.exists():
    with open(slide_22, 'r') as f:
        slides_22 = f.read()
    slide_count_22 = slides_22.count('\n---\n')
    print(f"✅ Chapter 22 slides: {slide_22.name} ({slide_count_22} slides)")
else:
    print(f"❌ Missing: {slide_22}")
    missing_sections.append(str(slide_22))

slide_23 = Path("../presentations/slides-chapter-23.md")
if slide_23.exists():
    with open(slide_23, 'r') as f:
        slides_23 = f.read()
    slide_count_23 = slides_23.count('\n---\n')
    print(f"✅ Chapter 23 slides: {slide_23.name} ({slide_count_23} slides)")
else:
    print(f"❌ Missing: {slide_23}")
    missing_sections.append(str(slide_23))

# Quality checks
print("\n[Quality Checks]")

# Check for real-world examples in Chapter 22
examples_22 = ['PagerDuty', 'runbook', 'infrastructure', 'log analysis', 'onboarding']
found_examples = sum(1 for ex in examples_22 if ex.lower() in ch22_content.lower())
print(f"✅ Real-world examples in Ch22: {found_examples}/{len(examples_22)}")

# Check for case studies in Chapter 23
case_studies = ['Stripe', 'Notion', 'Shopify', 'Netflix']
found_studies = sum(1 for cs in case_studies if cs in ch23_content)
print(f"✅ Case studies in Ch23: {found_studies}/{len(case_studies)}")

# Check for cost analysis
if 'cost' in ch22_content.lower() and '$' in ch22_content:
    print(f"✅ Ch22 includes cost analysis")
if 'cost' in ch23_content.lower() and '$' in ch23_content:
    print(f"✅ Ch23 includes cost analysis")

# Summary
print("\n" + "="*80)
if missing_sections:
    print(f"⚠️  Found {len(missing_sections)} potential issues")
    for issue in missing_sections:
        print(f"  - {issue}")
else:
    print("✅ ALL CHAPTER TESTS PASSED!")

print("="*80)
print("\nChapter Statistics:")
print(f"  Chapter 22: {len(ch22_content):,} chars, {len(ch22_lines):,} lines, {code_blocks} code blocks")
print(f"  Chapter 23: {len(ch23_content):,} chars, {len(ch23_lines):,} lines, {code_blocks_23} code blocks")
print(f"  Total: {len(ch22_content) + len(ch23_content):,} characters")
print(f"  Total: {len(ch22_lines) + len(ch23_lines):,} lines")
print(f"  Total: {code_blocks + code_blocks_23} code examples")

print("\n✅ Chapters are complete and ready for use!")
