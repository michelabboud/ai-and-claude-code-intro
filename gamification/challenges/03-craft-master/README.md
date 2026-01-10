# Challenge: CRAFT Framework Master

**ID**: `craft-master-01`
**Difficulty**: ⭐⭐⭐ Journeyman
**Points**: 40
**Time Limit**: 20 minutes
**Chapter**: 3 (The Art of Prompting)

---

## 🎯 Mission Brief

Your team lead just rejected your PR because "the AI-generated code doesn't follow our standards." The problem? Your prompts don't provide enough context or structure.

**Your mission**: Use the CRAFT framework to generate perfect, production-ready code on the FIRST try.

---

## 📋 Challenge Description

You need to generate a Python FastAPI endpoint that:
- Handles user authentication with JWT
- Includes rate limiting
- Has proper error handling
- Follows your company's coding standards
- Includes logging and metrics

Your first attempt (without CRAFT) generated code with 12 issues.

**Using CRAFT, get it to 0 issues.**

---

## 🎨 CRAFT Framework

**C**ontext - Environment, constraints, dependencies
**R**ole - What expert persona should AI adopt
**A**ction - Specific task to perform
**F**ormat - Desired output structure
**T**arget - Success criteria

---

## 🚀 Getting Started

```bash
./start.sh

# See the bad prompt in starter/bad-prompt.txt
# See company standards in starter/company-standards.md

# Write your CRAFT prompt in my-solution/craft-prompt.txt
# Generate code and save to my-solution/generated-code.py

# Grade it
./test-suite/grade.sh
```

---

## ✅ Success Criteria

- Uses all 5 CRAFT elements explicitly
- Generated code passes all checks:
  - Security scan (0 vulnerabilities)
  - Linting (company config)
  - Type checking (mypy strict)
  - Unit tests pass
  - Meets company standards

**Perfect score**: 0 issues + clear CRAFT structure

---

## 💡 Learning Objectives

- CRAFT framework mastery
- Structured prompting
- Context engineering
- First-try success rate

---

Get it right the first time! 🎯

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0
