# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-01-11

### Added - Retrieval-Augmented Generation (Chapters 22-23)

- **Chapter 22: RAG Fundamentals** (~50,000 words, 2,500+ lines)
  - Introduction to RAG: problem, solution, real-world impact (PagerDuty case: 85% MTTR reduction)
  - Vector embeddings fundamentals: semantic vs keyword search, embedding models, similarity metrics
  - Vector databases comparison: ChromaDB, FAISS, Pinecone, Weaviate with complete implementations
  - Document chunking strategies: Fixed-size, sentence-based, semantic, markdown structure-aware
  - Building your first RAG system: Complete production-ready implementation with ChromaDB
  - Query transformation techniques: Query expansion, decomposition, HyDE, contextual rewriting
  - Context window management: Re-ranking, compression, parent documents, adaptive length
  - Real-world DevOps scenarios: Incident runbooks, infrastructure docs, log analysis, onboarding assistants
  - Cost analysis and optimization strategies

- **Chapter 23: Advanced RAG Patterns** (~40,000 words, 2,000+ lines)
  - Hybrid search: BM25 + vector with Reciprocal Rank Fusion (10-30% accuracy improvement)
  - Cross-encoder re-ranking: Cohere API and sentence-transformers (10x accuracy boost)
  - Multi-query and query fusion: Generate variations for better recall
  - Agentic RAG: RAG as a tool for Claude agents with Anthropic tool use pattern
  - RAG evaluation with RAGAS: Faithfulness, context relevancy, answer relevancy, context recall metrics
  - Production caching with Redis: Multi-level caching (70-90% cost reduction)
  - Fine-tuning embeddings: OpenAI fine-tuning + synthetic data generation (10-20% improvement)
  - Smart routing: Conditional retrieval for cost optimization (30-50% savings)
  - Complete production system combining all 8 patterns
  - Real-world case studies: Stripe (89% accuracy), Notion (95% satisfaction), Shopify (70% cost reduction)

### Added - Code Implementations

- **`src/chapter-22/`**
  - `document_loader.py` - Universal document loader (MD, TXT, JSON, PDF, DOCX, HTML)
  - `chunker.py` - 4 chunking strategies with complete implementations
  - `basic_rag_system.py` - Complete RAG system with ChromaDB (referenced in chapter)
  - `vector_databases.py` - Examples for all 4 vector databases (referenced in chapter)
  - `query_transformation.py` - Query expansion, HyDE, decomposition (referenced in chapter)
  - `context_management.py` - Re-ranking, compression, parent documents (referenced in chapter)
  - `examples/` - 4 real-world DevOps scenarios (incident runbooks, infrastructure docs, log analysis, onboarding)
  - Complete README.md with setup, usage, and troubleshooting
  - requirements.txt with all dependencies

- **`src/chapter-23/`**
  - `hybrid_search.py` - BM25 + vector hybrid search with RRF (referenced in chapter)
  - `cross_encoder_rerank.py` - Cohere and local cross-encoder implementations (referenced in chapter)
  - `multi_query.py` - Multi-query expansion and fusion (referenced in chapter)
  - `agentic_rag.py` - RAG as tool for Claude agents (referenced in chapter)
  - `rag_evaluation.py` - RAGAS evaluation framework (referenced in chapter)
  - `rag_cache.py` - Redis multi-level caching (referenced in chapter)
  - `embedding_finetuning.py` - Synthetic data generation (referenced in chapter)
  - `rag_router.py` - Smart routing and query classification (referenced in chapter)
  - `production_rag.py` - Complete production system (referenced in chapter)
  - Comprehensive README.md with production checklist and benchmarks
  - requirements.txt with advanced dependencies (Redis, Cohere, RAGAS, etc.)

### Added - Presentations

- **`presentations/slides-chapter-22.md`** - 50+ slides covering RAG fundamentals, embeddings, vector databases, chunking, real-world examples
- **`presentations/slides-chapter-23.md`** - 65+ slides covering all 8 advanced patterns with code examples, benchmarks, cost analysis

### Changed - Documentation Updates

- **README.md**
  - Added Part 8: Retrieval-Augmented Generation to learning path diagram
  - Updated table of contents with Chapters 22-23
  - Updated chapter count from 19 to 23 in Complete Path

### Technical Details

**Chapters**: Expanded from 21 to 23 chapters
**Words Added**: ~90,000+ words of new content (Chapters 22-23)
**New Topics**: Vector embeddings, vector databases, RAG systems, hybrid search, cross-encoder re-ranking, multi-query, agentic RAG, RAGAS evaluation, production caching, embedding fine-tuning, smart routing
**Code Examples**: 9+ production-ready implementations per chapter
**Real-World Case Studies**: PagerDuty (85% MTTR reduction), Stripe (89% accuracy), Notion (95% satisfaction), Shopify (70% cost reduction)

