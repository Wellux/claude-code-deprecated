---
name: arch-diagrammer
description: >
  Create ASCII architecture and system diagrams. Invoke for: "draw architecture diagram",
  "system diagram", "architecture overview", "visualize the system", "component diagram",
  "data flow diagram", "sequence diagram", "C4 diagram".
argument-hint: system or component to diagram
allowed-tools: Read, Write, Glob, Grep
---

# Skill: Architecture Diagrammer — Visual System Maps
**Category:** Documentation

## Role
Create clear ASCII diagrams that communicate system architecture, data flow, and component relationships.

## When to invoke
- "draw this architecture"
- New system needs visual overview
- Explaining system to stakeholders
- docs/architecture.md needs updating

## Instructions
1. Read all code to understand actual system (not aspirational)
2. Choose diagram type: system context / container / component / sequence / data flow
3. Use ASCII art with clear boxes, arrows, and labels
4. Show: components, connections, data direction, external systems
5. Keep it at the right level of abstraction (don't diagram every function)

## Output format
```
## Architecture: <name>

┌──────────────────┐     ┌──────────────────┐
│   Claude CLI     │────▶│  .claude/skills/  │
└──────────────────┘     └──────────────────┘
         │                        │
         ▼                        ▼
┌──────────────────┐     ┌──────────────────┐
│   CLAUDE.md      │     │  .claude/hooks/  │
└──────────────────┘     └──────────────────┘
```

## Example
/arch-diagrammer draw complete system diagram for wellux_testprojects
