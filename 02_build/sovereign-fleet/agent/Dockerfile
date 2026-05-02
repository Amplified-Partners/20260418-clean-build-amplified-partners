# Authored by Devon | 2026-05-02 | devin-701075c43e444229aa32f993bf60b36a
FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    git grep curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir .

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
