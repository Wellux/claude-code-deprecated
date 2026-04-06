# Claude Code — Copy-Paste Prompts

15 battle-tested prompts for common Claude Code workflows.

---

## 1. Master CLAUDE.md — Drop in any project

```markdown
# Project Instructions

## Core Rules
- Plan before executing any task with 3+ steps — write steps to tasks/todo.md first
- Never mark a task complete without proving it works (run it, check output)
- Touch only what the task requires — no refactoring, no extra features, no cleanup beyond scope
- After any correction from me: add a lesson to tasks/lessons.md immediately
- Use subagents for research/exploration to keep main context clean

## Code Standards
- Read a file before editing it — always
- Prefer editing existing files over creating new ones
- No speculative abstractions — build what's needed, not what might be needed
- No backwards-compat shims, unused vars, or dead code — delete it
- Security: never commit .env, API keys, or secrets

## Git
- Always check git branch before committing
- Never push to main/master without explicit permission
- Commit messages: imperative mood, explain WHY not what

## When Stuck
- Read the error carefully before retrying
- Check your assumptions — don't retry the same failing approach twice
- Ask me only if genuinely blocked after investigation
```

---

## 2. Session Opener

```
Before starting any work:
1. Read CLAUDE.md (project rules)
2. Read tasks/todo.md (open tasks)
3. Read tasks/lessons.md (past mistakes to avoid)
4. Show me: current git branch, next open task, last lesson

Then confirm you're ready.
```

---

## 3. Max Autonomy Mode

```
I want you to work autonomously on the following task. Rules:
- Do NOT ask clarifying questions — make reasonable assumptions and document them
- Write your plan as numbered steps before starting
- Execute each step fully, mark it done, move to the next
- If you hit a blocker: diagnose it, try 2 approaches, then report what you found
- Verify your work before saying done (run it, check output, read the diff)
- Commit completed work at the end with a descriptive message

Task: [DESCRIBE TASK HERE]
```

---

## 4. Bug Fix

```
Bug report: [PASTE ERROR / DESCRIBE BUG]

Fix it. Rules:
- Find the root cause — not the symptom
- Read the relevant files before changing anything
- Make the minimal change that fixes it
- Explain what caused it in one sentence
- Verify the fix works
- Do not refactor surrounding code
```

---

## 5. Code Review — Security + Quality

```
Review this code for:
1. Security issues (OWASP top 10, injection, auth flaws, secrets exposure)
2. Logic bugs and edge cases
3. Performance problems (N+1, missing indexes, O(n²))
4. Error handling gaps (what happens when this fails?)

For each issue: severity (critical/high/medium/low), location (file:line), and the fix.
Prioritize by severity. Skip style nits unless they cause bugs.

[PASTE CODE OR FILE PATH]
```

---

## 6. Architect Mode

```
I want to build: [DESCRIBE FEATURE]

Act as a staff engineer reviewing this before we write a line of code.
Give me:
1. The simplest design that meets the requirements (no over-engineering)
2. The 2-3 tradeoffs I should be aware of
3. What could go wrong (top 3 failure modes)
4. What I should NOT build yet (scope boundaries)
5. A file/module structure if this requires new code

Be direct. Flag if the requirements are unclear before designing.
```

---

## 7. Karpathy Research Mode

```
Research: [TOPIC]

Use the Karpathy method:
1. What is this from first principles? (2-3 sentences, no jargon)
2. What is the single most important insight? (the thing that makes it work)
3. What would I need to rebuild a minimal version from scratch? (key steps)
4. What's the most common mistake practitioners make with this?
5. One concrete thing I can implement or try today

Be technical and specific. No fluff. Cite sources if you find them.
```

---

## 8. Refactor — Surgical

```
Refactor [FILE/FUNCTION] to improve [readability/performance/testability].

Constraints:
- Do NOT change behavior — only structure
- Do NOT rename public APIs or exported types
- Do NOT add new dependencies
- Make one type of change at a time
- Show me the before/after diff and explain each change

If you find bugs while refactoring, note them separately — don't fix them here.
```

---

## 9. Test Writer

```
Write tests for: [FILE/FUNCTION/MODULE]

Rules:
- Test behavior, not implementation — test what it does, not how
- Cover: happy path, error cases, edge cases (empty input, null, boundary values)
- Each test name should describe what it's testing: test_returns_empty_list_when_no_results
- Mock external dependencies (API calls, DB, filesystem)
- No tests that just check "it doesn't crash" — assert on actual output
- Use the existing test framework in the project (check package.json / requirements.txt first)
```

---

## 10. The "Stuck in a Loop" Reset

```
Stop. Let's reset.

Before continuing:
1. What exactly is the error you're seeing? (paste it)
2. What did you try? (list the approaches)
3. What's your current hypothesis about the root cause?
4. What's the simplest possible test to validate that hypothesis?

Do not write any code yet. Just answer these 4 questions.
```

---

## 11. PR Description Generator

```
Generate a PR description for my changes.

Run: git diff main...HEAD

Format:
## What
[1-3 bullet points: what changed, factually]

## Why
[1-2 sentences: why this change was needed]

## How to test
[Numbered steps a reviewer can follow to verify it works]

## Risk
[None / Low / Medium — and why]

Keep it under 200 words total. No fluff.
```

---

## 12. The "Elegant Solution" Prompt

```
You just implemented [DESCRIBE WHAT WAS BUILT].

Now step back. Knowing everything you know about the problem:
- Is there a simpler design that achieves the same result?
- Is there anything here that will be painful to maintain in 6 months?
- Did you add anything that wasn't strictly required?

If yes to any: implement the more elegant version.
If no: confirm it's clean and move on.
```

---

## 13. Incident Response

```
Production issue. Move fast.

Symptom: [DESCRIBE WHAT'S BROKEN]
Error: [PASTE LOGS / ERROR MESSAGE]
Started: [WHEN]
Impact: [WHO IS AFFECTED]

Do this in order:
1. Identify the likely root cause (top 3 hypotheses, ranked)
2. Identify the fastest mitigation (not fix — just stop the bleeding)
3. Then identify the permanent fix

Do NOT start implementing until you've completed step 1.
```

---

## 14. Self-Improvement — After any mistake

```
I just corrected you on: [WHAT WENT WRONG]

Add a lesson to tasks/lessons.md:

## Lesson — [DATE]: [SHORT TITLE]
**Mistake:** [What you did wrong]
**Why it happened:** [Root cause of the mistake]
**Rule:** [Specific rule to follow next time — imperative, one sentence]
**Example of correct behavior:** [One line showing the right approach]

Then confirm it's written.
```

---

## 15. Daily Workflow Kickoff

```
New session. Let's work on: [FEATURE / BUG / TASK]

Before touching any code:
1. Check git status and current branch
2. Read the relevant files for this task
3. Write a plan (numbered steps) to tasks/todo.md
4. Tell me the plan — I'll approve before you start

Max autonomy after I approve. Commit when done.
```

---

## Quick Reference

| Prompt | Use when |
|--------|----------|
| #2 Session Opener | Start of every session |
| #3 Max Autonomy | Complex multi-step tasks |
| #4 Bug Fix | Errors, regressions |
| #5 Code Review | Before merging anything |
| #6 Architect | Before building a new feature |
| #7 Karpathy Research | Learning something new deeply |
| #10 Reset | Claude is going in circles |
| #13 Incident | Prod is down |
| #14 Self-Improve | After any correction |
| #15 Kickoff | Start of a work session |
