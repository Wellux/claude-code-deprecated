---
description: >
  Run the full deployment pipeline: environment check → tests → Docker build →
  container start → health verification → smoke evals. Use for: "deploy",
  "ship it", "deploy to staging", "run the deploy pipeline", "build and deploy".
argument-hint: "[--env local|staging|prod] [--dry-run] [version tag]"
allowed-tools: Bash, Read, Write
---

# /deploy — Full Deploy Pipeline

## What this does
Runs `ccm deploy` which orchestrates: doctor → pytest → docker build → compose up → /health poll → smoke evals.

## Usage
```
/deploy                          # deploy to local (default)
/deploy --dry-run                # dry-run: validate all steps without starting containers
/deploy --env staging            # deploy to staging env
/deploy --skip-tests             # skip pytest (use when tests already passed in CI)
```

## Steps I will execute

### 1. Pre-deploy check
```bash
ccm doctor
```
Validates API key, package imports, paths, skills, git, log writability.
If any check fails: stop and report — do NOT deploy a broken environment.

### 2. Run tests (skip with --skip-tests)
```bash
python -m pytest tests/ -q --tb=short
```
ALL 368 tests must pass. If any fail: stop. Fix the failure before deploying.

### 3. Build Docker image (skip with --skip-build)
```bash
ccm build
```
Builds `ccm-api:latest` and `ccm-api:{version}`. Reports final image size.

### 4. Start containers
```bash
docker compose up -d
```
Starts the API service with resource limits from docker-compose.yml.
Dry-run stops before this step.

### 5. Health check (30s timeout)
```bash
ccm health --url http://localhost:${PORT:-8000}
```
Polls /health every 3s until status=ok or 30s timeout. On timeout: run `docker compose logs api` to diagnose.

### 6. Smoke evals
```bash
ccm eval run data/evals/smoke.jsonl --dry-run
```
Verifies the deployed service handles the 5 smoke cases correctly.

### 7. Summary
Print each step with ✓/✗ status. Exit 0 if all passed, 1 if any failed.

## On failure
- If tests fail: show failing test names, suggest `python -m pytest tests/<file> -v`
- If build fails: show last 20 lines of build output
- If health fails: run `docker compose logs api --tail 50`
- If evals fail: show which cases failed and expected vs. actual

## After successful deploy
Update tasks/todo.md with deployment entry:
```
- [x] Deploy {version} to {env} — {timestamp}
```

## Rollback
If something goes wrong after deploy:
```bash
docker compose down
git stash  # if needed
docker compose up -d  # restart previous image
```
