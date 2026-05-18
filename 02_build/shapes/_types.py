"""
Core types for the Huf Haus shape system.

Every Python file in the Amplified system is exactly one of fifteen shapes.
These types define the contracts, enums, and data structures shared across all shapes.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
Source architect: Ewan Bramley (shape taxonomy, 2026-05-17)
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import enum
import uuid
from typing import Any


# ---------------------------------------------------------------------------
# 1. Shape kinds — the fifteen shapes
# ---------------------------------------------------------------------------


class ShapeKind(enum.Enum):
    """The fifteen code shapes. Every file is exactly one."""

    ENTRY = "entry"
    SERVICE = "service"
    WORKER = "worker"
    CONNECTOR = "connector"
    MODEL = "model"
    STORE = "store"
    PIPELINE = "pipeline"
    ORCHESTRATOR = "orchestrator"
    GUARD = "guard"
    SCORER = "scorer"
    AGENT = "agent"
    TEST = "test"
    CONFIG = "config"
    TELEMETRY = "telemetry"
    GLUE = "glue"


# ---------------------------------------------------------------------------
# 2. Shape colours — visual classification
# ---------------------------------------------------------------------------


class ShapeColour(enum.Enum):
    """Each shape has a natural colour for instant visual classification."""

    BLUE = "blue"       # model, config — data definitions
    GREEN = "green"     # entry, connector — external boundary
    RED = "red"         # service, scorer, guard — business logic
    YELLOW = "yellow"   # store, worker, pipeline — infrastructure
    PURPLE = "purple"   # agent, orchestrator — AI and coordination
    GREY = "grey"       # test, telemetry, glue — support


SHAPE_COLOUR_MAP: dict[ShapeKind, ShapeColour] = {
    ShapeKind.MODEL: ShapeColour.BLUE,
    ShapeKind.CONFIG: ShapeColour.BLUE,
    ShapeKind.ENTRY: ShapeColour.GREEN,
    ShapeKind.CONNECTOR: ShapeColour.GREEN,
    ShapeKind.SERVICE: ShapeColour.RED,
    ShapeKind.SCORER: ShapeColour.RED,
    ShapeKind.GUARD: ShapeColour.RED,
    ShapeKind.STORE: ShapeColour.YELLOW,
    ShapeKind.WORKER: ShapeColour.YELLOW,
    ShapeKind.PIPELINE: ShapeColour.YELLOW,
    ShapeKind.AGENT: ShapeColour.PURPLE,
    ShapeKind.ORCHESTRATOR: ShapeColour.PURPLE,
    ShapeKind.TEST: ShapeColour.GREY,
    ShapeKind.TELEMETRY: ShapeColour.GREY,
    ShapeKind.GLUE: ShapeColour.GREY,
}


# ---------------------------------------------------------------------------
# 3. Handoff protocol — how shapes pass data between each other
# ---------------------------------------------------------------------------


class HandoffProtocol(enum.Enum):
    """How a shape receives data and how it hands off to the next shape."""

    SYNC_CALL = "sync_call"           # function call, immediate return
    ASYNC_MESSAGE = "async_message"   # message on a queue, eventual processing
    EVENT_EMIT = "event_emit"         # fire-and-forget event


# ---------------------------------------------------------------------------
# 4. Traffic light — GREEN / AMBER / RED / BLACK
# ---------------------------------------------------------------------------


class TrafficLight(enum.Enum):
    """Signal severity classification."""

    GREEN = "GREEN"   # within bounds
    AMBER = "AMBER"   # pattern forming — Kaizen target, not shame
    RED = "RED"       # critical breach — freeze boundary
    BLACK = "BLACK"   # epistemic P0 — hard halt


# ---------------------------------------------------------------------------
# 5. Escalation flags — three flags on every shape
# ---------------------------------------------------------------------------


class EscalationFlag(enum.Enum):
    """The three flags baked into every shape's proforma."""

    NEEDS_RESEARCH = "needs_research"   # unsolved territory
    NEEDS_TOOL = "needs_tool"           # missing external connector
    NEEDS_GENIUS = "needs_genius"       # expert declared this is a bastard


# ---------------------------------------------------------------------------
# 5b. Portable Spine — the nine principles, baked into the code
# ---------------------------------------------------------------------------


class SpinePrinciple(enum.Enum):
    """The nine immutable principles from the Portable Spine.

    Source: 00_authority/PORTABLE-SPINE.md
    These override everything. Not Ewan. Not any agent. Not any client.
    The Ulysses Clause: if Ewan overrides these, the system flags it.
    """

    RADICAL_HONESTY = "radical_honesty"
    RADICAL_TRANSPARENCY = "radical_transparency"
    RADICAL_ATTRIBUTION = "radical_attribution"
    WIN_WIN = "win_win"
    DETERMINISTIC_FIRST = "deterministic_first"
    CONGRUENCE = "congruence"
    NARROW_HANDOFF = "narrow_handoff"
    SHADOW_FIRST = "shadow_first"
    PRIVACY_FIRST = "privacy_first"

    def label(self) -> str:
        return self.value.replace("_", " ").title()


# ---------------------------------------------------------------------------
# 6. Core data structures
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class TrackingContext:
    """Every piece of data in the system carries a tracking context."""

    tracking_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    received_at: dt.datetime = dataclasses.field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)
    )
    source_shape: str = ""
    source_id: str = ""


@dataclasses.dataclass(frozen=True)
class ValidatedInput:
    """Output of an entry shape — typed, tracked, timestamped."""

    data: Any
    tracking_id: str
    received_at: dt.datetime
    input_hash: str = ""


