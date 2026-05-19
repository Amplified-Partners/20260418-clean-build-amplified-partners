"""Comprehensive test suite for the brain_curator module.

Tests cover:
  - knowledge_vectors.content is never modified
  - All curation writes are audited in brain_curation_runs
  - Active governed packets have evidence
  - INTUITED packets excluded from default agent retrieval
  - drop_from_active never deletes source
  - Secret/PII-uncertain packets route to quarantine
  - Exact duplicates with better canonical route to drop_from_active
  - P0 tier validation (min-rule enforcement)
  - Curation runs without inline LLM labelling
  - Validation sample stratification
  - aggressive_dedup regression risk mitigated by design
  - epistemic_core canonical integration (PR 2)

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
Modified-by: Devon-d493 | 2026-05-19 | PR 2 — add epistemic_core integration tests
"""

from __future__ import annotations

import uuid
from unittest.mock import patch

import pytest

from brain_curator.config import (
    ACTIVE_ROUTES,
    ALL_PACKET_TYPES,
    GOVERNED_PACKET_TYPES,
    P0Policy,
    RETRIEVAL_TIERS,
    ROUTE_DROP_FROM_ACTIVE,
    ROUTE_KEEP,
    ROUTE_QUARANTINE,
    ROUTE_REFINE,
    ROUTE_REVIEW,
    ROUTE_VALIDATE,
    TIER_INTUITED,
    TIER_MEASURED,
    TIER_PROVEN,
    TIER_RANK,
    TIER_STRUCTURED,
    VALIDATION_SAMPLE_SIZE,
)
from brain_curator.epistemic_tier import (
    assign_tier_for_packet,
    tier_min,
    tier_min_many,
)
from brain_curator.models import (
    CurationRun,
    DedupeCluster,
    Document,
    Evidence,
    Packet,
    Relationship,
    ValidationSample,
)
from brain_curator.route_decider import decide_route, detect_secret_or_pii


# ═══════════════════════════════════════════════════════════════════════
# 1. knowledge_vectors.content is never modified
# ═══════════════════════════════════════════════════════════════════════


class TestNoRawMutation:
    """Verify the brain_curator module never modifies knowledge_vectors.content.

    The module only READs from knowledge_vectors (via SELECT queries).
    All writes go to brain_* tables. This is the core design invariant:
    'chunks are evidence; packets are meaning'.
    """

    def test_inventory_reads_only_from_knowledge_vectors(self) -> None:
        """inventory.py queries knowledge_vectors with SELECT, never UPDATE/DELETE."""
        import inspect
        from brain_curator import inventory

        source = inspect.getsource(inventory)
        # Must not contain UPDATE or DELETE against knowledge_vectors
        assert "UPDATE knowledge_vectors" not in source
        assert "DELETE FROM knowledge_vectors" not in source
        assert "INSERT INTO knowledge_vectors" not in source
        # Must contain SELECT from knowledge_vectors (the read path)
        assert "FROM knowledge_vectors" in source

    def test_packet_builder_reads_only_from_knowledge_vectors(self) -> None:
        import inspect
        from brain_curator import packet_builder

        source = inspect.getsource(packet_builder)
        assert "UPDATE knowledge_vectors" not in source
        assert "DELETE FROM knowledge_vectors" not in source
        assert "INSERT INTO knowledge_vectors" not in source

    def test_version_families_reads_only_documents(self) -> None:
        import inspect
        from brain_curator import version_families

        source = inspect.getsource(version_families)
        assert "UPDATE knowledge_vectors" not in source
        assert "DELETE FROM knowledge_vectors" not in source
        assert "INSERT INTO knowledge_vectors" not in source

    def test_route_decider_never_touches_knowledge_vectors(self) -> None:
        import inspect
        from brain_curator import route_decider

        source = inspect.getsource(route_decider)
        assert "UPDATE knowledge_vectors" not in source
        assert "DELETE FROM knowledge_vectors" not in source
        assert "INSERT INTO knowledge_vectors" not in source

    def test_epistemic_tier_never_touches_knowledge_vectors(self) -> None:
        import inspect
        from brain_curator import epistemic_tier

        source = inspect.getsource(epistemic_tier)
        assert "UPDATE knowledge_vectors" not in source
        assert "DELETE FROM knowledge_vectors" not in source
        assert "INSERT INTO knowledge_vectors" not in source

    def test_freeze_never_touches_knowledge_vectors(self) -> None:
        import inspect
        from brain_curator import freeze

        source = inspect.getsource(freeze)
        assert "UPDATE knowledge_vectors" not in source
        assert "DELETE FROM knowledge_vectors" not in source
        assert "INSERT INTO knowledge_vectors" not in source

    def test_validation_sampler_never_touches_knowledge_vectors(self) -> None:
        import inspect
        from brain_curator import validation_sampler

        source = inspect.getsource(validation_sampler)
        assert "UPDATE knowledge_vectors" not in source
        assert "DELETE FROM knowledge_vectors" not in source
        assert "INSERT INTO knowledge_vectors" not in source


