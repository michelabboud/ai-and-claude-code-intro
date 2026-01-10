# Challenge: Token Detective

**ID**: `token-detective-01`
**Difficulty**: ⭐⭐⭐ Journeyman
**Points**: 30
**Time Limit**: 20 minutes
**Chapter**: 2 (Understanding LLMs and Tokens)

---

## 🎯 Mission Brief

Your company's monthly Claude API bill just hit $10,000! The CFO is demanding answers. You've been tasked with auditing all prompts used by your team and identifying where tokens are being wasted.

**Your mission**: Analyze 5 real-world prompts and reduce total token usage by 60% without losing functionality.

---

## 📋 Challenge Description

You've been given 5 prompts currently used in production:
1. **Infrastructure prompt** - Generates Terraform modules
2. **Incident response** - Analyzes logs during outages
3. **Code review** - Reviews pull requests
4. **Documentation** - Generates API docs
5. **Deployment** - Creates K8s manifests

**Current total**: ~8,500 tokens/day
**Target**: ≤3,400 tokens/day (60% reduction)

---

## 🚀 Getting Started

```bash
./start.sh

# Analyze the prompts in starter/
ls starter/
# prompt-1-infrastructure.txt  (2100 tokens)
# prompt-2-incident.txt        (1800 tokens)
# prompt-3-codereview.txt      (1700 tokens)
# prompt-4-documentation.txt   (1600 tokens)
# prompt-5-deployment.txt      (1300 tokens)

# Create optimized versions in my-solution/
```

---

## ✅ Success Criteria

- Total tokens ≤3,400 (60% reduction)
- All 5 prompts maintain functionality
- Output quality equivalent or better
- No security/best practice loss

**Bonus**: Achieve 70% reduction → +20 pts

---

## 💡 Learning Objectives

- Token auditing in real codebases
- Identifying patterns of waste
- Systematic optimization approach
- Cost-benefit analysis

---

Ready to save your company thousands? ⏱️
