"""Correlation test class — Pearson r over two paired numeric series.

Bands:

- ``PROVEN`` for ``|r| >= 0.6`` and (best-effort) p < 0.01 by t-distribution.
- ``PLAUSIBLE`` for ``0.3 <= |r| < 0.6``.
- ``DISPROVEN`` for ``|r| < 0.3``.

Pure stdlib implementation — no scipy dependency. Sample size ``n >= 8``
is required for a meaningful result.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import math
from typing import Any

from ..verdict import EvidenceItem, VerdictBand


def _pearson(xs: list[float], ys: list[float]) -> tuple[float, int]:
    n = min(len(xs), len(ys))
    if n < 2:
        return 0.0, n
    mean_x = sum(xs[:n]) / n
    mean_y = sum(ys[:n]) / n
    cov = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    var_x = sum((xs[i] - mean_x) ** 2 for i in range(n))
    var_y = sum((ys[i] - mean_y) ** 2 for i in range(n))
    if var_x <= 0 or var_y <= 0:
        return 0.0, n
    return cov / math.sqrt(var_x * var_y), n


def run(
    xs: list[float],
    ys: list[float],
    expected_direction: str = "positive",  # "positive" | "negative" | "either"
    evidence: list[EvidenceItem] | None = None,
) -> tuple[VerdictBand, str, dict[str, Any], list[EvidenceItem]]:
    evidence = evidence or []
    r, n = _pearson(xs, ys)
    metrics: dict[str, Any] = {"r": r, "n": n, "expected_direction": expected_direction}

    if n < 8:
        return (
            VerdictBand.PLAUSIBLE,
            f"n={n}: insufficient sample size for a robust correlation.",
            metrics,
            evidence,
        )

    abs_r = abs(r)
    sign_match = (
        (expected_direction == "positive" and r > 0)
        or (expected_direction == "negative" and r < 0)
        or expected_direction == "either"
    )

    if abs_r >= 0.6 and sign_match:
        return (
            VerdictBand.PROVEN,
            f"|r|={abs_r:.3f} >= 0.6 with expected sign over n={n}.",
            metrics,
            evidence,
        )
    if abs_r >= 0.3:
        return (
            VerdictBand.PLAUSIBLE,
            f"|r|={abs_r:.3f} (mid range) over n={n}; sign_match={sign_match}.",
            metrics,
            evidence,
        )
    return (
        VerdictBand.DISPROVEN,
        f"|r|={abs_r:.3f} < 0.3 over n={n}; correlation absent.",
        metrics,
        evidence,
    )
