# API Design Conventions

Sets rules for REST API design patterns in this project (src/api/).

## Endpoint Design
- Resources are nouns, not verbs: `/complete` not `/doComplete`
- HTTP methods: GET=read, POST=create/action, PUT=replace, PATCH=update, DELETE=remove
- Versioning: prefix with `/v1/` when breaking changes are needed (current API is unversioned/internal)
- Return 200 for success, 201 for created, 400 for client error, 422 for validation, 502 for upstream LLM error

## Request / Response Models
- All request and response bodies use Pydantic v2 models in `src/api/models.py`
- Field names: `snake_case` in Python → JSON serialises as `snake_case` (no camelCase)
- Optional fields default to `None`, not to magic sentinel values
- Always include `content_type: str` header hint for structured payloads

## Headers
- Every response carries `X-Request-ID` (set by CorrelationIDMiddleware)
- Every response carries `X-Process-Time-Ms` (set by TimingMiddleware)
- Pass `X-Request-ID` through to upstream services for distributed tracing

## Error Responses
- Use `HTTPException(status_code=..., detail=str(e))` — never expose stack traces
- Log the full error with `logger.error(event, error=str(e), request_id=get_request_id())`
- Upstream LLM errors → 502; validation errors → 422 (handled by FastAPI/Pydantic); auth → 401

## Streaming
- Streaming endpoints use `StreamingResponse` with `media_type="text/event-stream"`
- Token format: `data: <token>\n\n`; terminal token: `data: [DONE]\n\n`
- Errors during stream: `data: [ERROR] <message>\n\n`

## Auto-Routing
- All completion endpoints support `auto_route: bool = True`
- When True: call `routing_route(prompt)` to select model
- When False or `model` is specified: use the explicit model
- Always log `routed_by` reason for observability

## Middleware Order (outermost → innermost)
1. `CorrelationIDMiddleware` — attach request ID first
2. `TimingMiddleware` — time the full handler including inner middleware
3. Application routes

## Rate Limiting
- `RateLimiter` is initialized in `lifespan` and shared across requests
- Default: 100 requests/minute per instance (not per user — add auth layer for per-user)
- On rate limit exceeded: raise `HTTPException(status_code=429)`
