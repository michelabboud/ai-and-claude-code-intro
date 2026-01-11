"""
Document Chunking Strategies for RAG Systems.

Implements 4 chunking strategies:
1. Fixed-size chunking (simple, predictable)
2. Sentence-based chunking (preserves boundaries)
3. Semantic chunking (respects topics)
4. Markdown structure-aware chunking (by headers)
"""

import re
from typing import List, Dict
import tiktoken
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


class FixedSizeChunker:
    """
    Fixed-size chunking with overlap.

    Simple and predictable: chunks of N tokens with M overlap.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        encoding_name: str = "cl100k_base"
    ):
        """
        Args:
            chunk_size: Tokens per chunk
            chunk_overlap: Overlap tokens between chunks
            encoding_name: tiktoken encoding (cl100k_base for GPT-4/3.5)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Chunk text into fixed-size chunks.

        Args:
            text: Text to chunk
            metadata: Optional metadata to include in each chunk

        Returns:
            List of chunk dicts with content and metadata
        """
        # Tokenize text
        tokens = self.encoding.encode(text)

        chunks = []
        start = 0

        while start < len(tokens):
            # Get chunk tokens
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]

            # Decode back to text
            chunk_text = self.encoding.decode(chunk_tokens)

            # Create chunk dict
            chunk = {
                'content': chunk_text,
                'metadata': {
                    **(metadata or {}),
                    'chunk_index': len(chunks),
                    'start_token': start,
                    'end_token': end,
                    'token_count': len(chunk_tokens)
                }
            }

            chunks.append(chunk)

            # Move to next chunk with overlap
            start += self.chunk_size - self.chunk_overlap

        return chunks


class SentenceChunker:
    """
    Sentence-based chunking.

    Preserves sentence boundaries for natural text flow.
    """

    def __init__(
        self,
        target_chunk_size: int = 500,
        encoding_name: str = "cl100k_base"
    ):
        """
        Args:
            target_chunk_size: Target tokens per chunk (actual may vary)
            encoding_name: tiktoken encoding
        """
        self.target_chunk_size = target_chunk_size
        self.encoding = tiktoken.get_encoding(encoding_name)

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Chunk text by sentences, grouping to target size.

        Args:
            text: Text to chunk
            metadata: Optional metadata

        Returns:
            List of chunk dicts
        """
        # Split into sentences
        sentences = nltk.sent_tokenize(text)

        chunks = []
        current_chunk = []
        current_token_count = 0

        for sentence in sentences:
            sentence_tokens = len(self.encoding.encode(sentence))

            # If adding this sentence exceeds target, save current chunk
            if current_token_count + sentence_tokens > self.target_chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'content': chunk_text,
                    'metadata': {
                        **(metadata or {}),
                        'chunk_index': len(chunks),
                        'token_count': current_token_count,
                        'sentence_count': len(current_chunk)
                    }
                })

                # Start new chunk
                current_chunk = [sentence]
                current_token_count = sentence_tokens
            else:
                # Add sentence to current chunk
                current_chunk.append(sentence)
                current_token_count += sentence_tokens

        # Add final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'content': chunk_text,
                'metadata': {
                    **(metadata or {}),
                    'chunk_index': len(chunks),
                    'token_count': current_token_count,
                    'sentence_count': len(current_chunk)
                }
            })

        return chunks


