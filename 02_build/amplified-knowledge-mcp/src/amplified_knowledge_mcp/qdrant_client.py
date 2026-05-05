"""
Qdrant vector database client — semantic search and collection management.

Qdrant vector embeddings built by Clawd (OpenClaw).

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b
"""

from __future__ import annotations

import logging
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, PointStruct

from .config import QDRANT_HOST, QDRANT_PORT

_log = logging.getLogger("amplified_mcp.qdrant")

_client: QdrantClient | None = None


def _get_client() -> QdrantClient:
    global _client
    if _client is None:
        url = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
        _log.info("Connecting to Qdrant at %s", url)
        _client = QdrantClient(url=url, timeout=30)
    return _client


def list_collections() -> list[dict[str, Any]]:
    """List all Qdrant collections with stats."""
    client = _get_client()
    collections = client.get_collections().collections
    result = []
    for col in collections:
        info = client.get_collection(col.name)
        vector_size = None
        try:
            vparams = info.config.params.vectors
            if hasattr(vparams, "size"):
                vector_size = vparams.size
            elif isinstance(vparams, dict):
                first = next(iter(vparams.values()), None)
                if first and hasattr(first, "size"):
                    vector_size = first.size
        except Exception:
            pass

        result.append({
            "name": col.name,
            "points_count": info.points_count,
            "vectors_count": getattr(info, "vectors_count", info.points_count),
            "vector_size": vector_size,
            "status": info.status.value if info.status else "unknown",
        })
    return result


def search_vectors(
    collection: str,
    query_vector: list[float],
    limit: int = 5,
    category_filter: str | None = None,
) -> list[dict[str, Any]]:
    """Semantic search against a Qdrant collection."""
    client = _get_client()

    search_filter = None
    if category_filter:
        search_filter = Filter(
            must=[FieldCondition(key="category", match=MatchValue(value=category_filter))]
        )

    results = client.query_points(
        collection_name=collection,
        query=query_vector,
        limit=limit,
        query_filter=search_filter,
        with_payload=True,
    )

    return [
        {
            "id": str(hit.id),
            "score": hit.score,
            "payload": dict(hit.payload) if hit.payload else {},
        }
        for hit in results.points
    ]


def scroll_points(
    collection: str,
    limit: int = 10,
    category_filter: str | None = None,
    offset: str | int | None = None,
) -> dict[str, Any]:
    """Browse points in a collection with optional filtering."""
    client = _get_client()

    scroll_filter = None
    if category_filter:
        scroll_filter = Filter(
            must=[FieldCondition(key="category", match=MatchValue(value=category_filter))]
        )

    points, next_offset = client.scroll(
        collection_name=collection,
        limit=limit,
        scroll_filter=scroll_filter,
        offset=offset,
        with_payload=True,
        with_vectors=False,
    )

    return {
        "points": [
            {
                "id": str(p.id),
                "payload": dict(p.payload) if p.payload else {},
            }
            for p in points
        ],
        "next_offset": str(next_offset) if next_offset else None,
    }


def upsert_points(
    collection: str,
    points: list[PointStruct],
) -> None:
    """Insert or update points in a collection."""
    client = _get_client()
    client.upsert(collection_name=collection, points=points)
