"""Synthetic-data unit tests for the distribution test class.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from validators.tests import distribution
from validators.verdict import VerdictBand


def test_distribution_proven_above_one_sigma() -> None:
    sample = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    band, _, metrics, _ = distribution.run(sample=sample, claim=10.0, quantile=0.5)
    assert band == VerdictBand.PROVEN
    assert metrics["z"] >= 1.0


def test_distribution_disproven_below_one_sigma() -> None:
    sample = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    band, _, metrics, _ = distribution.run(sample=sample, claim=20.0, quantile=0.5)
    assert band == VerdictBand.DISPROVEN
    assert metrics["z"] <= -1.0


def test_distribution_plausible_within_one_sigma() -> None:
    sample = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    band, _, metrics, _ = distribution.run(sample=sample, claim=15.0, quantile=0.5)
    assert band == VerdictBand.PLAUSIBLE
    assert -1.0 < metrics["z"] < 1.0


def test_distribution_underpowered() -> None:
    band, msg, _, _ = distribution.run(sample=[1.0, 2.0], claim=1.0)
    assert band == VerdictBand.PLAUSIBLE
    assert "insufficient" in msg.lower()
