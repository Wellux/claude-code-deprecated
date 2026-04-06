---
name: changelog-maintainer
description: >
  Maintain and update the project CHANGELOG.md keeping it current. Invoke for:
  "keep changelog updated", "CHANGELOG is stale", "changelog maintenance",
  "update release history", "automate changelog", "add to changelog".
argument-hint: version or changes to add to changelog
allowed-tools: Read, Write, Edit, Bash
---

# Skill: Changelog Maintainer — Keep History Current
**Category:** Documentation

## Role
Keep CHANGELOG.md accurate, current, and following Keep a Changelog conventions.

## When to invoke
- After merging significant PRs
- Before a release
- "CHANGELOG is out of date"

## Instructions
1. Check git log since last changelog entry
2. Categorize: Added, Changed, Fixed, Removed, Security, Deprecated
3. Write human-readable entries (not raw commit messages)
4. Add [Unreleased] section if not present
5. When releasing: move Unreleased → [version] with date
6. Keep format consistent with existing entries

## Output format
```markdown
## [Unreleased]
### Added
- New feature X

## [1.1.0] — 2026-03-20
### Fixed
- Bug in Y
```

## Example
/changelog-maintainer update CHANGELOG.md with changes since v1.0.0
