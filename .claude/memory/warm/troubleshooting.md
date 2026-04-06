# Warm Memory: Troubleshooting
<!-- L1: known issues, gotchas, workarounds — what bit us and how to fix it -->

**Last Updated**: 2026-04-05

---

## Edit Tool: "String not found" on stale reads

**Symptom**: `Edit` fails with `String to replace not found in file`
**Root cause**: File changed between the last `Read` and the `Edit` call (another tool, hook, or background agent modified it)
**Fix**: Always `Read` immediately before `Edit`. Keep the match string small and unique — large blocks drift.
**Prevention**: Never batch a Read + multiple Edits without re-reading between them if anything could change the file.

---

## Editable Install: `ImportError: No module named 'src'`

**Symptom**: `ccm` or `python3 -m src.cli` fails with `ModuleNotFoundError`
**Root cause**: `.pth` file from `pip install -e .` added `/home/user/wellux_testprojects/src` instead of the project root
**Fix**: In `pyproject.toml`, set `[tool.setuptools.packages.find] where = ["."] include = ["src*"]`
**Also check**: `build-backend = "setuptools.build_meta"` (not `setuptools.backends.legacy:build`)

---

## Logger: JSON serialize crash on exc_info

**Symptom**: `TypeError: Object of type type is not JSON serializable` in structured logger
**Root cause**: `_STDLIB_KEYS` was seeded only from `LogRecord.__dict__` (class-level). Instance attrs like `exc_info` (set at runtime) bypassed the filter and hit `json.dumps` as raw `(type, value, traceback)` tuples.
**Fix**: `_STDLIB_KEYS = frozenset(LogRecord("", INFO, "", 0, "", (), None).__dict__.keys()) | frozenset(LogRecord.__dict__.keys())`
**File**: `src/utils/logger.py:_STDLIB_KEYS`

---

## Duplicate Trigger Phrases in Skill Registry

**Symptom**: `test_no_duplicate_trigger_phrases` fails
**Root cause**: Two skill entries share an identical trigger string — the second silently shadows the first
**Fix**: Find the duplicate with `python3 -c "from src.routing.skill_router import _SKILL_REGISTRY; seen={}; [print(t, e['skill']) for e in _SKILL_REGISTRY for t in e['triggers'] if (t in seen) and seen[t]!=e['skill'] or seen.update({t:e['skill']}) and False]"` and remove from the lower-priority skill

---

## setuptools.backends Missing

**Symptom**: `ModuleNotFoundError: No module named 'setuptools.backends'` during `pip install -e .`
**Root cause**: `setuptools<68` doesn't have the `backends` subpackage; `setuptools.backends.legacy:build` was introduced in 68+ but inconsistently available
**Fix**: Use `build-backend = "setuptools.build_meta"` — this is the stable, always-available alias

---

## ContextVar Leaking Across Requests

**Symptom**: Request IDs bleed between concurrent requests; `X-Request-ID` header has wrong value
**Root cause**: `ContextVar.reset(token)` not called in `finally` — if an exception occurs mid-handler, the context var is never reset
**Fix**: Wrap reset in `finally`:
```python
token = _request_id_var.set(request_id)
try:
    response = await call_next(request)
finally:
    _request_id_var.reset(token)
```
**File**: `src/api/middleware.py`

---

## EvalResult Positional Arg Mismatch

**Symptom**: Tests pass wrong values — e.g., `tags` field gets the `latency_ms` value
**Root cause**: `EvalResult(case_id, verdict, actual, score, latency_ms, tags)` — positional order is easy to get wrong
**Fix**: Always use keyword args: `EvalResult(case_id="a", verdict=Verdict.PASS, score=1.0, tags=["fast"])`

---

## Ruff F841 on Test Helper Variables

**Symptom**: `F841 Local variable 'mem' is assigned to but never used` in tests
**Root cause**: Creating an object just to trigger its side effects (e.g., dir creation) then checking the dirs
**Fix**: Drop the variable assignment: `TieredMemory(base=tmp_path)` (no assignment) — side effects still happen
