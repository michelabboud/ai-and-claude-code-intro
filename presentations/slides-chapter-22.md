---
marp: true
theme: default
paginate: true
---

# Chapter 22: RAG Fundamentals
## Retrieval-Augmented Generation for DevOps

**AI and Claude Code: A Comprehensive Guide for DevOps Engineers**

Michel Abboud
© 2026

---

## What You'll Learn

- **RAG Concept**: Why LLMs need external knowledge
- **Vector Embeddings**: Converting text to semantic vectors
- **Vector Databases**: Storing and searching embeddings
- **Chunking Strategies**: 4 approaches for splitting documents
- **Building RAG Systems**: Complete implementation
- **Query Transformation**: Improving retrieval quality
- **Context Management**: Handling token limits
- **Real-World Examples**: DevOps use cases

---

## The Problem: LLMs Don't Know Your Data

```
User: "What's the runbook for service-api high CPU?"

LLM: "I don't have access to your specific runbooks..."
```

**LLMs know**:
- General knowledge (trained on internet)
- Common patterns and best practices

**LLMs don't know**:
- Your company's runbooks
- Your infrastructure documentation
- Your internal procedures
- Recent incidents and resolutions

---

## The Solution: Retrieval-Augmented Generation (RAG)

```
┌─────────────────────────────────────────────┐
│          User Question                      │
│  "What's the runbook for high CPU?"         │
└──────────────┬──────────────────────────────┘
               │
               ▼
     ┌─────────────────┐
     │   1. Retrieve   │  ← Search knowledge base
     │   Relevant Docs │     for related runbooks
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │   2. Generate   │  ← LLM creates answer
     │   with Context  │     using retrieved docs
     └────────┬────────┘
              │
              ▼
    "1. Check which pods...
     2. Review metrics...
     3. Scale if needed..."
```

---

## RAG Benefits

**Accuracy**:
- Answers grounded in your actual documentation
- No hallucinations (if docs are wrong, answer reflects that)
- Citable sources for every answer

**Cost**:
- No fine-tuning required ($10K-100K+ savings)
- Update knowledge base without retraining

**Flexibility**:
- Add new docs instantly
- Works with any LLM
- Scale knowledge base independently

---

## Real-World Impact: PagerDuty

**Before RAG**:
- Engineers manually searched runbooks (5-10 min)
- Mean Time To Resolution (MTTR): 47 minutes

**After RAG**:
- Instant runbook retrieval (<1 second)
- MTTR reduced to 7 minutes

**Result**: **85% reduction in MTTR** = $2.4M annual savings

---

## Vector Embeddings: The Foundation

Convert text to numerical vectors that capture meaning:

```python
text = "Kubernetes pod is crashing"
embedding = get_embedding(text)
# → [0.123, -0.456, 0.789, ..., 0.234]  (1536 numbers)
```

**Why vectors?**
- Computers understand numbers, not text
- Similar meaning = similar vectors
- Enable semantic search (meaning-based, not keyword)

---

## Semantic vs Keyword Search

**Keyword Search** (traditional):
```
Query: "pod crash"
Finds: documents containing exact words "pod" and "crash"
Misses: "container failure", "CrashLoopBackOff", "OOMKilled"
```

**Semantic Search** (vector-based):
```
Query: "pod crash"
Finds: all related concepts:
  - "CrashLoopBackOff in Kubernetes"
  - "container keeps restarting"
  - "OOMKilled memory limit"
```

**Semantic search understands meaning, not just words.**

---

## Embedding Models

Popular embedding models:

| Model | Dimensions | Cost | Best For |
|-------|------------|------|----------|
| **OpenAI text-embedding-3-small** | 1536 | $0.02/1M tokens | General, cost-effective |
| **OpenAI text-embedding-3-large** | 3072 | $0.13/1M tokens | Highest accuracy |
| **Voyage AI voyage-2** | 1024 | $0.10/1M tokens | Enterprise |
| **Open-source e5-mistral-7b** | 4096 | Free | Self-hosted |

**Recommendation**: Start with `text-embedding-3-small` (best value)

---

## Similarity Metrics

