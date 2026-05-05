# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Reusable test classes for the retail validator pipeline.

All test classes return (verdict: str, evidence: dict). Verdict ∈ {PROVEN,
PLAUSIBLE, DISPROVEN}. INCONCLUSIVE folds into PLAUSIBLE; REFUTED equals
DISPROVEN — see 01_truth/schemas/2026-05_public-data-validation_v1.md.
"""

from .existence import existence_check  # noqa: F401
from .base_rate import base_rate_test  # noqa: F401
from .correlation import correlation_test  # noqa: F401
from .distribution import distribution_test  # noqa: F401
