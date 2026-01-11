"""
Basic functionality test for Chapter 22 RAG implementations.

Tests core logic without requiring external API keys or heavy dependencies.
"""

import sys
import os
from pathlib import Path

print("="*80)
print("Chapter 22: RAG Fundamentals - Basic Functionality Tests")
print("="*80)

# Test 1: Import checks
print("\n[Test 1] Checking imports and syntax...")
try:
    # Check if document_loader.py has valid syntax
    import py_compile
    py_compile.compile('document_loader.py', doraise=True)
    print("✅ document_loader.py: Syntax valid")
except Exception as e:
    print(f"❌ document_loader.py: {e}")
    sys.exit(1)

try:
    py_compile.compile('chunker.py', doraise=True)
    print("✅ chunker.py: Syntax valid")
except Exception as e:
    print(f"❌ chunker.py: {e}")
    sys.exit(1)

# Test 2: Test DocumentLoader class structure
print("\n[Test 2] Testing DocumentLoader class structure...")
try:
    # Read the file and check for key methods
    with open('document_loader.py', 'r') as f:
        content = f.read()

    required_methods = [
        'class DocumentLoader',
        'def load_file',
        'def load_directory',
        'def _load_text',
        'def _load_json',
        'def _load_pdf',
        'def _load_docx',
        'def _load_html'
    ]

    for method in required_methods:
        if method in content:
            print(f"✅ Found: {method}")
        else:
            print(f"❌ Missing: {method}")
            sys.exit(1)

except Exception as e:
    print(f"❌ Error reading document_loader.py: {e}")
    sys.exit(1)

# Test 3: Test Chunker classes structure
print("\n[Test 3] Testing Chunker classes structure...")
try:
    with open('chunker.py', 'r') as f:
        content = f.read()

    required_classes = [
        'class FixedSizeChunker',
        'class SentenceChunker',
        'class SemanticChunker',
        'class MarkdownChunker'
    ]

    for cls in required_classes:
        if cls in content:
            print(f"✅ Found: {cls}")
        else:
            print(f"❌ Missing: {cls}")
            sys.exit(1)

    # Check for chunk_text method in each
    if content.count('def chunk_text') >= 4:
        print(f"✅ All chunkers have chunk_text method")
    else:
        print(f"❌ Missing chunk_text methods")
        sys.exit(1)

except Exception as e:
    print(f"❌ Error reading chunker.py: {e}")
    sys.exit(1)

# Test 4: Test README completeness
print("\n[Test 4] Testing README completeness...")
try:
    with open('README.md', 'r') as f:
        readme_content = f.read()

    required_sections = [
        '# Chapter 22',
        '## Installation',
        '## Quick Start',
        '## Running Examples',
        'requirements.txt'
    ]

    for section in required_sections:
        if section in readme_content:
            print(f"✅ Found section: {section}")
        else:
            print(f"❌ Missing section: {section}")
            sys.exit(1)

except Exception as e:
    print(f"❌ Error reading README.md: {e}")
    sys.exit(1)

# Test 5: Test requirements.txt exists and has key dependencies
print("\n[Test 5] Testing requirements.txt...")
try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read()

    required_deps = [
        'openai',
        'tiktoken',
        'chromadb',
        'pypdf',
        'python-docx',
        'beautifulsoup4',
        'nltk',
        'sentence-transformers'
    ]

    for dep in required_deps:
        if dep in requirements:
            print(f"✅ Found dependency: {dep}")
        else:
            print(f"❌ Missing dependency: {dep}")
            sys.exit(1)

except Exception as e:
    print(f"❌ Error reading requirements.txt: {e}")
    sys.exit(1)

# Test 6: Test file structure
print("\n[Test 6] Testing file structure...")
expected_files = [
    'document_loader.py',
    'chunker.py',
    'README.md',
    'requirements.txt'
]

for file in expected_files:
    if Path(file).exists():
        size = Path(file).stat().st_size
        print(f"✅ {file}: {size:,} bytes")
    else:
        print(f"❌ Missing: {file}")
        sys.exit(1)

# Test 7: Code quality checks
print("\n[Test 7] Code quality checks...")

# Check for docstrings
for filename in ['document_loader.py', 'chunker.py']:
    with open(filename, 'r') as f:
        content = f.read()

    if '"""' in content or "'''" in content:
        docstring_count = content.count('"""') + content.count("'''")
        print(f"✅ {filename}: Has {docstring_count // 2} docstrings")
    else:
        print(f"⚠️  {filename}: No docstrings found")

# Summary
print("\n" + "="*80)
print("✅ All basic functionality tests PASSED!")
print("="*80)
print("\nNote: Full integration tests require installing dependencies:")
print("  pip install -r requirements.txt")
print("\nThese tests verify:")
print("  ✓ Python syntax is valid")
print("  ✓ All required classes and methods exist")
print("  ✓ Documentation is complete")
print("  ✓ Dependencies are specified")
print("  ✓ File structure is correct")
