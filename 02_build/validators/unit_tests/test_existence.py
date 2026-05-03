"""Synthetic-data unit tests for the existence test class.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from datetime import datetime, timezone

from validators.tests import existence
from validators.verdict import EvidenceItem, VerdictBand


def _ev(passed: bool) -> EvidenceItem:
    return EvidenceItem(
        source="synthetic",
        url="https://example.invalid/probe",
        accessed_at=datetime.now(timezone.utc).isoformat(),
        http_status=200 if passed else 404,
        response_sha256="0" * 64,
        summary="ok" if passed else "missing",
    )


def test_existence_proven_all_pass() -> None:
    probes = [
        lambda: (True, "probe-a passed", _ev(True)),
        lambda: (True, "probe-b passed", _ev(True)),
        lambda: (True, "probe-c passed", _ev(True)),
    ]
    band, _, metrics, ev = existence.run(probes)
    assert band == VerdictBand.PROVEN
    assert metrics["probes_passed"] == 3
    assert metrics["probes_total"] == 3
    assert len(ev) == 3


def test_existence_plausible_partial_pass() -> None:
    probes = [
        lambda: (True, "probe-a passed", _ev(True)),
        lambda: (False, "probe-b failed", _ev(False)),
    ]
    band, _, metrics, _ = existence.run(probes)
    assert band == VerdictBand.PLAUSIBLE
    assert metrics["probes_passed"] == 1


def test_existence_disproven_all_fail() -> None:
    probes = [
        lambda: (False, "probe-a failed", _ev(False)),
        lambda: (False, "probe-b failed", _ev(False)),
    ]
    band, _, metrics, _ = existence.run(probes)
    assert band == VerdictBand.DISPROVEN
    assert metrics["probes_passed"] == 0


def test_existence_disproven_when_no_probes() -> None:
    band, _, metrics, ev = existence.run([])
    assert band == VerdictBand.DISPROVEN
    assert metrics["probes_total"] == 0
    assert ev == []