**Cosine Similarity** (most common):
```
similarity = cos(θ) between vector1 and vector2
Range: -1 to 1 (1 = identical, 0 = unrelated, -1 = opposite)
```

**Example**:
```python
query_embedding = [0.8, 0.3, 0.5]
doc1_embedding = [0.7, 0.4, 0.5]  # Similar
doc2_embedding = [-0.2, 0.9, -0.3]  # Different

cosine_similarity(query, doc1) = 0.92  ← High similarity!
cosine_similarity(query, doc2) = 0.18  ← Low similarity
```

---

## Vector Databases

Store and search embeddings efficiently:

| Database | Type | Best For | Cost |
|----------|------|----------|------|
| **ChromaDB** | Local | Development | Free |
| **FAISS** | Local | Research | Free |
| **Pinecone** | Cloud | Production | $70/mo+ |
| **Weaviate** | Self-hosted | Enterprise | Free (DIY) |

**Start with ChromaDB** for prototyping, **Pinecone** for production.

---

## ChromaDB Example

```python
import chromadb
from openai import OpenAI

# Initialize
client = chromadb.Client()
collection = client.create_collection("devops_docs")

# Add documents
documents = ["Pod scaling with HPA...", "Incident response..."]
embeddings = [get_embedding(doc) for doc in documents]
collection.add(documents=documents, embeddings=embeddings, ids=["1", "2"])

# Search
query = "How do I scale pods?"
query_embedding = get_embedding(query)
results = collection.query(query_embeddings=[query_embedding], n_results=3)

print(results['documents'])
# → ["Pod scaling with HPA...", ...]
```

---

## Document Chunking: Why?

**Problem**: Documents are too long for embedding models

```
Your documentation: 50,000 tokens
Embedding model limit: 8,192 tokens
```

**Solution**: Split documents into chunks

**Benefits**:
- More precise retrieval (small chunks = specific matches)
- Fit within context windows
- Better relevance scoring

---

## Chunking Strategy 1: Fixed-Size

Split by token count with overlap:

```python
from chunker import FixedSizeChunker

chunker = FixedSizeChunker(chunk_size=500, overlap=50)
chunks = chunker.chunk_text(long_document)

# Result:
# Chunk 1: tokens 0-500
# Chunk 2: tokens 450-950  (50 token overlap)
# Chunk 3: tokens 900-1400
```

**Pros**: Simple, predictable, fast
**Cons**: May split sentences mid-way

---

## Chunking Strategy 2: Sentence-Based

Split by sentences, group to target size:

```python
from chunker import SentenceChunker

chunker = SentenceChunker(target_chunk_size=500)
chunks = chunker.chunk_text(document)

# Result:
# Chunk 1: Sentences 1-5 (487 tokens)
# Chunk 2: Sentences 6-9 (512 tokens)
```

**Pros**: Natural boundaries, readable
**Cons**: Variable chunk sizes

---

## Chunking Strategy 3: Semantic

Group sentences by topic similarity:

```python
from chunker import SemanticChunker

chunker = SemanticChunker(similarity_threshold=0.7)
chunks = chunker.chunk_text(document)

# Uses sentence embeddings to group related sentences
```

**Pros**: Topic coherence, contextually related
**Cons**: Slower (requires embeddings), more complex

---

## Chunking Strategy 4: Markdown Structure-Aware

Split by headers, preserve hierarchy:

```python
from chunker import MarkdownChunker

chunker = MarkdownChunker(max_chunk_size=1000)
chunks = chunker.chunk_text(markdown_doc)

# Result:
# Chunk 1: ## Introduction + content
# Chunk 2: ### Setup + content
# Chunk 3: ### Configuration + content
```

**Pros**: Preserves document structure, semantic sections
**Cons**: Only works with structured docs

---

## Chunking Best Practices

**Chunk size**: 500-1000 tokens
- Too small: Loses context
- Too large: Less precise

**Overlap**: 10-20% (50-100 tokens)
- Ensures continuity across chunks
- Prevents splitting important info

**Metadata**: Always include
```python
{
    'content': '...',
    'metadata': {
        'source': 'runbook-cpu.md',
        'type': 'runbook',
        'date': '2026-01-10'
    }
}
```

---

## Building Your First RAG System

Complete implementation:

