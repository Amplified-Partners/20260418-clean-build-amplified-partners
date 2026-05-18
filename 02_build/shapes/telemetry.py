"""
TelemetryBase — the sensors. The nervous system.

Shape: telemetry | Colour: GREY | Position: sensors throughout
Data for attention, not theatre. Signals route through Vellum to the right reader.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import ShapeKind, SignalClassification, TelemetryError, TrafficLight

log = logging.getLogger("amplified.shapes.telemetry")


@spine("radical_transparency", "shadow_first")
class TelemetryBase(ShapeBase):
    """Base class for all telemetry shapes.

    The sensors. What @monitor produces. Emits measurements,
    structures them into Vellum-ready records, routes signals,
    classifies by network shape, feeds the mycelial monitoring network.

    Every metric must answer a question someone will act on.
    A metric nobody looks at is noise. A metric everybody looks at
    but nobody acts on is theatre.
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.TELEMETRY

    def __init__(self) -> None:
        super().__init__()
        self._timeseries: dict[str, list[tuple[float, float]]] = defaultdict(list)
        self._baselines: dict[str, dict[str, float]] = {}
        self._calibration_count: dict[str, int] = defaultdict(int)
        self._calibration_target: int = 100  # first N runs establish baseline

    def record(self, metric_name: str, value: float) -> None:
        """Record a metric value with timestamp."""
        ts = time.monotonic()
        self._timeseries[metric_name].append((ts, value))
        self._calibration_count[metric_name] += 1

        # Auto-calibrate baseline during calibration period
        if self._calibration_count[metric_name] <= self._calibration_target:
            self._update_baseline(metric_name, value)

    def _update_baseline(self, metric_name: str, value: float) -> None:
        """Update running baseline during calibration period."""
        if metric_name not in self._baselines:
            self._baselines[metric_name] = {
                "sum": 0.0,
                "count": 0,
                "min": value,
                "max": value,
                "mean": value,
            }
        b = self._baselines[metric_name]
        b["sum"] += value
        b["count"] += 1
        b["min"] = min(b["min"], value)
        b["max"] = max(b["max"], value)
        b["mean"] = b["sum"] / b["count"]

    def is_calibrated(self, metric_name: str) -> bool:
        """Check if this metric has completed its calibration period."""
        return self._calibration_count.get(metric_name, 0) >= self._calibration_target

    def is_spike(self, metric_name: str, window_seconds: float = 300.0, threshold_factor: float = 3.0) -> bool:
        """Detect a transient spike in a metric."""
        if not self.is_calibrated(metric_name):
            return False
        baseline = self._baselines.get(metric_name)
        if baseline is None:
            return False
        recent = self._get_recent(metric_name, window_seconds)
        if not recent:
            return False
        recent_mean = sum(v for _, v in recent) / len(recent)
        return recent_mean > baseline["mean"] * threshold_factor

    def is_drift(self, metric_name: str, window_seconds: float = 3600.0, threshold_pct: float = 0.3) -> bool:
        """Detect gradual drift from baseline."""
        if not self.is_calibrated(metric_name):
            return False
        baseline = self._baselines.get(metric_name)
        if baseline is None or baseline["mean"] == 0:
            return False
        recent = self._get_recent(metric_name, window_seconds)
        if not recent:
            return False
        recent_mean = sum(v for _, v in recent) / len(recent)
        drift_pct = abs(recent_mean - baseline["mean"]) / baseline["mean"]
        return drift_pct > threshold_pct

    def classify(self, metric_name: str) -> SignalClassification:
        """Classify the current state of a metric. Override for custom classification."""
        if not self.is_calibrated(metric_name):
            return SignalClassification(shape="calibrating", severity=TrafficLight.GREEN.value)
        if self.is_spike(metric_name):
            return SignalClassification(shape="transient_spike", severity=TrafficLight.AMBER.value)
        if self.is_drift(metric_name):
            return SignalClassification(shape="drift", severity=TrafficLight.AMBER.value)
        return SignalClassification(shape="normal", severity=TrafficLight.GREEN.value)

    def _get_recent(self, metric_name: str, window_seconds: float) -> list[tuple[float, float]]:
        """Get metric values from the recent window."""
        now = time.monotonic()
        cutoff = now - window_seconds
        return [
            (ts, v)
            for ts, v in self._timeseries.get(metric_name, [])
            if ts >= cutoff
        ]
