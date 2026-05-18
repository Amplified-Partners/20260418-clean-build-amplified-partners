"""
Shape registry — every shape registers itself on creation.

The registry is the shape catalog. Vellum queries the catalog to pre-fill.
Without this, pre-fill is aspirational. With it, pre-fill is mechanical.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
import threading
from typing import Any

from ._types import ShapeKind, SpinePrinciple, SpineViolation

log = logging.getLogger("amplified.shapes.registry")


class ShapeRegistry:
    """Thread-safe registry of all shape instances and classes.

    Every shape, when created, registers itself: name, kind, domain, interface, version.
    Vellum queries the registry to pre-fill proformas.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._classes: dict[str, dict[str, Any]] = {}
        self._instances: dict[str, Any] = {}

    def register_class(self, cls: type) -> None:
        """Register a shape class. Called automatically by ShapeBase.__init_subclass__."""
        kind = getattr(cls, "shape_kind", None)
        entry = {
            "name": cls.__name__,
            "kind": kind.value if isinstance(kind, ShapeKind) else str(kind),
            "module": cls.__module__,
            "qualname": cls.__qualname__,
            "doc": (cls.__doc__ or "").strip(),
            "_cls_ref": cls,
        }
        with self._lock:
            self._classes[cls.__qualname__] = entry
        log.debug("REGISTRY class: %s (%s)", cls.__qualname__, entry["kind"])

    def register_instance(self, instance: Any) -> None:
        """Register a shape instance."""
        cls = type(instance)
        with self._lock:
            self._instances[id(instance)] = {
                "class": cls.__qualname__,
                "kind": getattr(cls, "shape_kind", "unknown"),
            }

    def get_by_kind(self, kind: ShapeKind) -> list[dict[str, Any]]:
        """Find all registered shape classes of a given kind."""
        with self._lock:
            return [
                entry
                for entry in self._classes.values()
                if entry["kind"] == kind.value
            ]

    def get_all(self) -> dict[str, dict[str, Any]]:
        """Return all registered shape classes."""
        with self._lock:
            return dict(self._classes)

    def count_by_kind(self) -> dict[str, int]:
        """Count registered shapes by kind."""
        counts: dict[str, int] = {}
        with self._lock:
            for entry in self._classes.values():
                kind = entry["kind"]
                counts[kind] = counts.get(kind, 0) + 1
        return counts

    def verify_spine_coverage(self) -> dict[str, Any]:
        """Verify that every spine principle is covered by at least one shape
        and every shape declares at least one spine principle.

        Returns a coverage report. Raises SpineViolation if any principle
        is uncovered — that's a dead principle, structural drift.
        """
        all_principles = set(SpinePrinciple)
        covered_principles: dict[SpinePrinciple, list[str]] = {p: [] for p in all_principles}
        unmoored_shapes: list[str] = []

        with self._lock:
            for qualname, entry in self._classes.items():
                # Look up the actual class to check _spine_principles
                # We store qualname, so we search by matching
                cls = entry.get("_cls_ref")
                spine_principles = getattr(cls, "_spine_principles", None) if cls else None

                if spine_principles is None:
                    # Try to find via the module system
                    spine_principles = None

                if spine_principles:
                    for p in spine_principles:
                        if p in covered_principles:
                            covered_principles[p].append(qualname)
                else:
                    unmoored_shapes.append(qualname)

        uncovered = [p for p, shapes in covered_principles.items() if not shapes]

        report = {
            "all_covered": len(uncovered) == 0,
            "all_moored": len(unmoored_shapes) == 0,
            "coverage": {
                p.value: [s for s in shapes]
                for p, shapes in covered_principles.items()
            },
            "uncovered_principles": [p.value for p in uncovered],
            "unmoored_shapes": unmoored_shapes,
        }

        if uncovered:
            names = ", ".join(p.label() for p in uncovered)
            raise SpineViolation(
                f"Dead principles — no shape enforces: {names}. "
                "Every principle must be structurally represented.",
                violation_type="uncovered_principle",
                principle=names,
            )

        return report


REGISTRY = ShapeRegistry()
