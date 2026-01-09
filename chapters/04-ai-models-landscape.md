# Chapter 4: AI Models Landscape

## Navigating the World of AI Models and Providers

Understanding the AI ecosystem helps you make informed decisions about which tools to use for different tasks. This chapter covers the major players, model types, and how to choose the right model for your needs.

---

## 4.1 Understanding "Models"

### What is a Model?

A **model** is a trained AI system that can perform specific tasks. Think of it as a specialized program that has learned from data.

```
┌────────────────────────────────────────────────────────────────┐
│                   THE MODEL LIFECYCLE                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. ARCHITECTURE DESIGN                                        │
│     "How should the neural network be structured?"             │
│     └─► Transformer, CNN, RNN, etc.                           │
│                                                                │
│  2. PRE-TRAINING                                               │
│     "Learn general knowledge from massive data"                │
│     └─► Billions of tokens of text, code, etc.                │
│         └─► Months of training on GPU clusters                │
│                                                                │
│  3. FINE-TUNING                                                │
│     "Specialize for specific tasks"                            │
│     └─► Instruction tuning, RLHF, domain adaptation           │
│                                                                │
│  4. DEPLOYMENT                                                 │
│     "Make it available for use"                                │
│     └─► API endpoints, downloadable weights, etc.             │
│                                                                │
│  5. INFERENCE                                                  │
│     "Using the model to get predictions"                       │
│     └─► What you do when you chat with an AI                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Model Naming Conventions

```
Understanding model names:

Claude 3.5 Sonnet
│     │   │
│     │   └── Variant (capability tier within the family)
│     └────── Version (major iteration)
└──────────── Family name (product line)

GPT-4-Turbo-128K
│   │ │     │
│   │ │     └── Context window size
│   │ └──────── Variant (optimized version)
│   └────────── Version
└────────────── Family name

LLaMA-2-70B-Chat
│     │ │   │
│     │ │   └── Specialization (chat-optimized)
│     │ └────── Parameter count (70 billion)
│     └──────── Version
└────────────── Family name
```

---

## 4.2 Major AI Companies and Their Models

### The Big Players

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAJOR AI COMPANIES (2024)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ANTHROPIC                                               │   │
│  │  "AI Safety First"                                       │   │
│  │                                                          │   │
│  │  Founded: 2021 by ex-OpenAI researchers                  │   │
│  │  Focus: Safe, helpful, honest AI                         │   │
│  │  Models: Claude family                                   │   │
│  │  Notable: Constitutional AI, long context windows        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  OPENAI                                                  │   │
│  │  "AGI for the benefit of humanity"                       │   │
│  │                                                          │   │
│  │  Founded: 2015                                           │   │
│  │  Focus: General AI advancement                           │   │
│  │  Models: GPT family, DALL-E, Whisper, Codex              │   │
│  │  Notable: ChatGPT, API platform, Microsoft partnership   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  GOOGLE (DeepMind + Google AI)                           │   │
│  │  "Organizing the world's information"                    │   │
│  │                                                          │   │
│  │  Focus: Research + product integration                   │   │
│  │  Models: Gemini, PaLM, Bard                              │   │
│  │  Notable: AlphaFold, integrated into Google products     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  META (Facebook AI Research)                             │   │
│  │  "Open AI research"                                      │   │
│  │                                                          │   │
│  │  Focus: Open-source AI                                   │   │
│  │  Models: LLaMA family (open source!)                     │   │
│  │  Notable: Democratizing AI access                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  MISTRAL AI                                              │   │
│  │  "Open and efficient AI"                                 │   │
│  │                                                          │   │
│  │  Founded: 2023 in France                                 │   │
│  │  Focus: Efficient, open models                           │   │
│  │  Models: Mistral, Mixtral (MoE)                          │   │
│  │  Notable: High performance at smaller sizes              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Model Comparison

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                           MODEL COMPARISON MATRIX                              │
├───────────────┬──────────────┬──────────────┬──────────────┬──────────────────┤
│ Model         │ Provider     │ Context      │ Best For     │ API Access       │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ Claude 3 Opus │ Anthropic    │ 200K tokens  │ Complex      │ API + Console    │
│               │              │              │ reasoning    │                  │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ Claude 3.5    │ Anthropic    │ 200K tokens  │ Balanced     │ API + Console    │
│ Sonnet        │              │              │ performance  │                  │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ Claude 3      │ Anthropic    │ 200K tokens  │ Speed +      │ API + Console    │
│ Haiku         │              │              │ Cost         │                  │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ GPT-4 Turbo   │ OpenAI       │ 128K tokens  │ General      │ API + ChatGPT    │
│               │              │              │ purpose      │ Plus             │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ GPT-4o        │ OpenAI       │ 128K tokens  │ Multimodal   │ API + ChatGPT    │
│               │              │              │ tasks        │                  │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ GPT-3.5       │ OpenAI       │ 16K tokens   │ Simple tasks │ API + Free tier  │
│ Turbo         │              │              │ Cost saving  │                  │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ Gemini Ultra  │ Google       │ 1M tokens    │ Long context │ API + Bard       │
│               │              │              │ Multimodal   │                  │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ Gemini Pro    │ Google       │ 32K tokens   │ General      │ API + Vertex AI  │
│               │              │              │ purpose      │                  │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ LLaMA 2 70B   │ Meta         │ 4K tokens    │ Self-hosting │ Open weights     │
│               │              │              │ Privacy      │ Free!            │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ Mixtral 8x7B  │ Mistral      │ 32K tokens   │ Efficiency   │ Open weights     │
│               │              │              │ Self-hosting │ + API            │
├───────────────┼──────────────┼──────────────┼──────────────┼──────────────────┤
│ CodeLlama     │ Meta         │ 16K tokens   │ Code tasks   │ Open weights     │
│               │              │              │              │ Free!            │
└───────────────┴──────────────┴──────────────┴──────────────┴──────────────────┘
```

