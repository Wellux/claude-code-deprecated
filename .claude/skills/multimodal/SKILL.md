---
name: multimodal
description: >
  Design and implement multimodal AI systems combining text, images, and other modalities.
  Invoke for: "multimodal", "text and images", "vision + language", "image + text pipeline",
  "document understanding", "multimodal embeddings", "cross-modal search".
argument-hint: multimodal task or system to design
allowed-tools: Read, Write, Edit, WebSearch
---

# Skill: Multimodal — Vision + Language Systems
**Category:** AI/ML Research

## Role
Build systems that combine multiple modalities (text, images, audio) using multimodal LLMs.

## When to invoke
- Building document understanding (PDF + text)
- Image captioning or visual Q&A
- Cross-modal retrieval
- Any task combining text and images

## Instructions
1. Identify modalities: text, images, structured data, code?
2. Choose model: Claude claude-sonnet-4-6 handles text+images natively
3. Input preparation: encode images as base64 or URL references
4. Prompt design: describe image role in task context
5. Output parsing: extract structured info from multimodal response
6. Pipeline: preprocess → multimodal LLM → postprocess → store

## Output format
```python
# Multimodal request pattern
messages = [{
    "role": "user",
    "content": [
        {"type": "image", "source": {"type": "base64", ...}},
        {"type": "text", "text": "Analyze this image and extract..."}
    ]
}]
```

## Example
/multimodal build document analyzer — extract text + tables + diagrams from PDFs
