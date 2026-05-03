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


def test_base_rate_handles_negative_claimed() -> None:
    """A negative claimed rate (e.g. a percentage drop measured with sign)
    must still produce the correct band — the deviation formula divides by
    abs(claimed), so the sign of `claimed` does not flip the comparison."""
    far = base_rate.run(measured=-0.10, claimed=-0.50, direction="approx", tolerance=0.20)
    assert far[0] == VerdictBand.DISPROVEN
    near = base_rate.run(measured=-0.45, claimed=-0.50, direction="approx", tolerance=0.20)
    assert near[0] == VerdictBand.PROVEN


def test_base_rate_above_below_handle_negative_claimed() -> None:
    """For negative ``claimed`` the directional band must use abs(claimed)
    so a 20% tolerance on -0.50 means [-0.60, -0.40] (not [-0.40, -0.60])."""
    # "above": measured -0.45 IS above claimed -0.50, within 20% band → PROVEN
    above_pass = base_rate.run(measured=-0.45, claimed=-0.50, direction="above", tolerance=0.20)
    assert above_pass[0] == VerdictBand.PROVEN
    # "above": measured -0.80 is below the band lower bound -0.60 → DISPROVEN
    above_fail = base_rate.run(measured=-0.80, claimed=-0.50, direction="above", tolerance=0.20)
    assert above_fail[0] == VerdictBand.DISPROVEN
    # "below": measured -0.55 is below claimed -0.50 within 20% band → PROVEN
    below_pass = base_rate.run(measured=-0.55, claimed=-0.50, direction="below", tolerance=0.20)
    assert below_pass[0] == VerdictBand.PROVEN
    # "below": measured -0.30 is above the band upper bound -0.40 → DISPROVEN
    below_fail = base_rate.run(measured=-0.30, claimed=-0.50, direction="below", tolerance=0.20)
    assert below_fail[0] == VerdictBand.DISPROVEN
