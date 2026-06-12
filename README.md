# AI and Claude Code: A Comprehensive Guide for DevOps Engineers

> **From AI fundamentals to professional Claude Code workflows**

**Author:** Michel Abboud
**Created with:** Claude AI (Anthropic)
**Copyright:** © 2026 Michel Abboud. All rights reserved.

---

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

> **License Notice:** This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License. Free for personal and educational use. Commercial use requires written permission from the author.

> **Claude Code Version:** This guide covers features up to **Claude Code v2.1.4 (January 2026)** including the unified skills/commands system, hot-reload, sub-agent context forking, and latest environment variables. See [CLAUDE.md](./CLAUDE.md#claude-code-version-information) for detailed version information.

---

Welcome to this comprehensive guide designed specifically for DevOps professionals who want to master AI tools and integrate them into their daily workflows. Whether you're new to AI or looking to advance your skills with Claude Code, this guide has you covered.

---

## Who This Guide Is For

This guide is designed for:
- **DevOps Engineers** who want to leverage AI in their workflows
- **SREs** looking to improve incident response with AI
- **Platform Engineers** wanting to automate infrastructure tasks
- **Technical professionals** seeking a hands-on introduction to AI and LLMs

Prerequisites:
- Basic understanding of Linux/Unix command line
- Familiarity with DevOps concepts (CI/CD, containers, IaC)
- No prior AI/ML experience required

---

## What You'll Learn

```
┌────────────────────────────────────────────────────────────────┐
│                    LEARNING PATH                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  FOUNDATIONS (Chapters 1-3)                                    │
│  ├── What is AI and how it works                               │
│  ├── Understanding LLMs and tokens                             │
│  └── The art of writing effective prompts                      │
│                                                                │
│  AI ECOSYSTEM (Chapters 4-5)                                   │
│  ├── AI models landscape and providers                         │
│  └── Introduction to Claude                                    │
│                                                                │
│  CLAUDE CODE (Chapters 6-9)                                    │
│  ├── Fundamentals: Installation and core usage                 │
│  ├── Intermediate: Configuration and workflows                 │
│  ├── Skills & Sub-agents: Advanced capabilities                │
│  └── Hooks & Advanced: Automation and CI/CD                    │
│                                                                │
│  MCP INTEGRATION (Chapters 10-11)                              │
│  ├── MCP Fundamentals: Architecture and usage                  │
│  └── MCP Server Development: Build custom servers              │
│                                                                │
│  WORKFLOW AUTOMATION (Chapters 12-14)                          │
│  ├── AI for DevOps: Practical applications                     │
│  ├── n8n Fundamentals: Workflow automation basics              │
│  └── n8n Advanced: AI integration and production               │
│                                                                │
│  MULTI-AGENT SYSTEMS (Chapters 15-16)                         │
│  ├── Multi-Agent Fundamentals: Agent teams & coordination      │
│  └── Advanced Multi-Agent: Production workflows & monitoring   │
│                                                                │
│  AIOPS & OBSERVABILITY (Chapters 17-18)                       │
│  ├── AIOps Fundamentals: Anomaly detection, predictions       │
│  └── Advanced AIOps: Auto-remediation, self-healing           │
│                                                                │
│  ADVANCED AGENTIC & LEADERSHIP (Chapters 19-21)               │
│  ├── Team Transformation: Leading AI adoption                 │
│  ├── Loop Detection: Ralph Wiggum loops, security, monitoring │
│  └── Resilient Systems: Circuit breakers, self-healing        │
│                                                                │
│  RETRIEVAL-AUGMENTED GENERATION (Chapters 23-25)              │
│  ├── RAG Fundamentals: Embeddings, vector DBs, chunking       │
│  ├── RAG Search Optimization: Hybrid search, re-ranking       │
│  └── Production RAG: Agentic RAG, evaluation, scaling         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Table of Contents

### Part 1: AI Fundamentals

| Chapter | Title | Description |
|---------|-------|-------------|
| [1](./chapters/01-introduction-to-ai.md) | Introduction to AI | What is AI, history, types, and DevOps applications |
| [2](./chapters/02-understanding-llms-and-tokens.md) | Understanding LLMs and Tokens | How LLMs work, tokenization, context windows, costs |
| [3](./chapters/03-the-art-of-prompting.md) | The Art of Prompting | CRAFT framework, techniques, DevOps patterns |

### Part 2: The AI Ecosystem

| Chapter | Title | Description |
|---------|-------|-------------|
| [4](./chapters/04-ai-models-landscape.md) | AI Models Landscape | Providers, models, open source vs proprietary |
| [5](./chapters/05-introduction-to-claude.md) | Introduction to Claude | Anthropic, Claude models, capabilities, access methods |

### Part 3: Claude Code Mastery

| Chapter | Title | Description |
|---------|-------|-------------|
| [6](./chapters/06-claude-code-fundamentals.md) | Claude Code Fundamentals | Installation, basic usage, core workflows |
| [7](./chapters/07-claude-code-intermediate.md) | Claude Code Intermediate | Configuration, custom commands, IDE integration |
| [8](./chapters/08-skills-and-subagents.md) | Skills and Sub-Agents | Custom capabilities, Task Tool, agentic workflows |
| [9](./chapters/09-hooks-and-advanced-features.md) | Hooks and Advanced Features | Event-driven automation, memory, CI/CD integration |

### Part 4: MCP Integration

| Chapter | Title | Description |
|---------|-------|-------------|
| [10](./chapters/10-mcp-fundamentals.md) | MCP Fundamentals | Model Context Protocol architecture, using MCP servers |
| [11](./chapters/11-mcp-server-development.md) | MCP Server Development | Building custom MCP servers (TypeScript) |

### Part 5: Workflow Automation

| Chapter | Title | Description |
|---------|-------|-------------|
| [12](./chapters/12-ai-for-devops.md) | AI for DevOps | Practical applications, tips, real-world workflows |
| [13](./chapters/13-n8n-fundamentals.md) | n8n Fundamentals | Workflow automation, installation, DevOps patterns |
| [14](./chapters/14-n8n-advanced.md) | Advanced n8n Workflows | AI integration, production deployment, complex automations |

### Part 6: Multi-Agent Orchestration & AIOps

| Chapter | Title | Description |
|---------|-------|-------------|
| [15](./chapters/15-multi-agent-fundamentals.md) | Multi-Agent Fundamentals | Agent teams, communication protocols, specialist agents |
| [16](./chapters/16-multi-agent-advanced.md) | Advanced Multi-Agent Workflows | Production workflows, incident response swarms, monitoring |
| [17](./chapters/17-aiops-fundamentals.md) | AIOps Fundamentals | Anomaly detection, predictive alerting, intelligent correlation |
| [18](./chapters/18-aiops-advanced.md) | Advanced AIOps | Auto-remediation, self-healing, chaos engineering, production implementation |

### Part 7: Team Transformation & Advanced Reliability

| Chapter | Title | Description |
|---------|-------|-------------|
| [19](./chapters/19-team-transformation.md) | Team Transformation | Leading organizational change, upskilling teams, measuring success |
| [20](./chapters/20-agent-loop-detection.md) | Agent Loop Detection & Prevention | Ralph Wiggum loops, 6 loop types, detection strategies, DoW protection, production monitoring |

### Part 8: Production-Ready Agentic Systems

| Chapter | Title | Description |
|---------|-------|-------------|
| [21](./chapters/21-resilience-patterns.md) | Resilience Patterns for Agents | Circuit breakers, idempotency, state checkpointing, pattern selection framework (Part 1 of 2) |
| [22](./chapters/22-production-deployment.md) | Production Deployment of Agentic Systems | Exponential backoff with jitter, graceful degradation, self-healing, staged rollouts, ROI measurement (Part 2 of 2) |

### Part 9: Retrieval-Augmented Generation (RAG)

| Chapter | Title | Description |
|---------|-------|-------------|
| [23](./chapters/23-rag-fundamentals.md) | RAG Fundamentals | Vector embeddings, vector databases, chunking strategies, building RAG systems, query transformation, real-world DevOps use cases |
| [24](./chapters/24-rag-search-optimization.md) | RAG Search & Retrieval Optimization | Hybrid search (BM25 + vector), cross-encoder re-ranking, multi-query fusion, pattern selection (Part 1 of 2) |
| [25](./chapters/25-production-rag-systems.md) | Production RAG Systems | Agentic RAG, RAGAS evaluation, production caching, fine-tuning embeddings, smart routing, scaling patterns (Part 2 of 2) |

### Appendices

| Appendix | Title | Description |
|----------|-------|-------------|
| [A](./appendices/appendix-a-platform-blueprint.md) | AI DevOps Platform Blueprint | Complete reference architecture, tech stacks, roadmap, cost modeling |

---

## 🎯 Learning Paths

Choose the learning path that fits your needs and schedule:

### 🚀 Express Path (4-6 hours)
**For busy DevOps engineers who need practical skills fast**

Read only the essential sections and TL;DRs:

**Phase 1: AI Basics (45 min)**
- [Chapter 1](./chapters/01-introduction-to-ai.md) - Full chapter (9 min)
- [Chapter 2](./chapters/02-understanding-llms-and-tokens.md) - **TL;DR only** + Section2.3 Tokens, Section2.5 Costs (8 min)
- [Chapter 3](./chapters/03-the-art-of-prompting.md) - **TL;DR only** + Section3.2 CRAFT Framework, Section3.4 DevOps Patterns (12 min)

**Phase 2: Getting Started with Claude (90 min)**
- [Chapter 5](./chapters/05-introduction-to-claude.md) - Section5.1, Section5.2, Section5.4 (skip detailed API examples) (8 min)
- [Chapter 6](./chapters/06-claude-code-fundamentals.md) - **Full chapter** (13 min) → Do exercises!
- [Quick Reference](./references/claude-code-quick-reference.md) - Skim for commands (10 min)

**Phase 3: Professional Usage (90 min)**
- [Chapter 7](./chapters/07-claude-code-intermediate.md) - **TL;DR** + Section7.2 Custom Commands, Section7.5 Workflows (10 min)
- [Chapter 8](./chapters/08-skills-and-subagents.md) - **TL;DR** + Section8.2 Skills, Section8.3 Sub-Agents (10 min)
- [Chapter 9](./chapters/09-hooks-and-advanced-features.md) - **TL;DR** + Section9.1 Hooks (8 min)
- [Hooks Cookbook](./references/hooks-cookbook.md) - Pick 3 hooks to implement (10 min)

**Phase 4: Real-World Application (90 min)**
- [Chapter 12](./chapters/12-ai-for-devops.md) - **Full chapter** (14 min) → Try examples!
- **Hands-on**: Apply to your actual work (60 min)

**Total: ~4-6 hours** (includes hands-on practice)

---

### 📖 Complete Path (15-20 hours)
**For comprehensive understanding and mastery**

Read all 23 chapters in order, complete all exercises, and build your own:
- Custom commands for your team
- MCP servers for your tools
- Automated workflows with hooks
- Multi-agent orchestration systems
- Production AIOps platform with auto-remediation
- Team transformation strategies

**Perfect for**: Team leads, platform engineers, those building AI-powered DevOps platforms

---

### 🎯 Practical Path (8-12 hours)
**Skip theory, focus on hands-on**

1. Skim Chapters 1-2 for basics
2. Read Chapter 3 (CRAFT Framework) fully
3. **Do all exercises** in Chapters 6-9
4. Read Chapters 12-14, implement 3 real-world workflows
5. Explore Chapters 17-18 for advanced AIOps patterns
6. Review Appendix A for production platform architecture
7. Build your own commands, hooks, workflows, and auto-remediation systems

**Perfect for**: Learn-by-doing DevOps engineers, SREs building AI-powered platforms

---

### 🎮 Gamified Path (Variable)
**Make learning fun with DevOps Quest**

Complete challenges, earn achievements, track your progress:
```bash
cd gamification/progress-tracker
python tracker.py init
python tracker.py
```

See [gamification/README.md](./gamification/README.md) for the full quest system!

---

## Quick Start

### 1. Read the Fundamentals
Start with Chapters 1-3 to build a solid understanding of AI concepts.

### 2. Set Up Claude Code
```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Authenticate
claude login

# Start using
cd your-project
claude
```

### 3. Try Your First DevOps Task
```bash
> Create a Dockerfile for a Python Flask application with:
  - Multi-stage build
  - Non-root user
  - Health check
```

### 4. Explore Advanced Features
- Configure custom commands (Chapter 7)
- Set up MCP servers for your tools (Chapters 10-11)
- Build automation workflows (Chapters 12-14)
- Implement multi-agent orchestration (Chapters 15-16)
- Deploy production AIOps with auto-remediation (Chapters 17-18)
- Lead team transformation (Chapter 19)

---

## Repository Structure

```
ai-and-claude-code-intro/
├── README.md                    # This file
├── LICENSE                      # CC BY-NC 4.0 License
├── CONTRIBUTING.md              # Contributor guidelines
├── chapters/                    # Guide content (25 chapters)
│   ├── 01-introduction-to-ai.md
│   ├── 02-understanding-llms-and-tokens.md
│   ├── 03-the-art-of-prompting.md
│   ├── 04-ai-models-landscape.md
│   ├── 05-introduction-to-claude.md
│   ├── 06-claude-code-fundamentals.md
│   ├── 07-claude-code-intermediate.md
│   ├── 08-skills-and-subagents.md
│   ├── 09-hooks-and-advanced-features.md
│   ├── 10-mcp-fundamentals.md
│   ├── 11-mcp-server-development.md
│   ├── 12-ai-for-devops.md
│   ├── 13-n8n-fundamentals.md
│   ├── 14-n8n-advanced.md
│   ├── 15-multi-agent-fundamentals.md
│   ├── 16-multi-agent-advanced.md
│   ├── 17-aiops-fundamentals.md
│   ├── 18-aiops-advanced.md
│   ├── 19-team-transformation.md
│   ├── 20-agent-loop-detection.md
│   ├── 21-resilience-patterns.md
│   ├── 22-production-deployment.md
│   ├── 23-rag-fundamentals.md
│   ├── 24-rag-search-optimization.md
│   └── 25-production-rag-systems.md
├── appendices/                  # Reference architectures and blueprints
│   └── appendix-a-platform-blueprint.md
├── presentations/               # Slides for each chapter
│   ├── *.md                     # Marp source files
│   └── pptx/                    # Generated PowerPoint files
├── references/                  # Quick reference guides
│   ├── README.md
│   ├── claude-code-quick-reference.md
│   └── hooks-cookbook.md
├── src/                         # Code examples by chapter (selective coverage)
│   ├── chapter-01/              # Traditional vs ML, AIOps patterns
│   ├── chapter-02/              # Token counting, cost estimation
│   ├── chapter-03/              # CRAFT framework, prompt templates
│   ├── chapter-04/              # Model selection guide
│   ├── chapter-05/              # Claude API examples
│   ├── chapter-06/              # Claude Code config, commands
│   ├── chapter-07/              # Custom commands, GitHub Actions
│   ├── chapter-08/              # Skills, sub-agents configurations
│   ├── chapter-09/              # Hooks, memory, CI/CD examples
│   ├── chapter-10/              # MCP usage examples, shell aliases, incident response
│   ├── chapter-15/              # Multi-agent fundamentals (coordination, agents)
│   ├── chapter-16/              # Advanced multi-agent (swarms, monitoring)
│   ├── chapter-17/              # AIOps fundamentals (monitoring integration)
│   ├── chapter-18/              # Advanced AIOps (auto-remediation, self-healing)
│   ├── chapter-20/              # Agent loop detection examples
│   ├── chapter-21/              # Resilience patterns examples
│   └── chapter-24/              # RAG search optimization examples
├── gamification/                # DevOps Quest learning system
│   ├── progress-tracker/        # Track progress, achievements, streaks
│   ├── challenges/              # Hands-on coding challenges
│   ├── story-mode/              # Narrative-driven learning
│   ├── sandbox/                 # Docker-based incident scenarios
│   └── README.md
└── assets/                      # Images and diagrams
```

---

## Key Concepts Quick Reference

### Token Estimation
```
~4 characters = 1 token
~0.75 words = 1 token
100 lines of code ≈ 1,000 tokens
```

### Claude Models
| Model | Best For | Speed | Cost (per MTok) |
|-------|----------|-------|-----------------|
| Claude Sonnet 4.5 | Most tasks | Fast | $3-6 / $15-22.50 |
| Claude Opus 4.5 | Complex reasoning | Slower | $5 / $25 |
| Claude Haiku 4.5 | Simple tasks | Fastest | $1 / $5 |

### CRAFT Prompting Framework
- **C**ontext - Environment, versions, constraints
- **R**ole - Expert persona for the AI
- **A**ction - Specific task to perform
- **F**ormat - Desired output structure
- **T**arget - Success criteria

---

## Hands-On Exercises

Each chapter includes practical exercises:
- **Chapter 1**: Identify AI opportunities in your workflow
- **Chapter 2**: Token counting and cost estimation
- **Chapter 3**: Prompt improvement practice
- **Chapter 4**: Model comparison testing
- **Chapter 5**: Claude API exploration
- **Chapter 6**: First Claude Code session
- **Chapter 7**: Custom commands creation
- **Chapter 8**: Multi-agent workflows
- **Chapter 9**: Building an MCP server
- **Chapter 10**: Full DevOps automation

---

## Additional Resources

### Official Documentation
- [Claude Documentation](https://docs.anthropic.com/)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [MCP Specification](https://modelcontextprotocol.io/)

### Community
- [Anthropic Discord](https://discord.gg/anthropic)
- [GitHub Discussions](https://github.com/anthropics/claude-code/discussions)

### Related Tools
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Claude Code VS Code Extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

## Community Tools & Utilities

### 🛠️ Claude Code Helper - Complete Toolkit

**Repository**: [michelabboud/claude-code-helper](https://github.com/michelabboud/claude-code-helper)
**Author**: Michel Abboud (with AI assistance from Claude Code)
**License**: MIT
**Version**: 1.1.0 - 100% Complete

A comprehensive, production-ready toolkit that complements this guide with hands-on examples and configurations. Perfect for applying the concepts learned in Chapters 6-10.

#### What's Included:
 - 📚 **Guides**: Zero-to-hero learning paths and advanced agent patterns
 - 🌐 **5 MCP Servers**: 30+ specialized tools for code quality, testing, and design systems
 - 🤖 **33 Sub-Agents**: Production-ready domain experts covering all major tech stacks
 - Frontend: React/Next.js, Vue/Nuxt, Angular
 - Backend: Node.js, Python, Go, Rust, PHP, Laravel, Ruby on Rails
 - Mobile: iOS (Swift), Android (Kotlin)
 - Cloud: AWS, Azure, GCP architects
 - Specialized: IoT/Embedded, Game Design, ML/AI, Redis, WordPress
 - ✨ **13 Skills**: Comprehensive workflow and testing patterns
 - 8 workflow/architecture skills (code review, refactoring, API design, TDD, CI/CD)
 - 5 advanced testing skills (visual regression, contract, mutation, BDD, E2E)
 - 📐 **Templates**: Starter templates for skills, agents, commands, and plugins
 - ⚙️ **Config Bundle**: Production-ready global configuration with model transparency
 - 🎯 **100% Complete**: 79/79 items delivered - comprehensive coverage across all major stacks

#### Quick Start:

```bash
git clone https://github.com/michelabboud/claude-code-helper.git
cd claude-code-helper

# Install everything
cd config-bundle && ./scripts/install-all.sh
```

#### How It Complements This Guide:

```
Theory (This Guide)           Practice (Claude Code Helper)
─────────────────────────────────────────────────────────────
📖 Learn what Claude Code is → 🛠️ Get 33 production-ready agents
📖 Understand how it works   → 🛠️ Use professional configurations
📖 Study AI fundamentals     → 🛠️ Apply with real-world examples
📖 Explore MCP architecture  → 🛠️ Install 5 working MCP servers
📖 Master prompt engineering → 🛠️ See CRAFT framework in action
```

#### Best For:

- Hands-on practice after completing theoretical chapters
- Production-ready configurations for professional DevOps workflows
- Learning multi-agent coordination patterns (supports Chapter 8)
- Understanding MCP server implementation (supports Chapter 9)
- Real-world integration examples for DevOps scenarios
- Complete testing strategies from unit tests to E2E

#### New in v1.1.0:

- 🧪 Advanced Testing Suite: 5 comprehensive testing skills
  - Visual regression testing (Percy, Chromatic, BackstopJS)
  - Contract testing with Pact (consumer-driven contracts)
  - Mutation testing (Stryker, PITest, Mutmut)
  - BDD frameworks (Cucumber, Behave, SpecFlow)
  - Advanced E2E testing (auth flows, API mocking, WebSockets)
- 🔧 Claude Code v2.1.3+ compatibility with latest features
- 📊 100% completion with comprehensive coverage

#### Learning Path:

1. 📚 Read this guide      → Understand theory and concepts
2. 🛠️ Use Claude Code Helper → Apply with production examples
3. 🚀 Build real projects   → Master Claude Code workflows

---

## 🎮 New in v1.0.0: DevOps Quest Gamification System

Transform your learning experience with interactive challenges, progress tracking, and achievements!

### ✨ What's Included

#### 📊 Progress Tracker
Track your journey with a beautiful ASCII dashboard:
```bash
cd gamification/progress-tracker
pip install -r requirements.txt
python tracker.py init
python tracker.py  # View your dashboard
```

**Features**:
- 15 unlockable achievement badges 🎖️
- Learning streak tracking 🔥
- Chapter and challenge completion tracking
- Beautiful terminal UI with progress bars

#### 🏆 Challenges (4 Available)
Hands-on coding challenges with auto-grading:

1. **Prompt Dojo** (⭐⭐) - Reduce tokens by 75%
2. **Token Detective** (⭐⭐⭐) - Audit 5 production prompts
3. **CRAFT Master** (⭐⭐⭐) - Master prompt engineering framework
4. **Claude Code Basics** (⭐) - First hands-on session

Each challenge includes:
- Auto-grader with instant feedback
- Progressive 3-hint system
- Multiple difficulty modes
- Token optimization focus

#### 📖 Story Mode
Experience learning through immersive narratives:

**Chapter 6: "The Midnight Deployment Crisis"** 🚨
- Production is down at 2:47 AM
- You have 30 minutes to fix it
- Multiple difficulty levels
- Real-time events and pressure

```bash
cd gamification/story-mode
./play.sh
```

#### 🛠️ Sandbox Labs
Docker-based incident scenarios:

**Incident 01: CrashLoopBackOff** - Debug a broken Kubernetes deployment
```bash
cd gamification/sandbox/incident-01-crashloop
docker-compose up -d
# Fix the bug, then:
./check-solution.sh
```

### 🎯 Three Learning Paths

Choose your style:
- 🚀 **Speed Run** (20 hours) - Core challenges, get it working
- 🎓 **Knowledge Master** (40-60 hours) - Deep understanding
- ⚡ **Hybrid** (30-40 hours) - Balanced approach (recommended)

### 📈 Track Your Progress

Your dashboard shows:
- Chapters completed (10 total)
- Challenges completed (30 planned)
- Sandbox incidents resolved (10 planned)
- Achievement badges earned
- Current learning streak
- Total points and score

### 🚀 Quick Start

```bash
# 1. Initialize your quest
cd gamification/progress-tracker
pip install -r requirements.txt tiktoken
python tracker.py init

# 2. Start first challenge
cd ../challenges/01-prompt-dojo
./start.sh

# 3. Experience story mode
cd ../../story-mode
./play.sh
```

**See**: [Gamification README](./gamification/README.md) for full details

---

## License

This work is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

### You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

### Under the following terms:
- **Attribution** — You must give appropriate credit to Michel Abboud, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes without written permission.

### Commercial Use
For commercial licensing inquiries, please contact the author.

See the [LICENSE](./LICENSE) file for full details.

---

## About the Author

**Michel Abboud** - DevOps enthusiast and technical educator passionate about helping professionals leverage AI effectively in their workflows.

This guide was created with the assistance of Claude AI, demonstrating the very capabilities it teaches.

---

## Contributing

Contributions are welcome! We reward contributors with commercial use rights.

| Tier | Requirements | Rights |
|------|--------------|--------|
| **Contributor** | 1+ merged PR | Attribution |
| **Core Contributor** | 3+ significant PRs or new chapter | Commercial use rights |
| **Co-Author** | Major contributions | Full commercial rights |

See **[CONTRIBUTING.md](./CONTRIBUTING.md)** for full details on:
- How to contribute
- Style guidelines
- Contributor license agreement
- Commercial rights details

---

## Acknowledgments

- Anthropic for creating Claude and Claude Code
- The DevOps community for inspiration and feedback
- All readers and contributors

---

**Happy Learning! May your deployments be smooth and your incidents be few.**

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│     Your DevOps Expertise  +  AI Tools  =  Superpowers         │
│                                                                │
│                    © 2026 Michel Abboud                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```
