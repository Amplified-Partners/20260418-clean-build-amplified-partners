"""Intent router — parses Ewan's text replies into actionable intents.

Emoji routing:
  👍 → acknowledge (log, no further action)
  ⚠️ → escalate (create urgent task)
  ❓ → clarify (trigger clarification agent)

Text routing (via keyword matching, upgradeable to LLM):
  "cancel/reschedule/move" → calendar_action
  "park/hold/pause" → park_task
  "do/fix/build/wire" → create_task
  "decide/decision/approved/go" → decision
  Fallback → general_reply

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

IntentKind = Literal[
    "acknowledge",
    "escalate",
    "clarify",
    "calendar_action",
    "park_task",
    "create_task",
    "decision",
    "general_reply",
]

EMOJI_MAP: dict[str, IntentKind] = {
    "👍": "acknowledge",
    "thumbsup": "acknowledge",
    "👌": "acknowledge",
    "✅": "acknowledge",
    "⚠️": "escalate",
    "warning": "escalate",
    "🔥": "escalate",
    "❓": "clarify",
    "question": "clarify",
    "❓": "clarify",
}

KEYWORD_PATTERNS: list[tuple[re.Pattern[str], IntentKind]] = [
    (re.compile(r"\b(cancel|reschedule|move|postpone)\b", re.I), "calendar_action"),
    (re.compile(r"\b(park|hold|pause|defer|shelve)\b", re.I), "park_task"),
    (re.compile(r"\b(do|fix|build|wire|implement|ship|deploy)\b", re.I), "create_task"),
    (re.compile(r"\b(decide|decision|approved|go ahead|green.?light|confirmed)\b", re.I), "decision"),
]


@dataclass(frozen=True)
class Intent:
    kind: IntentKind
    raw_content: str
    confidence: float
    extracted_action: str


def classify_reply(content: str) -> Intent:
    """Classify a reply into an intent. Deterministic keyword matching."""
    stripped = content.strip()

    if stripped in EMOJI_MAP:
        return Intent(
            kind=EMOJI_MAP[stripped],
            raw_content=content,
            confidence=0.95,
            extracted_action=stripped,
        )

    for pattern, intent_kind in KEYWORD_PATTERNS:
        match = pattern.search(stripped)
        if match:
            return Intent(
                kind=intent_kind,
                raw_content=content,
                confidence=0.80,
                extracted_action=match.group(0),
            )

    return Intent(
        kind="general_reply",
        raw_content=content,
        confidence=0.50,
        extracted_action=stripped,
    )
