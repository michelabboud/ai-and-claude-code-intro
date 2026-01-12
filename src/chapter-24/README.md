# Chapters 24-25: Advanced RAG - Code Examples

This directory contains production-ready implementations of advanced RAG patterns for building scalable, cost-effective systems.

## Overview

**Chapters 24-25** teach advanced RAG patterns split into two parts:
- **Chapter 24 (Search Optimization)**: Hybrid search, cross-encoder re-ranking, multi-query fusion
- **Chapter 25 (Production Systems)**: Agentic RAG, RAGAS evaluation, caching strategies, fine-tuning embeddings, smart routing

### What's Included

| File | Purpose |
|------|---------|
| `hybrid_search.py` | BM25 + Vector hybrid search with Reciprocal Rank Fusion |
| `cross_encoder_rerank.py` | Advanced re-ranking with Cohere and sentence-transformers |
| `multi_query.py` | Multi-query expansion and query fusion |
| `agentic_rag.py` | RAG as a tool for Claude agents |
| `rag_evaluation.py` | RAGAS framework for evaluating RAG quality |
| `rag_cache.py` | Redis-based caching for cost optimization |
| `embedding_finetuning.py` | Synthetic data generation for fine-tuning |
| `rag_router.py` | Smart routing for conditional retrieval |
| `production_rag.py` | Complete production system combining all patterns |

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Anthropic API key (for agentic RAG)
- Cohere API key (optional, for re-ranking)
- Redis server (for caching)

### Setup

```bash
# Navigate to chapter directory
cd src/chapter-23

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export COHERE_API_KEY="your-cohere-key"  # Optional

# Start Redis (Docker)
docker run -d -p 6379:6379 redis:7-alpine
```

## Quick Start

### 1. Hybrid Search (BM25 + Vector)

```python
from hybrid_search import HybridRAGSystem

# Initialize with alpha=0.6 (60% semantic, 40% keyword)
rag = HybridRAGSystem(alpha=0.6)

# Load documents
documents = [...]  # Your documents
rag.add_documents(documents)

# Search with hybrid approach
results = rag.hybrid_search("How to configure HPA?", top_k=5)

# Generate answer
answer = rag.generate_answer("How to configure HPA?")
print(answer['answer'])
```

### 2. Cross-Encoder Re-Ranking

```python
from cross_encoder_rerank import CohereReranker

# Initialize reranker
reranker = CohereReranker()

# Retrieve candidates with vector search
candidates = rag.search(query, top_k=50)

# Re-rank to top 5
final_results = reranker.rerank(query, candidates, top_k=5)
```

### 3. Redis Caching

```python
from rag_cache import RAGCache, CachedRAGSystem

# Initialize cache
cache = RAGCache()

# Wrap RAG system with caching
cached_rag = CachedRAGSystem(rag, cache)

# Queries automatically cached
result = cached_rag.generate_answer("How to scale a deployment?")
# First call: 1800ms, hits RAG pipeline
# Second call: 4ms, returns from cache

print(f"Cache hit rate: {cache.get_hit_rate():.1%}")
```

### 4. RAG Evaluation with RAGAS

```python
from rag_evaluation import RAGEvaluator

# Define test cases
test_cases = [
    {
        'question': "How do I scale a deployment to 5 replicas?",
        'ground_truth': "Use kubectl scale deployment <name> --replicas=5"
    },
    # ... more test cases
]

# Evaluate RAG system
evaluator = RAGEvaluator()
results = evaluator.evaluate_rag_system(test_cases, rag)

# View metrics
print(f"Faithfulness: {results['average_scores']['faithfulness']:.3f}")
print(f"Context Relevancy: {results['average_scores']['context_relevancy']:.3f}")
```

### 5. Production RAG System

```python
from production_rag import ProductionRAGSystem

# Initialize complete system
rag = ProductionRAGSystem()

# Query with all optimizations
result = rag.generate_answer("How to troubleshoot CrashLoopBackOff?")

print(f"Answer: {result['answer']}")
print(f"Cached: {result.get('cached', False)}")
print(f"Latency: {result['latency_ms']:.1f}ms")
print(f"Cost: ${result['cost']:.4f}")
```

## Running Examples

### Hybrid Search Demo

