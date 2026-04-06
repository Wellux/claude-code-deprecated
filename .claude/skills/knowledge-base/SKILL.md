---
name: knowledge-base
description: >
  Build and maintain a structured knowledge base (Obsidian-style second brain). Invoke for:
  "knowledge base", "second brain", "organize notes", "Obsidian", "note taking",
  "personal wiki", "structured notes", "knowledge management",
  "organize research into notes".
argument-hint: topic area or notes to organize
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Skill: Knowledge Base — Second Brain & Note Organization
**Category:** Documentation

## Role
Build a structured, searchable knowledge base using Obsidian-style linked notes stored in `data/` directories.

## When to invoke
- Organizing research findings
- Building a personal wiki
- "structure all my notes about X"
- After research sessions to consolidate learnings

## Instructions
1. Atomic notes: one concept per note, short (< 200 lines)
2. Linking: connect related notes with [[wikilinks]] or relative paths
3. Structure: MOC (Map of Content) files as indexes for topics
4. Tags: #topic #status #type for filtering
5. Daily notes: date-stamped notes for time-sensitive learnings
6. Review cycle: weekly review to strengthen connections
7. Save to `data/research/` or appropriate location

## Output format
```markdown
# <Concept Name>
**Tags:** #ai #rag #retrieval
**Related:** [[embeddings]], [[vector-search]]

## Core Idea

## Key Details

## Examples

## References
```

## Example
/knowledge-base organize all research in data/research/ into linked atomic notes with MOC
