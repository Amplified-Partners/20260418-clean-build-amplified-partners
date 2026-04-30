"""
AG2 Executive Team — GroupChat with Believability-Weighted Speaker Selection
=============================================================================
The "brain" of Cove. Five AI executives that collaborate on decisions,
planning, and operational oversight for Amplified Partners.

Architecture:
  - AG2 (AutoGen) GroupChat manages multi-turn conversation
  - Speaker selection weighted by "believability" scores per topic
  - Chief of Staff (CoS) is the orchestrator/router
  - All executives share a common context via the chat history
  - Each executive has MCP server access for their domain tools

Usage:
    team = await build_executive_team()
    result = await team.discuss("What should our Q2 priorities be?")
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ─── Executive Roles ────────────────────────────────────────────────


class ExecRole(str, Enum):
    CHIEF_OF_STAFF = "chief_of_staff"
    CFO = "cfo"
    CTO = "cto"
    COO = "coo"
    CMO = "cmo"


@dataclass
class ExecConfig:
    """Configuration for an AI executive."""
    role: ExecRole
    display_name: str
    title: str
    model_tier: str
    system_prompt_file: str
    mcp_servers: list[str] = field(default_factory=list)
    temperature: float = 0.3          # Slightly creative for exec discussions
    max_tokens: int = 4096
    believability: dict[str, float] = field(default_factory=dict)
    description: str = ""


# ─── Believability Weights ──────────────────────────────────────────
# Each executive has topic-level believability scores (0.0 - 1.0).
# Higher = more likely to speak on that topic.
# CoS always gets a base weight as orchestrator.

TOPIC_DOMAINS = [
    "strategy", "finance", "technology", "operations", "marketing",
    "sales", "hr", "legal", "product", "partnerships", "security",
    "infrastructure", "customer", "data", "ai", "compliance",
]


# ─── Executive Registry ─────────────────────────────────────────────

EXECUTIVE_REGISTRY: dict[ExecRole, ExecConfig] = {
    ExecRole.CHIEF_OF_STAFF: ExecConfig(
        role=ExecRole.CHIEF_OF_STAFF,
        display_name="Alex",
        title="Chief of Staff",
        model_tier="premium",
        system_prompt_file="agents/prompts/executive/chief_of_staff.md",
        mcp_servers=[
            "postgresql_mcp", "litellm_mcp", "langfuse_mcp",
            "telegram_mcp", "email_mcp", "nightscout_mcp",
        ],
        believability={
            "strategy": 0.9, "operations": 0.7, "partnerships": 0.8,
            "product": 0.7, "hr": 0.6, "compliance": 0.5,
        },
        description=(
            "Orchestrates the executive team. Routes questions to the right exec. "
            "Synthesises decisions. Reports to Ewan. Has access to all systems."
        ),
    ),
    ExecRole.CFO: ExecConfig(
        role=ExecRole.CFO,
        display_name="Morgan",
        title="Chief Financial Officer",
        model_tier="premium",
        system_prompt_file="agents/prompts/executive/cfo.md",
        mcp_servers=["postgresql_mcp", "langfuse_mcp", "litellm_mcp"],
        believability={
            "finance": 0.95, "compliance": 0.8, "strategy": 0.6,
            "operations": 0.5, "legal": 0.7, "sales": 0.4,
        },
        description=(
            "Financial oversight: costs, revenue, margins, forecasting. "
            "Tracks AI spend via Langfuse. Watches burn rate like a hawk."
        ),
    ),
    ExecRole.CTO: ExecConfig(
        role=ExecRole.CTO,
        display_name="Dev",
        title="Chief Technology Officer",
        model_tier="premium",
        system_prompt_file="agents/prompts/executive/cto.md",
        mcp_servers=[
            "postgresql_mcp", "github_mcp", "filesystem_mcp",
            "litellm_mcp", "langfuse_mcp",
        ],
        believability={
            "technology": 0.95, "infrastructure": 0.9, "security": 0.8,
            "ai": 0.9, "data": 0.8, "product": 0.6,
        },
        description=(
            "Technical architecture, infrastructure, AI model selection, "
            "security posture. Owns Beast server and all self-hosted services."
        ),
    ),
    ExecRole.COO: ExecConfig(
        role=ExecRole.COO,
        display_name="Sam",
        title="Chief Operating Officer",
        model_tier="medium",
        system_prompt_file="agents/prompts/executive/coo.md",
        mcp_servers=[
            "postgresql_mcp", "email_mcp", "telegram_mcp",
        ],
        believability={
            "operations": 0.95, "customer": 0.8, "hr": 0.7,
            "compliance": 0.6, "sales": 0.5, "product": 0.5,
        },
        description=(
            "Day-to-day operations: client onboarding, service delivery, "
            "process optimisation, team workflows. Keeps the machine running."
        ),
    ),
    ExecRole.CMO: ExecConfig(
        role=ExecRole.CMO,
        display_name="Riley",
        title="Chief Marketing Officer",
        model_tier="medium",
        system_prompt_file="agents/prompts/executive/cmo.md",
        mcp_servers=[
            "postgresql_mcp", "nightscout_mcp",
        ],
        believability={
            "marketing": 0.95, "sales": 0.7, "partnerships": 0.6,
            "customer": 0.7, "product": 0.5, "strategy": 0.4,
        },
        description=(
            "Market positioning, content strategy, lead generation, "
            "brand voice. Uses NightScout intel for content opportunities."
        ),
    ),
}


# ─── Believability Speaker Selection ────────────────────────────────


def compute_speaker_weights(
    topic_keywords: list[str],
    exclude_roles: list[ExecRole] | None = None,
) -> dict[ExecRole, float]:
    """
    Compute which executive should speak based on topic keywords.
    Returns normalised weights (sum = 1.0).

    The CoS always gets a minimum base weight of 0.15 as orchestrator.
    """
    exclude = set(exclude_roles or [])
    raw_weights: dict[ExecRole, float] = {}

    for role, config in EXECUTIVE_REGISTRY.items():
        if role in exclude:
            continue

        # Sum believability scores for matching topics
        score = 0.0
        matched = 0
        for keyword in topic_keywords:
            kw = keyword.lower().strip()
            if kw in config.believability:
                score += config.believability[kw]
                matched += 1

        # Average if multiple keywords match, else small base weight
        if matched > 0:
            score = score / matched
        else:
            score = 0.1  # Base weight — everyone gets a voice

        # CoS orchestrator bonus
        if role == ExecRole.CHIEF_OF_STAFF:
            score = max(score, 0.15)

        raw_weights[role] = score

    # Normalise to sum = 1.0
    total = sum(raw_weights.values())
    if total == 0:
        # Equal weights if nothing matches
        n = len(raw_weights)
        return {r: 1.0 / n for r in raw_weights}

    return {r: w / total for r, w in raw_weights.items()}


def select_speaker(
    topic_keywords: list[str],
    last_speaker: ExecRole | None = None,
) -> ExecRole:
    """
    Select the next speaker using weighted random selection.
    Avoids same speaker twice in a row (unless they're the clear expert).
    """
    import random

    exclude = []
    weights = compute_speaker_weights(topic_keywords, exclude)

    # If last speaker has < 0.5 weight, deprioritise them
    if last_speaker and last_speaker in weights:
        if weights[last_speaker] < 0.5:
            weights[last_speaker] *= 0.3  # Reduce repeat probability

    # Renormalise
    total = sum(weights.values())
    normalised = {r: w / total for r, w in weights.items()}

    roles = list(normalised.keys())
    probs = list(normalised.values())

    return random.choices(roles, weights=probs, k=1)[0]


# ─── Topic Extraction (simple keyword approach) ─────────────────────


TOPIC_KEYWORDS_MAP: dict[str, list[str]] = {
    "money": ["finance"], "cost": ["finance"], "revenue": ["finance", "sales"],
    "budget": ["finance"], "spend": ["finance"], "margin": ["finance"],
    "server": ["technology", "infrastructure"], "code": ["technology"],
    "deploy": ["technology", "operations"], "model": ["ai", "technology"],
    "client": ["customer", "sales", "operations"], "onboard": ["operations", "customer"],
    "lead": ["marketing", "sales"], "content": ["marketing"],
    "brand": ["marketing"], "seo": ["marketing"],
    "hire": ["hr"], "team": ["hr", "operations"],
    "security": ["security", "compliance"], "gdpr": ["compliance", "legal"],
    "pipeline": ["operations", "technology"], "process": ["operations"],
    "partner": ["partnerships", "strategy"], "strategy": ["strategy"],
    "product": ["product"], "roadmap": ["product", "strategy"],
    "data": ["data", "technology"], "ai": ["ai", "technology"],
    "nightscout": ["strategy", "marketing", "ai"],
    "email": ["operations", "customer"],
}


def extract_topics(text: str) -> list[str]:
    """Extract topic domains from natural language text."""
    text_lower = text.lower()
    topics: set[str] = set()
    for keyword, domains in TOPIC_KEYWORDS_MAP.items():
        if keyword in text_lower:
            topics.update(domains)
    return list(topics) if topics else ["strategy"]  # Default to strategy


# ─── Team Builder ───────────────────────────────────────────────────


def get_executive(role: ExecRole) -> ExecConfig:
    """Get executive config by role."""
    return EXECUTIVE_REGISTRY[role]


def get_all_executives() -> list[ExecConfig]:
    """Get all executive configs in order."""
    return list(EXECUTIVE_REGISTRY.values())
