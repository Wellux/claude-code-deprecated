---
name: agent-orchestrator
description: >
  Design and implement multi-agent orchestration systems. Invoke for: "multi-agent system",
  "orchestrate agents", "agent pipeline", "agent workflow", "how should agents communicate",
  "agent coordination", "task delegation to agents", "build an agent system".
argument-hint: agent system to design or orchestrate
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Agent Orchestrator — Multi-Agent Coordination
**Category:** AI/ML Research

## Role
Design multi-agent systems with clear role separation, communication protocols, and failure handling.

## When to invoke
- Building a multi-agent pipeline
- Agent coordination design
- "how do I have Claude agents work together"
- Complex task decomposition with specialized agents

## Instructions
1. Identify agent roles: what is each agent's specific responsibility?
2. Define communication: how do agents pass results? Shared state or message passing?
3. Design orchestration: sequential, parallel, or conditional branching?
4. Handle failures: what if an agent fails? Retry? Fallback? Human escalation?
5. Implement orchestrator: spawns sub-agents, collects results, synthesizes output
6. Add monitoring: log each agent's input/output, measure performance

## Output format
```
## Agent System Design — <name>
### Agents
| Agent | Role | Input | Output |
### Communication Protocol
### Orchestration Flow
### Failure Handling
### Implementation
```

## Example
/agent-orchestrator design research→code→test→review pipeline for feature implementation
