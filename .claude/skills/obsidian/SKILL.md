---
name: obsidian
description: >
  Manage knowledge using Obsidian-style second-brain with linked atomic notes. Invoke for:
  "organize in Obsidian", "second brain", "atomic notes", "linked notes", "knowledge graph",
  "note-taking", "build a wiki", "organize my knowledge", "create linked notes".
  Inspired by kepano's Obsidian skills — knowledge management meets Claude.
argument-hint: knowledge area or notes to organize
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Skill: Obsidian — Second Brain Knowledge Management
**Category:** Ecosystem
**Inspired by:** kepano (github.com/kepano) Obsidian Skills

## Role
Build a structured, linked knowledge base using Obsidian's atomic note principles, stored in `data/research/` and accessible via semantic search.

## When to invoke
- "organize all my notes about X"
- After research sessions
- Building a topic knowledge graph
- "turn these notes into linked notes"

## Atomic Note Principles
1. **One idea per note**: split compound notes
2. **Short and dense**: < 200 lines, packed with insight
3. **Link everything**: connect related concepts with [[links]]
4. **Tags**: #topic, #status/draft, #type/concept
5. **MOC (Map of Content)**: index notes that link to all notes on a topic
6. **Progressive summarization**: bold key insights, highlight critical parts

## Instructions
1. Identify all concepts in the input material
2. Create one atomic note per concept
3. Link related notes: references to other notes
4. Create MOC for the topic
5. Add to data/research/ with consistent naming
6. Update data/research/README.md index

## Output format
```markdown
---
tags: [#ai, #rag, #concept]
related: [[embeddings]], [[vector-search]]
---
# Concept Name
**Core idea:** [one sentence]
...atomic content...
```

## Example
/obsidian organize all RAG research into linked atomic notes with MOC in data/research/