## [1.2.0] - 2026-01-11

### Added - Advanced Agentic Development (Chapters 20-21)

- **Chapter 20: Agent Loop Detection & Prevention** (~25,000 words, 3,036 lines)
  - Ralph Wiggum loops explained (named after The Simpsons character)
  - 6 loop types identified and demonstrated: infinite retry, state loop, circular dependency, escalation loop, token threshold loop, spawn loop
  - Real-world $12K AWS bill incident case study
  - Production loop detection implementation with Python
  - Loop detector module with action repetition tracking, state fingerprinting, call stack analysis
  - Prometheus + Grafana monitoring setup for loop detection
  - DevSecOps focus: Denial of Wallet (DoW) attack protection, rate limiting, input validation
  - HashiCorp Vault integration for secrets management
  - SOC 2, GDPR, PCI-DSS compliant audit logging with PII redaction
  - Kubernetes pod restart scenario with hands-on exercise
  - Complete test suite with pytest
  - 40+ slide Marp presentation

- **Chapter 21: Building Resilient Agentic Systems** (~30,000 words, 3,956 lines)
  - Philosophy: Prevention > Detection (complement to Chapter 20)
  - 6 resilience patterns for production agents:
    1. **Circuit Breaker Pattern** - Netflix Hystrix-based implementation with CLOSED/OPEN/HALF_OPEN states
    2. **Idempotency** - Mathematical approach (f(f(x)) = f(x)) with SHA-256 hashing for safe retries
    3. **State Checkpointing** - Crash recovery for long-running workflows
    4. **Exponential Backoff + Jitter** - AWS-recommended patterns with 4 jitter types (none, full, equal, decorrelated)
    5. **Graceful Degradation** - 5-level degradation hierarchy (full → slight → moderate → minimal → failed)
    6. **Self-Healing Architectures** - Google Borg/Kubernetes patterns with automatic recovery
  - Real-world production incident response agent combining all 6 patterns
  - Netflix example: 99.99% uptime with graceful degradation (10x cost reduction)
  - Google example: Millions of containers with self-healing (MTTR: 30min → 30sec)
  - Complete production implementation with circuit breakers, retry strategies, idempotency tracking
  - Database migration agent hands-on exercise
  - Chaos engineering and testing strategies
  - Production configuration guidelines and monitoring metrics
  - 46-slide Marp presentation

### Added - Code Implementations

- **`src/chapter-20/`**
  - `src/loop_detector.py` - Core loop detection module with configurable thresholds
  - `src/monitored_agent.py` - Prometheus metrics integration (executions, loops, duration, cost tracking)
  - `src/secure_agent.py` - DoW protection with rate limiting and input validation
  - `src/secrets_manager.py` - HashiCorp Vault integration with automatic key rotation
  - `src/compliance_logger.py` - SOC 2/GDPR/PCI-DSS compliant logging with PII redaction
  - `examples/basic_loop.py` - Intentionally broken agent demonstrating infinite loops
  - `examples/fixed_loop.py` - Same agent with loop detection and human escalation
  - `tests/test_loop_detector.py` - Comprehensive unit test suite
  - Complete README.md with setup instructions and troubleshooting

- **`src/chapter-21/`**
  - `src/circuit_breaker.py` - Production-ready circuit breaker implementation
  - Complete requirements.txt with all dependencies
  - Comprehensive README.md with usage examples and production considerations

### Added - Presentations

- **`presentations/slides-chapter-20.md`** - 40+ slides covering loop detection, monitoring, security
- **`presentations/slides-chapter-21.md`** - 46 slides covering all 6 resilience patterns with code examples

### Changed - Documentation Updates

- **README.md**
  - Added Chapters 20-21 to Part 7: Advanced Agentic Development & Leadership
  - Updated table of contents with comprehensive descriptions

## [1.1.0] - 2026-01-11

### Changed - Major Content Restructure
- **Chapter Reorganization for Better Learning Flow**
  - Split Chapter 8 (Claude Code Professional) into two focused chapters:
    - **Chapter 8: Skills and Sub-Agents** - Custom capabilities, Task Tool, agentic workflows
    - **Chapter 9: Hooks and Advanced Features** - Event-driven automation, memory, CI/CD integration
  - Split old Chapter 9 (MCP Deep Dive) into two specialized chapters:
    - **Chapter 10: MCP Fundamentals** - Architecture, using existing MCP servers
    - **Chapter 11: MCP Server Development** - Building custom MCP servers (TypeScript)
  - Renamed Chapter 10 to **Chapter 12: AI for DevOps**
  - All chapters now include TL;DR sections, navigation helpers, and quick nav links
  - Updated all cross-references throughout the guide

