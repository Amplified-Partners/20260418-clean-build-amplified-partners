"""
Amplified Shapes — the Huf Haus code shape system.

Fifteen code shapes. Every Python file is exactly one shape.
Each shape is a function, not a domain. Each shape gets a pre-made template
with pipes and electrics already in. The lads on site just put the glue together.

Usage:
    from shapes import EntryBase, ServiceBase, monitored, tracked, REGISTRY

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
Source architect: Ewan Bramley (shape taxonomy, Huf Haus doctrine, 2026-05-17)
"""

# --- Types ---
from ._types import (
    AgentError,
    ConfigError,
    ConnectorError,
    EntryError,
    EpistemicViolation,
    EscalationFlag,
    SpinePrinciple,
    SpineViolation,
    GuardHalt,
    HandoffProtocol,
    PipelineError,
    Rejection,
    Rule,
    ShapeColour,
    ShapeError,
    ShapeKind,
    SignalClassification,
    StoreError,
    TelemetryError,
    TrackingContext,
    TrafficLight,
    ValidatedInput,
    WorkerResult,
    WorkflowError,
    WorkflowResult,
    SHAPE_COLOUR_MAP,
)

# --- Decorators ---
from ._decorators import (
    circuit_breaker,
    confidence_floor,
    debt_tracked,
    epistemic,
    field,
    hash_protected,
    metric,
    monitored,
    no_bypass,
    reader_first,
    retryable,
    secret,
    setting,
    signal_classifier,
    spine,
    step,
    tracked,
    transactional,
    validated,
    workflow,
    METRICS,
)

# --- Epistemic bridge ---
from ._epistemic import (
    EpistemicTier,
    PreconditionCheck,
    ShapeProvenance,
    StatusedOutput,
    ShapeAuditRecord,
    ShapeAuditLog,
    SHAPE_AUDIT_LOG,
)

# --- Registry ---
from ._registry import REGISTRY, ShapeRegistry

# --- Base ---
from ._base import ShapeBase

# --- Shape base classes ---
from .entry import EntryBase
from .service import ServiceBase
from .worker import WorkerBase
from .connector import ConnectorBase
from .model_shape import ModelBase
from .store import StoreBase
from .pipeline import PipelineBase
from .orchestrator import OrchestratorBase
from .guard import GuardBase
from .scorer import ScorerBase
from .agent_shape import AgentBase
from .test_shape import TestBase
from .config_shape import ConfigBase
from .telemetry import TelemetryBase
from .glue import GlueBase


__all__ = [
    # Types
    "ShapeKind",
    "ShapeColour",
    "SHAPE_COLOUR_MAP",
    "HandoffProtocol",
    "TrafficLight",
    "EscalationFlag",
    "TrackingContext",
    "ValidatedInput",
    "WorkerResult",
    "WorkflowResult",
    "SignalClassification",
    "Rule",
    "Rejection",
    # Errors
    "ShapeError",
    "EntryError",
    "ConnectorError",
    "StoreError",
    "GuardHalt",
    "PipelineError",
    "WorkflowError",
    "ConfigError",
    "AgentError",
    "TelemetryError",
    "EpistemicViolation",
    "SpinePrinciple",
    "SpineViolation",
    # Epistemic
    "EpistemicTier",
    "PreconditionCheck",
    "ShapeProvenance",
    "StatusedOutput",
    "ShapeAuditRecord",
    "ShapeAuditLog",
    "SHAPE_AUDIT_LOG",
    # Decorators
    "monitored",
    "tracked",
    "validated",
    "retryable",
    "circuit_breaker",
    "no_bypass",
    "epistemic",
    "reader_first",
    "confidence_floor",
    "hash_protected",
    "transactional",
    "debt_tracked",
    "step",
    "workflow",
    "signal_classifier",
    "field",
    "setting",
    "secret",
    "metric",
    "spine",
    # Registry
    "REGISTRY",
    "ShapeRegistry",
    "METRICS",
    # Base
    "ShapeBase",
    # Shape base classes
    "EntryBase",
    "ServiceBase",
    "WorkerBase",
    "ConnectorBase",
    "ModelBase",
    "StoreBase",
    "PipelineBase",
    "OrchestratorBase",
    "GuardBase",
    "ScorerBase",
    "AgentBase",
    "TestBase",
    "ConfigBase",
    "TelemetryBase",
    "GlueBase",
]
