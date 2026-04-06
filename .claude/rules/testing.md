# Testing Rules

Defines how tests should be written in this project.

## Framework
- pytest + pytest-asyncio (asyncio_mode = auto)
- Tests live in `tests/test_<module>.py` mirroring `src/<module>.py`
- No test logic in `src/`

## Structure
- Group tests in classes: `class TestClassName:` → `def test_<behaviour>(self):`
- One assertion focus per test — test one thing
- Fixture scope: `function` default; `module` only for expensive read-only setup
- Name tests as: `test_<what>_<when_condition>` or `test_<what>_<expected_result>`

## Coverage Requirements
- New code must ship with tests covering the happy path + at least one failure case
- Public API methods: 100% coverage expected
- Never mark code `# pragma: no cover` without a comment explaining why

## Mocking
- Mock at the boundary (LLM calls, HTTP, filesystem) — not inside your own code
- Use `unittest.mock.patch` or `monkeypatch` fixture
- Async mocks: `unittest.mock.AsyncMock`
- Inject dependencies via constructor args to make them easily mockable

## Async Tests
- All async tests auto-detected via `asyncio_mode = auto` in pytest.ini
- No `@pytest.mark.asyncio` decorator needed
- Use `asyncio.sleep(0)` to yield control in concurrency tests

## Eval Tests
- Behavioural tests go in `data/evals/*.jsonl`, not in pytest
- `ccm eval run data/evals/smoke.jsonl --dry-run` must always pass in CI
- Live API eval suites tagged `live` are excluded from CI (require ANTHROPIC_API_KEY)

## What Not to Test
- Private implementation details (prefix `_`)
- Third-party library behaviour
- Framework internals (FastAPI routing, Pydantic serialization)
- Trivial one-liners with no branching logic

## CI Gate
- All tests must pass before merge: `pytest tests/ --tb=short -q`
- Lint must pass: `ruff check src/ tests/ --select E,F,W --ignore E501`
- Smoke evals must pass: `python -m src.cli eval run data/evals/smoke.jsonl --dry-run`
