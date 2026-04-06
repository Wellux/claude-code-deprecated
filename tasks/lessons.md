# Lessons Learned — Self-Improvement Log

## Format
```
DATE | PATTERN | RULE | PREVENTION
```
After ANY correction: append a new lesson here.
session-start.sh shows last 6 lines on boot.

---

## 2026-03-28

### Lesson 1: SKILL.md frontmatter is critical
- PATTERN: Skills without proper YAML frontmatter (name: + description:) don't auto-activate
- RULE: Every SKILL.md MUST start with `---\nname: <name>\ndescription: >` block
- PREVENTION: post-tool-edit.sh hook validates SKILL.md frontmatter on every write

### Lesson 2: Plan before building
- PATTERN: Starting implementation without a MASTER_PLAN causes rework and lost context
- RULE: Always check MASTER_PLAN.md next step before any new task
- PREVENTION: session-start.sh shows next MASTER_PLAN step on every boot

### Lesson 3: Parallel agents need separate directories
- PATTERN: Multiple agents writing to same files causes conflicts
- RULE: Always assign each agent to non-overlapping file paths
- PREVENTION: /swarm skill checks for path conflicts before spawning agents

### Lesson 4: Hook exit codes matter
- PATTERN: Forgetting exit codes in hooks breaks them silently
- RULE: Always end hooks with explicit exit 0 (allow) or exit 2 (block)
- PREVENTION: post-tool-edit.sh validates hook scripts end with exit statement

### Lesson 5: Settings.local.json for development freedom
- PATTERN: Overly restrictive settings.json blocks legitimate local dev commands
- RULE: Use settings.local.json for unrestricted local access (gitignored)
- PREVENTION: settings.local.json is always present with Bash(*) allow

### Lesson 6: LLMs fail on reasoning, not knowledge
- PATTERN: Vague prompts ("summarize this") produce inconsistent output quality
- RULE: Always specify output format + reasoning steps explicitly in every prompt
- PREVENTION: Use tools/prompts/claude-code-prompts.md templates as starting points

### Lesson 7: MCP provides intelligence, Hooks provide discipline
- PATTERN: Adding MCP tools without hooks means Claude can use them unsafely
- RULE: For every new capability (MCP tool), add a corresponding hook guard if destructive
- PREVENTION: pre-tool-bash.sh hook reviews all Bash; extend for MCP tool calls as needed

### Lesson 8: Graph RAG for relational, flat RAG for simple
- PATTERN: Using vector-only RAG on knowledge bases with complex relationships → hallucinations
- RULE: If the domain has entity relationships (medical, legal, financial), evaluate LightRAG first
- PREVENTION: /rag-builder skill now defaults to recommending LightRAG for relational domains

### Lesson 9: LoRA rank r=32 is the 2026 sweet spot
- PATTERN: Default r=8 in most tutorials undertrained for domain-specific tasks
- RULE: Use r=32 for fine-tuning, paged_adamw optimizer, bf16 dtype — document all three
- PREVENTION: /fine-tuner skill includes r=32 as the recommended default config

### Lesson 10: Safety is neuron-sparse — freeze SCUs before fine-tuning
- PATTERN: Domain fine-tuning degrades safety refusals by 10-15% when applied naively
- RULE: Run safety neuron analysis before any fine-tune; freeze top 20% SCU neurons
- PREVENTION: /fine-tuner skill now includes pre-tune safety unit identification step

### Lesson 11: Write lint-clean code from the start — CI will catch it otherwise
- MISTAKE: 30 ruff errors committed across src/ and tests/ — CI failed on first real run
- WHY: Unused imports, ambiguous names (`l`), mid-module imports, f-strings without placeholders,
  unused local variables — all fixable locally but not caught before push
- RULE: Run `ruff check src/ tests/ --select E,F,W --ignore E501` before every commit
- PREVENTION: pre-commit hook (`.pre-commit-config.yaml`) now enforces this automatically;
  `ruff --fix` auto-resolves ~80% of issues; remaining 6 require manual fixes:
  - E402: move `import` to top of file
  - E741: rename `l`/`O`/`I` vars → `ln`/`val`/etc.
  - F841: prefix unused vars with `_` or delete the assignment

