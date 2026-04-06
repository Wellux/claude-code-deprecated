"""Tests for src/evals/ — types, scorers, suite, and runner."""
from __future__ import annotations

import pytest

from src.evals import (
    AsyncEvalRunner,
    EvalCase,
    EvalReport,
    EvalRunner,
    EvalSuite,
    Verdict,
    composite,
    contains_all,
    exact_match,
    excludes_none,
    max_length,
    min_length,
    non_empty,
    regex_match,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

def echo_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    """Returns the prompt unchanged — useful for contains/excludes tests."""
    return prompt


def static_llm(response: str):
    """Factory: always returns the given response."""
    def _llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
        return response
    return _llm


def error_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    raise RuntimeError("API unavailable")


@pytest.fixture
def simple_suite():
    return (
        EvalSuite("test")
        .add(EvalCase("greet", "Say hello", contains=["hello"]))
        .add(EvalCase("math",  "2+2=4", contains=["4"]))
    )


# ── EvalCase ──────────────────────────────────────────────────────────────────

class TestEvalCase:
    def test_minimal(self):
        c = EvalCase("id1", "prompt text")
        assert c.id == "id1"
        assert c.prompt == "prompt text"
        assert c.expected is None
        assert c.contains == []
        assert c.excludes == []
        assert c.tags == []

    def test_defaults(self):
        c = EvalCase("x", "p")
        assert c.max_tokens == 512
        assert c.temperature == 0.0

    def test_empty_id_raises(self):
        with pytest.raises(ValueError, match="id"):
            EvalCase("", "prompt")

    def test_empty_prompt_raises(self):
        with pytest.raises(ValueError, match="prompt"):
            EvalCase("id", "")

    def test_full_construction(self):
        c = EvalCase(
            "c1", "hello", expected="world",
            contains=["foo"], excludes=["bar"],
            tags=["smoke", "fast"], metadata={"author": "test"},
        )
        assert c.expected == "world"
        assert "smoke" in c.tags
        assert c.metadata["author"] == "test"


# ── Scorers ───────────────────────────────────────────────────────────────────

class TestExactMatch:
    def test_match(self):
        c = EvalCase("x", "p", expected="hello world")
        score, _ = exact_match("hello world", c)
        assert score == 1.0

    def test_match_strips_whitespace(self):
        c = EvalCase("x", "p", expected="hello")
        score, _ = exact_match("  hello  ", c)
        assert score == 1.0

    def test_mismatch(self):
        c = EvalCase("x", "p", expected="hello")
        score, _ = exact_match("goodbye", c)
        assert score == 0.0

    def test_no_expected_passes(self):
        c = EvalCase("x", "p")
        score, _ = exact_match("anything", c)
        assert score == 1.0


class TestContainsAll:
    def test_all_present(self):
        c = EvalCase("x", "p", contains=["foo", "bar"])
        score, _ = contains_all("foo and bar here", c)
        assert score == 1.0

    def test_partial_credit(self):
        c = EvalCase("x", "p", contains=["foo", "bar", "baz"])
        score, _ = contains_all("foo and bar", c)
        assert score == pytest.approx(2 / 3)

    def test_none_present(self):
        c = EvalCase("x", "p", contains=["xyz", "abc"])
        score, _ = contains_all("nothing here", c)
        assert score == 0.0

    def test_case_insensitive(self):
        c = EvalCase("x", "p", contains=["Python"])
        score, _ = contains_all("python is great", c)
        assert score == 1.0

    def test_no_constraints_passes(self):
        c = EvalCase("x", "p")
        score, _ = contains_all("anything", c)
        assert score == 1.0


class TestExcludesNone:
    def test_none_present_passes(self):
        c = EvalCase("x", "p", excludes=["bad", "wrong"])
        score, _ = excludes_none("this is good", c)
        assert score == 1.0

    def test_forbidden_present_fails(self):
        c = EvalCase("x", "p", excludes=["error"])
        score, _ = excludes_none("an error occurred", c)
        assert score == 0.0

    def test_case_insensitive(self):
        c = EvalCase("x", "p", excludes=["ERROR"])
        score, _ = excludes_none("error here", c)
        assert score == 0.0

    def test_no_excludes_passes(self):
        c = EvalCase("x", "p")
        score, _ = excludes_none("anything", c)
        assert score == 1.0


class TestNonEmpty:
    def test_non_empty_passes(self):
        c = EvalCase("x", "p")
        score, _ = non_empty("some text", c)
        assert score == 1.0

    def test_empty_fails(self):
        c = EvalCase("x", "p")
        score, _ = non_empty("", c)
        assert score == 0.0

    def test_whitespace_only_fails(self):
        c = EvalCase("x", "p")
        score, _ = non_empty("   ", c)
        assert score == 0.0


class TestMinLength:
    def test_meets_minimum(self):
        c = EvalCase("x", "p")
        scorer = min_length(10)
        score, _ = scorer("hello world", c)
        assert score == 1.0

    def test_below_minimum_partial(self):
        c = EvalCase("x", "p")
        scorer = min_length(20)
        score, _ = scorer("short", c)   # 5 chars → 5/20 = 0.25
        assert score == pytest.approx(0.25)


class TestMaxLength:
    def test_within_max(self):
        c = EvalCase("x", "p")
        scorer = max_length(100)
        score, _ = scorer("short", c)
        assert score == 1.0

    def test_exceeds_max_fails(self):
        c = EvalCase("x", "p")
        scorer = max_length(3)
        score, _ = scorer("toolong", c)
        assert score == 0.0


class TestRegexMatch:
    def test_matches(self):
        c = EvalCase("x", "p")
        scorer = regex_match(r"\d{4}")
        score, _ = scorer("year 2024 was good", c)
        assert score == 1.0

    def test_no_match(self):
        c = EvalCase("x", "p")
        scorer = regex_match(r"\d{4}")
        score, _ = scorer("no numbers here", c)
        assert score == 0.0

    def test_case_insensitive_by_default(self):
        c = EvalCase("x", "p")
        scorer = regex_match(r"python")
        score, _ = scorer("Python is great", c)
        assert score == 1.0


class TestComposite:
    def test_equal_weights(self):
        c = EvalCase("x", "p", contains=["hello"])
        scorer = composite(non_empty, contains_all)
        score, _ = scorer("hello world", c)
        assert score == 1.0

    def test_partial_fail(self):
        c = EvalCase("x", "p", contains=["missing"])
        scorer = composite(non_empty, contains_all)
        score, _ = scorer("hello world", c)
        assert 0.0 < score < 1.0

    def test_custom_weights(self):
        c = EvalCase("x", "p")
        scorer = composite(non_empty, contains_all, weights=[3.0, 1.0])
        score, _ = scorer("something", c)
        assert score == 1.0

    def test_weight_length_mismatch_raises(self):
        with pytest.raises(ValueError):
            composite(non_empty, contains_all, weights=[1.0])


# ── EvalSuite ─────────────────────────────────────────────────────────────────

class TestEvalSuite:
    def test_empty(self):
        s = EvalSuite("test")
        assert len(s) == 0

    def test_add_returns_self(self):
        s = EvalSuite("test")
        result = s.add(EvalCase("a", "prompt"))
        assert result is s

    def test_duplicate_id_raises(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "prompt"))
        with pytest.raises(ValueError, match="Duplicate"):
            s.add(EvalCase("a", "other prompt"))

    def test_extend(self):
        s = EvalSuite("test")
        s.extend([EvalCase("a", "p1"), EvalCase("b", "p2")])
        assert len(s) == 2

    def test_iter(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p")).add(EvalCase("b", "q"))
        ids = [c.id for c in s]
        assert ids == ["a", "b"]

    def test_getitem(self):
        s = EvalSuite("test")
        s.add(EvalCase("alpha", "prompt"))
        assert s["alpha"].id == "alpha"

    def test_getitem_missing_raises(self):
        s = EvalSuite("test")
        with pytest.raises(KeyError):
            _ = s["nonexistent"]

    def test_filter_tags(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p", tags=["smoke"]))
        s.add(EvalCase("b", "p", tags=["slow"]))
        filtered = s.filter_tags("smoke")
        assert len(filtered) == 1
        assert filtered["a"].id == "a"

    def test_filter_ids(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p"))
        s.add(EvalCase("b", "p"))
        s.add(EvalCase("c", "p"))
        filtered = s.filter_ids("a", "c")
        assert len(filtered) == 2

    def test_exclude_tags(self):
        s = EvalSuite("test")
        s.add(EvalCase("a", "p", tags=["skip"]))
        s.add(EvalCase("b", "p", tags=["run"]))
        filtered = s.exclude_tags("skip")
        assert len(filtered) == 1

    def test_jsonl_roundtrip(self, tmp_path):
        s = EvalSuite("round")
        s.add(EvalCase("x", "prompt", contains=["hi"], tags=["t1"]))
        path = s.to_jsonl(tmp_path / "cases.jsonl")
        loaded = EvalSuite.from_jsonl(path)
        assert len(loaded) == 1
        assert loaded["x"].contains == ["hi"]
        assert "t1" in loaded["x"].tags

    def test_from_jsonl_skips_comments(self, tmp_path):
        p = tmp_path / "cases.jsonl"
        p.write_text('# comment\n{"id":"a","prompt":"p","contains":[],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":512,"temperature":0.0}\n')
        s = EvalSuite.from_jsonl(p)
        assert len(s) == 1

    def test_from_jsonl_duplicate_id_raises(self, tmp_path):
        p = tmp_path / "dup.jsonl"
        row = '{"id":"dup","prompt":"p","contains":[],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":512,"temperature":0.0}'
        p.write_text(row + "\n" + row + "\n")
        with pytest.raises(ValueError, match="Duplicate"):
            EvalSuite.from_jsonl(p)


# ── EvalRunner ────────────────────────────────────────────────────────────────

class TestEvalRunner:
    def test_all_pass(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        assert report.passed == 2
        assert report.failed == 0
        assert report.pass_rate == 1.0

    def test_all_fail(self):
        suite = EvalSuite("fail_suite").add(EvalCase("a", "prompt", contains=["MISSING"]))
        runner = EvalRunner(static_llm("no match here"))
        report = runner.run(suite)
        assert report.failed == 1
        assert report.passed == 0

    def test_error_case(self):
        suite = EvalSuite("err").add(EvalCase("e", "prompt"))
        runner = EvalRunner(error_llm)
        report = runner.run(suite)
        assert report.errors == 1
        assert report.results[0].verdict == Verdict.ERROR

    def test_latency_recorded(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        assert all(r.latency_ms >= 0 for r in report.results)

    def test_custom_pass_threshold(self):
        c = EvalCase("a", "prompt", contains=["x", "y", "z"])
        suite = EvalSuite("t").add(c)
        # Only "x" present → score = 1/3 ≈ 0.33
        runner = EvalRunner(static_llm("x only"), pass_threshold=0.3)
        report = runner.run(suite)
        assert report.passed == 1

    def test_run_case_single(self):
        runner = EvalRunner(static_llm("hello"))
        case = EvalCase("a", "p", contains=["hello"])
        result = runner.run_case(case)
        assert result.verdict == Verdict.PASS

    def test_report_summary_format(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        summary = report.summary()
        assert "test" in summary
        assert "passed" in summary

    def test_report_failures_list(self):
        suite = (
            EvalSuite("mix")
            .add(EvalCase("pass1", "hello world", contains=["hello"]))
            .add(EvalCase("fail1", "prompt", contains=["MISSING"]))
        )
        runner = EvalRunner(echo_llm)
        report = runner.run(suite)
        failures = report.failures()
        assert len(failures) == 1
        assert failures[0].case_id == "fail1"

    def test_mean_score(self, simple_suite):
        runner = EvalRunner(echo_llm)
        report = runner.run(simple_suite)
        assert report.mean_score == pytest.approx(1.0)

    def test_verbose_mode(self, simple_suite, capsys):
        runner = EvalRunner(echo_llm, verbose=True)
        runner.run(simple_suite)
        out = capsys.readouterr().out
        assert "greet" in out

    def test_max_workers_parallel_produces_same_results(self, simple_suite):
        sequential = EvalRunner(echo_llm).run(simple_suite)
        parallel = EvalRunner(echo_llm, max_workers=4).run(simple_suite)
        assert parallel.passed == sequential.passed
        assert parallel.total == sequential.total

    def test_max_workers_one_is_sequential(self, simple_suite):
        # max_workers=1 should behave identically to the default sequential path
        report = EvalRunner(echo_llm, max_workers=1).run(simple_suite)
        assert report.passed == report.total

    def test_max_workers_error_propagates(self):
        suite = EvalSuite("err").add(EvalCase("e1", "x", contains=["x"]))
        report = EvalRunner(error_llm, max_workers=2).run(suite)
        assert report.errors == 1


# ── EvalReport ────────────────────────────────────────────────────────────────

class TestEvalReport:
    def test_pass_rate_no_skipped(self):
        report = EvalReport("t", total=4, passed=3, failed=1, skipped=0, errors=0)
        assert report.pass_rate == pytest.approx(0.75)

    def test_pass_rate_with_skipped(self):
        report = EvalReport("t", total=5, passed=3, failed=1, skipped=1, errors=0)
        assert report.pass_rate == pytest.approx(0.75)

    def test_pass_rate_all_skipped(self):
        report = EvalReport("t", total=2, passed=0, failed=0, skipped=2, errors=0)
        assert report.pass_rate == 0.0

    def test_mean_score_empty(self):
        report = EvalReport("t", total=0, passed=0, failed=0, skipped=0, errors=0)
        assert report.mean_score == 0.0

    def test_by_tag_filters_results(self):
        from src.evals.types import EvalResult, Verdict
        r1 = EvalResult(case_id="a", verdict=Verdict.PASS, score=1.0, tags=["fast"])
        r2 = EvalResult(case_id="b", verdict=Verdict.FAIL, score=0.0, tags=["slow"])
        report = EvalReport("t", total=2, passed=1, failed=1, skipped=0, errors=0, results=[r1, r2])
        assert report.by_tag("fast") == [r1]
        assert report.by_tag("slow") == [r2]
        assert report.by_tag("missing") == []


# ── AsyncEvalRunner ───────────────────────────────────────────────────────────

async def async_echo(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    return prompt


async def async_error(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
    raise RuntimeError("async API error")


class TestAsyncEvalRunner:
    async def test_all_pass(self, simple_suite):
        runner = AsyncEvalRunner(async_echo)
        report = await runner.run(simple_suite)
        assert report.passed == 2
        assert report.failed == 0

    async def test_error_case(self):
        suite = EvalSuite("err").add(EvalCase("e", "prompt"))
        runner = AsyncEvalRunner(async_error)
        report = await runner.run(suite)
        assert report.errors == 1
        assert report.results[0].verdict == Verdict.ERROR

    async def test_concurrency_limit(self):
        import asyncio
        active: list[int] = []
        peak: list[int] = []

        async def counting_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            active.append(1)
            peak.append(len(active))
            await asyncio.sleep(0)
            active.pop()
            return prompt

        suite = EvalSuite("conc")
        for i in range(10):
            suite.add(EvalCase(f"c{i}", f"prompt {i}"))

        runner = AsyncEvalRunner(counting_llm, concurrency=3)
        await runner.run(suite)
        assert max(peak) <= 3

    async def test_all_fail(self):
        suite = EvalSuite("f").add(EvalCase("a", "prompt", contains=["MISSING"]))
        runner = AsyncEvalRunner(async_echo)
        report = await runner.run(suite)
        assert report.failed == 1

    async def test_run_case_single(self):
        runner = AsyncEvalRunner(async_echo)
        case = EvalCase("x", "hello world", contains=["hello"])
        result = await runner.run_case(case)
        assert result.verdict == Verdict.PASS

    async def test_latency_recorded(self, simple_suite):
        runner = AsyncEvalRunner(async_echo)
        report = await runner.run(simple_suite)
        assert all(r.latency_ms >= 0 for r in report.results)

    async def test_case_timeout_returns_error(self):
        import asyncio as _asyncio

        async def slow_llm(prompt: str, *, max_tokens: int = 512, temperature: float = 0.0) -> str:
            await _asyncio.sleep(60)
            return prompt

        suite = EvalSuite("timeout").add(EvalCase("slow", "prompt"))
        runner = AsyncEvalRunner(slow_llm, case_timeout=0.05)
        report = await runner.run(suite)
        assert report.errors == 1
        assert "timed out" in report.results[0].reason

    async def test_default_timeout_is_30s(self):
        runner = AsyncEvalRunner(async_echo)
        assert runner.case_timeout == 30.0

    async def test_verbose_mode_prints_results(self, capsys):
        suite = EvalSuite("v").add(EvalCase("a", "hello", contains=["hello"]))
        runner = AsyncEvalRunner(async_echo, verbose=True)
        await runner.run(suite)
        out = capsys.readouterr().out
        assert "a" in out  # result printed for case id "a"


class TestEvalSuiteRepr:
    def test_repr_includes_name_and_count(self):
        suite = EvalSuite("my-suite").add(EvalCase("a", "p")).add(EvalCase("b", "p"))
        assert "my-suite" in repr(suite)
        assert "2" in repr(suite)


# ── ccm eval CLI ──────────────────────────────────────────────────────────────

class TestCLIEval:
    def test_eval_list_no_dir(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "list"])
        assert result == 0
        out = capsys.readouterr().out
        assert "No eval suites" in out

    def test_eval_list_with_suites(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "smoke.jsonl").write_text(
            '{"id":"a","prompt":"p","contains":[],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "list"])
        assert result == 0
        out = capsys.readouterr().out
        assert "smoke.jsonl" in out

    def test_eval_inspect(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        suite_path = evals_dir / "test.jsonl"
        suite_path.write_text(
            '{"id":"case1","prompt":"hello world","contains":["hello"],"excludes":[],"tags":["smoke"],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "inspect", "test.jsonl"])
        assert result == 0
        out = capsys.readouterr().out
        assert "case1" in out
        assert "hello" in out

    def test_eval_run_dry_run(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        suite_path = evals_dir / "smoke.jsonl"
        suite_path.write_text(
            '{"id":"echo1","prompt":"hello world","contains":["hello"],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "run", "smoke.jsonl", "--dry-run"])
        assert result == 0
        out = capsys.readouterr().out
        assert "passed" in out.lower()

    def test_eval_run_missing_suite(self, tmp_path, capsys):
        from unittest.mock import patch

        from src.cli import main
        with patch("src.cli._project_root", return_value=tmp_path):
            result = main(["eval", "run", "nonexistent.jsonl", "--dry-run"])
        assert result == 1

    def test_eval_run_with_json_output(self, tmp_path, capsys):
        import json as _json
        from unittest.mock import patch

        from src.cli import main
        evals_dir = tmp_path / "data" / "evals"
        evals_dir.mkdir(parents=True)
        (evals_dir / "test.jsonl").write_text(
            '{"id":"j1","prompt":"test","contains":["test"],"excludes":[],"tags":[],"metadata":{},"expected":null,"max_tokens":64,"temperature":0.0}\n'
        )
        with patch("src.cli._project_root", return_value=tmp_path):
            main(["eval", "run", "test.jsonl", "--dry-run", "--json"])
        out = capsys.readouterr().out
        # JSON is printed after the summary; find the { start
        json_start = out.find("{")
        data = _json.loads(out[json_start:])
        assert "pass_rate" in data
        assert data["passed"] == 1
