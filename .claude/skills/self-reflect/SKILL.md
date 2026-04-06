---
name: self-reflect
description: >
  Mine recent sessions, commits, and PR feedback for patterns and auto-update lessons.
  Invoke for: "self reflect", "extract patterns", "what did we learn", "mine learnings",
  "update lessons from history", "retrospective patterns", "session patterns",
  "what patterns emerged", "learn from mistakes", "self reflection", "improve from history".
  Post-merge / post-session autonomous learning.
argument-hint: scope (e.g. "last 5 commits", "this week", "recent sessions")
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skill: Self-Reflect — Autonomous Pattern Mining & Lesson Extraction

## Role
Autonomously analyze recent work history and extract patterns, recurring mistakes, and
successful techniques. Append structured lessons to `tasks/lessons.md` without manual input.
Inspired by dsifry/metaswarm post-merge self-reflection pattern.

## When to invoke
- After a complex feature lands (post-merge)
- After a debugging session resolves a tricky bug
- At end of sprint or major milestone
- When user says "what did we learn", "extract patterns", "self reflect"
- Proactively: once per week as a cron job

## Data Sources
1. `git log --oneline -20` — recent commit history
2. `git diff HEAD~5..HEAD` — recent code changes
3. `tasks/todo.md` — completed vs open tasks
4. `tasks/lessons.md` — existing lessons (avoid duplicating)
5. `data/sessions/` — daily session logs if available
6. Test failure patterns: `pytest --tb=no -q` output if failures exist

## Pattern Types to Extract

**Anti-patterns** (recurring mistakes):
- Repeated same error category (e.g., whitespace in Edit, circular imports)
- Same file edited multiple times in one session
- Tests broken by same root cause multiple times

**Success patterns** (techniques that worked):
- Approaches that unblocked hard problems
- Architectural decisions that proved correct
- Shortcuts that saved significant time

**Improvement opportunities**:
- Friction points in workflow
- Missing tooling or automation
- Underused existing features

## Instructions

1. Run `git log --oneline -20` and `git diff HEAD~5..HEAD --stat`
2. Read `tasks/lessons.md` to understand existing lessons (avoid duplicating)
3. Read `data/sessions/*.md` for recent session logs
4. Identify: what went wrong, what went right, what took too long
5. Formulate 1–5 new lessons in the standard format
6. Append to `tasks/lessons.md` only if novel (not already captured)
7. Optionally update `.claude/memory/hot/hot-memory.md` with critical new insights

## Lesson Format

```markdown
### PATTERN: <1-line description of the situation>
**RULE:** <what to do / not to do>
**PREVENTION:** <how to catch it earlier next time>
**Source:** self-reflect from <date> via git-log / session-log / test-failure
```

## Output

```
## Self-Reflect: <scope>

### Analyzed
- Commits reviewed: N
- Session logs: N days
- Existing lessons: N

### New Patterns Found

1. **Anti-pattern: Edit fails on stale string match**
   → Added to lessons.md

2. **Success: Parallel tool calls cut task time by ~40%**
   → Added to lessons.md

### Lessons appended: N
### No duplicates of existing N lessons
```
