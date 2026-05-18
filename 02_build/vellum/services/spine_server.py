"""Spine server — serve and update portable spines per-agent.

Pure domain logic. Storage is in-memory for now; will move to
PostgresSheetStore when Beast deployment is wired.

The spine is served on agent wakeup. Updated when a baton pass
contains learnings that change future behaviour.

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from vellum.models.spine import (
    BehaviouralPrior,
    FailurePattern,
    PortableSpine,
)

log = logging.getLogger("vellum.spine")

# In-memory spine store — keyed by (tenant_id, agent_id)
_spines: dict[tuple[str, str], PortableSpine] = {}


def get_spine(agent_id: str, tenant_id: str = "ewan") -> PortableSpine | None:
    """Read the portable spine for an agent. None if no spine registered."""
    return _spines.get((tenant_id, agent_id))


def list_spines(tenant_id: str = "ewan") -> list[PortableSpine]:
    """List all spines for a tenant."""
    return [s for k, s in _spines.items() if k[0] == tenant_id]


def register_spine(spine: PortableSpine) -> PortableSpine:
    """Register or replace a spine for an agent."""
    spine.updated_at = datetime.now(timezone.utc)
    _spines[(spine.tenant_id, spine.agent_id)] = spine
    log.info("Spine registered: agent=%s tenant=%s", spine.agent_id, spine.tenant_id)
    return spine


def update_spine_from_baton(
    agent_id: str,
    tenant_id: str,
    *,
    failed_paths: list[str] | None = None,
    if_then_lessons: list[str] | None = None,
    decision_log_refs: list[str] | None = None,
    experience_line: str | None = None,
    job_context: str | None = None,
) -> PortableSpine | None:
    """Update a spine with learnings from a baton pass.

    Only updates fields that are provided (non-None).
    Creates failure patterns from failed_paths.
    Appends IF-THEN lessons and decision log refs.
    """
    spine = _spines.get((tenant_id, agent_id))
    if spine is None:
        return None

    if failed_paths:
        for path in failed_paths:
            existing = [fp for fp in spine.failure_patterns if fp.description == path]
            if existing:
                existing[0].times_observed += 1
            else:
                spine.failure_patterns.append(
                    FailurePattern(description=path, source_session="baton")
                )

    if if_then_lessons:
        for lesson in if_then_lessons:
            if lesson not in spine.if_then_lessons:
                spine.if_then_lessons.append(lesson)

    if decision_log_refs:
        for ref in decision_log_refs:
            if ref not in spine.decision_log_refs:
                spine.decision_log_refs.append(ref)

    if experience_line is not None:
        spine.experience_line = experience_line

    if job_context is not None:
        spine.current_job_context = job_context

    spine.updated_at = datetime.now(timezone.utc)
    log.info("Spine updated from baton: agent=%s", agent_id)
    return spine


def clear_spines() -> None:
    """Clear all spines. For testing."""
    _spines.clear()
