# Runbook: Deploy

## Prerequisites
- Docker installed
- `ANTHROPIC_API_KEY` set in environment
- Git on branch `claude/optimize-cli-autonomy-xNamK` (or main after merge)

## Steps

### 1. Validate before deploy
```bash
# Syntax check
find src/ -name "*.py" | xargs python3 -m py_compile
python3 -m json.tool .claude/settings.json

# Tests (if configured)
pytest tests/ -v --tb=short 2>/dev/null || echo "No tests yet"

# Security scan
bash tools/scripts/security-scan.sh
```

### 2. Build Docker image
```bash
docker build -t claude-code-max:$(git rev-parse --short HEAD) .
docker tag claude-code-max:$(git rev-parse --short HEAD) claude-code-max:latest
```

### 3. Run locally
```bash
docker run --rm \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -v "$(pwd)/data:/app/data" \
  claude-code-max:latest
```

### 4. Git tag + push
```bash
git tag v$(date +%Y%m%d)-$(git rev-parse --short HEAD)
git push origin --tags
```

## Rollback
See `docs/runbooks/rollback.md`.

## Verification
- Check `data/outputs/` for recent run artifacts
- Review `data/cache/bash-log.txt` for hook activity
- Confirm no secrets in `docker inspect` environment