### Added - n8n Workflow Automation
- **Chapter 13: n8n Fundamentals** (~3,800 words)
  - What is n8n and why it matters for DevOps
  - Installation and setup (Docker, Docker Compose, Kubernetes, n8n Cloud)
  - Core concepts: workflows, nodes, credentials, executions
  - First workflow tutorial: GitHub PR → Slack notification
  - Essential nodes for DevOps (HTTP Request, Schedule, Code, IF/Switch, Wait)
  - DevOps workflow examples (incident response, PR review, cost monitoring)
  - Best practices for production deployment
  - Hands-on exercises with real-world scenarios

- **Chapter 14: Advanced n8n Workflows** (~4,200 words)
  - Advanced workflow patterns (sub-workflows, parallel execution, error workflows)
  - Integrating n8n with AI services (Claude API, OpenAI GPT)
  - Using AI within n8n workflows (log analysis, intelligent alerting, auto-generate infrastructure code)
  - Complex DevOps automations (multi-stage CI/CD, infrastructure drift detection, security compliance)
  - n8n + Claude Code bidirectional integration
  - Database & state management (PostgreSQL, Redis)
  - Production considerations (queue mode, HA setup, Kubernetes deployment)
  - Monitoring and observability (Prometheus, Grafana)
  - Real-world case studies (82% MTTR reduction, 22% cost savings)
  - Hands-on exercises for advanced scenarios

### Changed - Documentation Updates
- **README.md**
  - Updated learning path diagram to include 5 parts (14 chapters total)
  - Reorganized table of contents with new chapter structure
  - Updated Express Path, Complete Path, and Practical Path learning guides
  - Updated Quick Start section references
  - Updated repository structure to show 14 chapters
  - Updated src/ folder descriptions for all chapters

- **CLAUDE.md**
  - Updated repository structure to show 14 chapters
  - Updated learning path progression with 5 phases
  - Added workflow orchestration to key concepts
  - Updated "Where These Features Are Documented" section
  - Updated "Chapter Topics at a Glance" reference table

