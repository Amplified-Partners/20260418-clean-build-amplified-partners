# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Synthetic-data unit tests for the four test classes.

Live-call integration tests (Land Registry, Companies House, …) live elsewhere
and run on Beast on a schedule, not in CI. This module deliberately uses no
network.
"""

from __future__ import annotations

from validators.core import VerdictBand
from validators.tests.base_rate import test_base_rate as _base_rate
from validators.tests.correlation import test_correlation as _correlation
from validators.tests.distribution import test_distribution as _distribution
from validators.tests.existence import test_existence as _existence


def test_existence_proven_when_rows_and_match():
    band, _ = _existence(rows=10, granularity_match=True, license_open=True)
    assert band == VerdictBand.PROVEN


def test_existence_plausible_when_granularity_off():
    band, _ = _existence(rows=10, granularity_match=False, license_open=True)
    assert band == VerdictBand.PLAUSIBLE


def test_existence_disproven_without_rows():
    band, _ = _existence(rows=0, granularity_match=True, license_open=True)
    assert band == VerdictBand.DISPROVEN


def test_base_rate_proven_within_tolerance():
    band, _ = _base_rate(observed_rate=0.10, claimed_rate=0.10, n=500, tolerance=0.20)
    assert band == VerdictBand.PROVEN


def test_base_rate_plausible_outside_tolerance_but_within_2x():
    band, _ = _base_rate(observed_rate=0.13, claimed_rate=0.10, n=500, tolerance=0.20)
    assert band == VerdictBand.PROVEN  # delta=0.03, tolerance=0.20 → still proven


def test_base_rate_disproven_far_off():
    band, _ = _base_rate(observed_rate=0.50, claimed_rate=0.10, n=500, tolerance=0.20)
    assert band == VerdictBand.DISPROVEN


def test_correlation_proven_high_r_correct_sign():
    a = list(range(50))
    b = [3 * x + 7 for x in a]
    band, _ = _correlation(
        series_a=a, series_b=b, expected_sign=1, r_threshold=0.6, p_threshold=0.01, minimum_n=24
    )
    assert band == VerdictBand.PROVEN


def test_correlation_disproven_wrong_sign():
    a = list(range(50))
    b = [-3 * x + 7 for x in a]
    band, _ = _correlation(
        series_a=a, series_b=b, expected_sign=1, r_threshold=0.6, minimum_n=24
    )
    assert band == VerdictBand.DISPROVEN


def test_distribution_proven_above_threshold_with_low_variance():
    samples = [10.0] * 40
    band, _ = _distribution(
        samples=samples, claim_threshold=5.0, direction=">=", minimum_n=30, sigma_floor=0.0
    )
    assert band == VerdictBand.PROVEN


def test_distribution_disproven_below_threshold():
    samples = [1.0] * 40
    band, _ = _distribution(samples=samples, claim_threshold=5.0, direction=">=", minimum_n=30)
    assert band == VerdictBand.DISPROVEN
