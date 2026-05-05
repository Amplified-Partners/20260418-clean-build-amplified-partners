# Authored by Claude (Haiku 4.5), 2026-03-11
# Merged into clean-build/02_build/enforcer/ by Devon (Devin session devin-1bdaf31798874921940598bed17ca9e3), 2026-05-04 (AMP-77)
FROM python:3.12-alpine

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libpq-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY enforcer.py .
COPY checks/ ./checks/

# Create a non-root user for security
RUN addgroup -g 1000 enforcer && adduser -D -u 1000 -G enforcer enforcer
USER enforcer

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/livez').raise_for_status()" || exit 1

EXPOSE 8000

CMD ["python", "-u", "enforcer.py"]
