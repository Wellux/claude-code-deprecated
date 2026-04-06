"""Tests for src/utils/cache.py — ResponseCache hit/miss/TTL/eviction."""
import time

from src.llm.base import CompletionRequest, CompletionResponse
from src.utils.cache import ResponseCache, _cache_key


def make_request(**kwargs) -> CompletionRequest:
    defaults = dict(prompt="test", system=None, model=None, max_tokens=4096, temperature=0.7)
    defaults.update(kwargs)
    return CompletionRequest(**defaults)


def make_response(content="answer") -> CompletionResponse:
    return CompletionResponse(
        content=content, model="claude-sonnet-4-6",
        input_tokens=10, output_tokens=5, stop_reason="end_turn",
    )


class TestCacheKey:
    def test_same_request_same_key(self):
        r1 = make_request(prompt="hello")
        r2 = make_request(prompt="hello")
        assert _cache_key(r1) == _cache_key(r2)

    def test_different_prompt_different_key(self):
        assert _cache_key(make_request(prompt="a")) != _cache_key(make_request(prompt="b"))

    def test_different_temperature_different_key(self):
        assert _cache_key(make_request(temperature=0.0)) != _cache_key(make_request(temperature=1.0))

    def test_different_model_different_key(self):
        assert _cache_key(make_request(model="opus")) != _cache_key(make_request(model="haiku"))


class TestResponseCache:
    def test_miss_on_empty_cache(self):
        cache = ResponseCache()
        assert cache.get(make_request()) is None

    def test_set_then_get(self):
        cache = ResponseCache()
        req = make_request(prompt="q1")
        resp = make_response("answer1")
        cache.set(req, resp)
        result = cache.get(req)
        assert result is not None
        assert result.content == "answer1"

    def test_different_requests_dont_collide(self):
        cache = ResponseCache()
        req1 = make_request(prompt="q1")
        req2 = make_request(prompt="q2")
        cache.set(req1, make_response("a1"))
        cache.set(req2, make_response("a2"))
        assert cache.get(req1).content == "a1"
        assert cache.get(req2).content == "a2"

    def test_ttl_expiry(self):
        cache = ResponseCache(ttl_seconds=0.05)
        req = make_request()
        cache.set(req, make_response())
        assert cache.get(req) is not None
        time.sleep(0.1)
        assert cache.get(req) is None

    def test_invalidate(self):
        cache = ResponseCache()
        req = make_request()
        cache.set(req, make_response())
        cache.invalidate(req)
        assert cache.get(req) is None

    def test_clear(self):
        cache = ResponseCache()
        for i in range(5):
            cache.set(make_request(prompt=str(i)), make_response())
        assert cache.size == 5
        cache.clear()
        assert cache.size == 0

    def test_max_size_evicts_oldest(self):
        cache = ResponseCache(max_size=3)
        reqs = [make_request(prompt=str(i)) for i in range(4)]
        for r in reqs:
            cache.set(r, make_response())
        assert cache.size == 3
        # oldest (prompt="0") should be evicted
        assert cache.get(reqs[0]) is None
        assert cache.get(reqs[3]) is not None
