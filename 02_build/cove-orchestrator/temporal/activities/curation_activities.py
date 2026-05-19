"""Temporal activities for the brain_curator post-write curation pipeline.

Stages 3.5-9: inventory, version families, packet building, epistemic
tiering, route decision, validation sampling, freeze governance.

All stages are separate activities with their own retry policies.
None of them modify knowledge_vectors.content.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from temporalio import activity

logger = logging.getLogger("cove.curation")


# ═══════════════════════════════════════════════════════════════════════
# Data classes
# ═══════════════════════════════════════════════════════════════════════


@dataclass
class CurationInput:
    """Input for the full curation pipeline."""

    run_id_prefix: str = "curation"
    provenance_filter: str = "amplified-pipeline-v0.3"


@dataclass
class CurationStageResult:
    """Result from a single curation stage."""

    success: bool
    stage: str
    metrics: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class CurationPipelineResult:
    """Result from the full curation pipeline."""

    success: bool
    stages: dict[str, CurationStageResult] = field(default_factory=dict)
    error: str | None = None


# ═══════════════════════════════════════════════════════════════════════
# Activities
# ═══════════════════════════════════════════════════════════════════════


@activity.defn(name="backfill_documents")
async def backfill_documents(input: CurationInput) -> CurationStageResult:
    """Run inventory backfill from knowledge_vectors to brain_documents."""
    from brain_curator.inventory import backfill_documents as _backfill

    run_id = f"{input.run_id_prefix}-inventory"
    try:
        metrics = await _backfill(
            run_id=run_id,
            provenance_filter=input.provenance_filter,
        )
        return CurationStageResult(success=True, stage="inventory", metrics=metrics)
    except Exception as e:
        logger.exception("Inventory backfill failed")
        return CurationStageResult(
            success=False, stage="inventory", error=str(e)
        )


@activity.defn(name="detect_version_families")
async def detect_version_families(input: CurationInput) -> CurationStageResult:
    """Run version family detection on brain_documents."""
    from brain_curator.version_families import detect_version_families as _detect

    run_id = f"{input.run_id_prefix}-version-families"
    try:
        metrics = await _detect(run_id=run_id)
        return CurationStageResult(
            success=True, stage="version_families", metrics=metrics
        )
    except Exception as e:
        logger.exception("Version family detection failed")
        return CurationStageResult(
            success=False, stage="version_families", error=str(e)
        )


@activity.defn(name="build_packets")
async def build_packets(input: CurationInput) -> CurationStageResult:
    """Run packet builder on inventoried documents."""
    from brain_curator.packet_builder import build_packets as _build

    run_id = f"{input.run_id_prefix}-packets"
    try:
        metrics = await _build(run_id=run_id)
        return CurationStageResult(
            success=True, stage="packet_builder", metrics=metrics
        )
    except Exception as e:
        logger.exception("Packet builder failed")
        return CurationStageResult(
            success=False, stage="packet_builder", error=str(e)
        )


@activity.defn(name="assign_epistemic_tiers")
async def assign_epistemic_tiers(input: CurationInput) -> CurationStageResult:
    """Run epistemic tier assignment on draft packets."""
    from brain_curator.epistemic_tier import assign_epistemic_tiers as _assign

    run_id = f"{input.run_id_prefix}-tiers"
    try:
        metrics = await _assign(run_id=run_id)
        return CurationStageResult(
            success=True, stage="epistemic_tier", metrics=metrics
        )
    except Exception as e:
        logger.exception("Epistemic tier assignment failed")
        return CurationStageResult(
            success=False, stage="epistemic_tier", error=str(e)
        )


@activity.defn(name="decide_routes")
async def decide_routes(input: CurationInput) -> CurationStageResult:
    """Run route decision on tiered draft packets."""
    from brain_curator.route_decider import decide_routes as _decide

    run_id = f"{input.run_id_prefix}-routes"
    try:
        metrics = await _decide(run_id=run_id)
        return CurationStageResult(
            success=True, stage="route_decider", metrics=metrics
        )
    except Exception as e:
        logger.exception("Route decision failed")
        return CurationStageResult(
            success=False, stage="route_decider", error=str(e)
        )


@activity.defn(name="sample_validation")
async def sample_validation(input: CurationInput) -> CurationStageResult:
    """Run stratified validation sampling on routed packets."""
    from brain_curator.validation_sampler import sample_validation as _sample

    run_id = f"{input.run_id_prefix}-validation"
    try:
        metrics = await _sample(run_id=run_id)
        return CurationStageResult(
            success=True, stage="validation_sampler", metrics=metrics
        )
    except Exception as e:
        logger.exception("Validation sampling failed")
        return CurationStageResult(
            success=False, stage="validation_sampler", error=str(e)
        )


@activity.defn(name="freeze_curation_packets")
async def freeze_curation_packets(input: CurationInput) -> CurationStageResult:
    """Run freeze governance on active/draft packets."""
    from brain_curator.freeze import freeze_packets as _freeze

    run_id = f"{input.run_id_prefix}-freeze"
    try:
        metrics = await _freeze(run_id=run_id)
        return CurationStageResult(
            success=True, stage="freeze", metrics=metrics
        )
    except Exception as e:
        logger.exception("Freeze governance failed")
        return CurationStageResult(
            success=False, stage="freeze", error=str(e)
        )


@activity.defn(name="run_curation_pipeline")
async def run_curation_pipeline(input: CurationInput) -> CurationPipelineResult:
    """Orchestrate the full curation pipeline (stages 3.5-9).

    Runs all stages sequentially. If any stage fails, records the error
    and continues to the next stage (best-effort curation).
    """
    from brain_curator.epistemic_tier import assign_epistemic_tiers as _assign_tiers
    from brain_curator.freeze import freeze_packets as _freeze
    from brain_curator.inventory import backfill_documents as _backfill
    from brain_curator.packet_builder import build_packets as _build
    from brain_curator.route_decider import decide_routes as _decide
    from brain_curator.validation_sampler import sample_validation as _sample
    from brain_curator.version_families import detect_version_families as _detect

    stages: dict[str, CurationStageResult] = {}
    prefix = input.run_id_prefix

    stage_runners = [
        ("inventory", lambda: _backfill(f"{prefix}-inventory", input.provenance_filter)),
        ("version_families", lambda: _detect(f"{prefix}-version-families")),
        ("packet_builder", lambda: _build(f"{prefix}-packets")),
        ("epistemic_tier", lambda: _assign_tiers(f"{prefix}-tiers")),
        ("route_decider", lambda: _decide(f"{prefix}-routes")),
        ("validation_sampler", lambda: _sample(f"{prefix}-validation")),
        ("freeze", lambda: _freeze(f"{prefix}-freeze")),
    ]

    all_success = True
    for stage_name, runner in stage_runners:
        try:
            metrics = await runner()
            stages[stage_name] = CurationStageResult(
                success=True, stage=stage_name, metrics=metrics
            )
        except Exception as e:
            logger.exception("Curation stage %s failed", stage_name)
            stages[stage_name] = CurationStageResult(
                success=False, stage=stage_name, error=str(e)
            )
            all_success = False

    return CurationPipelineResult(success=all_success, stages=stages)
