# Challenge: Token Minimization

**ID**: `prompt-dojo-01`
**Difficulty**: ⭐⭐ Apprentice
**Points**: 20 (base)
**Time Limit**: 15 minutes
**Chapter**: 3 (The Art of Prompting)

---

## 🎯 Mission Brief

You're a DevOps engineer at a startup with a tight API budget. Your team is using Claude API heavily, and token costs are adding up fast. The CEO just asked you to reduce costs by 50%.

Your mission: **Generate the same quality output using 75% fewer tokens.**

---

## 📋 Challenge Description

You need to create a Dockerfile for a Python Flask application. Your colleague wrote a prompt that works... but uses **2,000 tokens**!

### Starting Prompt (Inefficient)
See `starter/inefficient-prompt.txt` - it's verbose and poorly structured.

### Your Goal
Rewrite the prompt to generate an equivalent Dockerfile using **≤500 tokens** while maintaining quality.

### Requirements

The generated Dockerfile must include:
- ✅ Python 3.11 base image
- ✅ Non-root user
- ✅ Health check endpoint
- ✅ Multi-stage build (optional but recommended)
- ✅ Proper dependency installation
- ✅ Working entry point

---

## 🎓 What You'll Learn

- Token counting and estimation
- Removing redundant context
- Concise prompt engineering
- Cost optimization strategies

---

## 📊 Scoring Criteria

| Metric | Weight | Target |
|--------|--------|--------|
| **Correctness** | 40% | All requirements met |
| **Token Efficiency** | 40% | ≤500 tokens |
| **Output Quality** | 20% | Production-ready Dockerfile |

### Bonuses
- **Extreme Efficiency**: <300 tokens → +20 pts
- **Speed Bonus**: Complete in <10 min → +10 pts
- **No Hints**: Complete without hints → +10 pts

### Penalties
- **Over Token Limit**: 501-600 tokens → -5 pts, >600 → -10 pts
- **Hint Usage**: -5 pts per hint

---

## 🚀 Getting Started

### 1. Read the inefficient prompt
```bash
cat starter/inefficient-prompt.txt
```

### 2. Understand what makes it wasteful
- Unnecessary verbosity
- Redundant instructions
- Poor structure

### 3. Rewrite it concisely
Create your optimized prompt in: `my-solution/optimized-prompt.txt`

### 4. Test with Claude
```bash
# Copy your prompt and test with Claude (CLI or API)
claude < my-solution/optimized-prompt.txt > my-solution/generated-dockerfile
```

### 5. Count tokens
```bash
python ../lib/count-tokens.py my-solution/optimized-prompt.txt
```

### 6. Grade your solution
```bash
./test-suite/grade.sh my-solution/
```

---

## 💡 Hints Available

Need help? Three progressive hints are available:

```bash
./hints.sh 1  # High-level strategy
./hints.sh 2  # Specific technique
./hints.sh 3  # Near-solution guidance
```

Each hint costs **-5 points**.

---

## ✅ Success Criteria

Your solution passes if:
1. Generated Dockerfile is functional
2. All requirements present
3. Token count ≤500
4. No security vulnerabilities

---

## 🎯 Difficulty Options

### Normal Mode
Follow the requirements as stated.

### Hard Mode 🔥
- Token limit: ≤300
- Time limit: 10 minutes
- No hints allowed
- **Bonus**: +50 points

### Nightmare Mode 💀
- Token limit: ≤200
- Must use CRAFT framework explicitly
- Time limit: 8 minutes
- **Bonus**: +100 points

---

## 📚 Related Content

Review before starting:
- Chapter 2: Understanding Tokens (token counting)
- Chapter 3: The Art of Prompting (CRAFT framework)
- `src/chapter-02/token_examples.py` (token counter tool)

---

## 🏆 Leaderboard

Top solutions will be featured in:
- `solutions/community/top-10.md`
- Guide's GitHub discussions

**Current records**:
- Lowest tokens: *Be the first!*
- Fastest time: *Be the first!*

---

## 📝 After Completion

1. Grade your solution
2. Update progress tracker:
   ```bash
   cd ../../progress-tracker
   python tracker.py complete-challenge prompt-dojo-01 --time <seconds> --tokens <count>
   ```
3. Review reference solution in `solutions/reference.md`
4. Compare with alternatives in `solutions/alternative-*.md`

---

## 🐛 Troubleshooting

**"Token counter not working"**
```bash
pip install tiktoken
```

**"Claude API not available"**
- Use Claude.ai web interface
- Copy/paste your prompt
- Save generated Dockerfile

**"Auto-grader failing"**
```bash
# Check Docker is installed
docker --version

# Test generated Dockerfile manually
cd my-solution
docker build -t test-flask .
```

---

**Ready? Set your timer and begin! ⏱️**

```
╔════════════════════════════════════════════════════╗
║  "The best code is the code you don't write."     ║
║  The best tokens are the tokens you don't use.    ║
╚════════════════════════════════════════════════════╝
```
