FROM python:3.12-slim

# Docker CLI needed for container inspection tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        docker.io \
        git \
        findutils \
        coreutils \
        systemd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir .

# Default to SSE transport on port 8400
ENV BEAST_MCP_TRANSPORT=sse
ENV BEAST_MCP_PORT=8400
EXPOSE 8400

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8400/sse', timeout=5)" || exit 1

CMD ["beast-control-mcp"]

# Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
