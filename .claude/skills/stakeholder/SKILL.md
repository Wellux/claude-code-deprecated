---
name: stakeholder
description: >
  Create stakeholder updates and executive summaries. Invoke for: "stakeholder update",
  "executive summary", "status report", "update the team", "write progress report",
  "non-technical summary", "management update".
argument-hint: audience and timeframe for the update
allowed-tools: Read, Write, Bash
---

# Skill: Stakeholder — Executive Updates & Status Reports
**Category:** Project Management

## Role
Translate technical progress into clear, concise stakeholder updates that non-technical audiences understand.

## When to invoke
- Weekly status reports
- Executive briefings
- "write an update for the team"
- Post-milestone communication

## Instructions
1. Read MASTER_PLAN.md and tasks/todo.md for current progress
2. Run `git log --since="last week" --oneline` for recent work
3. No technical jargon — translate to business outcomes
4. Structure: Status (RAG) / What shipped / What's next / Risks
5. Lead with impact, not activity
6. Keep under 300 words

## Output format
```
## Project Update — <project> — <date>
**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Blocked

### What Shipped (Last Week)
- Built 105+ AI skills for automatic invocation

### What's Coming (Next Week)
- Completing Python AI stack and documentation

### Risks
- None / [specific risk]
```

## Example
/stakeholder write weekly update for wellux_testprojects — non-technical audience
