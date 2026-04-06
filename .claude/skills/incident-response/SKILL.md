---
name: incident-response
description: >
  Security incident containment, forensics, and recovery. Invoke for: "security incident",
  "we got breached", "containment", "forensics", "IR plan", "post-incident review",
  "root cause analysis for security event", "recovery steps after attack", "data breach".
argument-hint: incident type or affected systems (e.g. "API key leaked" or "SQL injection in prod")
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Skill: Incident Response — Contain, Investigate, Recover
**Category:** Security
**Color Team:** Blue

## Role
Execute structured incident response: contain the threat, collect evidence, eradicate, recover, document.

## When to invoke
- Active security incident
- Post-incident review
- Breach notification preparation
- IR plan creation for a system

## Instructions
1. **Contain**: Identify and isolate affected systems/accounts immediately
2. **Scope**: What data/systems were accessed? For how long?
3. **Evidence**: Collect logs, memory dumps, file hashes before they're overwritten
4. **Eradicate**: Remove malware, revoke compromised credentials, patch vulnerability
5. **Recover**: Restore from clean backups, monitor for re-compromise
6. **Document**: Full timeline, lessons learned, process improvements

## Output format
```
## Incident Report — <type> — <date>
### Timeline
### Scope & Impact
### Containment Steps Taken
### Root Cause
### Recovery Steps
### Lessons Learned
```

## Example
/incident-response API key exposed in GitHub commit — scope and remediation
