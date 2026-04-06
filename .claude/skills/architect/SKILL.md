---
name: architect
description: >
  System design and architecture planning. Invoke for: "design this system", "architecture
  review", "how should I structure this", "system design", "technical design doc",
  "ADR", "architecture decision", "scalability design", "what's the right architecture".
argument-hint: system or feature to design (e.g. "real-time chat system" or "review src/ architecture")
allowed-tools: Read, Write, Grep, Glob
---

# Skill: Architect — System Design & Architecture
**Category:** Development

## Role
Design scalable, maintainable system architectures. Produce clear diagrams, component descriptions, and trade-off analysis.

## When to invoke
- New system or major feature design
- Architecture review of existing system
- Evaluating architectural trade-offs
- Writing an Architecture Decision Record (ADR)

## Instructions
1. Clarify requirements: what must it do? Non-functional requirements? Scale? Latency?
2. Identify components and their responsibilities
3. Design data flow: how does data move between components?
4. Consider: scalability, fault tolerance, coupling, cohesion, data consistency
5. Draw ASCII architecture diagram
6. Identify key decisions and trade-offs
7. Write ADR if decision is significant (see /adr-writer)

## Output format
```
## Architecture Design — <system> — <date>
### ASCII Diagram
### Components
### Data Flow
### Key Decisions & Trade-offs
### Risks & Mitigations
```

## Example
/architect design the LLM prompt chaining system for src/prompt_engineering/
