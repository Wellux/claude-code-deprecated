Review the code changes in this session (or the files/PR specified).

## What to review

If a PR number or file list is given, review that. Otherwise review all staged and unstaged changes (`git diff HEAD`).

## Review checklist

Go through each changed file and check:

### Correctness
- [ ] Logic is correct — trace through edge cases mentally
- [ ] No off-by-one errors, null-pointer risks, or unhandled exceptions
- [ ] Async code: no missing `await`, no fire-and-forget without error handling
- [ ] Any new public function has a test

### Code style (see `.claude/rules/code-style.md`)
- [ ] Naming follows conventions (snake_case, PascalCase, UPPER_CONST)
- [ ] No ambiguous single-letter names (`l`, `O`, `I`)
- [ ] No unused imports or variables
- [ ] f-strings only where there are actual placeholders
- [ ] Imports at top of file (no mid-module imports unless lazy-loading)

### Tests (see `.claude/rules/testing.md`)
- [ ] New behaviour has unit tests
- [ ] Edge cases tested (empty input, None, error paths)
- [ ] No test logic in `src/`
- [ ] `pytest --tb=short -q` passes

### Security
- [ ] No secrets or API keys in code
- [ ] No `eval()`, `exec()`, or shell injection risks
- [ ] External inputs are validated before use
- [ ] No `except:` bare catches that swallow errors silently

### API changes (if applicable, see `.claude/rules/api-conventions.md`)
- [ ] Response model updated in `src/api/models.py`
- [ ] `X-Request-ID` flows through to new endpoints
- [ ] Errors raise `HTTPException` with appropriate status codes

## Output format

For each file, output:

```
FILE: src/foo/bar.py
  ✓ Looks good — [brief reason]
  ⚠ [issue description] — line N — [suggested fix]
  ✗ [blocking issue] — line N — [required change]
```

Summarise at the end:
- Total files reviewed
- Blocking issues (✗) that must be fixed before merge
- Warnings (⚠) that should be addressed
- Verdict: APPROVE / REQUEST CHANGES
