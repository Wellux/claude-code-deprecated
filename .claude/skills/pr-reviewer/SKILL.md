---
name: pr-reviewer
description: >
  Review pull requests: code quality, design, tests, security. Invoke for: "review PR",
  "PR feedback", "pull request review", "diff review", "code change review",
  "should I merge this", "LGTM check".
argument-hint: PR number, diff, or branch to review
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: PR Reviewer — Pull Request Review
**Category:** Development

## Role
Provide thorough pull request reviews covering code quality, correctness, design, tests, security, and documentation.

## When to invoke
- Pre-merge review
- "review this PR" / "is this ready to merge"
- Code change audit

## Instructions
1. Read the PR diff / changed files
2. Understand: what is this PR trying to do? Is it the right approach?
3. Check correctness: does it do what it says? Edge cases handled?
4. Check tests: are new tests added? Coverage maintained?
5. Check security: any new vulnerabilities introduced?
6. Check style: follows conventions? Good naming?
7. Verdict: APPROVE / REQUEST_CHANGES / COMMENT

## Output format
```
## PR Review — <title> — <date>
### Summary
### Blocking Issues 🔴
- file.py:34 — must fix before merge
### Suggestions 🟡
- file.py:12 — consider renaming for clarity
### Approved Changes 🟢
### Verdict: APPROVE / REQUEST CHANGES
```

## Example
/pr-reviewer review changes in src/llm/ for the new streaming response feature
