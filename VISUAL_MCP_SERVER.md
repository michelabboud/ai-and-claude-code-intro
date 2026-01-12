# Project Bootstrap: Visual Forge MCP

## Project Overview

Create an MCP (Model Context Protocol) server called **Visual Forge MCP** (`visual-forge-mcp`) that automates AI image generation for technical documentation. The server reads a structured markdown file containing image prompts and generates images using various AI providers (DALL-E 3, Stability AI, Replicate/Flux, Leonardo.ai).

### Primary Use Case

This MCP server was designed to generate 151 images for an educational guide called "AI and Claude Code: A Comprehensive Guide for DevOps Engineers". However, it should be generic enough to work with any similarly structured visual guide markdown file.

### Key Capabilities

1. **Parse Visual Guides**: Extract image specifications from structured markdown files
2. **Multi-Provider Support**: Connect to multiple AI image generation APIs
3. **Flexible Workflows**: Support interactive (one-by-one with approval), batch, and bulk generation modes
4. **Version Control**: Generate multiple variants of each image for comparison
5. **Cost Tracking**: Monitor and limit spending across providers
6. **State Persistence**: Resume interrupted sessions, track approvals/rejections
7. **Smart Output**: Save images with consistent naming conventions and metadata
8. **Universal IDE Support**: Works with any MCP-compatible client or IDE

---

## Supported Clients & IDEs

Visual Forge MCP is built on the Model Context Protocol (MCP), making it compatible with any MCP-enabled client. **One server, all platforms.**

### Verified Compatible Clients (18 Platforms)

| Client | Type | Developer | Notes |
|--------|------|-----------|-------|
| **Amp** | IDE | Sourcegraph | AI-native code editor |
| **Claude Code** | CLI | Anthropic | Primary development target |
| **Claude Desktop** | Desktop App | Anthropic | Full GUI experience |
| **Cline** | VS Code Extension | Cline | Autonomous coding agent |
| **Codex** | CLI | OpenAI | OpenAI's coding assistant |
| **Copilot** | IDE Extension | GitHub/Microsoft | GitHub Copilot with MCP |
| **Cursor** | IDE | Cursor | AI-first code editor |
| **Factory** | Platform | Factory | AI software development platform |
| **Gemini CLI** | CLI | Google | Google's AI CLI tool |
| **Goose** | CLI | Block | Open-source AI agent |
| **Kiro** | IDE | Amazon | AWS AI-powered IDE |
| **LM Studio** | Desktop App | LM Studio | Local LLM runner with MCP |
| **opencode** | CLI | Open Source | Terminal-based AI coding |
| **OpenHands** | Agent Platform | All Hands AI | Open-source AI software agent (64k+ stars) |
| **Qodo Gen** | IDE Extension | Qodo | AI code generation |
| **VS Code** | IDE | Microsoft | Via MCP extensions |
| **Warp** | Terminal | Warp | AI-native terminal |
| **Windsurf** | IDE | Codeium | Codeium's AI IDE |

### Configuration by Client

