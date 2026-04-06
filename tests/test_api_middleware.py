"""Tests for src/api/middleware.py — CorrelationIDMiddleware and TimingMiddleware."""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.middleware import (
    ContentLengthLimitMiddleware,
    CorrelationIDMiddleware,
    TimingMiddleware,
    get_request_id,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_app(with_correlation: bool = True, with_timing: bool = True) -> FastAPI:
    app = FastAPI()

    @app.get("/ping")
    async def ping():
        return {"request_id": get_request_id()}

    @app.get("/error")
    async def err():
        raise ValueError("boom")

    if with_correlation:
        app.add_middleware(CorrelationIDMiddleware)
    if with_timing:
        app.add_middleware(TimingMiddleware)

    return app


@pytest.fixture
def client():
    return TestClient(_make_app(), raise_server_exceptions=False)


# ── CorrelationIDMiddleware ───────────────────────────────────────────────────

class TestCorrelationIDMiddleware:
    def test_response_has_request_id_header(self, client):
        resp = client.get("/ping")
        assert "X-Request-ID" in resp.headers

    def test_generated_id_is_non_empty(self, client):
        resp = client.get("/ping")
        assert len(resp.headers["X-Request-ID"]) > 0

    def test_honours_incoming_request_id(self, client):
        resp = client.get("/ping", headers={"X-Request-ID": "my-trace-123"})
        assert resp.headers["X-Request-ID"] == "my-trace-123"

    def test_different_requests_get_different_ids(self, client):
        r1 = client.get("/ping")
        r2 = client.get("/ping")
        assert r1.headers["X-Request-ID"] != r2.headers["X-Request-ID"]

    def test_request_id_available_in_handler(self, client):
        resp = client.get("/ping", headers={"X-Request-ID": "ctx-abc"})
        data = resp.json()
        assert data["request_id"] == "ctx-abc"

    def test_prefix_prepended_to_generated_id(self):
        app = FastAPI()

        @app.get("/ping")
        async def ping():
            return {"ok": True}

        app.add_middleware(CorrelationIDMiddleware, prefix="svc-")
        c = TestClient(app)
        resp = c.get("/ping")
        assert resp.headers["X-Request-ID"].startswith("svc-")

    def test_ids_are_hex_format_when_generated(self, client):
        resp = client.get("/ping")
        rid = resp.headers["X-Request-ID"]
        # UUIDs without dashes → 32 hex chars
        assert all(c in "0123456789abcdef" for c in rid)
        assert len(rid) == 32

    def test_get_request_id_returns_empty_outside_request(self):
        # Outside a request context, should return empty string
        assert get_request_id() == ""


# ── TimingMiddleware ──────────────────────────────────────────────────────────

class TestTimingMiddleware:
    def test_response_has_timing_header(self, client):
        resp = client.get("/ping")
        assert "X-Process-Time-Ms" in resp.headers

    def test_timing_is_non_negative_float(self, client):
        resp = client.get("/ping")
        val = float(resp.headers["X-Process-Time-Ms"])
        assert val >= 0.0

    def test_timing_without_correlation(self):
        app = FastAPI()

        @app.get("/t")
        async def t():
            return {"ok": True}

        app.add_middleware(TimingMiddleware)
        c = TestClient(app)
        resp = c.get("/t")
        assert "X-Process-Time-Ms" in resp.headers


# ── Both middlewares together ─────────────────────────────────────────────────

class TestMiddlewareStack:
    def test_both_headers_present(self, client):
        resp = client.get("/ping")
        assert "X-Request-ID" in resp.headers
        assert "X-Process-Time-Ms" in resp.headers

    def test_request_id_propagates_through_timing(self, client):
        resp = client.get("/ping", headers={"X-Request-ID": "trace-xyz"})
        assert resp.headers["X-Request-ID"] == "trace-xyz"
        assert float(resp.headers["X-Process-Time-Ms"]) >= 0.0

    def test_app_import_includes_middleware(self):
        """The production app.py should have middleware wired in."""
        from src.api import app
        # Check middleware is registered (stored as Middleware objects)
        names = str(app.user_middleware)
        assert "CorrelationIDMiddleware" in names or "Correlation" in names


# ── ContentLengthLimitMiddleware ──────────────────────────────────────────────

def _make_size_app(max_bytes: int = 100) -> FastAPI:
    app = FastAPI()

    @app.post("/upload")
    async def upload():
        return {"ok": True}

    app.add_middleware(ContentLengthLimitMiddleware, max_bytes=max_bytes)
    return app


class TestContentLengthLimitMiddleware:
    def test_allows_request_under_limit(self):
        c = TestClient(_make_size_app(max_bytes=100))
        body = b"x" * 50
        resp = c.post("/upload", content=body,
                      headers={"Content-Length": str(len(body))})
        assert resp.status_code == 200

    def test_allows_request_exactly_at_limit(self):
        c = TestClient(_make_size_app(max_bytes=50))
        body = b"x" * 50
        resp = c.post("/upload", content=body,
                      headers={"Content-Length": "50"})
        assert resp.status_code == 200

    def test_rejects_request_over_limit(self):
        c = TestClient(_make_size_app(max_bytes=50))
        resp = c.post("/upload", content=b"x",
                      headers={"Content-Length": "51"})
        assert resp.status_code == 413

    def test_413_response_has_detail(self):
        c = TestClient(_make_size_app(max_bytes=10))
        resp = c.post("/upload", content=b"x",
                      headers={"Content-Length": "999"})
        data = resp.json()
        assert "detail" in data
        assert "999" in data["detail"]

    def test_no_content_length_passes_through(self):
        """Chunked / streaming requests without Content-Length are allowed."""
        c = TestClient(_make_size_app(max_bytes=10))
        # httpx sends without Content-Length when we omit it explicitly
        resp = c.post("/upload")
        assert resp.status_code == 200

    def test_invalid_content_length_returns_400(self):
        c = TestClient(_make_size_app(max_bytes=100))
        resp = c.post("/upload", headers={"Content-Length": "notanumber"})
        assert resp.status_code == 400

    def test_default_limit_is_one_mib(self):
        assert ContentLengthLimitMiddleware.DEFAULT_MAX_BYTES == 1_048_576

    def test_production_app_has_middleware(self):
        from src.api import app
        names = str(app.user_middleware)
        assert "ContentLengthLimit" in names
