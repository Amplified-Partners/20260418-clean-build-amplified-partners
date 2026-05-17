"""Prompt rewriter — transforms verbatim speech into structured agent-ready prompts.

Pipeline:
  1. Ewan speaks → Monologue transcribes → paste into Vellum
  2. Vellum stores verbatim (radical attribution, untouched)
  3. This module rewrites into structured prompt agents can execute
  4. Both entries go on the same hash chain

The rewrite is informed by the Business Brain AI Context Schema (19 fields).
v1 uses deterministic extraction; upgradeable to LLM-powered rewrite later.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class StructuredPrompt:
    """The cleaned, agent-ready version of raw speech."""

    action: str
    subject: str
    context: str
    urgency: str
    constraints: list[str] = field(default_factory=list)
    raw_length: int = 0
    clean_text: str = ""


# Urgency signal words
_URGENT_PATTERNS = re.compile(
    r"\b(now|today|asap|urgent|immediately|right now|straight away|"
    r"before end of day|eod|priority|critical)\b",
    re.I,
)
_LOW_PRIORITY = re.compile(
    r"\b(when you can|no rush|eventually|sometime|low priority|"
    r"whenever|park it|back burner)\b",
    re.I,
)

# Action extraction — what does Ewan want done?
_ACTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(fix|repair|patch|debug|sort out|sort)\b", re.I), "fix"),
    (re.compile(r"\b(build|create|make|wire|implement|add|set up|spin up)\b", re.I), "build"),
    (re.compile(r"\b(deploy|ship|push|release|launch)\b", re.I), "deploy"),
    (re.compile(r"\b(check|verify|confirm|test|validate|inspect)\b", re.I), "verify"),
    (re.compile(r"\b(cancel|stop|kill|remove|delete|drop|tear down)\b", re.I), "cancel"),
    (re.compile(r"\b(move|reschedule|postpone|shift|bring forward)\b", re.I), "reschedule"),
    (re.compile(r"\b(research|find out|investigate|look into|dig into)\b", re.I), "research"),
    (re.compile(r"\b(write|draft|document|spec out|outline)\b", re.I), "write"),
    (re.compile(r"\b(review|assess|evaluate|audit|score)\b", re.I), "review"),
    (re.compile(r"\b(decide|approve|go ahead|green.?light|confirmed)\b", re.I), "decide"),
    (re.compile(r"\b(park|hold|pause|defer|shelve)\b", re.I), "park"),
    (re.compile(r"\b(tell|inform|notify|let .+ know|update)\b", re.I), "communicate"),
]

# Constraint signals
_CONSTRAINT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(don'?t|do not|never|without|no)\s+(.{3,40})", re.I), "exclude"),
    (re.compile(r"\b(must|always|make sure|ensure)\s+(.{3,40})", re.I), "require"),
    (re.compile(r"\b(before|by|deadline|due)\s+(.{3,30})", re.I), "deadline"),
]


def _extract_urgency(text: str) -> str:
    """Determine urgency from signal words."""
    if _URGENT_PATTERNS.search(text):
        return "high"
    if _LOW_PRIORITY.search(text):
        return "low"
    return "normal"


def _extract_action(text: str) -> str:
    """Extract primary action verb category."""
    for pattern, action in _ACTION_PATTERNS:
        if pattern.search(text):
            return action
    return "act"


def _extract_subject(text: str) -> str:
    """Extract the subject/target of the action.

    Heuristic: take the noun phrase after the first action verb,
    or the first noun-like phrase if no verb found.
    """
    # Try to find "verb + the/a/this + noun phrase" pattern
    match = re.search(
        r"\b(?:fix|build|deploy|check|cancel|move|research|write|review|"
        r"tell|park|wire|implement|add|ship|create|make|sort|set up|"
        r"investigate|look into)\s+"
        r"(?:the |a |this |that |our |my )?(.{3,60}?)(?:\.|,|$|\s+(?:and|but|because|so|then))",
        text,
        re.I,
    )
    if match:
        return match.group(1).strip().rstrip(".")
    # Fallback: first significant phrase (skip filler words)
    cleaned = re.sub(r"^(?:so|right|ok|okay|um|uh|like|basically|yeah)\s+", "", text, flags=re.I)
    words = cleaned.split()
    if len(words) > 8:
        return " ".join(words[:8]) + "..."
    return cleaned[:80] if cleaned else text[:80]


def _extract_constraints(text: str) -> list[str]:
    """Extract explicit constraints or requirements."""
    constraints: list[str] = []
    for pattern, kind in _CONSTRAINT_PATTERNS:
        for match in pattern.finditer(text):
            constraint_text = match.group(0).strip()
            if len(constraint_text) > 5:
                constraints.append(f"{kind}: {constraint_text}")
    return constraints[:5]  # cap at 5


def _extract_context(text: str, action: str, subject: str) -> str:
    """Extract background context — the 'why' or 'because' parts."""
    # Look for explicit reasoning
    because_match = re.search(
        r"\b(?:because|since|as|reason is|the thing is|issue is)\s+(.{5,100}?)(?:\.|$)",
        text,
        re.I,
    )
    if because_match:
        return because_match.group(1).strip()

    # Look for background clauses
    background_match = re.search(
        r"\b(?:it'?s|they'?re|we'?re|currently|right now|at the moment)\s+(.{5,80}?)(?:\.|,|$)",
        text,
        re.I,
    )
    if background_match:
        return background_match.group(1).strip()

    return ""


def _build_clean_text(action: str, subject: str, context: str, urgency: str, constraints: list[str]) -> str:
    """Assemble the structured prompt text."""
    parts: list[str] = []

    # Action line
    parts.append(f"Action: {action}")
    parts.append(f"Subject: {subject}")

    if context:
        parts.append(f"Context: {context}")

    if urgency != "normal":
        parts.append(f"Urgency: {urgency}")

    if constraints:
        parts.append("Constraints: " + "; ".join(constraints))

    return "\n".join(parts)


def rewrite_to_prompt(raw_text: str) -> StructuredPrompt:
    """Transform raw verbatim speech into a structured agent-ready prompt.

    Returns a StructuredPrompt with extracted fields and a clean_text
    representation suitable for agents to consume.
    """
    text = raw_text.strip()
    if not text:
        return StructuredPrompt(
            action="none",
            subject="",
            context="",
            urgency="normal",
            raw_length=0,
            clean_text="[empty input]",
        )

    action = _extract_action(text)
    subject = _extract_subject(text)
    context = _extract_context(text, action, subject)
    urgency = _extract_urgency(text)
    constraints = _extract_constraints(text)

    clean_text = _build_clean_text(action, subject, context, urgency, constraints)

    return StructuredPrompt(
        action=action,
        subject=subject,
        context=context,
        urgency=urgency,
        constraints=constraints,
        raw_length=len(text),
        clean_text=clean_text,
    )