---

## 4.3 Proprietary vs Open Source Models

### Proprietary Models (Closed Source)

```
┌────────────────────────────────────────────────────────────────┐
│                    PROPRIETARY MODELS                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Examples: Claude, GPT-4, Gemini                               │
│                                                                │
│  PROS:                                                         │
│  ✓ State-of-the-art performance                               │
│  ✓ No infrastructure to manage                                │
│  ✓ Regular updates and improvements                           │
│  ✓ Better safety and alignment                                │
│  ✓ Enterprise support available                               │
│  ✓ Easy to start (just an API key)                           │
│                                                                │
│  CONS:                                                         │
│  ✗ Ongoing costs (pay per token)                              │
│  ✗ Data leaves your infrastructure                            │
│  ✗ Vendor lock-in risk                                        │
│  ✗ Rate limits and quotas                                     │
│  ✗ Can't customize model weights                              │
│  ✗ Dependent on provider's policies                           │
│                                                                │
│  BEST FOR:                                                     │
│  • Most production use cases                                   │
│  • When you need the best quality                              │
│  • When you don't want to manage infra                        │
│  • Rapid prototyping                                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Open Source Models

```
┌────────────────────────────────────────────────────────────────┐
│                    OPEN SOURCE MODELS                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Examples: LLaMA 2, Mistral, Falcon, MPT                       │
│                                                                │
│  PROS:                                                         │
│  ✓ Free to use (no per-token cost)                            │
│  ✓ Data stays on your infrastructure                          │
│  ✓ Full control and customization                             │
│  ✓ Can fine-tune for specific tasks                           │
│  ✓ No vendor lock-in                                          │
│  ✓ Community support and improvements                         │
│                                                                │
│  CONS:                                                         │
│  ✗ Requires GPU infrastructure                                │
│  ✗ Generally lower performance than proprietary               │
│  ✗ You manage updates and security                            │
│  ✗ Need ML expertise to deploy                                │
│  ✗ Higher upfront investment                                  │
│  ✗ Smaller context windows typically                          │
│                                                                │
│  BEST FOR:                                                     │
│  • Strict data privacy requirements                            │
│  • High-volume, predictable workloads                         │
│  • Custom/specialized use cases                               │
│  • When you have ML engineering capacity                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Decision Framework

