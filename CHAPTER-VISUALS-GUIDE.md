# Chapter Visuals Guide

**Purpose**: This document contains detailed AI image generation prompts for all chapter visuals in "AI and Claude Code: A Comprehensive Guide for DevOps Engineers".

**Author**: Michel Abboud
**Created**: January 2026
**Last Updated**: January 2026

---

## Table of Contents

- [Global Context Preamble](#global-context-preamble-copy-paste-this-first)
- [Style Guidelines](#style-guidelines)
- [Naming Convention](#naming-convention)
- [Image Types Reference](#image-types-reference)
- [Chapter 01: Introduction to AI](#chapter-01-introduction-to-ai)
- [Chapter 02: Understanding LLMs and Tokens](#chapter-02-understanding-llms-and-tokens)
- [Chapter 03: The Art of Prompting](#chapter-03-the-art-of-prompting)
- [Chapter 04: AI Models Landscape](#chapter-04-ai-models-landscape)
- [Chapter 05: Introduction to Claude](#chapter-05-introduction-to-claude)
- [Chapter 06: Claude Code Fundamentals](#chapter-06-claude-code-fundamentals)
- [Chapter 07: Claude Code Intermediate](#chapter-07-claude-code-intermediate)
- [Chapter 08: Skills and Subagents](#chapter-08-skills-and-subagents)
- [Chapter 09: Hooks and Advanced Features](#chapter-09-hooks-and-advanced-features)
- [Chapter 10: MCP Fundamentals](#chapter-10-mcp-fundamentals)
- [Chapter 11: MCP Server Development](#chapter-11-mcp-server-development)
- [Chapter 12: AI for DevOps](#chapter-12-ai-for-devops)
- [Chapter 13: n8n Fundamentals](#chapter-13-n8n-fundamentals)
- [Chapter 14: n8n Advanced](#chapter-14-n8n-advanced)
- [Chapter 15: Multi-Agent Fundamentals](#chapter-15-multi-agent-fundamentals)
- [Chapter 16: Multi-Agent Advanced](#chapter-16-multi-agent-advanced)
- [Chapter 17: AIOps Fundamentals](#chapter-17-aiops-fundamentals)
- [Chapter 18: AIOps Advanced](#chapter-18-aiops-advanced)
- [Chapter 19: Team Transformation](#chapter-19-team-transformation)
- [Chapter 20: Agent Loop Detection](#chapter-20-agent-loop-detection)
- [Chapter 21: Resilience Patterns](#chapter-21-resilience-patterns)
- [Chapter 22: Production Deployment](#chapter-22-production-deployment)
- [Chapter 23: RAG Fundamentals](#chapter-23-rag-fundamentals)
- [Chapter 24: RAG Search Optimization](#chapter-24-rag-search-optimization)
- [Chapter 25: Production RAG Systems](#chapter-25-production-rag-systems)

---

## Global Context Preamble (Copy-Paste This First)

**Important**: Before using any prompt from this guide, copy and paste the context block below to your AI image generator first. This gives the model essential context about the subject matter, visual style, and intended use.

### Context Block for AI Image Generators

```
CONTEXT FOR ALL IMAGES:

I am creating visuals for an educational technical guide titled "AI and Claude Code: A Comprehensive Guide for DevOps Engineers" by Michel Abboud.

ABOUT THE GUIDE:
- A 25-chapter comprehensive guide teaching AI fundamentals through professional Claude Code workflows
- Target audience: DevOps engineers, SREs, platform engineers, and infrastructure professionals
- Covers: AI/LLM fundamentals, prompt engineering, Claude (Anthropic's AI assistant), Claude Code (CLI development tool), Model Context Protocol (MCP), workflow automation, multi-agent systems, AIOps, and production deployment
- The guide is practical and hands-on, focusing on real-world DevOps scenarios

KEY SUBJECTS AND TERMINOLOGY:
- Claude: Anthropic's AI assistant (the AI model itself)
- Claude Code: A command-line interface (CLI) tool that allows developers to interact with Claude directly from their terminal
- Anthropic: The AI safety company that created Claude
- DevOps: Development operations - automation, CI/CD pipelines, infrastructure as code
- MCP (Model Context Protocol): A protocol for AI tools to access external data sources
- n8n: An open-source workflow automation platform
- AIOps: AI for IT operations - monitoring, alerting, incident response
- RAG: Retrieval-Augmented Generation - enhancing AI with external knowledge

VISUAL STYLE REQUIREMENTS:
- Modern tech illustration, clean and professional
- Flat design with subtle gradients, isometric elements where appropriate
- Primary colors: Tech blues (#1a73e8, #4285f4), DevOps oranges (#ff6d00, #ff9100)
- Secondary colors: Neutral grays (#5f6368), accent purples (#7c4dff, #b388ff)
- Professional, approachable, educational mood - slightly futuristic
- Suitable for technical documentation and presentations
- Clean backgrounds (white, light gray #f8f9fa, or dark mode #1e1e1e)
- NO photorealistic humans, NO stock photo aesthetics, NO clip-art style
- Minimal text in images; when needed use clean sans-serif fonts

OUTPUT REQUIREMENTS:
- High resolution suitable for digital documentation
- Clean crisp edges, high contrast
- Professional quality suitable for a published technical guide
```

### How to Use This Guide

1. **Copy the context block above** and paste it at the start of your conversation with the AI image generator (Midjourney, DALL-E, Flux, Stable Diffusion, etc.)

2. **Then copy the specific image prompt** from the chapter section below

3. **Combine them** - the context block provides the "who, what, why" and the specific prompt provides the "exact image to generate"

**Example combined prompt:**
```
[Paste context block first]

Now generate this specific image:
[Paste individual prompt from chapter section]
```

---

## Style Guidelines

### Overall Visual Identity

| Attribute | Specification |
|-----------|---------------|
| **Primary Style** | Modern tech illustration, clean and professional |
| **Art Direction** | Flat design with subtle gradients, isometric elements where appropriate |
| **Color Palette** | Tech blues (#1a73e8, #4285f4), DevOps oranges (#ff6d00, #ff9100), neutral grays (#5f6368, #202124), accent purples (#7c4dff, #b388ff) |
| **Background** | Clean white, subtle light gray (#f8f9fa), or dark mode (#1e1e1e) depending on context |
| **Typography in Images** | Minimal text; when needed use clean sans-serif (Roboto, Inter style) |
| **Mood** | Professional, approachable, educational, slightly futuristic |
| **Avoid** | Overly cartoonish, clip-art style, photorealistic humans, stock photo aesthetics |

### Resolution and Aspect Ratios

| Use Case | Aspect Ratio | Minimum Resolution |
|----------|--------------|-------------------|
| Chapter header images | 16:9 | 1920x1080 |
| Inline diagrams | 4:3 or 16:9 | 1200x900 or 1600x900 |
| Concept illustrations | 1:1 or 4:3 | 1200x1200 or 1200x900 |
| Process flows | 16:9 or 21:9 | 1920x1080 or 2560x1080 |
| Infographics | 3:4 or 2:3 (vertical) | 1200x1600 |

### Style Modifiers for Prompts

Always include these style modifiers in prompts (adjust as needed):

```
Style modifiers: modern tech illustration, clean vector style, flat design with subtle depth,
professional color palette (tech blues, DevOps orange accents), minimal and elegant,
educational diagram aesthetic, high contrast, crisp edges, no text unless specified,
white or light gray background, suitable for technical documentation
```

### Animation Candidates (GIF/Video)

Mark images that could benefit from animation with: `🎬 ANIMATION CANDIDATE`

Criteria for animation:
- Processes with sequential steps
- Data flowing through systems
- Before/after transformations
- Real-time monitoring concepts
- Token streaming visualizations

---

## Naming Convention

### Format
```
chapter-XX-img-YY-[type]-[brief-description].[ext]
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| `XX` | Chapter number (01-25) | `01`, `15`, `25` |
| `YY` | Image number within chapter (01-99) | `01`, `05`, `12` |
| `type` | Image category (see below) | `diagram`, `concept`, `flow` |
| `brief-description` | 2-4 word description, hyphenated | `ai-evolution`, `token-flow` |
| `ext` | File extension | `png`, `jpg`, `gif` |

### Image Types

| Type Code | Description | Best For |
|-----------|-------------|----------|
| `header` | Chapter title/hero image | Opening visual for each chapter |
| `concept` | Abstract conceptual illustration | Explaining ideas, mental models |
| `diagram` | Technical architecture/structure | System designs, relationships |
| `flow` | Process/workflow visualization | Step-by-step processes, pipelines |
| `compare` | Comparison/contrast visual | Before/after, A vs B |
| `info` | Infographic with data/stats | Summaries, key points, stats |
| `icon` | Decorative icon or small visual | Section markers, callouts |
| `screen` | UI mockup or screenshot style | Tool interfaces, dashboards |

### Examples

```
chapter-01-img-01-header-introduction-to-ai.png
chapter-02-img-03-diagram-token-flow.png
chapter-05-img-02-concept-claude-personality.png
chapter-10-img-05-flow-mcp-protocol.gif
chapter-17-img-01-compare-traditional-vs-aiops.png
```

---

## Image Types Reference

### For AI Image Generators (Midjourney, DALL-E, Flux, Stable Diffusion)

Best suited for:
- Conceptual illustrations
- Abstract representations
- Header/hero images
- Metaphorical visuals

### For Diagramming Tools (Mermaid, Draw.io, Excalidraw)

Better suited for:
- Precise technical architectures
- Code flow diagrams
- Network topologies
- Sequence diagrams
- Entity relationships

When a diagram would be better created with tools, I'll note: `📐 RECOMMEND: Use diagramming tool`

---

## Chapter 01: Introduction to AI

### Overview
- **Chapter Focus**: AI fundamentals, history, types, and DevOps relevance
- **Total Images**: 8
- **Animation Candidates**: 2

---

### Image 01-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-01-header-introduction-to-ai.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Welcome, DevOps Engineer!" section |
| **Alt Text** | "Abstract visualization of artificial intelligence concepts with neural network patterns, code elements, and DevOps infrastructure symbols merging together" |

**Prompt:**
```
A stunning wide-angle hero illustration representing the introduction to artificial intelligence for DevOps engineers. The composition shows an abstract visualization where traditional infrastructure elements (servers, containers, network nodes depicted as geometric shapes) on the left side gradually transform and merge into flowing neural network patterns and AI brain representations on the right side.

The left portion features clean geometric server rack silhouettes, Docker container hexagons, and Kubernetes wheel symbols in cool grays and blues. These elements dissolve into flowing particle streams that form elegant neural pathway patterns, eventually coalescing into a stylized AI brain or abstract intelligence symbol on the right.

Color palette: Deep tech blue (#1a73e8) as primary, transitioning through electric blue gradients to warm DevOps orange (#ff6d00) accents on the AI elements. Background is a clean gradient from white to very light gray (#f8f9fa).

Style: Modern tech illustration, clean vector aesthetic with subtle depth and glow effects, professional and sophisticated, no text, suitable as a chapter opening hero image. The overall feeling should convey "traditional DevOps evolving into AI-powered operations."

Lighting: Soft ambient with subtle glowing nodes and connection lines. High contrast, crisp edges.
```

---

### Image 01-02: Traditional vs AI-Powered Systems

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-02-compare-traditional-vs-ai.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After the comparison table in section 1.1 (around line 43) |
| **Alt Text** | "Split comparison showing traditional rule-based automation on the left versus AI-powered adaptive systems on the right" |

**Prompt:**
```
A clean split-screen comparison illustration contrasting traditional automation versus AI-powered systems, designed for DevOps engineers.

LEFT SIDE - "Traditional Automation":
- A rigid, mechanical representation with hard geometric shapes
- Flowchart-style decision tree with if/then branches shown as angular pathways
- A stylized gauge or meter showing a fixed threshold (like CPU at 80%)
- Static, predictable arrows pointing in predetermined directions
- Color scheme: Cool grays (#5f6368), muted blues, mechanical silver tones
- Visual metaphor: A railroad track with fixed switches, or a rigid pipeline with set valves
- Mood: Functional but inflexible

RIGHT SIDE - "AI-Powered System":
- Organic, flowing shapes with neural network patterns
- Adaptive pathways that branch and merge dynamically
- Multiple data streams feeding into a glowing brain/intelligence node
- Predictive arrows that anticipate and curve before events
- Color scheme: Vibrant tech blues (#4285f4), glowing accent purples (#7c4dff), warm orange highlights (#ff9100)
- Visual metaphor: A living organism that learns and adapts, or water finding optimal paths
- Mood: Intelligent, adaptive, forward-looking

CENTER DIVIDER:
- A subtle gradient transition or vertical divide
- Could show the evolution/transformation from left to right

Style: Modern flat illustration with subtle gradients and depth, clean vector aesthetic, professional tech documentation style, no text labels, high contrast, white background.
```

**🎬 ANIMATION CANDIDATE**: This could be a short GIF showing the transformation from traditional to AI-powered, with elements morphing and coming alive.

---

### Image 01-03: AI History Timeline

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-03-flow-ai-history-timeline.png` |
| **Type** | Flow |
| **Aspect Ratio** | 21:9 (ultra-wide) or 16:9 |
| **Placement** | Replace or accompany the ASCII timeline in section 1.2 (around line 48-79) |
| **Alt Text** | "Visual timeline of AI history from 1950s to 2020s, showing major milestones and eras" |

**Prompt:**
```
An elegant horizontal timeline illustration depicting the history of artificial intelligence from the 1950s to the 2020s, designed for a technical audience.

The timeline flows from left to right as a stylized pathway or river that changes character through each era:

1950s - "THE DREAM BEGINS" (Far left):
- Vintage computer aesthetic, vacuum tubes, early mainframe silhouette
- A small spark or lightbulb moment
- Muted sepia/gray tones with a hint of hopeful yellow
- Icon: Classic Turing machine or early computer symbol

1960s-1970s - "AI WINTER":
- The pathway narrows and becomes icy/frozen
- Snowflake patterns, cold blue-white tones
- Descending graph line suggesting decline
- Mood: Cold, dormant, waiting

1980s - "EXPERT SYSTEMS":
- Pathway thaws, shows rigid decision trees
- Flowchart-style branching patterns
- Corporate/business aesthetic, muted professional colors
- Icon: Branching logic tree

1990s-2000s - "MACHINE LEARNING RISE":
- Pathway widens, shows data streams
- Chess piece (Deep Blue reference) as a milestone marker
- Emerging pattern recognition visualized as clustering dots
- Colors warming up: blues transitioning to teals

2010s - "DEEP LEARNING REVOLUTION":
- Pathway becomes a neural network
- GPU chip aesthetic, parallel processing visualization
- ImageNet moment shown as classified images in a grid
- Go board pattern (AlphaGo reference)
- Colors: Electric blues, emerging purples

2020s - "THE LLM ERA" (Far right, most prominent):
- Pathway explodes into text/language visualization
- Chat bubble or conversation interface aesthetic
- Glowing, most vibrant section
- Claude/ChatGPT era feeling: conversational, accessible
- Colors: Full vibrant palette, glowing oranges and blues, most saturated

Style: Clean modern illustration, flowing continuous design, each era visually distinct but connected, timeline feels like a journey. No text (eras will be labeled separately), infographic quality, suitable for educational materials, white or very light background.
```

---

### Image 01-04: Types of AI - Capability Pyramid

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-04-diagram-ai-capability-levels.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 4:3 or 1:1 |
| **Placement** | Replace or accompany the ASCII diagram in section 1.3 (around line 87-107) |
| **Alt Text** | "Pyramid diagram showing Narrow AI (current) at the base and Artificial General Intelligence (future goal) at the apex" |

**Prompt:**
```
A clean, modern pyramid or layered diagram illustrating the levels of AI capability.

STRUCTURE (bottom to top):

BOTTOM LAYER - "NARROW AI (ANI)" - Large, solid, well-established:
- Takes up approximately 70% of the pyramid's visual weight
- Filled with subtle iconography representing specific AI applications:
  - Chat bubble (language models like Claude/ChatGPT)
  - Paint palette or image frame (image generation like DALL-E)
  - Code brackets (code assistants like Copilot)
  - Car silhouette (autonomous driving)
- Solid, confident colors: Rich tech blue (#1a73e8), well-defined edges
- Badge or marker indicating "CURRENT STATE" or "TODAY"
- Feeling: Established, proven, tangible

TOP LAYER - "ARTIFICIAL GENERAL INTELLIGENCE (AGI)" - Smaller, aspirational:
- Takes up approximately 30% of the pyramid
- More ethereal, translucent, or dotted-line treatment
- Abstract representation of general intelligence: multiple connected domains, unified system
- Colors: Lighter, more transparent purples and silver tones
- Badge or marker indicating "FUTURE" or "THEORETICAL"
- Subtle upward arrow or reaching gesture
- Feeling: Aspirational, not yet achieved, future goal

VISUAL STYLE:
- Clean geometric pyramid with modern flat design
- Subtle shadow for depth
- Icons within the ANI layer should be minimal and recognizable
- Clear visual hierarchy: ANI is grounded and real, AGI is aspirational
- Background: Clean white or very light gray

Style: Modern tech infographic, professional documentation quality, no text (labels will be added separately), suitable for educational slide or chapter illustration.
```

---

### Image 01-05: Machine Learning Approaches Triptych

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-05-concept-ml-approaches.png` |
| **Type** | Concept |
| **Aspect Ratio** | 16:9 or 21:9 |
| **Placement** | After the "By Learning Approach" section header, around line 109, to visually represent ML, Deep Learning, and Reinforcement Learning |
| **Alt Text** | "Three-panel illustration showing Machine Learning (data patterns), Deep Learning (neural network layers), and Reinforcement Learning (agent-environment loop)" |

**Prompt:**
```
A triptych illustration showing three machine learning approaches side by side, designed for technical education.

PANEL 1 - MACHINE LEARNING (Left):
- Visual metaphor: Data points clustering into patterns
- Show scattered dots of various colors gradually organizing into clear clusters or a trend line
- A magnifying glass or lens revealing patterns in the data
- Simple, clean representation of pattern recognition
- Colors: Blues and teals, organized and analytical feeling
- Mood: Finding order in chaos, pattern discovery

PANEL 2 - DEEP LEARNING (Center):
- Visual metaphor: Neural network with multiple layers
- Stylized representation of interconnected nodes in distinct vertical layers
- Left side: Simple inputs (basic shapes or raw data dots)
- Middle: Multiple hidden layers with connections, showing increasing abstraction
- Right side: Refined output (a clear result or classification)
- Glowing connections between nodes to show information flow
- Colors: Deep blues to purples, showing depth and complexity
- Mood: Depth, layers of abstraction, transformation

PANEL 3 - REINFORCEMENT LEARNING (Right):
- Visual metaphor: Circular feedback loop
- An agent (could be abstract robot icon or geometric figure) in the center
- Circular arrows showing: Action → Environment → Reward/Feedback → Agent
- Environment could be represented as a game board, maze, or abstract space
- Positive feedback shown with warm colors (greens/golds), negative with cool
- Colors: Dynamic oranges and greens, showing trial and error
- Mood: Learning through interaction, iterative improvement

UNIFYING ELEMENTS:
- Consistent style across all three panels
- Subtle visual connection or flow between panels
- Each panel has its own distinct color accent but shares the overall palette
- Clean dividers or smooth transitions between sections

Style: Modern flat illustration with subtle gradients, tech documentation aesthetic, clean and educational, no text, white or very light gray background, high contrast and crisp edges.
```

---

### Image 01-06: AIOps Pipeline

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-06-flow-aiops-pipeline.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII AIOps diagram in section 1.6 (around line 264-279) |
| **Alt Text** | "AIOps pipeline showing data collection, AI analysis, and automated action phases with flowing data streams" |

**Prompt:**
```
A flowing pipeline diagram illustrating the AIOps (AI for IT Operations) workflow, designed for DevOps professionals.

THREE-STAGE HORIZONTAL FLOW (left to right):

STAGE 1 - "MONITORING / COLLECTION" (Left):
- Multiple data source icons feeding into a central collection point:
  - Server/compute metrics (stylized server rack icon)
  - Log files (document with lines icon)
  - Network traces (connected nodes icon)
  - Application metrics (chart/graph icon)
- Data streams visualized as flowing lines or particle streams
- Colors: Cool grays and blues, representing raw data
- Funnel or convergence point where streams merge
- Mood: Gathering, observing, collecting

STAGE 2 - "AI ANALYSIS" (Center, most prominent):
- Central brain or neural network processor
- Data streams enter and are transformed
- Visual representation of pattern detection:
  - Anomaly highlighted with a different color
  - Correlations shown as connecting lines
  - Root cause shown as a glowing node
- AI "magic" happening: raw data becoming insights
- Colors: Vibrant purples and electric blues, glowing effects
- Mood: Intelligence, processing, understanding

STAGE 3 - "ACTION" (Right):
- Two branching outputs from the AI brain:
  - Automated remediation path: Shows auto-healing, scaling, restarting (gear/wrench icon)
  - Human notification path: Alert to human operator (person icon with notification)
- Resolved incidents shown as checkmarks or healed systems
- Colors: Warm greens (success/automated) and oranges (human attention)
- Mood: Resolution, action, outcomes

FLOW ELEMENTS:
- Arrows or flowing lines connecting all stages
- Clear directionality from left to right
- Data transforms visually as it moves through the pipeline
- Subtle feedback loop from Action back to Monitoring (continuous improvement)

Style: Modern tech illustration, clean flow diagram aesthetic, DevOps-oriented iconography, professional and clear, no text labels, suitable for technical documentation, light background with subtle depth.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing data flowing through the pipeline, with the AI analysis stage pulsing as it processes, and actions being triggered on the right.

---

### Image 01-07: AI vs Human Strengths (80/20)

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-07-info-ai-human-strengths.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 4:3 or 1:1 |
| **Placement** | Replace or accompany the ASCII "80/20 Rule" diagram in section 1.8 (around line 448-466) |
| **Alt Text** | "Infographic showing complementary strengths of AI (pattern recognition, data processing) and humans (strategy, judgment, novel situations)" |

**Prompt:**
```
A balanced infographic illustration showing the complementary strengths of AI and human engineers, visualized as two interlocking or side-by-side columns.

LEFT COLUMN - "AI EXCELS AT" (80% of value, larger visual weight):
- Color theme: Tech blues and purples
- Icon representations for each strength:
  - Repetitive patterns: Grid of similar shapes being processed rapidly
  - Large data: Mountain or ocean of data points being analyzed
  - Boilerplate generation: Code blocks or document templates multiplying
  - Summarization: Large document condensing into key bullet points
  - Known patterns: Puzzle pieces matching to established solutions
- Visual metaphor: A powerful engine or processor
- Mood: Speed, scale, consistency, tireless

RIGHT COLUMN - "HUMANS EXCEL AT" (Critical 20%, smaller but emphasized):
- Color theme: Warm oranges and golds
- Icon representations for each strength:
  - Strategic decisions: Chess piece, roadmap, or compass
  - Business context: Building/organization icon with connections
  - Novel situations: Question mark transforming into lightbulb
  - Security/compliance judgment: Shield with checkmark
  - Final verification: Eye with magnifying glass, approval stamp
- Visual metaphor: A wise overseer or creative mind
- Mood: Wisdom, judgment, creativity, irreplaceable

CENTER CONNECTION:
- Where the two columns meet, show collaboration/synergy
- Handshake, puzzle pieces connecting, or Venn diagram overlap
- Glowing connection point showing "AI + Human = Superhuman"
- The combination is greater than either alone

VISUAL BALANCE:
- AI column visually larger (80%) but human column more prominent/golden
- Neither diminishes the other; they're complementary
- Equal importance despite different scale

Style: Modern infographic design, clean icons, balanced composition, professional color palette, no text labels (will be added separately), suitable for educational slide or documentation, light background.
```

---

### Image 01-08: Dockerfile Optimization Before/After

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-01-img-08-compare-dockerfile-optimization.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 1.7, Example 1 (around line 367) to visualize the optimization result |
| **Alt Text** | "Before and after comparison of Docker container optimization, showing a bloated container transforming into a slim, efficient one" |

**Prompt:**
```
A before/after comparison illustration showing Docker container optimization, designed for DevOps engineers.

LEFT SIDE - "BEFORE" (Unoptimized):
- A heavy, bloated Docker container representation
- Visualized as a large shipping container or box that's overstuffed
- Multiple redundant layers stacked messily
- Icons showing waste: duplicate packages, unnecessary files, cache debris
- Heavy anchor or weight attached, suggesting slowness
- Colors: Dull grays, warning yellows, bloated/unhealthy appearance
- Size indicator showing "LARGE" (e.g., 1.2GB visual representation)
- Mood: Inefficient, slow, problematic
- The whale/container looks tired or struggling

RIGHT SIDE - "AFTER" (Optimized):
- A slim, efficient Docker container representation
- Visualized as a sleek, minimal shipping container
- Clean, organized layers (multi-stage build visualization)
- Only essential components, clearly organized
- Lightweight feather or speed lines attached
- Colors: Clean blues, healthy greens, efficient appearance
- Size indicator showing "SMALL" (e.g., 150MB visual representation)
- Mood: Fast, efficient, professional
- The whale/container looks energetic and swift

CENTER TRANSFORMATION:
- Arrow or magic wand showing the transformation
- AI sparkles or neural network pattern suggesting AI-assisted optimization
- The optimization process visualized as refinement

VISUAL ELEMENTS:
- Docker whale logo stylized (or generic container whale)
- Layer visualization in both containers
- Clear size/weight difference
- Speed indicators (slow vs fast)

Style: Modern tech illustration, DevOps-oriented iconography, clear before/after contrast, professional and clean, no text labels, light background, suitable for technical documentation.
```

---

## Chapter 02: Understanding LLMs and Tokens

### Overview
- **Chapter Focus**: How LLMs work, tokenization, context windows, and cost economics
- **Total Images**: 10
- **Animation Candidates**: 3

---

### Image 02-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-01-header-llms-and-tokens.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "The Technology Powering Modern AI Assistants" |
| **Alt Text** | "Abstract visualization of large language models processing text into tokens, with neural pathways and text fragments flowing through a digital brain" |

**Prompt:**
```
A sophisticated wide-angle hero illustration representing Large Language Models and tokenization. The composition features an abstract digital brain or neural network structure in the center, with streams of text flowing into it from the left and transformed output emerging on the right.

Left side: Flowing streams of readable text fragments (could show code snippets, documentation, conversations) visualized as luminous particles or ribbons approaching the central structure.

Center: A stylized representation of a transformer model - could be visualized as interconnected crystalline structures, a complex node network, or an abstract "intelligence core" with multiple processing layers visible. Attention connections shown as glowing threads between different parts.

Right side: The same text transformed into organized token blocks - visualized as small, uniform glowing cubes or segments, neatly organized, representing the discretized nature of tokens.

Color palette: Deep electric blue (#1a73e8) for the neural core, purple gradients (#7c4dff) for attention connections, white and cyan for the flowing text particles, subtle orange accents (#ff6d00) for highlighted tokens.

Background: Gradient from dark navy (#0d1421) at edges to lighter center, creating depth and focus. Subtle grid or matrix pattern suggesting computation.

Style: Futuristic tech illustration, clean with elegant complexity, digital aesthetic with organic flow, professional and sophisticated, no readable text, suitable as a chapter hero image. The feeling should convey "text becoming understanding through computational intelligence."
```

---

### Image 02-02: Model Size Comparison

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-02-info-model-size-comparison.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII bar chart in section 2.1 (around line 65-76) |
| **Alt Text** | "Horizontal bar chart comparing AI model sizes from GPT-2 (1.5B parameters) to GPT-4 (1.7T parameters)" |

**Prompt:**
```
A clean, modern horizontal bar chart infographic comparing the parameter counts of major AI models, designed for technical education.

LAYOUT: Horizontal bars stacked vertically, representing model sizes with visual proportions

BARS (from top to bottom):
1. "GPT-2 (2019)" - Very small bar, barely visible - 1.5 Billion parameters
   - Color: Muted gray-blue, representing "old generation"

2. "GPT-3 (2020)" - Medium-large bar - 175 Billion parameters
   - Color: Medium blue, showing significant jump

3. "Claude 4.5 (2025)" - Large bar - ~200 Billion+ (estimated)
   - Color: Anthropic brand-inspired warm purple/orange gradient

4. "GPT-4 (2023)" - Massive bar, extending further - ~1.7 Trillion (rumored)
   - Color: Vibrant tech blue with glow effect

VISUAL ELEMENTS:
- Each bar should have subtle depth/3D effect
- Parameter counts represented both by bar length AND subtle node/neuron pattern density
- Scale indicator on the bottom showing billions/trillions
- Small brain icon or neural network snippet next to each bar
- Size increase arrows or indicators between bars showing the exponential growth

REFERENCE POINT (optional):
- Small human brain icon with "~86 billion neurons" label as a reference point

Style: Modern data visualization, clean infographic aesthetic, minimal decorative elements, focus on clear comparison, subtle gradients for depth, professional color palette, light background with subtle grid lines for scale reference. No excessive text - labels will be added separately.
```

---

### Image 02-03: LLM Training Pipeline

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-03-flow-llm-training-pipeline.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | Replace or accompany the ASCII training pipeline in section 2.2 (around line 88-126) |
| **Alt Text** | "Four-stage LLM training pipeline showing data collection, preprocessing, training, and fine-tuning phases" |

**Prompt:**
```
A vertical or horizontal flow diagram illustrating the four stages of LLM training, designed for DevOps engineers.

STAGE 1 - DATA COLLECTION (Top/Left):
- Visual: Multiple source icons flowing into a central funnel or collector
  - Book/document icon (books, papers)
  - Globe/web icon (websites, Common Crawl)
  - Code bracket icon (GitHub repositories)
  - Chat bubble icon (forums, Q&A sites)
- Data streams visualized as flowing particles or rivers
- Colors: Cool grays and light blues (raw data)
- Mood: Gathering, diversity of sources

STAGE 2 - PREPROCESSING (Second):
- Visual: A filter or refinery transformation
  - Raw data entering as chaotic streams
  - Cleaning process shown as filtering/sifting
  - Output as clean, organized text blocks becoming tokens
- Icons: Filter funnel, cleaning brush, duplicate removal
- Colors: Transition from gray to cleaner blues
- Mood: Purification, organization

STAGE 3 - TRAINING (Third, most prominent):
- Visual: The neural network "learning" process
  - Input text: "The DevOps engineer deployed the ___"
  - Model making predictions, arrows pointing to next word
  - Feedback loop showing "compare → adjust weights"
  - Multiple iterations visualized as cycling process
- Icons: Brain/neural network, circular arrows (iterations), weight/scale
- Colors: Electric blues and purples (computation)
- Mood: Learning, iteration, intelligence emerging

STAGE 4 - FINE-TUNING / RLHF (Bottom/Right):
- Visual: Human-AI collaboration
  - Human figure providing feedback
  - Thumbs up/down or rating system
  - Model being refined/polished
  - Output showing "helpful, harmless, honest" characteristics
- Icons: Human silhouette, rating stars, checkmark shield
- Colors: Warm oranges and greens (refinement, approval)
- Mood: Refinement, alignment, safety

CONNECTIONS:
- Flowing arrows between each stage
- Each stage visually distinct but part of continuous pipeline
- Progress indicator showing transformation from raw data to intelligent model

Style: Modern tech flow diagram, clean and educational, distinct stages with clear visual hierarchy, professional documentation quality, minimal text, suitable for technical slides.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing data flowing through each stage, with the training stage showing the iterative learning loop cycling.

---

### Image 02-04: Transformer Architecture Simplified

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-04-diagram-transformer-architecture.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 4:3 or 3:4 (vertical) |
| **Placement** | Replace or accompany the ASCII transformer diagram in section 2.2 (around line 133-177) |
| **Alt Text** | "Simplified transformer architecture showing tokenization, embedding, attention mechanism, and output layers" |

**Prompt:**
```
A simplified vertical flow diagram showing the transformer architecture, designed for educational understanding.

FLOW (top to bottom):

INPUT (Top):
- Text input shown as: "kubectl get pods -n"
- Clean text box or speech bubble style

TOKENIZATION LAYER:
- Text breaking into discrete token blocks
- Visualized as text splitting into separate glowing segments
- ["kubectl"] ["get"] ["pods"] ["-"] ["n"]
- Color: Light cyan/white blocks

EMBEDDING LAYER:
- Tokens transforming into dense vectors
- Each token block converting to a column of numbers or a small heatmap
- Visualized as tokens "deepening" into multi-dimensional representations
- Color: Blue gradients showing depth

ATTENTION MECHANISM (Most prominent, highlighted):
- The "magic" layer - emphasized with glow effect
- Multiple tokens connected by weighted lines
- Some connections thick (high attention), others thin
- Shows "kubectl" connecting strongly to "pods"
- "-n" connecting to concept of "namespace"
- Visualized as a network of relationships
- Color: Purple/magenta with glowing connections
- Label area: "Which words relate to which?"

FEED FORWARD LAYERS:
- Processing/transformation represented as layered boxes
- Information flowing through and being transformed
- Color: Deeper blues

OUTPUT LAYER:
- Probability distribution visualization
- Multiple possible next tokens with probability bars:
  - "production" : 0.35 (longest bar)
  - "default" : 0.28
  - "kube-system" : 0.22
- Shows selection of highest probability
- Color: Green/teal for selected output

FINAL OUTPUT:
- Selected token "production" highlighted
- Color: Warm orange/gold (success)

Style: Technical but accessible diagram, clean lines, clear layer separation, attention layer emphasized, modern tech aesthetic, educational quality, minimal text (labels added separately), light background with subtle depth indicators.
```

📐 **RECOMMEND**: Consider also creating a Mermaid or draw.io version for precise technical accuracy. This AI-generated version would be for conceptual understanding.

---

### Image 02-05: Attention Mechanism Visualization

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-05-diagram-attention-weights.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the attention weights example in section 2.2 (around line 183-201) |
| **Alt Text** | "Visualization of attention weights showing how 'crashed' relates to other words in the sentence 'The server crashed because the database connection pool was exhausted'" |

**Prompt:**
```
A horizontal attention weight visualization showing how words in a sentence relate to each other, specifically how "crashed" attends to other words.

LAYOUT:
- Sentence displayed horizontally at the top: "The server crashed because the database connection pool was exhausted"
- Each word in its own subtle box or node
- The target word "crashed" highlighted (glowing border, slightly larger)

ATTENTION CONNECTIONS:
- Lines or arcs connecting "crashed" to every other word
- Line thickness/opacity represents attention weight:
  - "server" → thick, bright connection (0.75) - labeled "subject"
  - "crashed" → self-connection (1.00)
  - "because" → medium connection (0.30) - indicates causation
  - "database" → medium-thick connection (0.55)
  - "connection" → medium connection (0.45)
  - "pool" → thick connection (0.65)
  - "exhausted" → very thick, brightest connection (0.90) - labeled "root cause"
  - "The", "the", "was" → very thin, faint connections (0.01-0.03)

VISUAL STYLE:
- Connections as glowing beams or ribbons
- High-attention connections in warm colors (orange/yellow)
- Low-attention connections in cool, faint colors (gray/light blue)
- "Exhausted" and "server" should stand out as key related words

OPTIONAL ELEMENTS:
- Small bar chart on the right showing attention weights as horizontal bars
- Color gradient legend from low attention (cool) to high attention (warm)

INSIGHT CALLOUT:
- Visual indicator showing: "The model learns: 'crashed' relates to 'server' and 'exhausted'"

Style: Clean data visualization, technical but beautiful, attention connections as the hero element, dark or light background (dark might show connections better), educational quality, minimal text.
```

---

### Image 02-06: Tokenization Concept

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-06-concept-tokenization.png` |
| **Type** | Concept |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 2.3 header "Understanding Tokens" (around line 207-223) |
| **Alt Text** | "Illustration showing how words are broken into tokens, with examples like 'Kubernetes' becoming 'Kub' + 'ernetes'" |

**Prompt:**
```
An educational illustration showing how text is broken down into tokens, with multiple examples.

LAYOUT:
Three horizontal example rows, each showing word → token breakdown

EXAMPLE 1 - Simple word:
- "Hello" shown as a complete word in a box
- Arrow pointing to single token block ["Hello"]
- Small indicator: "1 token"
- Color: Green (simple case)

EXAMPLE 2 - Technical term:
- "Kubernetes" shown as a word
- Arrow pointing to it splitting into: ["Kub"] ["ernetes"]
- Animated crack or split effect between the tokens
- Small indicator: "2 tokens"
- Color: Orange (important DevOps term)

EXAMPLE 3 - Complex command:
- "#!/bin/bash" shown as text
- Arrow pointing to multiple tokens: ["#!"] ["/"] ["bin"] ["/"] ["bash"]
- Shows how special characters become separate tokens
- Small indicator: "5 tokens"
- Color: Purple (code/special characters)

EXAMPLE 4 (optional) - IP Address:
- "192.168.1.1" shown as text
- Arrow pointing to: ["192"] ["."] ["168"] ["."] ["1"] ["."] ["1"]
- Small indicator: "7 tokens"
- Color: Blue (numbers/punctuation)

VISUAL METAPHOR:
- Could include a small "word processor" or "tokenizer machine" visual
- Words go in as whole, come out as puzzle-piece-like segments
- Each token as a distinct block/tile with subtle glow

BOTTOM INSIGHT:
- Visual showing the spectrum: Character-based ↔ Token-based ↔ Word-based
- Token-based highlighted as "best of both worlds"

Style: Clean educational illustration, clear before/after transformation, tokens as distinct block elements, professional documentation quality, light background, minimal but clear labels.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing words smoothly splitting into their component tokens.

---

### Image 02-07: Context Window Visualization

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-07-diagram-context-window.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 4:3 |
| **Placement** | Replace or accompany the context window diagram in section 2.4 (around line 343-363) |
| **Alt Text** | "Diagram showing context window as the sum of input tokens (prompt, system instructions, context) plus output tokens (response)" |

**Prompt:**
```
A clear diagram illustrating the concept of context window as a container that must fit both input and output.

VISUAL METAPHOR: A large container or bucket with a clear capacity limit

CONTAINER (Context Window):
- Large rectangular or bucket-shaped container
- Clear maximum capacity line at top
- Label: "Context Window Limit" or capacity indicator (e.g., "200K tokens")

INSIDE THE CONTAINER:

BOTTOM SECTION - INPUT (larger portion, ~60-70%):
- Stacked layers representing different input components:
  - Layer 1: "Your Question/Request" - document icon
  - Layer 2: "Code You Paste" - code bracket icon
  - Layer 3: "System Instructions" - gear icon
  - Layer 4: "Conversation History" - chat bubble icon
- Each layer a different shade of blue
- All labeled as "INPUT TOKENS"

TOP SECTION - OUTPUT (remaining space, ~30-40%):
- Single block representing the model's response
- Color: Green/teal
- Label: "MODEL OUTPUT"
- Shows this must also fit within the container

VISUAL INDICATORS:
- Plus sign between input and output sections
- Equals sign pointing to "Must fit within Context Window"
- Warning indicator if approaching limit
- Small overflow indicator showing what happens if you exceed (truncation)

SIDE ANNOTATION:
- Small meter or gauge showing "used/available" tokens
- Example calculation: "Input: 150K + Output: 30K = 180K / 200K available"

Style: Clean infographic style, clear visual metaphor of capacity/containment, professional color palette, educational quality, minimal text (will add labels), light background.
```

---

### Image 02-08: Token Economics and Pricing

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-08-info-token-economics.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 4:3 or 1:1 |
| **Placement** | After section 2.5 header "Token Economics" (around line 452-478) |
| **Alt Text** | "Infographic showing how LLM pricing works: input tokens (cheaper) plus output tokens (more expensive) equals total cost" |

**Prompt:**
```
An infographic illustrating LLM pricing economics in a clear, visual way.

LAYOUT: Visual equation or flow showing cost calculation

LEFT SIDE - INPUT TOKENS:
- Stack of document/text pages flowing into the model
- Icons: Documents, code files, conversation bubbles
- Label: "INPUT TOKENS"
- Subtitle: "What you send"
- Small coin/dollar icons (fewer, indicating "cheaper")
- Visual: Smaller price tag
- Color: Cool blues (reading/receiving)

CENTER - THE MODEL:
- Brain or processing unit icon
- Arrows from input entering, arrows to output leaving
- Subtle "processing" visualization (gears, neural pattern)
- Plus sign or addition symbol

RIGHT SIDE - OUTPUT TOKENS:
- Generated text/code flowing out
- Icons: Response documents, generated code
- Label: "OUTPUT TOKENS"
- Subtitle: "What AI generates"
- More coin/dollar icons (indicating "more expensive")
- Visual: Larger price tag
- Color: Warm greens/teals (generation/creation)

BOTTOM - TOTAL COST:
- Equals sign leading to total
- Calculator or receipt visual
- Formula: (Input × Input Price) + (Output × Output Price) = Total
- Example: "1000 × $0.003 + 400 × $0.015 = $0.009"

SIDE PANEL - QUICK TIPS:
- Icon grid showing optimization tips:
  - Minimize context (trim icon)
  - Use appropriate model (tier icon)
  - Cache responses (save icon)
  - Batch requests (bundle icon)

Style: Modern infographic, financial/economic visual language, clear equation layout, professional color palette with money-related colors (greens, golds), educational quality, minimal text.
```

---

### Image 02-09: Text Generation Process

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-09-flow-text-generation.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII text generation diagram in section 2.6 (around line 722-755) |
| **Alt Text** | "Sequential flow showing how LLMs generate text one token at a time through probability prediction and selection" |

**Prompt:**
```
A horizontal flow diagram showing the sequential token-by-token generation process of LLMs.

FLOW (left to right, with iterative loop):

STEP 1 - INPUT:
- Starting prompt in a text box: "Write a bash script to"
- Tokens shown as segments: ["Write"] [" a"] [" bash"] [" script"] [" to"]
- Color: Blue (input)

STEP 2 - PROBABILITY PREDICTION:
- Model processing (small brain/network icon)
- Output: Probability distribution visualization
- Multiple candidate tokens as vertical bars:
  - " backup" : 0.15 (tallest)
  - " check" : 0.12
  - " monitor" : 0.10
  - " list" : 0.08
  - " delete" : 0.05
  - "..." : (more options fading)
- Color: Purple gradients for probability bars

STEP 3 - TOKEN SELECTION:
- One token being "selected" or highlighted
- Selection mechanism shown (could be dice for sampling, or arrow for greedy)
- Selected: " backup" with checkmark or highlight
- Color: Green/gold for selected token

STEP 4 - APPEND AND REPEAT:
- New context shown: "Write a bash script to backup"
- The new token joins the sequence
- Arrow looping back to Step 2 (next prediction cycle)
- Small iteration counter or "repeat until done" indicator

STEP 5 - TERMINATION CONDITIONS (side panel):
- Icons showing when generation stops:
  - End token (stop sign)
  - Max length reached (ruler)
  - Stop sequence (specific text)

VISUAL FLOW:
- Clear left-to-right progression
- Iterative loop emphasized with curved arrow
- Each step visually distinct
- Growing output shown progressively (like building blocks)

Style: Clean flow diagram, sequential process visualization, professional documentation quality, emphasis on the iterative/autoregressive nature, minimal text, light background.
```

**🎬 ANIMATION CANDIDATE**: This would be excellent as an animated GIF showing the sequential token generation, with each token being predicted and appended in real-time.

---

### Image 02-10: Temperature Effect on Generation

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-02-img-10-compare-temperature-effect.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After the temperature explanation in section 2.6 (around line 759-788) |
| **Alt Text** | "Three-panel comparison showing how temperature affects token selection: deterministic at 0.0, balanced at 0.7, creative/random at 1.5" |

**Prompt:**
```
A three-panel comparison illustration showing how the temperature parameter affects LLM output randomness.

THREE VERTICAL PANELS (left to right):

PANEL 1 - TEMPERATURE 0.0 (Deterministic):
- Visual metaphor: Straight, rigid path; laser-focused beam
- Probability bars where top option dominates:
  - "backup" : ████████████████████ (always selected)
  - "check"  : ████████████░░░░░░░░
  - "monitor": ████████░░░░░░░░░░░░
- Arrow always pointing to same token
- Icon: Precise target/bullseye, rigid robot
- Color: Cool, precise blues and grays
- Label: "Deterministic"
- Use case icons: Code generation, configs

PANEL 2 - TEMPERATURE 0.7 (Balanced):
- Visual metaphor: Slightly curved paths; balanced scale
- Probability bars more evenly distributed:
  - "backup" : ██████████████░░░░░░ (usually selected)
  - "check"  : ██████████████░░░░░░ (sometimes)
  - "monitor": ████████████░░░░░░░░ (occasionally)
- Arrows showing some variability
- Icon: Balanced scale, flexible human
- Color: Mixed blues and purples
- Label: "Balanced"
- Use case icons: General assistance, explanations

PANEL 3 - TEMPERATURE 1.5 (Creative):
- Visual metaphor: Multiple diverging paths; explosion of options
- Probability bars nearly equal:
  - "backup" : ████████████░░░░░░░░
  - "check"  : ████████████░░░░░░░░
  - "monitor": ████████████░░░░░░░░
  - "analyze": ██████████░░░░░░░░░░
  - "encrypt": ████████░░░░░░░░░░░░
- Arrows pointing in multiple directions
- Icon: Explosion/starburst, creative artist
- Color: Warm oranges and reds, chaotic energy
- Label: "Creative/Random"
- Use case icons: Brainstorming, creative writing

VISUAL METAPHORS:
- Panel 1: Frozen/crystalline aesthetic
- Panel 2: Fluid/water-like aesthetic
- Panel 3: Fire/energy aesthetic

BOTTOM SCALE:
- Temperature gradient bar from 0.0 to 2.0
- Showing: Focused ← → Diverse

Style: Clean comparison layout, clear visual metaphors for randomness, consistent structure across panels, professional color coding, educational quality, minimal text.
```

---

## Chapter 03: The Art of Prompting

### Overview
- **Chapter Focus**: CRAFT framework, prompting techniques, DevOps-specific patterns
- **Total Images**: 8
- **Animation Candidates**: 1

---

### Image 03-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-01-header-art-of-prompting.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Mastering the Skill of Communicating with AI" |
| **Alt Text** | "Abstract illustration of a human communicating with AI through structured prompts, showing words transforming into code and solutions" |

**Prompt:**
```
A creative wide-angle hero illustration representing the art of prompting - the skill of communicating effectively with AI.

CENTRAL CONCEPT:
A stylized dialogue between human intelligence and artificial intelligence, visualized as two complementary forms meeting in the middle.

LEFT SIDE - HUMAN INPUT:
- Abstract representation of human thought/intention
- Structured text blocks floating from a person silhouette or thought bubble
- Text elements organized in a clear, structured format (like a template)
- Could show keywords like "Context", "Role", "Action" as floating elements
- Color: Warm tones (oranges, golds) representing human creativity

CENTER - THE PROMPT:
- A beautifully crafted message or document
- Structured with clear sections, bullet points, formatting
- Could be visualized as a scroll, blueprint, or command interface
- Glowing connection point where human intent meets AI understanding
- Shows transformation from rough ideas to structured communication

RIGHT SIDE - AI RESPONSE:
- AI system receiving the structured input
- Output emerging as perfect code blocks, diagrams, solutions
- DevOps outputs: Kubernetes manifests, Terraform code, scripts
- Color: Cool blues and purples representing AI precision

VISUAL METAPHOR OPTIONS:
- Conductor's baton directing an orchestra (structured direction → beautiful output)
- Architect's blueprint being constructed into reality
- Key fitting perfectly into a lock (right prompt → right response)

DECORATIVE ELEMENTS:
- Floating syntax elements: curly braces, brackets, markdown symbols
- Code snippets visible but not readable
- Stars or particles showing the "magic" of good communication

Style: Modern tech illustration with artistic flair, clean but creative, professional yet inspiring, conveying "prompting is both art and science," no readable text, suitable as chapter hero image.
```

---

### Image 03-02: Anatomy of a Prompt

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-02-diagram-prompt-anatomy.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 4:3 |
| **Placement** | Replace or accompany the ASCII diagram in section 3.1 (around line 56-89) |
| **Alt Text** | "Layered diagram showing the three components of a prompt: system prompt, user prompt, and context, combining to produce an AI response" |

**Prompt:**
```
A clean layered diagram showing the anatomy of a prompt, with three stacked components combining into a response.

STRUCTURE (vertical stack):

LAYER 1 - SYSTEM PROMPT (Top):
- Rectangle with distinct border/style
- Icon: Gear or settings symbol
- Label area: "SYSTEM PROMPT"
- Subtitle: "Sets AI's role, personality, constraints"
- Example snippet space showing configuration-like text
- Color: Purple/magenta tones (configuration/setup)
- Represents the "behind the scenes" setup

LAYER 2 - USER PROMPT (Middle):
- Rectangle, slightly larger/more prominent
- Icon: User silhouette or speech bubble
- Label area: "USER PROMPT"
- Subtitle: "Your actual question or request"
- Example snippet space showing a question
- Color: Blue tones (user input)
- Represents the direct request

LAYER 3 - CONTEXT (Bottom, optional indicator):
- Rectangle with dashed/dotted border (indicating optional)
- Icon: Document stack or code brackets
- Label area: "CONTEXT (Optional)"
- Subtitle: "Additional information: code, logs, configs"
- Example snippet space showing code/data
- Color: Green/teal tones (supporting data)
- Represents additional context

COMBINATION VISUAL:
- Plus signs or arrows showing the layers combining
- Downward arrow to output section

OUTPUT SECTION:
- Distinct area showing "AI RESPONSE"
- Glowing or highlighted to show it's the result
- Icon: Lightbulb or output document
- Color: Gold/orange (result/success)

VISUAL STYLE:
- Clear layer separation with subtle 3D stacking effect
- Each layer slightly offset to show stacking
- Connecting lines showing data flow
- Clean, technical documentation aesthetic

Style: Modern technical diagram, clean layers, clear visual hierarchy, professional documentation quality, minimal text (labels added separately), light background with subtle depth.
```

---

### Image 03-03: CRAFT Framework

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-03-diagram-craft-framework.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 or 1:1 |
| **Placement** | Replace or accompany the ASCII CRAFT diagram in section 3.2 (around line 114-140) |
| **Alt Text** | "The CRAFT framework diagram showing five components: Context, Role, Action, Format, and Target arranged as interconnected elements" |

**Prompt:**
```
A memorable visual diagram representing the CRAFT framework for effective prompting, designed to be the key takeaway image of this chapter.

LAYOUT OPTIONS:
Option A - Pentagon/Star arrangement (each element a point)
Option B - Vertical pillars (five columns)
Option C - Interlocking puzzle pieces
Option D - Ascending steps/staircase

FIVE ELEMENTS (each with distinct visual identity):

C - CONTEXT (First):
- Icon: Environment/globe/compass
- Visual: Surrounding frame or foundation
- Represents: "Provide relevant background information"
- Sub-text area: "Environment, versions, constraints"
- Color: Blue (#4285f4) - foundation/information

R - ROLE (Second):
- Icon: Mask/persona/expert badge
- Visual: Character or avatar representation
- Represents: "Define who the AI should be"
- Sub-text area: "Expert level, perspective, focus"
- Color: Purple (#7c4dff) - identity/persona

A - ACTION (Third, central/prominent):
- Icon: Play button/arrow/gear in motion
- Visual: Dynamic, action-oriented element
- Represents: "Specify exactly what you want done"
- Sub-text area: "Clear, actionable request"
- Color: Orange (#ff6d00) - action/energy

F - FORMAT (Fourth):
- Icon: Document template/grid/list
- Visual: Structured output representation
- Represents: "Describe desired output format"
- Sub-text area: "Code, list, table, step-by-step"
- Color: Teal (#00bcd4) - structure/organization

T - TARGET (Fifth):
- Icon: Bullseye/checkmark/goal flag
- Visual: Success/completion indicator
- Represents: "Define success criteria"
- Sub-text area: "What does 'done' look like?"
- Color: Green (#4caf50) - success/goal

CENTRAL ELEMENT:
- "CRAFT" text or logo could be in center
- Shows all elements connecting to create perfect prompt
- Glowing or highlighted to show synergy

VISUAL FLOW:
- Elements should connect or flow into each other
- Shows that all five work together
- Could have arrows or pathways connecting them

Style: Modern, memorable infographic, each element distinct but part of whole, professional color palette, clean and easy to remember, suitable for presentation slides and documentation, minimal text.
```

---

### Image 03-04: Prompting Techniques Comparison

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-04-compare-prompting-techniques.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 3.3 header "Prompting Techniques" (before the individual technique sections, around line 182) |
| **Alt Text** | "Visual comparison of prompting techniques: zero-shot, one-shot, few-shot, and chain-of-thought, showing increasing complexity and examples" |

**Prompt:**
```
A horizontal comparison showing four main prompting techniques, each with a visual representation of its approach.

FOUR COLUMNS (left to right, increasing complexity):

COLUMN 1 - ZERO-SHOT:
- Icon: Single arrow pointing directly to output
- Visual: Simple direct path from question to answer
- Representation: One input box → One output box
- No examples shown
- Label: "Direct question, no examples"
- Color: Simple blue
- Best for: "Simple, unambiguous tasks"

COLUMN 2 - ONE-SHOT:
- Icon: Single example block before the question
- Visual: Example → Pattern learned → Applied
- Representation: Example box + Input box → Output box
- One example shown guiding format
- Label: "One example guides format"
- Color: Blue with purple accent
- Best for: "Consistent formatting, style"

COLUMN 3 - FEW-SHOT:
- Icon: Multiple example blocks (2-5)
- Visual: Pattern recognition from multiple examples
- Representation: Multiple example boxes + Input → Output
- Multiple examples showing pattern
- Label: "Multiple examples establish pattern"
- Color: Purple gradients
- Best for: "Complex patterns, domain-specific"

COLUMN 4 - CHAIN-OF-THOUGHT:
- Icon: Stepped progression with reasoning bubbles
- Visual: Input → Step 1 → Step 2 → Step 3 → Output
- Representation: Sequential reasoning process
- Thought bubbles showing "thinking" at each step
- Label: "Step-by-step reasoning"
- Color: Orange/warm tones
- Best for: "Complex problems, debugging"

VISUAL ELEMENTS:
- Arrow or progression indicator from simple (left) to complex (right)
- Each technique clearly bounded in its own section
- Subtle complexity scale at bottom
- Icons representing input/output/examples consistently

Style: Clean comparison layout, educational poster style, clear visual hierarchy, each technique visually distinct, professional documentation quality, minimal text.
```

---

### Image 03-05: Chain-of-Thought Visualization

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-05-flow-chain-of-thought.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After the Chain-of-Thought explanation in section 3.3, Technique 4 (around line 330) |
| **Alt Text** | "Flow diagram showing chain-of-thought prompting with a problem flowing through multiple reasoning steps to reach a solution" |

**Prompt:**
```
A horizontal flow diagram illustrating the chain-of-thought prompting technique, showing how complex problems are broken into reasoning steps.

FLOW (left to right):

START - PROBLEM INPUT:
- Box containing a complex problem statement
- Icon: Question mark or problem symbol
- Label: "Complex Problem"
- Example: High latency debugging scenario
- Color: Red/orange (problem state)

STEP 1 - IDENTIFY:
- Thought bubble or reasoning box
- Shows: "First, identify where time is spent"
- Icon: Magnifying glass or search
- Sub-steps visible within
- Connecting arrow with "Let me think..."
- Color: Light blue

STEP 2 - ANALYZE:
- Thought bubble connecting from Step 1
- Shows: "Check database performance"
- Icon: Database or analysis chart
- Reasoning visible: queries, connections, locks
- Color: Medium blue

STEP 3 - INVESTIGATE:
- Thought bubble connecting from Step 2
- Shows: "Verify cache effectiveness"
- Icon: Cache/memory symbol
- Reasoning: hit rates, expiration, network
- Color: Purple

STEP 4 - SYNTHESIZE:
- Thought bubble connecting from Step 3
- Shows: "Combine findings"
- Icon: Puzzle pieces coming together
- Connects multiple insights
- Color: Teal

END - SOLUTION:
- Final answer box
- Shows structured solution with clear steps
- Icon: Lightbulb or checkmark
- Label: "Reasoned Solution"
- Color: Green (solved state)

VISUAL ELEMENTS:
- Curved arrows connecting each step
- Each thought bubble shows internal reasoning
- "Reasoning visible" aspect emphasized
- Progression from uncertainty to clarity
- Small indicators showing each step builds on previous

ANNOTATION:
- Small callout: "Each step builds on previous reasoning"
- Visual showing AI's "thinking" is exposed

Style: Clean flow diagram, thought-bubble aesthetic, shows reasoning process clearly, professional but approachable, educational quality, emphasis on the step-by-step nature.
```

---

### Image 03-06: Prompt Quality Spectrum

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-06-info-prompt-quality-spectrum.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the quality spectrum diagram in section 3.1 (around line 93-106) |
| **Alt Text** | "Spectrum showing prompt quality from poor (vague, single word) to excellent (detailed, structured with context), with examples at each level" |

**Prompt:**
```
A horizontal spectrum/gradient infographic showing the progression from poor prompts to excellent prompts.

LAYOUT: Horizontal bar with markers at four quality levels

SPECTRUM BAR:
- Left side: Red/warning color (poor)
- Right side: Green/success color (excellent)
- Gradient transition across the bar
- Clear markers at each quality level

LEVEL 1 - POOR (Far left):
- Position: 0-20% of spectrum
- Example card: "fix this"
- Visual: Sad face or X mark
- Indicator: Red zone
- Small description: "Vague, no context"
- Icon: Broken or unclear symbol

LEVEL 2 - BASIC (Second):
- Position: 20-40% of spectrum
- Example card: "my script is broken"
- Visual: Neutral face
- Indicator: Orange zone
- Small description: "Slightly better, still unclear"
- Icon: Partial symbol

LEVEL 3 - GOOD (Third):
- Position: 40-70% of spectrum
- Example card: "This bash script fails with error code 1"
- Visual: Slight smile
- Indicator: Yellow-green zone
- Small description: "Has context, could be clearer"
- Icon: Good but incomplete symbol

LEVEL 4 - EXCELLENT (Far right):
- Position: 70-100% of spectrum
- Example card showing structured prompt with:
  - Clear description
  - Environment (Ubuntu 22.04)
  - Code and error provided
  - Specific question
- Visual: Happy face or checkmark
- Indicator: Bright green zone
- Small description: "Detailed, structured, complete"
- Icon: Perfect/complete symbol

RESULT INDICATORS:
- Below each level, show typical output quality:
  - Poor prompt → "Vague, unhelpful response"
  - Excellent prompt → "Precise, actionable solution"

VISUAL ELEMENTS:
- Arrow showing progression direction
- "Quality improves →" label
- Example prompts in card/bubble format
- Clear color coding

Style: Modern infographic, clear progression, actionable comparison, professional documentation style, emphasizes the direct relationship between prompt quality and output quality.
```

---

### Image 03-07: Prompt Chaining

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-07-flow-prompt-chaining.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Before or after section 3.5 "Prompt Chaining" (around line 537-563) |
| **Alt Text** | "Flow diagram showing four connected prompts: Architecture Design → GitHub Actions Workflow → Kubernetes Manifests → Security Review, with outputs feeding into subsequent prompts" |

**Prompt:**
```
A horizontal flow diagram showing how complex tasks are broken into connected prompts, with each output feeding into the next prompt.

CHAIN OF FOUR PROMPTS (left to right):

PROMPT 1 - ARCHITECTURE DESIGN:
- Box with "Prompt 1" label
- Title: "Architecture Design"
- Input: Project requirements
- Icon: Blueprint or architecture diagram
- Output bubble: "Architecture diagram + Components list"
- Color: Blue
- Shows this is the starting point

CONNECTING ARROW 1→2:
- Arrow from Prompt 1 output to Prompt 2 input
- Label: "Output feeds into..."
- Shows data transfer visualization

PROMPT 2 - GITHUB ACTIONS:
- Box with "Prompt 2" label
- Title: "GitHub Actions Workflow"
- Input: Uses architecture from Prompt 1
- Icon: GitHub/CI-CD symbol
- Output bubble: "Workflow YAML file"
- Color: Purple
- Shows dependency on previous output

CONNECTING ARROW 2→3:
- Arrow from Prompt 2 output to Prompt 3 input
- Shows continuous flow

PROMPT 3 - KUBERNETES MANIFESTS:
- Box with "Prompt 3" label
- Title: "K8s Manifests"
- Input: Uses workflow from Prompt 2
- Icon: Kubernetes wheel
- Output bubble: "Deployment manifests"
- Color: Teal
- Shows building on previous

CONNECTING ARROW 3→4:
- Arrow feeding all outputs to final review

PROMPT 4 - SECURITY REVIEW:
- Box with "Prompt 4" label
- Title: "Security Review"
- Input: ALL previous outputs combined
- Icon: Shield or security symbol
- Output bubble: "Validated, secure solution"
- Color: Green (final/validated)
- Shows synthesis of all work

VISUAL ELEMENTS:
- Each prompt clearly bounded
- Output bubbles distinct from input
- Arrows showing data flow direction
- Accumulating output visualization (each step adds to the whole)
- Small icons representing output artifacts

ANNOTATION:
- "Break complex tasks into connected prompts"
- "Each output becomes input for the next"

Style: Clean flow diagram, clear connections, shows the pipeline nature, professional documentation quality, emphasizes the iterative building process.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing each prompt executing in sequence, with outputs flowing to the next stage.

---

### Image 03-08: Common Prompting Mistakes

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-03-img-08-info-prompting-mistakes.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 4:3 or 3:4 (vertical) |
| **Placement** | After section 3.6 header "Common Prompting Mistakes" (around line 651) |
| **Alt Text** | "Infographic showing five common prompting mistakes with X marks and their corrections with checkmarks" |

**Prompt:**
```
A vertical infographic listing five common prompting mistakes with visual before/after or wrong/right comparisons.

LAYOUT: Five mistake sections stacked vertically, each with wrong and right versions

HEADER:
- Title area: "Common Prompting Mistakes"
- Warning icon or caution symbol
- Professional but attention-getting design

MISTAKE 1 - TOO VAGUE:
- Left side (Wrong - X mark, red):
  - Example: "How do I deploy?"
  - Icon: Fog or question marks
- Right side (Correct - Checkmark, green):
  - Example: "How do I deploy a Dockerized Python app to AWS EKS..."
  - Icon: Clear target
- Brief label: "Be Specific"

MISTAKE 2 - NO CONTEXT:
- Left side (Wrong):
  - Example: "Why is my pod crashing?"
  - Icon: Empty box
- Right side (Correct):
  - Example: Shows environment, logs, describe output included
  - Icon: Filled information box
- Brief label: "Provide Environment Details"

MISTAKE 3 - TOO MUCH AT ONCE:
- Left side (Wrong):
  - Example: "Create complete CI/CD with everything..."
  - Icon: Overflowing/chaotic
- Right side (Correct):
  - Example: "Let's build step by step. First..."
  - Icon: Organized steps
- Brief label: "Break Into Steps"

MISTAKE 4 - NO FORMAT SPECIFIED:
- Left side (Wrong):
  - Example: "List monitoring tools"
  - Icon: Unstructured blob
- Right side (Correct):
  - Example: "List in table with columns: Tool, Pros, Cons..."
  - Icon: Structured table
- Brief label: "Specify Output Format"

MISTAKE 5 - IGNORING LIMITATIONS:
- Left side (Wrong):
  - Example: "What's the current price of..."
  - Icon: Clock with question mark
- Right side (Correct):
  - Example: "What was the pricing as of your knowledge cutoff..."
  - Icon: Calendar with checkmark
- Brief label: "Acknowledge AI Limitations"

VISUAL STYLE:
- Clear X and checkmark icons
- Red/green color coding for wrong/right
- Each mistake in its own bounded section
- Consistent layout for easy scanning
- Brief, memorable lessons

Style: Warning-style infographic, clear dos and don'ts, professional but direct, easy to remember, suitable for quick reference, educational documentation quality.
```

---

## Chapter 04: AI Models Landscape

### Overview
- **Chapter Focus**: AI providers, model comparison, proprietary vs open source, hosting options
- **Total Images**: 8
- **Animation Candidates**: 1

---

### Image 04-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-01-header-ai-models-landscape.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Navigating the World of AI Models and Providers" |
| **Alt Text** | "Panoramic view of the AI ecosystem showing various AI companies and their models as a interconnected landscape with different terrains representing different capabilities" |

**Prompt:**
```
A panoramic wide-angle hero illustration representing the AI models landscape as a dynamic, interconnected ecosystem.

VISUAL CONCEPT: A stylized "map" or "landscape" showing the AI industry as a terrain with different regions and paths.

CENTRAL COMPOSITION:
- Multiple "islands" or "territories" representing major AI companies
- Connecting bridges, pathways, or data streams linking them
- Different terrain types representing different model capabilities

COMPANY TERRITORIES (stylized, not realistic logos):
- Anthropic region: Warm, safety-focused aesthetic (could be a lighthouse or beacon)
- OpenAI region: Innovation/research vibe (could be a laboratory or launch pad)
- Google region: Scale/infrastructure feel (could be a vast data center landscape)
- Meta region: Open/community aesthetic (could be open fields or commons)
- Mistral region: Efficient/French aesthetic (could be a sleek tower)

CONNECTING ELEMENTS:
- API pathways shown as glowing roads or data rivers
- Cloud regions floating above (AWS, Azure, GCP as floating islands)
- Open source models as freely accessible areas with multiple entry points

VISUAL METAPHORS:
- Models as different types of buildings/structures (larger = more parameters)
- Context windows as sizes of reception areas
- Speed as vehicle types on the roads

DECORATIVE ELEMENTS:
- Subtle grid pattern suggesting technology
- Data particles flowing through the landscape
- Different colored regions for different specializations (code, text, images)

Color palette: Diverse but harmonious - tech blues for infrastructure, warm oranges for innovation hubs, greens for open source areas, purples for cutting-edge regions.

Style: Modern illustrated map aesthetic, similar to video game world maps but professional and tech-focused, no readable text, suitable as chapter hero image conveying "the wide world of AI models awaits exploration."
```

---

### Image 04-02: Model Lifecycle

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-02-flow-model-lifecycle.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII model lifecycle in section 4.1 (around line 34-60) |
| **Alt Text** | "Five-stage flow diagram showing model lifecycle: Architecture Design → Pre-training → Fine-tuning → Deployment → Inference" |

**Prompt:**
```
A horizontal flow diagram illustrating the five stages of an AI model's lifecycle, from design to production use.

FIVE STAGES (left to right with connecting flow):

STAGE 1 - ARCHITECTURE DESIGN:
- Icon: Blueprint/schematic/neural network structure diagram
- Visual: Abstract neural network being designed on a drawing board
- Sub-elements: Different architecture options (Transformer blocks)
- Color: Light blue (planning/design phase)
- Caption area: "How should the network be structured?"

STAGE 2 - PRE-TRAINING:
- Icon: Massive data flowing into a model
- Visual: Books, websites, code all streaming into a growing brain
- Sub-elements: GPU clusters, massive compute infrastructure
- Time indicator: "Months of training"
- Scale indicator: "Billions of tokens"
- Color: Purple (compute-intensive phase)
- Caption area: "Learn general knowledge from massive data"

STAGE 3 - FINE-TUNING:
- Icon: Precision tools refining the model
- Visual: The model being specialized/refined
- Sub-elements: Human feedback loop (RLHF), instruction tuning
- Smaller but more precise than pre-training
- Color: Orange (refinement phase)
- Caption area: "Specialize for specific tasks"

STAGE 4 - DEPLOYMENT:
- Icon: Model being placed on servers/cloud
- Visual: API endpoints, download symbols, cloud infrastructure
- Sub-elements: API gateway, versioning, scaling
- Color: Green (go-live phase)
- Caption area: "Make it available for use"

STAGE 5 - INFERENCE:
- Icon: User interacting with model
- Visual: Chat interface, API calls, responses flowing
- Sub-elements: User queries, model responses
- "This is what you do when you chat with AI"
- Color: Teal (active use phase)
- Caption area: "Using the model to get predictions"

FLOW ELEMENTS:
- Arrows showing progression
- Time/cost indicators shrinking from pre-training to inference
- Quality/specialization indicators increasing
- Clear visual progression from broad to specific

Style: Modern tech flow diagram, clean stages with distinct visual identities, educational documentation quality, minimal text, suitable for teaching the model lifecycle concept.
```

---

### Image 04-03: Major AI Companies Overview

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-03-info-ai-companies.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | Replace or accompany the ASCII company boxes in section 4.2 (around line 94-148) |
| **Alt Text** | "Five-panel infographic showing major AI companies: Anthropic (safety), OpenAI (AGI), Google (scale), Meta (open source), and Mistral (efficiency)" |

**Prompt:**
```
An infographic showing the five major AI companies as distinct "cards" or "panels" with their key characteristics.

FIVE COMPANY PANELS (grid or horizontal layout):

PANEL 1 - ANTHROPIC:
- Visual identity: Safety beacon/lighthouse/shield
- Tagline visualization: "AI Safety First"
- Key visual: Constitutional AI, helpful robot
- Color scheme: Warm orange/coral (#ff6d00, #ff9100)
- Key models indicator: Claude family
- Unique feature icon: Extra-long context (200K)
- Founded: 2021

PANEL 2 - OPENAI:
- Visual identity: Rocket/laboratory/frontier exploration
- Tagline visualization: "AGI for humanity"
- Key visual: ChatGPT interface, research papers
- Color scheme: Green/teal (#00a67e)
- Key models indicator: GPT family, DALL-E
- Unique feature icon: ChatGPT popularity, Microsoft partnership
- Founded: 2015

PANEL 3 - GOOGLE (DeepMind):
- Visual identity: Data infrastructure/neural brain
- Tagline visualization: "Organizing information"
- Key visual: Massive scale, integrated products
- Color scheme: Google colors (blue, red, yellow, green)
- Key models indicator: Gemini, PaLM
- Unique feature icon: AlphaFold, product integration
- Established AI research presence

PANEL 4 - META:
- Visual identity: Open door/community/sharing
- Tagline visualization: "Open AI research"
- Key visual: Open source symbol, community contributions
- Color scheme: Blue (#1877f2)
- Key models indicator: LLaMA family
- Unique feature icon: Open weights, democratization
- FAIR research

PANEL 5 - MISTRAL:
- Visual identity: Efficient/sleek/European
- Tagline visualization: "Open and efficient"
- Key visual: Small but powerful, efficiency focused
- Color scheme: French-inspired (blue, white, red accents)
- Key models indicator: Mistral, Mixtral
- Unique feature icon: High performance at smaller sizes
- Founded: 2023

LAYOUT OPTIONS:
- 5 cards in a row
- 2-3 top row + 2-3 bottom row
- Central "AI Landscape" hub with radiating company cards

VISUAL CONSISTENCY:
- Each card same format but distinct color/icon
- Key stats or unique value proposition visible
- Year founded as timeline indicator

Style: Modern company profile cards, tech startup aesthetic, clean and professional, consistent format but distinct identities, no actual logos (stylized representations), suitable for educational comparison.
```

---

### Image 04-04: Proprietary vs Open Source Comparison

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-04-compare-proprietary-opensource.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 4.3 header "Proprietary vs Open Source Models" (around line 192) |
| **Alt Text** | "Split comparison showing proprietary models (cloud-based, managed, pay-per-use) versus open source models (self-hosted, customizable, infrastructure required)" |

**Prompt:**
```
A split-screen comparison illustration contrasting proprietary and open source AI models for DevOps decision-making.

SPLIT SCREEN LAYOUT:

LEFT SIDE - PROPRIETARY MODELS:
- Header visual: Cloud with API endpoints, polished interface
- Visual metaphor: Luxury car rental (convenient, no maintenance, pay per use)
- Examples shown as icons: Claude, GPT-4, Gemini logos (stylized)

PROS section (checkmarks, green):
- "State-of-the-art performance" - Trophy/medal icon
- "No infrastructure to manage" - Cloud with checkmark
- "Regular updates" - Refresh/update icon
- "Enterprise support" - Headset/support icon
- "Easy to start" - Key icon (just an API key)

CONS section (X marks, red):
- "Ongoing costs" - Dollar signs flowing out
- "Data leaves network" - Data flowing to external cloud
- "Vendor lock-in" - Chain/lock icon
- "Rate limits" - Throttle/gauge icon

Best for: "Most production use cases, rapid prototyping"

RIGHT SIDE - OPEN SOURCE MODELS:
- Header visual: On-premise server rack, DIY setup
- Visual metaphor: Own your own car (upfront cost, full control, you maintain)
- Examples shown as icons: LLaMA, Mistral, Falcon logos (stylized)

PROS section (checkmarks, green):
- "Free to use" - Open/free icon, no dollar signs
- "Data stays on-premise" - Data staying in box
- "Full control" - Control panel/switches
- "Can fine-tune" - Wrench/customization icon
- "No vendor lock-in" - Broken chain

CONS section (X marks, red):
- "Requires GPU infrastructure" - Server rack cost
- "Lower performance typically" - Slower indicator
- "You manage updates" - Maintenance icon
- "Need ML expertise" - Brain/expertise icon

Best for: "Privacy requirements, high-volume workloads, customization"

CENTER DIVIDER:
- Question: "Which is right for you?"
- Decision criteria hints
- "Most teams start proprietary, migrate to open source at scale"

Style: Clean comparison layout, clear pros/cons iconography, professional infographic style, balanced presentation (neither side "wins"), suitable for decision-making reference.
```

---

### Image 04-05: Model Types Taxonomy

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-05-diagram-model-taxonomy.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 4:3 or 16:9 |
| **Placement** | Replace or accompany the ASCII model taxonomy in section 4.4 (around line 502-545) |
| **Alt Text** | "Hierarchical taxonomy diagram showing AI model types: Text Generation, Text Understanding, Embeddings, Image Generation, Image Understanding, Speech, and Specialized models" |

**Prompt:**
```
A hierarchical taxonomy diagram showing the different types of AI models organized by their primary function.

LAYOUT: Tree structure or category grid showing model types

MAIN CATEGORIES (7 branches):

1. TEXT GENERATION (LLMs):
- Icon: Document with pen/writing
- Sub-categories:
  - General purpose: Claude, GPT-4, Gemini (icons)
  - Code specialized: CodeLlama, StarCoder (code brackets)
  - Instruction-tuned: Vicuna, Alpaca (assistant icon)
- Color: Blue (primary language models)

2. TEXT UNDERSTANDING:
- Icon: Document with magnifying glass
- Sub-categories:
  - Classification: BERT, RoBERTa (category icon)
  - Named Entity Recognition: SpaCy (tag icon)
  - Sentiment Analysis: (emotion icon)
- Color: Purple (analysis models)

3. EMBEDDINGS:
- Icon: Vector/arrow diagram
- Sub-categories:
  - Text embeddings: OpenAI Ada, E5
  - Code embeddings: CodeBERT
  - Multi-modal: CLIP
- Color: Teal (representation models)

4. IMAGE GENERATION:
- Icon: Paintbrush/canvas
- Sub-categories:
  - DALL-E 3, Midjourney
  - Stable Diffusion (open source highlighted)
  - Imagen
- Color: Orange (creative/generative)

5. IMAGE UNDERSTANDING:
- Icon: Eye/camera with brain
- Sub-categories:
  - GPT-4V, Claude Vision
  - LLaVA (open source)
  - BLIP-2
- Color: Yellow (vision models)

6. SPEECH:
- Icon: Microphone/soundwave
- Sub-categories:
  - Speech-to-Text: Whisper (open source highlighted)
  - Text-to-Speech: ElevenLabs, Azure
  - Voice Cloning
- Color: Green (audio models)

7. SPECIALIZED:
- Icon: Specialist/expert badge
- Sub-categories:
  - SQL Generation: SQLCoder
  - Math/Reasoning: specialized fine-tunes
  - Scientific: BioGPT, ChemBERTa
- Color: Red (domain-specific)

VISUAL ELEMENTS:
- Clear hierarchy from general categories to specific models
- Open source models highlighted with special indicator
- Size or prominence indicating popularity/capability
- Connection lines showing relationships

Style: Modern taxonomy visualization, clear categorization, educational poster style, suitable for understanding the AI model ecosystem, minimal text with clear icons.
```

---

### Image 04-06: Hosting Options Decision Tree

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-06-flow-hosting-decision-tree.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | Replace or accompany the ASCII decision flowchart in section 4.5 (around line 982-1042) |
| **Alt Text** | "Decision tree flowchart for choosing AI model hosting: API vs Cloud Marketplace vs Self-hosted, based on privacy, volume, and expertise requirements" |

**Prompt:**
```
A decision tree flowchart helping users choose the right AI model hosting option.

FLOWCHART STRUCTURE (top to bottom):

START NODE:
- "I need to run AI models for DevOps workflows"
- Entry point, neutral color

DECISION 1 - DATA RESIDENCY:
- Question: "Do you have strict data residency requirements?"
- Diamond shape decision node
- Branch YES → Go to GPU check
- Branch NO → Go to volume check

BRANCH A (YES → Data must stay):
- Decision: "Do you have GPU infrastructure?"
- YES → SELF-HOST OPEN SOURCE (Ollama/vLLM)
  - Result box: "Cost: GPU maintenance, Setup: 1-2 weeks, Skill: High"
  - Color: Orange (most complex)
- NO → "Can data touch cloud provider?"
  - YES → AWS BEDROCK / AZURE OPENAI (VPC)
    - Result box: "Cost: $500-2K/month, Setup: 2-3 days, Skill: Medium"
    - Color: Purple (enterprise)
  - NO → BUILD GPU CLUSTER + SELF-HOST
    - Result box: "Cost: $10K-50K/month, Setup: 1-3 months, Skill: Very High"
    - Color: Red (most expensive/complex)

BRANCH B (NO → Data can leave):
- Decision: "What's your expected monthly token volume?"
- <10M tokens/month → Check enterprise features need
  - Enterprise features needed → CLOUD MARKETPLACE
    - Result box: "Cost: $100-1K/month, Setup: Same day, Skill: Low"
    - Color: Blue
  - No enterprise features → DIRECT API
    - Result box: "Cost: $10-500/month, Setup: 1 hour, Skill: Very Low"
    - Color: Green (simplest)
- 10-50M tokens/month → COMPARE COSTS path
- >50M tokens/month → SELF-HOST OR MANAGED OPEN SOURCE
  - Result box: "At this scale, self-hosting often cheaper"
  - Color: Yellow

VISUAL ELEMENTS:
- Decision diamonds in neutral gray
- Result boxes color-coded by complexity
- Cost/time/skill indicators at each endpoint
- Clear flow arrows
- "Most common path" highlighted

Style: Professional flowchart, clear decision points, actionable endpoints with key metrics, suitable for actual decision-making, clean and readable.
```

**🎬 ANIMATION CANDIDATE**: This could be an interactive decision tree or animated GIF showing different paths highlighted based on different scenarios.

---

### Image 04-07: Model Trade-off Matrix

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-07-info-tradeoff-matrix.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 4.6 "Multi-Dimensional Trade-off Matrix" (around line 1514) |
| **Alt Text** | "Matrix visualization showing model trade-offs across quality, cost, latency, privacy, context window, and ease of use for major AI models" |

**Prompt:**
```
A multi-dimensional comparison matrix showing how different AI models trade off across key dimensions.

MATRIX LAYOUT:
Rows: Major models (8-10 models)
Columns: Key dimensions (6 dimensions)

MODELS (rows):
- Claude Opus 4.5
- Claude Sonnet 4.5
- Claude Haiku 4.5
- GPT-4 Turbo
- GPT-4o mini
- Gemini Ultra
- LLaMA 3 70B
- Mistral 7B
- CodeLlama 34B

DIMENSIONS (columns):
1. QUALITY (star rating visualization)
- 5 stars = Best reasoning
- Varying fill levels per model

2. COST (dollar sign scale)
- $ to $$$$$ scale
- Visual: Fewer dollars = cheaper

3. LATENCY (clock/speed indicator)
- Fast/Medium/Slow icons
- Visual: Fewer clock icons = faster

4. PRIVACY (lock/cloud icon)
- API only (cloud) vs Self-hosted (lock)
- Binary indicator

5. CONTEXT (number visualization)
- 8K to 1M tokens shown as bars
- Visual: Longer bar = larger context

6. EASE OF USE (difficulty indicator)
- Easy/Moderate/Hard
- Visual: Simple icons

VISUAL DESIGN:
- Heat map style coloring (green = good, red = challenging)
- Each cell has both icon and subtle color
- Highlighted "sweet spot" models (Pareto efficient)
- Clear legends for each dimension

CALLOUTS:
- "Best for most teams" highlight on Claude Sonnet
- "Best budget option" highlight on Claude Haiku
- "Best for privacy" highlight on self-hosted options

Style: Data-rich comparison matrix, scannable design, professional infographic, suitable for quick model comparison, clear visual hierarchy.
```

---

### Image 04-08: Emerging Trends Timeline

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-04-img-08-flow-emerging-trends.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 4.7 "Emerging Trends" header (around line 1759) |
| **Alt Text** | "Forward-looking illustration showing six emerging AI trends: multimodal models, longer context windows, specialized agents, local models, fine-tuning democratization, and real-time capabilities" |

**Prompt:**
```
A forward-looking visualization showing six emerging trends in AI models, arranged as a futuristic roadmap or trend landscape.

LAYOUT: Horizontal progression or radial arrangement showing 6 trends

SIX TREND AREAS:

1. MULTIMODAL BY DEFAULT:
- Visual: Multiple input types (text, image, audio, video) converging
- Icon: Eye + ear + document combining
- Future vision: "Upload screenshot, get debugging help"
- Color: Rainbow/multi-colored (multiple modalities)

2. LONGER CONTEXT WINDOWS:
- Visual: Expanding container or growing window
- Progression shown: 4K → 32K → 128K → 200K → 1M+
- Future vision: "Process entire codebases at once"
- Color: Deep blue (depth/capacity)

3. SPECIALIZED AGENTS:
- Visual: AI with action capabilities (hands, tools)
- Icon: Robot with kubectl/deployment tools
- Future vision: "AI that can run commands, create PRs, deploy"
- Examples: Claude Code, Copilot Workspace, Devin
- Color: Orange (action/agency)

4. LOCAL MODELS IMPROVING:
- Visual: Laptop or personal device running AI
- Icon: Small but powerful (tiny rocket)
- Future vision: "7B models matching GPT-3.5 quality"
- Tools: Ollama, LM Studio
- Color: Green (accessible/personal)

5. FINE-TUNING DEMOCRATIZATION:
- Visual: Customization/personalization tools
- Icon: DIY/maker tools, LoRA symbols
- Future vision: "Easier to create specialized models"
- Approaches: LoRA, few-shot, RAG
- Color: Purple (customization)

6. REAL-TIME CAPABILITIES:
- Visual: Speed/streaming/instant
- Icon: Lightning bolt, streaming data
- Future vision: "Interactive debugging, real-time log analysis"
- Color: Yellow (speed/energy)

TIMELINE ELEMENT:
- "2024-2025" indicator
- "What's coming" directional arrow
- Progression from current state to future capabilities

VISUAL METAPHORS:
- Could be arranged as a star map (exploring the future)
- Or as a road with different lanes/directions
- Or as emerging from a horizon

Style: Futuristic but professional, forward-looking optimism, tech industry aesthetic, suitable for understanding where AI is heading, inspiring but grounded in real trends.
```

---

## Chapter 05: Introduction to Claude

### Overview
- **Chapter Focus**: Claude AI assistant, model family, capabilities, access options, effective usage
- **Total Images**: 7
- **Animation Candidates**: 1

---

### Image 05-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-05-img-01-header-introduction-to-claude.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Meet Your AI Colleague" |
| **Alt Text** | "Welcoming illustration of Claude as an AI assistant, represented as a friendly, professional digital entity ready to help with DevOps tasks" |

**Prompt:**
```
A warm, professional hero illustration introducing Claude as an AI assistant for DevOps engineers.

CENTRAL CONCEPT:
A friendly, approachable representation of Claude as an AI entity - not a robot or human, but an abstract digital presence that feels helpful and trustworthy.

VISUAL REPRESENTATION OF CLAUDE:
- Abstract glowing form or avatar - could be a warm orb, constellation of particles, or stylized assistant icon
- Should feel intelligent but approachable
- Warm orange/coral tones (Anthropic brand colors)
- Subtle neural network or intelligence patterns within
- "Eyes" or focal point that feels attentive without being literal

SURROUNDING ELEMENTS (DevOps context):
- Floating DevOps icons approaching Claude for help:
  - Kubernetes wheel
  - Docker whale
  - Terraform logo shape
  - Code brackets
  - Terminal window
  - Cloud infrastructure symbols
- These elements are "being helped" - receiving solutions, fixes, documentation

INTERACTION VISUALIZATION:
- Light rays or connection lines from Claude to the DevOps elements
- Shows Claude understanding and responding
- Helpful aura or assistance visualization

MOOD ELEMENTS:
- Professional but warm
- Trustworthy and capable
- Ready to assist
- Intelligent but not intimidating

BACKGROUND:
- Clean, professional gradient
- Subtle tech patterns
- Could suggest a digital workspace

Color palette: Warm oranges and corals (#ff6d00, #ff9100) for Claude, tech blues (#1a73e8, #4285f4) for DevOps elements, creating harmony between the assistant and the technical domain.

Style: Modern tech illustration, warm and approachable, professional yet friendly, suitable as "meet your new AI colleague" intro image. The feeling should be welcoming and competent.
```

---

### Image 05-02: Claude at a Glance

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-05-img-02-info-claude-overview.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 4:3 or 16:9 |
| **Placement** | Replace or accompany the ASCII "Claude at a Glance" box in section 5.1 (around line 34-60) |
| **Alt Text** | "Infographic overview of Claude: creator Anthropic, key differentiators including Constitutional AI, 200K context, and access methods" |

**Prompt:**
```
A clean infographic providing a quick overview of Claude's key characteristics and access methods.

LAYOUT: Central Claude representation with radiating information sections

CENTER:
- Claude icon/avatar (warm, glowing)
- "Claude" label area
- Anthropic creator indicator

SECTION 1 - CREATOR INFO (Top):
- Anthropic logo area (stylized)
- Founded: 2021
- Mission: AI safety research
- Visual: Safety/research icons

SECTION 2 - KEY DIFFERENTIATORS (Left):
Six key points with icons:
1. Constitutional AI icon - trained with safety principles
2. Honesty icon - transparent about limitations
3. 200K token icon - massive context window
4. Brain icon - strong reasoning capabilities
5. Instruction icon - excellent at following complex instructions
6. Conversation icon - natural communication style

SECTION 3 - ACCESS METHODS (Right):
Five access options with icons:
1. claude.ai - web browser icon
2. API - code/terminal icon
3. AWS Bedrock - AWS cloud icon
4. Google Vertex AI - GCP icon
5. Claude Code - CLI/terminal icon

VISUAL ELEMENTS:
- Clean connecting lines from center to sections
- Each point has a small, clear icon
- Color-coded sections
- Professional but approachable design

Color palette: Warm Anthropic orange for Claude center, tech blues for differentiators, greens for access methods.

Style: Modern quick-reference infographic, scannable design, suitable for "at a glance" understanding, clean icons and minimal text.
```

---

### Image 05-03: The Three H's - Helpful, Harmless, Honest

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-05-img-03-concept-three-hs.png` |
| **Type** | Concept |
| **Aspect Ratio** | 16:9 or 1:1 |
| **Placement** | After section 5.1 "Claude's Design Philosophy" (around line 64-90) |
| **Alt Text** | "Three pillars diagram showing Claude's core values: Helpful (provides working solutions), Harmless (avoids dangerous outputs), Honest (transparent about limitations)" |

**Prompt:**
```
A memorable diagram illustrating Claude's three core design principles: Helpful, Harmless, Honest.

LAYOUT OPTIONS:
- Three pillars supporting a structure
- Three interlocking circles (Venn diagram style)
- Three points of a triangle/shield
- Three ascending steps

THREE H'S:

H1 - HELPFUL (First):
- Icon: Lightbulb, wrench, helping hand
- Visual: Claude providing working solutions
- Examples shown:
  - Working code output
  - Clarifying questions being asked
  - Alternative suggestions offered
- Color: Warm orange/gold (positive action)
- Mood: Proactive, useful, practical

H2 - HARMLESS (Second):
- Icon: Shield, checkmark, safety barrier
- Visual: Claude blocking harmful outputs
- Examples shown:
  - Rejecting malicious requests
  - Warning about security risks
  - Considering implications
- Color: Green (safety)
- Mood: Protective, careful, responsible

H3 - HONEST (Third):
- Icon: Eye, truth symbol, transparency indicator
- Visual: Claude being transparent
- Examples shown:
  - Admitting uncertainty
  - Acknowledging limitations
  - Distinguishing fact from opinion
- Color: Blue (trust, clarity)
- Mood: Transparent, trustworthy, humble

CENTER/CONNECTING ELEMENT:
- Claude icon at the intersection
- Shows all three principles working together
- "Constitutional AI" connection if space permits

BALANCE VISUALIZATION:
- All three equally important
- Each supports the others
- Together they create a reliable assistant

Style: Clean, memorable diagram, each H distinct but connected, suitable for understanding Claude's design philosophy, professional color palette, minimal text with clear icons.
```

---

### Image 05-04: Claude Model Family

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-05-img-04-compare-claude-models.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII model family boxes in section 5.2 (around line 99-138) |
| **Alt Text** | "Three-tier comparison of Claude models: Opus 4.5 (The Powerhouse), Sonnet 4.5 (The Sweet Spot), and Haiku 4.5 (The Speed Demon)" |

**Prompt:**
```
A three-panel comparison showing the Claude 4.5 model family with their distinct characteristics and use cases.

THREE HORIZONTAL PANELS (or vertical tiers):

PANEL 1 - CLAUDE SONNET 4.5 "The Sweet Spot" (CENTER/HIGHLIGHTED):
- Position: Center or most prominent (recommended default)
- Visual: Balanced scale, golden/optimal indicator
- Icon: Star or "recommended" badge
- Key attributes:
  - Best balance indicator
  - Code generation icon
  - Complex reasoning icon
  - 200K context icon
  - Vision capability icon
- Color: Rich blue with gold accents (premium but accessible)
- Badge: "Recommended for most DevOps tasks"
- Mood: Optimal, balanced, professional choice

PANEL 2 - CLAUDE OPUS 4.5 "The Powerhouse" (TOP):
- Position: Top or premium tier
- Visual: Crown, power symbol, strongest indicator
- Icon: Trophy or maximum power gauge
- Key attributes:
  - Most capable indicator
  - Complex analysis icon
  - Architecture decisions icon
  - Higher cost indicator
  - "Quality matters most" indicator
- Color: Deep purple/gold (premium)
- Badge: "For complex analysis and critical decisions"
- Mood: Premium, powerful, for important tasks

PANEL 3 - CLAUDE HAIKU 4.5 "The Speed Demon" (BOTTOM):
- Position: Bottom or efficiency tier
- Visual: Lightning bolt, speed indicator, efficiency
- Icon: Speedometer or rocket
- Key attributes:
  - Fastest response icon
  - Cost-effective icon
  - High volume icon
  - Chatbot/quick query icon
  - Automation icon
- Color: Teal/cyan (efficient, light)
- Badge: "For high-volume and simple tasks"
- Mood: Fast, efficient, scalable

COMPARISON ELEMENTS:
- Speed indicator: Haiku fastest, Opus slowest
- Cost indicator: Haiku cheapest, Opus most expensive
- Capability indicator: Opus highest, Haiku lowest
- Sweet spot highlight on Sonnet

VISUAL FLOW:
- Clear hierarchy from premium to budget
- Each model clearly distinguished
- Recommendation visible for default choice

Style: Clean comparison cards, tier-based visualization, clear use case guidance, suitable for model selection decisions, professional color palette.
```

---

### Image 05-05: Claude Capabilities vs Limitations

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-05-img-05-compare-can-cannot.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 5.3 covering capabilities and limitations (around line 250-292) |
| **Alt Text** | "Split comparison showing what Claude can do (code generation, debugging, documentation) versus limitations (no real-time data, no code execution, no internet access)" |

**Prompt:**
```
A split-screen comparison showing Claude's capabilities and limitations for DevOps engineers.

SPLIT LAYOUT:

LEFT SIDE - "WHAT CLAUDE EXCELS AT" (Green/positive):
- Header: Checkmark icon, "Excellent" badge
- Section style: Green accents, achievement indicators

Categories with icons:
1. CODE GENERATION - Excellent
   - Terraform modules icon
   - Kubernetes manifests icon
   - CI/CD pipelines icon
   - Monitoring scripts icon

2. CODE REVIEW - Excellent
   - Security scan icon
   - Performance suggestions icon
   - Best practices icon

3. DEBUGGING - Excellent
   - Log analysis icon
   - Error tracing icon
   - Root cause icon

4. DOCUMENTATION - Excellent
   - README icon
   - API docs icon
   - Runbooks icon

5. LONG CONTEXT - Industry-leading
   - 200K tokens badge
   - "Analyze entire log files" indicator

RIGHT SIDE - "WHAT CLAUDE CANNOT DO" (Yellow/informative):
- Header: Info icon, "Limitations" badge
- Section style: Yellow accents, awareness indicators

Categories with icons and workarounds:
1. REAL-TIME DATA - No access
   - Clock with X icon
   - Workaround: "Provide data in prompt"

2. EXECUTE CODE - Generate only
   - Terminal with X icon
   - Exception: "Claude Code CAN execute"

3. INTERNET ACCESS - No browsing
   - Globe with X icon
   - Workaround: "Paste content in prompt"

4. MEMORY BETWEEN SESSIONS - Fresh start
   - Brain with X icon
   - Workaround: "Save context for reuse"

5. DIRECT SYSTEM ACCESS - No SSH
   - Server with X icon
   - Exception: "Claude Code for local files"

CENTER DIVIDER:
- "Know both sides to use effectively"
- Balance indicator

Style: Clear capabilities/limitations layout, informative not negative, workarounds visible, suitable for setting realistic expectations, green/yellow color coding.
```

---

### Image 05-06: Claude Access Options

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-05-img-06-flow-access-options.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 5.4 header "How to Access Claude" (around line 296) |
| **Alt Text** | "Five access paths to Claude: Web Interface (claude.ai), Direct API, AWS Bedrock, Google Vertex AI, and Claude Code CLI" |

**Prompt:**
```
A flow diagram showing five different ways to access Claude, with guidance on when to use each.

LAYOUT: Central Claude node with five branching access paths

CENTER:
- Claude icon/avatar
- "Access Claude" label
- Connection point for all paths

FIVE ACCESS PATHS (radiating outward):

PATH 1 - CLAUDE.AI WEB INTERFACE (Top):
- Icon: Browser window
- Tiers shown: Free → Pro → Max
- Best for: "Quick questions, exploration, learning"
- Color: Light blue (easy access)
- Complexity: Lowest

PATH 2 - ANTHROPIC API (Right-top):
- Icon: Code/terminal with API symbol
- Code snippet visual: Python import anthropic
- Best for: "Automation, custom integrations"
- Color: Purple (developer)
- Complexity: Medium

PATH 3 - AWS BEDROCK (Right-bottom):
- Icon: AWS cloud symbol
- Features: VPC, IAM, CloudTrail
- Best for: "Enterprise, compliance, AWS shops"
- Color: Orange (AWS)
- Complexity: Medium-high

PATH 4 - GOOGLE VERTEX AI (Left-bottom):
- Icon: GCP cloud symbol
- Features: GCP integration
- Best for: "GCP-based organizations"
- Color: Google blue/green
- Complexity: Medium-high

PATH 5 - CLAUDE CODE CLI (Left-top):
- Icon: Terminal/command line
- Features: File access, code execution
- Best for: "DevOps coding, local development"
- Color: Green (power user)
- Complexity: Low-medium
- "Covered in next chapters" indicator

DECISION GUIDANCE:
- Quick path highlighted for "Most users start here"
- Enterprise path for compliance needs
- Developer path for automation

VISUAL ELEMENTS:
- Each path clearly labeled
- Complexity/ease indicators
- Best use case visible
- Cost tier hints where relevant

Style: Clean radial flow diagram, clear access options, actionable guidance, suitable for choosing the right access method, color-coded by provider/type.
```

---

### Image 05-07: Vision Capabilities for DevOps

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-05-img-07-concept-vision-capabilities.png` |
| **Type** | Concept |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 5.6 "Claude's Vision Capabilities" (around line 786) |
| **Alt Text** | "Four examples of Claude's vision capabilities for DevOps: analyzing architecture diagrams, error screenshots, log images, and network topology diagrams" |

**Prompt:**
```
An illustration showing four practical DevOps use cases for Claude's vision/image analysis capabilities.

LAYOUT: Four quadrants or panels showing different vision use cases

PANEL 1 - ARCHITECTURE DIAGRAMS:
- Input visual: A stylized cloud architecture diagram (boxes, arrows, AWS icons)
- Arrow pointing to Claude processing
- Output visual: Terraform code blocks
- Caption area: "Upload diagram → Get infrastructure code"
- Color: Blue (infrastructure)

PANEL 2 - ERROR SCREENSHOTS:
- Input visual: Grafana/monitoring dashboard screenshot style
- Arrow pointing to Claude processing
- Output visual: Analysis text, identified issues
- Caption area: "Share dashboard → Get incident analysis"
- Color: Red/orange (alerts/errors)

PANEL 3 - LOG IMAGES (Slack sharing scenario):
- Input visual: Screenshot of log output (when someone shares via Slack)
- Arrow pointing to Claude processing
- Output visual: Extracted text, identified error
- Caption area: "Log screenshot → Transcribed and analyzed"
- Color: Green (logs)

PANEL 4 - NETWORK TOPOLOGY:
- Input visual: Network diagram (nodes, connections, firewalls)
- Arrow pointing to Claude processing
- Output visual: Security analysis, improvement suggestions
- Caption area: "Network diagram → Security review"
- Color: Purple (security)

CENTER ELEMENT:
- Claude's "eye" or vision capability icon
- "Claude Vision" label
- Connection to all four use cases

VISUAL FLOW:
- Image input → Claude processing → Actionable output
- Each panel shows the transformation
- Practical, real-world DevOps scenarios

Style: Clean four-panel layout, practical examples, shows image-to-insight transformation, suitable for understanding vision capabilities in DevOps context, professional documentation quality.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing an architecture diagram being "scanned" by Claude and transforming into Terraform code output.

---

## Chapter 06: Claude Code Fundamentals

### Overview
- **Chapter Focus**: Claude Code CLI introduction, installation, authentication, basic usage, core workflows, DevOps examples
- **Total Images**: 10
- **Animation Candidates**: 2

---

### Image 06-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-01-header-claude-code-fundamentals.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Your AI Pair Programmer for the Terminal" |
| **Alt Text** | "Developer at terminal with Claude Code running, showing AI-assisted code generation and file operations in a professional DevOps environment" |

**Prompt:**
```
A dynamic hero illustration showing Claude Code as an AI pair programmer integrated into the terminal/command-line environment.

CENTRAL COMPOSITION:
A stylized terminal window that serves as the gateway between the developer and AI assistance, with energy and productivity flowing through it.

TERMINAL REPRESENTATION:
- Large, prominent terminal/CLI window as the focal point
- Clean, modern terminal aesthetic (dark theme with syntax highlighting)
- Claude Code interface visible within:
  - Input prompt area
  - AI response area with code
  - File tree sidebar suggestion
- Glowing cursor or input indicator showing active interaction

LEFT SIDE - DEVELOPER CONTEXT:
- Abstract developer presence (hands on keyboard, or silhouette)
- Surrounding DevOps artifacts floating nearby:
  - Kubernetes YAML files
  - Docker compose files
  - GitHub/Git icons
  - CI/CD pipeline symbols
  - Cloud infrastructure diagrams
- These represent the "input" - what the developer works with

RIGHT SIDE - AI ASSISTANCE OUTPUT:
- Code blocks being generated in real-time
- File operations being performed:
  - Files being created (new document icons)
  - Files being edited (edit symbols)
  - Tests running (checkmarks)
- Commands being executed (terminal symbols)
- These represent the "output" - what Claude Code produces

CONNECTING ELEMENTS:
- Data flow visualization between developer input and AI output
- The terminal as the bridge/conduit
- Energy particles or light streams showing active processing
- Anthropic orange glow emanating from AI processing areas

VISUAL METAPHOR:
- The terminal as a "portal" to AI assistance
- Developer and AI working as one team
- Productivity and capability amplification

BACKGROUND:
- Professional workspace atmosphere
- Subtle code patterns or git graph visualization
- Dark, focused environment suitable for coding

Color palette: Deep terminal blacks and grays, Anthropic orange (#ff6d00) for AI elements, tech blues (#1a73e8) for code/DevOps elements, green (#4caf50) for success/output indicators.

Style: Modern tech illustration, dynamic and productive feeling, shows the power of CLI-based AI assistance, professional DevOps context, suitable as chapter hero image introducing Claude Code.
```

---

### Image 06-02: Claude Code Capabilities Overview

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-02-diagram-capabilities-overview.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII capabilities diagram in section 6.1 (around line 34-63) |
| **Alt Text** | "Three-category diagram of Claude Code capabilities: Read & Understand, Execute & Modify, and Automate & Assist" |

**Prompt:**
```
A clean three-section diagram illustrating Claude Code's core capability categories.

LAYOUT: Three vertical columns or horizontal sections, each representing a capability category

SECTION 1 - READ & UNDERSTAND (Left):
- Header icon: Eye or magnifying glass over documents
- Color: Blue tones (information gathering)
- Four capability icons with labels:
  1. "Read files in your project" - File/document icon
  2. "Understand codebase structure" - Tree/hierarchy icon
  3. "Navigate directories" - Folder navigation icon
  4. "Search for patterns across files" - Search/grep icon
- Visual: Documents flowing into an understanding/brain visualization
- Mood: Observational, analytical

SECTION 2 - EXECUTE & MODIFY (Center):
- Header icon: Wrench/tool or edit symbol
- Color: Orange/amber tones (action/modification)
- Four capability icons with labels:
  1. "Run shell commands" - Terminal/command icon
  2. "Edit existing files" - Pencil/edit icon
  3. "Create new files" - Plus/new document icon
  4. "Run tests and builds" - Checkmark/build icon
- Visual: Code being actively modified, commands executing
- Mood: Active, productive

SECTION 3 - AUTOMATE & ASSIST (Right):
- Header icon: Robot arm or automation gear
- Color: Green/teal tones (automation/efficiency)
- Four capability icons with labels:
  1. "Complete multi-step tasks autonomously" - Multi-step workflow icon
  2. "Git operations (commit, branch, PR)" - Git branch icon
  3. "Debug issues with access to real data" - Bug fix icon
  4. "Refactor code across multiple files" - Refactor/multi-file icon
- Visual: Multiple tasks being coordinated, autonomous workflow
- Mood: Efficient, autonomous

CONNECTING ELEMENTS:
- Arrows or flow showing how capabilities work together
- Central Claude Code icon connecting all three sections
- "Your AI Pair Programmer" label
- Shows progression from understanding to action to automation

VISUAL STYLE:
- Clean, modern icons
- Distinct color coding per section
- Professional documentation quality
- Each capability clearly bounded and labeled

Style: Clean capability diagram, three distinct categories, professional icons, suitable for quick understanding of what Claude Code can do, minimal text with clear visual hierarchy.
```

---

### Image 06-03: Claude.ai vs Claude Code Comparison

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-03-compare-claudeai-claudecode.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII comparison table in section 6.1 (around line 67-96) |
| **Alt Text** | "Split comparison showing Claude.ai (web browser, copy-paste workflow) versus Claude Code (terminal, direct file access, command execution)" |

**Prompt:**
```
A split-screen comparison illustration contrasting Claude.ai web interface with Claude Code CLI for development work.

SPLIT LAYOUT:

LEFT SIDE - CLAUDE.AI (Web Interface):
- Header: Browser window frame with claude.ai
- Visual representation: Chat interface in browser
- Workflow steps shown:
  1. "You paste the file content" - Copy icon
  2. "Claude suggests changes" - Chat bubble with code
  3. "You manually copy and apply changes" - Manual copy icon
  4. "You run tests yourself" - Separate terminal icon
- Color scheme: Light blues, web aesthetic
- Icons: Browser, clipboard, chat bubbles
- Workflow indicators: Manual, multi-step, copy-paste
- Label: "Session-based, manual workflow"

CENTER DIVIDER:
- "VS" or comparison indicator
- "Same AI, Different Interface" tagline
- Shows task example: "Add error handling to database module"

RIGHT SIDE - CLAUDE CODE (Terminal):
- Header: Terminal window frame
- Visual representation: CLI interface with commands
- Workflow steps shown:
  1. "Claude reads the database module directly" - Direct file access
  2. "Claude edits the file in place" - Direct edit icon
  3. "Claude runs the tests" - Integrated test icon
  4. "Claude fixes any issues found" - Automatic fix icon
- Color scheme: Dark theme, terminal green/orange
- Icons: Terminal, file system, direct arrows
- Workflow indicators: Automatic, integrated, direct
- Label: "Project context, automated workflow"

COMPARISON METRICS:
- Speed indicator: Claude Code faster
- Steps required: Claude Code fewer
- Context awareness: Claude Code automatic
- Integration: Claude Code superior

VISUAL METAPHOR:
- Claude.ai: Multiple disconnected windows/tools
- Claude Code: Single integrated environment
- Arrows showing workflow difference (multi-hop vs direct)

KEY DIFFERENCES TABLE (visual):
- Web browser ↔ Terminal
- Copy-paste ↔ Direct access
- Manual commands ↔ Automatic execution
- Session-based ↔ Project context

Style: Clear side-by-side comparison, workflow visualization, professional documentation style, highlights the efficiency advantage of CLI integration.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing the same task being done in both interfaces, with Claude Code completing faster with fewer steps.

---

### Image 06-04: Installation Methods Decision Flow

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-04-flow-installation-methods.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 6.2 "Installation Method Selection" (around line 223-234) |
| **Alt Text** | "Decision flowchart for choosing Claude Code installation method: npm, Homebrew, winget, or direct download based on environment and requirements" |

**Prompt:**
```
A decision flowchart helping users choose the right Claude Code installation method.

FLOWCHART STRUCTURE:

START NODE:
- "Install Claude Code"
- Entry point, neutral color

DECISION 1 - PLATFORM:
- Question: "What's your operating system?"
- Three branches: macOS, Windows, Linux
- Color-coded paths

macOS PATH:
- Decision: "Node.js already installed?"
  - YES → "npm install -g @anthropic-ai/claude-code" (Recommended)
  - NO → Decision: "Prefer package manager?"
    - YES → "brew install claude-code" (Homebrew)
    - NO → "Direct download" (Binary)

WINDOWS PATH:
- Decision: "Using WSL?"
  - YES → Follow Linux path
  - NO → "winget install Anthropic.ClaudeCode" (Native)

LINUX PATH:
- Decision: "Node.js already installed?"
  - YES → "npm install -g @anthropic-ai/claude-code" (Recommended)
  - NO → Decision: "Want to install Node.js?"
    - YES → Install Node.js first → npm install
    - NO → "Direct download" (Binary)

ENDPOINT BOXES (color-coded by method):

NPM (Blue - most common):
- Icon: npm logo stylized
- Command: `npm install -g @anthropic-ai/claude-code`
- Pros: "Easy updates, cross-platform"
- Best for: "Most developers"

HOMEBREW (Orange - macOS):
- Icon: Homebrew stylized
- Command: `brew install claude-code`
- Pros: "Native macOS, auto-updates"
- Best for: "Mac users without Node.js"

WINGET (Blue - Windows):
- Icon: Windows stylized
- Command: `winget install Anthropic.ClaudeCode`
- Pros: "Native Windows integration"
- Best for: "Windows users"

DIRECT DOWNLOAD (Gray - universal):
- Icon: Download arrow
- Command: `curl -fsSL ... && chmod +x`
- Pros: "No dependencies, air-gapped"
- Best for: "Restricted environments, Docker"

VISUAL ELEMENTS:
- Clear decision diamonds
- Color-coded paths
- Platform icons at decision points
- "Recommended" badges on preferred paths
- Verification step at all endpoints: `claude --version`

Style: Professional flowchart, clear decision points, actionable endpoints, suitable for quick installation method selection.
```

---

### Image 06-05: Authentication Security Comparison

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-05-compare-auth-security.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 6.3 "Authentication Security Best Practices" table (around line 519-528) |
| **Alt Text** | "Four-tier security comparison of authentication methods: Interactive Login (highest), AWS Bedrock IAM (high), Environment Variable (medium), Config File (lowest)" |

**Prompt:**
```
A security-focused comparison showing four authentication methods ranked by security level.

LAYOUT: Four horizontal tiers arranged from most secure (top) to least secure (bottom), or four columns with security meters

TIER 1 - INTERACTIVE LOGIN (Highest Security - 5 stars):
- Icon: Browser + lock/shield combination
- Security meter: Full green (★★★★★)
- Visual: OAuth flow diagram simplified
- How it works: "Browser auth → Token in keychain"
- Pros (checkmarks):
  - "Token encrypted at rest"
  - "Auto-refresh, auto-expiration"
  - "Can revoke from dashboard"
  - "Full audit trail"
- Risk level: LOW
- Use case: "Individual developers"
- Color: Green security zone

TIER 2 - AWS BEDROCK (IAM Roles) (High Security - 5 stars):
- Icon: AWS + IAM shield
- Security meter: Full green (★★★★★)
- Visual: IAM role assumption flow
- How it works: "IAM role → Temporary credentials"
- Pros (checkmarks):
  - "No long-lived keys"
  - "AWS manages rotation"
  - "CloudTrail audit logs"
  - "VPC restrictions possible"
- Risk level: VERY LOW
- Use case: "Enterprise, production"
- Color: Green security zone

TIER 3 - ENVIRONMENT VARIABLE (Medium Security - 3 stars):
- Icon: Terminal with key visible
- Security meter: Yellow (★★★☆☆)
- Visual: Key exposed in terminal environment
- How it works: "API key → Environment variable"
- Warnings (caution icons):
  - "Visible in process list"
  - "Logged in shell history"
  - "Inherited by child processes"
- Risk level: MEDIUM
- Use case: "CI/CD pipelines (with secrets manager)"
- Color: Yellow caution zone
- Mitigation: "Load from secrets manager"

TIER 4 - CONFIG FILE (Lowest Security - 2 stars):
- Icon: File with key/lock broken
- Security meter: Red (★★☆☆☆)
- Visual: Plaintext file with exposed key
- How it works: "API key → Plaintext file"
- Risks (X marks):
  - "Can be accidentally committed"
  - "Synced to cloud backups"
  - "Readable by other users"
- Risk level: HIGH
- Use case: "NOT RECOMMENDED"
- Color: Red danger zone
- Warning badge: "Avoid if possible"

VISUAL ELEMENTS:
- Security gradient from top to bottom (green → yellow → red)
- Clear star ratings
- Pros/cons icons consistent
- Risk level indicators
- "Recommended" path highlighted (Interactive Login for dev, Bedrock for prod)

CENTER GUIDANCE:
- Decision helper: "Which should I use?"
- Developer workstation → Interactive Login
- CI/CD Pipeline → Env Var from Secrets Manager
- Production/Enterprise → AWS Bedrock

Style: Security-focused comparison, clear tier separation, visual risk indicators, suitable for understanding auth security trade-offs.
```

---

### Image 06-06: Claude Code Interface Mockup

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-06-screen-interface-mockup.png` |
| **Type** | Screen (Mockup) |
| **Aspect Ratio** | 4:3 or 16:9 |
| **Placement** | Replace or accompany the ASCII interface diagram in section 6.4 (around line 872-899) |
| **Alt Text** | "Claude Code terminal interface mockup showing header, status indicators, input area, and navigation hints" |

**Prompt:**
```
A realistic mockup of the Claude Code terminal interface showing its key elements.

TERMINAL WINDOW FRAME:
- Standard terminal chrome (title bar, window controls)
- Dark theme background (#1e1e1e or similar)
- Monospace font throughout

INTERFACE ELEMENTS:

HEADER SECTION (top):
- Claude Code logo/banner (stylized)
- Version indicator: "Claude Code v2.x.x"
- Decorative border (box drawing characters)

STATUS BAR:
- Connection status: 🟢 "Connected to Claude"
- Working directory: 📁 "/home/user/myproject"
- Tools available: 🔧 "file, bash, edit, etc."
- Model indicator (optional): "Using Claude Sonnet"

MAIN AREA (conversation):
- Sample exchange visible:
  - User input: "> explain this codebase"
  - Claude response: Structured output with:
    - Project structure analysis
    - Key files identified
    - Framework detection
- Syntax highlighting on code blocks
- Proper formatting and indentation

INPUT AREA (bottom):
- Prompt indicator: ">"
- Cursor blinking (or cursor indicator)
- Input hint: "Type your message or /help"

NAVIGATION HINTS PANEL (side or bottom):
- Keyboard shortcuts visible:
  - "Enter - Send message"
  - "Shift+Enter - Multi-line (modern terminals)"
  - "↑/↓ - History navigation"
  - "Tab - Autocompletion"
  - "Ctrl+C - Cancel operation"
  - "Ctrl+T - Toggle theme"
  - "Ctrl+B - Background tasks"
  - "/help - Show commands"

VISUAL ELEMENTS:
- Proper terminal color scheme
- Realistic code formatting
- Status indicators color-coded
- Clean, readable layout

ANNOTATIONS (for documentation purposes):
- Callout labels pointing to key areas
- "Status indicators" pointing to status bar
- "Your input" pointing to prompt area
- "Claude's response" pointing to output area
- "Keyboard shortcuts" pointing to hints

Style: Realistic terminal mockup, professional appearance, clearly shows interface elements, suitable for documentation and user orientation.
```

---

### Image 06-07: Core Workflows Visualization

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-07-flow-core-workflows.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Before section 6.5 "Core Workflows" (around line 935) |
| **Alt Text** | "Five core Claude Code workflows: Understand Codebase, Write New Code, Debug Issues, Refactor Code, and Git Operations" |

**Prompt:**
```
A workflow diagram showing the five core Claude Code workflows as connected, practical processes.

LAYOUT: Five workflow cards arranged horizontally or in a pentagon/star pattern

WORKFLOW 1 - UNDERSTANDING A CODEBASE:
- Icon: Magnifying glass + code structure
- Color: Blue (discovery/learning)
- Flow steps:
  1. Start Claude Code in project
  2. Ask "explain the structure"
  3. Claude reads key files
  4. Receive architecture overview
- Input example: "explain the structure of this project"
- Output example: Project summary, key components
- Badge: "Start here for new projects"

WORKFLOW 2 - WRITING NEW CODE:
- Icon: Plus sign + code brackets
- Color: Green (creation)
- Flow steps:
  1. Describe requirements
  2. Claude identifies patterns
  3. Claude creates code
  4. Review and approve
- Input example: "create POST /api/users endpoint"
- Output example: New endpoint with validation
- Pro tip: "Ask for plan before changes"

WORKFLOW 3 - DEBUGGING:
- Icon: Bug + magnifying glass
- Color: Red/orange (problem solving)
- Flow steps:
  1. Share error message
  2. Claude reads relevant file
  3. Claude analyzes context
  4. Receive fix suggestion
- Input example: "I'm getting TypeError..."
- Output example: Root cause + fix
- Pro tip: "Include full error context"

WORKFLOW 4 - REFACTORING:
- Icon: Arrows reorganizing + code
- Color: Purple (transformation)
- Flow steps:
  1. Identify refactoring target
  2. Claude analyzes function
  3. Claude extracts/reorganizes
  4. Tests verified
- Input example: "refactor processOrder into smaller functions"
- Output example: Clean, testable functions
- Pro tip: "Work incrementally"

WORKFLOW 5 - GIT OPERATIONS:
- Icon: Git branch + commit
- Color: Teal (version control)
- Flow steps:
  1. Request git action
  2. Claude checks status/diff
  3. Claude composes message
  4. Execute with approval
- Input example: "commit these changes with descriptive message"
- Output example: Proper commit message, executed
- Pro tip: "Claude understands git context"

CENTER HUB (connecting element):
- Claude Code icon
- "Your AI Pair Programmer"
- Shows all workflows available
- "All workflows work together"

VISUAL ELEMENTS:
- Each workflow card distinct
- Flow arrows within each card
- Input/output examples visible
- Pro tips highlighted
- Connection lines showing workflows can chain

Style: Clean workflow cards, practical focus, shows real commands and outputs, suitable for understanding core usage patterns.
```

---

### Image 06-08: Approval Flow Diagram

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-08-flow-approval-process.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | Replace or accompany the ASCII approval flow in section 6.7 (around line 1172-1205) |
| **Alt Text** | "Claude Code approval flow: Claude proposes action, user reviews, then chooses Yes (execute), No (skip), or Explain (learn more)" |

**Prompt:**
```
A clear flow diagram illustrating Claude Code's approval mechanism for actions.

FLOW STRUCTURE:

TRIGGER NODE:
- "Claude proposes an action"
- Example shown: Command or file edit
- Neutral color

PROPOSAL DISPLAY:
- Mock terminal showing proposed action
- Example 1 (Command):
  - "I'll run this command:"
  - "$ npm install express"
  - Options shown: [y]es / [n]o / [e]xplain
- Example 2 (File Edit):
  - "I'll make these changes to src/app.js:"
  - Diff view: - old line / + new line
  - Options shown: [y]es / [n]o / [e]xplain / [d]iff

USER DECISION DIAMOND:
- "Your choice?"
- Three main branches

BRANCH Y - YES (Execute):
- Icon: Checkmark, green
- Action: "Command/edit executes"
- Result: "Claude continues to next step"
- Flow continues forward
- Color: Green path

BRANCH N - NO (Skip):
- Icon: X mark, red
- Action: "Command/edit skipped"
- Result: "Claude notes rejection, may suggest alternative"
- Flow pauses/redirects
- Color: Red path

BRANCH E - EXPLAIN:
- Icon: Question mark, blue
- Action: "Claude explains why"
- Result: "You get more context before deciding"
- Flow loops back to decision
- Color: Blue path

BRANCH D - DIFF (File edits only):
- Icon: Compare icon, purple
- Action: "Show full diff context"
- Result: "See complete changes"
- Flow loops back to decision
- Color: Purple path

POST-APPROVAL FLOW:
- Success → Continue to next action
- Multiple actions → Each gets approval
- Completion → Summary of actions taken

SAFETY CALLOUTS:
- "Always review commands before approving"
- "Be cautious with destructive operations"
- "Use /stop if unexpected behavior"
- "You're always in control"

AUTO-APPROVE MENTION:
- Side note: "Auto-approve available for trusted operations"
- Warning: "Use carefully in controlled environments"
- How to enable indicator

VISUAL ELEMENTS:
- Clear decision flow
- Mock terminal displays
- Color-coded paths
- Safety indicators
- "You control everything" emphasis

Style: Clean approval flowchart, shows user control emphasis, security-aware design, suitable for understanding the safety model.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing a proposed action, user reviewing it, and choosing to approve or explain.

---

### Image 06-09: DevOps Use Cases Matrix

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-09-info-devops-usecases.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | Replace or accompany the YAML use case matrix in section 6.9 (around line 1296-1335) |
| **Alt Text** | "Four-category matrix of DevOps use cases: Daily Tasks, Infrastructure, Troubleshooting, and Documentation with example prompts" |

**Prompt:**
```
A categorized matrix showing DevOps use cases for Claude Code with example prompts.

LAYOUT: Four category quadrants or sections

QUADRANT 1 - DAILY TASKS (Top-Left):
- Icon: Calendar/daily checklist
- Color: Blue
- Use cases with example prompts:
  1. "Review CI pipeline failures"
     - Prompt: "The CI is failing, check .github/workflows/ and fix"
  2. "Update dependencies"
     - Prompt: "Update all npm dependencies and fix breaking changes"
  3. "Add monitoring"
     - Prompt: "Add Prometheus metrics to Express endpoints"
- Frequency indicator: Daily/Weekly
- Complexity: Low-Medium

QUADRANT 2 - INFRASTRUCTURE (Top-Right):
- Icon: Cloud/server infrastructure
- Color: Purple
- Use cases with example prompts:
  1. "IaC generation"
     - Prompt: "Create Terraform for S3 bucket with encryption"
  2. "K8s manifests"
     - Prompt: "Generate K8s manifests from docker-compose"
  3. "Security hardening"
     - Prompt: "Review Dockerfile and K8s for security issues"
- Frequency indicator: As needed
- Complexity: Medium-High

QUADRANT 3 - TROUBLESHOOTING (Bottom-Left):
- Icon: Bug/wrench/fix
- Color: Orange/Red
- Use cases with example prompts:
  1. "Analyze logs"
     - Prompt: "Here are 100 error logs, identify patterns"
  2. "Debug performance"
     - Prompt: "API is slow, analyze and suggest optimizations"
  3. "Fix deployment"
     - Prompt: "Pods are CrashLoopBackOff, here's describe output"
- Frequency indicator: When issues arise
- Complexity: Variable

QUADRANT 4 - DOCUMENTATION (Bottom-Right):
- Icon: Document/book
- Color: Green
- Use cases with example prompts:
  1. "Generate runbooks"
     - Prompt: "Create runbook for production deployment"
  2. "API docs"
     - Prompt: "Generate OpenAPI spec from Express routes"
  3. "Architecture docs"
     - Prompt: "Document system architecture from codebase"
- Frequency indicator: Periodic
- Complexity: Medium

CENTER ELEMENT:
- Claude Code icon
- "DevOps Superpowers"
- Connection to all quadrants

VISUAL ELEMENTS:
- Each quadrant distinctly colored
- Example prompts in quote/command style
- Icons for each use case
- Frequency/complexity indicators
- "Copy-ready prompts" feeling

FOOTER:
- "Start with these prompts, customize for your environment"
- Pro tip: "Be specific about your stack and requirements"

Style: Matrix/quadrant layout, actionable prompts visible, practical DevOps focus, suitable for quick reference and prompt ideas.
```

---

### Image 06-10: Troubleshooting Decision Tree

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-06-img-10-flow-troubleshooting.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 6.11 header "Troubleshooting Common Issues" (around line 1431) |
| **Alt Text** | "Decision tree for troubleshooting Claude Code issues: file access problems, slow responses, wrong changes, permission errors, crashes" |

**Prompt:**
```
A troubleshooting decision tree helping users diagnose and fix common Claude Code issues.

FLOWCHART STRUCTURE:

START NODE:
- "Having issues with Claude Code?"
- Branch to issue types

ISSUE SELECTOR (First Decision):
- "What's the problem?"
- Six branches for common issues

BRANCH 1 - "Can't See Files":
- Problem: Claude doesn't see files
- Decision tree:
  - Wrong directory? → Restart in project root
  - File outside allowed paths? → Check config allowed_paths
  - Gitignored? → Check .gitignore or .claudeignore
- Solution endpoint: "cd /project && claude"

BRANCH 2 - "Slow/Timing Out":
- Problem: Responses too slow
- Decision tree:
  - Context too large? → /clear or be more specific
  - Network issues? → Check api.anthropic.com connectivity
  - Rate limited? → Check /cost for rate status
- Solutions: Reduce context, switch model, check proxy

BRANCH 3 - "Wrong Changes":
- Problem: Claude makes incorrect changes
- Prevention flow:
  - Ask for plan first
  - Work incrementally
  - Use explicit file references
- Recovery: git reset, git stash, ask to revert

BRANCH 4 - "Permission Denied":
- Problem: Can't execute or write
- Decision tree:
  - Shell execution disabled? → Enable in /config
  - File permissions? → chmod +x or check ownership
  - Protected directory? → Create elsewhere, copy with sudo

BRANCH 5 - "Crashes/Freezes":
- Problem: Claude Code becomes unresponsive
- Recovery steps:
  - Ctrl+C → Try to cancel
  - Ctrl+Z then kill %1 → Force stop
  - Restart Claude Code
- Causes: Memory, corrupted session, filesystem issues

BRANCH 6 - "Changes Not Applied":
- Problem: Claude says done but nothing changed
- Diagnostics:
  - Approval missed? → Check for y/n prompt
  - File write-protected? → Check permissions
  - Auto-approve off? → Check settings

SOLUTION ENDPOINTS:
- Each branch leads to actionable solution
- Color-coded: Green for fixes, Blue for commands

QUICK COMMANDS BOX:
- /doctor - Diagnose config issues
- /help - Show all commands
- /config - Check settings
- claude --version - Verify installation

ESCALATION PATH:
- Still stuck? →
  - Check docs.anthropic.com
  - Search GitHub issues
  - File bug report if reproducible

VISUAL ELEMENTS:
- Clear problem → diagnostic → solution flow
- Color-coded by issue severity
- Quick commands readily visible
- "Most common" indicators on frequent issues

Style: Practical troubleshooting flowchart, diagnostic approach, actionable solutions, suitable for quick problem resolution.
```

📐 **RECOMMEND**: This could also be created as an interactive troubleshooting wizard using a web-based tool or decision tree software

---

## Chapter 07: Claude Code Intermediate

### Overview
- **Chapter Focus**: Configuration, custom commands/skills, IDE integration, browser mode, advanced workflows, session management
- **Total Images**: 9
- **Animation Candidates**: 1

---

### Image 07-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-01-header-claude-code-intermediate.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Leveling Up Your Claude Code Skills" |
| **Alt Text** | "Developer ascending skill levels with Claude Code, showing progression from basic terminal usage to advanced workflows with custom commands and IDE integration" |

**Prompt:**
```
A hero illustration representing the journey from basic Claude Code usage to intermediate mastery, showing skill progression and capability expansion.

VISUAL CONCEPT:
A "leveling up" visualization showing a developer ascending through layers of capability, each layer revealing more sophisticated features.

PROGRESSION LAYERS (bottom to top):

BASE LAYER - FUNDAMENTALS (already mastered):
- Simple terminal with basic commands
- Grayed out slightly (already covered)
- Foundation that everything builds on

LEVEL 1 - CONFIGURATION:
- Gear icons, settings files floating
- ~/.claude/config.json representation
- Color: Blue (foundation)

LEVEL 2 - CUSTOM COMMANDS:
- Multiple command cards/templates
- .claude/commands/ folder representation
- Reusable prompts visualization
- Color: Purple (customization)

LEVEL 3 - IDE INTEGRATION:
- Multiple IDE icons (VS Code, JetBrains, Vim)
- Connected to central Claude Code
- Bidirectional arrows
- Color: Green (integration)

LEVEL 4 - ADVANCED WORKFLOWS:
- Multi-step flow diagrams
- CI/CD pipeline representation
- Automated review symbols
- Color: Orange (automation)

CENTRAL FIGURE:
- Developer/engineer ascending the levels
- Each level unlocks new capabilities
- "Power-ups" or skill icons at each tier
- Achievement/progression feeling

FLOATING ELEMENTS:
- Code snippets
- Configuration fragments
- Workflow arrows
- Integration connectors

VISUAL STYLE:
- Gamification aesthetic (skill tree, progression)
- Professional but engaging
- Each layer visually distinct
- Upward momentum

Color palette: Progressive from cool blues at base to warm oranges at top, representing increasing capability and energy.

Style: Modern tech illustration with progression/leveling aesthetic, shows journey from basic to intermediate, engaging and motivating, suitable as chapter hero.
```

---

### Image 07-02: Configuration Hierarchy

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-02-diagram-config-hierarchy.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 7.1 "Configuration File Locations" (around line 52-63) |
| **Alt Text** | "Three-tier configuration hierarchy: Project-level (.claude/config.json), User-level (~/.claude/config.json), and Environment variables, with priority shown top to bottom" |

**Prompt:**
```
A hierarchical diagram showing how Claude Code configuration is resolved across different levels.

LAYOUT: Pyramid or layered structure showing configuration priority

TOP LAYER - HIGHEST PRIORITY (Environment Variables):
- Icon: Terminal with env variables
- Examples: ANTHROPIC_API_KEY, CLAUDE_CODE_MODEL
- Label: "Environment Variables (Override All)"
- Color: Red/orange (immediate override)
- Use case: "Temporary overrides, CI/CD, testing"

MIDDLE LAYER - PROJECT LEVEL:
- Icon: Folder with project icon
- Path shown: "./.claude/config.json"
- Label: "Project Configuration"
- Color: Purple
- Use case: "Team-shared settings, project-specific"
- Note: "Committed to git, shared with team"

BOTTOM LAYER - USER LEVEL:
- Icon: Home folder or user icon
- Path shown: "~/.claude/config.json"
- Label: "User Defaults"
- Color: Blue
- Use case: "Personal preferences, API keys"
- Note: "Not shared, your defaults"

OPTIONAL - SYSTEM LEVEL:
- Path shown: "/etc/claude/config.json"
- Faded/small: "Rarely used"
- Color: Gray

RESOLUTION FLOW:
- Arrow showing lookup order
- "Claude checks in order: Project → User → System"
- "Environment vars override at any level"

MERGE VISUALIZATION:
- Show how settings from different levels combine
- Later settings override earlier ones
- Visual merge/combine indicator

EXAMPLE CALLOUT:
```
Project: model = "haiku"
User:    model = "sonnet"
Env:     CLAUDE_CODE_MODEL = "opus"

Result:  model = "opus" (env wins)
```

Style: Clear hierarchy visualization, shows configuration resolution, practical for understanding which settings apply, professional documentation quality.
```

---

### Image 07-03: Auto-Approve Security Levels

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-03-compare-autoapprove-security.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 7.1 "Security Implications of Configuration" (around line 156-178) |
| **Alt Text** | "Three security profiles for auto-approve settings: Low Risk (development), Medium Risk (personal projects), and High Risk (production) with specific read/write/execute permissions" |

**Prompt:**
```
A three-column comparison showing auto-approve security configurations for different risk environments.

THREE COLUMNS:

COLUMN 1 - LOW RISK (Development Environment):
- Icon: Developer laptop, sandbox
- Color: Green (safe)
- Settings visualization:
  - read: true ✅ (green checkmark)
  - write: false ❌ (red X)
  - execute: false ❌ (red X)
- Risk indicator: Shield with checkmark
- Description: "You review writes and commands"
- Use case icons: Local development, learning, experimentation
- Safety level: RECOMMENDED DEFAULT

COLUMN 2 - MEDIUM RISK (Personal Projects):
- Icon: Personal computer, solo work
- Color: Yellow/amber (caution)
- Settings visualization:
  - read: true ✅
  - write: true ⚠️ (yellow warning)
  - execute: false ❌
- Risk indicator: Caution triangle
- Description: "Faster but risky - review commands"
- Use case icons: Personal repos, prototypes
- Warning: "Claude can modify any file"

COLUMN 3 - HIGH RISK (Production/Shared):
- Icon: Server rack, team collaboration
- Color: Red (maximum caution)
- Settings visualization:
  - read: false ❌
  - write: false ❌
  - execute: false ❌
- Risk indicator: Full lock
- Description: "Every action requires approval"
- Use case icons: Production systems, shared codebases
- Note: "Audit trail for all actions"

VISUAL ELEMENTS:
- Lock icons showing increasing restrictions
- Permission checkboxes clearly visible
- Risk gradient from green → yellow → red
- "Recommended for most users" highlight on Low Risk

REAL-WORLD WARNING BOX:
- Small callout: "A developer with write: true asked Claude to 'clean up configs'..."
- Brief cautionary tale icon

BOTTOM GUIDANCE:
- "Choose based on environment, not convenience"
- Quick selection guide

Style: Clear security comparison, risk-based color coding, actionable guidance, suitable for configuration decisions.
```

---

### Image 07-04: Custom Command Anatomy

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-04-diagram-command-anatomy.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 7.2 "Anatomy of Effective Custom Commands" header (around line 382) |
| **Alt Text** | "Annotated diagram of a custom command file showing frontmatter (name, description, arguments), prompt body, and output format specification" |

**Prompt:**
```
An annotated diagram showing the structure of an effective custom command file with callouts explaining each section.

LAYOUT: A mock command file (.md) with annotation callouts pointing to each section

COMMAND FILE VISUAL:
```
---
name: review
description: Comprehensive code review
arguments:
  - name: file
    description: File to review
    required: true
---

You are a senior DevOps engineer reviewing infrastructure code.

Our standards:
- All Terraform must use remote state
- Security groups must never allow 0.0.0.0/0 on SSH
- Resources must have Name tags

Review {{file}} and flag any violations.

Output format:
## Security Review for {{file}}
### Critical Issues (Must Fix)
- [Line X] Issue description
  Fix: Specific remediation
```

ANNOTATION CALLOUTS:

SECTION 1 - FRONTMATTER (top, between ---):
- Callout: "Metadata block"
- Sub-callouts:
  - name: "Command name (invoked as /review)"
  - description: "Shows in /commands list"
  - arguments: "Parameters you can pass"
    - required: true/false indicator
    - default values possible
- Color: Purple zone

SECTION 2 - CONTEXT (middle):
- Callout: "Role and constraints"
- Explains: "Tell Claude WHO it is and WHAT rules apply"
- "Your team's standards go here"
- Color: Blue zone

SECTION 3 - ACTION (body):
- Callout: "What to do"
- Shows: {{file}} placeholder highlighted
- "Use arguments with {{name}} syntax"
- Color: Orange zone

SECTION 4 - OUTPUT FORMAT (bottom):
- Callout: "Structured output template"
- "Ensures consistent, parseable results"
- Color: Green zone

BEST PRACTICES SIDEBAR:
- ✅ Single responsibility
- ✅ Context over instructions
- ✅ Parameterized (not hardcoded)
- ✅ Output format specified
- ❌ Don't over-constrain
- ❌ Don't script step-by-step

Style: Code editor aesthetic with annotation overlays, clear section boundaries, educational documentation quality.
```

---

### Image 07-05: Browser vs CLI Decision Matrix

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-05-compare-browser-vs-cli.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 7.3 "Decision Matrix Summary" (around line 964-977) |
| **Alt Text** | "Decision matrix comparing Browser (claude.ai) vs CLI (Claude Code) across factors: installation, quick tasks, multi-file changes, command execution, git integration" |

**Prompt:**
```
A comprehensive decision matrix comparing browser-based Claude (claude.ai) versus CLI Claude Code.

LAYOUT: Two-column comparison with factor rows

LEFT COLUMN - BROWSER (claude.ai):
- Header icon: Browser window
- Color scheme: Light blue/web aesthetic

RIGHT COLUMN - CLI (Claude Code):
- Header icon: Terminal window
- Color scheme: Dark/terminal green

COMPARISON ROWS (with icons):

1. INSTALLATION:
   - Browser: ✅ "Zero setup" (big green check)
   - CLI: ⚠️ "Requires npm/node" (yellow)

2. QUICK TASKS:
   - Browser: ✅ "Instant access"
   - CLI: ➖ "Neutral"

3. MULTI-FILE CHANGES:
   - Browser: ❌ "Manual sync" (red X)
   - CLI: ✅ "Automatic"

4. RUNNING COMMANDS:
   - Browser: ❌ "Not possible"
   - CLI: ✅ "Full shell access"

5. VISUAL LEARNING:
   - Browser: ✅ "Syntax highlighting, rich UI"
   - CLI: ➖ "Terminal-only"

6. GIT INTEGRATION:
   - Browser: ❌ "Manual"
   - CLI: ✅ "Automatic"

7. AUTOMATION/CI:
   - Browser: ❌ "Not suitable"
   - CLI: ✅ "Scriptable"

8. TEAM SHARING:
   - Browser: ✅ "Shareable URLs"
   - CLI: ❌ "Local only"

SCENARIO BOXES:
- Box 1: "Quick code review" → BROWSER
- Box 2: "Multi-file refactoring" → CLI
- Box 3: "Learning new codebase" → BROWSER
- Box 4: "Incident response" → CLI

DECISION RULE:
- "If you'll run commands or modify >2-3 files → CLI"
- "Otherwise → Browser is often faster"

VISUAL ELEMENTS:
- Clear check/X icons
- Color coding (green for strength, red for weakness)
- Scenario-based recommendations
- "Choose based on task" emphasis

Style: Clean comparison matrix, actionable decision guidance, professional documentation style.
```

---

### Image 07-06: IDE Integration Comparison

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-06-compare-ide-integration.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 7.4 "Comparison Matrix: All IDE Options" (around line 1062-1073) |
| **Alt Text** | "Five-column comparison of IDE integration options: VS Code Extension, JetBrains Plugin, Vim/Neovim Plugin, CLI + tmux, and Browser" |

**Prompt:**
```
A multi-column comparison showing different ways to integrate Claude Code with development environments.

FIVE COLUMNS:

COLUMN 1 - VS CODE EXTENSION:
- Icon: VS Code logo stylized
- Setup: "Low (1-click)"
- Key features:
  - ✅ Full workspace context
  - ✅ Inline suggestions
  - ✅ Visual diff views
  - ✅ Permission badges
- Best for: "General development"
- Color: Blue (VS Code)

COLUMN 2 - JETBRAINS PLUGIN:
- Icon: JetBrains logo stylized
- Setup: "Low (marketplace)"
- Key features:
  - ✅ Full project context
  - ✅ Inline suggestions
  - ✅ Integrated debugging
  - ✅ Refactoring tools
- Best for: "IntelliJ/PyCharm users"
- Color: Orange (JetBrains)

COLUMN 3 - VIM/NEOVIM PLUGIN:
- Icon: Vim logo stylized
- Setup: "Medium (config)"
- Key features:
  - ✅ Fastest performance
  - ✅ Full project context
  - ⚠️ Limited inline suggestions
  - ✅ Custom keybindings
- Best for: "Vim power users"
- Color: Green (Vim)

COLUMN 4 - CLI + TMUX:
- Icon: Terminal with splits
- Setup: "Low (native)"
- Key features:
  - ✅ Editor-agnostic
  - ✅ Full shell access
  - ❌ No inline suggestions
  - ✅ Fastest overall
- Best for: "Terminal power users"
- Color: Purple (terminal)

COLUMN 5 - BROWSER:
- Icon: Web browser
- Setup: "None"
- Key features:
  - ❌ Manual upload
  - ❌ No commands
  - ✅ Shareable sessions
  - ✅ Works anywhere
- Best for: "Quick reviews"
- Color: Light blue (web)

DECISION GUIDANCE ROW:
- "Choose based on your primary editor and workflow needs"

USAGE PATTERNS:
- "Daily coding" → IDE Extension
- "Automation" → CLI
- "Team sharing" → Browser

Style: Clean multi-column comparison, icon-based features, actionable selection guidance.
```

---

### Image 07-07: Advanced Workflow Patterns

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-07-flow-advanced-workflows.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Before section 7.5 "Advanced Workflows" (around line 1423) |
| **Alt Text** | "Four advanced workflow patterns: Multi-File Refactoring, Infrastructure Migration, Automated Code Review, and Incident Response with flow indicators" |

**Prompt:**
```
A four-quadrant diagram showing the four advanced workflows covered in the chapter.

FOUR QUADRANTS:

QUADRANT 1 - MULTI-FILE REFACTORING (Top-Left):
- Icon: Multiple files with arrows/changes
- Color: Blue
- Flow visualization:
  1. Understand current state
  2. Plan the changes
  3. Execute incrementally
  4. Verify with tests
  5. Cleanup
- Key benefit: "Context carryover across files"
- Example: "JWT migration across 15 files"

QUADRANT 2 - INFRASTRUCTURE MIGRATION (Top-Right):
- Icon: Cloud/servers with migration arrows
- Color: Purple
- Flow visualization:
  1. Document current state
  2. Plan migration
  3. Create new infrastructure
  4. Create K8s manifests
  5. Test plan
- Key benefit: "Claude maintains architecture knowledge"
- Example: "EC2 to EKS migration"

QUADRANT 3 - AUTOMATED CODE REVIEW (Bottom-Left):
- Icon: PR/code review symbols
- Color: Green
- Flow visualization:
  1. PR triggers workflow
  2. Claude analyzes changes
  3. Security + quality checks
  4. Report generated
  5. Posted as comment
- Key benefit: "Consistent reviews in CI/CD"
- Example: "GitHub Actions integration"

QUADRANT 4 - INCIDENT RESPONSE (Bottom-Right):
- Icon: Alert/fire/incident symbols
- Color: Orange/red
- Flow visualization:
  1. Gather information
  2. Initial assessment
  3. Diagnostic steps
  4. Recommended actions
- Key benefit: "Situational awareness maintained"
- Example: "Pod crash investigation"

CENTER HUB:
- Claude Code icon
- "Advanced Workflows"
- Connection to all quadrants

KEY INSIGHT CALLOUT:
- "Context carryover = Claude remembers throughout"
- "No need to re-explain your project"

Style: Clean quadrant layout, workflow flows visible in each, shows capability breadth, professional documentation quality.
```

---

### Image 07-08: CI/CD Review Pipeline

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-08-flow-cicd-review-pipeline.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 7.5 Workflow 3 "Automated Code Review Pipeline" (around line 1642) |
| **Alt Text** | "GitHub Actions workflow: PR Created → Checkout Code → Run Claude Review → Parse Results → Post Comment → Status Check" |

**Prompt:**
```
A horizontal flow diagram showing how Claude Code integrates into a CI/CD pipeline for automated code review.

FLOW (left to right):

TRIGGER:
- Icon: GitHub PR icon
- Label: "PR Created"
- Event: pull_request
- Color: GitHub dark

STEP 1 - CHECKOUT:
- Icon: Download/clone
- Label: "Checkout Code"
- Action: actions/checkout@v4
- Note: "fetch-depth: 0 for full history"

STEP 2 - SETUP:
- Icon: npm/install
- Label: "Setup Claude Code"
- Action: npm install
- Shows: API key from secrets

STEP 3 - RUN REVIEW:
- Icon: Claude Code / AI brain
- Label: "Run Claude Review"
- Command: claude --output "/pr-review"
- Shows: Custom command being invoked
- Color: Anthropic orange

STEP 4 - PARSE OUTPUT:
- Icon: Document analysis
- Label: "Parse Results"
- Shows: pr-review.md generated
- Critical issues check

STEP 5 - POST COMMENT:
- Icon: Comment bubble
- Label: "Post to PR"
- Action: github-script
- Shows: Review posted as PR comment

STEP 6 - STATUS CHECK:
- Icon: Check/X status
- Label: "Status Check"
- Conditional: "Critical issues? → Fail"
- Green check or red X based on results

VISUAL ELEMENTS:
- Pipeline style with arrows
- Each step clearly bounded
- GitHub Actions aesthetic
- Success/failure paths shown

SAMPLE OUTPUT BOX:
- Mini preview of review comment format
- Security findings summary
- Code quality notes

ERROR HANDLING NOTE:
- Retry logic for rate limiting
- Graceful failure handling

Style: CI/CD pipeline visualization, GitHub Actions aesthetic, shows end-to-end flow, professional DevOps documentation style.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing the pipeline executing step by step, with the review being generated and posted.

---

### Image 07-09: Session Management

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-07-img-09-flow-session-management.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 7.6 "Session Management" header (around line 1983) |
| **Alt Text** | "Session management workflow showing /rename to name sessions, /resume to continue work, and /save//load for export/import" |

**Prompt:**
```
A workflow diagram illustrating Claude Code session management features.

LAYOUT: Central session icon with workflows radiating outward

CENTER:
- Session icon (conversation/history symbol)
- "Claude Code Sessions"
- Auto-save indicator

WORKFLOW 1 - NAMING & RESUMING (Primary):
- Path: Work → /rename → Name assigned → Later → /resume
- Flow:
  1. Working on feature
  2. "/rename my-feature-work"
  3. Session named (saved automatically)
  4. Close/exit
  5. Next day: "/resume my-feature-work"
  6. Continue with full context
- Color: Green (recommended workflow)
- Label: "New in 2.0.64"

WORKFLOW 2 - SAVE/LOAD (Legacy):
- Path: Work → /save → ~/.claude/sessions/ → /load
- Flow:
  1. "/save feature-auth-day3"
  2. Session saved to disk
  3. "/sessions" to list
  4. "/load feature-auth-day3"
- Color: Gray/muted (still supported)
- Label: "Legacy (still works)"

WORKFLOW 3 - EXPORT/SHARE:
- Path: /export → JSON file → Share → Import
- Flow:
  1. "/export security-audit audit.json"
  2. Share with teammate
  3. Teammate imports: claude --import audit.json
  4. Continue investigation
- Color: Blue (collaboration)
- Label: "Team sharing"

BEST PRACTICES BOX:
- "Save at key milestones"
- "Before risky changes"
- "After tests pass"
- Icons for each tip

VISUAL ELEMENTS:
- Timeline/calendar indicators for resuming later
- File system representation for storage
- Team collaboration icons for sharing

SESSION LIST MOCKUP:
- Small terminal showing /sessions output
- Named sessions visible

Style: Clean workflow visualization, multiple usage patterns shown, practical session management guidance.
```

---

## Chapter 08: Skills and Subagents

### Overview
- **Chapter Focus**: Agentic capabilities, skills system, sub-agents, task delegation, advanced autonomous workflows
- **Total Images**: 8
- **Animation Candidates**: 2

---

### Image 08-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-01-header-skills-subagents.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Extending Claude Code with Custom Capabilities" |
| **Alt Text** | "Claude Code as an orchestrator with multiple specialized skills and sub-agents working in parallel, representing autonomous DevOps capabilities" |

**Prompt:**
```
A dynamic hero illustration showing Claude Code as an intelligent orchestrator coordinating multiple specialized skills and sub-agents.

CENTRAL COMPOSITION:
Claude Code represented as a central intelligence hub, with multiple specialized agents and skill modules radiating outward.

CENTRAL HUB - CLAUDE CODE ORCHESTRATOR:
- Large central node representing the main Claude Code agent
- Pulsing energy/activity indicators
- "Brain" or intelligence visualization
- Command and coordination signals emanating outward
- Color: Core Anthropic orange

SURROUNDING SKILLS (First Ring):
- Multiple skill modules as specialized cards/nodes:
  - Kubernetes skill (K8s logo stylized, manifests)
  - Terraform skill (purple, infrastructure diagrams)
  - Docker skill (whale icon, container boxes)
  - Security skill (shield, lock icons)
  - CI/CD skill (pipeline arrows)
- Each skill glows with its domain color
- Connection lines to central hub

SUB-AGENTS (Second Ring):
- Multiple autonomous workers in action:
  - Explorer agent (magnifying glass, file trees)
  - Planner agent (flowchart, checklist)
  - Code writer agent (code brackets, pencil)
  - Test agent (checkmarks, test tubes)
  - Reviewer agent (eye, security scan)
- Each sub-agent shown actively working on tasks
- Parallel execution visual (simultaneous activity)

WORKFLOW CONNECTIONS:
- Data/task flow lines between components
- Coordination signals between agents
- Skill knowledge feeding into agents
- Results flowing back to central hub

BACKGROUND ELEMENTS:
- Codebase structure subtly visible
- DevOps infrastructure suggestions
- Parallel processing visualization
- Cloud/servers in distance

VISUAL METAPHORS:
- Orchestra conductor (orchestration)
- Multi-threaded processing (parallelism)
- Expertise modules (skills)
- Autonomous workers (sub-agents)

Color palette: Anthropic orange for central hub, domain colors for each skill (K8s blue, Terraform purple, Docker blue, Security green, CI/CD orange), muted versions for sub-agents.

Style: Dynamic tech illustration showing orchestration and parallel capability, professional yet engaging, represents the power of extending Claude Code with skills and sub-agents.
```

---

### Image 08-02: Agentic Behavior Model

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-02-flow-agentic-behavior.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | Replace or accompany the ASCII agentic behavior model in section 8.1 (around line 89-140) |
| **Alt Text** | "Five-step agentic behavior loop: Perceive (read files, understand context) → Plan (reason, identify steps) → Act (execute, edit) → Verify (test, validate) → Iterate (fix, refine)" |

**Prompt:**
```
A circular or vertical flow diagram showing the five stages of agentic behavior in Claude Code.

FLOW STRUCTURE:

ENTRY POINT:
- "Your Request"
- Example: "Add caching to the user endpoint"
- User icon

STAGE 1 - PERCEIVE:
- Icon: Eye / magnifying glass over code
- Color: Blue (observation/input)
- Actions:
  - "Read existing code"
  - "Understand project structure"
  - "Identify patterns used"
- Visual: Files being scanned, structure being mapped

STAGE 2 - PLAN:
- Icon: Brain / flowchart / lightbulb
- Color: Purple (thinking)
- Actions:
  - "Decide on caching strategy"
  - "Identify files to modify"
  - "Plan implementation steps"
- Visual: Decision tree forming, checklist appearing

STAGE 3 - ACT:
- Icon: Wrench / code brackets / terminal
- Color: Orange (execution)
- Actions:
  - "Edit code files"
  - "Add dependencies"
  - "Update configurations"
- Visual: Files being modified, code being written

STAGE 4 - VERIFY:
- Icon: Checkmark / test tube / validation
- Color: Green (validation)
- Actions:
  - "Run tests"
  - "Check for errors"
  - "Validate changes work"
- Visual: Tests running, results appearing

STAGE 5 - ITERATE (conditional loop):
- Icon: Loop arrow / refinement
- Color: Cyan (refinement)
- Actions:
  - "Fix any issues found"
  - "Refine implementation"
  - "Re-verify"
- Visual: Loop back to earlier stages if needed
- Decision point: "Issues found?" → Yes: Loop back / No: Complete

COMPLETION:
- "Task Complete"
- Summary/result indication
- Checkmark

LOOP VISUALIZATION:
- Clear arrow showing iteration back from Verify/Iterate to earlier stages
- Most common loop: Act → Verify → fix issues → Act again

HUMAN IN THE LOOP INDICATOR:
- Small callout: "You approve actions along the way"
- Human checkpoint between Plan and Act

Style: Clear lifecycle flow, shows autonomous yet controlled execution, emphasizes the verify/iterate capability that makes Claude Code reliable.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing the cycle in motion, with an example task progressing through each stage.

---

### Image 08-03: Skills System Overview

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-03-diagram-skills-system.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII skills system diagram in section 8.2 (around line 192-220) |
| **Alt Text** | "Skills system architecture showing four skill cards (Kubernetes, Terraform, Docker, CI/CD) each with specialized knowledge, tools, and patterns" |

**Prompt:**
```
A modular diagram showing the skills system architecture with example skill cards.

LAYOUT: Central concept with skill card examples

CENTRAL CONCEPT:
- "Skills = Specialized Knowledge + Tools + Patterns"
- Claude Code core receiving skills
- Skills enhance capabilities

SKILL CARDS (Four Examples):

CARD 1 - KUBERNETES SKILL:
- Icon: K8s wheel logo stylized
- Color: Kubernetes blue
- Capabilities list:
  - "K8s manifests"
  - "Helm charts"
  - "kubectl commands"
  - "Debugging pods"
- Visual: Mini manifest snippet

CARD 2 - TERRAFORM SKILL:
- Icon: Terraform logo stylized
- Color: Terraform purple
- Capabilities list:
  - "AWS/GCP/Azure"
  - "Module patterns"
  - "State management"
  - "Best practices"
- Visual: Mini .tf snippet

CARD 3 - DOCKER SKILL:
- Icon: Docker whale stylized
- Color: Docker blue
- Capabilities list:
  - "Dockerfile optimization"
  - "Multi-stage builds"
  - "Docker Compose"
  - "Security scanning"
- Visual: Mini Dockerfile snippet

CARD 4 - CI/CD SKILL:
- Icon: Pipeline arrows
- Color: Orange
- Capabilities list:
  - "GitHub Actions"
  - "GitLab CI"
  - "Jenkins"
  - "ArgoCD"
- Visual: Mini workflow snippet

SKILL COMBINATION INDICATOR:
- Show how skills can be combined
- "/skill kubernetes terraform"
- Visual: K8s + Terraform cards merging

HOT-RELOAD BADGE:
- "Hot-reloaded" indicator
- "Available immediately without restart"
- Lightning bolt icon

CUSTOM SKILLS SECTION:
- "Create your own" indicator
- Points to ~/.claude/skills/ or .claude/skills/
- "Team-specific knowledge"

Style: Clean skill cards layout, each card visually distinct, shows modularity and extensibility of skills system.
```

---

### Image 08-04: Sub-Agent Architecture

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-04-diagram-subagent-architecture.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Replace or accompany the ASCII sub-agent architecture in section 8.3 (around line 398-429) |
| **Alt Text** | "Main agent as coordinator with three sub-agents (Code Review, Test Writer, Docs Writer) working in parallel, results aggregating back to final output" |

**Prompt:**
```
A hierarchical diagram showing how the main Claude Code agent spawns and coordinates sub-agents.

ARCHITECTURE:

TOP - MAIN AGENT (Coordinator):
- Large node: "Main Agent (Coordinator)"
- Icon: Central brain/hub
- Shows: Receiving user request, delegating tasks
- Color: Anthropic orange

DISTRIBUTION ARROWS:
- Three arrows pointing down from coordinator
- Each labeled with task being delegated
- Shows parallel distribution

MIDDLE - SUB-AGENTS (Parallel Workers):

SUB-AGENT 1 - CODE REVIEWER:
- Icon: Eye + code
- Color: Red/orange (review)
- Tasks:
  - "Security analysis"
  - "Quality check"
  - "Style review"
- Working indicator (progress bar or spinner)

SUB-AGENT 2 - TEST WRITER:
- Icon: Checkmark + code
- Color: Green (testing)
- Tasks:
  - "Unit tests"
  - "Integration tests"
  - "E2E tests"
- Working indicator

SUB-AGENT 3 - DOCS WRITER:
- Icon: Document + pencil
- Color: Blue (documentation)
- Tasks:
  - "README updates"
  - "API docs"
  - "Code comments"
- Working indicator

PARALLEL EXECUTION VISUAL:
- Clock/timeline showing simultaneous work
- "Parallel processing" label
- Time savings indicator

AGGREGATION ARROWS:
- Three arrows pointing down from sub-agents
- Converging to result node

BOTTOM - AGGREGATED RESULT:
- Node: "Final Result (Aggregated)"
- Shows: Combined output from all sub-agents
- Color: Green (complete)

CONTEXT FORKING CALLOUT:
- Small indicator: "Each sub-agent has own context"
- "context: fork" badge
- Shows isolation benefit

BENEFITS SIDEBAR:
- "Parallel execution = faster completion"
- "Isolated contexts = no pollution"
- "Specialized focus = better results"

Style: Clear hierarchical flow, shows parallelism and coordination, professional documentation quality.
```

---

### Image 08-05: Sub-Agent Types

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-05-compare-subagent-types.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 8.3 "Sub-Agent Types" (around line 453-503) |
| **Alt Text** | "Five sub-agent types: Explorer (codebase navigation), Planner (implementation design), Code Writer (feature development), Test Agent (quality assurance), Reviewer (code analysis)" |

**Prompt:**
```
A five-column comparison showing the different types of sub-agents available in Claude Code.

FIVE COLUMNS:

COLUMN 1 - EXPLORER AGENT:
- Icon: Magnifying glass over file tree
- Color: Blue (discovery)
- Purpose: "Explore and understand codebases"
- Capabilities:
  - "Fast file searching"
  - "Pattern recognition"
  - "Architecture mapping"
- Use case: "Where is X implemented?"
- Example prompt: "Find all authentication-related code"
- Speed: Fast

COLUMN 2 - PLANNER AGENT:
- Icon: Flowchart / strategy board
- Color: Purple (planning)
- Purpose: "Create implementation plans"
- Capabilities:
  - "Break down complex tasks"
  - "Identify dependencies"
  - "Estimate complexity"
- Use case: "Plan a large refactor"
- Example prompt: "Plan migration from REST to GraphQL"
- Speed: Medium

COLUMN 3 - CODE WRITER AGENT:
- Icon: Code brackets + pencil
- Color: Orange (creation)
- Purpose: "Write and modify code"
- Capabilities:
  - "Generate new code"
  - "Refactor existing code"
  - "Follow patterns"
- Use case: "Implement features"
- Example prompt: "Create rate limiting middleware"
- Speed: Variable

COLUMN 4 - TEST AGENT:
- Icon: Checkmark + test tube
- Color: Green (validation)
- Purpose: "Create and run tests"
- Capabilities:
  - "Generate unit tests"
  - "Create integration tests"
  - "Run test suites"
- Use case: "Ensure code quality"
- Example prompt: "Write tests for new auth module"
- Speed: Medium

COLUMN 5 - REVIEWER AGENT:
- Icon: Eye + shield
- Color: Red (analysis)
- Purpose: "Review code for issues"
- Capabilities:
  - "Security analysis"
  - "Performance review"
  - "Best practice checking"
- Use case: "Code review automation"
- Example prompt: "Audit authentication for vulnerabilities"
- Speed: Medium

BOTTOM ROW - COMBINATION HINT:
- "Combine agents for complex workflows"
- Example: "Explorer → Planner → Code Writer → Test → Reviewer"

Style: Clean comparison cards, each type visually distinct, shows capability spectrum, actionable agent selection guidance.
```

---

### Image 08-06: Multi-Agent Workflow Example

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-06-flow-multiagent-workflow.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 8.4 "Advanced Agentic Workflows" (around line 546) |
| **Alt Text** | "Production readiness workflow with four parallel agents: Security Audit, Performance Analysis, Test Coverage, and Documentation Review, feeding into aggregated report" |

**Prompt:**
```
A workflow diagram showing a realistic multi-agent workflow for production readiness checking.

WORKFLOW: Production Readiness Check

ENTRY:
- User request: "Prepare this service for production deployment"
- Timestamp indicator: Start time

ORCHESTRATOR DECISION:
- Claude Code analyzes request
- Decides on parallel checks needed
- Spawns sub-agents

PARALLEL EXECUTION PHASE:
- Four agents working simultaneously
- Visual: Timeline showing parallel bars

AGENT 1 - SECURITY AUDIT:
- Icon: Shield + magnifying glass
- Tasks:
  - "Scan for hardcoded secrets"
  - "Check for vulnerabilities"
  - "Review auth/authz"
- Progress: In progress...
- Output: Security findings report

AGENT 2 - PERFORMANCE ANALYSIS:
- Icon: Speedometer
- Tasks:
  - "Analyze resource usage"
  - "Check for N+1 queries"
  - "Review memory patterns"
- Progress: In progress...
- Output: Performance report

AGENT 3 - TEST COVERAGE:
- Icon: Checkmark grid
- Tasks:
  - "Run test suite"
  - "Calculate coverage %"
  - "Identify untested paths"
- Progress: In progress...
- Output: Coverage report (e.g., 85%)

AGENT 4 - DOCUMENTATION REVIEW:
- Icon: Document + checkmark
- Tasks:
  - "Check README completeness"
  - "Verify API docs"
  - "Review inline comments"
- Progress: In progress...
- Output: Docs completeness score

AGGREGATION PHASE:
- All reports feeding into central aggregator
- Claude Code synthesizing findings

FINAL OUTPUT:
- "Production Readiness Report"
- Sections from each agent
- Overall recommendation: GO / NO-GO
- Issues to address before deployment

TIMELINE INDICATOR:
- Shows time saved via parallelism
- "Sequential: ~15 min → Parallel: ~5 min"

Style: Real-world workflow, shows practical benefit of multi-agent orchestration, professional DevOps documentation quality.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing the parallel agents working and their results aggregating into the final report.

---

### Image 08-07: Task Tool Visualization

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-07-diagram-task-tool.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 8.5 "Understanding the Task Tool" (around line 679-716) |
| **Alt Text** | "Task Tool interface showing parameters: subagent_type (Explore, Plan, general-purpose), prompt, model selection, and example spawning flow" |

**Prompt:**
```
A technical diagram showing the Task Tool interface for spawning sub-agents.

LAYOUT: API-style documentation with examples

TASK TOOL INTERFACE:

HEADER:
- "Task Tool: Sub-Agent Spawning Mechanism"
- Tool icon

PARAMETERS SECTION:

PARAMETER 1 - subagent_type:
- Type: enum (dropdown visualization)
- Options with icons:
  - "general-purpose" - Multi-step tasks
  - "Explore" - Codebase exploration
  - "Plan" - Implementation planning
  - "code-reviewer" - Code review (if configured)
- Color coding for each type

PARAMETER 2 - prompt:
- Type: string
- Description: "The task for the agent to perform"
- Example shown in input field

PARAMETER 3 - model (optional):
- Type: enum
- Options:
  - "sonnet" (default) - Balanced
  - "opus" - Complex reasoning
  - "haiku" - Fast, simple tasks
- Cost/speed indicators for each

BEHAVIOR SECTION:
- Bullet points with icons:
  - "Sub-agents run autonomously"
  - "Report back when complete"
  - "Can be run in parallel"
  - "Each has its own context"

EXAMPLE INVOCATIONS:

EXAMPLE 1 - EXPLORE:
Task(
  subagent_type="Explore",
  prompt="Find auth-related code"
)
- Shows: Spawns explorer, returns findings

EXAMPLE 2 - PLAN:
Task(
  subagent_type="Plan",
  prompt="Design caching strategy"
)
- Shows: Spawns planner, returns plan

EXAMPLE 3 - GENERAL:
Task(
  subagent_type="general-purpose",
  prompt="Update all tests"
)
- Shows: Spawns worker, executes task

SPAWN FLOW VISUALIZATION:
- Main agent → Task Tool call → Sub-agent spawned → Works autonomously → Returns result

Style: Technical API documentation aesthetic, clear parameter definitions, practical examples, suitable for understanding Task Tool usage.
```

---

### Image 08-08: Context Forking Concept

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-08-img-08-concept-context-forking.png` |
| **Type** | Concept |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 8.2 "Sub-Agent Context Forking" (around line 367-388) |
| **Alt Text** | "Context forking visualization: Main conversation preserved while skill runs in isolated sub-agent context, results returning without pollution" |

**Prompt:**
```
A conceptual diagram explaining context forking for sub-agents.

LAYOUT: Before/After or Split comparison

WITHOUT CONTEXT FORKING (Problem):
- Main conversation context shown as container
- Skill execution happening inside same context
- Visual pollution:
  - Context growing large
  - Irrelevant information mixing in
  - "Context pollution" label
- Result: Slower responses, confused context

WITH CONTEXT FORKING (Solution):
- Main conversation context preserved (clean)
- Fork indicator: context: fork
- Separate sub-agent context spawned:
  - Isolated container
  - Skill runs inside
  - Own workspace
- Results channel:
  - Only final results return to main context
  - Main context stays clean
- Benefits shown:
  - "Isolated execution"
  - "Clean main context"
  - "Long-running tasks don't pollute"

SKILL FILE SNIPPET:
---
name: security-audit
context: fork  # Key setting
---

FORK VISUALIZATION:
- Tree branch metaphor
- Main trunk = main conversation
- Branch = forked sub-agent
- Graft = results returning

USE CASE EXAMPLES:
- "Long-running security scans"
- "Resource-intensive analysis"
- "Tasks generating lots of intermediate output"

VISUAL ELEMENTS:
- Container/sandbox imagery
- Clean vs cluttered contexts
- Fork/merge indicators

Style: Clear conceptual explanation, shows benefit of isolation, suitable for understanding when to use context: fork.
```

---

## Chapter 09: Hooks and Advanced Features

### Overview
- **Chapter Focus**: Hooks system for automation, memory management, CI/CD integration, professional best practices
- **Total Images**: 7
- **Animation Candidates**: 1

---

### Image 09-01: Chapter Header

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-09-img-01-header-hooks-advanced.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title, before "Automation, CI/CD Integration, and Professional Best Practices" |
| **Alt Text** | "Claude Code as an automation platform with hooks triggering workflows, CI/CD pipelines connecting, and memory/context management symbols" |

**Prompt:**
```
A hero illustration showing Claude Code transformed into a full automation platform through hooks, memory, and CI/CD integration.

CENTRAL CONCEPT:
Claude Code at the center, but now surrounded by automation infrastructure - hooks, pipelines, memory systems, and integration points.

MAIN VISUAL:
Claude Code represented as a central processing hub with multiple automation layers:

HOOKS LAYER (surrounding the core):
- Event trigger points (lightning bolts, hooks icons)
- Pre_edit, post_edit, pre_command hooks visualized as intercept points
- Actions being triggered automatically
- Color: Orange/amber for triggers

MEMORY LAYER (above):
- Brain/memory icon
- Long-term storage visualization
- Facts, patterns, conventions floating
- Persistent across sessions indicator
- Color: Purple for memory

CI/CD LAYER (below):
- Pipeline visualization (GitHub Actions, GitLab CI)
- Automated PR reviews
- Test generation symbols
- Deployment arrows
- Color: Green for automation

INTEGRATION POINTS (sides):
- Connection to external systems
- API connections
- Git integrations
- Environment variable flows

WORKFLOW ANIMATIONS:
- Arrows showing automated flows
- Events triggering actions
- Results feeding back
- Continuous loop indication

VISUAL METAPHORS:
- Factory automation (hooks as assembly line triggers)
- Neural network (memory as persistent knowledge)
- Pipeline (CI/CD as continuous flow)
- Control panel (professional management)

BACKGROUND:
- Professional DevOps environment
- Infrastructure hints (servers, clouds)
- Code/terminal aesthetic

Color palette: Anthropic orange for core, amber for hooks/triggers, purple for memory, green for CI/CD success, blue for integrations.

Style: Technical automation platform visualization, shows transformation from interactive tool to production automation system, professional and capable.
```

---

### Image 09-02: Hooks System Flow

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-09-img-02-flow-hooks-system.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 9.1 "What are Hooks?" (around line 48-94) |
| **Alt Text** | "Hooks workflow showing six event types (pre_edit, post_edit, pre_command, post_test, session_start, session_end) with their trigger points and example actions" |

**Prompt:**
```
A workflow diagram showing the hooks system with event types and their trigger points.

LAYOUT: Central Claude Code workflow with hook intercept points

MAIN WORKFLOW (horizontal center):
- "Session Start" → "Read/Understand" → "Edit Files" → "Run Commands" → "Run Tests" → "Session End"
- This represents the normal Claude Code workflow

HOOK INTERCEPT POINTS (above and below main flow):

HOOK 1 - SESSION_START:
- Trigger point: Session begins
- Position: At workflow start
- Example action: "git status"
- Icon: Play button / session icon
- Color: Blue

HOOK 2 - PRE_EDIT:
- Trigger point: Before file modification
- Position: Before "Edit Files" step
- Example action: "cp {{file}} {{file}}.backup"
- Icon: Save/backup icon
- Color: Orange (warning/prepare)

HOOK 3 - POST_EDIT:
- Trigger point: After file modification
- Position: After "Edit Files" step
- Example actions:
  - "prettier --write {{file}}" (JS/TS)
  - "black {{file}}" (Python)
  - "gitleaks detect" (security)
- Icon: Format/check icon
- Color: Green (success/validate)

HOOK 4 - PRE_COMMAND:
- Trigger point: Before command execution
- Position: Before "Run Commands" step
- Example action: "echo '{{command}}' >> log"
- Can also: Block dangerous commands
- Icon: Shield/filter icon
- Color: Red (security gate)

HOOK 5 - POST_TEST:
- Trigger point: After tests complete
- Position: After "Run Tests" step
- Example action: "coverage report --fail-under=80"
- Icon: Checkmark/report icon
- Color: Green

HOOK 6 - SESSION_END:
- Trigger point: Session closing
- Position: At workflow end
- Example action: "git diff --stat"
- Icon: Stop/summary icon
- Color: Blue

YAML SNIPPET:
- Small example of hooks.yaml structure
- Shows how hooks are configured

TIMEOUT BADGE:
- "10-minute timeout (v2.1.3)"
- Shows hook can run complex operations

Style: Clear workflow with intercept points, shows hook timing and purpose, practical for understanding when hooks fire.
```

---

### Image 09-03: DevOps Hook Use Cases

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-09-img-03-info-devops-hooks.png` |
| **Type** | Info (Infographic) |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 9.1 "Hook Use Cases for DevOps" (around line 96-133) |
| **Alt Text** | "Five DevOps hook categories: Infrastructure Safety (terraform destroy protection), K8s Validation (kubeval), Security Scanning (gitleaks), Docker Linting (hadolint), Terraform Formatting (terraform fmt)" |

**Prompt:**
```
An infographic showing practical DevOps hook use cases with examples.

LAYOUT: Five category cards/sections

CARD 1 - INFRASTRUCTURE SAFETY:
- Icon: Shield + terraform logo
- Color: Red (danger prevention)
- Hook type: pre_command
- Use case: "Confirm destructive commands"
- Example: Detect "terraform destroy" and require confirmation
- Visual: Warning dialog simulation
- Impact: "Prevents accidental infrastructure deletion"

CARD 2 - KUBERNETES VALIDATION:
- Icon: K8s logo + checkmark
- Color: Blue (K8s)
- Hook type: post_edit
- Use case: "Validate K8s manifests on save"
- Example: Run kubeval on *.yaml files
- Visual: Manifest being validated
- Impact: "Catch errors before deployment"

CARD 3 - SECURITY SCANNING:
- Icon: Lock + magnifying glass
- Color: Green (security)
- Hook type: post_edit
- Use case: "Scan for secrets in code"
- Example: Run gitleaks on modified files
- Visual: Secret detection alert
- Impact: "Prevent credential exposure"

CARD 4 - DOCKER LINTING:
- Icon: Docker whale + lint icon
- Color: Docker blue
- Hook type: post_edit
- Use case: "Lint Dockerfiles"
- Example: Run hadolint on Dockerfile changes
- Visual: Best practice suggestions
- Impact: "Ensure container best practices"

CARD 5 - TERRAFORM FORMATTING:
- Icon: Terraform logo + format icon
- Color: Purple (Terraform)
- Hook type: post_edit
- Use case: "Auto-format .tf files"
- Example: Run terraform fmt on save
- Visual: Code being formatted
- Impact: "Consistent infrastructure code"

CENTER INSIGHT:
- "Set up once, benefit forever"
- "Automated quality gates"

COMMAND LOGGING BONUS:
- Small callout: pre_command logging for audit trails
- "Log all actions for compliance"

Style: Practical use case cards, DevOps-focused, shows real commands and benefits, actionable reference.
```

**🎬 ANIMATION CANDIDATE**: This could be an animated GIF showing a file being edited, then hooks automatically triggering (formatting, scanning, validating).

---

### Image 09-04: Memory and Context Management

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-09-img-04-diagram-memory-context.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 9.2 "Long-Term Memory" (around line 137-175) |
| **Alt Text** | "Memory configuration with three sections: Facts (project knowledge), Conventions (naming, architecture), and Context Prioritization (file importance levels)" |

**Prompt:**
```
A diagram showing how memory and context configuration enhances Claude Code's understanding.

LAYOUT: Three connected sections feeding into Claude Code

SECTION 1 - FACTS (memory.yaml):
- Icon: Brain / lightbulb
- Color: Purple (knowledge)
- Content types:
  - "Project uses Django 4.2 with PostgreSQL"
  - "GitFlow branching strategy"
  - "Production needs two approvals"
  - "Main API at /api/v2/"
- Visual: Knowledge cards/facts floating
- Purpose: "Persistent project knowledge"

SECTION 2 - CONVENTIONS (memory.yaml):
- Icon: Ruler / standards
- Color: Blue (rules)
- Sub-sections:
  - Naming: "snake_case for Python, kebab-case for K8s"
  - Architecture: "External calls through gateway"
  - Anti-patterns: "Don't use print(), use logger"
- Visual: Pattern templates
- Purpose: "Team standards Claude follows"

SECTION 3 - CONTEXT PRIORITIZATION (context.yaml):
- Icon: Priority indicator / layers
- Color: Orange (importance)
- Levels shown:
  - High priority: README.md, config/*.py, k8s/*.yaml
  - Medium priority: docs/*.md, scripts/*.sh
  - Ignore: *.min.js, coverage/*, dist/*
- Visual: File tree with priority indicators
- Purpose: "Focus Claude on what matters"

FLOW INTO CLAUDE CODE:
- All three sections feed into central Claude Code representation
- "Enhanced Understanding" result
- Better suggestions, follows standards, focuses on right files

SESSION PERSISTENCE:
- Indicator showing memory persists across sessions
- "Remember project context automatically"

YAML SNIPPETS:
- Small code previews of memory.yaml and context.yaml structure

BENEFITS CALLOUT:
- "No need to re-explain project every session"
- "Claude follows team conventions automatically"
- "Relevant files are prioritized"

Style: Knowledge organization diagram, shows configuration files feeding into enhanced Claude Code capability, practical configuration guide.
```

---

### Image 09-05: CI/CD Integration Pipeline

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-09-img-05-flow-cicd-integration.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | After section 9.3 "GitHub Actions Integration" (around line 211-295) |
| **Alt Text** | "CI/CD integration flow: PR Created → Setup Claude → Get Changes → Run Claude Review → Post Comment → Create PR with fixes" |

**Prompt:**
```
A pipeline diagram showing Claude Code integration into CI/CD workflows.

LAYOUT: Horizontal CI/CD pipeline with Claude Code integration points

PIPELINE STAGES:

STAGE 1 - TRIGGER:
- Events: PR created, workflow_dispatch
- Icons: GitHub/GitLab PR icons
- "Pull Request" or "Manual Trigger"

STAGE 2 - SETUP:
- Checkout code (actions/checkout)
- Install Claude Code (npm install)
- Configure API key from secrets
- Visual: Setup icons, key icon

STAGE 3 - ANALYZE:
- Get changed files (git diff)
- Prepare review context
- Visual: Files being gathered

STAGE 4 - CLAUDE CODE REVIEW:
- Icon: Claude Code brain + review
- Color: Anthropic orange (highlight)
- Actions:
  - Security analysis
  - Code quality check
  - Best practices review
  - Test coverage assessment
- Output: review.md generated

STAGE 5 - POST RESULTS:
- Post review as PR comment
- Visual: Comment bubble on PR
- github-script action

STAGE 6 (Optional) - AUTO-FIX:
- Create new branch
- Apply Claude's suggestions
- Create follow-up PR
- Visual: New PR being created

TWO WORKFLOWS SHOWN:

WORKFLOW A - PR REVIEW:
- Automatic on PR creation
- Review and comment
- Human makes decisions

WORKFLOW B - AUTOMATED TASK:
- Manual trigger with task input
- Claude executes task
- Creates PR with changes
- Human reviews result

SECRETS CALLOUT:
- ANTHROPIC_API_KEY from GitHub Secrets
- Secure handling

RETRY LOGIC:
- Rate limiting handling
- Exponential backoff

GITLAB ALTERNATIVE:
- Small note: "Similar pattern for GitLab CI"
- Link to GitLab example

Style: CI/CD pipeline visualization, shows two integration patterns, professional DevOps documentation quality.
```

---

### Image 09-06: Safety and Permissions

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-09-img-06-diagram-safety-permissions.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 9.4 "Safety Guidelines" and "Wildcard Bash Permissions" (around line 352-422) |
| **Alt Text** | "Safety configuration with four areas: Permission Wildcards (allow/deny patterns), Environment Variables (DISABLE_BACKGROUND_TASKS, IS_DEMO), Audit Trail (logging), and Secret Management" |

**Prompt:**
```
A safety and permissions configuration diagram for production Claude Code usage.

LAYOUT: Four safety domains around central Claude Code

DOMAIN 1 - WILDCARD PERMISSIONS:
- Icon: Filter / wildcard pattern
- Color: Blue
- Allow patterns shown:
  - "npm *" - All npm commands
  - "kubectl get *" - Read operations
  - "terraform plan *" - Safe planning
  - "docker build *" - Build operations
- Deny patterns shown:
  - "rm -rf *" - Dangerous delete
  - "* --force" - Force flags blocked
  - "terraform destroy *" - Destructive blocked
  - "kubectl delete *" - Delete blocked
- Visual: Filter allowing/blocking commands

DOMAIN 2 - ENVIRONMENT VARIABLES:
- Icon: Terminal / env vars
- Color: Green
- Key variables:
  - CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1
    - "Use in CI/CD"
    - Prevents auto-backgrounding
  - IS_DEMO=1
    - "Use for presentations"
    - Hides sensitive info
  - FORCE_AUTOUPDATE_PLUGINS=1
    - "Force skill reload"
- Visual: Environment settings panel

DOMAIN 3 - AUDIT TRAIL:
- Icon: Log / history
- Color: Purple
- Practices:
  - "Log all Claude Code sessions"
  - "Track automation changes"
  - "PR review for AI code"
- Visual: Audit log entries
- Hook integration: pre_command logging

DOMAIN 4 - SECRET MANAGEMENT:
- Icon: Lock / key
- Color: Red (security)
- Practices:
  - "Never include secrets in prompts"
  - "Use environment variables"
  - "Exclude .env from context"
  - "Scan for secrets in hooks"
- Visual: Secrets being protected

CENTER - SAFETY PRINCIPLES:
- "Always verify before applying"
- "Test in non-production first"
- "Have rollback plans ready"
- "Separate keys for CI/CD vs interactive"

PRODUCTION BADGE:
- "Production-Ready Safety"
- Checkmark indicators for each domain

Style: Security-focused diagram, shows comprehensive safety setup, suitable for production deployment guidance.
```

---

### Image 09-07: Efficiency and Model Selection

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-09-img-07-compare-model-efficiency.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 or 4:3 |
| **Placement** | After section 9.4 "Efficiency Tips" (around line 424-453) |
| **Alt Text** | "Model selection guide: Haiku for exploration (fast, cheap), Sonnet for implementation (balanced), Opus for architecture decisions (deep reasoning)" |

**Prompt:**
```
A model selection and efficiency guide for optimal Claude Code usage.

THREE COLUMNS - MODEL SELECTION:

COLUMN 1 - HAIKU 4.5:
- Icon: Rabbit / speed
- Color: Green (fast)
- Best for: "Exploration & Quick Searches"
- Tasks:
  - "Where is X implemented?"
  - "Find all files matching..."
  - "Quick code lookups"
  - "Simple questions"
- Speed: Fastest
- Cost: Cheapest
- Depth: Sufficient for search

COLUMN 2 - SONNET 4.5:
- Icon: Balance scale
- Color: Blue (balanced)
- Best for: "Most Coding Tasks"
- Tasks:
  - "Implement this feature"
  - "Refactor this code"
  - "Write tests"
  - "Code review"
- Speed: Fast
- Cost: Balanced
- Depth: Most tasks
- Badge: "Default Recommendation"

COLUMN 3 - OPUS 4.5:
- Icon: Brain / deep thinking
- Color: Purple (depth)
- Best for: "Architecture & Complex Decisions"
- Tasks:
  - "Design system architecture"
  - "Complex debugging"
  - "Security analysis"
  - "Multi-service refactoring"
- Speed: Slower
- Cost: Premium
- Depth: Maximum reasoning
- Note: "Thinking mode enabled by default"

EFFICIENCY TIPS SECTION:

TIP 1 - PARALLEL PROCESSING:
- Visual: Multiple agents working simultaneously
- Example: @parallel { security, performance, tests }
- Benefit: "Break large tasks into parallel sub-tasks"

TIP 2 - CONTEXT MANAGEMENT:
- Visual: Clean context vs cluttered
- Tips:
  - "Start in right directory"
  - "Use context.yaml to prioritize"
  - "Clear between unrelated tasks"

TIP 3 - AUTOMATION BOUNDARIES:
- Visual: Human/AI boundary line
- Automate: "Repetitive, well-defined tasks"
- Human review: "Security-critical changes"
- Human decision: "Architecture choices"

DECISION FLOW:
- Quick question? → Haiku
- Building feature? → Sonnet
- Critical decision? → Opus

Style: Clear model comparison, practical selection guidance, efficiency-focused, suitable for optimizing Claude Code usage.
```

---

## Chapter 10: MCP Fundamentals

### Overview
- **Chapter Focus**: Model Context Protocol introduction, architecture, using MCP servers, DevOps use cases
- **Total Images**: 6
- **Animation Candidates**: 1

---

### Image 10-01: Chapter Header - MCP as Universal Adapter
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-10-img-01-header-mcp-fundamentals.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Claude Code connecting to databases, clouds, and tools through MCP universal adapter" |

**Prompt:** Hero illustration showing MCP as a universal connector hub. Center: Claude Code with MCP ring around it. Radiating connections to: databases (PostgreSQL, Redis), cloud providers (AWS, GCP, Azure), Kubernetes, monitoring (Grafana), CI/CD (GitHub). All connections standardized and uniform. Color: Orange core, blue MCP layer, system-specific colors for externals. Style: Technical connectivity diagram, professional DevOps context.

---

### Image 10-02: Before/After MCP Comparison
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-10-img-02-compare-before-after-mcp.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | Section 10.1 (line ~82-139) |
| **Alt Text** | "Before MCP: chaotic custom integrations. After MCP: clean standardized protocol" |

**Prompt:** Split-screen. LEFT "BEFORE MCP": AI app with tangled spaghetti lines to Git, DB, Slack, AWS, K8s - each connection different. Problems listed: custom-built, duplicated, inconsistent. RED/GRAY tones. RIGHT "WITH MCP": Multiple AI apps connecting to clean MCP LAYER bar, then uniform connections to same systems with "MCP Server" labels. GREEN/BLUE tones. Benefits: standard protocol, build once use everywhere.

---

### Image 10-03: MCP Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-10-img-03-diagram-mcp-architecture.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Section 10.2 (line ~184-225) |
| **Alt Text** | "MCP Client (Claude Code) connecting via JSON-RPC to MCP Servers" |

**Prompt:** Three-layer architecture. TOP: MCP CLIENT box containing Server Manager, Protocol Handler, Capability Cache. MIDDLE: JSON-RPC Protocol layer with bidirectional arrows. BOTTOM: Three MCP Servers - GitHub (clone, commit, create_pr), Kubernetes (get_pods, apply_manifest), PostgreSQL (query, list_tables). Clean technical diagram style.

---

### Image 10-04: Three Primitives (Tools, Resources, Prompts)
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-10-img-04-diagram-three-primitives.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Section 10.2 (line ~227-281) |
| **Alt Text** | "MCP three primitives: Tools, Resources, Prompts" |

**Prompt:** Three-section diagram. TOOLS (Orange): wrench icon, "Functions to execute", examples: create_file(), run_query(). RESOURCES (Blue): database icon, "Data to read", examples: file:///config.yaml, postgres://db/users. PROMPTS (Purple): template icon, "Reusable templates", examples: debug_pod(), analyze_query(). Show how they work together.

🎬 **ANIMATION CANDIDATE**: Show Claude using each primitive in sequence.

---

### Image 10-05: DevOps Use Cases Matrix
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-10-img-05-info-devops-usecases.png` |
| **Type** | Info |
| **Aspect Ratio** | 16:9 |
| **Placement** | Section 10.4 (line ~464) |
| **Alt Text** | "Four MCP use cases: Multi-Cloud, Monitoring, CI/CD, Database" |

**Prompt:** Four quadrants. MULTI-CLOUD (Purple): AWS/GCP/Azure icons, "List instances across clouds". MONITORING (Orange): Prometheus/Grafana, "Query metrics, show alerts". CI/CD (Green): GitHub/ArgoCD, "Show failed runs, trigger builds". DATABASE (Blue): PostgreSQL/Redis, "Compare schemas, slow queries". Center: Claude Code + MCP hub.

---

### Image 10-06: MCP Security Best Practices
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-10-img-06-diagram-mcp-security.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Section 10.5 (line ~660) |
| **Alt Text** | "Four MCP security domains: Authentication, Authorization, Network, Data Protection" |

**Prompt:** Four domains around center. AUTHENTICATION: Use ${ENV_VARS} not hardcoded tokens. AUTHORIZATION: Least privilege, read-only where possible. NETWORK: Local stdio preferred, TLS for HTTP. DATA PROTECTION: Audit logging, data masking. Show good/bad examples for each.

---

## Chapter 11: MCP Server Development

### Overview
- **Chapter Focus**: Building custom MCP servers, TypeScript/Python development, production patterns
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 11-01: Chapter Header - Building Custom Integrations
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-11-img-01-header-mcp-development.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Developer building custom MCP server connecting Claude to internal tools" |

**Prompt:** Developer at workstation building MCP server code. On screen: TypeScript/Python code. From the server: connections radiating to internal company tools (custom deployment system, internal API, proprietary database). Shows transformation from "any tool" to "Claude-accessible". Code editor aesthetic with terminal showing server running. Orange/blue palette.

---

### Image 11-02: Build vs Use Decision Matrix
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-11-img-02-flow-build-vs-use.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Section 11.1 decision matrix |
| **Alt Text** | "Decision flowchart: Build custom MCP server or use existing" |

**Prompt:** Flowchart. START: "Need MCP integration". Decision 1: "Public server exists?" YES→"Use existing" (green). NO→Decision 2: "Internal/proprietary tool?" YES→"Build custom" (orange). Decision 3: "Existing covers 80%?" YES→Use existing. NO→Build custom. Include time estimates: Existing=1 hour setup, Custom=4-8 hours. Show real examples: GitHub→use existing, DeployMaster→build custom.

---

### Image 11-03: MCP Server Structure
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-11-img-03-diagram-server-structure.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | After server code examples |
| **Alt Text** | "MCP server structure: Initialize, Define tools, Handle requests, Return results" |

**Prompt:** Four-stage vertical flow. 1) INITIALIZE: Create server instance, set metadata. 2) DEFINE TOOLS: Register tool schemas with parameters. 3) HANDLE REQUESTS: Request handler receives calls. 4) RETURN RESULTS: Format and return data. Side: show both TypeScript (@modelcontextprotocol/sdk) and Python (mcp package) approaches. Code snippets for each stage.

---

### Image 11-04: Kubernetes MCP Server Example
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-11-img-04-diagram-k8s-mcp-server.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Complete K8s server example section |
| **Alt Text** | "Kubernetes MCP server architecture with tools and cluster connection" |

**Prompt:** Architecture showing K8s MCP Server in center. INPUTS (left): Tool calls from Claude Code (get_pods, get_deployments, apply_manifest, get_logs). CENTER: Server with @kubernetes/client-node. OUTPUT (right): Kubernetes cluster with pods, deployments, services. Show KUBECONFIG authentication flow. Tool descriptions visible for each operation.

---

### Image 11-05: Minimum Viable MCP Server Phases
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-11-img-05-flow-mvp-phases.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | MVP approach section |
| **Alt Text** | "Three phases: Core Operations, Feedback & Expansion, Polish" |

**Prompt:** Timeline/phases diagram. PHASE 1 (Week 1): "Core Operations" - 3-5 tools, 4-6 hours, "Usable not complete". PHASE 2 (Weeks 2-4): "Feedback & Expansion" - Track usage, add requested tools, "Cover 90% use cases". PHASE 3 (Month 2+): "Polish" - Error handling, caching, docs, "Production-ready". Show time investment vs value curve increasing.

---

## Chapter 12: AI for DevOps

### Overview
- **Chapter Focus**: Real-world AI applications in DevOps workflows, practical examples
- **Total Images**: 5
- **Animation Candidates**: 1

---

### Image 12-01: Chapter Header - AI-Powered DevOps
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-12-img-01-header-ai-devops.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "AI assistant integrated into DevOps workflow: code review, deployment, monitoring" |

**Prompt:** Split scene showing DevOps activities enhanced by AI. LEFT: Traditional DevOps (manual reviews, manual deployments). RIGHT: AI-enhanced (automated code review, intelligent deployment decisions, proactive monitoring). Center: AI brain/Claude icon bridging the two. Show: CI/CD pipelines, K8s clusters, monitoring dashboards, all with AI enhancement indicators. Professional DevOps aesthetic.

---

### Image 12-02: DevOps AI Use Cases Wheel
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-12-img-02-diagram-usecase-wheel.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 1:1 or 16:9 |
| **Placement** | Use cases overview section |
| **Alt Text** | "Wheel of DevOps AI use cases: Code Review, IaC Generation, Incident Response, Documentation, Testing, Security" |

**Prompt:** Circular wheel with AI/Claude at center. Six segments: CODE REVIEW (automated PR analysis), IaC GENERATION (Terraform/K8s from requirements), INCIDENT RESPONSE (log analysis, RCA), DOCUMENTATION (auto-generate docs), TESTING (test generation, coverage), SECURITY (vulnerability scanning, compliance). Each segment with icon and example prompt.

🎬 **ANIMATION CANDIDATE**: Wheel spinning to highlight each use case with example.

---

### Image 12-03: Incident Response Flow
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-12-img-03-flow-incident-response.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Incident response section |
| **Alt Text** | "AI-assisted incident response: Alert→Gather→Analyze→Diagnose→Mitigate→Document" |

**Prompt:** Horizontal flow. 1) ALERT: PagerDuty notification. 2) GATHER: AI collects logs, metrics, recent changes. 3) ANALYZE: Pattern recognition, anomaly detection. 4) DIAGNOSE: Root cause identification. 5) MITIGATE: Suggested fixes, runbook steps. 6) DOCUMENT: Auto-generate post-mortem. Show time savings at each step. Human checkpoints for critical decisions.

---

### Image 12-04: IaC Generation Workflow
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-12-img-04-flow-iac-generation.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Infrastructure as Code section |
| **Alt Text** | "Natural language to Terraform/Kubernetes: Requirement→Generate→Review→Apply" |

**Prompt:** Flow showing transformation. INPUT: Natural language "I need an S3 bucket with encryption and lifecycle rules". PROCESS: Claude Code analyzing requirements. OUTPUT: Terraform code + K8s manifests. VALIDATION: Security scan, best practice check. APPLY: terraform plan/apply with human approval. Show generated code snippets.

---

### Image 12-05: Code Review Automation
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-12-img-05-flow-code-review.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Automated code review section |
| **Alt Text** | "Automated PR review pipeline: PR Created→AI Analysis→Report→Human Decision" |

**Prompt:** CI/CD pipeline style. TRIGGER: PR created on GitHub. ANALYSIS: Claude Code checks security, quality, patterns, tests. REPORT: Structured findings posted as PR comment. Categories: Critical (red), Warning (yellow), Info (blue). HUMAN: Developer reviews AI suggestions, makes decision. Show example review comment format.

---

## Chapter 13: n8n Fundamentals

### Overview
- **Chapter Focus**: n8n workflow automation basics, AI integration fundamentals
- **Total Images**: 5
- **Animation Candidates**: 1

---

### Image 13-01: Chapter Header - Visual Workflow Automation
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-13-img-01-header-n8n-fundamentals.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "n8n visual workflow editor with connected nodes forming automation pipeline" |

**Prompt:** n8n-style interface showing visual workflow. Nodes connected: Webhook trigger → Process data → AI node (Claude) → Multiple outputs (Slack, Database, Email). Show the visual programming paradigm - no code, drag-and-drop nodes, connection lines. n8n orange/coral brand color. Modern workflow automation aesthetic.

---

### Image 13-02: n8n Architecture Overview
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-13-img-02-diagram-n8n-architecture.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Architecture section |
| **Alt Text** | "n8n architecture: Triggers, Nodes, Connections, Executions" |

**Prompt:** Layered architecture. TOP: TRIGGERS (Webhook, Schedule, App events). MIDDLE: n8n Engine processing workflows. NODES: 400+ integrations shown as icons (Slack, GitHub, AWS, databases). BOTTOM: Outputs and actions. Show workflow execution flow with data transformation between nodes.

---

### Image 13-03: Node Types Comparison
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-13-img-03-compare-node-types.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | Node types section |
| **Alt Text** | "Four node types: Trigger, Regular, AI, Function" |

**Prompt:** Four columns. TRIGGER NODES: Webhook, Schedule, App triggers - "Start workflows". REGULAR NODES: HTTP, Database, Apps - "Move and transform data". AI NODES: Claude, OpenAI, LangChain - "Intelligent processing". FUNCTION NODES: Code, IF, Switch - "Logic and control". Each with examples and when to use.

🎬 **ANIMATION CANDIDATE**: Show data flowing through different node types.

---

### Image 13-04: First Workflow Tutorial
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-13-img-04-flow-first-workflow.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Tutorial section |
| **Alt Text** | "Step-by-step first workflow: Trigger→Process→AI→Output" |

**Prompt:** Numbered tutorial steps. 1) Add Webhook trigger node. 2) Connect HTTP Request node. 3) Add Claude AI node for processing. 4) Connect Slack node for output. Show n8n editor interface at each step. Highlight connection points. Include sample data flowing through.

---

### Image 13-05: AI Node Configuration
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-13-img-05-diagram-ai-node-config.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | AI integration section |
| **Alt Text** | "Claude AI node configuration: API key, model, prompt, parameters" |

**Prompt:** n8n node configuration panel mockup. Show Claude AI node with: API Key field (from credentials), Model selector (Sonnet/Opus/Haiku), Prompt template area with {{variables}}, Temperature/tokens settings. Side: show input data mapping and output handling. Best practices callouts.

---

## Chapter 14: n8n Advanced

### Overview
- **Chapter Focus**: Advanced n8n patterns, production deployment, complex AI workflows
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 14-01: Chapter Header - Production Workflows
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-14-img-01-header-n8n-advanced.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Complex n8n workflow with error handling, sub-workflows, and monitoring" |

**Prompt:** Sophisticated n8n workflow showing: multiple branches, error handling nodes, sub-workflow calls, retry logic, monitoring hooks. Production-ready aesthetic with status indicators, logging nodes. Show complexity while maintaining clarity. Include queue processing, rate limiting nodes.

---

### Image 14-02: Error Handling Patterns
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-14-img-02-diagram-error-handling.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Error handling section |
| **Alt Text** | "Three error handling patterns: Retry, Fallback, Alert" |

**Prompt:** Three workflow patterns. RETRY: Node fails → Wait → Retry (exponential backoff). FALLBACK: Primary fails → Switch to backup method. ALERT: Error captured → Format → Send to PagerDuty/Slack. Show error output nodes, continue on fail settings. Best practices for each pattern.

---

### Image 14-03: Sub-Workflow Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-14-img-03-diagram-subworkflows.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Sub-workflows section |
| **Alt Text** | "Main workflow calling reusable sub-workflows" |

**Prompt:** Hierarchical diagram. MAIN WORKFLOW at top calling three SUB-WORKFLOWS: "Process Order", "Notify Customer", "Update Inventory". Each sub-workflow shown as collapsed module. Show parameter passing in, results returning out. Benefits: reusability, maintainability, testing.

---

### Image 14-04: Production Deployment Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-14-img-04-diagram-production-deploy.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Production deployment section |
| **Alt Text** | "n8n production setup: Load balancer, workers, queue, database" |

**Prompt:** Infrastructure diagram. Load balancer → Multiple n8n workers. Shared components: Redis queue, PostgreSQL database, S3 for files. Monitoring: Prometheus metrics, Grafana dashboard. Show scaling indicators, health checks. Docker/Kubernetes deployment context.

---

### Image 14-05: AI Agent Workflow Pattern
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-14-img-05-flow-ai-agent-pattern.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | AI agents section |
| **Alt Text** | "AI agent loop: Plan→Execute→Evaluate→Iterate" |

**Prompt:** Circular flow showing AI agent pattern in n8n. Claude AI node for PLANNING → Tool execution nodes (HTTP, DB, etc.) for EXECUTE → Claude AI for EVALUATE results → Decision: Done? YES→Output, NO→Loop back to Plan. Show memory/context persistence. Max iterations safeguard.

---

## Chapter 15: Multi-Agent Fundamentals

### Overview
- **Chapter Focus**: Multi-agent systems concepts, coordination patterns, agent teams
- **Total Images**: 6
- **Animation Candidates**: 1

---

### Image 15-01: Chapter Header - Agent Teams
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-15-img-01-header-multiagent-fundamentals.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Team of specialized AI agents collaborating on complex task" |

**Prompt:** Multiple AI agents represented as specialized team members working together. COORDINATOR agent in center directing. Surrounding: RESEARCHER agent (magnifying glass), CODER agent (brackets), REVIEWER agent (checklist), DEPLOYER agent (rocket). Communication lines between them. Collaborative team aesthetic. Show task being broken down and distributed.

---

### Image 15-02: Single vs Multi-Agent Comparison
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-15-img-02-compare-single-vs-multi.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | Concepts section |
| **Alt Text** | "Single agent handling everything vs specialized multi-agent team" |

**Prompt:** Split comparison. LEFT "SINGLE AGENT": One AI trying to do everything - overloaded, context limits, jack of all trades. RIGHT "MULTI-AGENT": Specialized agents - Researcher, Planner, Coder, Tester each focused. Show same complex task being handled. Benefits: specialization, parallelism, better results.

🎬 **ANIMATION CANDIDATE**: Complex task flowing through multi-agent system.

---

### Image 15-03: Agent Coordination Patterns
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-15-img-03-diagram-coordination-patterns.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Coordination section |
| **Alt Text** | "Four patterns: Hierarchical, Peer-to-Peer, Broadcast, Pipeline" |

**Prompt:** Four coordination patterns. HIERARCHICAL: Manager agent directing worker agents. PEER-TO-PEER: Agents communicating directly, no central control. BROADCAST: One agent sending to all others. PIPELINE: Sequential handoff A→B→C→D. Show when to use each, pros/cons. DevOps context for examples.

---

### Image 15-04: Agent Specializations
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-15-img-04-info-agent-specializations.png` |
| **Type** | Info |
| **Aspect Ratio** | 16:9 |
| **Placement** | Specialist agents section |
| **Alt Text** | "Six specialist agent types with capabilities" |

**Prompt:** Six agent cards. RESEARCHER: Find information, explore codebases. PLANNER: Break down tasks, create roadmaps. CODER: Write and modify code. REVIEWER: Security, quality, best practices. TESTER: Generate and run tests. DEPLOYER: Infrastructure, CI/CD, releases. Each card with icon, capabilities list, example prompts.

---

### Image 15-05: Agent Communication Flow
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-15-img-05-flow-agent-communication.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Communication section |
| **Alt Text** | "Agent communication: Message passing, shared context, result aggregation" |

**Prompt:** Communication flow diagram. MESSAGE PASSING: Agent A sends task to Agent B. SHARED CONTEXT: Multiple agents reading/writing shared memory. RESULT AGGREGATION: Multiple agent outputs combined by coordinator. Show message formats, context structures. Error handling for failed agents.

---

### Image 15-06: Agent Pool Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-15-img-06-diagram-agent-pool.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Agent pools section |
| **Alt Text** | "Agent pool with task queue, worker agents, result collection" |

**Prompt:** Pool architecture. TASK QUEUE: Incoming tasks waiting. AGENT POOL: Multiple available agents (some busy, some idle). DISPATCHER: Assigns tasks to available agents. RESULTS: Collected and aggregated. Show scaling (more agents for more tasks), load balancing, fault tolerance (replace failed agent).

---

## Chapter 16: Multi-Agent Advanced

### Overview
- **Chapter Focus**: Production incident response swarms, code review teams, monitoring agents
- **Total Images**: 5
- **Animation Candidates**: 1

---

### Image 16-01: Chapter Header - Incident Response Swarm
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-16-img-01-header-multiagent-advanced.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Swarm of agents responding to production incident" |

**Prompt:** Dynamic incident response scene. Alert triggering swarm deployment. Multiple agents converging: LOG ANALYZER examining logs, METRICS AGENT checking dashboards, CODE REVIEWER looking at recent commits, REMEDIATION AGENT preparing fixes. War room aesthetic with urgency. Coordinated response visualization.

---

### Image 16-02: Incident Swarm Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-16-img-02-diagram-incident-swarm.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Incident response section |
| **Alt Text** | "Incident swarm: Coordinator spawning specialist agents in parallel" |

**Prompt:** Swarm architecture. TRIGGER: PagerDuty alert. COORDINATOR: Spawns specialist agents. PARALLEL AGENTS: Log Analyzer, Metrics Checker, Change Detector, Impact Assessor, Remediation Planner. AGGREGATION: Findings combined. OUTPUT: RCA report, suggested fixes, auto-remediation options. Timeline showing parallel execution.

🎬 **ANIMATION CANDIDATE**: Incident triggering swarm response with parallel investigation.

---

### Image 16-03: Code Review Team Structure
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-16-img-03-diagram-review-team.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Code review section |
| **Alt Text** | "Multi-agent code review team with specialized reviewers" |

**Prompt:** Review team structure. PR TRIGGER → REVIEW COORDINATOR. Coordinator dispatches to: SECURITY REVIEWER (vulnerabilities, auth), PERFORMANCE REVIEWER (efficiency, queries), STYLE REVIEWER (patterns, conventions), TEST REVIEWER (coverage, quality). Each produces findings. AGGREGATOR combines into single PR review. Show finding severity levels.

---

### Image 16-04: Monitoring Agent Network
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-16-img-04-diagram-monitoring-network.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Monitoring agents section |
| **Alt Text** | "Network of monitoring agents watching different system aspects" |

**Prompt:** Distributed monitoring network. Infrastructure showing: API servers, databases, queues, caches. MONITORING AGENTS positioned throughout: API Agent (latency, errors), DB Agent (queries, connections), Queue Agent (depth, processing), Cache Agent (hit rate). Central CORRELATION AGENT finding patterns across data. Alert escalation flow.

---

### Image 16-05: Swarm Scaling Patterns
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-16-img-05-diagram-swarm-scaling.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Scaling section |
| **Alt Text** | "Swarm scaling: More agents for bigger incidents" |

**Prompt:** Scaling visualization. Three scenarios: SMALL INCIDENT (Sev3): 2-3 agents, quick resolution. MEDIUM INCIDENT (Sev2): 5-7 agents, deeper analysis. MAJOR INCIDENT (Sev1): 10+ agents, full swarm, war room mode. Show resource allocation, agent specialization at each level. Cost/benefit indicators.

---

## Chapter 17: AIOps Fundamentals

### Overview
- **Chapter Focus**: AI-powered observability, anomaly detection, predictive alerting basics
- **Total Images**: 5
- **Animation Candidates**: 1

---

### Image 17-01: Chapter Header - AI-Powered Observability
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-17-img-01-header-aiops-fundamentals.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "AI analyzing metrics, logs, and traces to detect anomalies" |

**Prompt:** Modern observability dashboard enhanced by AI. THREE PILLARS visible: Metrics (graphs), Logs (text streams), Traces (distributed paths). AI brain/neural network overlay analyzing all three. Anomalies being highlighted automatically. Predictive alerts showing future issues. Clean, professional monitoring aesthetic.

---

### Image 17-02: Traditional vs AIOps Monitoring
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-17-img-02-compare-traditional-vs-aiops.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | AIOps concepts section |
| **Alt Text** | "Traditional monitoring (static thresholds) vs AIOps (intelligent detection)" |

**Prompt:** Split comparison. LEFT "TRADITIONAL": Static threshold alerts (CPU > 80%), many false positives, alert fatigue, reactive only. RIGHT "AIOPS": Dynamic baselines, anomaly detection, noise reduction, predictive alerts. Show same metrics data handled differently. AIOps catching subtle issues traditional misses.

---

### Image 17-03: Anomaly Detection Types
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-17-img-03-diagram-anomaly-types.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Anomaly detection section |
| **Alt Text** | "Three anomaly types: Point, Contextual, Collective" |

**Prompt:** Three anomaly visualizations. POINT ANOMALY: Single outlier spike on time series. CONTEXTUAL ANOMALY: Value normal overall but wrong for time (high traffic at 3am). COLLECTIVE ANOMALY: Pattern of points that together indicate issue. Each with metric graph example, detection approach, real-world scenario.

🎬 **ANIMATION CANDIDATE**: Anomaly detection in action on streaming metrics.

---

### Image 17-04: Predictive Alerting Flow
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-17-img-04-flow-predictive-alerting.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Predictive alerting section |
| **Alt Text** | "Predictive alert flow: Collect→Learn→Predict→Alert before failure" |

**Prompt:** Flow diagram. COLLECT: Historical metrics, patterns. LEARN: ML model training on normal behavior. PREDICT: Forecast future values, detect trending toward threshold. ALERT: Proactive notification before actual failure. Show timeline: Traditional alert at failure time, Predictive alert hours earlier. Lead time benefit highlighted.

---

### Image 17-05: AIOps Implementation Stack
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-17-img-05-diagram-aiops-stack.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Implementation section |
| **Alt Text** | "AIOps stack: Data layer, ML layer, Action layer" |

**Prompt:** Three-layer stack. DATA LAYER: Prometheus, Loki, Jaeger collecting metrics/logs/traces. ML LAYER: Anomaly detection models, forecasting, correlation. ACTION LAYER: Intelligent alerts, auto-remediation, runbook triggers. Show data flowing up through layers, actions flowing down. Integration points with existing tools.

---

## Chapter 18: AIOps Advanced

### Overview
- **Chapter Focus**: Alert correlation, noise reduction, automated remediation, production patterns
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 18-01: Chapter Header - Intelligent Alert Management
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-18-img-01-header-aiops-advanced.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "AI correlating multiple alerts into single incident with auto-remediation" |

**Prompt:** Alert storm (many alerts) being processed by AI correlation engine. Multiple related alerts combining into single meaningful incident. Auto-remediation robot/arm taking corrective action. Before: chaos of alerts. After: organized, actionable, automated. Show noise reduction metrics (100 alerts → 3 incidents).

---

### Image 18-02: Alert Correlation Engine
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-18-img-02-diagram-correlation-engine.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Alert correlation section |
| **Alt Text** | "Correlation engine: Multiple alerts → Pattern matching → Single incident" |

**Prompt:** Correlation architecture. INPUT: Stream of alerts from different sources (Prometheus, CloudWatch, app logs). CORRELATION ENGINE: Time-based grouping, topology-aware correlation, ML pattern matching. OUTPUT: Grouped incidents with root cause indication. Show example: DB slow + API errors + queue backup = "Database performance degradation" single incident.

---

### Image 18-03: Noise Reduction Techniques
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-18-img-03-diagram-noise-reduction.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Noise reduction section |
| **Alt Text** | "Four noise reduction techniques: Deduplication, Suppression, Aggregation, Smart routing" |

**Prompt:** Four technique boxes. DEDUPLICATION: Same alert × 50 → 1 alert. SUPPRESSION: Maintenance window → alerts muted. AGGREGATION: Similar alerts grouped by service/type. SMART ROUTING: Alert → right team based on content. Show before/after alert counts. Metrics: 95% noise reduction possible.

---

### Image 18-04: Auto-Remediation Decision Tree
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-18-img-04-flow-auto-remediation.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Auto-remediation section |
| **Alt Text** | "Decision tree: When to auto-remediate vs human escalation" |

**Prompt:** Decision flowchart. ALERT RECEIVED → Is known issue? YES→Runbook exists? YES→Safe to auto-remediate? YES→EXECUTE AUTO-REMEDIATION. NO paths → ESCALATE TO HUMAN. Show safety gates: impact assessment, blast radius check, rollback capability. Examples: restart pod (auto), scale down production (human).

---

### Image 18-05: AIOps Maturity Model
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-18-img-05-diagram-maturity-model.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Maturity section |
| **Alt Text** | "AIOps maturity: Reactive → Proactive → Predictive → Autonomous" |

**Prompt:** Four-stage maturity ladder. LEVEL 1 REACTIVE: Static thresholds, manual response. LEVEL 2 PROACTIVE: Dynamic baselines, anomaly detection. LEVEL 3 PREDICTIVE: Forecasting, early warning. LEVEL 4 AUTONOMOUS: Self-healing, auto-scaling, minimal human intervention. Show capabilities and tools at each level. Assessment questions for each stage.

---

## Chapter 19: Team Transformation

### Overview
- **Chapter Focus**: Organizational change management, AI adoption strategies, cultural transformation
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 19-01: Chapter Header - AI Team Transformation
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-19-img-01-header-team-transformation.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Team evolving from traditional workflows to AI-augmented collaboration" |

**Prompt:** Transformation journey visualization. LEFT: Traditional team (manual processes, siloed). CENTER: Transformation arrow with AI integration symbol. RIGHT: AI-augmented team (humans + AI collaboration, automated workflows). Show cultural shift: skepticism → experimentation → adoption → advocacy. Team members at various stages.

---

### Image 19-02: AI Adoption Curve
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-19-img-02-diagram-adoption-curve.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Adoption section |
| **Alt Text** | "Technology adoption curve: Innovators → Early Adopters → Majority → Laggards" |

**Prompt:** Classic adoption curve with AI context. Curve showing: INNOVATORS (2.5%) - AI enthusiasts experimenting. EARLY ADOPTERS (13.5%) - Champions driving adoption. EARLY MAJORITY (34%) - Practical users seeing value. LATE MAJORITY (34%) - Following proven success. LAGGARDS (16%) - Reluctant adopters. Strategies for each group.

---

### Image 19-03: Change Management Framework
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-19-img-03-flow-change-management.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Change management section |
| **Alt Text** | "ADKAR change model: Awareness → Desire → Knowledge → Ability → Reinforcement" |

**Prompt:** ADKAR framework applied to AI adoption. AWARENESS: Why AI matters for DevOps. DESIRE: Personal benefits, career growth. KNOWLEDGE: Training, documentation, examples. ABILITY: Practice, support, tools access. REINFORCEMENT: Recognition, metrics, continuous improvement. Activities for each stage.

---

### Image 19-04: Resistance and Solutions
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-19-img-04-compare-resistance-solutions.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | Resistance section |
| **Alt Text** | "Common resistance concerns and solutions" |

**Prompt:** Two-column format. CONCERNS (left): Job security fears, Quality doubts, Learning curve, Loss of control. SOLUTIONS (right): AI as augmentation not replacement, Quality metrics showing improvement, Gradual rollout with training, Human-in-the-loop design. Empathetic tone, practical responses.

---

### Image 19-05: Success Metrics Dashboard
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-19-img-05-diagram-success-metrics.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Metrics section |
| **Alt Text** | "AI adoption metrics: Productivity, Quality, Satisfaction, Adoption rate" |

**Prompt:** Dashboard-style layout. Four metric categories: PRODUCTIVITY (time saved, tasks automated), QUALITY (error reduction, code quality), SATISFACTION (team sentiment, confidence), ADOPTION (active users, feature usage). Each with example KPIs, targets, measurement methods. Show improvement trends.

---

## Chapter 20: Agent Loop Detection

### Overview
- **Chapter Focus**: Detecting and preventing infinite loops in AI agents
- **Total Images**: 4
- **Animation Candidates**: 1

---

### Image 20-01: Chapter Header - Preventing Infinite Loops
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-20-img-01-header-loop-detection.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "AI agent caught in loop being detected and stopped" |

**Prompt:** Visual of agent stuck in circular pattern (loop visualization). Detection system recognizing pattern. STOP mechanism engaging. Before: Agent spinning endlessly consuming resources. After: Loop detected, agent redirected or stopped safely. Warning indicators, resource meters showing consumption.

---

### Image 20-02: Loop Pattern Types
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-20-img-02-diagram-loop-types.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Loop patterns section |
| **Alt Text** | "Three loop types: Action loops, Thought loops, Tool loops" |

**Prompt:** Three loop visualizations. ACTION LOOP: Agent repeatedly taking same action (edit file → check → edit same file). THOUGHT LOOP: Agent reasoning in circles without progress. TOOL LOOP: Agent calling same tool repeatedly with same parameters. Detection signals for each: repetition count, similarity score, progress metric.

🎬 **ANIMATION CANDIDATE**: Agent entering loop, detection triggering, intervention.

---

### Image 20-03: Detection Mechanisms
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-20-img-03-diagram-detection-mechanisms.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Detection section |
| **Alt Text** | "Loop detection: Iteration counting, State comparison, Progress tracking" |

**Prompt:** Three detection methods. ITERATION COUNTING: Max iterations limit with counter. STATE COMPARISON: Hash/fingerprint of agent state, detect repeated states. PROGRESS TRACKING: Measure goal distance, detect no progress. Implementation code snippets for each. Thresholds and tuning guidance.

---

### Image 20-04: Recovery Strategies
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-20-img-04-flow-recovery-strategies.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Recovery section |
| **Alt Text** | "Loop recovery: Detect → Intervene → Recover or Escalate" |

**Prompt:** Recovery flow. DETECT: Loop identified. INTERVENTION OPTIONS: Inject new context, Change approach, Reduce scope, Pause and prompt user. RECOVERY: Agent continues with new strategy. ESCALATION: If recovery fails → Human intervention. Show decision points, timeout handling, state preservation for debugging.

---

## Chapter 21: Resilience Patterns

### Overview
- **Chapter Focus**: Building resilient AI agent systems, fault tolerance, graceful degradation
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 21-01: Chapter Header - Resilient Agent Systems
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-21-img-01-header-resilience-patterns.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Resilient AI system weathering failures and continuing to operate" |

**Prompt:** System reliability visualization. AI agent system facing various failures (network issues, API errors, rate limits) but continuing to operate. Redundancy shown (multiple paths). Graceful degradation (reduced but functional). Circuit breakers preventing cascade. Robust, stable aesthetic despite challenges.

---

### Image 21-02: Circuit Breaker Pattern
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-21-img-02-diagram-circuit-breaker.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Circuit breaker section |
| **Alt Text** | "Circuit breaker states: Closed, Open, Half-Open" |

**Prompt:** Three-state diagram. CLOSED: Normal operation, requests flow through. OPEN: Failures exceeded threshold, requests blocked immediately. HALF-OPEN: Testing recovery, limited requests allowed. Show state transitions, failure counters, timeout configuration. API call context for AI agents.

---

### Image 21-03: Retry Strategies
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-21-img-03-diagram-retry-strategies.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Retry section |
| **Alt Text** | "Retry patterns: Immediate, Fixed delay, Exponential backoff, Jitter" |

**Prompt:** Four retry patterns visualized on timeline. IMMEDIATE: Rapid retries (risky). FIXED DELAY: Equal spacing (simple). EXPONENTIAL BACKOFF: Increasing delays (recommended). WITH JITTER: Randomized to prevent thundering herd. Show wait times, success scenarios, max retry limits.

---

### Image 21-04: Fallback Hierarchy
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-21-img-04-flow-fallback-hierarchy.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Fallback section |
| **Alt Text** | "Fallback chain: Primary → Secondary → Cache → Default" |

**Prompt:** Fallback cascade. PRIMARY: Claude Opus (best quality). FALLBACK 1: Claude Sonnet (still good). FALLBACK 2: Claude Haiku (fast, cheaper). FALLBACK 3: Cached response (if available). FALLBACK 4: Default/safe response. Show decision at each level, graceful degradation of capability.

---

### Image 21-05: Bulkhead Pattern
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-21-img-05-diagram-bulkhead.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Isolation section |
| **Alt Text** | "Bulkhead pattern: Isolated pools preventing cascade failures" |

**Prompt:** Ship bulkhead metaphor. Multiple isolated compartments (resource pools). One compartment flooding (service failure) doesn't sink ship (system). Apply to agents: separate pools for different tasks, rate limit per pool, failure contained. Show isolation benefit when one pool fails.

---

## Chapter 22: Production Deployment

### Overview
- **Chapter Focus**: Deploying AI agents to production, scaling, monitoring, operations
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 22-01: Chapter Header - Production AI Systems
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-22-img-01-header-production-deployment.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "AI agent system deployed in production with scaling and monitoring" |

**Prompt:** Production infrastructure view. AI agent cluster running in Kubernetes. Load balancers distributing traffic. Monitoring dashboards showing health. Auto-scaling indicators. Multiple availability zones. Production-grade aesthetic: robust, monitored, scalable.

---

### Image 22-02: Deployment Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-22-img-02-diagram-deployment-architecture.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Architecture section |
| **Alt Text** | "Production architecture: API Gateway, Agent Workers, Queue, Storage" |

**Prompt:** Layered architecture. INGRESS: API Gateway, rate limiting, auth. ORCHESTRATION: Agent coordinator, task queue (Redis/SQS). WORKERS: Scalable agent pods. EXTERNAL: LLM APIs (Claude), tools (MCP servers). STORAGE: State store, conversation history. OBSERVABILITY: Metrics, logs, traces. Show connections and data flow.

---

### Image 22-03: Scaling Strategies
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-22-img-03-diagram-scaling-strategies.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Scaling section |
| **Alt Text** | "Scaling: Horizontal (more agents), Vertical (bigger agents), Queue-based" |

**Prompt:** Three scaling approaches. HORIZONTAL: Add more agent instances based on queue depth. VERTICAL: Use more powerful models for complex tasks. QUEUE-BASED: Buffer requests, process at sustainable rate. Show auto-scaling triggers, metrics (queue depth, latency, CPU). Cost implications of each.

---

### Image 22-04: Production Monitoring Dashboard
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-22-img-04-diagram-monitoring-dashboard.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Monitoring section |
| **Alt Text** | "Agent monitoring: Success rate, Latency, Token usage, Errors" |

**Prompt:** Dashboard mockup for AI agent monitoring. KEY METRICS: Success rate (%), Average latency (s), Token usage (cost), Error rate, Queue depth. GRAPHS: Request volume over time, Latency percentiles, Error breakdown by type. ALERTS: SLO violations highlighted. Agent-specific metrics: loop detection rate, fallback usage.

---

### Image 22-05: Deployment Pipeline
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-22-img-05-flow-deployment-pipeline.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | CI/CD section |
| **Alt Text** | "Agent deployment pipeline: Test → Stage → Canary → Production" |

**Prompt:** Progressive deployment flow. BUILD: Code + prompt testing. STAGE: Deploy to staging, integration tests. CANARY: Deploy to small % of production traffic. MONITOR: Watch metrics, compare to baseline. PROMOTE: Gradual rollout to full production. ROLLBACK: Automatic on metric degradation. Show gates between stages.

---

## Chapter 23: RAG Fundamentals

### Overview
- **Chapter Focus**: Retrieval-Augmented Generation basics, vector databases, embedding fundamentals
- **Total Images**: 5
- **Animation Candidates**: 1

---

### Image 23-01: Chapter Header - Knowledge-Enhanced AI
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-23-img-01-header-rag-fundamentals.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "AI retrieving relevant documents to enhance response generation" |

**Prompt:** RAG concept visualization. User question entering system. RETRIEVAL: Searching through document collection, relevant chunks highlighted. AUGMENTATION: Retrieved content combined with question. GENERATION: Claude producing informed response. Knowledge base (documents, code, docs) visible. Show enhancement over base LLM.

---

### Image 23-02: RAG vs Fine-tuning Comparison
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-23-img-02-compare-rag-vs-finetuning.png` |
| **Type** | Compare |
| **Aspect Ratio** | 16:9 |
| **Placement** | Concepts section |
| **Alt Text** | "RAG (external knowledge) vs Fine-tuning (baked-in knowledge)" |

**Prompt:** Split comparison. LEFT "FINE-TUNING": Training data baked into model, expensive to update, good for style/behavior. RIGHT "RAG": External knowledge retrieved at runtime, easy to update, good for facts/docs. Compare: update frequency, cost, freshness, use cases. When to use each.

---

### Image 23-03: RAG Pipeline Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-23-img-03-flow-rag-pipeline.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Architecture section |
| **Alt Text** | "RAG pipeline: Ingest → Embed → Store → Retrieve → Generate" |

**Prompt:** End-to-end RAG flow. INGESTION: Documents chunked and processed. EMBEDDING: Text → vectors via embedding model. STORAGE: Vectors stored in vector database (Pinecone, Weaviate). RETRIEVAL: Query embedded, similar vectors found. GENERATION: Retrieved context + query → LLM → response. Show each stage with data transformation.

🎬 **ANIMATION CANDIDATE**: Query flowing through RAG pipeline with retrieval and generation.

---

### Image 23-04: Vector Embeddings Explained
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-23-img-04-concept-embeddings.png` |
| **Type** | Concept |
| **Aspect Ratio** | 16:9 |
| **Placement** | Embeddings section |
| **Alt Text** | "Text to vectors: Similar concepts cluster together in vector space" |

**Prompt:** Embedding visualization. Text examples: "Kubernetes deployment", "K8s pod", "Docker container", "Python function". Show conversion to vectors (arrays of numbers). 2D/3D projection of vector space showing similar concepts clustered together. K8s concepts cluster, code concepts cluster. Similarity = proximity.

---

### Image 23-05: Chunking Strategies
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-23-img-05-diagram-chunking.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Chunking section |
| **Alt Text** | "Chunking strategies: Fixed size, Semantic, Document structure" |

**Prompt:** Three chunking approaches. FIXED SIZE: Document split every N tokens, simple but may break context. SEMANTIC: Split at natural boundaries (paragraphs, sections), preserves meaning. DOCUMENT STRUCTURE: Respect headings, code blocks, lists. Show same document chunked three ways. Trade-offs: retrieval precision vs context preservation.

---

## Chapter 24: RAG Search Optimization

### Overview
- **Chapter Focus**: Improving RAG retrieval quality, hybrid search, reranking
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 24-01: Chapter Header - Precision Retrieval
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-24-img-01-header-rag-optimization.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Optimized retrieval finding exact relevant documents from large corpus" |

**Prompt:** Precision search visualization. Large document corpus. Query entering system. Multiple retrieval techniques working: vector search, keyword search, hybrid combination. Reranking stage sorting results. Top results highly relevant (green), less relevant filtered (gray). Accuracy metrics displayed.

---

### Image 24-02: Hybrid Search Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-24-img-02-diagram-hybrid-search.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Hybrid search section |
| **Alt Text** | "Hybrid search: Vector + Keyword combined for better results" |

**Prompt:** Parallel search paths. QUERY branches to: VECTOR SEARCH (semantic similarity) and KEYWORD SEARCH (BM25/exact match). Results merged with fusion algorithm (RRF or weighted). Show scenarios: "K8s deploy errors" - vector finds semantic matches, keyword finds exact terms. Combined results better than either alone.

---

### Image 24-03: Reranking Pipeline
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-24-img-03-flow-reranking.png` |
| **Type** | Flow |
| **Aspect Ratio** | 16:9 |
| **Placement** | Reranking section |
| **Alt Text** | "Reranking: Initial retrieval → Cross-encoder scoring → Final ranking" |

**Prompt:** Two-stage retrieval. STAGE 1: Fast retrieval gets top-100 candidates (bi-encoder). STAGE 2: Reranker scores each candidate against query (cross-encoder). Results reordered by relevance score. Show quality improvement: initial ranking vs final ranking. Speed/quality trade-off explained.

---

### Image 24-04: Query Transformation
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-24-img-04-diagram-query-transform.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Query optimization section |
| **Alt Text** | "Query transformations: Expansion, Decomposition, HyDE" |

**Prompt:** Three query techniques. EXPANSION: "deploy error" → "deploy error failure deployment issue K8s". DECOMPOSITION: Complex query → multiple sub-queries. HYDE (Hypothetical Document): Generate hypothetical answer, use it for retrieval. Show original query, transformation, improved results.

---

### Image 24-05: Evaluation Metrics
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-24-img-05-diagram-evaluation.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Evaluation section |
| **Alt Text** | "RAG metrics: Precision, Recall, MRR, NDCG" |

**Prompt:** Metrics dashboard. PRECISION@K: Relevant docs in top K / K. RECALL@K: Relevant docs found / total relevant. MRR: Mean reciprocal rank (position of first relevant). NDCG: Normalized discounted cumulative gain. Visual examples of each metric calculation. Benchmark targets for production systems.

---

## Chapter 25: Production RAG Systems

### Overview
- **Chapter Focus**: Building production-ready RAG systems, scaling, operations
- **Total Images**: 5
- **Animation Candidates**: 0

---

### Image 25-01: Chapter Header - Enterprise RAG
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-25-img-01-header-production-rag.png` |
| **Type** | Header |
| **Aspect Ratio** | 16:9 |
| **Placement** | After chapter title |
| **Alt Text** | "Enterprise RAG system with multiple data sources, caching, and monitoring" |

**Prompt:** Production RAG infrastructure. Multiple data sources: documentation, code repos, wikis, tickets. Ingestion pipeline processing all. Vector database cluster. Query serving layer with caching. Monitoring and observability. Multi-tenant support indicators. Enterprise-grade, scalable, monitored.

---

### Image 25-02: Production Architecture
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-25-img-02-diagram-prod-architecture.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Architecture section |
| **Alt Text** | "Production RAG: Ingestion pipeline, Vector store cluster, Query service" |

**Prompt:** Three main components. INGESTION PIPELINE: Document processors, embedding service, batch/streaming modes. VECTOR STORE: Clustered database (Pinecone/Weaviate/Qdrant), replication, sharding. QUERY SERVICE: Load balanced, cached, rate limited. MONITORING: Retrieval quality metrics, latency, cost. Show scaling points.

---

### Image 25-03: Data Freshness Strategies
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-25-img-03-diagram-data-freshness.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Data management section |
| **Alt Text** | "Freshness strategies: Batch, Incremental, Real-time" |

**Prompt:** Three update strategies. BATCH: Full re-index on schedule (nightly), simple but stale. INCREMENTAL: Process changes only, webhook triggers. REAL-TIME: Stream processing, instant updates. Compare: freshness, complexity, cost. Choose based on data change rate and freshness requirements.

---

### Image 25-04: Multi-tenant RAG
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-25-img-04-diagram-multi-tenant.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Multi-tenancy section |
| **Alt Text** | "Multi-tenant RAG: Tenant isolation, Access control, Resource limits" |

**Prompt:** Multi-tenant architecture. Multiple tenants (companies/teams) sharing infrastructure. ISOLATION: Separate namespaces, filtered queries. ACCESS CONTROL: User → permissions → visible documents. RESOURCE LIMITS: Per-tenant quotas, fair scheduling. Show query path with tenant context applied.

---

### Image 25-05: RAG Observability Dashboard
| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-25-img-05-diagram-observability.png` |
| **Type** | Diagram |
| **Aspect Ratio** | 16:9 |
| **Placement** | Observability section |
| **Alt Text** | "RAG monitoring: Retrieval quality, Latency, User feedback" |

**Prompt:** Comprehensive dashboard. RETRIEVAL METRICS: Hit rate, empty results %, diversity score. LATENCY: Embedding time, search time, generation time. COST: Token usage, API costs, storage costs. USER FEEDBACK: Thumbs up/down, citations clicked. ALERTS: Quality degradation, latency spikes. Track improvements over time.

---

## Summary Statistics

| Chapter | Images | Animation Candidates |
|---------|--------|---------------------|
| 01 - Introduction to AI | 8 | 2 |
| 02 - Understanding LLMs and Tokens | 10 | 3 |
| 03 - The Art of Prompting | 8 | 1 |
| 04 - AI Models Landscape | 8 | 1 |
| 05 - Introduction to Claude | 7 | 1 |
| 06 - Claude Code Fundamentals | 10 | 2 |
| 07 - Claude Code Intermediate | 9 | 1 |
| 08 - Skills and Subagents | 8 | 2 |
| 09 - Hooks and Advanced Features | 7 | 1 |
| 10 - MCP Fundamentals | 6 | 1 |
| 11 - MCP Server Development | 5 | 0 |
| 12 - AI for DevOps | 5 | 1 |
| 13 - n8n Fundamentals | 5 | 1 |
| 14 - n8n Advanced | 5 | 0 |
| 15 - Multi-Agent Fundamentals | 6 | 1 |
| 16 - Multi-Agent Advanced | 5 | 1 |
| 17 - AIOps Fundamentals | 5 | 1 |
| 18 - AIOps Advanced | 5 | 0 |
| 19 - Team Transformation | 5 | 0 |
| 20 - Agent Loop Detection | 4 | 1 |
| 21 - Resilience Patterns | 5 | 0 |
| 22 - Production Deployment | 5 | 0 |
| 23 - RAG Fundamentals | 5 | 1 |
| 24 - RAG Search Optimization | 5 | 0 |
| 25 - Production RAG Systems | 5 | 0 |

**Total Images**: 151
**Total Animation Candidates**: 22
**Image Types Breakdown**:
- Header images: 25
- Diagrams: ~60
- Flow charts: ~35
- Comparisons: ~20
- Infographics: ~11

---

## Appendix: Prompt Template

Use this template for consistency:

```markdown
### Image XX-YY: [Title]

| Attribute | Value |
|-----------|-------|
| **Filename** | `chapter-XX-img-YY-[type]-[description].png` |
| **Type** | [Header/Concept/Diagram/Flow/Compare/Info/Icon/Screen] |
| **Aspect Ratio** | [16:9 / 4:3 / 1:1 / 21:9 / 3:4] |
| **Placement** | [Specific location in chapter with line reference] |
| **Alt Text** | "[Accessibility description]" |

**Prompt:**
```
[Detailed prompt here]
```

[Optional: 🎬 ANIMATION CANDIDATE note]
[Optional: 📐 RECOMMEND: Use diagramming tool note]
```

---

**Document Version**: 1.0
**Created by**: Claude (AI Assistant)
**For**: Michel Abboud - AI and Claude Code Guide
