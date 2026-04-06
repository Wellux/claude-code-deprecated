---
name: rag-builder
description: >
  Build Retrieval-Augmented Generation (RAG) systems including LightRAG graph-based retrieval.
  Invoke for: "build RAG", "add retrieval", "vector search", "semantic search",
  "RAG system", "document retrieval", "knowledge base search", "LightRAG",
  "graph-based retrieval", "reduce hallucination with retrieval".
argument-hint: documents to index or RAG system to design
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch
---

# Skill: RAG Builder — Retrieval-Augmented Generation
**Category:** AI/ML Research

## Role
Design and implement RAG systems that ground LLM responses in actual data, reducing hallucination.

## When to invoke
- "my LLM is hallucinating — add retrieval"
- Building knowledge base Q&A
- Document search and retrieval
- LightRAG graph-based retrieval setup

## Instructions
1. Choose RAG approach: naive, advanced, or graph-based (LightRAG)
2. Document processing: chunk → embed → index
3. Retrieval: semantic similarity, keyword hybrid, or graph traversal
4. Prompt augmentation: inject retrieved context into LLM prompt
5. Implement with: chromadb / faiss / LightRAG for indexing
6. Store embeddings in `data/embeddings/`
7. Test: retrieval precision, response groundedness

## Output format
Complete implementation including:
- Document ingestion pipeline
- Vector store setup
- Query pipeline
- Evaluation metrics

## Example
/rag-builder build RAG for data/research/ docs — enable semantic search over all research notes