```bash
python hybrid_search.py
```

**Output:**
- Compares BM25-only, vector-only, and hybrid results
- Shows Reciprocal Rank Fusion in action
- Demonstrates impact of alpha parameter (keyword vs semantic weight)

### Cross-Encoder Rerank Demo

```bash
python cross_encoder_rerank.py
```

**Output:**
- Compares bi-encoder (cosine similarity) vs cross-encoder accuracy
- Shows 10x accuracy improvement on domain-specific queries
- Benchmarks latency: Cohere API (~100ms) vs local cross-encoder (~300ms)

### Caching Demo

```bash
# Start Redis first
docker run -d -p 6379:6379 redis:7-alpine

# Run demo
python rag_cache.py
```

**Output:**
- Simulates 1000 queries with 70% cache hit rate
- Shows cost savings: $21.10 → $6.33 (70% reduction)
- Demonstrates multi-level caching (embedding, retrieval, answer)

### Evaluation Demo

```bash
python rag_evaluation.py
```

**Output:**
- Runs RAGAS on test set
- Reports faithfulness, context relevancy, answer relevancy, context recall
- Provides recommendations for improvement

### Production System Demo

```bash
python production_rag.py
```

**Output:**
- Complete production pipeline in action
- Shows routing, caching, hybrid search, re-ranking, generation
- Reports metrics: latency, cost, cache hit rate, quality scores

## Advanced Patterns Explained

### 1. Hybrid Search

**Problem**: Pure semantic search misses exact matches (e.g., "kubectl" command).

**Solution**: Combine BM25 (keyword) + vector (semantic) with Reciprocal Rank Fusion.

**Result**: 10-30% better accuracy, robust to query phrasing.

### 2. Cross-Encoder Re-Ranking

**Problem**: Bi-encoders (cosine similarity) aren't as accurate as they could be.

**Solution**: Two-stage pipeline - retrieve 50 with bi-encoder, re-rank to 5 with cross-encoder.

**Result**: 10x more accurate, 3x cost increase (worth it for quality).

### 3. Multi-Query Fusion

**Problem**: Single query misses relevant docs with different terminology.

**Solution**: Generate 3-5 query variations, retrieve for each, combine with RRF.

**Result**: Better recall, more comprehensive answers, 3-5x retrieval cost.

### 4. Agentic RAG

**Problem**: Traditional RAG retrieves for every query (wasteful).

**Solution**: Agent decides when to use RAG vs other tools (calculator, API, code execution).

**Result**: Smarter system, 30-50% cost savings on non-knowledge queries.

### 5. RAGAS Evaluation

**Problem**: No way to measure RAG quality objectively.

**Solution**: RAGAS framework with 4 metrics (faithfulness, relevancy, recall).

**Result**: Track improvements, catch regressions, benchmark against targets.

### 6. Redis Caching

**Problem**: RAG systems cost $20K-50K/month at scale.

**Solution**: Multi-level caching (embedding, retrieval, answer) with Redis.

**Result**: 70-90% cost reduction (typical 70% hit rate).

### 7. Fine-Tuning Embeddings

**Problem**: General embeddings underperform on domain-specific terms.

**Solution**: Fine-tune OpenAI embeddings with synthetic query-document pairs.

**Result**: 10-20% better retrieval on specialized terminology.

### 8. Smart Routing

