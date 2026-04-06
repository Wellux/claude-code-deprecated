---
name: paperclip
description: >
  Multi-agent orchestration with org structure, spend budgets, and audit trails.
  Invoke for: "paperclip", "multi-agent orchestration", "agent org chart", "assign to agents",
  "agent with budget", "orchestrate agents", "agent company", "zero-human team",
  "agent pipeline with audit", "parallel agents with tracking".
  Inspired by Paperclip AI (paperclipai/paperclip).
argument-hint: project or task to orchestrate across multiple agents
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: Paperclip — Multi-Agent Orchestration
**Category:** Ecosystem
**Inspired by:** Paperclip AI (github.com/paperclipai/paperclip)

## Role
Act as an orchestration architect. Structure complex projects as an agent organization — named
roles, explicit task handoffs, spend budgets, heartbeat tracking, and a full audit trail.
Prevent agents from double-working. Ensure context persists between agent sessions.

## When to Invoke
- A task is too large for one agent context window
- Multiple independent workstreams can run in parallel
- You need audit trails and budget controls on agent work
- Replacing a multi-step human workflow with agents
- Building a "zero-human" pipeline

## Org Structure Design

### Define Roles
Each agent gets:
- **Name** — unique identifier (e.g., `eng-1`, `qa-lead`, `researcher`)
- **Role** — responsibility scope
- **Budget** — max tokens / cost before auto-pause
- **Input** — what it receives to start
- **Output** — what it produces when done
- **Reports to** — who reviews its output

### Prevent Double-Work
- Use atomic task checkout: each task has a `status` (pending → claimed → done)
- Store task state in `data/cache/paperclip-tasks.json`
- Agents read and lock tasks before starting

### Audit Trail
Every agent logs to `data/cache/paperclip-audit.jsonl`:
```json
{"ts": "ISO8601", "agent": "eng-1", "task": "task-id", "status": "started", "note": "..."}
{"ts": "ISO8601", "agent": "eng-1", "task": "task-id", "status": "done", "output": "..."}
```

## Orchestration Template

```
## Paperclip: <Project Name>
Budget: <total token budget>
Deadline: <date or sprint>

### Org Chart
Orchestrator (this session)
├── researcher    — gather context, write design doc
├── eng-1         — implement core module
├── eng-2         — implement tests
├── qa-lead       — review + integration test
└── tech-writer   — update docs

### Tasks
| ID | Agent | Task | Input | Output | Budget | Status |
|----|-------|------|-------|--------|--------|--------|
| T1 | researcher | research approach | requirements | design-doc.md | 20k tok | pending |
| T2 | eng-1 | implement src/module.py | design-doc.md | module + diff | 40k tok | pending |
| T3 | eng-2 | write tests/test_module.py | module diff | test file | 30k tok | pending |
| T4 | qa-lead | review + run tests | T2+T3 output | review.md | 20k tok | pending |
| T5 | tech-writer | update docs/ | design-doc.md | updated docs | 10k tok | pending |

### Handoff Protocol
1. Orchestrator assigns T1 → researcher
2. researcher writes design-doc.md → signals done
3. Orchestrator reviews design-doc.md, approves
4. Orchestrator assigns T2 + T3 in parallel → eng-1 + eng-2
5. Both signal done → Orchestrator assigns T4 → qa-lead
6. qa-lead approves → Orchestrator assigns T5 → tech-writer
7. All done → Orchestrator runs /ship gate
```

## Process

1. **Decompose** — list all tasks, identify dependencies
2. **Assign** — match tasks to agent roles by capability
3. **Budget** — set token budgets to prevent runaway costs
4. **Checkpoint** — after each agent, orchestrator reviews before next handoff
5. **Audit** — log all agent activity to `data/cache/paperclip-audit.jsonl`
6. **Ship** — orchestrator runs `/ship` as final gate

## Quick Mode (3-agent pipeline)

For simple parallelization without full org overhead:
```
/swarm <task>    # Decomposes into parallel workstreams automatically
```

Use `/paperclip` when you need budget control and audit trails.
Use `/swarm` when you just need fast parallelization.

## Example
/paperclip build the full eval framework — researcher, 2 engineers, qa, docs writer
