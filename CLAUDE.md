# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Overview

This is **"AI and Claude Code: A Comprehensive Guide for DevOps Engineers"** - an educational resource teaching AI fundamentals through professional Claude Code workflows. The guide progresses from basic AI concepts to advanced MCP server integration, specifically designed for DevOps professionals.

**Author**: Michel Abboud
**License**: CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial)
**Claude Code Version Coverage**: v2.1.4 (January 2025) and earlier
**Last Updated**: January 2026

---

## Repository Structure

```
ai-and-claude-code-intro/
├── chapters/                    # Main guide content (16 markdown chapters)
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
│   └── 16-multi-agent-advanced.md
│
├── presentations/               # Marp slide decks for teaching
│   ├── slides-chapter-*.md     # Marp markdown source files
│   └── pptx/                   # Generated PowerPoint files (via GH Actions)
│
├── src/                        # Working code examples by chapter
│   ├── chapter-01/             # AI fundamentals examples (Python)
│   ├── chapter-02/             # Token counting utilities (Python)
│   ├── chapter-03/             # CRAFT framework templates
│   ├── chapter-04/             # Model selection tools
│   ├── chapter-05/             # Claude API examples
│   ├── chapter-06/             # Claude Code configs and commands
│   ├── chapter-07/             # Custom commands, GitHub Actions
│   ├── chapter-08/             # Skills, sub-agents configurations
│   ├── chapter-09/             # Hooks, memory, CI/CD examples
│   ├── chapter-10/             # MCP usage examples
│   ├── chapter-11/             # MCP server implementations (TypeScript)
│   ├── chapter-12/             # Shell aliases, DevOps workflows
│   ├── chapter-13/             # n8n workflow examples
│   ├── chapter-14/             # Advanced n8n workflows
│   ├── chapter-15/             # Multi-agent fundamentals (agents, coordination, pools)
│   └── chapter-16/             # Advanced multi-agent (incident swarms, code review, monitoring)
│
├── gamification/               # 🎮 NEW: DevOps Quest learning system
│   ├── progress-tracker/       # Track progress, achievements, streaks
│   ├── challenges/             # Hands-on coding challenges with auto-grading
│   ├── story-mode/             # Narrative-driven learning (in development)
│   ├── sandbox/                # Docker-based incident scenarios (planned)
│   └── README.md               # Gamification overview
│
├── README.md                   # Main documentation
├── CONTRIBUTING.md             # Contributor guidelines and licensing
└── LICENSE                     # CC BY-NC 4.0 license
```

---

## Content Architecture

### Learning Path Progression

The guide follows a deliberate progression:

1. **Foundations (Chapters 1-3)**: AI basics, LLMs, tokenization, prompt engineering
2. **AI Ecosystem (Chapters 4-5)**: Model landscape, Claude introduction
3. **Claude Code Mastery (Chapters 6-9)**: From basics to professional workflows with skills, sub-agents, and hooks
4. **MCP Integration (Chapters 10-11)**: Model Context Protocol fundamentals and custom server development
5. **Workflow Automation (Chapters 12-14)**: Real-world DevOps applications, n8n fundamentals and advanced patterns
6. **Multi-Agent Orchestration (Chapters 15-16)**: Agent teams, specialist agents, production incident response swarms

### Key Concepts Taught

- **CRAFT Framework**: Context, Role, Action, Format, Target (prompting methodology)
- **Token Economics**: Understanding costs, context windows, optimization
- **Multi-Agent Workflows**: Skills, sub-agents, hooks for Claude Code
- **MCP Integration**: Building custom Model Context Protocol servers
- **DevOps Automation**: Incident response, infrastructure generation, code review
- **Workflow Orchestration**: n8n automation, AI integration, production deployment

---

## Gamification System (DevOps Quest)

**NEW (2026-01)**: Interactive learning layer with challenges, progress tracking, and achievements.

### Quick Start

```bash
# Initialize your quest profile
cd gamification/progress-tracker
pip install -r requirements.txt
python tracker.py init

# View progress dashboard
python tracker.py

# Start first challenge
cd ../challenges/01-prompt-dojo
./start.sh
```

### Key Components

1. **Progress Tracker** (`gamification/progress-tracker/`)
   - Tracks chapter/challenge completion
   - Achievement/badge system
   - Learning streak tracking
   - Beautiful ASCII dashboard

2. **Challenges** (`gamification/challenges/`)
   - 30 planned coding challenges (1 complete)
   - Auto-graded with scoring
   - Progressive hint system
   - Token optimization focus

3. **Story Mode** (`gamification/story-mode/`) - *In Development*
   - Narrative-driven chapter overlays
   - DevOps crisis scenarios
   - Time-based missions

4. **Sandbox Labs** (`gamification/sandbox/`) - *Planned*
   - Docker-based broken environments
   - Incident response practice
   - Auto-graded solutions

### Development Status

