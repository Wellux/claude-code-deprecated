"""API middleware — correlation IDs, request timing, and structured access logs."""
from __future__ import annotations

import contextvars
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from ..utils.logger import get_logger

logger = get_logger("api.access")

# Context var so handlers can read the current request ID
_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default=""
)


def get_request_id() -> str:
    """Return the correlation ID for the current request (empty string if none)."""
    return _request_id_var.get()


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Attach a correlation/request ID to every request and response.

    - Reads ``X-Request-ID`` from incoming headers if present.
    - Otherwise generates a new UUID4.
    - Sets ``X-Request-ID`` on the response.
    - Logs structured access events with method, path, status, and latency.

    Usage::
        app.add_middleware(CorrelationIDMiddleware)
    """

    HEADER = "X-Request-ID"

    def __init__(self, app: ASGIApp, *, prefix: str = "") -> None:
        super().__init__(app)
        self._prefix = prefix

    async def dispatch(self, request: Request, call_next) -> Response:
        # Honour incoming ID (e.g. from a gateway) or generate a fresh one
        request_id = request.headers.get(self.HEADER) or f"{self._prefix}{uuid.uuid4().hex}"
        token = _request_id_var.set(request_id)

        t0 = time.monotonic()
        try:
            response: Response = await call_next(request)
            latency_ms = (time.monotonic() - t0) * 1000
            response.headers[self.HEADER] = request_id
            logger.info(
                "http_request",
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                latency_ms=round(latency_ms, 1),
                request_id=request_id,
            )
            return response
        finally:
            _request_id_var.reset(token)


class TimingMiddleware(BaseHTTPMiddleware):
    """Add ``X-Process-Time-Ms`` header to every response."""

    async def dispatch(self, request: Request, call_next) -> Response:
        t0 = time.monotonic()
        response = await call_next(request)
        response.headers["X-Process-Time-Ms"] = str(round((time.monotonic() - t0) * 1000, 1))
        return response


class ContentLengthLimitMiddleware(BaseHTTPMiddleware):
    """Reject requests whose declared Content-Length exceeds ``max_bytes``.

    Returns HTTP 413 before the body is read, protecting the server from
    large payload allocations. Requests without a Content-Length header
    are passed through (chunked/streaming transfers).

    Default limit: 1 MiB (1_048_576 bytes).

    Usage::
        app.add_middleware(ContentLengthLimitMiddleware, max_bytes=512_000)
    """

    DEFAULT_MAX_BYTES = 1_048_576  # 1 MiB

    def __init__(self, app: ASGIApp, *, max_bytes: int = DEFAULT_MAX_BYTES) -> None:
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError:
                return JSONResponse(
                    {"detail": "Invalid Content-Length header"},
                    status_code=400,
                )
            if length > self.max_bytes:
                logger.warning(
                    "request_too_large",
                    content_length=length,
                    max_bytes=self.max_bytes,
                    path=request.url.path,
                )
                return JSONResponse(
                    {"detail": f"Request body too large: {length} bytes (max {self.max_bytes})"},
                    status_code=413,
                )
        return await call_next(request)
