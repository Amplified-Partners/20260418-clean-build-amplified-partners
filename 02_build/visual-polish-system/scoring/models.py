"""
Data models for the Visual Polish Scoring Pipeline.
All types used across scoring, evaluation, and Kaizen decision-making.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import json
import time
import uuid


# ─── Enums ───────────────────────────────────────────────────────────────────

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    SUGGESTION = "suggestion"


class ExperimentTrigger(Enum):
    NIGHTLY = "nightly"
    PR = "pr"
    MANUAL = "manual"
    FEATURE = "feature"
    BASELINE = "baseline"


class Decision(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PENDING = "pending_review"


# ─── Rubric Dimension ───────────────────────────────────────────────────────

@dataclass
class RubricDimension:
    """A single scoring dimension from the rubric."""
    id: str
    name: str
    weight: float
    prompt: str
    scale_min: int = 1
    scale_max: int = 10
    anchor_low: str = ""
    anchor_high: str = ""

    def validate_score(self, score: float) -> bool:
        """Check a score is within the valid range."""
        return self.scale_min <= score <= self.scale_max

    def normalise_score(self, score: float) -> float:
        """Normalise a raw score (1-10) to 0.0-1.0 range."""
        return (score - self.scale_min) / (self.scale_max - self.scale_min)

    def weighted_normalised(self, score: float) -> float:
        """Return the weighted contribution of this dimension to the composite."""
        return self.normalise_score(score) * self.weight


# ─── Rubric (collection of dimensions) ──────────────────────────────────────

@dataclass
class Rubric:
    """The complete scoring rubric — loaded from rubric.json."""
    dimensions: list[RubricDimension] = field(default_factory=list)

    @classmethod
    def from_json(cls, path: str) -> "Rubric":
        """Load rubric from the JSON file."""
        with open(path, "r") as f:
            data = json.load(f)

        dims = []
        for d in data["rubric"]["dimensions"]:
            dims.append(RubricDimension(
                id=d["id"],
                name=d["name"],
                weight=d["weight"],
                prompt=d["prompt"],
                scale_min=d["scale"]["min"],
                scale_max=d["scale"]["max"],
                anchor_low=d["scale"].get("anchor_low", ""),
                anchor_high=d["scale"].get("anchor_high", ""),
            ))
        return cls(dimensions=dims)

    def total_weight(self) -> float:
        """Sum of all dimension weights. Must equal 1.0."""
        return sum(d.weight for d in self.dimensions)

    def validate_weights(self, tolerance: float = 0.001) -> bool:
        """Check weights sum to 1.0 within tolerance."""
        return abs(self.total_weight() - 1.0) < tolerance

    def dimension_ids(self) -> list[str]:
        return [d.id for d in self.dimensions]

    def get_dimension(self, dim_id: str) -> Optional[RubricDimension]:
        for d in self.dimensions:
            if d.id == dim_id:
                return d
        return None


# ─── Score Results ───────────────────────────────────────────────────────────

@dataclass
class DimensionScore:
    """Score for a single rubric dimension."""
    dimension_id: str
    raw_score: float       # 1-10
    normalised: float      # 0.0-1.0
    weighted: float        # normalised × weight
    rationale: str = ""


@dataclass
class RubricResult:
    """Complete rubric evaluation result."""
    scores: list[DimensionScore]
    overall_raw: float     # Weighted mean on 1-10 scale
    normalised: float      # 0.0-1.0
    top_suggestion: str = ""
    secondary_suggestions: list[str] = field(default_factory=list)
    scorer: str = ""
    scored_at: str = ""

    @property
    def dimension_dict(self) -> dict[str, float]:
        return {s.dimension_id: s.raw_score for s in self.scores}


@dataclass
class CompositeScore:
    """The final composite polish score combining all methods."""
    id: str = ""
    variant_id: str = ""

    uiclip_score: float = 0.0          # 0.0-1.0
    rubric_normalised: float = 0.0     # 0.0-1.0
    composite: float = 0.0             # 0.0-1.0

    uiclip_weight: float = 0.4
    rubric_weight: float = 0.6

    visual_regression_diff_pct: float = 0.0
    dimension_deltas: dict[str, float] = field(default_factory=dict)

    computed_at: str = ""

    def compute(self) -> float:
        """Calculate composite score from components."""
        self.composite = (
            self.uiclip_score * self.uiclip_weight
            + self.rubric_normalised * self.rubric_weight
        )
        return self.composite

    def validate_formula(self) -> bool:
        """Verify the composite was calculated correctly."""
        expected = (
            self.uiclip_score * self.uiclip_weight
            + self.rubric_normalised * self.rubric_weight
        )
        return abs(self.composite - expected) < 0.0001


# ─── Kaizen Decision ────────────────────────────────────────────────────────

@dataclass
class KaizenDecision:
    """
    Acceptance/rejection logic for a Kaizen experiment.

    From the spec:
        accepted = (
            all_hard_checks_pass
            AND composite_score_delta > +0.005
            AND no_dimension_regression > 0.01
            AND human_approval == True
        )
    """
    all_hard_checks_pass: bool = False
    composite_delta: float = 0.0
    max_dimension_regression: float = 0.0
    human_approval: Optional[bool] = None

    min_composite_improvement: float = 0.005
    max_allowed_regression: float = 0.01

    @property
    def machine_recommendation(self) -> str:
        """What the system recommends, before human input."""
        if not self.all_hard_checks_pass:
            return "REJECT: Hard check failures"
        if self.composite_delta < self.min_composite_improvement:
            return f"REJECT: Composite delta {self.composite_delta:.4f} < {self.min_composite_improvement}"
        if self.max_dimension_regression > self.max_allowed_regression:
            return f"REJECT: Dimension regression {self.max_dimension_regression:.4f} > {self.max_allowed_regression}"
        return "RECOMMEND ACCEPT: All criteria met, pending human approval"

    @property
    def auto_criteria_met(self) -> bool:
        return (
            self.all_hard_checks_pass
            and self.composite_delta >= self.min_composite_improvement
            and self.max_dimension_regression <= self.max_allowed_regression
        )

    @property
    def final_decision(self) -> Decision:
        if not self.auto_criteria_met:
            return Decision.REJECTED
        if self.human_approval is None:
            return Decision.PENDING
        if self.human_approval:
            return Decision.ACCEPTED
        return Decision.REJECTED


# ─── Hard Check Rule ────────────────────────────────────────────────────────

@dataclass
class Rule:
    """A single rule from core.rules.json."""
    id: str
    name: str
    category: str
    severity: Severity
    condition: dict
    rationale: str
    source: str = ""
    added: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Rule":
        return cls(
            id=d["id"],
            name=d["name"],
            category=d["category"],
            severity=Severity(d["severity"]),
            condition=d.get("condition", {}),
            rationale=d["rationale"],
            source=d.get("source", ""),
            added=d.get("added", ""),
        )


@dataclass
class HardCheckResult:
    """Result of running a single hard check rule."""
    rule_id: str
    passed: bool
    violations: list[dict] = field(default_factory=list)

    @property
    def violation_count(self) -> int:
        return len(self.violations)

