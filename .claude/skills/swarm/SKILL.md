---
name: swarm
description: >
  Decomposes a complex task into parallel subagents and creates all agent files for
  immediate execution. Invoke when: "create agents for this", "spin up a swarm",
  "parallel agents", "swarm this", "break into subagents", "orchestrate agents for",
  "what agents do I need", "build a swarm", "I need agents for this task",
  task is too large for a single context window, or multiple independent workstreams exist.
  Phase 1: read all project context. Phase 2: decompose into independent streams.
  Phase 3: create per-agent .md files in .claude/agents/. Phase 4: adversarial validation.
  Phase 5: deliver execution plan with quality gates.
argument-hint: full endstate description or task to decompose
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: Swarm — Parallel Agent Decomposer + Adversarial Validator

## Role
Decompose a complex task into parallel autonomous subagents, each with a focused mission.
Produce all agent definition files plus an orchestration plan with built-in adversarial
validation phase (dsifry/metaswarm pattern).

## When to invoke
- Task has 3+ independent workstreams that can run in parallel
- Task is too large for a single Claude context window
- User says "swarm", "parallel agents", "orchestrate agents", "build a swarm"
- Research + coding + testing + review can all happen simultaneously
- MASTER_PLAN phase has multiple parallel steps

## 4-Phase Execution Model

### Phase 1: Context + Decompose
1. Read CLAUDE.md, MASTER_PLAN.md, tasks/todo.md, relevant src/ files
2. Analyze endstate: what does "done" look like? What are all deliverables?
3. Split into independent workstreams (each needs no output from others to start)
   - Typical streams: research, code, test, review, docs, deploy

### Phase 2: Agent Design + File Creation
For each stream, define:
- **Mission**: 1-sentence outcome statement
- **Tools**: exactly which tools are needed
- **Input**: what context/files this agent needs to start
- **Output**: what files/artifacts it produces
- **Success criteria**: specific, verifiable conditions
- **Quality gate**: how to verify output before marking done

Write `.claude/agents/<stream>-agent.md` for each.

### Phase 3: Execution
- Run agents in dependency order (independent ones in parallel)
- Orchestrator does NOT trust subagent self-reports

### Phase 4: Adversarial Validation (NEW)
After each agent reports completion, the orchestrator spawns a **Validator agent** that:
- Independently re-reads the original spec
- Checks each success criterion with file:line evidence
- Reports: VERIFIED ✅ or FAILED ❌ with specific gaps
- On failure: spawns a new agent with the failure details as context
- Maximum 3 retry cycles before escalating to user

This prevents the "cargo cult complete" pattern where subagents report success without actually meeting the spec.

## Output Format

```
## Swarm Plan: <task name>
**Agents created:** N
**Parallelizable:** X of N
**Quality gates:** adversarial validation after each phase

| Agent | Mission | Runs After | Output | Quality Gate |
|-------|---------|------------|--------|-------------|
| research-agent | ... | — | data/research/ | content.md exists + >500 words |
| code-agent | ... | research | src/ | all tests pass |
| test-agent | ... | code | tests/ | coverage ≥80% |
| validator | ... | each agent | report | evidence-backed VERIFIED/FAILED |

## Execution Order
Round 1 (parallel): research-agent, docs-agent
Round 2 (parallel): code-agent
Round 3 (parallel): test-agent, review-agent
Round 4: adversarial-validator for all Round 1-3 outputs
```

## Example
/swarm Build a RAG system with Claude: research best approaches, implement retrieval, write tests, document API