class SemanticChunker:
    """
    Semantic chunking using sentence embeddings.

    Groups sentences by semantic similarity to preserve topic coherence.
    """

    def __init__(
        self,
        target_chunk_size: int = 500,
        similarity_threshold: float = 0.7,
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Args:
            target_chunk_size: Target tokens per chunk
            similarity_threshold: Cosine similarity threshold for grouping
            embedding_model: Sentence transformer model
        """
        self.target_chunk_size = target_chunk_size
        self.similarity_threshold = similarity_threshold
        self.encoding = tiktoken.get_encoding("cl100k_base")

        # Load sentence transformer for embeddings
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(embedding_model)

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Chunk text by semantic similarity.

        Strategy:
        1. Split into sentences
        2. Embed each sentence
        3. Group sentences with high similarity
        4. Respect target chunk size

        Args:
            text: Text to chunk
            metadata: Optional metadata

        Returns:
            List of chunk dicts
        """
        # Split into sentences
        sentences = nltk.sent_tokenize(text)

        if len(sentences) <= 1:
            return [{
                'content': text,
                'metadata': {**(metadata or {}), 'chunk_index': 0}
            }]

        # Embed sentences
        embeddings = self.model.encode(sentences)

        # Group sentences by similarity
        chunks = []
        current_chunk = [sentences[0]]
        current_embedding = embeddings[0]
        current_token_count = len(self.encoding.encode(sentences[0]))

        for i in range(1, len(sentences)):
            sentence = sentences[i]
            embedding = embeddings[i]
            sentence_tokens = len(self.encoding.encode(sentence))

            # Calculate similarity with current chunk
            similarity = cosine_similarity(
                [current_embedding],
                [embedding]
            )[0][0]

            # Decide whether to add to current chunk or start new one
            if (similarity >= self.similarity_threshold and
                current_token_count + sentence_tokens <= self.target_chunk_size):
                # Add to current chunk
                current_chunk.append(sentence)
                current_token_count += sentence_tokens

                # Update chunk embedding (average)
                current_embedding = np.mean(embeddings[i-len(current_chunk)+1:i+1], axis=0)
            else:
                # Save current chunk and start new one
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'content': chunk_text,
                    'metadata': {
                        **(metadata or {}),
                        'chunk_index': len(chunks),
                        'token_count': current_token_count,
                        'sentence_count': len(current_chunk)
                    }
                })

                # Start new chunk
                current_chunk = [sentence]
                current_embedding = embedding
                current_token_count = sentence_tokens

        # Add final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'content': chunk_text,
                'metadata': {
                    **(metadata or {}),
                    'chunk_index': len(chunks),
                    'token_count': current_token_count,
                    'sentence_count': len(current_chunk)
                }
            })

        return chunks