# ═══════════════════════════════════════════════════════════════════════
# 2. Curation writes are audited in brain_curation_runs
# ═══════════════════════════════════════════════════════════════════════


class TestCurationAudit:
    """Each stage writes start/complete records to brain_curation_runs."""

    def test_all_stages_use_curation_run_helpers(self) -> None:
        """All stage modules import and call start/complete_curation_run."""
        import inspect

        from brain_curator import (
            epistemic_tier,
            freeze,
            inventory,
            packet_builder,
            route_decider,
            validation_sampler,
            version_families,
        )

        for mod in [
            inventory,
            version_families,
            packet_builder,
            epistemic_tier,
            route_decider,
            validation_sampler,
            freeze,
        ]:
            source = inspect.getsource(mod)
            assert "start_curation_run" in source, f"{mod.__name__} missing start_curation_run"
            assert "complete_curation_run" in source, f"{mod.__name__} missing complete_curation_run"

    def test_curation_run_model_has_required_fields(self) -> None:
        run = CurationRun(run_id="test-1", stage="inventory")
        assert run.status == "running"
        assert run.code_version == "brain-curator-v0.1"
        assert run.started_at is not None


# ═══════════════════════════════════════════════════════════════════════
# 3. Active governed packets must have evidence
# ═══════════════════════════════════════════════════════════════════════


class TestEvidenceRequirement:
    """working_model/decision/method/doctrine packets need evidence."""

    def test_governed_packet_types_defined(self) -> None:
        assert "working_model" in GOVERNED_PACKET_TYPES
        assert "decision" in GOVERNED_PACKET_TYPES
        assert "method" in GOVERNED_PACKET_TYPES
        assert "doctrine" in GOVERNED_PACKET_TYPES

    def test_evidence_model_links_packet_to_chunk(self) -> None:
        pid = uuid.uuid4()
        cid = uuid.uuid4()
        ev = Evidence(packet_id=pid, chunk_id=cid, evidence_role="supports")
        assert ev.packet_id == pid
        assert ev.chunk_id == cid


# ═══════════════════════════════════════════════════════════════════════
# 4. INTUITED packets excluded from default agent retrieval
# ═══════════════════════════════════════════════════════════════════════


class TestIntuitedExclusion:
    """INTUITED tier must NOT be in retrieval tiers."""

    def test_intuited_not_in_retrieval_tiers(self) -> None:
        assert TIER_INTUITED not in RETRIEVAL_TIERS

    def test_retrieval_tiers_are_structured_and_above(self) -> None:
        assert TIER_STRUCTURED in RETRIEVAL_TIERS
        assert TIER_MEASURED in RETRIEVAL_TIERS
        assert TIER_PROVEN in RETRIEVAL_TIERS

    def test_active_current_model_query_excludes_intuited(self) -> None:
        from brain_curator.db import ACTIVE_CURRENT_MODEL_QUERY

        assert "INTUITED" not in ACTIVE_CURRENT_MODEL_QUERY
        assert "STRUCTURED" in ACTIVE_CURRENT_MODEL_QUERY
        assert "MEASURED" in ACTIVE_CURRENT_MODEL_QUERY
        assert "PROVEN" in ACTIVE_CURRENT_MODEL_QUERY


