---
name: changelog
description: >
  Generate and maintain CHANGELOG.md from git history. Invoke for: "update changelog",
  "what changed", "release notes", "changelog entry", "commit history summary",
  "CHANGELOG", "what's new in this release", "summarize changes since last release".
argument-hint: version range or "since last release" or specific version number
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Skill: Changelog — Generate Release Notes
**Category:** Development

## Role
Generate well-structured CHANGELOG.md entries from git commit history following Keep a Changelog format.

## When to invoke
- Before a release
- "update changelog"
- After a sprint to document what shipped
- "what changed since v1.0?"

## Instructions
1. Run `git log --oneline --since=<date>` or between tags
2. Categorize commits: Added / Changed / Fixed / Removed / Security / Deprecated
3. Write human-readable descriptions (not raw commit messages)
4. Follow Keep a Changelog: https://keepachangelog.com
5. Include breaking changes prominently
6. Update CHANGELOG.md with new version section at top

## Output format
```markdown
## [1.2.0] — 2026-03-28
### Added
- New `/swarm` skill for parallel agent decomposition
- Karpathy research agent with weekly automation

### Fixed
- Claude client retry logic now uses exponential backoff

### Security
- Updated anthropic package to patch CVE-XXXX
```

## Example
/changelog generate notes for v1.1.0 from git log since v1.0.0
