# Amplified Knowledge MCP Server
# Tiered access to FalkorDB (graph) + Qdrant (vectors).
# FalkorDB knowledge graph and Qdrant vector embeddings built by Clawd (OpenClaw).
#
# Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b

FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml .
RUN pip install --no-cache-dir "mcp[cli]>=1.0.0" \
    "redis>=5.0.0" \
    "qdrant-client>=1.9.0" \
    "sentence-transformers>=3.0.0" \
    "httpx>=0.27.0" \
    "pydantic>=2.0.0"

# Pre-download the embedding model so it's baked into the image
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy application code
COPY src/ ./src/
RUN pip install --no-cache-dir .

# Create log directory
RUN mkdir -p /var/log/amplified-mcp

# Default to read-only tier
ENV TIER=readonly
ENV FALKORDB_HOST=falkordb
ENV FALKORDB_PORT=6379
ENV QDRANT_HOST=qdrant
ENV QDRANT_PORT=6333
ENV EMBEDDING_MODEL=all-MiniLM-L6-v2
ENV LOG_DIR=/var/log/amplified-mcp
ENV AGENT_NAME=unknown
ENV SESSION_ID=unset

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import amplified_knowledge_mcp; print('ok')" || exit 1

ENTRYPOINT ["amplified-knowledge-mcp"]