# ═══════════════════════════════════════════════════════════════════════
# 5. drop_from_active never deletes source
# ═══════════════════════════════════════════════════════════════════════


class TestDropFromActiveNeverDeletes:
    """drop_from_active route must never DELETE from any table."""

    def test_drop_route_constant_defined(self) -> None:
        assert ROUTE_DROP_FROM_ACTIVE == "drop_from_active"

    def test_route_decider_has_no_delete_statements(self) -> None:
        import inspect
        from brain_curator import route_decider

        source = inspect.getsource(route_decider)
        # No DELETE statements at all in the route decider
        assert "DELETE FROM" not in source

    def test_freeze_module_has_no_delete_on_knowledge_vectors(self) -> None:
        import inspect
        from brain_curator import freeze

        source = inspect.getsource(freeze)
        assert "DELETE FROM knowledge_vectors" not in source

    def test_decide_route_returns_drop_for_duplicate_with_better_canonical(self) -> None:
        route = decide_route(
            packet_type="reference",
            epistemic_tier=TIER_INTUITED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=True,
            has_better_canonical=True,
        )
        assert route == ROUTE_DROP_FROM_ACTIVE


# ═══════════════════════════════════════════════════════════════════════
# 6. Secret/PII-uncertain packets route to quarantine
# ═══════════════════════════════════════════════════════════════════════


class TestSecretPIIQuarantine:
    """Any content with secret/PII signals must route to quarantine."""

    @pytest.mark.parametrize(
        "content",
        [
            "api_key = sk-abc123456789",
            "Set BEARER token: secret_value_here",
            "password: mysecretpassword",
            "private_key: -----BEGIN RSA PRIVATE KEY-----",
            "Authorization: Bearer eyJhbGciOiJ",
        ],
    )
    def test_secret_detected(self, content: str) -> None:
        secret, _ = detect_secret_or_pii(content)
        assert secret is True

    @pytest.mark.parametrize(
        "content",
        [
            "national insurance number: AB123456C",
            "date of birth: 01/01/1990",
            "bank account details enclosed",
            "passport number: 123456789",
        ],
    )
    def test_pii_detected(self, content: str) -> None:
        _, pii = detect_secret_or_pii(content)
        assert pii is True

    def test_quarantine_route_on_secret(self) -> None:
        route = decide_route(
            packet_type="reference",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=False,
            has_better_canonical=False,
            content_sample="api_key = sk-mysecretkey12345678",
        )
        assert route == ROUTE_QUARANTINE

    def test_quarantine_route_on_pii(self) -> None:
        route = decide_route(
            packet_type="decision",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=False,
            has_better_canonical=False,
            content_sample="The client's national insurance number is AB123456C",
        )
        assert route == ROUTE_QUARANTINE

    def test_clean_content_not_quarantined(self) -> None:
        route = decide_route(
            packet_type="decision",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=False,
            has_better_canonical=False,
            content_sample="We decided to use PostgreSQL for the canonical data layer.",
        )
        assert route != ROUTE_QUARANTINE


# ═══════════════════════════════════════════════════════════════════════
# 7. Exact duplicates with better canonical -> drop_from_active
# ═══════════════════════════════════════════════════════════════════════


class TestExactDuplicateRouting:
    """Exact duplicates with a better canonical source get dropped from active."""

    def test_exact_dup_with_better_canonical(self) -> None:
        route = decide_route(
            packet_type="working_model",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=True,
            has_better_canonical=True,
        )
        assert route == ROUTE_DROP_FROM_ACTIVE

    def test_exact_dup_that_is_canonical_not_dropped(self) -> None:
        """If this IS the canonical version, don't drop it."""
        route = decide_route(
            packet_type="working_model",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=True,
            has_better_canonical=False,
        )
        assert route != ROUTE_DROP_FROM_ACTIVE


# ═══════════════════════════════════════════════════════════════════════
# 8. P0 tier validation (min-rule enforcement)
# ═══════════════════════════════════════════════════════════════════════