- ✅ Progress tracker functional (achievement logic needs implementation)
- ✅ First challenge complete (Prompt Dojo 01: Token Minimization)
- 🚧 29 more challenges planned
- 🚧 Story mode designed, content pending
- 🚧 Sandbox environments planned

See `gamification/IMPLEMENTATION_SUMMARY.md` for full details.

---

## Common Commands

### Generate PowerPoint Presentations

The repository uses Marp CLI to convert Markdown slides to PowerPoint format.

```bash
# Install Marp CLI globally
npm install -g @marp-team/marp-cli

# Convert a single presentation
cd presentations
marp slides-chapter-01.md --pptx -o pptx/slides-chapter-01.pptx

# Convert all presentations
for file in slides-chapter-*.md; do
  marp "$file" --pptx -o "pptx/${file%.md}.pptx"
done

# Export to PDF instead
marp slides-chapter-01.md --pdf -o chapter-01.pdf

# Preview in browser
marp -s .  # Opens server at http://localhost:8080
```

**Note**: There's also a GitHub Actions workflow (`.github/workflows/generate-pptx.yml`) that can be manually triggered to generate all PowerPoint files automatically.

### Working with Examples

```bash
# Python examples (Chapters 1-5)
cd src/chapter-02
python token_examples.py

# TypeScript examples (MCP servers in Chapter 9)
cd src/chapter-09/mcp-servers
npm init -y
npm install @modelcontextprotocol/sdk @kubernetes/client-node @aws-sdk/client-ec2
npx tsx kubernetes-mcp-server.ts

# Shell aliases (Chapter 10)
source src/chapter-10/shell-aliases.sh
```

### Git Workflow

```bash
# Standard contribution workflow
git checkout -b feature/your-contribution-name
# Make changes...
git add .
git commit -m "Description of changes"
git push origin feature/your-contribution-name
# Create PR via GitHub UI
```

---

## Development Guidelines

### Content Standards

#### Chapter Formatting
- **Audience**: DevOps engineers, SREs, platform engineers
- **Tone**: Professional, practical, hands-on focused
- **Structure**: Each chapter includes:
  - Clear learning objectives
  - Real-world DevOps examples
  - Practical exercises
  - Key takeaways section

#### Code Examples
- All code examples must be tested and working
- Include comments explaining DevOps-specific context
- Prefer realistic scenarios over toy examples
- Place examples in appropriate `src/chapter-XX/` directory

#### Presentation Slides
- Use Marp markdown format
- Follow consistent theme across all slides
- Include visual diagrams where beneficial
- Keep slides concise (teaching format)

### File Naming Conventions

- Chapters: `XX-descriptive-name.md` (e.g., `11-new-topic.md`)
- Presentations: `slides-chapter-XX.md` or `slides-chapter-XX-YY.md`
- Code examples: Descriptive names matching chapter content
- Use lowercase with hyphens for all filenames

### When Editing Content

**Critical**: This is a copyrighted educational work (CC BY-NC 4.0). When making changes:

1. **Preserve Attribution**: Maintain author credits
2. **Respect License**: All content remains under CC BY-NC 4.0
3. **Follow Style**: Match existing tone and formatting
4. **Test Examples**: Verify all code works before committing
5. **Update Cross-References**: If adding chapters, update README.md table of contents

### Contributor Rights

See `CONTRIBUTING.md` for details on contributor tiers:
- **Contributor**: 1+ merged PR → Attribution
- **Core Contributor**: 3+ significant PRs → Personal commercial use rights
- **Co-Author**: Major contributions → Full commercial rights

---

## Key Files and Their Purpose

| File | Purpose | Edit Frequency |
|------|---------|----------------|
| `README.md` | Main guide overview, quick start, navigation | Update when adding chapters |
| `chapters/*.md` | Core educational content | Primary editing target |
| `presentations/slides-*.md` | Teaching slide decks (Marp format) | Update with chapter changes |
| `src/chapter-XX/*` | Working code examples and configurations | Add new examples as needed |
| `CONTRIBUTING.md` | Contributor guidelines, licensing terms | Rarely changed |
| `LICENSE` | CC BY-NC 4.0 legal text | Never change |

---

## Important Context for Claude Code

### Code Examples Are Educational
The code in `src/` is designed for **teaching**, not production use. Examples prioritize clarity and demonstration over optimization. When suggesting improvements:
- Explain the educational trade-offs
- Consider whether changes aid or hinder learning
- Maintain simplicity where appropriate for teaching

### Dual-Format Content
Many concepts appear in **both** chapter text and presentation slides. When updating content:
- Check if related presentation exists
- Consider updating both formats for consistency
- Slides are intentionally more concise

### Target Audience Context
Content is specifically written for **DevOps engineers**. When making suggestions:
- Use DevOps terminology (Kubernetes, Terraform, CI/CD, etc.)
- Provide infrastructure and operations examples
- Reference relevant tools (Docker, Ansible, AWS, monitoring systems)
- Assume command-line comfort, Linux familiarity

