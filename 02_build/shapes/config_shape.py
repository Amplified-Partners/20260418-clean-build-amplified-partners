"""
ConfigBase — settings, thresholds, and environment values.

Shape: config | Colour: BLUE | Position: knobs throughout
Validates on load, fails fast. Every config difference between environments is a potential bug.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import dataclasses
import logging
import os
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import ConfigError, ShapeKind

log = logging.getLogger("amplified.shapes.config")


@spine("congruence", "privacy_first")
class ConfigBase(ShapeBase):
    """Base class for all config shapes.

    Settings, thresholds, environment values. The knobs.
    Typed access, validated on load, documented.

    Subclasses define settings using the setting() and secret() descriptors.
    Bad config = crash on startup, not at 3am.
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.CONFIG

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

    def load(self) -> None:
        """Load and validate all settings. Call on startup."""
        errors: list[str] = []
        if not dataclasses.is_dataclass(self):
            return

        for f in dataclasses.fields(self):
            meta = f.metadata
            value = getattr(self, f.name, None)

            # Load secrets from environment
            if meta.get("secret"):
                env_var = meta.get("env_var", "")
                if env_var:
                    env_value = os.environ.get(env_var, "")
                    if env_value:
                        object.__setattr__(self, f.name, env_value)
                        value = env_value
                    elif not value:
                        errors.append(
                            f"Secret '{f.name}': env var {env_var} not set"
                        )

            # Validate min/max
            min_value = meta.get("min_value")
            max_value = meta.get("max_value")
            if min_value is not None and value is not None:
                try:
                    if float(value) < min_value:
                        errors.append(
                            f"Setting '{f.name}': value {value} below minimum {min_value}"
                        )
                except (ValueError, TypeError):
                    pass
            if max_value is not None and value is not None:
                try:
                    if float(value) > max_value:
                        errors.append(
                            f"Setting '{f.name}': value {value} above maximum {max_value}"
                        )
                except (ValueError, TypeError):
                    pass

        if errors:
            raise ConfigError(
                f"Configuration validation failed: {'; '.join(errors)}",
                setting_name=errors[0].split("'")[1] if "'" in errors[0] else "",
            )

    def describe(self) -> dict[str, dict[str, Any]]:
        """Return all settings with their descriptions and current values."""
        if not dataclasses.is_dataclass(self):
            return {}
        return {
            f.name: {
                "value": getattr(self, f.name, None),
                "description": f.metadata.get("description", ""),
                "source": f.metadata.get("source", "config"),
                "secret": f.metadata.get("secret", False),
            }
            for f in dataclasses.fields(self)
        }
