"""Eval framework — test LLM outputs systematically.

Quick start:
    from src.evals import EvalCase, EvalSuite, EvalRunner

    suite = (
        EvalSuite("smoke")
        .add(EvalCase("greet", "Say hello", contains=["hello"]))
        .add(EvalCase("math",  "What is 2+2?", contains=["4"]))
    )

    def my_llm(prompt, *, max_tokens=512, temperature=0.0):
        return client.complete(prompt)

    report = EvalRunner(my_llm).run(suite)
    print(report.summary())
"""
from .runner import AsyncEvalRunner, EvalRunner
from .scorers import (
    DEFAULT_SCORER,
    composite,
    contains_all,
    exact_match,
    excludes_none,
    max_length,
    min_length,
    non_empty,
    regex_match,
)
from .suite import EvalSuite
from .types import EvalCase, EvalReport, EvalResult, Verdict

__all__ = [
    # types
    "EvalCase", "EvalResult", "EvalReport", "Verdict",
    # suite
    "EvalSuite",
    # runner
    "EvalRunner", "AsyncEvalRunner",
    # scorers
    "DEFAULT_SCORER", "exact_match", "contains_all", "excludes_none",
    "non_empty", "min_length", "max_length", "regex_match", "composite",
]