@dataclasses.dataclass(frozen=True)
class WorkerResult:
    """Output of a worker shape — completion report."""

    status: str  # "complete" | "failed" | "partial"
    processed: int = 0
    tracking_id: str = ""
    error: str | None = None


@dataclasses.dataclass(frozen=True)
class WorkflowResult:
    """Output of an orchestrator shape — workflow completion report."""

    status: str  # "complete" | "failed" | "partial"
    steps_completed: int = 0
    steps_total: int = 0
    record_id: str = ""
    step_log: tuple[str, ...] = ()
    error: str | None = None


@dataclasses.dataclass(frozen=True)
class SignalClassification:
    """A classified monitoring signal."""

    shape: str  # network shape: load, drift, spike, cascade, etc.
    severity: str  # GREEN / AMBER / RED / BLACK
    detail: str = ""
    timestamp: dt.datetime = dataclasses.field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)
    )


@dataclasses.dataclass(frozen=True)
class Rule:
    """A guard rule definition."""

    name: str
    severity: str  # GREEN / AMBER / RED / BLACK
    pattern: str | None = None
    check: Any = None  # callable
    description: str = ""


@dataclasses.dataclass(frozen=True)
class Rejection:
    """A guard rejection — data did not pass."""

    reason: str
    violations: tuple[str, ...] = ()
    severity: str = "RED"


# ---------------------------------------------------------------------------
# 7. Shape errors — typed, structured, never raw exceptions
# ---------------------------------------------------------------------------


class ShapeError(Exception):
    """Base exception for all shape errors."""

    def __init__(self, message: str, shape_kind: str = "", tracking_id: str = "") -> None:
        super().__init__(message)
        self.shape_kind = shape_kind
        self.tracking_id = tracking_id


class EntryError(ShapeError):
    """Entry shape error — bad input from external source."""

    def __init__(self, message: str, status_code: int = 400, **kwargs: Any) -> None:
        super().__init__(message, shape_kind="entry", **kwargs)
        self.status_code = status_code


class ConnectorError(ShapeError):
    """Connector shape error — external system failure."""

    def __init__(
        self,
        message: str,
        external_status: int | None = None,
        retry_eligible: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, shape_kind="connector", **kwargs)
        self.external_status = external_status
        self.retry_eligible = retry_eligible


class StoreError(ShapeError):
    """Store shape error — persistence failure."""

    def __init__(self, message: str, operation: str = "", retriable: bool = False, **kwargs: Any) -> None:
        super().__init__(message, shape_kind="store", **kwargs)
        self.operation = operation
        self.retriable = retriable


class GuardHalt(ShapeError):
    """Guard BLACK condition — full propagation halt."""

    def __init__(self, message: str, violations: tuple[str, ...] = (), **kwargs: Any) -> None:
        super().__init__(message, shape_kind="guard", **kwargs)
        self.violations = violations


class PipelineError(ShapeError):
    """Pipeline shape error — transformation failure."""

    def __init__(
        self,
        message: str,
        step_failed: str = "",
        steps_completed: tuple[str, ...] = (),
        **kwargs: Any,
    ) -> None:
        super().__init__(message, shape_kind="pipeline", **kwargs)
        self.step_failed = step_failed
        self.steps_completed = steps_completed


class WorkflowError(ShapeError):
    """Orchestrator shape error — workflow failure."""

    def __init__(
        self,
        message: str,
        steps_completed: tuple[str, ...] = (),
        step_failed: str = "",
        compensation_performed: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, shape_kind="orchestrator", **kwargs)
        self.steps_completed = steps_completed
        self.step_failed = step_failed
        self.compensation_performed = compensation_performed


class ConfigError(ShapeError):
    """Config shape error — invalid configuration."""

    def __init__(self, message: str, setting_name: str = "", expected: str = "", **kwargs: Any) -> None:
        super().__init__(message, shape_kind="config", **kwargs)
        self.setting_name = setting_name
        self.expected = expected


class AgentError(ShapeError):
    """Agent shape error — AI reasoning failure."""

    def __init__(
        self,
        message: str,
        confidence_at_failure: float = 0.0,
        fallback_used: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, shape_kind="agent", **kwargs)
        self.confidence_at_failure = confidence_at_failure
        self.fallback_used = fallback_used


class TelemetryError(ShapeError):
    """Telemetry shape error — metric emission failure. Never blocks source shape."""

    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, shape_kind="telemetry", **kwargs)


class SpineViolation(ShapeError):
    """Spine principle structurally violated — the system caught itself drifting.

    Raised when:
    - A shape has no spine principles declared (unmoored shape)
    - A spine principle has no shape enforcing it (dead principle)
    - Spine coverage verification fails
    """

    def __init__(
        self,
        message: str,
        *,
        principle: str = "",
        shape_name: str = "",
        violation_type: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, shape_kind="spine", **kwargs)
        self.principle = principle
        self.shape_name = shape_name
        self.violation_type = violation_type


class EpistemicViolation(ShapeError):
    """P0-class error — epistemic invariant violated. System halts.

    Raised when:
    - A bare value crosses a protected boundary (laundering trap)
    - A shape over-claims its status (declares higher than declared_max)
    - Illegal promotion or tier-skipping detected
    - Gap >= 2 between declared and effective status
    """

    def __init__(
        self,
        message: str,
        *,
        declared_tier: str = "",
        effective_tier: str = "",
        violation_type: str = "",
        shape_name: str = "",
        boundary_method: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, shape_kind="epistemic", **kwargs)
        self.declared_tier = declared_tier
        self.effective_tier = effective_tier
        self.violation_type = violation_type
        self.shape_name = shape_name
        self.boundary_method = boundary_method