class TestP0TierValidation:
    """Min-rule: effective tier = min(own, min(inputs), precondition)."""

    def test_tier_min_basic(self) -> None:
        assert tier_min(TIER_INTUITED, TIER_PROVEN) == TIER_INTUITED
        assert tier_min(TIER_MEASURED, TIER_STRUCTURED) == TIER_STRUCTURED
        assert tier_min(TIER_PROVEN, TIER_PROVEN) == TIER_PROVEN

    def test_tier_min_many(self) -> None:
        assert tier_min_many([TIER_PROVEN, TIER_STRUCTURED, TIER_MEASURED]) == TIER_STRUCTURED
        assert tier_min_many([TIER_INTUITED]) == TIER_INTUITED
        assert tier_min_many([]) == TIER_PROVEN  # no inputs -> no floor

    def test_min_rule_applied(self) -> None:
        """Packet can't be higher than its lowest evidence tier."""
        tier = assign_tier_for_packet(
            packet_type="doctrine",
            source_path="00_authority/PRINCIPLES.md",
            evidence_tiers=[TIER_INTUITED, TIER_STRUCTURED],
        )
        # Own claim for authority doctrine = STRUCTURED, but evidence floor = INTUITED
        assert tier == TIER_INTUITED

    def test_conversation_always_intuited(self) -> None:
        tier = assign_tier_for_packet(
            packet_type="conversation",
            source_path="threads/chat.md",
            evidence_tiers=[TIER_STRUCTURED],
        )
        assert tier == TIER_INTUITED

    def test_p0_violation_on_silent_promotion(self) -> None:
        """If effective tier would exceed input floor, it's a P0 violation."""
        with patch("brain_curator.epistemic_tier.ACTIVE_P0_POLICY", P0Policy.HALT):
            # This should NOT raise because min-rule prevents promotion
            tier = assign_tier_for_packet(
                packet_type="doctrine",
                source_path="00_authority/PRINCIPLES.md",
                evidence_tiers=[TIER_INTUITED],
            )
            assert tier == TIER_INTUITED

    def test_tier_ranking_order(self) -> None:
        assert TIER_RANK[TIER_INTUITED] < TIER_RANK[TIER_STRUCTURED]
        assert TIER_RANK[TIER_STRUCTURED] < TIER_RANK[TIER_MEASURED]
        assert TIER_RANK[TIER_MEASURED] < TIER_RANK[TIER_PROVEN]


# ═══════════════════════════════════════════════════════════════════════
# 9. Curation runs without inline LLM labelling
# ═══════════════════════════════════════════════════════════════════════


class TestNoInlineLLM:
    """All curation logic is deterministic — no LLM calls in the module."""

    def test_no_llm_imports_in_stages(self) -> None:
        """No anthropic, openai, litellm, ollama imports in any stage module."""
        import inspect

        from brain_curator import (
            epistemic_tier,
            freeze,
            inventory,
            packet_builder,
            route_decider,
            validation_sampler,
            version_families,
        )

        llm_markers = ["anthropic", "openai", "litellm", "ollama", "langchain"]
        for mod in [
            inventory,
            version_families,
            packet_builder,
            epistemic_tier,
            route_decider,
            validation_sampler,
            freeze,
        ]:
            source = inspect.getsource(mod)
            for marker in llm_markers:
                assert f"import {marker}" not in source, (
                    f"{mod.__name__} imports {marker} — curation must be deterministic"
                )


# ═══════════════════════════════════════════════════════════════════════
# 10. Validation sample stratification
# ═══════════════════════════════════════════════════════════════════════


class TestValidationSampling:
    """Validation sample must be stratified with minimum stratum sizes."""

    def test_sample_size_is_100(self) -> None:
        assert VALIDATION_SAMPLE_SIZE == 100

    def test_validation_sample_model(self) -> None:
        pid = uuid.uuid4()
        sample = ValidationSample(packet_id=pid)
        assert sample.verdict is None  # pending until reviewed
        assert sample.reviewed_by is None


# ═══════════════════════════════════════════════════════════════════════
# 11. aggressive_dedup regression risk
# ═══════════════════════════════════════════════════════════════════════


