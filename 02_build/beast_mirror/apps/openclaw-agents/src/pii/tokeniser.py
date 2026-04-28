"""
PII Tokeniser
==============
WHY: Cloud LLMs (OpenAI, Anthropic) should never see real customer data.
Every piece of PII gets replaced with a reversible token before it leaves
our network. The token looks like [PII:PERSON:a3f2b1] — readable in logs,
clearly fake, and we can swap it back on the way out.

HOW:
  1. Presidio detects PII entities (names, emails, phones, addresses, etc.)
  2. Overlapping detections are resolved (highest score wins)
  3. Each detected entity gets a deterministic short hash (same input = same token)
  4. The mapping (token -> real value) goes into Redis with a configurable TTL
  5. After the LLM responds, we swap tokens back to real values

DETERMINISTIC: Same PII always maps to the same token within a thread.
This means the LLM sees consistent references — "[PII:PERSON:a3f2b1] called
[PII:PERSON:a3f2b1] twice" — coherent reasoning without real names.

THREAD-SCOPED: Mappings are keyed by thread_id. Different conversations
get different token spaces. When a thread expires, so do its PII mappings.
"""

import hashlib
import json
import re
from typing import Optional

import redis.asyncio as aioredis
import structlog
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from config import settings

log = structlog.get_logger()

# Entities we care about — covers SMB client data
PII_ENTITIES = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "LOCATION",
    "UK_NHS",             # NHS numbers (UK clients)
    "CREDIT_CARD",
    "IBAN_CODE",
    "IP_ADDRESS",
    "DATE_TIME",          # Birthdays, appointment dates
    "NRP",                # Nationality/religious/political group
]

# Priority: when two entities overlap, higher-priority type wins
# Phone numbers should beat DATE_TIME, specific types beat generic
ENTITY_PRIORITY = {
    "EMAIL_ADDRESS": 100,
    "PHONE_NUMBER": 90,
    "CREDIT_CARD": 90,
    "IBAN_CODE": 90,
    "UK_NHS": 90,
    "IP_ADDRESS": 85,
    "PERSON": 80,
    "LOCATION": 70,
    "NRP": 60,
    "DATE_TIME": 50,
}

# TTL for PII mappings in Redis (seconds)
# 24 hours default — long enough for a conversation, short enough to not hoard data
PII_TTL_SECONDS = 86400

# Regex to find PII tokens in text for detokenisation
PII_TOKEN_RE = re.compile(r"\[PII:[A-Z_]+:[a-f0-9]{6}\]")


def _short_hash(value: str, entity_type: str) -> str:
    """
    Deterministic 6-char hash from the PII value + type.
    Same input always produces same token — critical for coherent LLM reasoning.
    """
    raw = f"{entity_type}:{value.lower().strip()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:6]


def _token(entity_type: str, hash_id: str) -> str:
    """Format: [PII:PERSON:a3f2b1]"""
    return f"[PII:{entity_type}:{hash_id}]"


def _resolve_overlaps(results: list[RecognizerResult]) -> list[RecognizerResult]:
    """
    When Presidio detects the same text span as multiple entity types,
    keep only the highest-priority one. For overlapping (but not identical)
    spans, keep the one with higher score * priority.
    """
    if not results:
        return results

    # Sort by start position, then by priority (descending)
    sorted_results = sorted(
        results,
        key=lambda r: (r.start, -ENTITY_PRIORITY.get(r.entity_type, 0), -r.score),
    )

    resolved = []
    for result in sorted_results:
        # Check if this overlaps with any already-kept result
        overlaps = False
        for kept in resolved:
            if result.start < kept.end and result.end > kept.start:
                # Overlap detected — skip this one (the kept one had higher priority)
                overlaps = True
                break
        if not overlaps:
            resolved.append(result)

    return resolved


class PIITokeniser:
    """
    Stateful PII tokeniser scoped to a conversation thread.

    Usage:
        tokeniser = PIITokeniser(redis_client, thread_id="abc-123")
        safe_text = await tokeniser.tokenise("Call John Smith at 07700 900123")
        # -> "Call [PII:PERSON:e4a2f1] at [PII:PHONE_NUMBER:b3c1d2]"

        real_text = await tokeniser.detokenise(llm_response)
        # -> swaps tokens back to real values
    """

    def __init__(self, redis_client: aioredis.Redis, thread_id: str):
        self._redis = redis_client
        self._thread_id = thread_id
        self._analyzer = AnalyzerEngine()
        self._anonymizer = AnonymizerEngine()
        self._redis_key = f"pii:thread:{thread_id}"

    async def tokenise(self, text: str, language: str = "en") -> str:
        """
        Detect PII in text, replace with tokens, store mappings in Redis.
        Returns the tokenised (safe) text.
        """
        if not text or not text.strip():
            return text

        # Detect PII entities
        results = self._analyzer.analyze(
            text=text,
            entities=PII_ENTITIES,
            language=language,
        )

        if not results:
            log.debug("pii_tokenise", thread_id=self._thread_id, entities_found=0)
            return text  # No PII found — pass through unchanged

        # Resolve overlapping detections
        results = _resolve_overlaps(results)

        # Sort by position (reverse) so we can replace from end to start
        # without messing up indices
        results.sort(key=lambda r: r.start, reverse=True)

        tokenised = text
        mappings = {}

        for result in results:
            original_value = text[result.start:result.end]
            hash_id = _short_hash(original_value, result.entity_type)
            token_str = _token(result.entity_type, hash_id)

            # Replace in text
            tokenised = tokenised[:result.start] + token_str + tokenised[result.end:]

            # Store mapping: token -> original value
            mappings[token_str] = original_value

        # Persist to Redis (merge with existing mappings for this thread)
        if mappings:
            existing = await self._redis.get(self._redis_key)
            if existing:
                existing_map = json.loads(existing)
                existing_map.update(mappings)
                mappings = existing_map

            await self._redis.set(
                self._redis_key,
                json.dumps(mappings),
                ex=PII_TTL_SECONDS,
            )

        log.info(
            "pii_tokenise",
            thread_id=self._thread_id,
            entities_found=len(results),
            entity_types=[r.entity_type for r in results],
            tokenised_preview=tokenised[:200],
        )

        return tokenised

    async def detokenise(self, text: str) -> str:
        """
        Replace PII tokens back with real values.
        Used on LLM responses before sending to the client.
        """
        if not text or "[PII:" not in text:
            return text

        raw = await self._redis.get(self._redis_key)
        if not raw:
            return text  # No mappings found — tokens stay as-is

        mappings = json.loads(raw)

        result = text
        for token_str, original_value in mappings.items():
            result = result.replace(token_str, original_value)

        # Log if any tokens remain unreplaced (LLM may have mangled them)
        remaining = PII_TOKEN_RE.findall(result)
        if remaining:
            log.warning(
                "pii_detokenise_incomplete",
                thread_id=self._thread_id,
                unreplaced_tokens=remaining,
            )

        return result

    async def get_mapping_count(self) -> int:
        """How many PII entities are tracked for this thread."""
        raw = await self._redis.get(self._redis_key)
        if not raw:
            return 0
        return len(json.loads(raw))

    async def clear_thread(self) -> None:
        """Explicitly delete all PII mappings for this thread."""
        await self._redis.delete(self._redis_key)


async def get_redis_client() -> aioredis.Redis:
    """Create an async Redis client for PII storage."""
    return aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
    )
