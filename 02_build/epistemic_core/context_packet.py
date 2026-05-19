"""Runtime Context Packet — the 19-field envelope for governed retrieval.

A ContextPacket wraps a brain_curator Packet with runtime metadata,
canonical references, PUDDING frontmatter, and permission constraints.
It is the standard shape consumed by Brain MCP, agents, and downstream
consumers.

Invariants:
  - canonical_refs.brain_packet_id is required (must reference a real packet)
  - epistemic_tier is required and must be a valid tier string
  - Packets without canonical refs are rejected at construction time

This is a runtime envelope, NOT a second curation system. It does not
persist — it is constructed on-demand from brain_curator Packet + evidence.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator

from epistemic_core.tiers import TIER_RANK, EpistemicTier


# ---------------------------------------------------------------------------
# Block 1: Canonical References (required — no packet without provenance)
# ---------------------------------------------------------------------------


class CanonicalRefs(BaseModel):
    """Links back to the governed source in brain_curator tables."""

    brain_packet_id: uuid.UUID
    source_document_id: uuid.UUID | None = None
    evidence_chunk_ids: list[uuid.UUID] = Field(default_factory=list)
    curation_run_id: str | None = None


# ---------------------------------------------------------------------------
# Block 2: Runtime metadata
# ---------------------------------------------------------------------------


class RuntimeBlock(BaseModel):
    """Runtime fields populated at retrieval time."""

    record_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    source_uri: str | None = None
    source_type: str | None = None
    source_owner: str | None = None
    content_hash: str | None = None
    client_scope: str | None = None
    project_scope: str | None = None
    domain: str | None = None
    summary: str | None = None
    verbatim_excerpt: str | None = None
    epistemic_tier: str
    provenance_chain: list[str] = Field(default_factory=list)
    valid_until: datetime | None = None
    recommended_use: str | None = None


# ---------------------------------------------------------------------------
# Block 3: PUDDING frontmatter (optional — only if labelled)
# ---------------------------------------------------------------------------


class PuddingBlock(BaseModel):
    """PUDDING 2026 taxonomy label and metadata."""

    pudding_label: str | None = None  # e.g. "OBS.QUA.IND.SNP"
    what: str | None = None
    how: str | None = None
    scale: str | None = None
    time: str | None = None
    pattern: str | None = None
    domain_distance: float | None = None
    confidence: float | None = None


# ---------------------------------------------------------------------------
# Block 4: Permissions (what consumers may do with this packet)
# ---------------------------------------------------------------------------


class PermissionsBlock(BaseModel):
    """Access constraints for downstream consumers."""

    pii_class: str = "none"  # "none" | "tokenised" | "contains_pii"
    allowed_uses: list[str] = Field(default_factory=lambda: ["agent_retrieval"])
    forbidden_uses: list[str] = Field(default_factory=list)
    approval_required: bool = False


# ---------------------------------------------------------------------------
# Block 5: Curator snapshot (from brain_curator.models.Packet)
# ---------------------------------------------------------------------------


class CuratorBlock(BaseModel):
    """Snapshot of brain_curator Packet fields at retrieval time."""

    packet_type: str | None = None
    title: str | None = None
    status: str | None = None
    route: str | None = None
    claim_status: str | None = None
    decision_state: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    last_verified_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Top-level ContextPacket
# ---------------------------------------------------------------------------

_VALID_TIERS = set(TIER_RANK.keys())


class ContextPacket(BaseModel):
    """The 19-field runtime envelope for governed retrieval.

    Construction requires:
      - canonical_refs with a valid brain_packet_id
      - runtime.epistemic_tier set to a valid tier string

    This is the shape consumed by Brain MCP, agents, and downstream systems.
    """

    runtime: RuntimeBlock
    canonical_refs: CanonicalRefs
    curator: CuratorBlock = Field(default_factory=CuratorBlock)
    pudding: PuddingBlock = Field(default_factory=PuddingBlock)
    permissions: PermissionsBlock = Field(default_factory=PermissionsBlock)

    @model_validator(mode="after")
    def _validate_tier(self) -> ContextPacket:
        tier = self.runtime.epistemic_tier
        if tier not in _VALID_TIERS:
            raise ValueError(
                f"epistemic_tier must be one of {sorted(_VALID_TIERS)}, got {tier!r}"
            )
        return self


# ---------------------------------------------------------------------------
# Mapper: brain_curator Packet → ContextPacket
# ---------------------------------------------------------------------------


def packet_to_context(
    packet: Any,
    *,
    evidence_chunk_ids: list[uuid.UUID] | None = None,
    curation_run_id: str | None = None,
    source_uri: str | None = None,
    source_owner: str | None = None,
    content_hash: str | None = None,
    client_scope: str | None = None,
    project_scope: str | None = None,
    domain: str | None = None,
    summary: str | None = None,
    verbatim_excerpt: str | None = None,
    recommended_use: str | None = None,
    pudding_label: str | None = None,
    pii_class: str = "none",
    allowed_uses: list[str] | None = None,
    forbidden_uses: list[str] | None = None,
    approval_required: bool = False,
) -> ContextPacket:
    """Map a brain_curator Packet to a ContextPacket.

    Requires packet.packet_id and packet.epistemic_tier to be set.
    Raises ValueError if epistemic_tier is missing or invalid.
    """
    tier = getattr(packet, "epistemic_tier", None)
    if not tier:
        raise ValueError("Packet must have epistemic_tier set")
    if isinstance(tier, EpistemicTier):
        tier_str = tier.name
    else:
        tier_str = str(tier).upper()
    if tier_str not in _VALID_TIERS:
        raise ValueError(
            f"Packet epistemic_tier must be one of {sorted(_VALID_TIERS)}, got {tier_str!r}"
        )

    packet_id = getattr(packet, "packet_id", None)
    if packet_id is None:
        raise ValueError("Packet must have packet_id set")

    return ContextPacket(
        runtime=RuntimeBlock(
            source_uri=source_uri or getattr(packet, "source_path", None),
            source_type=getattr(packet, "packet_type", None),
            source_owner=source_owner,
            content_hash=content_hash,
            client_scope=client_scope,
            project_scope=project_scope,
            domain=domain,
            summary=summary or getattr(packet, "summary", None),
            verbatim_excerpt=verbatim_excerpt,
            epistemic_tier=tier_str,
            provenance_chain=[],
            valid_until=getattr(packet, "valid_to", None),
            recommended_use=recommended_use,
        ),
        canonical_refs=CanonicalRefs(
            brain_packet_id=packet_id,
            source_document_id=getattr(packet, "source_document_id", None),
            evidence_chunk_ids=evidence_chunk_ids or [],
            curation_run_id=curation_run_id,
        ),
        curator=CuratorBlock(
            packet_type=getattr(packet, "packet_type", None),
            title=getattr(packet, "title", None),
            status=getattr(packet, "status", None),
            route=getattr(packet, "route", None),
            claim_status=getattr(packet, "claim_status", None),
            decision_state=getattr(packet, "decision_state", None),
            valid_from=getattr(packet, "valid_from", None),
            valid_to=getattr(packet, "valid_to", None),
            last_verified_at=getattr(packet, "last_verified_at", None),
            metadata=getattr(packet, "metadata", None) or {},
        ),
        pudding=PuddingBlock(pudding_label=pudding_label),
        permissions=PermissionsBlock(
            pii_class=pii_class,
            allowed_uses=allowed_uses or ["agent_retrieval"],
            forbidden_uses=forbidden_uses or [],
            approval_required=approval_required,
        ),
    )


# ---------------------------------------------------------------------------
# Mapper: ContextPacket → curator frontmatter dict
# ---------------------------------------------------------------------------


def context_to_frontmatter(ctx: ContextPacket) -> dict[str, Any]:
    """Convert a ContextPacket back to a flat frontmatter-style dict.

    Useful for round-trip validation and for writing governed YAML
    frontmatter into markdown files.
    """
    fm: dict[str, Any] = {
        "brain_packet_id": str(ctx.canonical_refs.brain_packet_id),
        "epistemic_tier": ctx.runtime.epistemic_tier,
    }
    if ctx.canonical_refs.source_document_id:
        fm["source_document_id"] = str(ctx.canonical_refs.source_document_id)
    if ctx.canonical_refs.evidence_chunk_ids:
        fm["evidence_chunk_ids"] = [
            str(cid) for cid in ctx.canonical_refs.evidence_chunk_ids
        ]
    if ctx.canonical_refs.curation_run_id:
        fm["curation_run_id"] = ctx.canonical_refs.curation_run_id

    if ctx.curator.packet_type:
        fm["packet_type"] = ctx.curator.packet_type
    if ctx.curator.title:
        fm["title"] = ctx.curator.title
    if ctx.curator.status:
        fm["status"] = ctx.curator.status
    if ctx.curator.route:
        fm["route"] = ctx.curator.route

    if ctx.pudding.pudding_label:
        fm["pudding_label"] = ctx.pudding.pudding_label

    fm["pii_class"] = ctx.permissions.pii_class
    if ctx.permissions.forbidden_uses:
        fm["forbidden_uses"] = ctx.permissions.forbidden_uses
    if ctx.permissions.approval_required:
        fm["approval_required"] = True

    if ctx.runtime.valid_until:
        fm["valid_until"] = ctx.runtime.valid_until.isoformat()
    if ctx.runtime.domain:
        fm["domain"] = ctx.runtime.domain
    if ctx.runtime.recommended_use:
        fm["recommended_use"] = ctx.runtime.recommended_use

    return fm
