# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# curl version tracks the base image — pin base image by digest for full reproducibility:
#   FROM python:3.12-slim@sha256:<digest>
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── deps layer (cached unless pyproject.toml changes) ────────────────────────
FROM base AS deps

COPY pyproject.toml ./
# Install only core runtime deps (no ML/dev extras — keeps image ~200 MB)
RUN pip install --no-cache-dir \
    "anthropic>=0.87.0,<1.0" \
    "cryptography>=46.0.6" \
    "httpx>=0.27.0,<1.0" \
    "aiohttp>=3.9.0,<4.0" \
    "fastapi>=0.111.0,<1.0" \
    "uvicorn[standard]>=0.30.0,<1.0" \
    "pydantic>=2.7.0,<3.0" \
    "PyYAML>=6.0.1" \
    "python-dotenv>=1.0.0"

# ── app layer ─────────────────────────────────────────────────────────────────
FROM deps AS app

COPY src/ ./src/
COPY config/ ./config/
COPY data/evals/ ./data/evals/

# Create remaining data directories and non-root user
RUN mkdir -p data/cache data/outputs data/research && \
    useradd --create-home --uid 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
