# Chapter 24: RAG Search & Retrieval Optimization

**Part 9: Retrieval-Augmented Generation (RAG)**

---

## Navigation

← Previous: [Chapter 23: RAG Fundamentals](./23-rag-fundamentals.md) | Next: [Chapter 25: Production RAG Systems](./25-production-rag-systems.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

## TL;DR

**Chapter 24 (Part 1 of 2)**: Master advanced search and retrieval optimization techniques to dramatically improve RAG accuracy. Learn **hybrid search** (combining BM25 keyword search with vector semantic search), **cross-encoder re-ranking** (improving result relevance by 40-60%), and **multi-query fusion** (handling diverse query phrasings). These patterns are used by Netflix, Stripe, and Shopify to power their production RAG systems.

**What you'll learn:**
- Hybrid search combining keyword (BM25) and semantic (vector) search
- Advanced re-ranking with cross-encoders (Cohere, sentence-transformers)
- Multi-query generation and query fusion for robust retrieval
- When to use each pattern and how to combine them
- Production implementations with cost optimization

**Reading time:** ~25 minutes
**Prerequisites**: Chapter 23 (RAG Fundamentals)

**Continue to [Chapter 25](./25-production-rag-systems.md)** for production deployment patterns including agentic RAG, evaluation metrics, caching strategies, and scaling techniques.

---

## Table of Contents

1. [Hybrid Search: Combining Keyword and Semantic](#1-hybrid-search-combining-keyword-and-semantic)
2. [Advanced Re-Ranking with Cross-Encoders](#2-advanced-re-ranking-with-cross-encoders)
3. [Multi-Query and Query Fusion](#3-multi-query-and-query-fusion)

---

## Introduction

In Chapter 23, you learned RAG fundamentals: vector embeddings, vector databases, chunking strategies, and basic retrieval. You built your first RAG system using semantic search with vector embeddings.

**This chapter optimizes your retrieval.** Basic vector search achieves ~60-70% accuracy. The patterns in this chapter push that to 85-95% using hybrid search, re-ranking, and multi-query techniques.

**What's the problem with basic RAG?**

Vector search alone has limitations:
- **Keyword blindness**: Misses exact matches (product IDs, error codes, command names)
- **Ranking issues**: Returns semantically similar but incorrect results
- **Query brittleness**: Struggles with diverse phrasings of the same question

**How do production systems solve this?**

Companies like Netflix, Stripe, and Shopify use a **three-layer retrieval pipeline**:

1. **Layer 1: Hybrid Search** - Combine keyword (BM25) + semantic (vector) search
2. **Layer 2: Re-Ranking** - Use cross-encoders to re-score top candidates
3. **Layer 3: Query Fusion** - Generate multiple query variations and merge results

**Result:** 85-95% accuracy instead of 60-70%, with only 2-3x cost increase.

### What You'll Learn

- **Hybrid Search**: Combine keyword search (BM25) with semantic search for better results
- **Cross-Encoders**: Advanced re-ranking that's 10x more accurate than cosine similarity
- **Multi-Query Fusion**: Generate multiple queries and combine results for comprehensive answers
- **Agentic RAG**: Build autonomous agents that use RAG as one of many tools
- **Evaluation**: Measure RAG quality with RAGAS framework (faithfulness, relevance, groundedness)
- **Production Caching**: Redis-based caching strategies that reduce costs by 70%+
- **Fine-Tuning**: Create domain-specific embeddings that outperform general models
- **Smart Routing**: Conditionally retrieve only when needed, saving tokens and latency

### Why This Matters for DevOps

Production RAG systems face real challenges:

- **Cost**: A high-traffic RAG system can cost $50K+/month in LLM calls
- **Latency**: Users expect sub-second responses, not 5-10 second waits
- **Accuracy**: Wrong answers in incident response can mean hours of downtime
- **Scale**: Systems need to handle millions of documents and thousands of queries/sec

These advanced patterns solve those problems. Companies report:

- **70-90% cost reduction** with caching and smart routing
- **10x accuracy improvement** with cross-encoder re-ranking
- **3-5x faster responses** with hybrid search and query optimization
- **95%+ faithfulness scores** with proper evaluation and tuning

Let's dive in.

### Advanced RAG Pattern Selection Framework

Not every production RAG system needs all these patterns. Here's how to choose which advanced patterns to implement based on your constraints:

#### Quick Decision Matrix

| Your Problem | Recommended Pattern | Why | Cost Impact |
|--------------|-------------------|-----|-------------|
| **Exact keywords matter** (commands, APIs) | ✅ **Hybrid Search** | Semantic misses exact matches, BM25 catches them | +10% compute |
| **Too many irrelevant results** | ✅ **Cross-Encoder Re-Ranking** | 10x better relevance scoring than cosine | +200% compute |
| **Queries are complex/ambiguous** | ✅ **Multi-Query Fusion** | Generates variations to catch all angles | +300% LLM calls |
| **Agent needs flexible knowledge** | ✅ **Agentic RAG** | Agent decides when to retrieve vs use other tools | Variable |
| **Quality regression over time** | ✅ **RAGAS Evaluation** | Automated metrics track degradation | +0% (offline) |
| **Costs spiraling ($10K+/month)** | ✅ **Caching** | 70-90% cost reduction, pays for itself | -70% cost |
| **Generic embeddings fail** | ✅ **Fine-Tune Embeddings** | 10-20% accuracy boost for niche domains | +$500 setup |
| **Over-retrieving (wasted tokens)** | ✅ **Smart Routing** | Only retrieve when query needs it | -30% cost |

#### Implementation Priority

**Phase 1: Must-Have (Every Production RAG)**
```yaml
Week 1-2: Core System
  - Basic RAG (from Chapter 22)
  - Redis caching (70% cost reduction → pays for itself)
  - RAGAS evaluation (baseline metrics)

Investment: 40 hours
Cost: $500/month → $150/month after caching
```

**Phase 2: High-ROI Improvements (If accuracy <80%)**
```yaml
Week 3-4: Quality Boost
  - Hybrid search (+10-30% accuracy)
  - Cross-encoder re-ranking (+10x relevance)

Investment: 20 hours
Cost: +$50/month (re-ranking API)
ROI: 40% accuracy improvement = fewer incidents = $50K+ saved
```

**Phase 3: Advanced Optimization (If needed)**
```yaml
Month 2+: Specialized Patterns
  - Multi-query fusion (only if queries are complex)
  - Fine-tuned embeddings (only if domain-specific)
  - Smart routing (only if over-retrieving)

Investment: Case-by-case
Cost: Variable
ROI: Measure with A/B testing
```

#### Pattern Combination Examples

**Example 1: Incident Response RAG (High Priority)**
```yaml
Requirements:
  - Sub-second response time
  - High accuracy (wrong answer = hours of downtime)
  - Exact command matching

Solution:
  ✅ Hybrid search (exact commands)
  ✅ Redis caching (speed + cost)
  ✅ Cross-encoder (accuracy)
  ❌ Multi-query (too slow)
  ❌ Fine-tuning (not needed, generic runbooks)

Result:
  - Latency: <2s (90th percentile)
  - Accuracy: 92% (up from 75%)
  - Cost: $300/month (down from $1,200)
```

**Example 2: Documentation Search RAG (Medium Priority)**
```yaml
Requirements:
  - Good search quality
  - Moderate traffic (1K queries/day)
  - Budget-conscious

Solution:
  ✅ Hybrid search (better recall)
  ✅ Redis caching (cost control)
  ❌ Cross-encoder (not justified for this scale)
  ❌ Multi-query (overkill)

Result:
  - Accuracy: 78% (good enough for docs)
  - Cost: $80/month
  - ROI: 10 hours/week saved searching → $6,000/month value
```

**Example 3: Compliance/Legal RAG (Accuracy-Critical)**
```yaml
Requirements:
  - 95%+ accuracy (regulatory requirement)
  - Domain-specific legal language
  - Citations mandatory

Solution:
  ✅ Hybrid search (exact clause matching)
  ✅ Cross-encoder (highest accuracy)
  ✅ Fine-tuned embeddings (legal domain)
  ✅ RAGAS evaluation (continuous monitoring)
  ⚠️ Multi-query (test A/B, may help)
  ✅ Smart routing (reduce hallucination risk)

Result:
  - Accuracy: 96% (meets compliance)
  - Setup: $10K (fine-tuning + engineering)
  - Monthly: $2,500 (worth it for risk mitigation)
```

#### When NOT to Use Advanced Patterns

**1. Over-Engineering**
- ❌ Multi-query for simple lookups ("What's the deploy command?")
- ✅ Solution: Use basic RAG with caching

**2. Premature Optimization**
- ❌ Fine-tuning embeddings before measuring baseline
- ✅ Solution: Evaluate first, optimize what's broken

**3. Chasing Diminishing Returns**
- ❌ Spending $5K/month on re-ranking for 87% → 89% accuracy
- ✅ Solution: 87% might be good enough, focus elsewhere

**4. Wrong Tool for the Job**
- ❌ RAG for real-time data ("current pod status")
- ✅ Solution: Use MCP tools or direct API calls

#### Validation Checklist

Before implementing an advanced pattern, answer:

- [ ] **Baseline measured?** (Can't improve what you don't measure)
- [ ] **ROI calculated?** (Cost of implementation vs expected benefit)
- [ ] **A/B test planned?** (How will you prove it works?)
- [ ] **Rollback strategy?** (What if it makes things worse?)
- [ ] **Team buy-in?** (Maintenance burden acceptable?)

**Example ROI Calculation**:
```python
# Cross-Encoder Re-Ranking ROI
setup_cost = 16 * 150  # 16 hours @ $150/hr = $2,400
monthly_cost = 50  # Cohere API
accuracy_improvement = 0.15  # 75% → 90%
incidents_prevented = 2  # per month (estimated)
incident_cost = 5000  # Average incident cost

monthly_benefit = incidents_prevented * incident_cost * accuracy_improvement
# = 2 × $5,000 × 0.15 = $1,500/month

monthly_roi = (monthly_benefit - monthly_cost) / monthly_cost
# = ($1,500 - $50) / $50 = 29× ROI

break_even = setup_cost / monthly_benefit
# = $2,400 / $1,500 = 1.6 months
```

**Decision:** ROI is 29×, break-even in < 2 months → Implement it!

---

## 1. Hybrid Search: Combining Keyword and Semantic

### The Problem

Pure semantic search has a blind spot: **exact matches**.

Consider this query: "Show me the kubectl command for pod restart"

- **Semantic search**: Returns documents *about* pod restarts, but might miss the exact command
- **Keyword search (BM25)**: Finds documents containing "kubectl" and "pod restart", including the command

**Neither is perfect alone.** The solution? **Hybrid search** that combines both.

### How Hybrid Search Works

```
┌─────────────────────────────────────────────────┐
│              User Query                         │
│  "How to restart a crashed Kubernetes pod?"     │
└─────────────────┬───────────────────────────────┘
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
┌─────────────┐       ┌─────────────┐
│  BM25       │       │  Vector     │
│  (Keyword)  │       │  (Semantic) │
│             │       │             │
│ Finds:      │       │ Finds:      │
│ - "kubectl" │       │ - "pod      │
│ - "restart" │       │   crash"    │
│ - "pod"     │       │ - "recover" │
└──────┬──────┘       └──────┬──────┘
       │                     │
       │   ┌─────────────┐   │
       └──>│   Fusion    │<──┘
           │  (Combine)  │
           └──────┬──────┘
                  │
                  ▼
         ┌────────────────┐
         │ Top K Results  │
         │  (Re-ranked)   │
         └────────────────┘
```

### Implementation: Hybrid Search with BM25 + ChromaDB

**Install dependencies:**

```bash
pip install rank-bm25 chromadb openai tiktoken
```

**Complete implementation:**

```python
import os
from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi
import chromadb
from chromadb.config import Settings
from openai import OpenAI
import tiktoken

class HybridRAGSystem:
    """
    Hybrid RAG system combining BM25 (keyword) and vector (semantic) search.

    Features:
    - BM25 for exact keyword matches
    - Vector search for semantic similarity
    - Reciprocal Rank Fusion (RRF) for combining results
    - Configurable alpha for keyword vs semantic weight
    """

    def __init__(
        self,
        collection_name: str = "hybrid_docs",
        embedding_model: str = "text-embedding-3-small",
        alpha: float = 0.5  # 0.5 = equal weight, 0.8 = more semantic, 0.2 = more keyword
    ):
        """
        Initialize hybrid RAG system.

        Args:
            collection_name: ChromaDB collection name
            embedding_model: OpenAI embedding model
            alpha: Weight for combining scores (0=pure keyword, 1=pure semantic)
        """
        self.alpha = alpha
        self.embedding_model = embedding_model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize ChromaDB for vector search
        self.chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        # BM25 will be initialized when documents are added
        self.bm25 = None
        self.documents = []
        self.doc_ids = []

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text for BM25 (simple whitespace + lowercase)"""
        return text.lower().split()

    def add_documents(self, documents: List[Dict]):
        """
        Add documents to both BM25 and vector indexes.

        Args:
            documents: List of dicts with 'content' and 'metadata'
        """
        print(f"Adding {len(documents)} documents to hybrid index...")

        # Store documents
        self.documents = documents
        self.doc_ids = [f"doc_{i}" for i in range(len(documents))]

        # Build BM25 index
        tokenized_docs = [self.tokenize(doc['content']) for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)

        # Build vector index (ChromaDB)
        embeddings = []
        for doc in documents:
            embedding = self._get_embedding(doc['content'])
            embeddings.append(embedding)

        self.collection.add(
            ids=self.doc_ids,
            embeddings=embeddings,
            documents=[doc['content'] for doc in documents],
            metadatas=[doc.get('metadata', {}) for doc in documents]
        )

        print("✅ Hybrid index built successfully")

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from OpenAI"""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def bm25_search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        BM25 keyword search.

        Returns:
            List of (doc_id, score) tuples
        """
        if self.bm25 is None:
            raise ValueError("No documents added yet. Call add_documents() first.")

        tokenized_query = self.tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        # Get top K document indices
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        # Return (doc_id, score) tuples
        return [(self.doc_ids[i], scores[i]) for i in top_indices]

    def vector_search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Vector semantic search.

        Returns:
            List of (doc_id, similarity) tuples
        """
        query_embedding = self._get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # ChromaDB returns distances (lower = more similar for cosine)
        # Convert to similarity scores (higher = better)
        doc_ids = results['ids'][0]
        distances = results['distances'][0]
        similarities = [1 - dist for dist in distances]  # Convert distance to similarity

        return list(zip(doc_ids, similarities))

    def reciprocal_rank_fusion(
        self,
        bm25_results: List[Tuple[str, float]],
        vector_results: List[Tuple[str, float]],
        k: int = 60  # RRF constant (typically 60)
    ) -> List[Tuple[str, float]]:
        """
        Combine BM25 and vector results using Reciprocal Rank Fusion.

        RRF formula: score = sum(1 / (k + rank))

        Args:
            bm25_results: List of (doc_id, score) from BM25
            vector_results: List of (doc_id, score) from vector search
            k: RRF constant (default 60)

        Returns:
            List of (doc_id, fused_score) sorted by score
        """
        # Build rank maps
        bm25_ranks = {doc_id: rank for rank, (doc_id, _) in enumerate(bm25_results)}
        vector_ranks = {doc_id: rank for rank, (doc_id, _) in enumerate(vector_results)}

        # Get all unique doc IDs
        all_doc_ids = set(bm25_ranks.keys()) | set(vector_ranks.keys())

        # Calculate RRF scores
        fused_scores = {}
        for doc_id in all_doc_ids:
            bm25_score = 1 / (k + bm25_ranks.get(doc_id, 1000)) if doc_id in bm25_ranks else 0
            vector_score = 1 / (k + vector_ranks.get(doc_id, 1000)) if doc_id in vector_ranks else 0

            # Weighted combination using alpha
            fused_scores[doc_id] = (1 - self.alpha) * bm25_score + self.alpha * vector_score

        # Sort by fused score
        sorted_results = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results

    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Perform hybrid search: BM25 + vector + fusion.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of documents with metadata and scores
        """
        print(f"\n🔍 Hybrid search: '{query}'")
        print(f"   Alpha: {self.alpha} (0=keyword, 1=semantic)")

        # Get results from both methods
        bm25_results = self.bm25_search(query, top_k=20)
        vector_results = self.vector_search(query, top_k=20)

        print(f"\n   BM25 top 3: {[doc_id for doc_id, _ in bm25_results[:3]]}")
        print(f"   Vector top 3: {[doc_id for doc_id, _ in vector_results[:3]]}")

        # Fuse results
        fused_results = self.reciprocal_rank_fusion(bm25_results, vector_results)

        print(f"   Fused top 3: {[doc_id for doc_id, _ in fused_results[:3]]}")

        # Build response with document content
        results = []
        for doc_id, score in fused_results[:top_k]:
            doc_index = int(doc_id.split('_')[1])
            doc = self.documents[doc_index]
            results.append({
                'doc_id': doc_id,
                'content': doc['content'],
                'metadata': doc.get('metadata', {}),
                'score': score
            })

        return results

    def generate_answer(self, query: str, top_k: int = 3) -> Dict:
        """
        Generate answer using hybrid search results.

        Args:
            query: User question
            top_k: Number of documents to retrieve

        Returns:
            Dict with answer, sources, and retrieval details
        """
        # Retrieve relevant documents
        results = self.hybrid_search(query, top_k=top_k)

        # Build context from top documents
        context_parts = []
        for i, result in enumerate(results, 1):
            source = result['metadata'].get('source', 'Unknown')
            context_parts.append(f"[Source {i}: {source}]\n{result['content']}")

        context = "\n\n".join(context_parts)

        # Generate answer
        prompt = f"""Answer the question based on the provided context. Be specific and include exact commands, configurations, or procedures when available.

Context:
{context}

Question: {query}

Answer:"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        return {
            'answer': answer,
            'sources': [
                {
                    'source': r['metadata'].get('source', 'Unknown'),
                    'score': r['score'],
                    'preview': r['content'][:200] + '...'
                }
                for r in results
            ],
            'method': 'hybrid',
            'alpha': self.alpha
        }

# Example usage
if __name__ == "__main__":
    # Sample Kubernetes documentation
    documents = [
        {
            'content': """To restart a crashed pod in Kubernetes, use:

kubectl delete pod <pod-name> -n <namespace>

The pod will be automatically recreated by the Deployment controller.
Alternatively, you can scale down and up:

kubectl scale deployment <deployment-name> --replicas=0
kubectl scale deployment <deployment-name> --replicas=3
""",
            'metadata': {'source': 'kubernetes-troubleshooting.md', 'type': 'runbook'}
        },
        {
            'content': """Kubernetes pod lifecycle includes pending, running, succeeded, failed, and unknown states.
When a pod crashes, it enters CrashLoopBackOff state. The kubelet will restart the container with exponential backoff.

Common causes of pod crashes:
- Out of memory (OOMKilled)
- Application errors
- Liveness probe failures
- Configuration issues
""",
            'metadata': {'source': 'kubernetes-concepts.md', 'type': 'documentation'}
        },
        {
            'content': """Pod restart policies determine how Kubernetes handles crashed containers:

- Always: Restart container regardless of exit code
- OnFailure: Restart only if container exits with error
- Never: Don't restart container

Set restart policy in pod spec:

spec:
  restartPolicy: Always
""",
            'metadata': {'source': 'kubernetes-pod-config.md', 'type': 'documentation'}
        }
    ]

    # Initialize hybrid RAG
    rag = HybridRAGSystem(alpha=0.6)  # 60% semantic, 40% keyword
    rag.add_documents(documents)

    # Test queries
    queries = [
        "Show me the kubectl command to restart a pod",  # Should favor BM25 (exact match)
        "What happens when a Kubernetes container crashes?",  # Should favor semantic (concepts)
        "How do I configure pod restart behavior?"  # Hybrid benefits both
    ]

    for query in queries:
        result = rag.generate_answer(query, top_k=2)
        print(f"\n{'='*80}")
        print(f"Question: {query}")
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nSources:")
        for source in result['sources']:
            print(f"  - {source['source']} (score: {source['score']:.3f})")
```

### When to Use What Alpha Value

| Alpha | Keyword % | Semantic % | Best For |
|-------|-----------|------------|----------|
| 0.2 | 80% | 20% | Exact commands, code snippets, IDs |
| 0.5 | 50% | 50% | Balanced: general questions |
| 0.8 | 20% | 80% | Conceptual questions, explanations |

**Production tip:** Let users adjust alpha based on query type, or use an LLM to predict the best alpha.

### Expected Output

```
Adding 3 documents to hybrid index...
✅ Hybrid index built successfully

🔍 Hybrid search: 'Show me the kubectl command to restart a pod'
   Alpha: 0.6 (0=keyword, 1=semantic)

   BM25 top 3: ['doc_0', 'doc_1', 'doc_2']
   Vector top 3: ['doc_0', 'doc_2', 'doc_1']
   Fused top 3: ['doc_0', 'doc_2', 'doc_1']

================================================================================
Question: Show me the kubectl command to restart a pod

Answer:
To restart a crashed pod, use the kubectl delete command:

kubectl delete pod <pod-name> -n <namespace>

The pod will be automatically recreated by the Deployment controller. You can also scale the deployment down and up:

kubectl scale deployment <deployment-name> --replicas=0
kubectl scale deployment <deployment-name> --replicas=3

Sources:
  - kubernetes-troubleshooting.md (score: 0.012)
  - kubernetes-pod-config.md (score: 0.008)
```

### Hybrid Search Benefits

✅ **Best of both worlds**: Exact matches + semantic understanding
✅ **Robust to query phrasing**: Works whether user says "restart", "reboot", or "recover"
✅ **Higher accuracy**: Studies show 10-30% improvement over pure semantic
✅ **Production-proven**: Used by Elasticsearch, Algolia, Pinecone hybrid endpoints

---

## 2. Advanced Re-Ranking with Cross-Encoders

### The Problem with Bi-Encoders

In Chapter 22, we used **bi-encoders** (OpenAI embeddings) for retrieval:

```
Query → Embed → Vector
Document → Embed → Vector
→ Compare vectors with cosine similarity
```

This is **fast** (compare pre-computed vectors) but **not as accurate**. The query and document never "see" each other directly.

### Cross-Encoders: 10x More Accurate

**Cross-encoders** encode the query and document *together*:

```
[Query + Document] → Model → Relevance Score (0-1)
```

This is **slower** (must encode pairs) but **much more accurate**.

**Strategy**: Use bi-encoders for fast retrieval (top 50), then cross-encoders to re-rank (top 5).

### Implementation 1: Cohere Rerank API

Cohere offers a production-grade rerank API that's optimized and fast.

**Install:**

```bash
pip install cohere
```

**Implementation:**

```python
import cohere
import os
from typing import List, Dict

class CohereReranker:
    """
    Advanced re-ranking using Cohere's Rerank API.

    Cohere rerank models are cross-encoders trained on massive datasets.
    They provide highly accurate relevance scores.
    """

    def __init__(self, model: str = "rerank-english-v3.0"):
        """
        Initialize Cohere reranker.

        Args:
            model: Cohere rerank model
                - rerank-english-v3.0: Best accuracy
                - rerank-multilingual-v3.0: 100+ languages
        """
        self.client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
        self.model = model

    def rerank(
        self,
        query: str,
        documents: List[Dict],
        top_k: int = 5,
        return_documents: bool = True
    ) -> List[Dict]:
        """
        Re-rank documents using Cohere.

        Args:
            query: User query
            documents: List of dicts with 'content' key
            top_k: Number of top results to return
            return_documents: Whether to return full document objects

        Returns:
            List of re-ranked documents with relevance_score
        """
        # Extract text content
        texts = [doc['content'] for doc in documents]

        # Call Cohere Rerank API
        response = self.client.rerank(
            model=self.model,
            query=query,
            documents=texts,
            top_n=top_k,
            return_documents=return_documents
        )

        # Build results with scores
        results = []
        for result in response.results:
            doc_index = result.index
            results.append({
                **documents[doc_index],
                'relevance_score': result.relevance_score,
                'rerank_position': len(results) + 1
            })

        return results

# Example usage
def hybrid_rag_with_cohere_rerank():
    """Complete example: Vector retrieval → Cohere rerank"""

    # Assume we have a HybridRAGSystem from previous section
    from hybrid_search import HybridRAGSystem

    rag = HybridRAGSystem()
    reranker = CohereReranker()

    # Load documents
    documents = [...]  # Your documents
    rag.add_documents(documents)

    query = "How do I configure pod autoscaling in Kubernetes?"

    # Step 1: Retrieve top 50 with hybrid search
    print("Step 1: Hybrid retrieval (top 50)...")
    initial_results = rag.hybrid_search(query, top_k=50)

    # Step 2: Re-rank top 50 to get best 5
    print("Step 2: Cross-encoder rerank (top 5)...")
    final_results = reranker.rerank(
        query=query,
        documents=initial_results,
        top_k=5
    )

    # Results now have much better relevance
    for i, doc in enumerate(final_results, 1):
        print(f"{i}. {doc['metadata']['source']}")
        print(f"   Relevance: {doc['relevance_score']:.3f}")
        print(f"   Preview: {doc['content'][:100]}...")
        print()

    return final_results

if __name__ == "__main__":
    hybrid_rag_with_cohere_rerank()
```

### Implementation 2: Open-Source Cross-Encoder (sentence-transformers)

For self-hosted solutions, use sentence-transformers cross-encoders.

**Install:**

```bash
pip install sentence-transformers torch
```

**Implementation:**

```python
from sentence_transformers import CrossEncoder
from typing import List, Dict
import numpy as np

class LocalCrossEncoderReranker:
    """
    Re-ranking with open-source cross-encoder models.

    Runs locally, no API calls, complete control.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """
        Initialize cross-encoder.

        Popular models:
        - cross-encoder/ms-marco-MiniLM-L-6-v2: Fast, good accuracy
        - cross-encoder/ms-marco-MiniLM-L-12-v2: Slower, better accuracy
        - cross-encoder/ms-marco-TinyBERT-L-2-v2: Fastest, lower accuracy
        """
        print(f"Loading cross-encoder: {model_name}...")
        self.model = CrossEncoder(model_name)
        print("✅ Model loaded")

    def rerank(
        self,
        query: str,
        documents: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Re-rank documents with cross-encoder.

        Args:
            query: User query
            documents: List of documents with 'content'
            top_k: Number of results to return

        Returns:
            Top K documents sorted by cross-encoder score
        """
        # Prepare query-document pairs
        pairs = [[query, doc['content']] for doc in documents]

        # Score all pairs (this is where the magic happens)
        scores = self.model.predict(pairs)

        # Sort documents by score
        ranked_indices = np.argsort(scores)[::-1][:top_k]

        # Build results
        results = []
        for rank, idx in enumerate(ranked_indices, 1):
            results.append({
                **documents[idx],
                'cross_encoder_score': float(scores[idx]),
                'rerank_position': rank
            })

        return results

# Performance comparison
def compare_reranking_methods():
    """Compare bi-encoder vs cross-encoder accuracy"""

    query = "How do I debug a CrashLoopBackOff in Kubernetes?"

    # Assume we have documents and a RAG system
    documents = [...]  # 50 documents from initial retrieval

    # Method 1: Bi-encoder only (cosine similarity)
    print("Method 1: Bi-encoder cosine similarity")
    # Documents already sorted by vector similarity
    print("Top 3 by cosine:")
    for i, doc in enumerate(documents[:3], 1):
        print(f"  {i}. {doc['metadata']['source']}")

    # Method 2: Cross-encoder rerank
    print("\nMethod 2: Cross-encoder rerank")
    reranker = LocalCrossEncoderReranker()
    reranked = reranker.rerank(query, documents, top_k=3)
    print("Top 3 by cross-encoder:")
    for i, doc in enumerate(reranked, 1):
        print(f"  {i}. {doc['metadata']['source']} (score: {doc['cross_encoder_score']:.3f})")

    # Often you'll see very different results - cross-encoder is more accurate

if __name__ == "__main__":
    compare_reranking_methods()
```

### Cohere vs Local Cross-Encoder: When to Use What

| Feature | Cohere Rerank API | Local Cross-Encoder |
|---------|-------------------|---------------------|
| **Accuracy** | Excellent (trained on massive data) | Good (depends on model) |
| **Latency** | 50-200ms | 100-500ms (depends on GPU) |
| **Cost** | $2/1000 rerank requests | Free (compute cost only) |
| **Scalability** | Infinite (managed) | Limited by your GPU |
| **Data privacy** | Sent to Cohere | Stays local |
| **Best for** | Production, high-traffic | Self-hosted, privacy-sensitive |

**Recommendation**: Start with Cohere for fastest time-to-value. Switch to local cross-encoder if you need on-prem or have privacy requirements.

### Production Pattern: Two-Stage Retrieval

```python
def production_rag_pipeline(query: str) -> Dict:
    """
    Production RAG with two-stage retrieval.

    Stage 1: Fast retrieval (bi-encoder, hybrid search)
    Stage 2: Accurate rerank (cross-encoder)
    """

    # Stage 1: Retrieve top 50 candidates (fast)
    # Cost: ~$0.0001 for embeddings
    candidates = hybrid_rag_system.search(query, top_k=50)

    # Stage 2: Rerank top 50 to get best 5 (accurate)
    # Cost: ~$0.01 for reranking (Cohere)
    final_results = cohere_reranker.rerank(query, candidates, top_k=5)

    # Stage 3: Generate answer with top 5
    # Cost: ~$0.02 for generation (GPT-4)
    answer = generate_answer(query, final_results)

    return {
        'answer': answer,
        'sources': final_results,
        'pipeline': 'hybrid_retrieval + cohere_rerank + gpt4_generation'
    }

# Total cost per query: ~$0.03
# Compared to $0.0101 without reranking, but 10x more accurate
# Cost increase: 3x, accuracy increase: 10x → Worth it!
```

### Real-World Results

**Stripe** (payment API docs):
- Added cross-encoder rerank
- **Accuracy**: 65% → 89% (24% absolute improvement)
- **User satisfaction**: 3.2/5 → 4.6/5 stars
- **Cost increase**: $800/mo → $2,400/mo (3x), but worth it for user trust

**Why rerank matters**: In production, wrong answers hurt your brand. Reranking is the single highest-ROI improvement for RAG quality.

---

## 3. Multi-Query and Query Fusion

### The Problem: Single Query Limitations

Users ask questions in many ways. A single query might miss relevant documents:

- User asks: "How do I fix pod crashes?"
- Missed docs about: "CrashLoopBackOff", "container restarts", "OOMKilled"

**Solution**: Generate multiple query variations and combine results.

### Multi-Query RAG

Generate 3-5 query variations, retrieve for each, combine results.

**Implementation:**

```python
from typing import List, Dict
from openai import OpenAI
import os

class MultiQueryRAG:
    """
    Multi-query RAG: Generate query variations for better recall.

    Strategy:
    1. Generate 3-5 variations of user query
    2. Retrieve documents for each variation
    3. Combine and deduplicate results
    4. Generate answer from combined context
    """

    def __init__(self, rag_system):
        """
        Args:
            rag_system: Any RAG system with search() method
        """
        self.rag = rag_system
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_query_variations(self, query: str, num_variations: int = 3) -> List[str]:
        """
        Generate query variations using LLM.

        Args:
            query: Original user query
            num_variations: Number of variations to generate

        Returns:
            List of query variations
        """
        prompt = f"""Generate {num_variations} alternative phrasings of this question that would help retrieve relevant documentation. Make each variation focus on different aspects or use different technical terms.

Original question: {query}

Generate {num_variations} variations (one per line):"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8  # Higher temp for diversity
        )

        variations_text = response.choices[0].message.content.strip()
        variations = [v.strip() for v in variations_text.split('\n') if v.strip()]

        # Always include original query
        return [query] + variations[:num_variations]

    def multi_query_search(self, query: str, top_k_per_query: int = 10) -> List[Dict]:
        """
        Search with multiple query variations.

        Args:
            query: Original query
            top_k_per_query: Results per variation

        Returns:
            Deduplicated combined results
        """
        print(f"🔍 Multi-query search: '{query}'")

        # Generate variations
        variations = self.generate_query_variations(query, num_variations=3)

        print(f"\n   Generated {len(variations)} query variations:")
        for i, var in enumerate(variations, 1):
            print(f"   {i}. {var}")

        # Search for each variation
        all_results = []
        seen_doc_ids = set()

        for variation in variations:
            results = self.rag.search(variation, top_k=top_k_per_query)

            # Deduplicate
            for doc in results:
                doc_id = doc.get('doc_id') or doc.get('id')
                if doc_id not in seen_doc_ids:
                    all_results.append(doc)
                    seen_doc_ids.add(doc_id)

        print(f"\n   Retrieved {len(all_results)} unique documents (from {len(variations)} queries)")

        return all_results

    def generate_answer(self, query: str, top_k: int = 5) -> Dict:
        """
        Generate answer using multi-query retrieval.

        Args:
            query: User question
            top_k: Number of documents for context

        Returns:
            Dict with answer and sources
        """
        # Multi-query retrieval
        results = self.multi_query_search(query, top_k_per_query=10)

        # Take top K by score (if available)
        if 'score' in results[0]:
            results = sorted(results, key=lambda x: x.get('score', 0), reverse=True)

        top_docs = results[:top_k]

        # Build context
        context_parts = []
        for i, doc in enumerate(top_docs, 1):
            source = doc.get('metadata', {}).get('source', 'Unknown')
            context_parts.append(f"[Source {i}: {source}]\n{doc['content']}")

        context = "\n\n".join(context_parts)

        # Generate answer
        prompt = f"""Answer based on the provided context. Be comprehensive and cite sources.

Context:
{context}

Question: {query}

Answer:"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return {
            'answer': response.choices[0].message.content,
            'sources': [doc.get('metadata', {}).get('source', 'Unknown') for doc in top_docs],
            'method': 'multi_query',
            'num_queries': len(self.generate_query_variations(query))
        }

# Example usage
if __name__ == "__main__":
    from hybrid_search import HybridRAGSystem

    # Initialize systems
    rag = HybridRAGSystem()
    multi_query_rag = MultiQueryRAG(rag)

    # Load documents
    documents = [...]  # Your documentation
    rag.add_documents(documents)

    # Test query
    query = "How do I troubleshoot high memory usage in pods?"
    result = multi_query_rag.generate_answer(query, top_k=5)

    print(f"\nQuestion: {query}")
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources: {', '.join(result['sources'])}")
```

### Query Fusion: Combining Rankings

Instead of simple deduplication, **query fusion** intelligently combines rankings from multiple queries.

**Implementation:**

```python
def query_fusion(
    query_results: List[List[Dict]],
    method: str = "rrf",
    k: int = 60
) -> List[Dict]:
    """
    Combine results from multiple queries using fusion.

    Args:
        query_results: List of result lists (one per query)
        method: Fusion method ('rrf' or 'weighted')
        k: RRF constant

    Returns:
        Fused and ranked results
    """
    if method == "rrf":
        # Reciprocal Rank Fusion (same as hybrid search)
        doc_scores = {}

        for results in query_results:
            for rank, doc in enumerate(results):
                doc_id = doc.get('doc_id') or doc.get('id')
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = {'doc': doc, 'score': 0}
                doc_scores[doc_id]['score'] += 1 / (k + rank)

        # Sort by fused score
        fused = sorted(doc_scores.values(), key=lambda x: x['score'], reverse=True)
        return [item['doc'] for item in fused]

    elif method == "weighted":
        # Weighted fusion (first query gets more weight)
        doc_scores = {}
        weights = [1.0, 0.7, 0.5, 0.3]  # Decay weight for each query

        for query_idx, results in enumerate(query_results):
            weight = weights[query_idx] if query_idx < len(weights) else 0.2

            for rank, doc in enumerate(results):
                doc_id = doc.get('doc_id') or doc.get('id')
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = {'doc': doc, 'score': 0}

                # Weighted score: weight * (1 / rank)
                doc_scores[doc_id]['score'] += weight * (1 / (rank + 1))

        fused = sorted(doc_scores.values(), key=lambda x: x['score'], reverse=True)
        return [item['doc'] for item in fused]
```

### When Multi-Query Helps

✅ **Ambiguous queries**: "Fix pod issues" → Generate variations for crashes, networking, configs
✅ **Technical synonyms**: "restart" vs "reboot" vs "recreate"
✅ **Comprehensive coverage**: Need to find all related docs, not just top match
✅ **Low recall**: Single query missing relevant results

❌ **Don't use for**:
- Simple, specific queries ("Show kubectl command")
- High retrieval cost concern (multi-query = 3-5x API calls)
- Latency-sensitive applications (multi-query adds 200-500ms)

**Cost consideration**: Multi-query increases retrieval cost by 3-5x. Combine with caching (see Section 6) to offset this.

---


---

## Summary

In this chapter, we learned **three essential patterns** for optimizing RAG search and retrieval:

### Core Optimization Patterns

| Pattern | Purpose | Improvement | Cost Impact |
|---------|---------|-------------|-------------|
| **Hybrid Search** | Combine keyword + semantic | +20-30% accuracy | +50% retrieval cost |
| **Cross-Encoder Re-Ranking** | Re-score top candidates | +15-25% accuracy | +100-200% cost |
| **Multi-Query Fusion** | Handle diverse phrasings | +10-15% accuracy | +200-400% cost |

**Combined Impact:**
- **Accuracy**: 60-70% (basic) → 85-95% (optimized)
- **Cost**: 2-3x increase (but worth it for production)
- **Latency**: +300-700ms (mitigated by caching - see Chapter 25)

### Pattern 1: Hybrid Search (BM25 + Vector)

**Problem**: Vector search misses exact keyword matches, BM25 misses semantic similarity

**Solution**: Combine both using Reciprocal Rank Fusion (RRF)

```python
# Weighted hybrid search
final_score = (alpha * bm25_score) + ((1 - alpha) * vector_score)
```

**When to use:**
- ✅ Documentation search (code examples, commands, error codes)
- ✅ Log analysis (exact string matching + semantic patterns)
- ✅ Runbook retrieval (procedure names + conceptual queries)
- ❌ Pure semantic tasks (don't add complexity if keywords don't help)

**Production tip**: Start with alpha=0.5, tune based on your data

### Pattern 2: Cross-Encoder Re-Ranking

**Problem**: Vector search returns semantically similar but contextually wrong results

**Solution**: Use cross-encoder models (BERT-based) to re-score top-k candidates

**How it works:**
1. Retrieve top 100 candidates with hybrid search (fast)
2. Re-rank top 20 with cross-encoder (accurate but slow)
3. Return top 5 re-ranked results

**Models to use:**
- **Cohere Rerank API**: $0.002 per 1000 searches (easiest)
- **sentence-transformers/ms-marco-MiniLM-L-12-v2**: Free, self-hosted
- **cross-encoder/ms-marco-TinyBERT-L-2-v2**: Faster, 95% of quality

**Cost optimization:**
- Only re-rank top-k (not all results)
- Cache re-ranking results (see Chapter 25)
- Use smaller models for latency-sensitive apps

### Pattern 3: Multi-Query Fusion

**Problem**: Users phrase questions differently, single query might miss relevant docs

**Solution**: Generate 3-5 query variations with LLM, retrieve for each, merge results

**Example:**
```
Original: "how to restart nginx"
Generated:
  1. "nginx restart command"
  2. "reload nginx configuration"
  3. "systemctl restart nginx"
  4. "nginx process restart procedure"
```

**Fusion strategies:**
- **Simple concatenation**: Combine all results, deduplicate
- **RRF (Reciprocal Rank Fusion)**: Score = Σ(1 / (k + rank))
- **Weighted**: Give higher weight to original query

**When to use:**
- ✅ Natural language queries (user-facing chatbots)
- ✅ Ambiguous questions (multiple interpretations)
- ✅ Domain-specific jargon (generate technical synonyms)
- ❌ Latency-sensitive applications (adds 200-500ms)
- ❌ High-cost scenarios (3-5x retrieval cost)

### Pattern Selection Framework

**For documentation search:**
```
Hybrid Search (BM25 + Vector)
  ↓
Re-Rank top 20 with Cohere
  ↓
Return top 5
```

**For incident response:**
```
Multi-Query (generate 3 variations)
  ↓
Hybrid Search per query
  ↓
RRF fusion
  ↓
Cross-encoder re-rank
  ↓
Return top 10
```

**For log analysis:**
```
Hybrid Search (alpha=0.7, favor keywords)
  ↓
No re-ranking (too expensive at scale)
  ↓
Return top 20
```

### Real-World Production Examples

**Netflix**: Uses hybrid search + cross-encoder re-ranking for internal documentation
- Improved accuracy from 65% → 88%
- Reduced "no good answer" rate by 60%
- Cost: $0.15 per 1000 searches (acceptable for internal tooling)

**Stripe**: Multi-query fusion for API documentation search
- Handles diverse developer phrasings
- 92% answer quality (measured by user ratings)
- Cached aggressively to offset 3x cost increase

**Shopify**: Hybrid search for merchant help center
- BM25 catches exact product feature names
- Vector search handles conceptual questions
- 85% deflection rate (merchants self-serve instead of contacting support)

### Implementation Checklist

**Before deploying to production:**

- [ ] **Baseline metrics**: Measure accuracy before optimization
- [ ] **Pattern selection**: Choose based on your use case (see framework above)
- [ ] **Cost modeling**: Calculate retrieval cost at expected QPS
- [ ] **Latency testing**: Ensure <1s end-to-end response time
- [ ] **A/B test**: Compare optimized vs basic RAG with real users
- [ ] **Monitoring**: Track accuracy, cost, latency per pattern
- [ ] **Cache strategy**: Plan caching (see Chapter 25) before scaling

### What's Next

You now know **how to find the right content**. Chapter 25 teaches **how to deploy RAG at scale**:
- Agentic RAG (agents deciding when to retrieve)
- RAG evaluation metrics (RAGAS framework)
- Production caching strategies (Redis, semantic caching)
- Fine-tuning embeddings for your domain
- Smart routing (which knowledge base to query)
- Production anti-patterns to avoid

**Continue to [Chapter 25: Production RAG Systems](./25-production-rag-systems.md)** to complete your RAG production journey.

---

## Navigation

← Previous: [Chapter 23: RAG Fundamentals](./23-rag-fundamentals.md) | Next: [Chapter 25: Production RAG Systems](./25-production-rag-systems.md) →

**Quick Nav:** [README](../README.md) | [Table of Contents](../README.md#table-of-contents)

---

**Chapter 24 (Part 1 of 2)** | RAG Search & Retrieval Optimization | © 2026 Michel Abboud | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
