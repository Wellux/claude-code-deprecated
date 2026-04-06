---
name: onboarding
description: >
  Create onboarding documentation for new team members or contributors. Invoke for:
  "onboarding guide", "new developer guide", "contributor guide", "CONTRIBUTING.md",
  "how to get started", "new team member setup", "first day guide".
argument-hint: project or team to create onboarding for
allowed-tools: Read, Write, Glob
---

# Skill: Onboarding — New Developer Guide
**Category:** Documentation

## Role
Create clear onboarding documentation that gets a new developer productive in their first day.

## When to invoke
- New team members joining
- Open source contributors need guidance
- "write CONTRIBUTING.md"

## Instructions
1. Day 1 checklist: repo access, dev environment setup, first PR
2. Architecture overview: 5-minute mental model of the codebase
3. Development workflow: how to branch, test, PR, review, merge
4. Key concepts: domain-specific terms and patterns explained
5. Where to find things: map of the codebase
6. Who to ask: team contacts and their areas

## Output format
```markdown
# Getting Started — <project>
## Prerequisites
## Setup (15 minutes)
## Architecture Overview
## Development Workflow
## Key Concepts
## Where to Find Things
## Who to Ask
## First Task Suggestions
```

## Example
/onboarding create developer onboarding guide for wellux_testprojects project