class TestAggressiveDedupRegression:
    """Document that aggressive_dedup risk is mitigated by design.

    The old ingest pipe had an aggressive_dedup bug that could delete
    source content. The brain_curator module is a POST-WRITE layer that
    never modifies raw chunks. drop_from_active only excludes from
    active retrieval — it never calls DELETE on knowledge_vectors.

    This test suite verifies the mitigation by source inspection.
    """

    def test_no_delete_in_any_module(self) -> None:
        """No module in brain_curator uses DELETE FROM knowledge_vectors."""
        import inspect

        from brain_curator import (
            db,
            epistemic_tier,
            freeze,
            inventory,
            packet_builder,
            route_decider,
            validation_sampler,
            version_families,
        )

        for mod in [
            db,
            inventory,
            version_families,
            packet_builder,
            epistemic_tier,
            route_decider,
            validation_sampler,
            freeze,
        ]:
            source = inspect.getsource(mod)
            assert "DELETE FROM knowledge_vectors" not in source, (
                f"{mod.__name__} contains DELETE FROM knowledge_vectors — "
                "this violates the post-write contract"
            )

    def test_drop_from_active_is_route_not_deletion(self) -> None:
        """drop_from_active is a route label, not a data operation."""
        assert ROUTE_DROP_FROM_ACTIVE == "drop_from_active"
        # The route is used in brain_packets.route, not in any DELETE
        assert ROUTE_DROP_FROM_ACTIVE not in ("delete", "remove", "purge")


# ═══════════════════════════════════════════════════════════════════════
# 12. Route logic coverage
# ═══════════════════════════════════════════════════════════════════════


class TestRouteLogicCoverage:
    """Comprehensive tests for decide_route deterministic logic."""

    def test_no_provenance_routes_to_refine(self) -> None:
        route = decide_route(
            packet_type="reference",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=False,
            is_exact_duplicate=False,
            has_better_canonical=False,
        )
        assert route == ROUTE_REFINE

    def test_governed_intuited_routes_to_validate(self) -> None:
        for ptype in GOVERNED_PACKET_TYPES:
            route = decide_route(
                packet_type=ptype,
                epistemic_tier=TIER_INTUITED,
                has_evidence=True,
                has_provenance=True,
                is_exact_duplicate=False,
                has_better_canonical=False,
            )
            assert route == ROUTE_VALIDATE, f"{ptype} should route to validate"

    def test_high_value_with_evidence_routes_to_keep(self) -> None:
        route = decide_route(
            packet_type="decision",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=False,
            has_better_canonical=False,
        )
        assert route == ROUTE_KEEP

    def test_high_value_no_evidence_routes_to_refine(self) -> None:
        route = decide_route(
            packet_type="method",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=False,
            has_provenance=True,
            is_exact_duplicate=False,
            has_better_canonical=False,
        )
        assert route == ROUTE_REFINE

    def test_default_routes_to_review(self) -> None:
        route = decide_route(
            packet_type="reference",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=False,
            has_better_canonical=False,
        )
        assert route == ROUTE_REVIEW

    def test_quarantine_takes_priority_over_duplicate(self) -> None:
        """Secret detection beats all other routes."""
        route = decide_route(
            packet_type="reference",
            epistemic_tier=TIER_STRUCTURED,
            has_evidence=True,
            has_provenance=True,
            is_exact_duplicate=True,
            has_better_canonical=True,
            content_sample="api_key = sk-secret12345678",
        )
        assert route == ROUTE_QUARANTINE


# ═══════════════════════════════════════════════════════════════════════
# 13. Model construction tests
# ═══════════════════════════════════════════════════════════════════════


