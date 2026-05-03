"""Synthetic-data unit tests for the correlation test class.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from validators.tests import correlation
from validators.verdict import VerdictBand


def test_correlation_proven_strong_positive() -> None:
    xs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ys = [2, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    band, _, metrics, _ = correlation.run(xs, ys, expected_direction="positive")
    assert band == VerdictBand.PROVEN
    assert metrics["r"] > 0.95
    assert metrics["n"] == 10


def test_correlation_disproven_no_signal() -> None:
    import random

    xs = list(range(1, 11))
    random.seed(2)  # |r| ~ 0.15
    ys = [random.random() * 10 for _ in xs]
    band, _, metrics, _ = correlation.run(xs, ys, expected_direction="positive")
    assert band == VerdictBand.DISPROVEN
    assert abs(metrics["r"]) < 0.3


def test_correlation_plausible_mid_range() -> None:
    import random

    xs = list(range(1, 11))
    random.seed(4)  # |r| ~ 0.54
    ys = [random.random() * 10 for _ in xs]
    band, _, metrics, _ = correlation.run(xs, ys, expected_direction="positive")
    assert band == VerdictBand.PLAUSIBLE
    assert 0.3 <= abs(metrics["r"]) < 0.6


def test_correlation_underpowered_sample() -> None:
    xs = [1.0, 2.0, 3.0]
    ys = [2.0, 4.0, 6.0]
    band, msg, metrics, _ = correlation.run(xs, ys)
    assert band == VerdictBand.PLAUSIBLE
    assert metrics["n"] == 3
    assert "insufficient" in msg


def test_correlation_sign_mismatch_demoted_to_plausible() -> None:
    # Strong negative r against a "positive" expectation lands as PLAUSIBLE
    # (signal exists but wrong direction).
    xs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ys = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    band, _, metrics, _ = correlation.run(xs, ys, expected_direction="positive")
    assert band == VerdictBand.PLAUSIBLE
    assert metrics["r"] < -0.95
