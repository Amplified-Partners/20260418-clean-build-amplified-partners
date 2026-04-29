"""
Text embedding using sentence-transformers.

The amplified_knowledge collection uses 384-dimensional vectors,
consistent with all-MiniLM-L6-v2.

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b
"""

from __future__ import annotations

import logging

from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL

_log = logging.getLogger("amplified_mcp.embedder")

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _log.info("Loading embedding model: %s", EMBEDDING_MODEL)
        _model = SentenceTransformer(EMBEDDING_MODEL)
        _log.info("Model loaded — dimension: %d", _model.get_sentence_embedding_dimension())
    return _model


def embed_text(text: str) -> list[float]:
    """Embed a single text string into a vector."""
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts into vectors."""
    model = _get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]


def get_dimension() -> int:
    """Return the embedding dimension of the loaded model."""
    return _get_model().get_sentence_embedding_dimension()
