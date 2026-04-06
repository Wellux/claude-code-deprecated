"""Tests for src/utils/rate_limiter.py — token bucket behavior."""
import asyncio
import time

import pytest

from src.utils.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_single_acquire_succeeds():
    limiter = RateLimiter(requests_per_minute=60)
    await limiter.acquire()  # should not raise or block significantly


@pytest.mark.asyncio
async def test_burst_within_capacity():
    limiter = RateLimiter(requests_per_minute=600)  # 10/sec bucket
    t0 = time.monotonic()
    for _ in range(5):
        await limiter.acquire()
    elapsed = time.monotonic() - t0
    # 5 tokens available immediately — should complete fast
    assert elapsed < 1.0


@pytest.mark.asyncio
async def test_available_tokens_decreases():
    limiter = RateLimiter(requests_per_minute=60)
    before = limiter.available_tokens
    await limiter.acquire()
    after = limiter.available_tokens
    assert after < before


@pytest.mark.asyncio
async def test_rate_limiting_delays_excess_requests():
    # 60 rpm = 1 token/sec; start with 1 token, request 2 → second must wait ~1s
    limiter = RateLimiter(requests_per_minute=60)
    await limiter.acquire()  # consume the initial token
    # drain remaining tokens
    limiter._tokens = 0.0

    t0 = time.monotonic()
    await limiter.acquire()  # must wait for refill
    elapsed = time.monotonic() - t0
    assert elapsed >= 0.8  # at least ~1 second


@pytest.mark.asyncio
async def test_tokens_refill_over_time():
    limiter = RateLimiter(requests_per_minute=600)  # 10/sec
    limiter._tokens = 0.0
    await asyncio.sleep(0.2)
    assert limiter.available_tokens > 0
