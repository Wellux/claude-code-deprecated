# src/api — REST API Layer Context

## Purpose
FastAPI application exposing LLM completions and routing decisions over HTTP.

## Files
- `app.py` — FastAPI app factory, lifespan, middleware registration
- `routes.py` — endpoint handlers (`/health`, `/v1/complete`, `/v1/complete/stream`, `/v1/chat`, `/v1/route`)
- `models.py` — Pydantic v2 request/response models
- `middleware.py` — CorrelationIDMiddleware (X-Request-ID), TimingMiddleware (X-Process-Time-Ms)
- `rate_limiter.py` — token bucket, 100 req/min default, raises HTTP 429

## Middleware order (outermost → innermost)
1. `CorrelationIDMiddleware` — attach request ID first
2. `TimingMiddleware` — time the full handler

## Key conventions
- All fields: `snake_case` (no camelCase)
- Optional fields default to `None`
- Errors: `HTTPException(status_code=..., detail="Upstream LLM error [ExcType] — see server logs (request_id=…)")` — never expose `str(e)` to clients
- Upstream LLM errors → 502; validation → 422; rate limit → 429
- Streaming: `StreamingResponse(media_type="text/event-stream")`, token format `data: <token>\n\n`, terminal `data: [DONE]\n\n`

## Auto-routing
`auto_route: bool = True` on completion endpoints. When True: call `route_llm(prompt)` to select model.
Log `routed_by` reason for observability.

## Start
`ccm serve` or `uvicorn src.api.app:app --reload`
