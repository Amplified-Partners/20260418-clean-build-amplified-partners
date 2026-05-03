"""Correlation test class — Pearson r over two paired numeric series.

Bands:

- ``PROVEN`` if ``|r| >= 0.6`` AND the two-sided p-value is below
  ``ALPHA`` (default 0.01) AND the sign matches the expected direction.
  The p-value is computed from the Fisher z-transform
  ``z = atanh(r) * sqrt(n - 3)``, which is approximately N(0, 1) under
  H0: rho = 0; this is a standard, scipy-free test for n >= 8.
- ``PLAUSIBLE`` for ``0.3 <= |r| < 0.6``, or for ``|r| >= 0.6`` with
  ``p >= ALPHA`` (effect size large enough but sample too small to
  reject the null at the documented confidence level).
- ``DISPROVEN`` for ``|r| < 0.3``.

Pure stdlib implementation — no scipy dependency. Sample size ``n >= 8``
is required for a meaningful result.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import math
from typing import Any

from ..verdict import EvidenceItem, VerdictBand

ALPHA = 0.01


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


def _two_sided_p_value(r: float, n: int) -> float:
    """Fisher z-transform two-sided p-value against H0: rho = 0.

    Uses ``z = atanh(r) * sqrt(n - 3)`` which is approximately N(0, 1) under
    the null. ``p = 2 * (1 - Phi(|z|))`` with ``Phi`` derived from
    ``math.erf``. Returns 1.0 (i.e. cannot reject) for ``n <= 3`` or
    ``|r| >= 1`` (degenerate input).
    """
    if n <= 3 or abs(r) >= 1.0:
        return 1.0
    z = math.atanh(abs(r)) * math.sqrt(n - 3)
    # Phi(z) = 0.5 * (1 + erf(z / sqrt(2)))
    cdf = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    return max(0.0, min(1.0, 2.0 * (1.0 - cdf)))


def run(
    xs: list[float],
    ys: list[float],
    expected_direction: str = "positive",  # "positive" | "negative" | "either"
    evidence: list[EvidenceItem] | None = None,
) -> tuple[VerdictBand, str, dict[str, Any], list[EvidenceItem]]:
    evidence = evidence or []
    r, n = _pearson(xs, ys)
    p = _two_sided_p_value(r, n)
    metrics: dict[str, Any] = {
        "r": r,
        "n": n,
        "p_value": p,
        "alpha": ALPHA,
        "expected_direction": expected_direction,
    }

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

    if abs_r >= 0.6 and sign_match and p < ALPHA:
        return (
            VerdictBand.PROVEN,
            f"|r|={abs_r:.3f} >= 0.6 with expected sign over n={n} (p={p:.4f} < {ALPHA}).",
            metrics,
            evidence,
        )
    if abs_r >= 0.6 and sign_match:
        return (
            VerdictBand.PLAUSIBLE,
            (
                f"|r|={abs_r:.3f} >= 0.6 with expected sign over n={n}, "
                f"but p={p:.4f} >= {ALPHA}: effect size large, sample underpowered."
            ),
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
