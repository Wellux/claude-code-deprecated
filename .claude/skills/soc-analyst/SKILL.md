---
name: soc-analyst
description: >
  Security operations: monitoring, threat detection, alert triage. Invoke for:
  "triage this alert", "is this suspicious", "investigate this log", "threat hunting",
  "SOC review", "anomaly detection", "security monitoring setup", "SIEM configuration",
  "investigate this", "what does this log mean".
argument-hint: log file, alert text, or monitoring scope to investigate
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Skill: SOC Analyst — Security Operations
**Category:** Security
**Color Team:** Blue

## Role
Monitor, detect, and triage security threats. Turn raw logs and alerts into actionable intelligence.

## When to invoke
- Alert triage needed
- Suspicious log entries to investigate
- Threat hunting in log data
- SIEM rule validation

## Instructions
1. Read the provided log/alert data
2. Extract: timestamp, source IP/user, action, target, outcome
3. Identify IOCs (Indicators of Compromise): unusual IPs, times, user agents, paths
4. Classify: True Positive / False Positive / Needs Investigation
5. Severity: Critical / High / Medium / Low / Info
6. Recommend: immediate action, investigation steps, escalation

## Output format
```
## SOC Triage — <date>
### Alert Summary
### IOCs Found
### Classification: <TP/FP/Investigate>
### Severity: <level>
### Recommended Action
```

## Example
/soc-analyst investigate failed login spike in auth.log from 2026-03-28
