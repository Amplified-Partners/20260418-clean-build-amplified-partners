"""Synthetic-data unit tests for the base-rate test class.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from validators.tests import base_rate
from validators.verdict import VerdictBand


def test_base_rate_proven_within_tolerance() -> None:
    band, _, metrics, _ = base_rate.run(
        measured=0.18, claimed=0.20, direction="approx", tolerance=0.20
    )
    assert band == VerdictBand.PROVEN
    assert metrics["measured"] == 0.18
    assert metrics["claimed"] == 0.20


def test_base_rate_disproven_far_off() -> None:
    band, _, _, _ = base_rate.run(
        measured=0.45, claimed=0.20, direction="approx", tolerance=0.20
    )
    assert band == VerdictBand.DISPROVEN


def test_base_rate_proven_above_threshold() -> None:
    band, _, _, _ = base_rate.run(measured=0.30, claimed=0.20, direction="above", tolerance=0.10)
    assert band == VerdictBand.PROVEN


def test_base_rate_disproven_below_above_threshold() -> None:
    band, _, _, _ = base_rate.run(measured=0.05, claimed=0.20, direction="above", tolerance=0.10)
    assert band == VerdictBand.DISPROVEN


def test_base_rate_unmeasurable_is_plausible() -> None:
    band, msg, _, _ = base_rate.run(measured=None, claimed=0.20)
    assert band == VerdictBand.PLAUSIBLE
    assert "not measurable" in msg.lower() or "unmeasurable" in msg.lower()
