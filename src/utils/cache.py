"""In-memory response cache with optional TTL."""
from __future__ import annotations

import hashlib
import json
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..llm.base import CompletionRequest, CompletionResponse


def _cache_key(request: CompletionRequest) -> str:
    """Stable hash of the request fields that affect output."""
    payload = json.dumps(
        {
            "prompt": request.prompt,
            "system": request.system,
            "model": request.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


class ResponseCache:
    """Simple in-memory LRU-ish cache with TTL.

    Not thread-safe for concurrent writes — use asyncio.Lock externally
    if needed. Suitable for single-threaded async use.
    """

    def __init__(self, ttl_seconds: float = 3600.0, max_size: int = 1000):
        self._ttl = ttl_seconds
        self._max_size = max_size
        self._store: dict[str, tuple[float, CompletionResponse]] = {}

    def get(self, request: CompletionRequest) -> CompletionResponse | None:
        key = _cache_key(request)
        entry = self._store.get(key)
        if entry is None:
            return None
        ts, response = entry
        if time.monotonic() - ts > self._ttl:
            del self._store[key]
            return None
        return response

    def set(self, request: CompletionRequest, response: CompletionResponse) -> None:
        if len(self._store) >= self._max_size:
            # Evict oldest entry
            oldest_key = min(self._store, key=lambda k: self._store[k][0])
            del self._store[oldest_key]
        key = _cache_key(request)
        self._store[key] = (time.monotonic(), response)

    def invalidate(self, request: CompletionRequest) -> None:
        key = _cache_key(request)
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    @property
    def size(self) -> int:
        return len(self._store)