class MarkdownChunker:
    """
    Markdown structure-aware chunking.

    Splits by headers to preserve document structure.
    """

    def __init__(
        self,
        max_chunk_size: int = 1000,
        encoding_name: str = "cl100k_base"
    ):
        """
        Args:
            max_chunk_size: Maximum tokens per chunk
            encoding_name: tiktoken encoding
        """
        self.max_chunk_size = max_chunk_size
        self.encoding = tiktoken.get_encoding(encoding_name)

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Chunk markdown by headers.

        Strategy:
        1. Split by headers (## and ###)
        2. Keep section structure intact
        3. Split large sections if they exceed max_chunk_size

        Args:
            text: Markdown text
            metadata: Optional metadata

        Returns:
            List of chunk dicts
        """
        # Split by headers while keeping headers
        sections = re.split(r'(^#{1,6}\s+.+$)', text, flags=re.MULTILINE)

        chunks = []
        current_header = None
        current_content = []

        for part in sections:
            part = part.strip()
            if not part:
                continue

            # Check if this is a header
            if re.match(r'^#{1,6}\s+', part):
                # Save previous section if exists
                if current_content:
                    self._save_section(
                        header=current_header,
                        content='\n\n'.join(current_content),
                        chunks=chunks,
                        metadata=metadata
                    )
                    current_content = []

                # Start new section
                current_header = part
            else:
                # Add content to current section
                current_content.append(part)

        # Save final section
        if current_content:
            self._save_section(
                header=current_header,
                content='\n\n'.join(current_content),
                chunks=chunks,
                metadata=metadata
            )

        return chunks

    def _save_section(
        self,
        header: str,
        content: str,
        chunks: List[Dict],
        metadata: Dict
    ):
        """Save a section as chunk(s), splitting if too large."""
        full_text = f"{header}\n\n{content}" if header else content
        token_count = len(self.encoding.encode(full_text))

        if token_count <= self.max_chunk_size:
            # Section fits in one chunk
            chunks.append({
                'content': full_text,
                'metadata': {
                    **(metadata or {}),
                    'chunk_index': len(chunks),
                    'header': header,
                    'token_count': token_count
                }
            })
        else:
            # Section too large - split by paragraphs
            paragraphs = content.split('\n\n')
            current_chunk_parts = [header] if header else []
            current_tokens = len(self.encoding.encode(header)) if header else 0

            for para in paragraphs:
                para_tokens = len(self.encoding.encode(para))

                if current_tokens + para_tokens > self.max_chunk_size and current_chunk_parts:
                    # Save current chunk
                    chunk_text = '\n\n'.join(current_chunk_parts)
                    chunks.append({
                        'content': chunk_text,
                        'metadata': {
                            **(metadata or {}),
                            'chunk_index': len(chunks),
                            'header': header,
                            'token_count': current_tokens
                        }
                    })

                    # Start new chunk
                    current_chunk_parts = [header, para] if header else [para]
                    current_tokens = len(self.encoding.encode('\n\n'.join(current_chunk_parts)))
                else:
                    current_chunk_parts.append(para)
                    current_tokens += para_tokens

            # Save final chunk
            if current_chunk_parts:
                chunk_text = '\n\n'.join(current_chunk_parts)
                chunks.append({
                    'content': chunk_text,
                    'metadata': {
                        **(metadata or {}),
                        'chunk_index': len(chunks),
                        'header': header,
                        'token_count': len(self.encoding.encode(chunk_text))
                    }
                })


# Example usage and comparison
if __name__ == "__main__":
    # Sample document
    sample_text = """# Kubernetes Pod Lifecycle

Kubernetes pods go through several states during their lifecycle. Understanding these states is crucial for debugging and maintaining applications.

## Pod Phases

Pods have five possible phases: Pending, Running, Succeeded, Failed, and Unknown. Each phase represents a different stage in the pod's lifecycle.

### Pending Phase

A pod is in Pending state when it has been accepted by the cluster, but containers haven't been created yet. This usually happens when:
- Container images are being pulled
- The pod is waiting for scheduling
- Required resources aren't available yet

### Running Phase

The Running phase indicates that the pod has been bound to a node, and all containers have been created. At least one container is running, or is in the process of starting or restarting.

## Container States

Within a pod, containers can be in three states: Waiting, Running, or Terminated.

### Waiting State

A container in Waiting state is still running its startup operations. Common reasons include:
- Pulling the container image
- Applying Secret or ConfigMap data
- Resolving DNS

### Running State

The Running state indicates that the container is executing without issues. If the container has a postStart hook, it runs before the container enters Running state.

## Conclusion

Understanding pod and container states helps DevOps engineers troubleshoot issues quickly and maintain healthy Kubernetes clusters.
"""

    print("="*80)
    print("Chunking Strategy Comparison")
    print("="*80)

    # Strategy 1: Fixed-size
    print("\n1. Fixed-Size Chunking (500 tokens, 50 overlap)")
    print("-" * 80)
    fixed_chunker = FixedSizeChunker(chunk_size=500, chunk_overlap=50)
    fixed_chunks = fixed_chunker.chunk_text(sample_text)
    print(f"   Chunks: {len(fixed_chunks)}")
    for i, chunk in enumerate(fixed_chunks):
        print(f"   Chunk {i+1}: {chunk['metadata']['token_count']} tokens")
        print(f"            Preview: {chunk['content'][:80]}...")

    # Strategy 2: Sentence-based
    print("\n2. Sentence-Based Chunking")
    print("-" * 80)
    sentence_chunker = SentenceChunker(target_chunk_size=500)
    sentence_chunks = sentence_chunker.chunk_text(sample_text)
    print(f"   Chunks: {len(sentence_chunks)}")
    for i, chunk in enumerate(sentence_chunks):
        print(f"   Chunk {i+1}: {chunk['metadata']['token_count']} tokens, "
              f"{chunk['metadata']['sentence_count']} sentences")
        print(f"            Preview: {chunk['content'][:80]}...")

    # Strategy 3: Semantic (commented out - requires sentence-transformers)
    print("\n3. Semantic Chunking")
    print("-" * 80)
    print("   (Requires sentence-transformers model - see code for implementation)")

    # Strategy 4: Markdown structure-aware
    print("\n4. Markdown Structure-Aware Chunking")
    print("-" * 80)
    markdown_chunker = MarkdownChunker(max_chunk_size=800)
    markdown_chunks = markdown_chunker.chunk_text(sample_text)
    print(f"   Chunks: {len(markdown_chunks)}")
    for i, chunk in enumerate(markdown_chunks):
        header = chunk['metadata'].get('header', 'No header')
        print(f"   Chunk {i+1}: {chunk['metadata']['token_count']} tokens")
        print(f"            Header: {header}")
        print(f"            Preview: {chunk['content'][:80]}...")

    # Summary comparison
    print("\n" + "="*80)
    print("Summary Comparison")
    print("="*80)
    print(f"Fixed-size:   {len(fixed_chunks)} chunks (predictable, may split sentences)")
    print(f"Sentence:     {len(sentence_chunks)} chunks (natural boundaries)")
    print(f"Markdown:     {len(markdown_chunks)} chunks (preserves structure)")
    print("\nRecommendation:")
    print("  - Fixed-size: General text, when token count is critical")
    print("  - Sentence: Natural language, when readability matters")
    print("  - Semantic: Topic coherence, when context is important")
    print("  - Markdown: Structured docs, when hierarchy matters")