**Claude Code / Claude Desktop** (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "visual-forge": {
      "command": "npx",
      "args": ["visual-forge-mcp"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  }
}
```

**Cursor** (Settings → MCP Servers):
```json
{
  "visual-forge": {
    "command": "npx",
    "args": ["visual-forge-mcp"]
  }
}
```

**VS Code + Continue** (`~/.continue/config.json`):
```json
{
  "experimental": {
    "mcpServers": {
      "visual-forge": {
        "command": "npx",
        "args": ["visual-forge-mcp"]
      }
    }
  }
}
```

**Windsurf** (`~/.windsurf/settings.json`):
```json
{
  "mcpServers": {
    "visual-forge": {
      "command": "npx",
      "args": ["visual-forge-mcp"]
    }
  }
}
```

### Standalone CLI Mode

For clients without MCP support, Visual Forge MCP can run as a standalone CLI:

```bash
# Install globally
npm install -g visual-forge-mcp

# Run commands directly
visual-forge parse ./CHAPTER-VISUALS-GUIDE.md
visual-forge generate --chapter 1 --provider dalle
visual-forge status
visual-forge generate-all --batch-size 10
```

### Future: REST API Mode

Planned feature for universal integration:
```bash
# Start as HTTP server
visual-forge serve --port 3000

# Any client can call
curl http://localhost:3000/api/generate -d '{"imageId": "chapter-01-img-01"}'
```

---

## Technical Stack

- **Runtime**: Node.js 18+ with TypeScript
- **MCP SDK**: @modelcontextprotocol/sdk
- **HTTP Client**: axios or node-fetch for API calls
- **File System**: Node.js fs/promises for file operations
- **State**: JSON file-based persistence (no database required)
- **Image Processing**: sharp (optional, for resizing/format conversion)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            MCP Clients (18 Platforms)                                │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │
│  │  Amp  │ │Claude │ │Cursor │ │ Cline │ │ Codex │ │Copilot│ │Factory│ │Gemini │   │
│  │       │ │ Code  │ │       │ │       │ │       │ │       │ │       │ │  CLI  │   │
│  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘   │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │
│  │ Goose │ │ Kiro  │ │  LM   │ │ open  │ │ Open  │ │ Qodo  │ │  VS   │ │ Warp  │   │
│  │       │ │       │ │Studio │ │ code  │ │ Hands │ │  Gen  │ │ Code  │ │       │   │
│  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘   │
│                                                              ┌───────┐             │
│                                                              │ Wind  │             │
│                                                              │ surf  │             │
│                                                              └───────┘             │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                            MCP Protocol (stdio/SSE)
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                              Visual Forge MCP                                   │
│                                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐     │
│  │   Parser         │  │  Workflow        │  │  Provider Adapters       │     │
│  │   Module         │  │  Engine          │  │  ┌────────────────────┐  │     │
│  │                  │  │                  │  │  │ DALL-E 3           │  │     │
│  │ - Extract        │  │ - One-by-one     │  │  │ Stability AI       │  │     │
│  │   prompts        │  │ - Batch N        │  │  │ Replicate/Flux     │  │     │
│  │ - Metadata       │  │ - Batch all      │  │  │ Leonardo.ai        │  │     │
│  │ - Context        │  │ - Versions       │  │  └────────────────────┘  │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────┘     │
│                                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐     │
│  │   State          │  │   Output         │  │   Cost Tracker           │     │
│  │   Manager        │  │   Handler        │  │                          │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────┘     │
└───────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
                          ┌───────────────────────┐
                          │    Output Directory   │
                          │    /images/           │
                          │    chapter-01/        │
                          │    chapter-02/        │
                          │    ...                │
                          └───────────────────────┘
```

---

## MCP Tools to Implement

### Parsing Tools

| Tool | Parameters | Returns | Description |
|------|------------|---------|-------------|
| `parse_visual_guide` | `path: string` | `ImageSpec[]` | Parse markdown file, return all image specifications |
| `get_chapters` | `path?: string` | `ChapterSummary[]` | List all chapters with image counts |
| `get_chapter_images` | `chapter: number` | `ImageSpec[]` | Get all image specs for a specific chapter |
| `get_image_spec` | `imageId: string` | `ImageSpec` | Get details for a single image by ID |
| `search_images` | `query: string, type?: string` | `ImageSpec[]` | Search images by description or type |

### Generation Tools

| Tool | Parameters | Returns | Description |
|------|------------|---------|-------------|
| `generate_image` | `imageId: string, provider?: string, versions?: number` | `GenerationJob` | Generate a single image |
| `generate_batch` | `imageIds: string[], provider?: string` | `GenerationJob[]` | Generate multiple specific images |
| `generate_chapter` | `chapter: number, provider?: string` | `GenerationJob[]` | Generate all images for a chapter |
| `generate_range` | `startChapter: number, endChapter: number` | `GenerationJob[]` | Generate images for chapter range |
| `generate_all` | `provider?: string, costLimit?: number` | `GenerationJob[]` | Generate all remaining images |
| `regenerate` | `imageId: string, feedback?: string` | `GenerationJob` | Regenerate with optional feedback |

### Workflow Control Tools

| Tool | Parameters | Returns | Description |
|------|------------|---------|-------------|
| `configure_workflow` | `config: WorkflowConfig` | `WorkflowConfig` | Set workflow mode and parameters |
| `get_workflow_config` | none | `WorkflowConfig` | Get current workflow configuration |
| `approve_image` | `imageId: string, versionIndex?: number` | `ApprovalResult` | Approve generated image |
| `reject_image` | `imageId: string, feedback: string` | `RejectionResult` | Reject with feedback for regeneration |
| `pause_generation` | none | `QueueStatus` | Pause current generation queue |
| `resume_generation` | none | `QueueStatus` | Resume paused generation |
| `cancel_generation` | `jobId?: string` | `CancellationResult` | Cancel specific job or all pending |

### Status Tools

| Tool | Parameters | Returns | Description |
|------|------------|---------|-------------|
| `get_generation_status` | `jobId?: string` | `GenerationStatus` | Check progress of generation jobs |
| `get_queue_status` | none | `QueueStatus` | Get generation queue status |
| `list_generated` | `chapter?: number, status?: string` | `GeneratedImage[]` | List generated images with filters |
| `list_pending` | none | `ImageSpec[]` | List images not yet generated |
| `get_cost_summary` | none | `CostSummary` | Get spending totals by provider |
| `get_cost_estimate` | `scope: string, provider?: string` | `CostEstimate` | Estimate cost for planned generation |

### Provider Tools

| Tool | Parameters | Returns | Description |
|------|------------|---------|-------------|
| `list_providers` | none | `ProviderInfo[]` | List available providers and status |
| `test_provider` | `provider: string` | `ProviderTestResult` | Test provider connectivity |
| `set_default_provider` | `provider: string` | `ProviderInfo` | Set default provider for generation |

---

## MCP Resources to Implement

| Resource | URI Pattern | Description |
|----------|-------------|-------------|
| Visual Guide | `visuals://guide` | Full parsed visual guide as JSON |
| Chapter List | `visuals://chapters` | List of chapters with summaries |
| Chapter Images | `visuals://chapter/{num}` | Images for specific chapter |
| Generation Queue | `visuals://queue` | Current generation queue |
| Generated Images | `visuals://generated` | All generated images metadata |
| Pending Images | `visuals://pending` | Images not yet generated |
| Cost Summary | `visuals://costs` | Running cost totals |
| Workflow Config | `visuals://config` | Current workflow configuration |

---

## Core Data Structures (TypeScript Interfaces)

```typescript
// Image specification parsed from markdown
interface ImageSpec {
  id: string;                      // "chapter-01-img-01"
  chapter: number;                 // 1
  imageNumber: number;             // 1
  type: ImageType;                 // "header" | "diagram" | "flow" | "compare" | "info" | "concept" | "screen"
  filename: string;                // "chapter-01-img-01-header-ai-landscape.png"
  prompt: string;                  // Full generation prompt text
  contextPreamble: string;         // Global context block to prepend
  placement: string;               // "After introduction paragraph"
  altText: string;                 // Accessibility text
  aspectRatio: AspectRatio;        // "16:9" | "4:3" | "1:1" | "21:9" | "3:4"
  resolution: Resolution;          // { width: 1920, height: 1080 }
  isAnimationCandidate: boolean;   // Has 🎬 marker
  animationNotes?: string;         // Animation suggestions if applicable
  styleModifiers?: string[];       // Additional style keywords
}

type ImageType = "header" | "diagram" | "flow" | "compare" | "info" | "concept" | "screen";
type AspectRatio = "16:9" | "4:3" | "1:1" | "21:9" | "3:4" | "2:3";

interface Resolution {
  width: number;
  height: number;
}

// Generation job tracking
interface GenerationJob {
  id: string;                      // UUID
  imageSpec: ImageSpec;
  provider: Provider;
  versions: number;                // How many variants requested
  status: JobStatus;
  results: GeneratedImage[];       // Generated variants
  cost: number;                    // Actual cost incurred
  error?: string;                  // Error message if failed
  startedAt: Date;
  completedAt?: Date;
  feedback?: string;               // User feedback if rejected
  retryCount: number;
}

type JobStatus = "queued" | "generating" | "completed" | "review" | "approved" | "rejected" | "failed";
type Provider = "dalle" | "stability" | "replicate" | "leonardo";

// Generated image result
interface GeneratedImage {
  id: string;                      // UUID
  jobId: string;                   // Parent job ID
  imageSpecId: string;             // Original spec ID
  versionIndex: number;            // 0, 1, 2... for variants
  provider: Provider;
  filePath: string;                // Local file path
  url?: string;                    // Remote URL (temporary)
  metadata: ImageMetadata;
  generatedAt: Date;
  approved: boolean;
  selected: boolean;               // Selected as final version
}

interface ImageMetadata {
  width: number;
  height: number;
  format: string;                  // "png" | "jpg" | "webp"
  fileSize: number;                // bytes
  prompt: string;                  // Actual prompt sent
  provider: Provider;
  model: string;                   // e.g., "dall-e-3", "sdxl-1.0"
  seed?: number;                   // If available
  revisedPrompt?: string;          // DALL-E's revised prompt
}

// Workflow configuration
interface WorkflowConfig {
  mode: WorkflowMode;
  batchSize: number;               // For batch mode (default: 10)
  versionsPerImage: number;        // Variants to generate (1-4)
  defaultProvider: Provider;
  autoApprove: boolean;            // Skip approval step
  outputDirectory: string;         // Where to save images
  organizeByChapter: boolean;      // Create chapter subdirectories
  includeAnimations: boolean;      // Process animation candidates
  costLimit?: number;              // Stop if exceeded
  concurrency: number;             // Parallel generation limit
  retryOnFailure: boolean;
  maxRetries: number;
}

type WorkflowMode = "interactive" | "batch" | "bulk";

// Provider configuration
interface ProviderConfig {
  apiKey: string;
  enabled: boolean;
  model?: string;
  quality?: string;
  style?: string;
  rateLimit: number;               // Requests per minute
  costPerImage: number;            // Estimated cost
  supportedAspectRatios: AspectRatio[];
  maxResolution: Resolution;
}

// Cost tracking
interface CostSummary {
  total: number;
  byProvider: Record<Provider, number>;
  byChapter: Record<number, number>;
  imageCount: number;
  averagePerImage: number;
  estimatedRemaining: number;
}

interface CostEstimate {
  scope: string;
  imageCount: number;
  estimatedCost: { min: number; max: number };
  byProvider: Record<Provider, { count: number; cost: number }>;
  warnings?: string[];
}

// Queue management
interface QueueStatus {
  isPaused: boolean;
  totalJobs: number;
  pending: number;
  inProgress: number;
  completed: number;
  failed: number;
  currentJob?: GenerationJob;
  estimatedTimeRemaining?: number; // seconds
}

// Chapter summary
interface ChapterSummary {
  number: number;
  title: string;
  totalImages: number;
  generated: number;
  approved: number;
  pending: number;
  animationCandidates: number;
  imageTypes: Record<ImageType, number>;
}
```

---

## Project File Structure

```
image-generator-mcp/
├── package.json
├── tsconfig.json
├── README.md
├── LICENSE                        # MIT
├── .env.example
├── .gitignore
│
├── src/
│   ├── index.ts                   # MCP server entry point
│   │
│   ├── parser/
│   │   ├── index.ts               # Parser module exports
│   │   ├── markdown-parser.ts     # Parse visual guide markdown
│   │   ├── prompt-extractor.ts    # Extract individual prompts
│   │   ├── metadata-parser.ts     # Extract placement, alt text, etc.
│   │   └── context-parser.ts      # Extract global context preamble
│   │
│   ├── providers/
│   │   ├── index.ts               # Provider exports and factory
│   │   ├── base-provider.ts       # Abstract provider interface
│   │   ├── dalle-provider.ts      # OpenAI DALL-E 3 implementation
│   │   ├── stability-provider.ts  # Stability AI implementation
│   │   ├── replicate-provider.ts  # Replicate (Flux, SD) implementation
│   │   └── leonardo-provider.ts   # Leonardo.ai implementation
│   │
│   ├── workflow/
│   │   ├── index.ts               # Workflow exports
│   │   ├── workflow-engine.ts     # Main orchestration logic
│   │   ├── interactive-mode.ts    # One-by-one with approval
│   │   ├── batch-mode.ts          # Batch processing
│   │   └── bulk-mode.ts           # Fire and forget
│   │
│   ├── state/
│   │   ├── index.ts               # State exports
│   │   ├── state-manager.ts       # Track progress, approvals
│   │   ├── queue-manager.ts       # Generation queue FIFO
│   │   └── persistence.ts         # JSON file save/load
│   │
│   ├── output/
│   │   ├── index.ts               # Output exports
│   │   ├── file-handler.ts        # Save images to disk
│   │   ├── naming.ts              # Enforce naming convention
│   │   └── manifest.ts            # Track what's generated
│   │
│   ├── cost/
│   │   ├── index.ts               # Cost exports
│   │   ├── cost-tracker.ts        # Track spending
│   │   └── estimator.ts           # Estimate future costs
│   │
│   ├── tools/
│   │   ├── index.ts               # Register all tools
│   │   ├── parse-tools.ts         # Parsing-related MCP tools
│   │   ├── generate-tools.ts      # Generation MCP tools
│   │   ├── workflow-tools.ts      # Workflow control tools
│   │   ├── status-tools.ts        # Status/progress tools
│   │   └── provider-tools.ts      # Provider management tools
│   │
│   ├── resources/
│   │   ├── index.ts               # Register all resources
│   │   └── resource-handlers.ts   # Resource URI handlers
│   │
│   ├── utils/
│   │   ├── logger.ts              # Logging utility
│   │   ├── rate-limiter.ts        # API rate limiting
│   │   └── retry.ts               # Retry with backoff
│   │
│   └── types/
│       └── index.ts               # All TypeScript interfaces
│
├── config/
│   └── default.json               # Default configuration
│
├── test/
│   ├── parser.test.ts
│   ├── providers.test.ts
│   ├── workflow.test.ts
│   └── fixtures/
│       └── sample-visual-guide.md # Test fixture
│
└── data/                          # Runtime data (gitignored)
    ├── state.json
    ├── queue.json
    ├── costs.json
    └── generated/
        └── *.json
```

---

## Provider Implementation Details

### DALL-E 3 (OpenAI)

```typescript
// Endpoint: https://api.openai.com/v1/images/generations
// Auth: Bearer token
// Models: dall-e-3
// Quality: "standard" | "hd"
// Sizes: 1024x1024, 1024x1792, 1792x1024
// Cost: $0.04 (standard), $0.08 (hd) per image
// Rate limit: 5 images/minute (tier dependent)

interface DalleRequest {
  model: "dall-e-3";
  prompt: string;
  n: 1;                            // DALL-E 3 only supports 1
  size: "1024x1024" | "1024x1792" | "1792x1024";
  quality: "standard" | "hd";
  style?: "vivid" | "natural";
  response_format: "url" | "b64_json";
}
```

### Stability AI

```typescript
// Endpoint: https://api.stability.ai/v1/generation/{engine}/text-to-image
// Auth: Bearer token
// Engines: stable-diffusion-xl-1024-v1-0, stable-diffusion-v1-6
// Cost: ~$0.02-0.06 per image (credit based)

interface StabilityRequest {
  text_prompts: Array<{ text: string; weight: number }>;
  cfg_scale: number;               // 0-35, default 7
  height: number;
  width: number;
  samples: number;                 // 1-10
  steps: number;                   // 10-50
  style_preset?: string;           // "enhance", "anime", "photographic", etc.
}
```

### Replicate (Flux)

```typescript
// Endpoint: https://api.replicate.com/v1/predictions
// Auth: Bearer token
// Model: black-forest-labs/flux-schnell (fast) or flux-dev (quality)
// Cost: ~$0.003 per image (schnell), ~$0.03 (dev)

interface ReplicateRequest {
  version: string;                 // Model version hash
  input: {
    prompt: string;
    aspect_ratio?: string;
    num_outputs?: number;
    output_format?: "webp" | "png" | "jpg";
    output_quality?: number;
  };
}
```

### Leonardo.ai

```typescript
// Endpoint: https://cloud.leonardo.ai/api/rest/v1/generations
// Auth: Bearer token
// Models: Various Leonardo models
// Cost: Credit-based, ~$0.01-0.04 per image

interface LeonardoRequest {
  prompt: string;
  modelId: string;
  width: number;
  height: number;
  num_images: number;
  guidance_scale?: number;
  promptMagic?: boolean;
}
```

---

## Workflow Mode Details

### Interactive Mode
```
1. User requests generation
2. Server generates ONE image
3. Returns image for review (as base64 or file path)
4. Waits for approve_image or reject_image call
5. If approved: saves final, moves to next
6. If rejected: regenerates with feedback incorporated
7. Repeat until all images complete
```

### Batch Mode
```
1. User configures batch size (e.g., 10)
2. Server generates batch in parallel (respecting rate limits)
3. Returns all images for review
4. User approves/rejects each
5. Regenerates rejected ones
6. Once batch approved, moves to next batch
```

### Bulk Mode
```
1. User requests bulk generation (chapter/range/all)
2. Server queues all images
3. Processes queue with concurrency limit
4. Auto-saves all results
5. Reports completion summary
6. User can review/regenerate specific failures
```

---

## Configuration File Format

```json
{
  "visualGuidePath": "./CHAPTER-VISUALS-GUIDE.md",
  "outputDirectory": "./generated-images",
  "stateDirectory": "~/.image-generator-mcp",

  "providers": {
    "dalle": {
      "enabled": true,
      "apiKey": "${OPENAI_API_KEY}",
      "model": "dall-e-3",
      "quality": "hd",
      "style": "natural",
      "rateLimit": 5,
      "costPerImage": 0.08
    },
    "stability": {
      "enabled": true,
      "apiKey": "${STABILITY_API_KEY}",
      "engine": "stable-diffusion-xl-1024-v1-0",
      "rateLimit": 10,
      "costPerImage": 0.04
    },
    "replicate": {
      "enabled": true,
      "apiKey": "${REPLICATE_API_TOKEN}",
      "model": "black-forest-labs/flux-schnell",
      "rateLimit": 20,
      "costPerImage": 0.003
    },
    "leonardo": {
      "enabled": false,
      "apiKey": "${LEONARDO_API_KEY}",
      "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
      "rateLimit": 10,
      "costPerImage": 0.02
    }
  },

  "workflow": {
    "defaultMode": "interactive",
    "defaultProvider": "dalle",
    "batchSize": 10,
    "versionsPerImage": 1,
    "autoApprove": false,
    "concurrency": 3,
    "retryOnFailure": true,
    "maxRetries": 2,
    "organizeByChapter": true
  },

  "output": {
    "format": "png",
    "quality": 95,
    "createManifest": true,
    "includeMetadata": true
  }
}
```

---

## Expected Visual Guide Markdown Format

The parser should handle markdown structured like this:

```markdown
# Chapter Visuals Guide

## Global Context Preamble (Copy-Paste This First)

### Context Block for AI Image Generators

\`\`\`
CONTEXT FOR ALL IMAGES:
[Global context that applies to all images...]
\`\`\`

---

## Chapter 01: Chapter Title

### Image 1: Image Title

**Filename**: `chapter-01-img-01-type-description.png`
**Type**: header | diagram | flow | compare | info | concept | screen
**Aspect Ratio**: 16:9
**Placement**: After the introduction paragraph

**Prompt**:
\`\`\`
[Detailed generation prompt...]
\`\`\`

**Alt Text**: Descriptive text for accessibility

🎬 **ANIMATION CANDIDATE**: [Notes about potential animation]

---

### Image 2: Next Image Title
[...]
```

---

## Implementation Priorities

### Phase 1: MVP (Core Functionality)
1. Project setup (package.json, tsconfig, MCP boilerplate)
2. Markdown parser for visual guide format
3. Single provider implementation (DALL-E 3)
4. Basic `generate_image` tool
5. File output with naming convention
6. Simple state tracking

### Phase 2: Workflow Engine
1. Interactive mode with approval flow
2. Batch mode implementation
3. Queue management
4. State persistence (resume sessions)
5. Cost tracking basics

### Phase 3: Multi-Provider
1. Add Stability AI provider
2. Add Replicate/Flux provider
3. Provider selection logic
4. Fallback on failures
5. Rate limiting per provider

### Phase 4: Polish
1. All MCP resources
2. Cost estimation
3. Progress reporting
4. Error handling improvements
5. Comprehensive logging
6. Documentation

---

## Environment Variables

```bash
# Required (at least one provider)
OPENAI_API_KEY=sk-...
STABILITY_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...
LEONARDO_API_KEY=...

# Optional
IMAGE_GEN_OUTPUT_DIR=./generated-images
IMAGE_GEN_STATE_DIR=~/.image-generator-mcp
IMAGE_GEN_LOG_LEVEL=info
```

---

## Example Usage Scenarios

### Scenario 1: Parse and explore
```
User: "What images are in the visual guide?"
Claude: [calls parse_visual_guide]
→ "Found 151 images across 25 chapters. 22 are animation candidates."

User: "Show me chapter 6 images"
Claude: [calls get_chapter_images(6)]
→ Lists 10 images with IDs, types, descriptions
```

### Scenario 2: Interactive generation
```
User: "Generate chapter 1 images, I want to approve each one"
Claude: [calls configure_workflow({mode: "interactive"})]
Claude: [calls generate_image("chapter-01-img-01")]
→ "Generated image preview: [shows/describes image]"

User: "The neural network looks good, approve it"
Claude: [calls approve_image("chapter-01-img-01")]
→ "Approved and saved. Generating next image..."
```

### Scenario 3: Batch with versions
```
User: "Generate 3 versions of each header image so I can pick the best"
Claude: [calls search_images({type: "header"})]
Claude: [calls configure_workflow({versionsPerImage: 3, mode: "batch"})]
Claude: [calls generate_batch(headerImageIds)]
→ "Generated 75 images (25 headers × 3 versions). Ready for review."
```

### Scenario 4: Cost-conscious bulk
```
User: "How much would it cost to generate everything?"
Claude: [calls get_cost_estimate({scope: "all"})]
→ "Estimated $12-15 with DALL-E, $5-6 with Flux"

User: "Use Flux for diagrams, DALL-E for headers, max $20"
Claude: [calls generate_all({costLimit: 20, providerMapping: {...}})]
```

---

## Testing Strategy

1. **Unit Tests**: Parser, naming conventions, cost calculations
2. **Integration Tests**: Provider API calls (with mocks)
3. **E2E Tests**: Full workflow with test visual guide
4. **Fixtures**: Sample visual guide markdown for testing

---

## Success Criteria

1. Can parse any visual guide following the expected format
2. Successfully generates images with at least 2 providers
3. Interactive mode works with approval/rejection flow
4. Batch mode processes multiple images efficiently
5. State persists across sessions (can resume)
6. Cost tracking is accurate
7. Output follows naming conventions
8. Handles API errors gracefully with retries

---

## Notes for Implementation

1. **Start simple**: Get DALL-E working end-to-end before adding providers
2. **Parser flexibility**: The markdown format may vary; make parser resilient
3. **Rate limiting**: Essential for not getting banned; implement early
4. **Cost awareness**: Log costs prominently; users need visibility
5. **State recovery**: Sessions will be interrupted; robust persistence matters
6. **Error messages**: Make them actionable; include what to do next

---

## References

- MCP SDK: https://github.com/modelcontextprotocol/typescript-sdk
- OpenAI Images API: https://platform.openai.com/docs/api-reference/images
- Stability AI API: https://platform.stability.ai/docs/api-reference
- Replicate API: https://replicate.com/docs/reference/http
- Leonardo API: https://docs.leonardo.ai/reference

---

## Source Visual Guide

The original visual guide this MCP server was designed to process is located at:
- Repository: `ai-and-claude-code-intro`
- File: `CHAPTER-VISUALS-GUIDE.md`
- Contains: 151 image prompts across 25 chapters, 22 animation candidates

---

Begin by creating the project structure and implementing Phase 1 (MVP with DALL-E support).