### MCP Server Examples (Chapter 9)
The TypeScript MCP server examples demonstrate custom protocol implementations. These require:
- Node.js 18+ and npm/npx
- Appropriate SDKs (@modelcontextprotocol/sdk)
- Environment variables for API tokens/credentials
- Understanding they're teaching examples, not production-ready

### CRAFT Framework Reference
The guide teaches the **CRAFT prompting framework**:
- **C**ontext: Environment, versions, constraints
- **R**ole: Expert persona for the AI
- **A**ction: Specific task to perform
- **F**ormat: Desired output structure
- **T**arget: Success criteria

This framework should be referenced when discussing prompt engineering in the guide.

---

## License Compliance

**Critical**: This work is licensed under CC BY-NC 4.0. When working with this repository:

✅ **Allowed**:
- Reading and learning from content
- Forking for personal use
- Contributing improvements via PR
- Sharing with attribution

❌ **Requires Permission**:
- Commercial use (paid training, consulting, courses)
- Removing author attribution
- Sublicensing under different terms

Any PRs must agree to license contributions under the same CC BY-NC 4.0 terms (see CONTRIBUTING.md).

---

## Related Resources

The guide references a companion toolkit:
- **claude-code-helper** (by same author): Production-ready configurations, 33 sub-agents, 5 MCP servers, skills, templates
- Repository: github.com/michelabboud/claude-code-helper
- Complements this guide with hands-on examples

Official documentation referenced:
- Claude Documentation: docs.anthropic.com
- Claude Code Documentation: docs.anthropic.com/claude-code
- Claude Code CHANGELOG: github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- MCP Specification: modelcontextprotocol.io

---

## Claude Code Version Information

### Current Version Coverage

This guide covers **Claude Code v2.1.4 (January 2025)** and earlier versions.

### Key Features by Version

**v2.1.4 (Latest - January 2025)**
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable for disabling background tasks
- Improved OAuth token refresh handling

**v2.1.3 (January 2025)**
- **Unified slash commands and skills** - merged into single concept, simplified mental model
- Release channel toggle (`stable` or `latest`) in `/config`
- Tool hook timeout increased to 10 minutes (from 60 seconds)
- Improved permission rule detection and `/doctor` warnings

**v2.1.2 (December 2024)**
- Shift+Tab in plan mode for "auto-accept edits"
- Source path metadata for dragged images
- Clickable file path hyperlinks (OSC 8 support)
- Windows Package Manager (winget) support

**v2.1.0 (Major Release - November 2024)**
- Automatic skill hot-reload from `~/.claude/skills` or `.claude/skills`
- Sub-agent context forking (`context: fork` in frontmatter)
- Language setting configuration
- Real-time steering (send messages while Claude is working)
- Unified Ctrl+B backgrounding
- MCP `list_changed` notifications for dynamic tool updates

### Important Conceptual Changes

**Skills and Slash Commands (v2.1.3)**
The guide previously distinguished between "slash commands" and "skills" as separate concepts. As of v2.1.3, they are **completely unified** - there is no difference anymore. Use either `.claude/commands/` or `.claude/skills/` directories interchangeably. Both support:
- Custom frontmatter (arguments, description, context forking)
- Hot-reload (automatically available without restart)
- Same invocation pattern (`/command-name`)

**Context Forking (v2.1.0)**
Skills/commands can now run in isolated sub-agent contexts using `context: fork` in frontmatter. This prevents context pollution for long-running or resource-intensive operations.

### Where These Features Are Documented

- **Chapter 6**: Claude Code fundamentals
- **Chapter 7**: Custom commands/skills (unified system), IDE integration
- **Chapter 8**: Skills and sub-agents (Task Tool, agentic workflows)
- **Chapter 9**: Hooks and advanced features (event-driven automation, CI/CD)
- **Chapters 10-11**: MCP protocol fundamentals and server development

---

## Quick Reference

### Chapter Topics at a Glance

| Chapters | Focus Area |
|----------|-----------|
| 1-3 | AI fundamentals, LLMs, prompting |
| 4-5 | AI models landscape, Claude intro |
| 6-9 | Claude Code: fundamentals → intermediate → skills/sub-agents → hooks/advanced |
| 10-11 | MCP (Model Context Protocol): fundamentals and server development |
| 12-14 | Real-world AI for DevOps, n8n workflow automation (fundamentals and advanced) |
| 15-16 | Multi-Agent Orchestration: agent teams, specialist agents, production swarms |

### Key Commands Summary

```bash
# Generate presentations
npm install -g @marp-team/marp-cli
marp presentations/slides-*.md --pptx

# Run Python examples
cd src/chapter-XX && python example.py

# Run TypeScript/MCP examples
cd src/chapter-09/mcp-servers
npm install && npx tsx server-name.ts

# Test shell utilities
source src/chapter-10/shell-aliases.sh
```

---

**Last Updated**: 2026-01-10
