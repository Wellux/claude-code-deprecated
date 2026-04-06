---
name: team
description: >
  Activate preset agent teams for parallel multi-role execution. Invoke for:
  "team mode", "spawn a team", "agent team", "parallel team review", "multi-agent team",
  "code review team", "security team", "debug team", "architecture team", "ship team",
  "team of agents", "multi-agent review". Presets: code-review, security, debug, architect,
  ship, research, onboarding. Inspired by wshobson/agents Agent Teams plugin.
argument-hint: team preset name or description of what team to assemble
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
---

# Skill: Team — Preset Multi-Agent Teams

## Role
Assemble and coordinate preset teams of specialized agents for parallel, multi-perspective
execution of complex tasks. Each team member brings a different lens; the orchestrator
synthesizes findings into a unified recommendation.

## Available Teams

### `code-review` team
| Agent | Role | Focus |
|-------|------|-------|
| Correctness Reviewer | Senior Engineer | Logic errors, edge cases, race conditions |
| Style Reviewer | Code Quality | Naming, structure, readability, DRY |
| Security Reviewer | AppSec | OWASP Top 10, injection, auth, secrets |
| Test Reviewer | QA Engineer | Coverage gaps, test quality, missing cases |
| Performance Reviewer | Perf Eng | Algorithmic complexity, hot paths, memory |

### `security` team
| Agent | Role | Focus |
|-------|------|-------|
| AppSec | OWASP audit | Input validation, auth, XSS, SQLi |
| PenTester | Red team | Attack surface, exploitation paths |
| IAM Reviewer | Access control | Permissions, secrets, least privilege |
| Supply Chain | Dep auditor | CVEs, license issues, dependency risks |

### `debug` team
| Agent | Role | Focus |
|-------|------|-------|
| Root Cause Analyst | Senior Eng | Trace the failure to its origin |
| Hypothesis Generator | Scientist | Generate 5 alternative explanations |
| Test Case Designer | QA | Reproduce the bug in a minimal test |
| Fix Validator | Reviewer | Verify the fix doesn't break other paths |

### `architect` team
| Agent | Role | Focus |
|-------|------|-------|
| Systems Designer | Architect | Component design, data flow |
| Scalability Analyst | Infra | Performance, capacity, bottlenecks |
| Security Architect | SecEng | Threat model, trust boundaries |
| Pragmatist | Senior Dev | Complexity, maintainability, time-to-build |

### `ship` team (from gstack)
| Agent | Role | Focus |
|-------|------|-------|
| Test Runner | QA | All tests passing? |
| Lint Enforcer | CI | Lint clean? |
| Security Scanner | SecOps | No secrets, no vulnerabilities |
| Deploy Validator | DevOps | Health checks, rollback plan |
| Release Chronicler | PM | CHANGELOG updated? Version tagged? |

### `research` team (Karpathy-style)
| Agent | Role | Focus |
|-------|------|-------|
| Paper Miner | Researcher | Find relevant papers and repos |
| First-Principles Distiller | Theorist | Reduce to fundamental concepts |
| Implementation Sketcher | Engineer | Minimal working prototype idea |
| Skeptic | Critic | What's wrong with this approach? |

## Instructions

1. **Parse the request**: identify which preset team fits (or design a custom team)
2. **Define shared context**: what all agents need to know upfront
3. **Spawn agents in parallel** with isolated context windows
4. **Collect outputs**: each agent returns findings in standard format
5. **Synthesize**: orchestrator merges findings, surfaces conflicts, writes final recommendation
6. **Decision**: ranked action list with owner and urgency

## Output Format

```
## Team: <preset> on <target>

### Agent Assignments
- Agent 1 (Role): [brief mission]
- Agent 2 (Role): [brief mission]
...

### Findings
**[Agent 1]**: <key finding>
**[Agent 2]**: <key finding>

### Synthesis
[Where agents agree / where they conflict]

### Recommendations (ranked)
1. [Critical] Fix X — owner: security
2. [High] Refactor Y — owner: correctness
3. [Medium] Add test for Z — owner: test
```
