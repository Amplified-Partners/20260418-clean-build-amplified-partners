"""
Scoring Engine — reads rubric.json, computes scores, runs composite formula.

This is the pure arithmetic core. No AI, no images — just numbers in, numbers out.
External scorers (UIClip model, LLM rubric evaluator) feed raw scores INTO this
engine, which validates, normalises, weights, and composites them.

Usage:
    engine = ScoringEngine.from_rubric("path/to/rubric.json")
    result = engine.score(raw_scores={"calm_surface": 7, "clear_hierarchy": 8, ...})
    composite = engine.composite(rubric_result=result, uiclip_score=0.72)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional

from .models import (
    Rubric,
    RubricDimension,
    DimensionScore,
    RubricResult,
    CompositeScore,
    KaizenDecision,
    Rule,
    HardCheckResult,
    Severity,
)


# ─── Hard Check Engine ──────────────────────────────────────────────────────

@dataclass
class HardCheckEngine:
    """
    Evaluates hard rules from core.rules.json.
    
    In the full pipeline these run against actual CSS / DOM.
    Here we accept pre-computed check results (pass/fail per rule)
    so the arithmetic can be tested in isolation.
    """
    rules: list[Rule] = field(default_factory=list)

    @classmethod
    def from_json(cls, path: str) -> "HardCheckEngine":
        with open(path, "r") as f:
            data = json.load(f)
        rules = [Rule.from_dict(r) for r in data["rules"]]
        return cls(rules=rules)

    def evaluate(self, check_results: dict[str, bool]) -> list[HardCheckResult]:
        """
        Given a dict of {rule_id: passed_bool}, return structured results.
        Missing rules default to passed=True (not yet checked).
        """
        results = []
        for rule in self.rules:
            passed = check_results.get(rule.id, True)
            violations = [] if passed else [{"rule_id": rule.id, "message": f"Failed: {rule.name}"}]
            results.append(HardCheckResult(
                rule_id=rule.id,
                passed=passed,
                violations=violations,
            ))
        return results

    @staticmethod
    def all_errors_pass(results: list[HardCheckResult], rules: list[Rule]) -> bool:
        """
        Return True only if all ERROR-severity rules passed.
        Warnings and suggestions don't block.
        """
        error_rule_ids = {r.id for r in rules if r.severity == Severity.ERROR}
        for result in results:
            if result.rule_id in error_rule_ids and not result.passed:
                return False
        return True

    def count_by_severity(self, results: list[HardCheckResult]) -> dict[str, int]:
        """Count failures grouped by severity."""
        severity_map = {r.id: r.severity for r in self.rules}
        counts = {"error": 0, "warning": 0, "suggestion": 0}
        for result in results:
            if not result.passed:
                sev = severity_map.get(result.rule_id, Severity.SUGGESTION)
                counts[sev.value] += 1
        return counts


# ─── Rubric Scoring Engine ──────────────────────────────────────────────────

@dataclass
class ScoringEngine:
    """
    Pure arithmetic scoring engine.
    
    Takes raw dimension scores (1-10) and produces:
    - Normalised per-dimension scores (0.0-1.0)
    - Weighted per-dimension contributions
    - Overall rubric normalised score (0.0-1.0)
    - Composite score with UIClip blend
    """
    rubric: Rubric = field(default_factory=Rubric)

    @classmethod
    def from_rubric(cls, rubric_path: str) -> "ScoringEngine":
        rubric = Rubric.from_json(rubric_path)
        return cls(rubric=rubric)

    def validate_rubric(self) -> list[str]:
        """
        Run arithmetic validation checks on the rubric itself.
        Returns a list of error messages (empty = valid).
        """
        errors = []

        # 1. Weights must sum to 1.0
        total = self.rubric.total_weight()
        if abs(total - 1.0) >= 0.001:
            errors.append(f"Weights sum to {total:.6f}, expected 1.0 (tolerance 0.001)")

        # 2. No negative weights
        for dim in self.rubric.dimensions:
            if dim.weight < 0:
                errors.append(f"Dimension '{dim.id}' has negative weight: {dim.weight}")
            if dim.weight == 0:
                errors.append(f"Dimension '{dim.id}' has zero weight (dead dimension)")

        # 3. Scale min < max for all dimensions
        for dim in self.rubric.dimensions:
            if dim.scale_min >= dim.scale_max:
                errors.append(f"Dimension '{dim.id}' has invalid scale: min={dim.scale_min} >= max={dim.scale_max}")

        # 4. No duplicate dimension IDs
        ids = [d.id for d in self.rubric.dimensions]
        if len(ids) != len(set(ids)):
            dupes = [x for x in ids if ids.count(x) > 1]
            errors.append(f"Duplicate dimension IDs: {set(dupes)}")

        return errors

    def score(
        self,
        raw_scores: dict[str, float],
        scorer: str = "test",
        rationales: Optional[dict[str, str]] = None,
    ) -> RubricResult:
        """
        Compute a full rubric result from raw dimension scores.
        
        Args:
            raw_scores: {dimension_id: raw_score (1-10)}
            scorer: Name of the scorer (e.g. "llm:claude-sonnet", "human:ewan")
            rationales: Optional {dimension_id: text_rationale}
        
        Returns:
            RubricResult with all normalised/weighted scores + overall.
        
        Raises:
            ValueError: If a score is out of range or dimension is unknown.
        """
        rationales = rationales or {}
        dimension_scores: list[DimensionScore] = []

        for dim in self.rubric.dimensions:
            if dim.id not in raw_scores:
                raise ValueError(f"Missing score for dimension '{dim.id}'")
            
            raw = raw_scores[dim.id]
            if not dim.validate_score(raw):
                raise ValueError(
                    f"Score {raw} for '{dim.id}' is out of range "
                    f"[{dim.scale_min}, {dim.scale_max}]"
                )

            normalised = dim.normalise_score(raw)
            weighted = dim.weighted_normalised(raw)

            dimension_scores.append(DimensionScore(
                dimension_id=dim.id,
                raw_score=raw,
                normalised=normalised,
                weighted=weighted,
                rationale=rationales.get(dim.id, ""),
            ))

        # Overall normalised = sum of weighted normalised scores
        overall_normalised = sum(ds.weighted for ds in dimension_scores)

        # Overall raw = weighted mean on the original 1-10 scale
        # = Σ(raw_score × weight) for all dimensions
        overall_raw = sum(
            raw_scores[dim.id] * dim.weight
            for dim in self.rubric.dimensions
        )

        import time
        result = RubricResult(
            scores=dimension_scores,
            overall_raw=overall_raw,
            normalised=overall_normalised,
            scorer=scorer,
            scored_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        return result

    def composite(
        self,
        rubric_result: RubricResult,
        uiclip_score: float,
        uiclip_weight: float = 0.4,
        rubric_weight: float = 0.6,
        variant_id: str = "",
    ) -> CompositeScore:
        """
        Blend rubric + UIClip into a single composite score.
        
        composite = (uiclip × 0.4) + (rubric_normalised × 0.6)
        
        Both inputs must be in [0.0, 1.0].
        """
        if not (0.0 <= uiclip_score <= 1.0):
            raise ValueError(f"UIClip score must be 0.0-1.0, got {uiclip_score}")
        if not (0.0 <= rubric_result.normalised <= 1.0):
            raise ValueError(f"Rubric normalised must be 0.0-1.0, got {rubric_result.normalised}")
        if abs((uiclip_weight + rubric_weight) - 1.0) >= 0.001:
            raise ValueError(
                f"Composite weights must sum to 1.0, got {uiclip_weight + rubric_weight}"
            )

        import time
        comp = CompositeScore(
            variant_id=variant_id,
            uiclip_score=uiclip_score,
            rubric_normalised=rubric_result.normalised,
            uiclip_weight=uiclip_weight,
            rubric_weight=rubric_weight,
            computed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        comp.compute()
        return comp

    def kaizen_compare(
        self,
        baseline: CompositeScore,
        candidate: CompositeScore,
        hard_checks_pass: bool = True,
    ) -> KaizenDecision:
        """
        Compare candidate against baseline for Kaizen acceptance.
        
        From the spec:
            accepted = (
                all_hard_checks_pass
                AND composite_delta > +0.005
                AND no_dimension_regression > 0.01
                AND human_approval == True
            )
        """
        composite_delta = candidate.composite - baseline.composite

        # Find max per-dimension regression
        max_regression = 0.0
        for dim_id, candidate_val in candidate.dimension_deltas.items():
            baseline_val = baseline.dimension_deltas.get(dim_id, 0.0)
            regression = baseline_val - candidate_val  # positive = regression
            max_regression = max(max_regression, regression)

        return KaizenDecision(
            all_hard_checks_pass=hard_checks_pass,
            composite_delta=composite_delta,
            max_dimension_regression=max_regression,
            human_approval=None,  # Always starts as pending
        )


# ─── Convenience: Full Pipeline Run ─────────────────────────────────────────

@dataclass
class PipelineResult:
    """Complete result of running the full scoring pipeline."""
    hard_check_results: list[HardCheckResult]
    hard_checks_pass: bool
    hard_check_counts: dict[str, int]
    rubric_result: RubricResult
    composite: CompositeScore
    kaizen: Optional[KaizenDecision] = None

    @property
    def passed(self) -> bool:
        """Overall pass/fail (hard checks pass AND composite >= threshold)."""
        return self.hard_checks_pass

    def summary(self, threshold: float = 0.60) -> str:
        """Human-readable summary of the pipeline result."""
        lines = []
        lines.append("=" * 60)
        lines.append("  VISUAL POLISH SCORING REPORT")
        lines.append("=" * 60)

        # Hard checks
        lines.append(f"\n  HARD CHECKS: {'PASS' if self.hard_checks_pass else 'FAIL'}")
        for sev, count in self.hard_check_counts.items():
            if count > 0:
                lines.append(f"    {sev.upper()}: {count} failure(s)")

        # Rubric dimensions
        lines.append(f"\n  RUBRIC SCORES (weighted)")
        lines.append(f"  {'Dimension':<25} {'Raw':>5} {'Norm':>7} {'Weighted':>9}")
        lines.append(f"  {'-'*25} {'─'*5} {'─'*7} {'─'*9}")
        for ds in self.rubric_result.scores:
            lines.append(
                f"  {ds.dimension_id:<25} {ds.raw_score:>5.1f} {ds.normalised:>7.4f} {ds.weighted:>9.6f}"
            )
        lines.append(f"  {'─'*50}")
        lines.append(f"  {'OVERALL (raw weighted)':<25} {self.rubric_result.overall_raw:>5.2f}")
        lines.append(f"  {'OVERALL (normalised)':<25} {self.rubric_result.normalised:>12.6f}")

        # Composite
        lines.append(f"\n  COMPOSITE SCORE")
        lines.append(f"    UIClip score:       {self.composite.uiclip_score:.4f} × {self.composite.uiclip_weight}")
        lines.append(f"    Rubric normalised:  {self.composite.rubric_normalised:.4f} × {self.composite.rubric_weight}")
        lines.append(f"    ────────────────────────────")
        lines.append(f"    COMPOSITE:          {self.composite.composite:.4f}")
        lines.append(f"    Threshold:          {threshold:.4f}")
        status = "PASS" if self.composite.composite >= threshold else "FAIL"
        lines.append(f"    Result:             {status}")

        # Kaizen
        if self.kaizen:
            lines.append(f"\n  KAIZEN DECISION")
            lines.append(f"    {self.kaizen.machine_recommendation}")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


def run_pipeline(
    rubric_path: str,
    rules_path: str,
    raw_scores: dict[str, float],
    hard_check_results: dict[str, bool],
    uiclip_score: float,
    uiclip_weight: float = 0.4,
    rubric_weight: float = 0.6,
    baseline: Optional[CompositeScore] = None,
    scorer: str = "test",
) -> PipelineResult:
    """
    Run the full scoring pipeline end-to-end.
    
    This is the function the CLI and tests call.
    """
    # 1. Load engines
    scoring = ScoringEngine.from_rubric(rubric_path)
    hard_check_engine = HardCheckEngine.from_json(rules_path)

    # 2. Validate rubric integrity
    rubric_errors = scoring.validate_rubric()
    if rubric_errors:
        raise ValueError(f"Rubric validation failed: {rubric_errors}")

    # 3. Run hard checks
    hc_results = hard_check_engine.evaluate(hard_check_results)
    hc_pass = hard_check_engine.all_errors_pass(hc_results, hard_check_engine.rules)
    hc_counts = hard_check_engine.count_by_severity(hc_results)

    # 4. Run rubric scoring
    rubric_result = scoring.score(raw_scores, scorer=scorer)

    # 5. Compute composite
    composite = scoring.composite(
        rubric_result=rubric_result,
        uiclip_score=uiclip_score,
        uiclip_weight=uiclip_weight,
        rubric_weight=rubric_weight,
    )
    # Store per-dimension normalised values for Kaizen comparison
    composite.dimension_deltas = {
        ds.dimension_id: ds.normalised for ds in rubric_result.scores
    }

    # 6. Kaizen comparison (if baseline provided)
    kaizen = None
    if baseline is not None:
        kaizen = scoring.kaizen_compare(baseline, composite, hard_checks_pass=hc_pass)

    return PipelineResult(
        hard_check_results=hc_results,
        hard_checks_pass=hc_pass,
        hard_check_counts=hc_counts,
        rubric_result=rubric_result,
        composite=composite,
        kaizen=kaizen,
    )

