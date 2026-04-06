# ADR 0002: Python as Primary Stack

**Status:** Accepted
**Date:** 2026-03-28

## Context

The project needs a language for: LLM API clients, data pipelines, prompt engineering,
and scripting. Candidates: Python, TypeScript, Go.

## Decision

Use **Python 3.12+** as the primary language for all `src/` code.

## Reasons

1. **ML ecosystem** — PyTorch, transformers, sentence-transformers, FAISS all Python-native
2. **Anthropic SDK** — Python SDK is the most mature and feature-complete
3. **Async support** — `asyncio` handles concurrent API calls efficiently
4. **Type hints** — Python 3.12 generics, `X | Y` unions, dataclasses provide sufficient type safety
5. **Tooling** — ruff (lint+format), mypy (types), pytest (testing) cover all needs

## Consequences

- **Positive:** Direct access to all AI/ML libraries; no transpilation needed
- **Negative:** Slower than Go/Rust for CPU-bound work; GIL limits true parallelism
- **Mitigation:** Async I/O eliminates most GIL concerns for API-bound workloads; numpy/torch release GIL

## Key Conventions

- Python ≥ 3.11 (required for `X | Y` union syntax without `from __future__ import annotations`)
- Async-first: all LLM calls use `async def` + `asyncio`
- Type hints everywhere in `src/`; examples can be untyped
- `ruff` for linting + formatting (replaces black + flake8 + isort)
- `pytest-asyncio` for async test support
