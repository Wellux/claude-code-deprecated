"""Token-bucket rate limiter for API calls."""
import asyncio
import time


class RateLimiter:
    """Async token-bucket rate limiter.

    Allows up to `requests_per_minute` calls per 60-second window.
    Callers await `acquire()` which blocks until a slot is available.
    """

    def __init__(self, requests_per_minute: int = 100):
        self.rpm = requests_per_minute
        self._interval = 60.0 / requests_per_minute  # seconds per token
        self._tokens = float(requests_per_minute)
        self._max_tokens = float(requests_per_minute)
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._max_tokens, self._tokens + elapsed / self._interval)
        self._last_refill = now

    async def acquire(self, tokens: float = 1.0) -> None:
        """Block until `tokens` slots are available."""
        async with self._lock:
            while True:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                wait = (tokens - self._tokens) * self._interval
                await asyncio.sleep(wait)

    @property
    def available_tokens(self) -> float:
        self._refill()
        return self._tokens
