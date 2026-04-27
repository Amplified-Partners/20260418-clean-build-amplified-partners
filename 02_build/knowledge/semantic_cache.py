"""
Semantic Cache — Drop-in wrapper for Anthropic messages.create()

Checks Qdrant for a semantically similar cached response before calling the API.
On cache miss, calls the API and stores the result.

Usage:
    from app.core.semantic_cache import SemanticCache
    cache = SemanticCache()
    response = cache.create(model="claude-sonnet-4-6", messages=[...], system="...")

Cache hit threshold: 0.95 cosine similarity (high precision — only near-identical prompts hit)
Storage collection: llm_cache (separate from gatekeeper_notes)
TTL: 24 hours (enforced at read time — no Qdrant native TTL)

Target: 70-90% savings on interview engine calls where the same context
recurs across sessions (same business type, same question sequence).
"""

import os
import json
import time
import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from app.core.secrets import secrets  # noqa: F401 — populates os.environ on import

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance,
        VectorParams,
        PointStruct,
        Filter,
        FieldCondition,
        Range,
    )
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    raise ImportError(
        f"Missing dependency: {e}\n"
        "Run: pip install qdrant-client sentence-transformers"
    )

try:
    import anthropic
except ImportError:
    raise ImportError("Run: pip install anthropic")


# ---- Config ----------------------------------------------------------------

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "llm_cache"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384-dim, fast, local
EMBEDDING_DIM = 384
SIMILARITY_THRESHOLD = 0.95  # Very high — we only want near-identical prompts
TTL_HOURS = 24
CACHE_ENABLED = os.getenv("SEMANTIC_CACHE_ENABLED", "true").lower() == "true"


# ---- Cache key construction ------------------------------------------------

def _make_cache_key(model: str, messages: List[Dict], system: Optional[str] = None) -> str:
    """
    Build a canonical string for embedding.
    Includes model, system prompt, and last 3 messages (the most recent context).
    We don't embed the entire history — it changes every turn.
    """
    parts = [f"model:{model}"]
    if system:
        # First 500 chars of system is enough for differentiation
        parts.append(f"sys:{system[:500]}")
    # Last 3 messages carry the semantic meaning of the current request
    for msg in messages[-3:]:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if isinstance(content, list):
            # Handle content block format
            text_parts = [b.get("text", "") for b in content if isinstance(b, dict)]
            content = " ".join(text_parts)
        parts.append(f"{role}:{str(content)[:300]}")
    return " | ".join(parts)


def _make_point_id(key: str) -> int:
    h = hashlib.sha256(key.encode()).digest()
    return int.from_bytes(h[:8], "big") % (2**63)


# ---- SemanticCache ---------------------------------------------------------

