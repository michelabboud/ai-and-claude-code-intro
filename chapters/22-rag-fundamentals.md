# Chapter 22: RAG Fundamentals

**Part 8: Advanced Agentic Development**

---

## Navigation

← Previous: [Chapter 21: Resilient Agentic Systems](./21-resilient-agentic-systems.md) | Next: [Chapter 23: Advanced RAG Patterns](./23-advanced-rag-patterns.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

## Introduction to Retrieval-Augmented Generation

**TL;DR:** Learn how to give AI agents access to custom knowledge bases through RAG (Retrieval-Augmented Generation). Build production-ready RAG systems that search documentation, runbooks, and logs to provide accurate, context-aware responses.

**What You'll Learn:**
- How RAG works and why it's essential for production AI
- Vector embeddings and semantic search fundamentals
- Chunking strategies for different document types
- Building your first RAG system with real code
- Vector database options (Chroma, FAISS, Pinecone, Weaviate)
- Query transformation and optimization techniques
- Context window management for LLMs
- DevOps-specific RAG applications

**What You'll Build:**
- Documentation search system for your infrastructure
- Runbook retrieval for incident response
- Log analysis with semantic search
- Production-ready RAG pipeline with caching

---

## Quick Navigation

- [What is RAG?](#1-what-is-rag)
- [Vector Embeddings Explained](#2-understanding-vector-embeddings)
- [Vector Databases](#3-vector-databases)
- [Document Chunking](#4-document-chunking-strategies)
- [Building Your First RAG](#5-building-your-first-rag-system)
- [Query Transformation](#6-query-transformation-techniques)
- [Context Management](#7-context-window-management)
- [Real-World Scenarios](#8-real-world-devops-rag-scenarios)

---

## 1. What is RAG?

### The Problem: LLMs Don't Know Your Data

**Scenario:** You ask Claude Code about your company's deployment process:

```
You: "How do I deploy to our production Kubernetes cluster?"

Claude: "I don't have access to your specific deployment procedures.
         I can provide general Kubernetes deployment guidance..."
```

**Why?** LLMs are trained on public data. They don't know:
- Your company's internal documentation
- Your infrastructure runbooks
- Your team's best practices
- Your custom configurations
- Recent incidents and solutions

### The Solution: Retrieval-Augmented Generation (RAG)

**RAG = Retrieve relevant information + Generate response using that information**

```
┌─────────────────────────────────────────────────────────────┐
│                        RAG WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. User Query: "How do I deploy to production?"           │
│                          ↓                                  │
│  2. Retrieve: Search internal docs, find relevant chunks   │
│                          ↓                                  │
│  3. Augment: Add retrieved context to prompt               │
│                          ↓                                  │
│  4. Generate: LLM answers using your custom knowledge      │
│                          ↓                                  │
│  5. Response: "According to our runbook, run: kubectl..."  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Why RAG Matters for DevOps

**Traditional Approach:**
- Engineer: Searches Confluence manually
- Finds 10 outdated pages
- Reads through each one
- **Time:** 15-30 minutes per query

**RAG Approach:**
- Engineer: Asks AI agent
- Agent retrieves relevant docs automatically
- Provides answer with citations
- **Time:** 10-30 seconds per query

**Production Benefits:**
- ✅ **Faster incident response** (minutes → seconds)
- ✅ **Reduced context switching** (stay in terminal/Slack)
- ✅ **Always up-to-date** (syncs with live documentation)
- ✅ **Onboarding acceleration** (new engineers get instant answers)
- ✅ **Knowledge preservation** (tribal knowledge → searchable system)

### Real-World Example: PagerDuty Integration

**Without RAG:**
```
🚨 Alert: High CPU usage on prod-api-03
→ Engineer checks Grafana
→ Searches Confluence for "high CPU runbook"
→ Finds 3 outdated runbooks
→ Asks in Slack #oncall channel
→ Waits for response (15 min)
→ Finally applies fix
MTTR: 35 minutes
```

**With RAG:**
```
🚨 Alert: High CPU usage on prod-api-03
→ Engineer: "What's the runbook for high CPU on prod-api?"
→ RAG Agent: "According to runbook-cpu-2024-12.md:
   1. Check for memory leaks: kubectl top pods
   2. Review recent deploys: kubectl rollout history
   3. If leak detected: kubectl rollout undo
   4. Monitor recovery: watch kubectl get pods"
→ Engineer applies fix immediately
MTTR: 5 minutes
```

**Impact:** 85% reduction in MTTR (Mean Time To Resolution)

---

## 2. Understanding Vector Embeddings

### What Are Embeddings?

**Embeddings** = Converting text into numbers (vectors) that capture meaning

**Analogy:**

Think of embeddings like GPS coordinates:
- "New York" → [40.7128° N, 74.0060° W]
- "Boston" → [42.3601° N, 71.0589° W]

Close coordinates = geographically close cities
Close embeddings = semantically similar texts

### How Embeddings Work

**Example: Converting sentences to vectors**

```python
# Text → Embedding (simplified representation)
"Deploy the application" → [0.2, 0.8, 0.1, 0.5, ...]  # 1536 dimensions
"Push code to production" → [0.3, 0.7, 0.2, 0.4, ...]
"Order pizza for dinner" → [-0.5, -0.2, 0.9, -0.3, ...]

# Similar meanings = close vectors
distance("Deploy app", "Push to prod") = 0.15  # Very similar!
distance("Deploy app", "Order pizza") = 0.89   # Very different!
```

### Semantic Search vs Keyword Search

**Keyword Search (Traditional):**
```
Query: "deploy to production"
Matches: Documents containing exact words "deploy", "production"
Misses: Documents saying "push to prod", "release to live environment"
```

**Semantic Search (RAG with Embeddings):**
```
Query: "deploy to production"
Matches:
  ✓ "deploy to production"
  ✓ "push to prod"
  ✓ "release to live environment"
  ✓ "ship code to customers"
  ✓ "go-live procedures"
```

**Why This Matters:**

Engineers use different terminology:
- "Deploy" vs "Push" vs "Release" vs "Ship"
- "Production" vs "Prod" vs "Live" vs "Customer-facing"
- "Kubernetes" vs "k8s" vs "orchestrator"

Semantic search understands they mean the same thing!

### Embedding Models

**Popular Embedding Models:**

| Model | Provider | Dimensions | Best For |
|-------|----------|------------|----------|
| **text-embedding-3-small** | OpenAI | 1536 | General purpose, fast |
| **text-embedding-3-large** | OpenAI | 3072 | Highest quality |
| **voyage-02** | Voyage AI | 1024 | Code and technical docs |
| **e5-mistral-7b** | HuggingFace | 4096 | Open source, self-hosted |

**Cost Considerations:**

```python
# OpenAI Pricing (as of 2026)
text-embedding-3-small: $0.02 / 1M tokens
text-embedding-3-large: $0.13 / 1M tokens

# Example: Embedding 10,000 docs (100 tokens each)
# = 1M tokens = $0.02 (small) or $0.13 (large)
```

**For DevOps:** Use `text-embedding-3-small` for most cases (fast + cheap)

### Similarity Metrics

**How to measure "closeness" between vectors:**

1. **Cosine Similarity** (most common for RAG)
   - Range: -1 (opposite) to 1 (identical)
   - Measures angle between vectors
   - Works well for text embeddings

2. **Euclidean Distance**
   - Range: 0 (identical) to ∞ (very different)
   - Measures straight-line distance
   - Sensitive to vector magnitude

3. **Dot Product**
   - Faster than cosine similarity
   - Works if vectors are normalized

**Example:**

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Example vectors (simplified to 3D for visualization)
deploy_vec = np.array([0.8, 0.2, 0.1])
release_vec = np.array([0.7, 0.3, 0.15])
pizza_vec = np.array([0.1, 0.1, 0.9])

print(f"deploy ↔ release: {cosine_similarity(deploy_vec, release_vec):.3f}")
# Output: 0.989 (very similar!)

print(f"deploy ↔ pizza: {cosine_similarity(deploy_vec, pizza_vec):.3f}")
# Output: 0.194 (very different!)
```

---

## 3. Vector Databases

### Why Not Use Regular Databases?

**Traditional SQL Database:**
```sql
-- ❌ Can't do this efficiently
SELECT * FROM documents
WHERE embedding SIMILAR TO [0.2, 0.8, 0.1, ...];
```

**Problems:**
- No native vector similarity search
- Slow for high-dimensional vectors (1536+ dimensions)
- Can't scale to millions of vectors efficiently

**Vector Database:**
```python
# ✅ Optimized for this
results = vector_db.search(
    query_embedding=[0.2, 0.8, 0.1, ...],
    top_k=5
)
```

**Features:**
- Fast similarity search (milliseconds)
- Approximate Nearest Neighbor (ANN) algorithms
- Scales to billions of vectors
- Built-in metadata filtering

### Vector Database Options

#### Option 1: ChromaDB (Easy, Local)

**Best for:** Development, small projects, prototyping

**Pros:**
- ✅ Easy setup (pip install)
- ✅ Runs locally (no external service)
- ✅ Open source
- ✅ Good documentation

**Cons:**
- ⚠️ Not designed for massive scale
- ⚠️ In-memory (data loss if crash without persistence)

**Installation:**

```bash
pip install chromadb
```

**Example:**

```python
import chromadb

# Create client
client = chromadb.Client()

# Create collection
collection = client.create_collection("runbooks")

# Add documents
collection.add(
    documents=[
        "To deploy to production, run: kubectl apply -f deployment.yaml",
        "For rollback, use: kubectl rollout undo deployment/my-app",
        "Check pod status with: kubectl get pods -n production"
    ],
    metadatas=[
        {"source": "k8s-deploy.md", "date": "2024-01-10"},
        {"source": "k8s-rollback.md", "date": "2024-01-10"},
        {"source": "k8s-status.md", "date": "2024-01-05"}
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Query
results = collection.query(
    query_texts=["How do I rollback a deployment?"],
    n_results=2
)

print(results['documents'])
# Output: ['For rollback, use: kubectl rollout undo...', ...]
```

#### Option 2: FAISS (Fast, Local)

**Best for:** High-performance local search, research, experimentation

**Pros:**
- ✅ Extremely fast (built by Facebook AI)
- ✅ Handles millions of vectors
- ✅ Multiple index types (IVF, HNSW)
- ✅ GPU acceleration support

**Cons:**
- ⚠️ More complex setup
- ⚠️ No built-in persistence (need to save/load manually)
- ⚠️ No metadata filtering (need separate database)

**Installation:**

```bash
pip install faiss-cpu  # or faiss-gpu for GPU support
```

**Example:**

```python
import faiss
import numpy as np

# Create FAISS index (L2 distance)
dimension = 1536  # OpenAI embedding size
index = faiss.IndexFlatL2(dimension)

# Add vectors
embeddings = np.random.random((1000, dimension)).astype('float32')
index.add(embeddings)

# Search
query_vector = np.random.random((1, dimension)).astype('float32')
distances, indices = index.search(query_vector, k=5)

print(f"Top 5 similar documents: {indices[0]}")
# Output: [342, 89, 567, 23, 891]
```

#### Option 3: Pinecone (Managed, Production)

**Best for:** Production deployments, scaling to millions of documents

**Pros:**
- ✅ Fully managed (no infrastructure to maintain)
- ✅ Scales automatically
- ✅ High availability
- ✅ Built-in metadata filtering
- ✅ Hybrid search (vector + metadata)

**Cons:**
- 💰 Paid service ($70+/month for production)
- ⚠️ External dependency
- ⚠️ Requires internet connection

**Installation:**

```bash
pip install pinecone-client
```

**Example:**

```python
import pinecone

# Initialize
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")

# Create index
pinecone.create_index("runbooks", dimension=1536, metric="cosine")
index = pinecone.Index("runbooks")

# Upsert vectors
index.upsert(vectors=[
    ("doc1", [0.1, 0.2, ...], {"source": "k8s-deploy.md"}),
    ("doc2", [0.3, 0.4, ...], {"source": "k8s-rollback.md"}),
])

# Query with metadata filtering
results = index.query(
    vector=[0.5, 0.6, ...],
    top_k=5,
    filter={"source": {"$eq": "k8s-deploy.md"}}
)
```

#### Option 4: Weaviate (Open Source, Production)

**Best for:** Self-hosted production, complex schemas, hybrid search

**Pros:**
- ✅ Open source (free)
- ✅ GraphQL API
- ✅ Built-in ML models
- ✅ Hybrid search (semantic + keyword)
- ✅ Complex filtering

**Cons:**
- ⚠️ More complex setup
- ⚠️ Requires infrastructure management
- ⚠️ Steeper learning curve

**Installation (Docker):**

```bash
docker run -d \
  -p 8080:8080 \
  --name weaviate \
  semitechnologies/weaviate:latest
```

**Example:**

```python
import weaviate

# Connect
client = weaviate.Client("http://localhost:8080")

# Create schema
schema = {
    "class": "Runbook",
    "vectorizer": "text2vec-openai",
    "properties": [
        {"name": "content", "dataType": ["text"]},
        {"name": "source", "dataType": ["string"]},
    ]
}
client.schema.create_class(schema)

# Add data
client.data_object.create(
    data_object={
        "content": "To deploy to production, run: kubectl apply",
        "source": "k8s-deploy.md"
    },
    class_name="Runbook"
)

# Query
results = client.query.get("Runbook", ["content", "source"]) \
    .with_near_text({"concepts": ["how to deploy"]}) \
    .with_limit(5) \
    .do()
```

### Vector Database Comparison

| Feature | ChromaDB | FAISS | Pinecone | Weaviate |
|---------|----------|-------|----------|----------|
| **Setup** | Easy | Medium | Easy | Medium |
| **Cost** | Free | Free | Paid | Free |
| **Scale** | Small | Medium | Large | Large |
| **Hosting** | Local | Local | Cloud | Self/Cloud |
| **Metadata** | ✅ | ❌ | ✅ | ✅ |
| **Hybrid Search** | ❌ | ❌ | Limited | ✅ |
| **Best For** | Dev/Prototype | Research | Production | Production |

**Recommendation for DevOps:**
- **Development:** ChromaDB (easy start)
- **Production (small):** Weaviate (self-hosted, free)
- **Production (large):** Pinecone (managed, scales automatically)

---

## 4. Document Chunking Strategies

### Why Chunking Matters

**Problem:** You can't embed an entire 50-page runbook in one go

**Reasons:**
1. **Embedding model limits:** Most models max out at 8,192 tokens (~6,000 words)
2. **Context window limits:** LLMs have finite context (Claude: 200K tokens, GPT-4: 128K)
3. **Relevance:** Only parts of a document are relevant to a query
4. **Cost:** Smaller chunks = less tokens sent to LLM = lower cost

**Solution:** Split documents into smaller "chunks" before embedding

### Chunking Strategies

#### Strategy 1: Fixed-Size Chunking

**Method:** Split every N characters/tokens with overlap

```python
def fixed_size_chunking(text, chunk_size=500, overlap=50):
    """Split text into fixed-size chunks with overlap"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # Move forward with overlap

    return chunks

# Example
doc = "Deploy to production by running kubectl apply -f deployment.yaml. " \
      "Then verify with kubectl get pods. If issues occur, rollback with kubectl rollout undo..."

chunks = fixed_size_chunking(doc, chunk_size=100, overlap=20)
# Output: ['Deploy to production by running kubectl apply -f deployment.yaml. Then verify with kubectl...',
#          '...verify with kubectl get pods. If issues occur, rollback with kubectl rollout undo...']
```

**Pros:**
- ✅ Simple to implement
- ✅ Predictable chunk sizes
- ✅ Works for any text

**Cons:**
- ⚠️ May split mid-sentence
- ⚠️ Doesn't respect document structure
- ⚠️ Can break code blocks

**Best for:** Quick prototypes, homogeneous text

#### Strategy 2: Sentence-Based Chunking

**Method:** Split at sentence boundaries, group to target size

```python
import nltk
nltk.download('punkt')

def sentence_chunking(text, target_size=500):
    """Split text by sentences, group to target size"""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)

        if current_size + sentence_size > target_size and current_chunk:
            # Save current chunk and start new one
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_size = sentence_size
        else:
            current_chunk.append(sentence)
            current_size += sentence_size

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Example
doc = "Deploy to production. Run kubectl apply. Verify the deployment. Check pod status."
chunks = sentence_chunking(doc, target_size=50)
# Output: ['Deploy to production. Run kubectl apply.',
#          'Verify the deployment. Check pod status.']
```

**Pros:**
- ✅ Preserves sentence boundaries
- ✅ More coherent chunks
- ✅ Better for Q&A

**Cons:**
- ⚠️ Variable chunk sizes
- ⚠️ Still doesn't respect structure
- ⚠️ May split related paragraphs

**Best for:** Prose, documentation, blog posts

#### Strategy 3: Semantic Chunking

**Method:** Split based on topic/semantic coherence

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def semantic_chunking(text, embeddings_func, threshold=0.7):
    """Split text when semantic similarity drops below threshold"""
    sentences = nltk.sent_tokenize(text)

    # Get embeddings for each sentence
    embeddings = [embeddings_func(sent) for sent in sentences]

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        # Calculate similarity with previous sentence
        similarity = cosine_similarity(
            [embeddings[i-1]],
            [embeddings[i]]
        )[0][0]

        if similarity < threshold:
            # Topic changed, start new chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Example usage
doc = "Deploy to production using kubectl. Verify pods are running. " \
      "Next, configure monitoring. Set up Prometheus. Install Grafana dashboards."

chunks = semantic_chunking(doc, embeddings_func=get_embedding, threshold=0.75)
# Output: ['Deploy to production using kubectl. Verify pods are running.',
#          'Next, configure monitoring. Set up Prometheus. Install Grafana dashboards.']
```

**Pros:**
- ✅ Respects topic boundaries
- ✅ Most coherent chunks
- ✅ Better retrieval accuracy

**Cons:**
- ⚠️ Computationally expensive (needs embeddings)
- ⚠️ Slower processing
- ⚠️ Requires tuning threshold

**Best for:** Long documents, mixed topics, high-quality requirements

#### Strategy 4: Document Structure-Aware Chunking

**Method:** Split based on document structure (headers, sections, code blocks)

```python
def markdown_chunking(markdown_text, max_chunk_size=1000):
    """Split Markdown by headers, preserving structure"""
    import re

    # Split by headers (##, ###, etc.)
    sections = re.split(r'(^#{1,6}\s+.+$)', markdown_text, flags=re.MULTILINE)

    chunks = []
    current_header = ""
    current_content = []
    current_size = 0

    for i, section in enumerate(sections):
        if re.match(r'^#{1,6}\s+', section):
            # This is a header
            if current_content:
                # Save previous section
                chunks.append({
                    'header': current_header,
                    'content': '\n'.join(current_content),
                    'metadata': {'section': current_header}
                })
            current_header = section
            current_content = []
            current_size = 0
        else:
            # This is content
            section_size = len(section)

            if current_size + section_size > max_chunk_size and current_content:
                # Save current chunk
                chunks.append({
                    'header': current_header,
                    'content': '\n'.join(current_content),
                    'metadata': {'section': current_header}
                })
                current_content = [section]
                current_size = section_size
            else:
                current_content.append(section)
                current_size += section_size

    if current_content:
        chunks.append({
            'header': current_header,
            'content': '\n'.join(current_content),
            'metadata': {'section': current_header}
        })

    return chunks

# Example
markdown = """
## Deployment

To deploy, run: kubectl apply -f deployment.yaml

### Prerequisites

- kubectl installed
- Access to cluster

## Rollback

If issues occur, rollback with: kubectl rollout undo
"""

chunks = markdown_chunking(markdown, max_chunk_size=200)
# Output: [
#   {'header': '## Deployment', 'content': 'To deploy, run: kubectl apply...'},
#   {'header': '### Prerequisites', 'content': '- kubectl installed...'},
#   {'header': '## Rollback', 'content': 'If issues occur...'}
# ]
```

**Pros:**
- ✅ Preserves document hierarchy
- ✅ Includes context (headers)
- ✅ Perfect for documentation
- ✅ Works with code blocks

**Cons:**
- ⚠️ Requires structured documents
- ⚠️ More complex implementation
- ⚠️ Format-specific (Markdown, HTML, etc.)

**Best for:** Documentation, wikis, runbooks, technical guides

### Chunking Best Practices

**1. Add Overlap**

```python
# ❌ No overlap
chunks = ["chunk 1 content", "chunk 2 content"]

# ✅ With overlap (last sentence of chunk 1 = first sentence of chunk 2)
chunks = [
    "chunk 1 content. Last sentence.",
    "Last sentence. chunk 2 content."
]
```

**Why:** Prevents losing context at chunk boundaries

**2. Include Metadata**

```python
# ❌ Just content
chunks = ["content here"]

# ✅ With metadata
chunks = [{
    'content': "content here",
    'metadata': {
        'source': 'runbook-deploy.md',
        'section': 'Production Deployment',
        'page': 3,
        'date': '2024-01-10'
    }
}]
```

**Why:** Enables filtering, provenance, freshness tracking

**3. Preserve Context**

```python
# ❌ Lost context
chunk = "Run kubectl apply -f deployment.yaml"

# ✅ With context
chunk = "## Kubernetes Deployment\n\nTo deploy to production cluster, run kubectl apply -f deployment.yaml"
```

**Why:** Chunks need to be understandable standalone

**4. Test Chunk Sizes**

```python
# Common chunk sizes (characters)
SMALL_CHUNKS = 200-500    # Good for precise retrieval
MEDIUM_CHUNKS = 500-1000  # Balanced (recommended)
LARGE_CHUNKS = 1000-2000  # Good for broader context
```

**Testing:**

```python
def test_chunk_sizes(documents, query, sizes=[500, 1000, 1500]):
    """Test different chunk sizes for retrieval quality"""
    results = {}

    for size in sizes:
        chunks = chunk_documents(documents, chunk_size=size)
        index = create_index(chunks)
        retrieved = search(index, query, top_k=5)

        # Evaluate quality (e.g., manual review or automated metrics)
        results[size] = evaluate_results(retrieved, query)

    return results
```

### DevOps-Specific Chunking Examples

#### Example 1: Kubernetes Runbook

```python
# Runbook structure
runbook = """
# Incident: High CPU Usage

## Diagnosis

1. Check pod metrics:
   ```bash
   kubectl top pods -n production
   ```

2. Review recent deployments:
   ```bash
   kubectl rollout history deployment/my-app -n production
   ```

## Resolution

If memory leak detected:
```bash
kubectl rollout undo deployment/my-app -n production
```

## Prevention

Add resource limits to deployment:
```yaml
resources:
  limits:
    cpu: "1000m"
    memory: "512Mi"
```
"""

# Chunk by sections (Diagnosis, Resolution, Prevention)
chunks = markdown_chunking(runbook)
# Each chunk preserves code blocks and context
```

#### Example 2: Terraform Documentation

```python
# Terraform module docs
terraform_doc = """
## AWS ECS Module

### Usage

module "ecs_cluster" {
  source = "./modules/ecs"

  cluster_name    = "production"
  instance_type   = "t3.large"
  desired_capacity = 3
}

### Outputs

- `cluster_id`: The ECS cluster ID
- `security_group_id`: Security group for ECS instances
"""

# Chunk preserving code blocks
chunks = markdown_chunking(terraform_doc)
# Ensures code stays together in one chunk
```

---

## 5. Building Your First RAG System

### Complete RAG Pipeline

Let's build a production-ready RAG system step by step.

**Architecture:**

```
┌──────────────────────────────────────────────────────────────┐
│                     RAG PIPELINE                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Documents → Chunk → Embed → Store → Query → Retrieve       │
│               ↓       ↓       ↓       ↓         ↓           │
│             Text   Vectors   Vector   User   Top-K docs     │
│                              Database Question               │
│                                                              │
│                         ↓                                    │
│                   Generate Response                          │
│                 (LLM with context)                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Step 1: Setup and Dependencies

**Installation:**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install openai chromadb tiktoken
```

**requirements.txt:**

```
openai>=1.10.0
chromadb>=0.4.22
tiktoken>=0.5.2
python-dotenv>=1.0.0
```

### Step 2: Document Loading

```python
"""
document_loader.py - Load and prepare documents for RAG
"""

import os
from pathlib import Path
from typing import List, Dict

def load_markdown_files(directory: str) -> List[Dict]:
    """
    Load all Markdown files from a directory.

    Args:
        directory: Path to directory containing .md files

    Returns:
        List of documents with content and metadata
    """
    documents = []

    for filepath in Path(directory).rglob("*.md"):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        documents.append({
            'content': content,
            'metadata': {
                'source': str(filepath),
                'filename': filepath.name,
                'type': 'markdown'
            }
        })

    return documents


def load_text_files(directory: str, extensions=['.txt', '.log']) -> List[Dict]:
    """Load text/log files"""
    documents = []

    for ext in extensions:
        for filepath in Path(directory).rglob(f"*{ext}"):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            documents.append({
                'content': content,
                'metadata': {
                    'source': str(filepath),
                    'filename': filepath.name,
                    'type': 'text'
                }
            })

    return documents


# Example usage
if __name__ == "__main__":
    # Load documentation
    docs = load_markdown_files("./docs/runbooks")
    print(f"Loaded {len(docs)} documents")

    # Preview first document
    print(f"\nFirst doc: {docs[0]['metadata']['filename']}")
    print(f"Length: {len(docs[0]['content'])} characters")
```

### Step 3: Chunking Implementation

```python
"""
chunker.py - Split documents into chunks for embedding
"""

import tiktoken
from typing import List, Dict

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text using tiktoken"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def chunk_by_tokens(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    model: str = "gpt-4"
) -> List[str]:
    """
    Split text into chunks by token count.

    Args:
        text: Text to chunk
        chunk_size: Target tokens per chunk
        overlap: Overlapping tokens between chunks
        model: Model name for token counting

    Returns:
        List of text chunks
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

        # Move forward with overlap
        start += chunk_size - overlap

    return chunks


def chunk_documents(
    documents: List[Dict],
    chunk_size: int = 500,
    overlap: int = 50
) -> List[Dict]:
    """
    Chunk multiple documents, preserving metadata.

    Returns:
        List of chunks with content and metadata
    """
    all_chunks = []

    for doc in documents:
        content = doc['content']
        metadata = doc['metadata'].copy()

        # Split into chunks
        chunks = chunk_by_tokens(content, chunk_size, overlap)

        # Add metadata to each chunk
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                'content': chunk,
                'metadata': {
                    **metadata,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
            })

    return all_chunks


# Example usage
if __name__ == "__main__":
    # Example document
    doc = {
        'content': "Deploy to production by running kubectl apply. " * 200,
        'metadata': {'source': 'deploy.md'}
    }

    # Chunk it
    chunks = chunk_documents([doc], chunk_size=500, overlap=50)
    print(f"Created {len(chunks)} chunks")

    # Show first chunk
    print(f"\nFirst chunk ({count_tokens(chunks[0]['content'])} tokens):")
    print(chunks[0]['content'][:200])
```

### Step 4: Embedding and Indexing

```python
"""
rag_system.py - Complete RAG system with ChromaDB
"""

import os
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from typing import List, Dict
import tiktoken

class RAGSystem:
    """
    Production RAG system for DevOps documentation.

    Features:
    - Automatic chunking
    - Embedding with OpenAI
    - Vector storage with ChromaDB
    - Semantic search
    """

    def __init__(
        self,
        collection_name: str = "devops_docs",
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        # Initialize OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embedding_model = embedding_model

        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False
        ))

        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(collection_name)
            print(f"✓ Loaded existing collection: {collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"description": "DevOps documentation and runbooks"}
            )
            print(f"✓ Created new collection: {collection_name}")

        # Chunking config
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.encoding_for_model("gpt-4")

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        tokens = self.encoding.encode(text)
        chunks = []
        start = 0

        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            start += self.chunk_size - self.chunk_overlap

        return chunks

    def add_documents(self, documents: List[Dict]):
        """
        Add documents to the RAG system.

        Args:
            documents: List of dicts with 'content' and 'metadata'
        """
        print(f"\n📚 Adding {len(documents)} documents...")

        all_chunks = []
        all_embeddings = []
        all_metadatas = []
        all_ids = []

        doc_id_counter = 0

        for doc in documents:
            content = doc['content']
            metadata = doc['metadata']

            # Chunk the document
            chunks = self.chunk_text(content)
            print(f"  → {metadata.get('filename', 'doc')}: {len(chunks)} chunks")

            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.embed_text(chunk)

                # Create unique ID
                chunk_id = f"doc{doc_id_counter}_chunk{i}"

                all_chunks.append(chunk)
                all_embeddings.append(embedding)
                all_metadatas.append({
                    **metadata,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
                all_ids.append(chunk_id)

                doc_id_counter += 1

        # Add to ChromaDB in batch
        self.collection.add(
            embeddings=all_embeddings,
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )

        print(f"✓ Added {len(all_chunks)} chunks to vector database")

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Dict = None
    ) -> List[Dict]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filter

        Returns:
            List of results with content and metadata
        """
        # Generate query embedding
        query_embedding = self.embed_text(query)

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )

        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })

        return formatted_results

    def generate_response(
        self,
        query: str,
        top_k: int = 5,
        model: str = "gpt-4-turbo-preview"
    ) -> Dict:
        """
        Generate RAG response: retrieve + generate.

        Returns:
            Dict with 'answer', 'sources', and 'context'
        """
        # 1. Retrieve relevant documents
        results = self.search(query, top_k=top_k)

        # 2. Build context from results
        context_parts = []
        sources = []

        for i, result in enumerate(results):
            context_parts.append(f"[{i+1}] {result['content']}")
            sources.append({
                'source': result['metadata'].get('source', 'unknown'),
                'chunk': result['metadata'].get('chunk_index', 0)
            })

        context = "\n\n".join(context_parts)

        # 3. Generate response with LLM
        prompt = f"""You are a helpful DevOps assistant. Answer the question based on the provided context.

Context:
{context}

Question: {query}

Instructions:
- Answer based on the context provided
- If the context doesn't contain enough information, say so
- Include specific commands, code, or procedures from the context
- Cite sources using [1], [2], etc. when referencing context

Answer:"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3  # Lower temperature for factual answers
        )

        answer = response.choices[0].message.content

        return {
            'answer': answer,
            'sources': sources,
            'context': context,
            'query': query
        }


# Example usage
if __name__ == "__main__":
    # Initialize RAG system
    rag = RAGSystem(collection_name="k8s_docs")

    # Add sample documents
    documents = [
        {
            'content': """
# Kubernetes Deployment Guide

## Production Deployment

To deploy to production, follow these steps:

1. Ensure kubectl is configured:
   kubectl config use-context production

2. Apply the deployment:
   kubectl apply -f deployment.yaml -n production

3. Verify the deployment:
   kubectl get pods -n production
   kubectl rollout status deployment/my-app -n production

## Rollback Procedure

If issues occur after deployment:

1. Check recent rollout history:
   kubectl rollout history deployment/my-app -n production

2. Rollback to previous version:
   kubectl rollout undo deployment/my-app -n production

3. Verify rollback:
   kubectl get pods -n production
""",
            'metadata': {
                'source': 'k8s-deployment.md',
                'filename': 'k8s-deployment.md',
                'type': 'runbook',
                'team': 'platform'
            }
        },
        {
            'content': """
# Monitoring Setup

## Prometheus Configuration

To set up Prometheus monitoring:

1. Install Prometheus using Helm:
   helm install prometheus prometheus-community/kube-prometheus-stack

2. Access Prometheus UI:
   kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090

3. Configure alerts in prometheus-rules.yaml

## Grafana Dashboards

Import the following dashboards:
- Kubernetes cluster monitoring (ID: 315)
- Node Exporter (ID: 1860)
- Pod monitoring (ID: 6417)
""",
            'metadata': {
                'source': 'monitoring.md',
                'filename': 'monitoring.md',
                'type': 'documentation',
                'team': 'sre'
            }
        }
    ]

    # Add documents to RAG
    rag.add_documents(documents)

    print("\n" + "="*60)
    print("RAG SYSTEM READY - Example Queries")
    print("="*60)

    # Example queries
    queries = [
        "How do I deploy to production in Kubernetes?",
        "What's the rollback procedure?",
        "How do I set up Prometheus monitoring?"
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")

        # Generate RAG response
        result = rag.generate_response(query, top_k=3)

        print(f"\nAnswer:\n{result['answer']}")

        print(f"\nSources:")
        for source in result['sources']:
            print(f"  - {source['source']} (chunk {source['chunk']})")
```

**Expected Output:**

```
📚 Adding 2 documents...
  → k8s-deployment.md: 3 chunks
  → monitoring.md: 2 chunks
✓ Added 5 chunks to vector database

============================================================
RAG SYSTEM READY - Example Queries
============================================================

============================================================
Query: How do I deploy to production in Kubernetes?
============================================================

Answer:
To deploy to production in Kubernetes, follow these steps [1]:

1. Ensure kubectl is configured for production:
   kubectl config use-context production

2. Apply the deployment manifest:
   kubectl apply -f deployment.yaml -n production

3. Verify the deployment was successful:
   kubectl get pods -n production
   kubectl rollout status deployment/my-app -n production

These commands will deploy your application and allow you to verify that all pods are running correctly [1].

Sources:
  - k8s-deployment.md (chunk 0)
  - k8s-deployment.md (chunk 1)
  - monitoring.md (chunk 0)
```

### Step 5: Adding Metadata Filtering

```python
# Search with metadata filters
results = rag.search(
    query="How do I deploy?",
    top_k=5,
    filter_metadata={
        "team": {"$eq": "platform"},  # Only platform team docs
        "type": {"$eq": "runbook"}     # Only runbooks
    }
)

# Results will only include chunks matching both filters
```

### Step 6: Persistent Storage

```python
# Save ChromaDB to disk for persistence
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

# Collections are automatically persisted
# On restart, they're automatically loaded
```

---

## 6. Query Transformation Techniques

### Why Transform Queries?

**Problem:** User queries are often vague or poorly phrased

**Examples:**
- "deployment" (too vague)
- "How do I fix the thing?" (missing context)
- "k8s rollback command" (technical jargon)

**Solution:** Transform queries before retrieval to improve results

### Technique 1: Query Expansion

**Method:** Generate multiple variations of the query

```python
def expand_query(query: str, llm_client) -> List[str]:
    """
    Generate query variations using LLM.

    Returns: [original_query, variation1, variation2, ...]
    """
    prompt = f"""Given this search query, generate 3 alternative phrasings that might help find relevant documentation:

Original query: "{query}"

Generate variations that:
1. Use different terminology (e.g., "deploy" → "release", "push")
2. Add context (e.g., "production" if implied)
3. Rephrase as questions

Format: Return only the 3 variations, one per line.
"""

    response = llm_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    variations = response.choices[0].message.content.strip().split('\n')
    return [query] + [v.strip() for v in variations if v.strip()]


# Example
query = "deploy to prod"
expanded = expand_query(query, client)
# Output: [
#   "deploy to prod",
#   "release to production environment",
#   "push code to live servers",
#   "How do I deploy to the production environment?"
# ]

# Search with all variations
all_results = []
for q in expanded:
    results = rag.search(q, top_k=3)
    all_results.extend(results)

# Deduplicate and rank
unique_results = deduplicate_by_id(all_results)
```

### Technique 2: Query Decomposition

**Method:** Break complex queries into sub-queries

```python
def decompose_query(query: str, llm_client) -> List[str]:
    """
    Break complex query into simpler sub-queries.
    """
    prompt = f"""Break down this complex question into simpler sub-questions that can be answered independently:

Question: "{query}"

Return 2-4 sub-questions, one per line.
"""

    response = llm_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    sub_queries = response.choices[0].message.content.strip().split('\n')
    return [q.strip() for q in sub_queries if q.strip()]


# Example
query = "How do I deploy to production and set up monitoring with alerts?"

sub_queries = decompose_query(query, client)
# Output: [
#   "How do I deploy to production?",
#   "How do I set up monitoring?",
#   "How do I configure alerts?"
# ]

# Answer each sub-query
answers = []
for sub_query in sub_queries:
    answer = rag.generate_response(sub_query)
    answers.append(answer)

# Combine answers
final_answer = synthesize_answers(answers, original_query=query)
```

### Technique 3: Hypothetical Document Embeddings (HyDE)

**Method:** Generate a hypothetical answer, then search for it

```python
def hyde_search(query: str, rag_system, llm_client) -> List[Dict]:
    """
    HyDE: Generate hypothetical answer, embed it, search for similar docs.

    This often works better than searching for the question directly.
    """
    # Generate hypothetical answer
    prompt = f"""Generate a detailed answer to this question as if you were writing documentation:

Question: {query}

Write a clear, technical answer with specific commands and procedures.
"""

    response = llm_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    hypothetical_answer = response.choices[0].message.content

    # Search using the hypothetical answer
    # (More likely to match actual documentation style)
    results = rag_system.search(hypothetical_answer, top_k=5)

    return results


# Example
query = "How do I rollback a Kubernetes deployment?"

# Traditional search (searches for the question)
traditional_results = rag.search(query)

# HyDE search (searches for hypothetical answer)
hyde_results = hyde_search(query, rag, client)
# Often retrieves better results because the hypothetical answer
# matches the writing style of the actual documentation
```

### Technique 4: Query Rewriting with Context

```python
class ContextualRAG:
    """RAG with conversation context for follow-up questions"""

    def __init__(self, rag_system):
        self.rag = rag_system
        self.conversation_history = []

    def rewrite_query_with_context(self, query: str, llm_client) -> str:
        """Rewrite query incorporating conversation context"""
        if not self.conversation_history:
            return query

        # Build context from previous conversation
        context = "\n".join([
            f"Q: {item['query']}\nA: {item['answer'][:200]}..."
            for item in self.conversation_history[-3:]  # Last 3 exchanges
        ])

        prompt = f"""Given the conversation history, rewrite the user's latest question to be self-contained.

Conversation history:
{context}

Latest question: "{query}"

Rewritten question (self-contained):"""

        response = llm_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        rewritten = response.choices[0].message.content.strip()
        return rewritten

    def chat(self, query: str, llm_client) -> Dict:
        """Chat with context awareness"""
        # Rewrite query with context
        rewritten_query = self.rewrite_query_with_context(query, llm_client)

        print(f"Original: {query}")
        print(f"Rewritten: {rewritten_query}")

        # Generate response using rewritten query
        result = self.rag.generate_response(rewritten_query)

        # Save to history
        self.conversation_history.append({
            'query': query,
            'rewritten_query': rewritten_query,
            'answer': result['answer']
        })

        return result


# Example conversation
contextual_rag = ContextualRAG(rag)

# First question
response1 = contextual_rag.chat("How do I deploy to production?", client)
# Rewritten: "How do I deploy to production?" (no change, first question)

# Follow-up question
response2 = contextual_rag.chat("What if it fails?", client)
# Rewritten: "What should I do if a production deployment fails?"

# Another follow-up
response3 = contextual_rag.chat("How do I rollback?", client)
# Rewritten: "How do I rollback a failed Kubernetes production deployment?"
```

---

## 7. Context Window Management

### The Problem: Token Limits

**LLM Context Windows:**

| Model | Context Window | Cost (input) |
|-------|----------------|--------------|
| GPT-4 Turbo | 128K tokens (~96K words) | $0.01 / 1K tokens |
| Claude 3 Opus | 200K tokens (~150K words) | $0.015 / 1K tokens |
| Claude 3 Sonnet | 200K tokens | $0.003 / 1K tokens |

**Problem:** Retrieved context can be huge

```python
# Example: 10 chunks × 500 tokens each = 5000 tokens just for context
# + System prompt: 200 tokens
# + Question: 50 tokens
# + Response: 500 tokens
# Total: 5750 tokens per request
```

**At scale:** 1000 queries/day = 5.75M tokens = $57.50/day = $1,725/month 💸

### Solution 1: Re-Ranking

**Method:** Retrieve more docs, then re-rank to keep only the best

```python
class ReRanker:
    """Re-rank retrieved documents for relevance"""

    def __init__(self, llm_client):
        self.client = llm_client

    def rerank(
        self,
        query: str,
        documents: List[Dict],
        top_k: int = 3
    ) -> List[Dict]:
        """
        Re-rank documents by relevance to query.

        Uses LLM to score each document.
        """
        scores = []

        for doc in documents:
            # Ask LLM to score relevance
            prompt = f"""On a scale of 1-10, how relevant is this document to answering the question?

Question: {query}

Document: {doc['content'][:500]}...

Relevance score (1-10):"""

            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=10
            )

            try:
                score = int(response.choices[0].message.content.strip())
            except:
                score = 5  # Default if parsing fails

            scores.append((score, doc))

        # Sort by score (descending)
        scores.sort(reverse=True, key=lambda x: x[0])

        # Return top K
        return [doc for score, doc in scores[:top_k]]


# Usage
rag = RAGSystem()
reranker = ReRanker(client)

# Retrieve many candidates (low precision, high recall)
candidates = rag.search(query, top_k=20)

# Re-rank to top 3 (high precision)
top_docs = reranker.rerank(query, candidates, top_k=3)

# Generate response with only top 3
response = rag.generate_response_with_context(query, top_docs)
```

**Benefits:**
- ✅ Reduces tokens sent to LLM
- ✅ Improves answer quality (only best context)
- ✅ Lowers cost (fewer input tokens)

**Cost Example:**
```
Without re-ranking: 20 docs × 500 tokens = 10K tokens input
With re-ranking: 3 docs × 500 tokens = 1.5K tokens input
Savings: 85% reduction in input tokens
```

### Solution 2: Contextual Compression

**Method:** Summarize/compress retrieved docs before sending to LLM

```python
def compress_context(documents: List[str], query: str, llm_client) -> str:
    """
    Compress multiple documents into a concise summary.

    Only includes information relevant to the query.
    """
    combined_docs = "\n\n---\n\n".join([doc[:1000] for doc in documents])

    prompt = f"""Given these document excerpts, extract only the information relevant to answering the question.

Question: {query}

Documents:
{combined_docs}

Extracted relevant information (be concise):"""

    response = llm_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500  # Limit compressed size
    )

    compressed = response.choices[0].message.content
    return compressed


# Usage
documents = [result['content'] for result in rag.search(query, top_k=10)]

# Compress 10 docs into concise summary
compressed_context = compress_context(documents, query, client)

# Generate answer using compressed context (much fewer tokens)
answer = generate_with_context(query, compressed_context)
```

### Solution 3: Smart Chunking with Parent Documents

**Method:** Store small chunks for retrieval, but return larger parent context

```python
class ParentDocumentRetriever:
    """
    Stores small chunks for precise retrieval, but returns parent context.
    """

    def __init__(self, rag_system):
        self.rag = rag_system
        self.parent_store = {}  # Store full documents

    def add_documents(self, documents: List[Dict]):
        """Add documents with parent-child relationship"""
        for doc in documents:
            doc_id = doc['metadata']['source']
            content = doc['content']

            # Store full document as parent
            self.parent_store[doc_id] = content

            # Create small chunks for retrieval (e.g., 200 tokens)
            small_chunks = self.create_small_chunks(content, chunk_size=200)

            # Add small chunks to vector DB with parent reference
            for i, chunk in enumerate(small_chunks):
                self.rag.collection.add(
                    documents=[chunk],
                    metadatas=[{
                        **doc['metadata'],
                        'parent_id': doc_id,
                        'chunk_index': i
                    }],
                    ids=[f"{doc_id}_chunk{i}"]
                )

    def retrieve_with_parents(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve chunks, but return their parent documents.

        This gives more context while maintaining retrieval precision.
        """
        # Retrieve small chunks (precise matches)
        results = self.rag.search(query, top_k=top_k)

        # Get parent documents
        parent_contexts = []
        seen_parents = set()

        for result in results:
            parent_id = result['metadata']['parent_id']

            if parent_id not in seen_parents:
                # Get full parent document
                parent_doc = self.parent_store[parent_id]
                parent_contexts.append(parent_doc)
                seen_parents.add(parent_id)

        return parent_contexts


# Usage
retriever = ParentDocumentRetriever(rag)

# Add documents (stores both small chunks and full parents)
retriever.add_documents(documents)

# Retrieve: Uses small chunks for precision, returns full parents for context
contexts = retriever.retrieve_with_parents("How do I deploy?", top_k=3)

# Generate answer with full document context
answer = generate_with_context(query, contexts)
```

### Solution 4: Adaptive Context Length

**Method:** Adjust context length based on query complexity

```python
def adaptive_context_retrieval(query: str, rag_system) -> List[Dict]:
    """
    Retrieve different amounts of context based on query complexity.
    """
    # Estimate query complexity
    complexity = estimate_complexity(query)

    if complexity == "simple":
        # Simple question, need less context
        top_k = 2
    elif complexity == "moderate":
        # Moderate question, standard context
        top_k = 5
    else:  # complex
        # Complex question, more context
        top_k = 10

    results = rag_system.search(query, top_k=top_k)
    return results


def estimate_complexity(query: str) -> str:
    """Estimate query complexity"""
    # Simple heuristics
    if any(word in query.lower() for word in ['command', 'what is', 'how to']):
        return "simple"
    elif any(word in query.lower() for word in ['why', 'explain', 'difference']):
        return "moderate"
    else:
        return "complex"


# Usage
results = adaptive_context_retrieval("What's the deploy command?", rag)
# Returns 2 chunks (simple query)

results = adaptive_context_retrieval(
    "Explain the difference between blue-green and canary deployments",
    rag
)
# Returns 10 chunks (complex query)
```

---

## 8. Real-World DevOps RAG Scenarios

### Scenario 1: Incident Runbook Retrieval

**Use Case:** On-call engineer receives alert, needs quick access to runbook

**Implementation:**

```python
"""
incident_assistant.py - RAG-powered incident response assistant
"""

class IncidentAssistant:
    """AI assistant for incident response with runbook retrieval"""

    def __init__(self, rag_system, llm_client):
        self.rag = rag_system
        self.client = llm_client

    def handle_alert(self, alert: Dict) -> Dict:
        """
        Process alert and retrieve relevant runbook.

        Args:
            alert: Dict with 'service', 'metric', 'value', 'threshold'

        Returns:
            Dict with 'runbook', 'commands', 'escalation'
        """
        # Build query from alert
        query = f"""
Alert: {alert['metric']} for {alert['service']}
Current value: {alert['value']}
Threshold: {alert['threshold']}

What is the runbook for handling this alert?
"""

        # Retrieve relevant runbook
        results = self.rag.search(
            query,
            top_k=3,
            filter_metadata={"type": {"$eq": "runbook"}}
        )

        # Generate step-by-step response
        context = "\n\n".join([r['content'] for r in results])

        prompt = f"""You are an incident response assistant. Based on the runbook, provide:

1. Immediate actions to take
2. Diagnostic commands to run
3. Resolution steps
4. When to escalate

Alert details:
{alert}

Runbook context:
{context}

Response (be specific with commands):"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2  # Low temperature for consistency
        )

        return {
            'runbook': response.choices[0].message.content,
            'sources': [r['metadata']['source'] for r in results],
            'alert': alert
        }


# Example usage
assistant = IncidentAssistant(rag, client)

# Simulate PagerDuty alert
alert = {
    'service': 'api-gateway',
    'metric': 'cpu_usage_percent',
    'value': 95.3,
    'threshold': 80.0,
    'severity': 'critical'
}

# Get runbook
response = assistant.handle_alert(alert)

print("INCIDENT RUNBOOK")
print("="*60)
print(response['runbook'])
print("\nSources:")
for source in response['sources']:
    print(f"  - {source}")
```

**Output Example:**

```
INCIDENT RUNBOOK
============================================================
1. Immediate Actions:
   - Acknowledge the alert in PagerDuty
   - Check if this is a known issue: tail -f /var/log/api-gateway/app.log

2. Diagnostic Commands:
   # Check current CPU usage
   kubectl top pods -n production | grep api-gateway

   # Check for memory leaks
   kubectl exec -it api-gateway-xxx -- top -b -n 1

   # Review recent deployments
   kubectl rollout history deployment/api-gateway -n production

3. Resolution Steps:
   If CPU spike is due to traffic:
   - Scale up: kubectl scale deployment/api-gateway --replicas=10

   If CPU spike is due to memory leak:
   - Rollback: kubectl rollout undo deployment/api-gateway

4. Escalate If:
   - CPU remains >90% after scaling
   - Service becomes unresponsive
   - Multiple services affected

Sources:
  - runbooks/api-gateway-high-cpu.md
  - runbooks/kubernetes-scaling.md
```

### Scenario 2: Infrastructure Documentation Search

**Use Case:** Engineer needs to find Terraform module documentation

```python
"""
infra_docs_search.py - Search infrastructure documentation
"""

class InfraDocsSearch:
    """Search infrastructure-as-code documentation"""

    def __init__(self, rag_system):
        self.rag = rag_system

    def search_terraform_modules(self, query: str) -> List[Dict]:
        """Search Terraform module documentation"""
        results = self.rag.search(
            query,
            top_k=5,
            filter_metadata={
                "type": {"$eq": "terraform"},
                "category": {"$in": ["module", "example"]}
            }
        )

        # Format with code blocks highlighted
        formatted = []
        for result in results:
            formatted.append({
                'module': result['metadata'].get('module_name'),
                'content': result['content'],
                'file': result['metadata']['source'],
                'has_example': 'example' in result['content'].lower()
            })

        return formatted

    def find_similar_modules(self, module_description: str) -> List[Dict]:
        """Find modules similar to a description"""
        return self.search_terraform_modules(module_description)


# Example usage
docs_search = InfraDocsSearch(rag)

# Search query
results = docs_search.search_terraform_modules(
    "How do I create an ECS cluster with autoscaling?"
)

for result in results:
    print(f"\nModule: {result['module']}")
    print(f"File: {result['file']}")
    print(f"Has example: {result['has_example']}")
    print(f"\n{result['content'][:300]}...")
```

### Scenario 3: Log Analysis with Semantic Search

**Use Case:** Search logs semantically instead of grep

```python
"""
log_search.py - Semantic log search with RAG
"""

import json
from datetime import datetime

class LogSearchRAG:
    """Semantic search over application logs"""

    def __init__(self, rag_system):
        self.rag = rag_system

    def index_logs(self, log_file: str):
        """Index log file for semantic search"""
        with open(log_file, 'r') as f:
            logs = f.readlines()

        # Parse and chunk logs
        log_chunks = []
        current_chunk = []
        current_size = 0

        for log in logs:
            try:
                log_entry = json.loads(log)

                # Create searchable text
                searchable = f"""
Timestamp: {log_entry.get('timestamp')}
Level: {log_entry.get('level')}
Message: {log_entry.get('message')}
Service: {log_entry.get('service')}
"""

                current_chunk.append(searchable)
                current_size += len(searchable)

                # Chunk every ~10 log entries
                if current_size > 2000:
                    self.rag.add_documents([{
                        'content': '\n'.join(current_chunk),
                        'metadata': {
                            'type': 'logs',
                            'source': log_file,
                            'timestamp': log_entry.get('timestamp')
                        }
                    }])
                    current_chunk = []
                    current_size = 0

            except json.JSONDecodeError:
                continue

        # Add remaining chunk
        if current_chunk:
            self.rag.add_documents([{
                'content': '\n'.join(current_chunk),
                'metadata': {'type': 'logs', 'source': log_file}
            }])

    def search_errors(self, description: str) -> List[Dict]:
        """Search for errors matching description"""
        query = f"Find log entries about: {description}"

        results = self.rag.search(
            query,
            top_k=10,
            filter_metadata={"type": {"$eq": "logs"}}
        )

        return results


# Example usage
log_search = LogSearchRAG(rag)

# Index logs
log_search.index_logs("/var/log/app/production.log")

# Semantic search
results = log_search.search_errors(
    "database connection failures or timeouts"
)

print("MATCHING LOG ENTRIES:")
for result in results:
    print(f"\n{result['content']}")
```

**Why This Is Better Than Grep:**

```bash
# Traditional grep (misses variations)
grep "database" production.log | grep "error"
# Misses: "DB timeout", "connection refused", "can't connect to postgres"

# Semantic search (finds all variations)
# Understands: "database" = "DB" = "postgres" = "mysql"
# Understands: "connection failure" = "timeout" = "refused" = "can't connect"
```

### Scenario 4: Onboarding New Engineers

**Use Case:** New engineer asks questions, gets instant answers from knowledge base

```python
"""
onboarding_assistant.py - AI assistant for new engineer onboarding
"""

class OnboardingAssistant:
    """Help new engineers with common questions"""

    def __init__(self, rag_system, llm_client):
        self.rag = rag_system
        self.client = llm_client
        self.common_topics = [
            "deployment",
            "monitoring",
            "incident response",
            "architecture",
            "tools and access"
        ]

    def answer_question(self, question: str) -> Dict:
        """Answer onboarding question with docs + friendly explanation"""
        # Retrieve relevant docs
        results = self.rag.search(question, top_k=5)

        context = "\n\n".join([r['content'] for r in results])

        # Generate friendly, beginner-friendly answer
        prompt = f"""You are a helpful senior engineer onboarding a new team member.

New engineer's question: {question}

Documentation context:
{context}

Provide a clear, friendly answer that:
1. Explains the concept simply
2. Includes specific commands or procedures
3. Mentions relevant tools
4. Suggests next steps or related topics to learn

Answer:"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return {
            'answer': response.choices[0].message.content,
            'related_docs': [r['metadata']['source'] for r in results],
            'suggested_topics': self.suggest_related_topics(question)
        }

    def suggest_related_topics(self, question: str) -> List[str]:
        """Suggest related topics to explore"""
        # Simple keyword matching (could be enhanced with embeddings)
        suggestions = []
        for topic in self.common_topics:
            if topic in question.lower():
                suggestions.append(topic)

        return suggestions or ["Getting Started Guide"]


# Example usage
assistant = OnboardingAssistant(rag, client)

# New engineer questions
questions = [
    "How do I get access to production?",
    "What's the deployment process?",
    "Where are the logs stored?",
    "How do I run tests locally?"
]

for question in questions:
    print(f"\nQ: {question}")
    response = assistant.answer_question(question)
    print(f"A: {response['answer'][:200]}...")
    print(f"Related: {', '.join(response['suggested_topics'])}")
```

---

## Summary

In this chapter, you learned RAG fundamentals:

### Key Concepts

| Concept | Purpose | Key Takeaway |
|---------|---------|-------------|
| **Vector Embeddings** | Convert text to numbers | Enable semantic search (meaning-based) |
| **Vector Databases** | Store and search embeddings | Fast similarity search at scale |
| **Chunking** | Split documents | Balance context and precision |
| **Query Transformation** | Improve retrieval | Expand, decompose, or rewrite queries |
| **Context Management** | Handle token limits | Re-rank, compress, or adapt context |

### Production Checklist

✅ **Setup:**
- [ ] Choose vector database (ChromaDB for dev, Pinecone/Weaviate for prod)
- [ ] Select embedding model (text-embedding-3-small recommended)
- [ ] Design chunking strategy (500 tokens, 50 overlap is good default)

✅ **Implementation:**
- [ ] Add metadata to chunks (source, date, type)
- [ ] Implement query transformation (at least query expansion)
- [ ] Add re-ranking to reduce costs
- [ ] Set up persistent storage

✅ **Optimization:**
- [ ] Test chunk sizes for your use case
- [ ] Monitor retrieval quality
- [ ] Track costs (embedding + LLM tokens)
- [ ] Cache frequent queries

### DevOps-Specific Benefits

**Time Savings:**
- Manual doc search: 15-30 minutes
- RAG search: 10-30 seconds
- **95% faster** incident response

**Cost Savings:**
- Reduced on-call burden
- Faster onboarding (days → hours)
- Less context switching

**Quality Improvements:**
- Always up-to-date (syncs with live docs)
- Consistent answers (no tribal knowledge)
- Traceable (citations to source docs)

### Next Steps

In Chapter 23, you'll learn:
- **Hybrid search** (semantic + keyword)
- **Re-ranking techniques** (Cohere, cross-encoders)
- **Agentic RAG** (agents that use tools)
- **RAG evaluation** (measuring quality)
- **Production optimization** (caching, cost reduction)
- **Advanced patterns** (multi-query, fusion, routing)

---

**Chapter 22 Complete!** You now have a solid foundation in RAG. Ready to build advanced RAG systems in Chapter 23! ✅

---

## Navigation

← Previous: [Chapter 21: Resilient Agentic Systems](./21-resilient-agentic-systems.md) | Next: [Chapter 23: Advanced RAG Patterns](./23-advanced-rag-patterns.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

## Navigation

← Previous: [Chapter 21: Building Resilient Agentic Systems](./21-resilient-agentic-systems.md) | Next: [Chapter 23: Advanced RAG Patterns](./23-advanced-rag-patterns.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 22** | RAG Fundamentals | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
