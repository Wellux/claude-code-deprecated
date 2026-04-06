---
name: readme-writer
description: >
  Write or update README.md files that are clear, complete, and developer-friendly.
  Invoke for: "write README", "update README", "docs are outdated", "document this project",
  "README is missing", "improve documentation", "README for this".
argument-hint: project or directory to document
allowed-tools: Read, Write, Glob, Grep
---

# Skill: README Writer — Project Documentation
**Category:** Documentation

## Role
Write clear, comprehensive README.md files that help developers get up and running quickly.

## When to invoke
- New project needs documentation
- README is outdated or incomplete
- "document this project"

## Instructions
1. Read all code to understand what the project actually does
2. Structure: Project Name → What it does → Quick Start → Usage → Configuration → Contributing
3. Quick Start must work: test the installation steps
4. Include: badges (version, status), architecture overview, prerequisites
5. Code examples: show real usage, not toy examples
6. Keep current: check all links work, versions are correct

## Output format
Complete README.md with:
- Badges + title
- One-paragraph what + why
- Prerequisites
- Installation (works on copy-paste)
- Usage examples
- Configuration reference
- Contributing guide

## Example
/readme-writer write comprehensive README for the wellux_testprojects project
