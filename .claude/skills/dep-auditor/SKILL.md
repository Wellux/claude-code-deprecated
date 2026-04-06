---
name: dep-auditor
description: >
  Audit dependencies for vulnerabilities, license issues, and outdated packages. Invoke for:
  "dependency audit", "npm audit", "pip audit", "outdated packages", "CVE check",
  "license compliance", "supply chain security", "vulnerable dependency", "update packages".
argument-hint: requirements.txt, package.json, or project path
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Skill: Dependency Auditor — Supply Chain Security
**Category:** Development

## Role
Audit all project dependencies for known CVEs, license compliance issues, and outdated versions.

## When to invoke
- Regular security maintenance
- Before production deployment
- "any vulnerable dependencies"
- Supply chain security review

## Instructions
1. Read requirements.txt / package.json / pyproject.toml
2. Check for known CVEs in current versions (use WebSearch for NIST NVD)
3. Identify outdated packages (major version behind)
4. Check license compatibility: GPL? AGPL? Copyleft issues?
5. Flag: unpinned versions, packages with no recent updates (abandoned), forks
6. Produce upgrade plan with risk assessment

## Output format
```
## Dependency Audit — <date>
### Critical CVEs (patch immediately)
- package@x.x.x — CVE-XXXX-XXXX — upgrade to x.x.x
### Outdated (upgrade soon)
### License Issues
### Recommendations
```

## Example
/dep-auditor requirements.txt — check for CVEs and outdated packages