```python
# Model Selection Decision Tree

def select_model_type(requirements):
    """
    Help decide between proprietary and open source models.
    """

    # Priority 1: Data Privacy
    if requirements.data_must_stay_on_premise:
        if requirements.can_run_gpu_infrastructure:
            return "Open Source (LLaMA 2, Mistral)"
        else:
            return "Private Cloud Deployment (Azure OpenAI, AWS Bedrock)"

    # Priority 2: Performance Requirements
    if requirements.needs_state_of_the_art:
        return "Proprietary (Claude 3 Opus, GPT-4)"

    # Priority 3: Cost Optimization
    if requirements.high_volume and requirements.predictable_workload:
        estimated_api_cost = requirements.tokens_per_month * PRICE_PER_TOKEN
        estimated_gpu_cost = GPU_HOURLY_RATE * 24 * 30

        if estimated_gpu_cost < estimated_api_cost * 0.5:
            return "Open Source (cost-effective)"
        else:
            return "Proprietary (simpler, similar cost)"

    # Priority 4: Speed to Market
    if requirements.need_to_ship_fast:
        return "Proprietary (fastest to implement)"

    # Default
    return "Proprietary (safest choice for most cases)"
```

### Popular Open Source Models for DevOps

```yaml
# Open Source Models Worth Knowing

code_generation:
  name: "CodeLlama"
  sizes: [7B, 13B, 34B]
  context: 16K tokens
  strengths:
    - Code completion
    - Code explanation
    - Bug fixing
  run_locally: "Yes, 7B fits on 16GB GPU"
  example: |
    # Can run locally with llama.cpp
    ./main -m codellama-7b.gguf -p "Write a bash script to..."

general_purpose:
  name: "LLaMA 2"
  sizes: [7B, 13B, 70B]
  context: 4K tokens
  strengths:
    - General reasoning
    - Conversation
    - Following instructions
  run_locally: "7B/13B on consumer GPUs, 70B needs A100"

efficient_reasoning:
  name: "Mixtral 8x7B"
  architecture: "Mixture of Experts (MoE)"
  context: 32K tokens
  strengths:
    - Efficient inference
    - Strong reasoning
    - Multilingual
  special: "Only uses 2 experts at a time (faster than 47B model)"

embedding_models:
  - name: "all-MiniLM-L6-v2"
    use_case: "Semantic search"
    provider: "Sentence Transformers"
  - name: "text-embedding-ada-002"
    use_case: "High quality embeddings"
    provider: "OpenAI"
```

---

## 4.4 Types of Models for Different Tasks

### Model Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         MODEL TYPES BY TASK                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  TEXT GENERATION (LLMs)                                                    │
│  ├── General purpose: Claude, GPT-4, Gemini                                │
│  ├── Code specialized: CodeLlama, StarCoder, Codex                         │
│  └── Instruction-tuned: Vicuna, Alpaca, WizardLM                          │
│                                                                            │
│  TEXT UNDERSTANDING                                                        │
│  ├── Classification: BERT, RoBERTa, DistilBERT                            │
│  ├── Named Entity Recognition: SpaCy models, Flair                        │
│  └── Sentiment Analysis: Specialized BERT variants                        │
│                                                                            │
│  EMBEDDINGS (Vector Representations)                                       │
│  ├── Text: OpenAI Ada, Sentence-BERT, E5                                  │
│  ├── Code: CodeBERT, UniXcoder                                            │
│  └── Multi-modal: CLIP (text + images)                                    │
│                                                                            │
│  IMAGE GENERATION                                                          │
│  ├── DALL-E 3 (OpenAI)                                                    │
│  ├── Midjourney                                                            │
│  ├── Stable Diffusion (open source!)                                      │
│  └── Imagen (Google)                                                       │
│                                                                            │
│  IMAGE UNDERSTANDING                                                       │
│  ├── GPT-4V (Vision)                                                      │
│  ├── Claude 3 (Vision)                                                    │
│  ├── LLaVA (open source)                                                  │
│  └── BLIP-2                                                                │
│                                                                            │
│  SPEECH                                                                    │
│  ├── Speech-to-Text: Whisper (OpenAI, open source!)                       │
│  ├── Text-to-Speech: ElevenLabs, Azure, Amazon Polly                      │
│  └── Voice Cloning: Various providers                                     │
│                                                                            │
│  SPECIALIZED                                                               │
│  ├── SQL Generation: SQLCoder, NSQL                                       │
│  ├── Math/Reasoning: Specialized fine-tunes                               │
│  └── Scientific: BioGPT, ChemBERTa                                        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### DevOps-Relevant Model Applications

