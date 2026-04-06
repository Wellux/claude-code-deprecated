# src/evals — Evaluation Framework Context

## Purpose
Structured LLM evaluation: define cases, run suites, report pass rates, latency, and scores.

## Key Classes
- `EvalCase(id, prompt, contains=[], not_contains=[], tags=[])` — single test case
- `EvalSuite(name)` — collection of cases; `.add(case)` enforces no duplicate IDs
- `EvalRunner(llm_fn, max_workers=None)` — sync runner; sequential by default, parallel via `ThreadPoolExecutor` when `max_workers > 1`
- `AsyncEvalRunner(llm_fn, concurrency=5)` — async runner with semaphore + 30s timeout per case
- `EvalReport` — `.summary()`, `.pass_rate`, `.mean_score`, `.by_tag(tag)`
- `Verdict` — `PASS | FAIL | ERROR`

## Running evals
```bash
ccm eval run data/evals/smoke.jsonl           # live (requires ANTHROPIC_API_KEY)
ccm eval run data/evals/smoke.jsonl --dry-run # skip LLM calls, always PASS
ccm eval list                                  # list all .jsonl suites
ccm eval inspect data/evals/smoke.jsonl        # show cases
```

## JSONL format
```json
{"id": "greet", "prompt": "Say hello", "contains": ["hello"], "tags": ["fast"]}
```

## Key invariants
- `EvalSuite.from_jsonl` uses `.extend(cases)` (calls `.add()` for each) — duplicate ID check enforced
- `AsyncEvalRunner` wraps every LLM call in `asyncio.wait_for(..., timeout=30.0)` — no hung awaits
- Use keyword args for `EvalResult` construction — positional order is error-prone

## Tests
`tests/test_evals.py` — covers happy path, tag filtering, duplicate ID rejection, async timeout, verbose mode
