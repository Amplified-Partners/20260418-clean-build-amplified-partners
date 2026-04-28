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
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()" || exit 1

EXPOSE 8000

CMD ["python", "-u", "enforcer.py"]
