"""EvalRunner — executes an EvalSuite against a callable LLM backend.

Two runners are provided:
    EvalRunner       — synchronous; sequential by default, parallel with max_workers
    AsyncEvalRunner  — async, concurrent (up to `concurrency` parallel calls)
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import time
from collections.abc import Callable, Coroutine
from typing import Any

from .scorers import DEFAULT_SCORER, ScorerFn
from .suite import EvalSuite
from .types import EvalCase, EvalReport, EvalResult, Verdict

# Sync callable: (prompt, *, max_tokens, temperature) -> str
LLMCallable = Callable[..., str]
# Async callable: (prompt, *, max_tokens, temperature) -> Coroutine[Any, Any, str]
AsyncLLMCallable = Callable[..., Coroutine[Any, Any, str]]


class EvalRunner:
    """Synchronous, sequential eval runner.

    Example:
        def my_llm(prompt, *, max_tokens=512, temperature=0.0):
            return client.complete(prompt)

        report = EvalRunner(my_llm).run(suite)
        print(report.summary())
    """

    def __init__(
        self,
        llm: LLMCallable,
        scorer: ScorerFn = DEFAULT_SCORER,
        pass_threshold: float = 0.8,
        verbose: bool = False,
        max_workers: int | None = None,
    ) -> None:
        self.llm = llm
        self.scorer = scorer
        self.pass_threshold = pass_threshold
        self.verbose = verbose
        self.max_workers = max_workers

    def run(self, suite: EvalSuite) -> EvalReport:
        """Run all cases — parallel when max_workers > 1, sequential otherwise."""
        cases = list(suite)
        if self.max_workers and self.max_workers > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                results = list(pool.map(self._run_case, cases))
        else:
            results = [self._run_case(case) for case in cases]
        if self.verbose:
            for result in results:
                _print_result(result)
        return _aggregate(suite.name, results)

    def run_case(self, case: EvalCase) -> EvalResult:
        return self._run_case(case)

    def _run_case(self, case: EvalCase) -> EvalResult:
        t0 = time.monotonic()
        try:
            actual = self.llm(
                case.prompt,
                max_tokens=case.max_tokens,
                temperature=case.temperature,
            )
        except Exception as exc:  # noqa: BLE001
            return EvalResult(
                case_id=case.id,
                verdict=Verdict.ERROR,
                actual="",
                score=0.0,
                reason=f"LLM raised: {exc}",
                latency_ms=(time.monotonic() - t0) * 1000,
                error=str(exc),
                tags=list(case.tags),
            )
        latency_ms = (time.monotonic() - t0) * 1000
        score, reason = self.scorer(actual, case)
        verdict = Verdict.PASS if score >= self.pass_threshold else Verdict.FAIL
        return EvalResult(
            case_id=case.id, verdict=verdict, actual=actual,
            score=score, reason=reason, latency_ms=latency_ms,
            tags=list(case.tags),
        )


class AsyncEvalRunner:
    """Concurrent async eval runner — runs up to `concurrency` cases in parallel.

    The `llm` callable must be an async function:
        async def my_llm(prompt, *, max_tokens=512, temperature=0.0) -> str: ...

    Example:
        runner = AsyncEvalRunner(my_llm, concurrency=5)
        report = await runner.run(suite)
        print(report.summary())
    """

    def __init__(
        self,
        llm: AsyncLLMCallable,
        scorer: ScorerFn = DEFAULT_SCORER,
        pass_threshold: float = 0.8,
        concurrency: int = 5,
        verbose: bool = False,
        case_timeout: float = 30.0,
    ) -> None:
        self.llm = llm
        self.scorer = scorer
        self.pass_threshold = pass_threshold
        self.concurrency = concurrency
        self.verbose = verbose
        self.case_timeout = case_timeout

    async def run(self, suite: EvalSuite) -> EvalReport:
        """Run all cases concurrently (up to `concurrency` at a time)."""
        semaphore = asyncio.Semaphore(self.concurrency)
        tasks = [self._run_case(case, semaphore) for case in suite]
        results = await asyncio.gather(*tasks)
        if self.verbose:
            for r in results:
                _print_result(r)
        return _aggregate(suite.name, list(results))

    async def run_case(self, case: EvalCase) -> EvalResult:
        return await self._run_case(case, asyncio.Semaphore(1))

    async def _run_case(self, case: EvalCase, sem: asyncio.Semaphore) -> EvalResult:
        async with sem:
            t0 = time.monotonic()
            try:
                actual = await asyncio.wait_for(
                    self.llm(
                        case.prompt,
                        max_tokens=case.max_tokens,
                        temperature=case.temperature,
                    ),
                    timeout=self.case_timeout,
                )
            except TimeoutError:
                return EvalResult(
                    case_id=case.id,
                    verdict=Verdict.ERROR,
                    actual="",
                    score=0.0,
                    reason=f"LLM timed out after {self.case_timeout}s",
                    latency_ms=(time.monotonic() - t0) * 1000,
                    error=f"TimeoutError: exceeded {self.case_timeout}s",
                    tags=list(case.tags),
                )
            except Exception as exc:  # noqa: BLE001
                return EvalResult(
                    case_id=case.id,
                    verdict=Verdict.ERROR,
                    actual="",
                    score=0.0,
                    reason=f"LLM raised: {exc}",
                    latency_ms=(time.monotonic() - t0) * 1000,
                    error=str(exc),
                    tags=list(case.tags),
                )
            latency_ms = (time.monotonic() - t0) * 1000
            score, reason = self.scorer(actual, case)
            verdict = Verdict.PASS if score >= self.pass_threshold else Verdict.FAIL
            return EvalResult(
                case_id=case.id, verdict=verdict, actual=actual,
                score=score, reason=reason, latency_ms=latency_ms,
                tags=list(case.tags),
            )


# ── shared helpers ────────────────────────────────────────────────────────────

def _print_result(result: EvalResult) -> None:
    icon = {"pass": "✓", "fail": "✗", "skip": "–", "error": "!"}.get(result.verdict.value, "?")
    print(f"  [{icon}] {result.case_id}: {result.reason[:80]}")


def _aggregate(suite_name: str, results: list[EvalResult]) -> EvalReport:
    counts = {v: 0 for v in Verdict}
    for r in results:
        counts[r.verdict] += 1
    return EvalReport(
        suite_name=suite_name,
        total=len(results),
        passed=counts[Verdict.PASS],
        failed=counts[Verdict.FAIL],
        skipped=counts[Verdict.SKIP],
        errors=counts[Verdict.ERROR],
        results=results,
    )
