# Product Requirements Document
# Claude Code Max — Gold-Standard AI Development Template

**Version:** 1.0.7
**Date:** 2026-04-06
**Status:** SHIPPED
**Owner:** Claude Code Max Project

---

## 1. Vision

Build the definitive Claude Code project template that any developer can clone and immediately have:
- Maximum autonomy with safety guardrails
- 123 specialized skills auto-invoked by context
- Karpathy-style autonomous research loop
- Ralph Loop self-driving development agent
- Self-improvement system that gets smarter over time
- Production-quality Python AI stack

---

## 2. Goals

| Goal | Metric | Status |
|------|--------|--------|
| 123 skills with proper frontmatter | `ls .claude/skills/ \| wc -l ≥ 123` | ✅ Done |
| All hooks wired and functional | `bash .claude/hooks/session-start.sh` exits 0 | ✅ Done |
| Max autonomy settings | settings.json has broad allow list | ✅ Done |
| Research loop runs autonomously | `bash tools/scripts/research-agent.sh` succeeds | ✅ Done |
| Ralph Loop agent defined | `.claude/agents/ralph-loop.md` exists | ✅ Done |
| Python stack complete | All src/ modules importable | ✅ Done |
| MASTER_PLAN loopable | "f" → next step executes | ✅ Done |
| Auto-boot on session start | session-start.sh shows context | ✅ Done |
| Self-improvement loop | lessons.md updated after corrections | ✅ Done |

---

## 3. Non-Goals

- NOT a production application (this is a template/harness)
- NOT language-specific (Python stack is illustrative, not mandatory)
- NOT a replacement for actual project CLAUDE.md files
- NOT tied to any specific cloud provider

---

## 4. Architecture

### 5-Layer System
```
L1: CLAUDE.md + .claude/SOUL.md + USER.md  → Persistent context + agent identity
L2: .claude/skills/  → 123 auto-invoked knowledge packs
L3: .claude/hooks/   → 5 deterministic safety/automation gates
L4: .claude/agents/  → 4 autonomous subagent definitions
L5: .claude/rules/   → Modular instruction files (code-style, testing, api-conventions)
```

### Memory Hierarchy
```
~/.claude/CLAUDE.md  → Global (all projects)
./CLAUDE.md          → Project (this file, shared via git)
./src/*/CLAUDE.md    → Subfolder (scoped context)
```

### Data Flow
```
User "f" → read MASTER_PLAN.md next step → execute → check off → update progress
User "r" → research-agent.sh → WebSearch → distill → data/research/ → lessons.md
```

---

## 5. Skill Categories

| Category | Count | Key Skills |
|----------|-------|------------|
| Meta | 2 | /create, /swarm |
| Security | 16 | /ciso (orchestrator), /pen-tester, /appsec-engineer |
| Development | 20 | /code-review, /debug, /architect, /test-writer |
| AI/ML Research | 15 | /karpathy-researcher, /rag-builder, /prompt-engineer |
| DevOps/Infra | 15 | /ci-cd, /docker, /terraform, /monitoring |
| Documentation | 10 | /readme-writer, /adr-writer, /runbook-creator |
| Optimization | 15 | /web-vitals, /bundle-analyzer, /query-optimizer |
| Project Management | 9 | /sprint-planner, /roadmap, /risk-assessor |
| Ecosystem | 5 | /gsd, /mem, /ui-ux, /superpowers, /obsidian |
| **Total** | **107** | |

---

## 6. Hook Specifications

| Hook | Trigger | Exit 0 | Exit 2 |
|------|---------|--------|--------|
| session-start.sh | Session opens | Show boot context | N/A |
| pre-tool-bash.sh | Before Bash | Log + allow | Dangerous pattern |
| post-tool-edit.sh | After Edit/Write | Lint + validate | N/A (never block) |
| stop.sh | Session ends | Show checklist | N/A |

---

## 7. Success Metrics

- [ ] `ls .claude/skills/ | wc -l` → ≥ 105
- [ ] `python3 -m json.tool .claude/settings.json` → valid JSON
- [ ] All .sh files have `chmod +x`
- [ ] `bash .claude/hooks/session-start.sh` runs without error
- [ ] `git branch --show-current` → `claude/optimize-cli-autonomy-xNamK`
- [ ] `grep "^- \[ \]" MASTER_PLAN.md | wc -l` → 0 (all steps done)

---

## 8. Open Questions

1. Which MCP servers to add by default? (GitHub is essential; Notion/Slack optional)
2. Cron scheduling: use crontab or a dedicated schedule skill?
3. Ralph Loop rate limiting: 100 calls/hr or configurable?
4. LightRAG integration: standalone service or embedded in rag-builder skill?
5. Global ~/.claude/CLAUDE.md: write once or managed per-user?
