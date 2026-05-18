"""
ModelBase — a data shape definition.

Shape: model | Colour: BLUE | Position: contracts throughout
The contract for what data looks like. Every field is a decision about what matters.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import dataclasses
import logging
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import ShapeKind

log = logging.getLogger("amplified.shapes.model")


@spine("deterministic_first", "congruence")
class ModelBase(ShapeBase):
    """Base class for all model shapes.

    Defines fields, types, constraints. Validates data against the shape.
    Serialises / deserialises. Documents the meaning of each field.

    Subclasses define fields using @dataclasses.dataclass or class attributes.
    Subclasses MUST define:
        version: int    — models change, track it

    All fields MUST be typed. No Any. No untyped dicts.
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.MODEL
    version: ClassVar[int] = 1

    def validate(self) -> list[str]:
        """Validate all fields against their constraints. Returns list of errors."""
        errors: list[str] = []
        if not dataclasses.is_dataclass(self):
            return errors

        for f in dataclasses.fields(self):
            value = getattr(self, f.name, None)
            meta = f.metadata

            if meta.get("required", True) and value is None:
                errors.append(f"Field '{f.name}' is required but is None")
                continue

            if value is None:
                continue

            gt = meta.get("gt")
            if gt is not None and value <= gt:
                errors.append(f"Field '{f.name}': value {value} must be > {gt}")

            min_length = meta.get("min_length")
            if min_length is not None and hasattr(value, "__len__") and len(value) < min_length:
                errors.append(f"Field '{f.name}': length {len(value)} must be >= {min_length}")

        return errors

    def to_dict(self) -> dict[str, Any]:
        """Serialise to dictionary."""
        if dataclasses.is_dataclass(self):
            return dataclasses.asdict(self)  # type: ignore[arg-type]
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}

    @classmethod
    def field_descriptions(cls) -> dict[str, str]:
        """Return field name → description mapping."""
        if not dataclasses.is_dataclass(cls):
            return {}
        return {
            f.name: f.metadata.get("description", "")
            for f in dataclasses.fields(cls)  # type: ignore[arg-type]
        }