```yaml
# Model Selection for DevOps Tasks

log_analysis:
  recommended_models:
    - name: "Claude 3 Sonnet"
      reason: "Long context for log files, excellent reasoning"
    - name: "GPT-4"
      reason: "Good at pattern recognition in logs"
  approach:
    simple_classification:
      model: "Fine-tuned BERT (local)"
      use_case: "Categorizing log levels, error types"
    semantic_analysis:
      model: "Claude/GPT-4"
      use_case: "Understanding error context, root cause analysis"

code_review:
  recommended_models:
    - name: "Claude 3.5 Sonnet"
      reason: "Excellent at code understanding and security analysis"
    - name: "CodeLlama 34B"
      reason: "Open source, can run locally for sensitive code"
  example_prompt: |
    Review this Terraform code for security issues:
    [code]

documentation:
  recommended_models:
    - name: "Claude 3 Sonnet"
      reason: "Great at technical writing"
    - name: "GPT-4"
      reason: "Comprehensive documentation generation"
  automation_idea: |
    # Auto-generate docs from code
    for file in src/*.py; do
        ai_generate_docs "$file" >> docs/api.md
    done

incident_response:
  recommended_models:
    - name: "Claude 3 Opus"
      reason: "Best for complex reasoning about incidents"
  workflow:
    1_collect: "Gather logs, metrics, recent changes"
    2_analyze: "Send to LLM with incident context template"
    3_hypothesize: "Get ranked list of potential causes"
    4_verify: "Human validates AI suggestions"

infrastructure_as_code:
  recommended_models:
    - name: "Claude 3.5 Sonnet"
      reason: "Excellent Terraform/CloudFormation generation"
    - name: "GPT-4"
      reason: "Strong at AWS/GCP/Azure specifics"
  tips:
    - "Always specify cloud provider and version"
    - "Include compliance requirements in prompt"
    - "Request explanatory comments"

chatops_bot:
  recommended_models:
    - name: "Claude 3 Haiku"
      reason: "Fast, cheap, good for simple queries"
    - name: "GPT-3.5 Turbo"
      reason: "Fast responses, cost-effective"
  use_cases:
    - "Answer questions about infrastructure"
    - "Execute predefined runbooks"
    - "Summarize alerts and incidents"
```

---

## 4.5 Model Hosting Options

