# Chapter Visuals Guide

**Purpose**: This document contains detailed AI image generation prompts for all chapter visuals in "AI and Claude Code: A Comprehensive Guide for DevOps Engineers".

**Author**: Michel Abboud
**Created**: January 2026
**Last Updated**: January 2026

---

## Table of Contents

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

*[To be populated after reading chapter]*

---

## Chapter 05: Introduction to Claude

*[To be populated after reading chapter]*

---

## Chapter 06: Claude Code Fundamentals

*[To be populated after reading chapter]*

---

## Chapter 07: Claude Code Intermediate

*[To be populated after reading chapter]*

---

## Chapter 08: Skills and Subagents

*[To be populated after reading chapter]*

---

## Chapter 09: Hooks and Advanced Features

*[To be populated after reading chapter]*

---

## Chapter 10: MCP Fundamentals

*[To be populated after reading chapter]*

---

## Chapter 11: MCP Server Development

*[To be populated after reading chapter]*

---

## Chapter 12: AI for DevOps

*[To be populated after reading chapter]*

---

## Chapter 13: n8n Fundamentals

*[To be populated after reading chapter]*

---

## Chapter 14: n8n Advanced

*[To be populated after reading chapter]*

---

## Chapter 15: Multi-Agent Fundamentals

*[To be populated after reading chapter]*

---

## Chapter 16: Multi-Agent Advanced

*[To be populated after reading chapter]*

---

## Chapter 17: AIOps Fundamentals

*[To be populated after reading chapter]*

---

## Chapter 18: AIOps Advanced

*[To be populated after reading chapter]*

---

## Chapter 19: Team Transformation

*[To be populated after reading chapter]*

---

## Chapter 20: Agent Loop Detection

*[To be populated after reading chapter]*

---

## Chapter 21: Resilience Patterns

*[To be populated after reading chapter]*

---

## Chapter 22: Production Deployment

*[To be populated after reading chapter]*

---

## Chapter 23: RAG Fundamentals

*[To be populated after reading chapter]*

---

## Chapter 24: RAG Search Optimization

*[To be populated after reading chapter]*

---

## Chapter 25: Production RAG Systems

*[To be populated after reading chapter]*

---

## Summary Statistics

| Chapter | Images | Diagrams (Tool) | Animations |
|---------|--------|-----------------|------------|
| 01 | 8 | 0 | 2 |
| 02 | TBD | TBD | TBD |
| ... | ... | ... | ... |

**Total Images**: TBD
**Total Animations**: TBD
**Tool-based Diagrams**: TBD

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
