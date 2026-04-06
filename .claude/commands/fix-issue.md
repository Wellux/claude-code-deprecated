Fix the issue described below (GitHub issue, error message, or bug description).

## Process

### 1. Understand the issue
- Read the full issue/error carefully
- Identify: what is expected? what is actually happening?
- If a GitHub issue number is given, fetch it with `mcp__github__get_issue`

### 2. Reproduce
- Find the failing test or write one that demonstrates the bug
- Run it to confirm the failure: `pytest tests/ -k "<test_name>" --tb=long`
- If no test exists, create one in the appropriate `tests/test_*.py` file

### 3. Diagnose root cause
- Trace the call stack from the error
- Identify the single line or logic branch responsible
- Do NOT fix symptoms — find the root cause

### 4. Fix
- Make the minimal change needed — do not refactor surrounding code
- Apply only in `src/` (never in `tests/` except to add the repro test)
- Check `.claude/rules/code-style.md` before writing any new code

### 5. Verify
```bash
# Run the specific test first
pytest tests/ -k "<test_name>" --tb=short

# Then full suite
pytest --tb=short -q

# Then lint
ruff check src/ tests/ --select E,F,W --ignore E501

# Then smoke evals
python -m src.cli eval run data/evals/smoke.jsonl --dry-run
```

All four must pass before marking the issue fixed.

### 6. Commit
```
fix: <imperative description of what was wrong>

Root cause: <one sentence>
Fix: <one sentence>

Fixes #<issue_number>
```

## Rules
- Never use `--no-verify` to skip hooks
- Never silence an exception to make a test pass
- If the fix requires changing a test, explain why the test was wrong
- If you cannot reproduce the issue, say so — do not guess
