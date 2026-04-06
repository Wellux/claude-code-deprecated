---
name: create
description: >
  Creates new skills or agents from scratch. Invoke proactively when: a repeatable
  workflow is identified, user says "make a skill", "create an agent", "turn this into
  a skill", "automate this", "save this workflow", "I keep doing this". If a workflow
  has been repeated twice, suggest capturing it. Decision: if task needs autonomous
  multi-step execution → agent; if it's a knowledge/instruction pack → skill.
argument-hint: describe the workflow or task to capture
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: Create

**Category:** Meta

## Role
Creates new skills or agents by analyzing a described workflow and generating the appropriate SKILL.md or agent file with correct frontmatter and trigger phrases.

## When to invoke
- User says "make a skill", "create an agent", "turn this into a skill"
- A workflow has been repeated twice and should be captured
- User says "automate this", "save this workflow", "I keep doing this"
- A complex multi-step process needs to be standardized

## Instructions
1. Ask clarifying questions: what triggers this workflow? What are the steps? What is the expected output?
2. Determine type: count agent signals — does it need autonomy, multi-tool use, long-running execution, self-directed decisions? If yes → agent (.claude/agents/<name>.md). If it's a knowledge/instruction pack → skill (.claude/skills/<name>/SKILL.md)
3. Draft the description field first — this is the most critical part. Include all trigger phrases a user might say. Make it specific about auto-activation conditions.
4. Write the complete file with YAML frontmatter (name, description, argument-hint, allowed-tools)
5. Include: Role, When to invoke, Instructions, Output format, Example sections
6. Run a quick sanity check: does the description field contain enough trigger phrases? Would it activate at the right time?

## Output format
A complete SKILL.md or agent.md file written to the correct path with no placeholders. Confirmation message with the file path and a brief explanation of the trigger conditions.

## Example
/create summarize git commits and post to Slack on every push