```python
from basic_rag_system import RAGSystem

# 1. Initialize
rag = RAGSystem(collection_name="devops_knowledge")

# 2. Load documents
documents = load_markdown_files('./docs')
rag.add_documents(documents)

# 3. Query
result = rag.generate_answer("How do I scale pods with HPA?")

print(result['answer'])
print(result['sources'])
```

---

## RAG System Architecture

```
┌────────────────────────────────────────────────┐
│              User Query                        │
└──────────────┬─────────────────────────────────┘
               │
               ▼
     ┌──────────────────┐
     │ 1. Embed Query   │  OpenAI Embeddings API
     └────────┬─────────┘   ($0.0001)
              │
              ▼
     ┌──────────────────┐
     │ 2. Vector Search │  ChromaDB / Pinecone
     │    (Find top 5)  │  (local or $0.001)
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────┐
     │ 3. LLM Generate  │  GPT-4 Turbo
     │  (with context)  │  ($0.02)
     └────────┬─────────┘
              │
              ▼
          Answer + Sources
```

**Total cost per query**: ~$0.02

---

## Query Transformation: Query Expansion

**Problem**: User query might miss relevant docs

Query: "Fix pod issues"
Misses: "CrashLoopBackOff", "OOMKilled", "liveness probe"

**Solution**: Generate query variations

```python
from query_transformation import QueryTransformer

transformer = QueryTransformer()
variations = transformer.expand_query("Fix pod issues")

# Results:
# 1. "Troubleshoot Kubernetes pod failures"
# 2. "Resolve CrashLoopBackOff errors"
# 3. "Debug pod crash loops"
# 4. "Handle pod OOMKilled issues"

# Search with all variations for better recall
```

---

## Query Transformation: HyDE

**HyDE** (Hypothetical Document Embeddings)

**Strategy**:
1. Generate hypothetical answer to question
2. Embed the answer (not the question)
3. Search for similar documents

```python
query = "What causes pod crashes?"

# Generate hypothetical answer
hypothetical = llm.generate(
    "Write a detailed answer about pod crashes"
)
# → "Pods crash due to OOMKilled, probe failures..."

# Search using this text (often more effective!)
results = vector_search(hypothetical)
```

**Why it works**: Answer text is more similar to documentation than questions are.

---

## Context Window Management

**Problem**: Retrieved docs exceed LLM context

```
Retrieved: 10 documents × 800 tokens = 8,000 tokens
LLM context limit: 128,000 tokens (OK)
But generation cost: tokens × $0.01/1K = $0.08 per query!
```

**Solution**: Re-ranking - Retrieve many, keep best

```python
# Retrieve 50 candidates
candidates = vector_search(query, top_k=50)

# Re-rank to top 5
from context_management import ReRanker
reranker = ReRanker()
final_docs = reranker.rerank(query, candidates, top_k=5)

# Use only top 5 for generation (saves 85% tokens!)
```

---

## Real-World Example: Incident Runbooks

```python
from examples.incident_runbooks import IncidentAssistant

assistant = IncidentAssistant()
assistant.load_runbooks('./runbooks')

# Alert comes in
alert = {
    'service': 'api-gateway',
    'metric': 'error_rate',
    'value': 15.3,
    'threshold': 5.0
}

# Get runbook
response = assistant.handle_alert(alert)

print(response['immediate_actions'])
# 1. Check error logs: kubectl logs api-gateway-xxx
# 2. Review recent deployments
# 3. Check downstream service health
```

---

## Real-World Example: Infrastructure Docs

```python
from examples.infrastructure_docs import InfrastructureRAG

infra_rag = InfrastructureRAG()
infra_rag.load_terraform_modules('./terraform')

# Developer question
result = infra_rag.search("How do I create an S3 bucket with versioning?")

print(result['answer'])
# Use the s3_bucket module:
#
# module "my_bucket" {
#   source = "./modules/s3_bucket"
#   versioning = true
# }

print(result['source_file'])
# → ./terraform/modules/s3_bucket/README.md
```

---

## Real-World Example: Log Analysis

**Traditional approach**:
```bash
grep "error" logs.txt  # Keyword search
```