### Lesson 12: Keep CLAUDE.md current — stale context misleads every future session
- MISTAKE: CLAUDE.md referenced `claude_code_max` directory and omitted CLI, eval framework,
  rules layer, middleware, and API conventions built over many sessions
- WHY: CLAUDE.md is loaded on every session start — outdated info causes wrong assumptions
- RULE: Update CLAUDE.md whenever a major new capability is added (CLI command, module, layer)
- PREVENTION: End-of-session checklist now explicitly includes "update CLAUDE.md if architecture changed"

### Lesson 13: Karpathy single-file rule — complexity is always optional
- PATTERN: Adding abstractions (base classes, plugin hooks, config inheritance) before they are
  needed creates cognitive overhead with no benefit for the current problem
- RULE: If a module cannot be understood in one read-through (<60 seconds), it is too complex.
  Each router is ~30-40 lines. Each runner is ~40 lines. This is correct.
- PREVENTION: Before adding an abstraction, ask "does this exist at nanoGPT scale?" If not, wait.

### Lesson 14: Unbounded in-memory state is a time bomb
- PATTERN: LogIndex._lines growing forever — after 30 days of 1000 req/day = 30M entries,
  potentially 30 GB RAM. No eviction = silent OOM after enough time passes.
- RULE: Every in-memory collection that grows via append MUST have a documented bound.
  Either: max_entries cap with eviction, or explicit lifecycle (cleared on restart), or TTL.
- PREVENTION: LogIndex now has max_entries=100_000 with FIFO 25% eviction (amortized O(1)).
  The pattern: n_drop = max(1, int(len * 0.25)); _lines = _lines[n_drop:]; rebuild_index().

### Lesson 15: Async timeouts are mandatory — not optional hardening
- PATTERN: AsyncEvalRunner._run_case awaited self.llm(...) with no timeout. A hung LLM call
  holds a semaphore slot indefinitely, blocking all other concurrent cases permanently.
- RULE: Every await on an external call (LLM, HTTP, database) MUST be wrapped in
  asyncio.wait_for(..., timeout=N). The timeout should match SLA expectations (30s for LLM).
- PREVENTION: AsyncEvalRunner now passes case_timeout=30.0 to asyncio.wait_for. The
  TimeoutError is caught and returned as EvalResult(verdict=ERROR) like any other exception.

### Lesson 16: context var must reset in finally, not in except+normal-path
- PATTERN: CorrelationIDMiddleware called _request_id_var.reset(token) in two places:
  once in the except block, once after the try/except. If response.headers access raises,
  the reset is skipped and the context var leaks into subsequent requests.
- RULE: Any contextvars.ContextVar.reset(token) call MUST be in a finally block.
  The try/finally pattern guarantees reset regardless of exception type.
- PREVENTION: Middleware dispatch now uses try/finally. The response return is inside try.

### Lesson 17: EvalSuite.from_jsonl bypassed duplicate check — silent data bugs
- PATTERN: from_jsonl used cls(suite_name, cases) which sets _cases directly, bypassing the
  add() method's duplicate ID check. A JSONL file with two identical IDs loaded silently,
  causing incorrect result counts in EvalReport.
- RULE: Internal construction of collections must use the same validation path as external
  mutation. from_jsonl now uses suite.extend(cases) which calls add() for each case.
- PREVENTION: Any cls(...) constructor that accepts a list should either validate in __init__
  or delegate to add(). Never bypass validation with direct assignment in classmethods.

### Lesson 18: Edit tool fails silently on whitespace drift — always Read immediately before Edit
- PATTERN: Multiple Edit calls in a session where the file was changed between the last Read
  and the Edit (by a hook, background agent, or parallel tool). The match string no longer
  exists and the edit silently no-ops or throws "String not found".
- RULE: Always Read a file immediately before Edit. Never batch a Read + multiple Edits
  if anything could change the file between them. Keep match strings small and unique.
- PREVENTION: Added to warm/troubleshooting.md as the #1 gotcha. Use Grep to confirm
  the exact string exists before attempting a multi-step Edit chain.

