"""Reusable test classes for the public-data validators.

Each test takes evidence + a claim and returns a `Verdict` band. The four
classes cover most of the 136 catalogue entries:

- existence: does the data needed to support this recipe exist at the
  granularity claimed? (cheap; runs first)
- base_rate: does the published headline number match what the catalogue
  asserts (within tolerance)?
- correlation: do two series move together at the strength claimed?
- distribution: does the empirical distribution exceed the claimed threshold?

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from .base_rate import BaseRateClaim, base_rate_test
from .correlation import correlation_test, pearson_r
from .distribution import distribution_test
from .existence import ExistenceCheck, existence_test

__all__ = [
    "BaseRateClaim",
    "ExistenceCheck",
    "base_rate_test",
    "correlation_test",
    "distribution_test",
    "existence_test",
    "pearson_r",
]
