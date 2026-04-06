# Hot Memory — Always Loaded (≤50 lines)
<!-- L0: active project context — DYNAMIC above marker, STATIC below -->

<!-- DYNAMIC: auto-updated by pre-compact.sh on every compaction -->
**Last Updated**: 2026-04-06 07:59:49

## Active Context (auto-updated)

## Recent Commits (auto-updated)
- 59d94ee fix(version): correct VERSION_INFO to 4-tuple (major, minor, patch, pre)
- 4b62160 fix(version): read version dynamically from installed metadata or pyproject.toml
- da20c0e docs(CLAUDE.md): document v1.0.7 additions — open-findings, 30 lessons, hook improvements

## Recent Lessons (auto-updated)

### Lesson 28: A module-level name that doesn't exist will always ImportError silently
- PATTERN: `cmd_serve_mcp` did `from src.mcp_server import mcp`. There was no `mcp` at
  module level in `mcp_server.py` — it was only created inside `_build_server()` which ran
  under `if __name__ == "__main__":`. The `ImportError` was caught and printed the misleading
  message "Error: 'mcp' not installed" — even when `mcp` was installed. The feature was
  completely broken and gave no useful diagnostic.
- RULE: Before shipping a `from module import name` call, verify `name` is actually defined
  at module level in the target file. Never import an internal helper's return value as if it
  were a module-level export.
- PREVENTION: Add a smoke test: `python3 -c "from src.mcp_server import run"`. If it raises
  `ImportError: cannot import name`, the export is missing. This takes 2 seconds and catches
  the entire class of broken-export bugs.


### Lesson 29: awk section extraction needs heading-as-delimiter, not separator lines
- PATTERN: Tried to extract lessons from `tasks/lessons.md` using `---` as the end-of-lesson
  sentinel: `/^---/{if(in_l && buf!=""){lessons[++c]=buf}}`. Only 1 of 26 lessons was
  captured — because lessons are separated only by the NEXT `### Lesson N` heading, not by
  `---` lines. The single `---` appears once at the top of the file after the Format section.
- RULE: When extracting numbered/headed sections from Markdown, use the START of the NEXT
  heading as the signal to save the PREVIOUS section's buffer, then reset. Do not assume
  separator lines (`---`, `===`) exist between sections.
- PREVENTION: Pattern: `/^### Heading/{if(in_s && buf!="") save(buf); buf=""; in_s=1} in_s{buf+=line}`
  with `END{if(in_s && buf!="") save(buf)}` to capture the final section with no trailing separator.

<!-- STATIC: manually curated below — never auto-overwritten by hooks -->

## Key Architecture Decisions
- **Routing first**: every task goes through 5-router system (llm/skill/agent/memory/task)
- **Skills over code**: prefer adding a skill before writing procedural code
- **Editable install**: `pip install -e ".[dev]"` with `build-backend = "setuptools.build_meta"`
- **Entry point**: `from src.cli import main` — project root must be on sys.path
- **PreCompact hook**: snapshots git state + open tasks before every context compaction
- **No-dup triggers**: `test_no_duplicate_trigger_phrases` enforces unique triggers across 123 skills
- **Chat via messages API**: always `client.chat(messages=[...])`, never flatten to string

## Completed Work
- v0.9.0–v0.9.4: tiered memory, 7 hooks, 9 new skills, per-module CLAUDE.md (6 files), glacier ADRs
- v1.0.0: first stable release — README updated, version bumped
- v1.0.1: 5 bugs fixed (error_handler op-precedence, tiered_memory dead var, llm_router dup,
  grc-analyst trigger, /chat native API); 8 new tests; smoke suite +1 case; 5 new lessons
- v1.0.2: ccm lint CLI subcommand; search_glacier limit param; mcp_server deferred FastMCP import
- v1.0.3: API /v1/ prefix via APIRouter; shared conftest fixtures; README/docs synced
- v1.0.4: dead var, content[0] IndexError, regex cache, ChatRequest validation, session-start URL fix
- v1.0.5: JSONL comment fix, pyproject requires-python <4, CI cache-dependency-path
- v1.0.6: HTTPException detail no longer leaks str(e); logger redacts password/token/api_key/secret
- v1.0.7: all P2/P3 findings resolved; EvalRunner max_workers; richer session-start boot display
  · 31 lessons total (27-31: hook static zones, module exports, awk delimiters, ANSI/sed, heredoc backticks)

## Critical Files
- `src/routing/skill_router.py` — 123-skill registry (no duplicates)
- `src/persistence/tiered_memory.py` — hot/warm/glacier tiers
- `src/llm/claude_client.py` — `chat()` + `complete()` with retry/backoff
- `.claude/hooks/pre-compact.sh` — context survival hook
- `tasks/lessons.md` — self-improvement log (31 lessons)

## Never Do
- Push to main without permission
- Commit .env or API keys
- Skip ruff check before marking done
- Flatten chat messages to a string — use `client.chat(messages=[...])`
- Mix `or`/`and` without explicit parentheses