class SemanticCache:
    """
    Semantic cache for Anthropic API calls.

    Wraps anthropic.Anthropic().messages.create() with Qdrant-backed caching.
    Call cache.create() exactly as you would client.messages.create().

    Stats are tracked in self.stats for observability.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
        ttl_hours: int = TTL_HOURS,
        enabled: bool = CACHE_ENABLED,
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.similarity_threshold = similarity_threshold
        self.ttl_hours = ttl_hours
        self.enabled = enabled

        self._client = anthropic.Anthropic(api_key=self.api_key)
        self._qdrant = QdrantClient(
            host=QDRANT_HOST, port=QDRANT_PORT,
            api_key=QDRANT_API_KEY, https=False,
        )
        self._embedder = SentenceTransformer(EMBEDDING_MODEL)

        self.stats = {"hits": 0, "misses": 0, "writes": 0, "errors": 0}

        self._ensure_collection()

    def _ensure_collection(self):
        """Create llm_cache collection if it doesn't exist."""
        collections = [c.name for c in self._qdrant.get_collections().collections]
        if COLLECTION_NAME not in collections:
            self._qdrant.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
            )

    def _embed(self, text: str) -> List[float]:
        return self._embedder.encode(text).tolist()

    def _is_expired(self, cached_at_iso: str) -> bool:
        try:
            cached_at = datetime.fromisoformat(cached_at_iso)
            return datetime.utcnow() - cached_at > timedelta(hours=self.ttl_hours)
        except Exception:
            return True  # Treat unparseable timestamps as expired

    def _lookup(self, key_embedding: List[float]) -> Optional[Dict]:
        """Search Qdrant for a similar cached response."""
        result = self._qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=key_embedding,
            limit=1,
            score_threshold=self.similarity_threshold,
        )
        results = result.points if hasattr(result, "points") else []
        if not results:
            return None
        hit = results[0]
        payload = hit.payload or {}
        if self._is_expired(payload.get("cached_at", "")):
            return None  # Treat as miss; stale entry stays until overwritten
        return payload.get("response")

    def _store(self, key: str, key_embedding: List[float], response_dict: Dict):
        """Store a response in Qdrant."""
        point_id = _make_point_id(key)
        payload = {
            "cache_key_preview": key[:200],
            "response": response_dict,
            "cached_at": datetime.utcnow().isoformat(),
            "model": response_dict.get("model", ""),
        }
        self._qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[PointStruct(id=point_id, vector=key_embedding, payload=payload)],
        )

    def _response_to_dict(self, response) -> Dict:
        """Convert Anthropic Message object to serialisable dict."""
        return {
            "id": response.id,
            "type": "message",
            "role": "assistant",
            "content": [{"type": b.type, "text": b.text} for b in response.content],
            "model": response.model,
            "stop_reason": response.stop_reason,
            "stop_sequence": response.stop_sequence,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            "_from_cache": True,
        }

    def _dict_to_response_like(self, d: Dict) -> "_CachedResponse":
        """Wrap a cached dict in an object that mirrors the Anthropic response interface."""
        return _CachedResponse(d)

    def create(self, model: str, messages: List[Dict], **kwargs) -> Any:
        """
        Drop-in replacement for anthropic.messages.create().

        Checks cache first. On miss, calls API and caches result.
        kwargs are passed through to the API (temperature, system, max_tokens, etc.)

        Returns an object with .content, .model, .stop_reason, .usage attributes.
        """
        if not self.enabled:
            return self._client.messages.create(model=model, messages=messages, **kwargs)

        system = kwargs.get("system")
        key = _make_cache_key(model, messages, system)
        key_embedding = self._embed(key)

        try:
            cached = self._lookup(key_embedding)
            if cached:
                self.stats["hits"] += 1
                return self._dict_to_response_like(cached)
        except Exception as e:
            self.stats["errors"] += 1
            print(f"[SemanticCache] Lookup error (proceeding to API): {e}")

        # Cache miss — call the real API
        self.stats["misses"] += 1
        response = self._client.messages.create(model=model, messages=messages, **kwargs)

        try:
            response_dict = self._response_to_dict(response)
            self._store(key, key_embedding, response_dict)
            self.stats["writes"] += 1
        except Exception as e:
            self.stats["errors"] += 1
            print(f"[SemanticCache] Store error: {e}")

        return response

    def hit_rate(self) -> float:
        total = self.stats["hits"] + self.stats["misses"]
        return self.stats["hits"] / total if total > 0 else 0.0

    def log_stats(self):
        total = self.stats["hits"] + self.stats["misses"]
        print(
            f"[SemanticCache] hits={self.stats['hits']} misses={self.stats['misses']} "
            f"hit_rate={self.hit_rate():.1%} writes={self.stats['writes']} "
            f"errors={self.stats['errors']} total={total}"
        )


class _CachedResponse:
    """
    Minimal object that mirrors the Anthropic Message interface for cached responses.
    Enough for .content[0].text, .model, .stop_reason, .usage access patterns.
    """

    class _Usage:
        def __init__(self, d: Dict):
            self.input_tokens = d.get("input_tokens", 0)
            self.output_tokens = d.get("output_tokens", 0)
            self.cache_creation_input_tokens = 0
            self.cache_read_input_tokens = 0

    class _ContentBlock:
        def __init__(self, d: Dict):
            self.type = d.get("type", "text")
            self.text = d.get("text", "")

    def __init__(self, d: Dict):
        self.id = d.get("id", "cached")
        self.type = "message"
        self.role = "assistant"
        self.content = [self._ContentBlock(b) for b in d.get("content", [])]
        self.model = d.get("model", "")
        self.stop_reason = d.get("stop_reason", "end_turn")
        self.stop_sequence = d.get("stop_sequence")
        self.usage = self._Usage(d.get("usage", {}))
        self._from_cache = True

    _ContentBlock = _ContentBlock
    _Usage = _Usage