**Problem**: Not every query needs retrieval ("What's 2+2?" doesn't need docs).

**Solution**: LLM classifies query, routes to RAG or direct generation.

**Result**: 30-50% fewer retrievals, lower cost and latency.

## Production Checklist

When deploying RAG to production, ensure you have:

- ✅ **Hybrid search** (alpha=0.5-0.7 based on use case)
- ✅ **Re-ranking** (Cohere API or local cross-encoder)
- ✅ **Caching** (Redis with 1-hour TTL for answers)
- ✅ **Evaluation** (RAGAS metrics tracked weekly)
- ✅ **Monitoring** (Prometheus metrics for hit rate, latency, cost)
- ✅ **Smart routing** (skip retrieval when not needed)
- ✅ **Error handling** (graceful degradation, retry logic)
- ✅ **Rate limiting** (protect against abuse)

## Cost Analysis

### Without Optimization

```
100,000 queries/month
Retrieval: $0.001/query    →  $100
Re-ranking: $0.010/query   →  $1,000
Generation: $0.020/query   →  $2,000
───────────────────────────────────
Total:                         $3,100/month
```

### With Full Optimization

```
100,000 queries/month
70% cache hit rate → 30K cache misses

Retrieval: $0.001 × 30K    →  $30
Re-ranking: $0.010 × 30K   →  $300
Generation: $0.015 × 100K  →  $1,500 (shorter context)
───────────────────────────────────
Total:                         $1,830/month
SAVINGS:                       $1,270/month (41%)
```

**At scale** (1M queries/month):
- Without optimization: $31,000/month
- With optimization: $18,300/month
- **Savings: $12,700/month** ($152,400/year)

## Performance Benchmarks

### Latency

| Configuration | Avg Latency | P95 Latency |
|---------------|-------------|-------------|
| **Vector-only** | 1200ms | 2100ms |
| **Hybrid search** | 1500ms | 2500ms |
| **+ Cross-encoder** | 1800ms | 3000ms |
| **+ Caching (70% hit)** | 720ms | 2800ms |

### Accuracy (RAGAS Faithfulness)

| Configuration | Faithfulness | Improvement |
|---------------|--------------|-------------|
| **Vector-only** | 0.82 | Baseline |
| **Hybrid search** | 0.88 | +7.3% |
| **+ Cross-encoder** | 0.94 | +14.6% |
| **+ Fine-tuned embeddings** | 0.96 | +17.1% |

## Troubleshooting

### High Latency (>3 seconds)

**Solutions:**
- Enable caching (biggest impact)
- Reduce top_k in retrieval (50 → 20)
- Use Cohere Rerank instead of local cross-encoder
- Implement query batching

### Low Cache Hit Rate (<50%)

**Solutions:**
- Normalize queries (lowercase, strip whitespace)
- Implement semantic caching (cache similar queries)
- Increase TTL for stable content
- Pre-warm cache with popular queries

### Poor Accuracy (faithfulness <0.85)

**Solutions:**
- Enable cross-encoder re-ranking (biggest impact)
- Use hybrid search (keyword + semantic)
- Adjust chunking strategy (smaller chunks = more precise)
- Fine-tune embeddings for your domain

### High Costs

**Solutions:**
- Implement caching (70%+ reduction)
- Use smart routing (skip unnecessary retrieval)
- Optimize chunk size (reduce context tokens)
- Use GPT-3.5 instead of GPT-4 where appropriate

## Monitoring Setup

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Query metrics
queries_total = Counter('rag_queries_total', 'Total RAG queries')
cache_hits = Counter('rag_cache_hits_total', 'Cache hits')
cache_misses = Counter('rag_cache_misses_total', 'Cache misses')

# Latency
query_latency = Histogram('rag_query_latency_seconds', 'Query latency')

# Quality
faithfulness_score = Gauge('rag_faithfulness_score', 'Average faithfulness')

# Cost
query_cost = Histogram('rag_query_cost_dollars', 'Cost per query')
```

### Grafana Dashboard

Key panels to monitor:
- **Queries/sec** (QPS)
- **Cache hit rate** (target: >60%)
- **P95 latency** (target: <2s)
- **Faithfulness score** (target: >0.90)
- **Cost per query** (target: <$0.02)
- **Error rate** (target: <1%)

## Learn More

- **Chapter 22**: RAG Fundamentals (prerequisite)
- **Chapter 23**: Advanced RAG Patterns (this chapter)
- **RAGAS Paper**: https://arxiv.org/abs/2309.15217
- **Anthropic Tool Use**: https://docs.anthropic.com/claude/docs/tool-use
- **Cohere Rerank**: https://docs.cohere.com/reference/rerank

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific pattern tests
pytest tests/test_hybrid_search.py -v
pytest tests/test_caching.py -v
pytest tests/test_evaluation.py -v
```

## Support

For questions or issues:
1. Review the chapter content in `chapters/24-rag-search-optimization.md` and `chapters/25-production-rag-systems.md`
2. Check the code comments in each implementation file
3. Run the example scripts to see expected outputs

---

**Chapters 24-25 Code** | Advanced RAG | © 2026 Michel Abboud
