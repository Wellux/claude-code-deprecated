# Runbook: Rollback

## When to use
- Deploy broke something in production
- Regression introduced in latest commit
- Config change caused unexpected behavior

## Steps

### 1. Identify last good commit
```bash
git log --oneline -10
# Find the last commit that worked
```

### 2. Revert to last good state (non-destructive)
```bash
GOOD_COMMIT=<sha>
git revert HEAD...$GOOD_COMMIT --no-edit
git push origin HEAD
```

### 3. If Docker container needs immediate rollback
```bash
# Run previous tagged image
PREV_TAG=$(docker images claude-code-max --format "{{.Tag}}" | grep -v latest | head -2 | tail -1)
docker run --rm \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -v "$(pwd)/data:/app/data" \
  claude-code-max:$PREV_TAG
```

### 4. Emergency: hard reset (only if commits not pushed)
```bash
# DESTRUCTIVE — only use for local-only commits
git reset --hard <good-sha>
```

## Post-rollback
1. Document what went wrong in `tasks/lessons.md`
2. Add a test case that would have caught the regression
3. Create a new branch to fix the root cause properly