### Lesson 19: Background agents can re-introduce fixed bugs — verify after subagent completion
- PATTERN: A background research/implementation agent was launched while duplicate triggers
  were being fixed. The agent re-added "backup verification", "decision log", and
  "runbook" as duplicate triggers in skill_router.py — re-breaking the test that was
  just fixed in the main context.
- RULE: After any background agent modifies shared files (especially registries and config),
  run the relevant tests before assuming the state is clean.
- PREVENTION: After every Agent tool completion that touches src/ or tests/, run
  `python3 -m pytest tests/ -q` before proceeding. Never trust subagent self-reports.

### Lesson 20: Skill routing registry duplicates are caught by test — fix the lower-priority skill
- PATTERN: When adding new ecosystem skills, several trigger phrases were shared
  between new skills and existing ones (e.g., "semantic search" in both rag-builder and
  embeddings; "ai safety review" in both ai-security and ai-safety).
- RULE: The lower-priority skill (or the one whose skill name is less specific to the
  trigger) should have its duplicate trigger removed. Keep the trigger in the skill
  that most accurately describes it.
- PREVENTION: Run duplicate check before every commit touching skill_router.py:
  `python3 -c "from src.routing.skill_router import _SKILL_REGISTRY; seen={}; [print('DUP:',t,e['skill'],seen[t]) for e in _SKILL_REGISTRY for t in e['triggers'] if t in seen and seen[t]!=e['skill'] or seen.update({t:e['skill']}) and False]"`

### Lesson 21: Hot memory must be updated at PreCompact — not just at Stop
- PATTERN: Pre-v0.9.0 the only lifecycle save was in stop.sh. When Claude Code compacted
  context mid-session, all in-flight state (active branch, open decisions, partial task
  state) was lost. The next session started completely cold.
- RULE: Critical session state (branch, open tasks, last commit, active feature) must be
  written to hot-memory.md in the PreCompact hook, not just at session end.
- PREVENTION: PreCompact hook now writes a full hot-memory.md snapshot before every
  compaction. This is the most important hook for context survival.

