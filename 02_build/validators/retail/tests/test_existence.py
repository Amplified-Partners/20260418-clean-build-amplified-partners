# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Tests for `existence_check` verdict logic.

Locks in the four-band semantics described in the docstring + the failed-
source branch added in response to Devin Review on commit b3ae408 (the
`require_all=False` default was silently accepting partial coverage as
PROVEN — INS-062 had n_reachable=1, n_failed=1, was reported PROVEN).

Run from repo root:
  PYTHONPATH=02_build python -m unittest validators.retail.tests.test_existence
"""
from __future__ import annotations

import unittest

from .existence import existence_check


def _ev(status: int, *, skipped: bool = False) -> dict:
    """Minimal evidence dict shape that existence_check inspects."""
    sample: dict = {"_skipped": True} if skipped else {}
    return {"status": status, "sample": sample, "url": "https://x", "source": "t"}


class ExistenceCheckTest(unittest.TestCase):
    def test_all_reachable_returns_proven(self):
        verdict, bundle = existence_check("c", [_ev(200), _ev(200)])
        self.assertEqual(verdict, "PROVEN")
        self.assertEqual(bundle["n_reachable"], 2)
        self.assertEqual(bundle["n_failed"], 0)

    def test_all_failed_returns_disproven(self):
        verdict, bundle = existence_check("c", [_ev(404), _ev(500)])
        self.assertEqual(verdict, "DISPROVEN")
        self.assertEqual(bundle["n_reachable"], 0)

    def test_mixed_reachable_and_keyless_skipped_returns_plausible(self):
        verdict, bundle = existence_check("c", [_ev(200), _ev(0, skipped=True)])
        self.assertEqual(verdict, "PLAUSIBLE")
        self.assertIn("need a key", bundle["reason"])

    def test_mixed_reachable_and_failed_returns_plausible(self):
        """The fix from Devin Review on b3ae408.

        Previously a 200 + 404 mix returned PROVEN ("all 1 sources reachable"),
        ignoring the failed source. Must return PLAUSIBLE — partial coverage
        is not full coverage.
        """
        verdict, bundle = existence_check("c", [_ev(200), _ev(404)])
        self.assertEqual(verdict, "PLAUSIBLE")
        self.assertEqual(bundle["n_reachable"], 1)
        self.assertEqual(bundle["n_failed"], 1)
        self.assertIn("failed", bundle["reason"])

    def test_require_all_with_one_failed_returns_plausible(self):
        verdict, bundle = existence_check("c", [_ev(200), _ev(404)], require_all=True)
        self.assertEqual(verdict, "PLAUSIBLE")
        self.assertIn("required sources reachable", bundle["reason"])


if __name__ == "__main__":
    unittest.main()
