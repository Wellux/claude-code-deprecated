"""Tests for src/utils/token_counter.py."""
import pytest

from src.utils.token_counter import (
    count_tokens_approx,
    estimate_cost,
    fits_in_context,
    split_into_chunks,
)


class TestCountTokensApprox:
    def test_empty_string(self):
        assert count_tokens_approx("") == 1  # max(1, 0//4)

    def test_short_text(self):
        # "hello" = 5 chars → 5//4 = 1, max(1,1) = 1
        assert count_tokens_approx("hello") >= 1

    def test_longer_text(self):
        text = "a" * 400
        count = count_tokens_approx(text)
        assert 90 <= count <= 110  # ~100 tokens

    def test_claude_model_uses_claude_ratio(self):
        text = "a" * 380
        count = count_tokens_approx(text, model="claude-sonnet-4-6")
        assert count > 0

    def test_different_models_may_differ(self):
        text = "x" * 1000
        c1 = count_tokens_approx(text, model="claude-sonnet-4-6")
        c2 = count_tokens_approx(text, model="gpt-4o")
        # Both positive, may differ slightly
        assert c1 > 0
        assert c2 > 0


class TestFitsInContext:
    def test_short_text_fits(self):
        assert fits_in_context("hello", "claude-sonnet-4-6", context_limit=10000)

    def test_long_text_doesnt_fit(self):
        text = "a" * 800_000  # ~200k tokens
        assert not fits_in_context(text, "claude-sonnet-4-6", context_limit=1000)


class TestEstimateCost:
    def test_zero_tokens_zero_cost(self):
        assert estimate_cost(0, 0, 3.0, 15.0) == 0.0

    def test_one_million_input_tokens(self):
        cost = estimate_cost(1_000_000, 0, 3.0, 15.0)
        assert cost == pytest.approx(3.0)

    def test_one_million_output_tokens(self):
        cost = estimate_cost(0, 1_000_000, 3.0, 15.0)
        assert cost == pytest.approx(15.0)

    def test_combined(self):
        cost = estimate_cost(1_000_000, 1_000_000, 3.0, 15.0)
        assert cost == pytest.approx(18.0)


class TestSplitIntoChunks:
    def test_short_text_one_chunk(self):
        chunks = split_into_chunks("hello world", max_tokens=1000)
        assert len(chunks) == 1
        assert chunks[0] == "hello world"

    def test_long_text_splits(self):
        text = "a" * 10000
        chunks = split_into_chunks(text, max_tokens=100)
        assert len(chunks) > 1
        assert "".join(chunks) == text  # no data lost

    def test_each_chunk_within_limit(self):
        text = "b" * 10000
        max_tokens = 100
        chunks = split_into_chunks(text, max_tokens=max_tokens)
        for chunk in chunks:
            assert count_tokens_approx(chunk) <= max_tokens + 5  # small tolerance
