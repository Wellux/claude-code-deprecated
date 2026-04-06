# Runbook: Incident Response

## Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| P0 | Complete outage | Immediate | API key invalid, 100% error rate |
| P1 | Major degradation | 15 min | Rate limit, >50% errors |
| P2 | Partial issue | 1 hour | Slow responses, cache miss spike |
| P3 | Minor issue | Next business day | Log noise, stale docs |

## P0/P1 Response

### 1. Triage (5 min)
```bash
# Check API connectivity
curl -s https://api.anthropic.com/v1/health -H "x-api-key: $ANTHROPIC_API_KEY" | python3 -m json.tool

# Check error logs
tail -100 data/cache/bash-log.txt | grep ERROR

# Check rate limit status
grep "rate_limit" data/cache/bash-log.txt | tail -20
```

### 2. Mitigate (10 min)
```bash
# API key invalid → rotate immediately
export ANTHROPIC_API_KEY="new-key"

# Rate limit → reduce RPM
# Edit src/llm/claude_client.py: RateLimiter(requests_per_minute=50)

# Fallback to GPT if Claude is down
# Edit code to use GPTClient as primary temporarily
```

### 3. Resolve & Document
- Fix root cause (not just symptoms)
- Add entry to `tasks/lessons.md` under `## Incident <date>`
- Add monitoring/alerting to prevent recurrence

## Common Incidents

### "anthropic.AuthenticationError"
1. Check `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`
2. Verify key is valid in Anthropic console
3. Check `.env` is not committed/corrupted

### "Rate limit exceeded"
1. Check current RPM setting in `ClaudeClient`
2. Add delays between batch requests
3. Use `ResponseCache` to avoid repeat calls
4. Consider upgrading API tier

### "context_length_exceeded"
1. Check prompt size: `ClaudeClient.count_tokens(prompt)`
2. Use `truncate_to_tokens()` from `src/llm/utils.py`
3. Switch to chunked processing via `split_into_chunks()`

### Hook blocking all Bash commands
1. Check `.claude/hooks/pre-tool-bash.sh` for false positive patterns
2. Temporarily disable: remove hook from `settings.json` PreToolUse
3. Fix pattern and re-enable