**RAG approach**:
```python
from examples.log_analysis import SemanticLogSearch

log_search = SemanticLogSearch()
log_search.index_logs('./logs', days=7)

# Semantic search
results = log_search.find("database connection issues")

# Finds:
# - "timeout connecting to postgres"
# - "connection pool exhausted"
# - "too many open connections"
```

**Finds related errors, not just exact keywords!**

---

## Real-World Example: Onboarding Assistant

```python
from examples.onboarding_assistant import OnboardingRAG

assistant = OnboardingRAG()
assistant.load_documentation('./onboarding-docs')

# New engineer questions
questions = [
    "How do I get AWS access?",
    "What's the deployment process?",
    "How do I create a new service?"
]

for question in questions:
    answer = assistant.answer(question)
    print(f"Q: {question}")
    print(f"A: {answer['answer']}\n")
```

Reduces onboarding time from **2 weeks to 3 days** (documented case at Shopify).

---

## RAG System Cost Breakdown

**For 10,000 queries/month**:

```
Component               Cost/Query      Monthly Total
─────────────────────────────────────────────────────
Query embedding         $0.0001         $1.00
Document embeddings     $0.0001         $1.00  (amortized)
Vector search           $0.0010         $10.00
LLM generation          $0.0200         $200.00
─────────────────────────────────────────────────────
TOTAL PER QUERY:        $0.0211
TOTAL MONTHLY:                          $211.00
```

**For 100K queries/month**: ~$2,110
**For 1M queries/month**: ~$21,100

*Optimization strategies in Chapter 23 (caching can reduce by 70%!)*

---

## Production Considerations

**Monitoring**:
- Track query latency (target: <2 seconds)
- Monitor embedding costs
- Measure retrieval relevance
- Log failed queries

**Error Handling**:
- Graceful degradation (if vector DB down, fall back to keyword search)
- Retry logic for API failures
- Rate limiting to prevent abuse

**Security**:
- Validate user permissions (only search authorized docs)
- Sanitize inputs (prevent injection attacks)
- Audit logs (who searched what, when)

---

## Common Issues and Solutions

**Problem**: Retrieved docs aren't relevant
**Solution**: Try different chunking strategy (semantic vs fixed-size)

**Problem**: High latency (>3 seconds)
**Solution**: Use Pinecone/FAISS instead of ChromaDB for production

**Problem**: High costs
**Solution**: Implement caching (Chapter 23), use smaller embedding models

**Problem**: Answers lack citations
**Solution**: Always return source metadata, format answers with `[Source: ...]`

---

## Key Takeaways

1. **RAG gives LLMs access to your knowledge** without fine-tuning
2. **Vector embeddings enable semantic search** (meaning, not keywords)
3. **Chunking strategy matters** (fixed-size for general, semantic for topics, markdown for structure)
4. **Query transformation improves retrieval** (expansion, HyDE)
5. **Context management controls costs** (re-ranking, compression)
6. **Real-world impact**: 85% MTTR reduction, $2.4M annual savings (PagerDuty)

---

## Next Steps

**Hands-on**:
1. Run `basic_rag_system.py` to build your first RAG
2. Experiment with different chunking strategies
3. Try query transformation techniques

**Production**:
- Implement monitoring and error handling
- Set up vector database (Pinecone for production)
- Add caching (Chapter 23)
- Evaluate with RAGAS metrics (Chapter 23)

**Chapter 23**: Advanced RAG patterns (hybrid search, re-ranking, caching, evaluation)

---

## Resources

**Code Examples**:
- `src/chapter-22/` - Complete implementations
- `src/chapter-22/examples/` - Real-world use cases

**Documentation**:
- OpenAI Embeddings: platform.openai.com/docs/guides/embeddings
- ChromaDB: docs.trychroma.com
- Vector DB Comparison: vdbs.superlinked.com

**Papers**:
- RAG Original Paper (Lewis et al., 2020)
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"

---

# Questions?

**Contact**: See repository README
**Code**: github.com/michelabboud/ai-and-claude-code-intro

**Next Chapter**: Advanced RAG Patterns
(Hybrid search, re-ranking, caching, evaluation, agentic RAG)

---

# Thank You!

© 2026 Michel Abboud
CC BY-NC 4.0 License
