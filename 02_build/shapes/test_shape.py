"""
TestBase — the shape that proves the others work.

Shape: test | Colour: GREY | Position: proves throughout
A test should read like a specification. The documentation that can't lie.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import logging
import unittest
from typing import Any, ClassVar

from ._base import ShapeBase
from ._decorators import spine
from ._types import ShapeKind

log = logging.getLogger("amplified.shapes.test")


@spine("radical_honesty", "radical_transparency")
class TestBase(ShapeBase):
    """Base class for all test shapes.

    Exercises another shape with known inputs, asserts expected outputs,
    catches regressions, documents behaviour through examples.

    Subclasses MUST define:
        shape_under_test: type    — which shape does this test prove

    Test names are sentences. Assertions have messages. Fixtures tell a story.
    Note: does NOT inherit unittest.TestCase — use pytest or unittest directly
    alongside this base. This shape provides the contract and registration,
    not the test runner.
    """

    shape_kind: ClassVar[ShapeKind] = ShapeKind.TEST

    # --- subclass MUST define ---
    shape_under_test: ClassVar[type | None] = None

    def setup(self) -> None:
        """Set up the shape instance for testing. Override in subclass."""
        if self.shape_under_test is not None:
            self.shape = self.shape_under_test()

    def assert_shape_kind(self, instance: Any, expected: ShapeKind) -> None:
        """Assert that an instance is the expected shape kind."""
        actual = getattr(type(instance), "shape_kind", None)
        self.assertEqual(
            actual,
            expected,
            f"Expected shape kind {expected.value}, got {actual}",
        )