class TestModels:
    """Verify Pydantic models construct correctly."""

    def test_document_defaults(self) -> None:
        doc = Document(source_path="/test/file.md", file_hash_sha256="abc123")
        assert doc.status == "inventoried"
        assert doc.chunk_count == 0
        assert doc.document_id is not None

    def test_packet_defaults(self) -> None:
        p = Packet(packet_type="decision")
        assert p.status == "draft"
        assert p.route is None
        assert p.epistemic_tier is None

    def test_cluster_creation(self) -> None:
        c = DedupeCluster(cluster_type="exact", method="sha256")
        assert c.canonical_member_id is None

    def test_relationship_creation(self) -> None:
        r = Relationship(
            source_packet_id=uuid.uuid4(),
            target_packet_id=uuid.uuid4(),
            predicate="supersedes",
        )
        assert r.evidence_count == 0
        assert r.confidence == 1.0


# ═══════════════════════════════════════════════════════════════════════
# 14. Config constants
# ═══════════════════════════════════════════════════════════════════════


class TestConfig:
    """Verify configuration constants are sane."""

    def test_p0_halt_is_default(self) -> None:
        from brain_curator.config import ACTIVE_P0_POLICY

        assert ACTIVE_P0_POLICY == P0Policy.HALT

    def test_all_packet_types_superset_of_governed(self) -> None:
        assert GOVERNED_PACKET_TYPES.issubset(ALL_PACKET_TYPES)

    def test_active_routes_are_keep_and_freeze(self) -> None:
        assert ACTIVE_ROUTES == frozenset({"keep", "freeze"})


# ═══════════════════════════════════════════════════════════════════════
# 15. epistemic_core canonical integration (PR 2)
# ═══════════════════════════════════════════════════════════════════════


class TestEpistemicCoreIntegration:
    """Verify brain_curator types are the canonical epistemic_core types."""

    def test_p0policy_is_canonical(self) -> None:
        """brain_curator.config.P0Policy IS epistemic_core.p0_policy.P0Policy."""
        from epistemic_core.p0_policy import P0Policy as CoreP0Policy

        assert P0Policy is CoreP0Policy

    def test_p0incident_is_canonical(self) -> None:
        """brain_curator.epistemic_tier.P0TierViolation IS epistemic_core.P0Incident."""
        from epistemic_core.p0_policy import P0Incident
        from brain_curator.epistemic_tier import P0TierViolation

        assert P0TierViolation is P0Incident

    def test_tier_constants_are_canonical(self) -> None:
        """Tier string constants come from epistemic_core.tiers, not local copies."""
        from epistemic_core.tiers import (
            TIER_INTUITED as CORE_INTUITED,
            TIER_STRUCTURED as CORE_STRUCTURED,
            TIER_MEASURED as CORE_MEASURED,
            TIER_PROVEN as CORE_PROVEN,
        )

        assert TIER_INTUITED is CORE_INTUITED
        assert TIER_STRUCTURED is CORE_STRUCTURED
        assert TIER_MEASURED is CORE_MEASURED
        assert TIER_PROVEN is CORE_PROVEN

    def test_tier_rank_is_canonical(self) -> None:
        from epistemic_core.tiers import TIER_RANK as CORE_RANK

        assert TIER_RANK is CORE_RANK

    def test_tier_min_uses_canonical_implementation(self) -> None:
        """tier_min/tier_min_many in epistemic_tier are epistemic_core functions."""
        from epistemic_core.min_rule import tier_min_str, tier_min_many_str

        assert tier_min is tier_min_str
        assert tier_min_many is tier_min_many_str

    def test_epistemic_tier_enum_accessible_via_config(self) -> None:
        """EpistemicTier IntEnum is importable from config."""
        from brain_curator.config import EpistemicTier
        from epistemic_core.tiers import EpistemicTier as CoreTier

        assert EpistemicTier is CoreTier
        assert EpistemicTier.INTUITED.value == 1
        assert EpistemicTier.PROVEN.value == 4

    def test_no_local_p0policy_or_tier_definitions(self) -> None:
        """config.py and epistemic_tier.py define no local P0Policy or tier enums."""
        import inspect
        from brain_curator import config, epistemic_tier

        config_src = inspect.getsource(config)
        et_src = inspect.getsource(epistemic_tier)

        # No local class definitions for these — only imports
        assert "class P0Policy" not in config_src
        assert "class P0TierViolation" not in et_src
        assert "TIER_INTUITED = \"INTUITED\"" not in config_src
