# Chapter 22: RAG Fundamentals - Code Examples

This directory contains production-ready implementations of RAG (Retrieval-Augmented Generation) patterns for DevOps use cases.

## Overview

**Chapter 22** teaches RAG fundamentals: vector embeddings, vector databases, chunking strategies, and building your first RAG system.

### What's Included

| File | Purpose |
|------|---------|
| `document_loader.py` | Load documents from various formats (MD, TXT, JSON) |
| `chunker.py` | 4 chunking strategies (fixed-size, sentence, semantic, markdown) |
| `basic_rag_system.py` | Complete RAG implementation with ChromaDB |
| `vector_databases.py` | Examples for ChromaDB, FAISS, Pinecone, Weaviate |
| `query_transformation.py` | Query expansion, decomposition, HyDE |
| `context_management.py` | Re-ranking, compression, parent documents |
| `examples/incident_runbooks.py` | Real-world incident response RAG |
| `examples/infrastructure_docs.py` | Infrastructure documentation search |
| `examples/log_analysis.py` | Semantic log analysis |
| `examples/onboarding_assistant.py` | New engineer onboarding Q&A |

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- (Optional) Cohere API key for re-ranking

### Setup

```bash
# Navigate to chapter directory
cd src/chapter-22

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys
export OPENAI_API_KEY="your-openai-key"
export COHERE_API_KEY="your-cohere-key"  # Optional
```

## Quick Start

### 1. Basic RAG System

```python
from basic_rag_system import RAGSystem

# Initialize
rag = RAGSystem(collection_name="my_docs")

# Load documents
documents = [
    {
        'content': "Kubernetes is a container orchestration platform...",
        'metadata': {'source': 'k8s-intro.md', 'type': 'documentation'}
    }
]
rag.add_documents(documents)

# Query
result = rag.generate_answer("What is Kubernetes?")
print(result['answer'])
```

### 2. Different Chunking Strategies

```python
from chunker import (
    FixedSizeChunker,
    SentenceChunker,
    SemanticChunker,
    MarkdownChunker
)

# Fixed-size chunking
chunker = FixedSizeChunker(chunk_size=500, overlap=50)
chunks = chunker.chunk_text(long_document)

# Semantic chunking
semantic_chunker = SemanticChunker()
chunks = semantic_chunker.chunk_text(long_document)
```

### 3. Query Transformation

```python
from query_transformation import QueryTransformer

transformer = QueryTransformer()

# Query expansion
variations = transformer.expand_query("How to configure HPA?")
# → ["Configure horizontal pod autoscaler", "Set up pod autoscaling", ...]

# HyDE (Hypothetical Document Embeddings)
hypothetical_doc = transformer.hyde_query("What causes pod crashes?")
# → Generate hypothetical answer, use it for search
```

### 4. Real-World Example: Incident Runbooks

```python
from examples.incident_runbooks import IncidentAssistant

assistant = IncidentAssistant()

# Load runbooks
assistant.load_runbooks('./runbooks')

# Handle alert
alert = {
    'service': 'api-gateway',
    'metric': 'error_rate',
    'value': 15.3,
    'threshold': 5.0
}

response = assistant.handle_alert(alert)
print(response['runbook'])
print(response['immediate_actions'])
```

## Running Examples

### Basic RAG Demo

```bash
python basic_rag_system.py
```

**Expected output:**
- Loads sample Kubernetes docs
- Performs 3 queries
- Shows retrieved documents and generated answers

### Chunking Comparison

```bash
python chunker.py
```

**Expected output:**
- Chunks sample document with 4 different strategies
- Compares chunk counts and quality
- Shows pros/cons of each approach

### Query Transformation Demo

```bash
python query_transformation.py
```

**Expected output:**
- Demonstrates query expansion
- Shows HyDE (hypothetical document generation)
- Compares retrieval results

### Context Management Demo

```bash
python context_management.py
```

**Expected output:**
- Demonstrates re-ranking
- Shows contextual compression
- Compares token usage before/after compression

## Directory Structure

```
chapter-22/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── document_loader.py             # Document loading utilities
├── chunker.py                     # Chunking strategies
├── basic_rag_system.py            # Complete RAG implementation
├── vector_databases.py            # Vector DB examples
├── query_transformation.py        # Query transformation
├── context_management.py          # Context management
├── examples/                      # Real-world examples
│   ├── incident_runbooks.py      # Incident response
│   ├── infrastructure_docs.py    # Infrastructure search
│   ├── log_analysis.py           # Log analysis
│   └── onboarding_assistant.py   # Onboarding Q&A
├── data/                          # Sample data
│   ├── sample_docs/              # Sample documentation
│   ├── runbooks/                 # Sample runbooks
│   └── logs/                     # Sample logs
└── tests/                         # Unit tests
    └── test_rag_system.py
```