### Lesson 22: Operator precedence in multi-condition if-statements is a silent logic bug
- PATTERN: `if "a" in x or "b" in x and "c" in x:` — Python evaluates `and` before `or`,
  so this is `("a" in x) OR ("b" in x AND "c" in x)`. Any string containing "a" (e.g. "asyncio
  context") matched the token-limit branch even when unrelated to token limits.
- RULE: Always use explicit parentheses when mixing `or` and `and` in the same condition.
  Write `if ("a" in x and "b" in x) or ("c" in x and "d" in x):` — never rely on precedence.
- PREVENTION: Add a test for the "false positive" case: `test_context_alone_is_not_token_limit`.
  CI catches regressions immediately.

### Lesson 23: Dead variable assignments mask latent path bugs
- PATTERN: `target = MODULE_CONST / "path"` followed immediately by `target = self._dir / "path"`
  — line 1 is dead code, but it looks like intentional initialization. If line 2 is accidentally
  removed (e.g. during a merge), line 1 silently uses the wrong path.
- RULE: Delete dead variable assignments immediately. "Two assignments to the same variable
  in consecutive lines" is always a bug or a cleanup failure.
- PREVENTION: Ruff B018 / pylint W0612 (unused variable) would catch this. Ensure `"B"` is in
  ruff select (it is: `pyproject.toml` has `select = ["E", "F", "W", "I", "UP", "B"]`).

### Lesson 24: String-flattening a chat history bypasses the LLM's trained behavior
- PATTERN: Building `"USER: ...\n\nASSISTANT: ...\n\nUSER: ..."` and passing it as a single
  prompt to a chat model. Claude is trained on structured `messages` arrays, not role-prefixed
  strings. Results are degraded and role injection is possible via `msg.role.upper()`.
- RULE: Always pass multi-turn history as a `messages: list[dict]` to the native API.
  For `ClaudeClient`, use the new `client.chat(messages, ...)` method — never `client.complete()`
  with a flattened string for conversations.
- PREVENTION: `test_multi_turn_passes_messages_list` in `test_api_endpoints.py` verifies the
  messages list is passed directly (not flattened) on every push.

### Lesson 25: Broad keyword triggers cause silent mis-routing
- PATTERN: `grc-analyst` had `"audit"` as a trigger. A user asking `"audit my code"` or
  `"run a db audit"` got routed to a GRC compliance analyst instead of `code-review` or `dba`.
  The error was silent — routing succeeded, but to the wrong skill.
- RULE: Skill triggers must be specific enough that they only match the intended use case.
  Prefer multi-word phrases: `"compliance audit"` over `"audit"`. Run `ccm route "audit my code"`
  to sanity-check routing after every skill registry change.
- PREVENTION: After any `_SKILL_REGISTRY` edit, manually test 3 representative prompts with
  `ccm route` before committing.

### Lesson 26: Abstract methods must be implemented even if you want to remove the concept
- PATTERN: Removed `count_tokens` from `ClaudeClient` because it was dead code. Broke all
  26 `ClaudeClient` instantiation tests with `TypeError: Can't instantiate abstract class`.
  The method is declared `@abstractmethod` in `LLMClient` (base class).
- RULE: Before removing a method from a concrete class, check if it's `@abstractmethod` in the
  parent. If the concept should be removed entirely, remove the `@abstractmethod` declaration
  from the base class first, then remove implementations.
- PREVENTION: `grep -r "abstractmethod" src/llm/base.py` before deleting any method from
  a class that inherits from `LLMClient` or any other ABC.

### Lesson 27: Automation hooks that overwrite files destroy manually curated content
- PATTERN: `pre-compact.sh` used `cat > hot-memory.md << EOF ... EOF` — a full overwrite.
  Every compaction silently wiped the carefully maintained "Completed Work", "Key Architecture
  Decisions", and "Never Do" sections, replacing them with a hardcoded stale template
  ("114 skills", 1 commit, no version). The loss was invisible until the session-start
  displayed only 4 bullet lines from a 46-line file.
- RULE: Any hook that updates a file must distinguish between dynamic (auto-generated) and
  static (manually curated) zones. Use a sentinel comment to mark the boundary.
  Only overwrite above the sentinel; extract and re-append everything below it.
- PREVENTION: Add `<!-- STATIC: never auto-overwritten -->` before any curated section in
  files touched by hooks. In the hook, extract the static zone with
  `awk '/<!-- STATIC:/{found=1} found{print}'` before writing, then re-append it.

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

### Lesson 30: ANSI escape codes in sed replacement strings are treated as literals
- PATTERN: `sed 's/^- \[ \] /  \033[1;33m▸\033[0m /'` — the `\033` is NOT expanded by sed
  into ESC. It becomes literal backslash + `033`, so the terminal receives the characters
  `\`, `0`, `3`, `3` instead of the ANSI escape sequence. The colored arrow appeared as
  garbled text in the output.
- RULE: Never use `\033` (or `\e`) ANSI escape codes inside sed replacement strings. Use
  `printf` with a while-read loop when color output is needed in shell scripts.
- PREVENTION: Replace `grep ... | sed 's/prefix/  \033[...m▸\033[0m /'` with:
  `grep ... | while IFS= read -r line; do printf '  \033[...m▸\033[0m %s\n' "${line#prefix}"; done`

### Lesson 31: Unquoted heredocs execute backticks in expanded variables
- PATTERN: `pre-compact.sh` used `cat > file << MEMEOF ... $RECENT_LESSONS ... MEMEOF`.
  `$RECENT_LESSONS` contained backtick-quoted code examples (awk patterns, grep pipelines)
  from lessons 29-30. Bash executed those backticks as command substitutions inside the
  heredoc, silently swallowing output and dropping the Branch/Version/Tests/Skills lines
  from Active Context on every compaction that followed a lesson-extraction run.
- RULE: Never embed user-sourced or file-sourced content (lesson text, commit messages,
  file contents) directly inside an unquoted heredoc. Use `printf '%s\n' "$VAR"` to append
  variable content to a file — printf treats `%s` literally and never interprets backticks.
- PREVENTION: For any shell script writing structured files with embedded variables:
  use `<< 'QUOTED_DELIM'` for static template text; use `printf '%s\n' "$VAR" >> file`
  for all user-sourced variable content. If both are needed, split into separate writes.

---
_Append new lessons above this line. Newest lessons should appear at the bottom._
