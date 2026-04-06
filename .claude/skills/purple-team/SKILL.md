---
name: purple-team
description: >
  Red-to-blue bridge: validates that detections work against known attack patterns.
  Invoke for: "purple team exercise", "detection validation", "does our monitoring catch
  this attack", "MITRE ATT&CK mapping", "test our defenses", "adversary simulation with
  detection check", "are we detecting this technique".
argument-hint: attack technique or MITRE ATT&CK ID to validate (e.g. "T1059 command execution")
allowed-tools: Read, Grep, Glob, WebSearch
---

# Skill: Purple Team — Detection Validation
**Category:** Security
**Color Team:** Purple

## Role
Bridge red and blue teams: emulate specific attack techniques and verify detection/response coverage.

## When to invoke
- "purple team exercise" for a specific technique
- Validating SIEM rules or WAF rules actually work
- MITRE ATT&CK coverage assessment
- After adding new detection rules

## Instructions
1. Select attack technique (from argument or MITRE ATT&CK)
2. Describe exactly how the attack would manifest in logs/traffic
3. Check existing detection rules (SIEM, WAF, IDS) against the attack pattern
4. Identify detection gaps: what would be missed?
5. Recommend: new rules, log sources, or monitoring improvements
6. Document: technique → expected log → detection rule → coverage status

## Output format
```
## Purple Team — <technique> — <date>
### Technique: <MITRE ID> <Name>
### Attack Simulation
### Detection Coverage: DETECTED / PARTIAL / MISSED
### Gaps Found
### Recommended Rules
```

## Example
/purple-team T1078 Valid Accounts — credential stuffing detection
