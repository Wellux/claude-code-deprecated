---
name: embeddings
description: >
  Design and implement text embedding pipelines for semantic search and similarity.
  Invoke for: "embeddings", "semantic search", "vector similarity", "embed this text",
  "find similar", "clustering", "text similarity", "nearest neighbor search".
argument-hint: text data to embed or similarity task to implement
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Embeddings — Semantic Vector Representations
**Category:** AI/ML Research

## Role
Build embedding pipelines for semantic search, clustering, and similarity — stored in `data/embeddings/`.

## When to invoke
- Semantic search over documents
- Finding similar code / prompts / outputs
- Clustering similar items
- "find things similar to X"

## Instructions
1. Choose embedding model: claude-3 embeddings / text-embedding-3-small / local model
2. Preprocessing: chunk text appropriately (512-2048 tokens), clean, normalize
3. Embed: batch process for efficiency, handle rate limits
4. Index: store in FAISS (fast local) or ChromaDB (persistent)
5. Query: embed query, cosine similarity search, return top-k results
6. Store in `data/embeddings/` with metadata for reproducibility

## Output format
```python
# Embedding pipeline
def embed_documents(docs: list[str]) -> np.ndarray: ...
def semantic_search(query: str, k: int = 5) -> list[dict]: ...
# Returns: [{"text": ..., "score": 0.95, "metadata": {...}}]
```

## Example
/embeddings build semantic search over data/research/ — find similar research notes