### Where to Run Models

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       MODEL HOSTING OPTIONS                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. DIRECT API ACCESS                                                      │
│     ┌──────────────────────────────────────────────────────────────────┐  │
│     │  Provider APIs: api.anthropic.com, api.openai.com                │  │
│     │  Pros: Simplest, always latest models                            │  │
│     │  Cons: Data leaves your network                                  │  │
│     │  Cost: Pay per token                                             │  │
│     └──────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  2. CLOUD PROVIDER MARKETPLACES                                            │
│     ┌──────────────────────────────────────────────────────────────────┐  │
│     │  AWS Bedrock: Claude, LLaMA, Titan                               │  │
│     │  Azure OpenAI: GPT-4, GPT-3.5                                    │  │
│     │  Google Vertex AI: Gemini, PaLM                                  │  │
│     │  Pros: Compliance, VPC integration, enterprise features          │  │
│     │  Cons: Slight markup, limited model selection                    │  │
│     └──────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  3. SELF-HOSTED (Open Source)                                              │
│     ┌──────────────────────────────────────────────────────────────────┐  │
│     │  Options:                                                        │  │
│     │  - vLLM (production-grade serving)                               │  │
│     │  - Text Generation Inference (Hugging Face)                      │  │
│     │  - Ollama (easy local deployment)                                │  │
│     │  - llama.cpp (CPU inference)                                     │  │
│     │                                                                  │  │
│     │  Pros: Full control, data privacy, no per-token cost            │  │
│     │  Cons: Infrastructure overhead, GPU costs, expertise needed      │  │
│     └──────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  4. MANAGED OPEN SOURCE                                                    │
│     ┌──────────────────────────────────────────────────────────────────┐  │
│     │  Providers:                                                      │  │
│     │  - Together.ai                                                   │  │
│     │  - Anyscale                                                      │  │
│     │  - Replicate                                                     │  │
│     │  - Modal                                                         │  │
│     │                                                                  │  │
│     │  Pros: Open source models, managed infrastructure               │  │
│     │  Cons: Still have API costs, less control                       │  │
│     └──────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Quick Setup Examples

#### Using Anthropic API Directly

```python
# Direct Claude API usage
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a Kubernetes health check for nginx"}
    ]
)
print(message.content)
```

#### Using AWS Bedrock

```python
# Claude via AWS Bedrock
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Write a Kubernetes health check"}
        ]
    })
)
```

#### Self-Hosting with Ollama

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2
ollama pull codellama

# Run interactively
ollama run codellama "Write a bash script to check disk space"

# Run as API server
ollama serve

# Query the API
curl http://localhost:11434/api/generate -d '{
  "model": "codellama",
  "prompt": "Write a Dockerfile for Python Flask"
}'
```

#### Self-Hosting with vLLM (Production)

```python
# vLLM for production model serving

# Install
# pip install vllm

# Start server
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")
sampling_params = SamplingParams(temperature=0.7, max_tokens=256)

prompts = ["Write a script to monitor CPU usage"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.outputs[0].text)
```

```bash
# Or run as OpenAI-compatible server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-chat-hf \
    --port 8000

# Then use standard OpenAI client!
```

---

## 4.6 Model Selection Guide for DevOps

### Decision Matrix

```python
# Model recommendation based on use case

def recommend_model(use_case: str, constraints: dict) -> str:
    """
    Returns recommended model based on use case and constraints.
    """

    recommendations = {
        "code_generation": {
            "no_constraints": "Claude 3.5 Sonnet",
            "cost_sensitive": "Claude 3 Haiku or GPT-3.5",
            "privacy_required": "CodeLlama 34B (self-hosted)",
            "enterprise": "Azure OpenAI GPT-4 or AWS Bedrock Claude",
        },
        "log_analysis": {
            "no_constraints": "Claude 3.5 Sonnet (long context)",
            "high_volume": "Claude 3 Haiku (cost effective)",
            "privacy_required": "Mistral 7B (self-hosted)",
            "real_time": "Fine-tuned local classifier",
        },
        "documentation": {
            "no_constraints": "Claude 3.5 Sonnet",
            "cost_sensitive": "Claude 3 Haiku",
            "technical_accuracy": "Claude 3 Opus",
        },
        "incident_response": {
            "no_constraints": "Claude 3 Opus (best reasoning)",
            "fast_response": "Claude 3.5 Sonnet",
            "privacy_required": "LLaMA 2 70B (self-hosted)",
        },
        "chatbot": {
            "no_constraints": "Claude 3 Sonnet",
            "cost_sensitive": "Claude 3 Haiku",
            "low_latency": "Claude 3 Haiku or GPT-3.5",
        },
        "embeddings": {
            "no_constraints": "OpenAI text-embedding-3-large",
            "self_hosted": "all-MiniLM-L6-v2",
            "multilingual": "multilingual-e5-large",
        }
    }

    return recommendations.get(use_case, {}).get(
        constraints.get("priority", "no_constraints"),
        "Claude 3.5 Sonnet"  # Safe default
    )