## Key Concepts

### Vector Embeddings

Convert text to numerical vectors that capture semantic meaning:

```python
text = "Kubernetes pod scaling"
embedding = get_embedding(text)
# → [0.123, -0.456, 0.789, ...] (1536 dimensions)
```

**Similarity**:
```python
similarity = cosine_similarity(embedding1, embedding2)
# → 0.92 (high similarity)
```

### Chunking Strategies

| Strategy | Best For | Chunk Size |
|----------|----------|------------|
| **Fixed-size** | General text | 500-1000 tokens |
| **Sentence** | Natural boundaries | Variable |
| **Semantic** | Topic coherence | Variable |
| **Markdown** | Structured docs | By section |

### Query Transformation

**Query Expansion**: Generate variations
```
"Fix pod crashes" → ["Troubleshoot CrashLoopBackOff", "Resolve pod failures", ...]
```

**HyDE**: Generate hypothetical answer, search with it
```
Query: "What causes pod crashes?"
→ Generate: "Pods crash due to OOMKilled, probe failures..."
→ Search using this text (often more effective)
```

### Context Management

**Problem**: Retrieved docs exceed LLM context window (8K-128K tokens)

**Solutions**:
1. **Re-ranking**: Retrieve 50, keep best 5
2. **Compression**: Summarize retrieved docs
3. **Parent documents**: Small chunks for search, large for context

## Production Considerations

### Vector Database Selection

| Use Case | Recommended DB |
|----------|---------------|
| **Development/prototyping** | ChromaDB (local) |
| **Production (managed)** | Pinecone |
| **Production (self-hosted)** | Weaviate |
| **Research/offline** | FAISS |

### Chunking Best Practices

- **Chunk size**: 500-1000 tokens (balance between context and precision)
- **Overlap**: 10-20% (50-100 tokens)
- **Metadata**: Always include source, date, type
- **Hierarchy**: Use parent-child relationships for complex docs

### Cost Optimization

**Typical costs per query:**
```
Embedding:    $0.0001  (query + 5 docs)
Retrieval:    $0.0010  (vector search)
Generation:   $0.0200  (GPT-4 Turbo with context)
─────────────────────────────
Total:        $0.0211 per query
```

**For 100K queries/month**: $2,110/month

**Optimization strategies**:
- Use smaller embedding models (text-embedding-3-small)
- Cache frequent queries (see Chapter 23)
- Compress context before generation
- Use GPT-3.5 Turbo for simpler queries

### Monitoring Metrics

Track these metrics in production:

```python
{
    'queries_per_day': 3421,
    'avg_latency_ms': 1847,
    'p95_latency_ms': 3201,
    'avg_docs_retrieved': 4.8,
    'avg_context_tokens': 3840,
    'cost_per_query': 0.0198,
    'embedding_cache_hit_rate': 0.23,
}
```

## Troubleshooting

### ChromaDB Issues

**Problem**: `RuntimeError: No available collections`

**Solution**:
```python
# Ensure collection is created before querying
collection = client.get_or_create_collection(name="docs")
```

**Problem**: `Dimensionality mismatch`

**Solution**: Ensure same embedding model for indexing and querying

### Poor Retrieval Quality

**Symptoms**: Irrelevant documents returned

**Solutions**:
1. Try different chunking strategies (semantic vs fixed-size)
2. Adjust chunk size (smaller = more precise, larger = more context)
3. Add metadata filtering (type='runbook', severity='critical')
4. Increase top_k and add re-ranking

### High Latency

**Symptoms**: Queries taking >3 seconds

**Solutions**:
1. Use FAISS or Pinecone instead of ChromaDB for production
2. Reduce top_k (retrieve fewer documents)
3. Use smaller embedding model (3-small vs 3-large)
4. Implement caching (see Chapter 23)

### High Costs

**Symptoms**: RAG system costing >$5K/month

**Solutions**:
1. Cache frequent queries (70% cost reduction typical)
2. Use GPT-3.5 Turbo instead of GPT-4 for simple queries
3. Compress context before generation
4. Implement smart routing (skip retrieval when not needed)

## Learn More

- **Chapter 22**: RAG Fundamentals (this chapter)
- **Chapter 23**: Advanced RAG Patterns (hybrid search, re-ranking, caching)
- **OpenAI Embeddings Guide**: https://platform.openai.com/docs/guides/embeddings
- **ChromaDB Docs**: https://docs.trychroma.com/
- **Vector DB Comparison**: https://vdbs.superlinked.com/

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Support

For questions or issues:
1. Review the chapter content in `chapters/22-rag-fundamentals.md`
2. Check the code comments in each implementation file
3. Run the example scripts to see expected outputs

---

**Chapter 22 Code** | RAG Fundamentals | © 2026 Michel Abboud
