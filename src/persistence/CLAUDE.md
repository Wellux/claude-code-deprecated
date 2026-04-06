# src/persistence — Persistence Layer Context

## Purpose
Three storage backends: file-based (FileStore), MCP-backed entity graph (MemoryStore),
and tiered hot/warm/glacier memory (TieredMemory).

## Files
- `file_store.py` — writes to `data/research/`, `tasks/todo.md`, `tasks/lessons.md`, `data/cache/events.log`
- `memory_store.py` — MCP memory server: entities, relations, recall via `mcp__memory__*` tools
- `tiered_memory.py` — three-tier: hot (≤50 lines), warm (domain files), glacier (YAML-frontmatter)
- `__init__.py` — exports `FileStore`, `MemoryStore`, `TieredMemory`

## TieredMemory paths (default)
- Hot: `.claude/memory/hot/hot-memory.md`
- Warm: `.claude/memory/warm/<domain>.md`
- Glacier: `.claude/memory/glacier/YYYY-MM-DD-<slug>.md`

## Key rule
Hot tier auto-evicts oldest active-context lines to warm when it exceeds 50 lines.
Glacier files have YAML frontmatter (`---\ntitle:\ndate:\ntags:\n---`) for indexed search.

## Tests
`tests/test_tiered_memory.py` — 26 tests covering all three tiers.
Always use `tmp_path` fixture to avoid writing to real `.claude/memory/`.