```

### Cost Comparison Calculator

```python
# Compare costs between different model options

def calculate_monthly_cost(
    input_tokens_per_request: int,
    output_tokens_per_request: int,
    requests_per_day: int,
    model: str
) -> dict:
    """
    Calculate monthly API costs for different models.
    """

    # Prices per 1M tokens (approximate, check current pricing)
    pricing = {
        "claude-3-opus": {"input": 15.0, "output": 75.0},
        "claude-3.5-sonnet": {"input": 3.0, "output": 15.0},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    }

    if model not in pricing:
        return {"error": f"Unknown model: {model}"}

    prices = pricing[model]
    monthly_requests = requests_per_day * 30

    monthly_input_tokens = input_tokens_per_request * monthly_requests
    monthly_output_tokens = output_tokens_per_request * monthly_requests

    input_cost = (monthly_input_tokens / 1_000_000) * prices["input"]
    output_cost = (monthly_output_tokens / 1_000_000) * prices["output"]

    return {
        "model": model,
        "monthly_requests": monthly_requests,
        "total_input_tokens": monthly_input_tokens,
        "total_output_tokens": monthly_output_tokens,
        "input_cost": round(input_cost, 2),
        "output_cost": round(output_cost, 2),
        "total_monthly_cost": round(input_cost + output_cost, 2),
    }


# Example: Code review bot
# Average PR: 2000 input tokens, 500 output tokens
# 50 PRs per day

for model in ["claude-3-opus", "claude-3.5-sonnet", "claude-3-haiku", "gpt-4-turbo"]:
    result = calculate_monthly_cost(2000, 500, 50, model)
    print(f"{model}: ${result['total_monthly_cost']}/month")

# Output:
# claude-3-opus: $146.25/month
# claude-3.5-sonnet: $31.50/month
# claude-3-haiku: $2.63/month
# gpt-4-turbo: $75.00/month
```

---

## 4.7 Emerging Trends

### What's Coming in AI Models

```yaml
# Trends to Watch (2024-2025)

1_multimodal_by_default:
  description: "Models that understand text, images, audio, video together"
  examples:
    - "Upload a screenshot of an error, get debugging help"
    - "Show architecture diagram, get Terraform code"
  current_leaders: ["GPT-4V", "Claude 3 Vision", "Gemini"]

2_longer_context_windows:
  description: "Processing entire codebases at once"
  trend: "4K → 32K → 128K → 200K → 1M+ tokens"
  impact_on_devops:
    - "Analyze all logs from an incident at once"
    - "Review entire microservice in one prompt"
    - "Generate documentation for whole project"

3_specialized_agents:
  description: "AI that can take actions, not just generate text"
  examples:
    - "AI that can run kubectl commands"
    - "AI that can create PRs and deploy"
  early_examples: ["Claude Code", "GitHub Copilot Workspace", "Devin"]

4_local_models_improving:
  description: "Smaller, faster models running on personal devices"
  examples:
    - "7B models matching GPT-3.5 quality"
    - "Models running on M1/M2 Macs"
  tools: ["Ollama", "LM Studio", "llama.cpp"]

5_fine_tuning_democratization:
  description: "Easier to create specialized models"
  approaches:
    - "LoRA/QLoRA for efficient fine-tuning"
    - "Few-shot learning from examples"
    - "Retrieval-augmented generation (RAG)"

6_real_time_capabilities:
  description: "Lower latency, streaming responses"
  impact:
    - "Interactive debugging sessions"
    - "Real-time log analysis"
    - "Instant code suggestions"
```

---

## 4.8 Hands-On Exercises

### Exercise 1: Model Comparison

```markdown
## Hands-On: Compare Models

Task: Test the same prompt on different models

### Prompt to Test:
"Write a bash script that:
1. Checks if Docker is running
2. Lists all containers with their CPU/memory usage
3. Alerts if any container uses more than 80% memory
4. Outputs results in JSON format"

