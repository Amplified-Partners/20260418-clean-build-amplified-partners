"""Tests for epistemic_core.context_packet — PR 3.

Covers the three required test categories from IMPLEMENTATION_PLAN.md:
  1. Runtime packet cannot exist without canonical refs
  2. Malformed/invalid epistemic tier is rejected
  3. Mapper round-trips: Packet → ContextPacket → frontmatter → validates

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from epistemic_core.context_packet import (
    CanonicalRefs,
    ContextPacket,
    CuratorBlock,
    PermissionsBlock,
    PuddingBlock,
    RuntimeBlock,
    context_to_frontmatter,
    packet_to_context,
)
from epistemic_core.tiers import TIER_RANK


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PACKET_ID = uuid.uuid4()
_DOC_ID = uuid.uuid4()
_CHUNK_1 = uuid.uuid4()
_CHUNK_2 = uuid.uuid4()


def _make_runtime(tier: str = "STRUCTURED", **overrides: object) -> RuntimeBlock:
    defaults = {"epistemic_tier": tier}
    defaults.update(overrides)
    return RuntimeBlock(**defaults)


def _make_refs(**overrides: object) -> CanonicalRefs:
    defaults = {"brain_packet_id": _PACKET_ID}
    defaults.update(overrides)
    return CanonicalRefs(**defaults)


def _make_context(**overrides: object) -> ContextPacket:
    kw: dict = {
        "runtime": _make_runtime(),
        "canonical_refs": _make_refs(),
    }
    kw.update(overrides)
    return ContextPacket(**kw)


class _FakePacket:
    """Mimics brain_curator.models.Packet without importing it."""

    def __init__(self, **kwargs: object) -> None:
        self.packet_id = kwargs.get("packet_id", _PACKET_ID)
        self.packet_type = kwargs.get("packet_type", "claim")
        self.title = kwargs.get("title", "Test packet")
        self.summary = kwargs.get("summary", "A test summary")
        self.status = kwargs.get("status", "draft")
        self.route = kwargs.get("route", "agent_layer")
        self.epistemic_tier = kwargs.get("epistemic_tier", "STRUCTURED")
        self.claim_status = kwargs.get("claim_status", None)
        self.decision_state = kwargs.get("decision_state", None)
        self.valid_from = kwargs.get("valid_from", None)
        self.valid_to = kwargs.get("valid_to", None)
        self.last_verified_at = kwargs.get("last_verified_at", None)
        self.source_document_id = kwargs.get("source_document_id", _DOC_ID)
        self.metadata = kwargs.get("metadata", {})


# ===================================================================
# 1. Canonical refs required — no packet without provenance
# ===================================================================


class TestCanonicalRefsRequired:
    def test_construction_requires_canonical_refs(self) -> None:
        with pytest.raises(Exception):
            ContextPacket(runtime=_make_runtime())  # type: ignore[call-arg]

    def test_canonical_refs_requires_brain_packet_id(self) -> None:
        with pytest.raises(Exception):
            CanonicalRefs()  # type: ignore[call-arg]

    def test_valid_construction_succeeds(self) -> None:
        ctx = _make_context()
        assert ctx.canonical_refs.brain_packet_id == _PACKET_ID

    def test_optional_evidence_chunk_ids_default_empty(self) -> None:
        refs = _make_refs()
        assert refs.evidence_chunk_ids == []

    def test_evidence_chunk_ids_populated(self) -> None:
        refs = _make_refs(evidence_chunk_ids=[_CHUNK_1, _CHUNK_2])
        assert refs.evidence_chunk_ids == [_CHUNK_1, _CHUNK_2]


# ===================================================================
# 2. Malformed epistemic tier rejected
# ===================================================================


class TestEpistemicTierValidation:
    def test_valid_tiers_accepted(self) -> None:
        for tier in TIER_RANK:
            ctx = _make_context(runtime=_make_runtime(tier=tier))
            assert ctx.runtime.epistemic_tier == tier

    def test_invalid_tier_rejected(self) -> None:
        with pytest.raises(ValueError, match="epistemic_tier must be one of"):
            _make_context(runtime=_make_runtime(tier="HALLUCINATED"))

    def test_empty_tier_rejected(self) -> None:
        with pytest.raises(ValueError, match="epistemic_tier must be one of"):
            _make_context(runtime=_make_runtime(tier=""))

    def test_lowercase_tier_rejected(self) -> None:
        with pytest.raises(ValueError, match="epistemic_tier must be one of"):
            _make_context(runtime=_make_runtime(tier="structured"))


# ===================================================================
# 3. Mapper: packet_to_context
# ===================================================================


class TestPacketToContext:
    def test_basic_mapping(self) -> None:
        pkt = _FakePacket()
        ctx = packet_to_context(pkt)
        assert ctx.canonical_refs.brain_packet_id == _PACKET_ID
        assert ctx.canonical_refs.source_document_id == _DOC_ID
        assert ctx.runtime.epistemic_tier == "STRUCTURED"
        assert ctx.curator.packet_type == "claim"
        assert ctx.curator.title == "Test packet"

    def test_evidence_chunk_ids_passed_through(self) -> None:
        pkt = _FakePacket()
        ctx = packet_to_context(pkt, evidence_chunk_ids=[_CHUNK_1, _CHUNK_2])
        assert ctx.canonical_refs.evidence_chunk_ids == [_CHUNK_1, _CHUNK_2]

    def test_curation_run_id_passed_through(self) -> None:
        pkt = _FakePacket()
        ctx = packet_to_context(pkt, curation_run_id="run-abc-123")
        assert ctx.canonical_refs.curation_run_id == "run-abc-123"

    def test_missing_epistemic_tier_raises(self) -> None:
        pkt = _FakePacket(epistemic_tier=None)
        with pytest.raises(ValueError, match="must have epistemic_tier"):
            packet_to_context(pkt)

    def test_missing_packet_id_raises(self) -> None:
        pkt = _FakePacket(packet_id=None)
        with pytest.raises(ValueError, match="must have packet_id"):
            packet_to_context(pkt)

    def test_invalid_tier_string_raises(self) -> None:
        pkt = _FakePacket(epistemic_tier="HALLUCINATED")
        with pytest.raises(ValueError, match="must be one of"):
            packet_to_context(pkt)

    def test_permissions_defaults(self) -> None:
        pkt = _FakePacket()
        ctx = packet_to_context(pkt)
        assert ctx.permissions.pii_class == "none"
        assert ctx.permissions.allowed_uses == ["agent_retrieval"]
        assert ctx.permissions.forbidden_uses == []
        assert ctx.permissions.approval_required is False

    def test_permissions_overrides(self) -> None:
        pkt = _FakePacket()
        ctx = packet_to_context(
            pkt,
            pii_class="tokenised",
            allowed_uses=["research"],
            forbidden_uses=["marketing"],
            approval_required=True,
        )
        assert ctx.permissions.pii_class == "tokenised"
        assert ctx.permissions.allowed_uses == ["research"]
        assert ctx.permissions.forbidden_uses == ["marketing"]
        assert ctx.permissions.approval_required is True

    def test_pudding_label_mapped(self) -> None:
        pkt = _FakePacket()
        ctx = packet_to_context(pkt, pudding_label="OBS.QUA.IND.SNP")
        assert ctx.pudding.pudding_label == "OBS.QUA.IND.SNP"

    def test_runtime_fields_mapped(self) -> None:
        pkt = _FakePacket()
        ctx = packet_to_context(
            pkt,
            source_uri="/path/to/doc.md",
            source_owner="ewan",
            domain="plumbing",
            client_scope="dave-plumbing-ltd",
            project_scope="q3-review",
            recommended_use="agent_retrieval",
        )
        assert ctx.runtime.source_uri == "/path/to/doc.md"
        assert ctx.runtime.source_owner == "ewan"
        assert ctx.runtime.domain == "plumbing"
        assert ctx.runtime.client_scope == "dave-plumbing-ltd"
        assert ctx.runtime.project_scope == "q3-review"
        assert ctx.runtime.recommended_use == "agent_retrieval"

    def test_enum_tier_converted_to_string(self) -> None:
        from epistemic_core.tiers import EpistemicTier

        pkt = _FakePacket(epistemic_tier=EpistemicTier.MEASURED)
        ctx = packet_to_context(pkt)
        assert ctx.runtime.epistemic_tier == "MEASURED"

    def test_curator_block_populated(self) -> None:
        now = datetime.now(timezone.utc)
        pkt = _FakePacket(
            claim_status="verified",
            decision_state="accepted",
            valid_from=now,
            valid_to=now,
            last_verified_at=now,
            metadata={"key": "val"},
        )
        ctx = packet_to_context(pkt)
        assert ctx.curator.claim_status == "verified"
        assert ctx.curator.decision_state == "accepted"
        assert ctx.curator.valid_from == now
        assert ctx.curator.valid_to == now
        assert ctx.curator.last_verified_at == now
        assert ctx.curator.metadata == {"key": "val"}


# ===================================================================
# 4. Mapper: context_to_frontmatter
# ===================================================================


class TestContextToFrontmatter:
    def test_basic_frontmatter(self) -> None:
        ctx = _make_context()
        fm = context_to_frontmatter(ctx)
        assert fm["brain_packet_id"] == str(_PACKET_ID)
        assert fm["epistemic_tier"] == "STRUCTURED"
        assert fm["pii_class"] == "none"

    def test_optional_fields_included_when_set(self) -> None:
        ctx = _make_context(
            canonical_refs=_make_refs(
                source_document_id=_DOC_ID,
                evidence_chunk_ids=[_CHUNK_1],
                curation_run_id="run-xyz",
            ),
            curator=CuratorBlock(
                packet_type="claim", title="T", status="frozen", route="agent_layer"
            ),
            pudding=PuddingBlock(pudding_label="OBS.QUA.IND.SNP"),
            permissions=PermissionsBlock(
                forbidden_uses=["marketing"], approval_required=True
            ),
        )
        fm = context_to_frontmatter(ctx)
        assert fm["source_document_id"] == str(_DOC_ID)
        assert fm["evidence_chunk_ids"] == [str(_CHUNK_1)]
        assert fm["curation_run_id"] == "run-xyz"
        assert fm["packet_type"] == "claim"
        assert fm["title"] == "T"
        assert fm["status"] == "frozen"
        assert fm["route"] == "agent_layer"
        assert fm["pudding_label"] == "OBS.QUA.IND.SNP"
        assert fm["forbidden_uses"] == ["marketing"]
        assert fm["approval_required"] is True

    def test_optional_fields_omitted_when_none(self) -> None:
        ctx = _make_context()
        fm = context_to_frontmatter(ctx)
        assert "source_document_id" not in fm
        assert "evidence_chunk_ids" not in fm
        assert "curation_run_id" not in fm
        assert "pudding_label" not in fm
        assert "forbidden_uses" not in fm
        assert "approval_required" not in fm


# ===================================================================
# 5. Round-trip: Packet → ContextPacket → frontmatter → validates
# ===================================================================


class TestRoundTrip:
    def test_packet_to_context_to_frontmatter_round_trip(self) -> None:
        pkt = _FakePacket(
            epistemic_tier="MEASURED",
            source_document_id=_DOC_ID,
        )
        ctx = packet_to_context(
            pkt,
            evidence_chunk_ids=[_CHUNK_1, _CHUNK_2],
            curation_run_id="run-round-trip",
            pudding_label="THR.QUA.IND.SNP",
            domain="consulting",
        )
        fm = context_to_frontmatter(ctx)

        # Frontmatter must contain all canonical refs
        assert fm["brain_packet_id"] == str(_PACKET_ID)
        assert fm["source_document_id"] == str(_DOC_ID)
        assert len(fm["evidence_chunk_ids"]) == 2
        assert fm["curation_run_id"] == "run-round-trip"
        assert fm["epistemic_tier"] == "MEASURED"
        assert fm["pudding_label"] == "THR.QUA.IND.SNP"
        assert fm["domain"] == "consulting"

    def test_frontmatter_can_reconstruct_context_packet(self) -> None:
        """Frontmatter contains enough to build a new ContextPacket."""
        pkt = _FakePacket()
        ctx = packet_to_context(pkt, evidence_chunk_ids=[_CHUNK_1])
        fm = context_to_frontmatter(ctx)

        # Reconstruct from frontmatter
        ctx2 = ContextPacket(
            runtime=RuntimeBlock(epistemic_tier=fm["epistemic_tier"]),
            canonical_refs=CanonicalRefs(
                brain_packet_id=uuid.UUID(fm["brain_packet_id"]),
            ),
        )
        assert ctx2.runtime.epistemic_tier == ctx.runtime.epistemic_tier
        assert ctx2.canonical_refs.brain_packet_id == ctx.canonical_refs.brain_packet_id


# ===================================================================
# 6. Default block construction
# ===================================================================


class TestDefaultBlocks:
    def test_curator_block_defaults(self) -> None:
        ctx = _make_context()
        assert ctx.curator.packet_type is None
        assert ctx.curator.metadata == {}

    def test_pudding_block_defaults(self) -> None:
        ctx = _make_context()
        assert ctx.pudding.pudding_label is None
        assert ctx.pudding.what is None

    def test_permissions_block_defaults(self) -> None:
        ctx = _make_context()
        assert ctx.permissions.pii_class == "none"
        assert ctx.permissions.allowed_uses == ["agent_retrieval"]
        assert ctx.permissions.forbidden_uses == []
        assert ctx.permissions.approval_required is False

    def test_runtime_record_id_auto_generated(self) -> None:
        ctx1 = _make_context()
        ctx2 = _make_context()
        assert ctx1.runtime.record_id != ctx2.runtime.record_id


# ===================================================================
# 7. Identity integration with epistemic_core top-level
# ===================================================================


class TestTopLevelImports:
    def test_context_packet_importable_from_epistemic_core(self) -> None:
        from epistemic_core import ContextPacket as CP
        from epistemic_core import packet_to_context as ptc
        from epistemic_core import context_to_frontmatter as ctf

        assert CP is ContextPacket
        assert ptc is packet_to_context
        assert ctf is context_to_frontmatter
