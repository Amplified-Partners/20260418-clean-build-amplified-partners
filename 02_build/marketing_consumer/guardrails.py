"""Radical Honesty guardrails for marketing content.

Every marketing artifact must pass these checks before publication:
  1. Permission basis — artifact references a governed brain_packet_id
  2. No fake persona — persona field must not impersonate a real person
  3. Attribution — all claims must have evidence_refs
  4. Unsourced factual claim detection — content scanned for claim patterns
     without corresponding evidence

Marketing-Kaizen emits candidates, never canonical truth.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from marketing_consumer.models import MarketingArtifact


# ---------------------------------------------------------------------------
# Known fake / impersonation persona patterns
# ---------------------------------------------------------------------------

FORBIDDEN_PERSONA_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bceo\b", re.IGNORECASE),
    re.compile(r"\bfounder\b", re.IGNORECASE),
    re.compile(r"\bdr\.?\s", re.IGNORECASE),
    re.compile(r"\bprofessor\b", re.IGNORECASE),
]

# Patterns suggesting factual claims in content
FACTUAL_CLAIM_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\d+%"),  # percentages
    re.compile(r"\bstud(?:y|ies)\s+(?:show|found|prove)", re.IGNORECASE),
    re.compile(r"\bresearch\s+(?:shows?|proves?|confirms?)", re.IGNORECASE),
    re.compile(r"\baccording\s+to\b", re.IGNORECASE),
    re.compile(r"\bscientifically\s+proven\b", re.IGNORECASE),
    re.compile(r"\b(?:proven|guaranteed)\s+(?:to|results?)\b", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Check result
# ---------------------------------------------------------------------------


@dataclass
class GuardrailResult:
    """Result of running all guardrail checks."""

    passed: bool
    violations: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def check_permission_basis(artifact: MarketingArtifact) -> list[str]:
    """Artifact must reference a governed brain_packet_id."""
    violations: list[str] = []
    if not artifact.brain_packet_id.strip():
        violations.append(
            "Missing brain_packet_id — artifact must reference "
            "a governed packet from the shared substrate."
        )
    return violations


def check_no_fake_persona(artifact: MarketingArtifact) -> list[str]:
    """Persona must not impersonate authority figures."""
    violations: list[str] = []
    persona = artifact.persona.strip()
    if not persona:
        return violations
    for pattern in FORBIDDEN_PERSONA_PATTERNS:
        if pattern.search(persona):
            violations.append(
                f"Forbidden persona pattern detected: '{persona}' "
                f"matches '{pattern.pattern}'. Marketing must not "
                "impersonate authority figures."
            )
    return violations


def check_attribution(artifact: MarketingArtifact) -> list[str]:
    """Content with factual claims must have evidence_refs."""
    violations: list[str] = []
    content = artifact.content
    has_claims = any(p.search(content) for p in FACTUAL_CLAIM_PATTERNS)
    if has_claims and not artifact.evidence_refs:
        violations.append(
            "Content contains factual claims but has no evidence_refs. "
            "Radical Honesty requires attribution for all factual claims."
        )
    return violations


def check_unsourced_claims(artifact: MarketingArtifact) -> list[str]:
    """Detect unsourced factual claims in content."""
    violations: list[str] = []
    content = artifact.content
    for pattern in FACTUAL_CLAIM_PATTERNS:
        matches = pattern.findall(content)
        if matches and not artifact.evidence_refs:
            violations.append(
                f"Unsourced factual claim detected (pattern: "
                f"'{pattern.pattern}'). Provide evidence_refs."
            )
            break
    return violations


# ---------------------------------------------------------------------------
# Combined check
# ---------------------------------------------------------------------------


def run_guardrails(artifact: MarketingArtifact) -> GuardrailResult:
    """Run all Radical Honesty guardrail checks.

    Returns a GuardrailResult with passed=True only if all checks pass.
    """
    violations: list[str] = []
    violations.extend(check_permission_basis(artifact))
    violations.extend(check_no_fake_persona(artifact))
    violations.extend(check_attribution(artifact))
    violations.extend(check_unsourced_claims(artifact))
    return GuardrailResult(passed=len(violations) == 0, violations=violations)
