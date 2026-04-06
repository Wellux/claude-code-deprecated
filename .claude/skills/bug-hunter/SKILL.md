---
name: bug-hunter
description: >
  Proactively hunt for bugs, edge cases, and failure modes before they hit production.
  Invoke for: "find bugs", "edge cases", "what could go wrong", "stress test this logic",
  "race condition", "off-by-one", "null pointer", "hunt for bugs", "find weaknesses",
  "adversarial inputs", "what breaks this".
argument-hint: file, function, or component to hunt
allowed-tools: Read, Grep, Glob
---

# Skill: Bug Hunter — Proactive Defect Detection
**Category:** Development

## Role
Hunt for bugs, edge cases, and failure modes before users find them. Read code adversarially.

## When to invoke
- Pre-release validation
- "what could break here"
- After writing complex logic
- Code feels "too clean" — something's probably missing

## Instructions
1. Read the code with an adversarial mindset
2. Check: None/null inputs → what happens?
3. Check: empty collections, zero values, negative numbers, max integers
4. Check: concurrent access → race conditions?
5. Check: error paths → all exceptions caught? Resources released on error?
6. Check: off-by-one in loops, slices, pagination
7. Check: type coercion surprises, float precision
8. For each bug found: show the input that triggers it + what breaks

## Output format
```
## Bug Hunt — <file> — <date>
### Bugs Found
1. [file.py:34] NULL_DEREF — if user is None, crashes on user.name
   Trigger: pass user=None to create_session()
   Fix: add `if user is None: raise ValueError`
### Edge Cases Not Handled
### All Clear ✅
```

## Example
/bug-hunter src/llm/claude_client.py — hunt for error handling gaps and edge cases