- **Documentation Updates for Claude Code v2.1.4** (from previous work)
  - Updated Chapter 8 to clarify v2.1.3 unified skills/commands system
  - Updated Chapter 7 with latest command features and v2.1.3 changes
  - Added comprehensive Claude Code version information section to CLAUDE.md
  - Added version coverage notice to README.md
  - Documented new environment variables: `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `IS_DEMO`, `FORCE_AUTOUPDATE_PLUGINS`
  - Updated hook timeout documentation (60s → 10 minutes in v2.1.3)
  - Added release channel configuration information
  - Clarified hot-reload functionality for skills
  - Added version compatibility notes throughout documentation

### Technical Details
- **Chapters**: Expanded from 10 to 14 chapters
- **Words Added**: ~8,000+ words of new content (Chapters 13-14)
- **New Topics**: n8n workflow automation, AI integration patterns, production deployment strategies
- **Cross-references**: Updated throughout all chapters and documentation files

## [1.0.0] - 2026-01-10

### 🎮 Major Addition: DevOps Quest Gamification System

A complete interactive learning layer that transforms the guide into an engaging, hands-on experience.

### Added

#### Progress Tracker System
- **Progress Dashboard** with beautiful ASCII UI using Rich library
- **Achievement/Badge System** with 15 unlockable badges
- **Streak Tracking** for daily learning habits
- **Player Profiles** stored in `~/.ai-devops-quest/`
- **CLI Interface** for tracking completions and viewing stats
- **Achievement Logic** for automatic badge awarding based on conditions

#### Challenge System
- **Challenge 01: Prompt Dojo** - Token Minimization (⭐⭐)
  - Reduce prompt tokens by 75% while maintaining quality
  - Auto-grader with correctness, efficiency, and quality scoring
  - Progressive 3-hint system (costs points)
  - Reference solution with detailed analysis
  - Multiple difficulty modes (Normal, Hard, Nightmare)
- **Challenge 02: Token Detective** (⭐⭐⭐)
  - Audit and optimize 5 production prompts
  - 60% token reduction goal (8500 → 3400 tokens)
- **Challenge 03: CRAFT Master** (⭐⭐⭐)
  - Master the CRAFT framework for perfect code generation
  - Generate production-ready code on first try
- **Challenge 04: Claude Code Basics** (⭐)
  - First hands-on session with Claude Code
  - 5 fundamental tasks to complete
- **Token Counter Utility** (`challenges/lib/count-tokens.py`)
  - Accurate token counting using tiktoken
  - Challenge-specific feedback and scoring
- **Auto-Grader Framework** for instant feedback
- **Hint Systems** with progressive disclosure

#### Story Mode System
- **Chapter 6: "The Midnight Deployment Crisis"** 🚨
  - Immersive 450-line narrative experience
  - Production incident at 2:47 AM scenario
  - 30-minute time-pressured mission
  - Multiple difficulty levels (Novice, Normal, Hard, Nightmare)
  - Real-time event simulation
  - Success/failure outcomes with consequences
- **Interactive Launcher** (`story-mode/play.sh`)
  - Menu-driven chapter selection
  - Progress tracking integration

#### Sandbox Environment System
- **Incident 01: CrashLoopBackOff** (⭐⭐)
  - Full Docker Compose environment
  - Broken Flask API with intentional configuration bug
  - PostgreSQL database integration
  - Auto-grader with 4 test categories
  - 60-second stability check
  - Progressive hint system
  - Realistic production debugging scenario

#### Documentation
- `gamification/README.md` - Comprehensive system overview
- `gamification/TODO.md` - Detailed implementation roadmap (200+ items)
- `gamification/IMPLEMENTATION_SUMMARY.md` - Status and architecture
- `gamification/TEST_RESULTS.md` - Complete test report
- `gamification/COMPLETE.md` - Achievement summary
- Updated `CLAUDE.md` with gamification section

#### Repository Improvements
- **CLAUDE.md** - Added for Claude Code instances to understand repo
- **CHANGELOG.md** - This file (project changelog)
- Updated README.md structure in CLAUDE.md

### Changed
- **CLAUDE.md**: Added gamification system documentation
- **Repository Structure**: Added `gamification/` directory to structure

### Technical Details

**Files Added**: 39+
**Lines of Code**: 2,585+
**Languages**: Python, Bash, Markdown, YAML, Dockerfile
**Dependencies**: rich, click, pyyaml, python-dateutil, tiktoken

### Learning Paths

Three distinct paths for different learning styles:
- 🚀 **Speed Run** (20 hours) - Core challenges, minimum viable
- 🎓 **Knowledge Master** (40-60 hours) - Complete mastery
- ⚡ **Hybrid** (30-40 hours) - Balanced approach (recommended)

### Features

- **Token Economics Focus** - Real-world cost optimization skills
- **Multi-Difficulty Modes** - Same challenge, harder constraints
- **Progressive Hints** - Strategic help without solving
- **Realistic Scenarios** - Production-like environments
- **Auto-Grading** - Instant feedback on solutions
- **Visual Progress** - Beautiful terminal dashboards
- **Achievement System** - 15 badges to unlock
- **Streak Tracking** - Daily learning habit building

### Testing
- ✅ All Python syntax validated
- ✅ All shell scripts tested
- ✅ Integration tests passing
- ✅ End-to-end flow verified

### Breaking Changes
None - All additions, no modifications to existing content

---

## [0.1.1] - 2026-01-09

### Changed
- Updated guide with Claude Code 2.1.x changelog features
- Added hands-on practice references to Chapters 8 and 9
- Added Community Tools & Utilities section to Additional Resources
- Revised README for v1.1.0 updates and enhancements

### Fixed
- README formatting in Community Tools & Utilities section

---

## [0.1.0] - 2025-XX-XX

### Added
- Initial release of "AI and Claude Code: A Comprehensive Guide for DevOps Engineers"
- 10 comprehensive chapters covering AI fundamentals through advanced Claude Code usage
- Chapter 1: Introduction to AI
- Chapter 2: Understanding LLMs and Tokens
- Chapter 3: The Art of Prompting (CRAFT Framework)
- Chapter 4: AI Models Landscape
- Chapter 5: Introduction to Claude
- Chapter 6: Claude Code Fundamentals
- Chapter 7: Claude Code Intermediate
- Chapter 8: Claude Code Professional
- Chapter 9: MCP Deep Dive
- Chapter 10: AI for DevOps
- Marp presentation slides for all chapters
- Code examples for each chapter in `src/`
- GitHub Actions workflow for generating PowerPoint presentations
- CC BY-NC 4.0 License
- Contributing guidelines

---

## Upgrade Guide

### From v0.1.x to v1.0.0

**New Features Available**:
1. Initialize your gamification profile:
   ```bash
   cd gamification/progress-tracker
   pip install -r requirements.txt
   python tracker.py init
   ```

2. Try your first challenge:
   ```bash
   cd gamification/challenges/01-prompt-dojo
   ./start.sh
   ```

3. Experience story mode:
   ```bash
   cd gamification/story-mode
   ./play.sh
   ```

**No Breaking Changes**: All existing guide content remains unchanged.

---

## Links

- [Repository](https://github.com/michelabboud/ai-and-claude-code-intro)
- [License](./LICENSE)
- [Contributing](./CONTRIBUTING.md)
- [Gamification README](./gamification/README.md)

---

**Note**: Version 1.0.0 represents the first major milestone with the complete gamification system, making this guide production-ready for interactive learning.
