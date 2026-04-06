---
name: tutorial-writer
description: >
  Write step-by-step tutorials and how-to guides. Invoke for: "write tutorial",
  "how-to guide", "tutorial for X", "explain how to use", "step-by-step guide",
  "workshop material", "create a tutorial", "teach someone to use".
argument-hint: topic and target audience for the tutorial
allowed-tools: Read, Write, Glob
---

# Skill: Tutorial Writer — Step-by-Step Learning Guides
**Category:** Documentation

## Role
Write tutorials that teach by doing — the reader ends up with something working after following along.

## When to invoke
- New feature needs user documentation
- "write a tutorial for X"
- Onboarding material needed
- Workshop or demo preparation

## Instructions
1. Define: who is the target reader? What will they accomplish?
2. Prerequisites: what must they have/know before starting?
3. Each step: one action, explanation of WHY, expected result
4. Code: runnable, tested, copy-pasteable
5. Checkpoint: verify working state at key points
6. Troubleshooting: common mistakes and how to fix them

## Output format
```markdown
# Tutorial: <title>
**Goal:** You will build/learn...
**Time:** ~Xmin | **Level:** Beginner/Intermediate

## Prerequisites
## Step 1: <verb + noun>
[explanation]
```code
```
Expected result: ...

## Troubleshooting
```

## Example
/tutorial-writer write tutorial for using the /karpathy-researcher skill — beginner level
