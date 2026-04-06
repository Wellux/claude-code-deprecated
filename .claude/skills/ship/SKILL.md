---
name: ship
description: >
  Full release checklist — tests, lint, security scan, build, deploy, health check, monitor.
  Invoke for: "ship it", "cut a release", "deploy to prod", "land this", "release",
  "push to production", "ship this feature", "ready to deploy", "go live".
  Inspired by gstack (Garry Tan) /ship and /land-and-deploy skills.
argument-hint: what to ship (branch, feature, or version)
allowed-tools: Read, Bash, Glob, Grep, Edit
---

# Skill: Ship — Full Release Pipeline
**Category:** Ecosystem
**Inspired by:** gstack (github.com/garrytan/gstack)

## Role
Act as Release Engineer. Enforce every gate before anything reaches production.
No step is skipped. No corner is cut. Ship with confidence or don't ship.

## When to Invoke
- Feature branch ready to merge
- Cutting a versioned release
- Deploying to staging or production
- "Can we ship this?" checkpoint

## Release Checklist

### Gate 1 — Code Quality
```bash
# All tests pass
pytest tests/ -q --tb=short

# Lint clean
ruff check src/ tests/ --select E,F,W --ignore E501

# Type check (if mypy configured)
mypy src/ --ignore-missing-imports 2>/dev/null || true

# No debug/TODO markers left
grep -rn "TODO\|FIXME\|HACK\|XXX\|breakpoint()\|pdb\|console\.log" src/ || echo "clean"
```

### Gate 2 — Evals
```bash
# Smoke suite (no API key needed)
ccm eval run data/evals/smoke.jsonl --dry-run

# Routing suite
ccm eval run data/evals/routing.jsonl --dry-run
```

### Gate 3 — Security
```bash
# No secrets in staged files
git diff --cached | grep -iE "(api_key|secret|password|token)\s*=" && echo "SECRETS FOUND — abort" || echo "clean"

# Dependency audit (if pip-audit available)
pip-audit 2>/dev/null || echo "pip-audit not installed — skip"
```

### Gate 4 — Build
```bash
# Docker build (if Dockerfile present)
docker build -t ccm:latest . --no-cache

# Or: Python package build
pip install -e ".[dev]" --quiet
ccm --help >/dev/null
```

### Gate 5 — Deploy & Verify
```bash
# Start service
docker compose up -d

# Health check
sleep 3
curl -sf http://localhost:8000/health | python3 -m json.tool

# Smoke test against live service
curl -sf -X POST http://localhost:8000/complete \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Say OK", "auto_route": true}' | python3 -m json.tool
```

### Gate 6 — Commit & Tag
```bash
# Ensure clean working tree
git status

# Create release commit
git add -A
git commit -m "release: <version> — <one-line summary>"

# Tag (semver)
git tag -a v<version> -m "Release v<version>"
git push -u origin <branch> --tags
```

### Gate 7 — Post-Ship
- [ ] Update `CHANGELOG.md` (or run `/changelog`)
- [ ] Update `tasks/todo.md` — mark shipped items complete
- [ ] Monitor logs for 5 minutes post-deploy
- [ ] Notify team / update issue tracker

## Abort Conditions
Any gate failure = **stop and fix before continuing**. Do not skip gates with `--force` flags.
Do not deploy with failing tests. Do not bypass lint with `# noqa` without comment.

## Example
/ship the streaming API endpoint — ready to merge and deploy

## Quick Mode
If only deploying locally for testing (not production):
```bash
pytest tests/ -q && ccm serve --reload
```
