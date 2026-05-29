FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install curl for lightweight readiness checks and shell scripts.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy uv from the official image to keep installs fast and reproducible.
COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies first for better layer caching.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

COPY main.py ./

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

CMD ["uv", "run", "main.py"]