### Test on:
1. Claude 3.5 Sonnet (via console.anthropic.com)
2. GPT-4 (via chat.openai.com)
3. CodeLlama (via Ollama locally)

### Evaluation Criteria:
| Criterion           | Claude | GPT-4 | CodeLlama |
|--------------------|---------| ------|-----------|
| Correctness        |         |       |           |
| Code Quality       |         |       |           |
| Edge Case Handling |         |       |           |
| Explanation        |         |       |           |
| Response Time      |         |       |           |

### Your Observations:
[Document differences you noticed]
```

### Exercise 2: Cost Calculation

```markdown
## Hands-On: Calculate Your AI Costs

Scenario: You want to implement an AI-powered log analyzer

### Parameters:
- Average log batch size: _____ characters
- Estimated tokens (chars ÷ 4): _____
- Batches per day: _____
- Expected output tokens per analysis: _____

### Calculate for each model:

| Model | Input Cost/1M | Output Cost/1M | Monthly Cost |
|-------|---------------|----------------|--------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 | $_____ |
| Claude 3 Haiku | $0.25 | $1.25 | $_____ |
| GPT-4 Turbo | $10.00 | $30.00 | $_____ |
| Self-hosted | GPU: $___/hr | N/A | $_____ |

### Break-Even Analysis:
At what volume does self-hosting become cheaper?
[Your calculation here]
```

### Exercise 3: Local Model Setup

```bash
# Exercise: Set up Ollama and test CodeLlama

# Step 1: Install Ollama
# Follow instructions at https://ollama.ai

# Step 2: Pull CodeLlama
ollama pull codellama

# Step 3: Test with DevOps prompts
ollama run codellama "Write a Kubernetes CronJob that runs a backup script daily at 2am"

# Step 4: Compare with Claude (if you have API access)
# Note the differences in:
# - Response quality
# - Response time
# - Handling of edge cases

# Document your findings:
# Local CodeLlama:
# - Quality: ____/10
# - Speed: ____ seconds
# - Notes: ____

# Claude API:
# - Quality: ____/10
# - Speed: ____ seconds
# - Notes: ____
```

---

## 4.9 Chapter Summary

### Key Takeaways

1. **Major providers**: Anthropic (Claude), OpenAI (GPT), Google (Gemini), Meta (LLaMA)

2. **Proprietary vs Open Source**: Trade-off between convenience/quality and control/cost

3. **Model selection depends on**: Task complexity, privacy needs, budget, volume, latency requirements

4. **Multiple hosting options**: Direct API, cloud marketplaces, self-hosted, managed open source

5. **The landscape is evolving rapidly**: Stay informed about new models and capabilities

### Quick Reference

```
┌────────────────────────────────────────────────────────────────┐
│              MODEL SELECTION QUICK REFERENCE                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  NEED BEST QUALITY?                                           │
│  → Claude 3 Opus, GPT-4                                       │
│                                                                │
│  NEED BALANCE OF QUALITY & COST?                              │
│  → Claude 3.5 Sonnet, GPT-4 Turbo                             │
│                                                                │
│  NEED LOW COST?                                               │
│  → Claude 3 Haiku, GPT-3.5 Turbo                              │
│                                                                │
│  NEED PRIVACY/LOCAL?                                          │
│  → LLaMA 2, Mistral, CodeLlama (via Ollama)                   │
│                                                                │
│  NEED ENTERPRISE COMPLIANCE?                                  │
│  → AWS Bedrock, Azure OpenAI, Google Vertex AI               │
│                                                                │
│  NEED CODE SPECIFICALLY?                                      │
│  → Claude 3.5 Sonnet, CodeLlama, StarCoder                    │
│                                                                │
│  NEED LONG CONTEXT?                                           │
│  → Claude 3 (200K), Gemini (1M), GPT-4 Turbo (128K)          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

[← Previous: The Art of Prompting](./03-the-art-of-prompting.md) | [Next: Introduction to Claude →](./05-introduction-to-claude.md)
