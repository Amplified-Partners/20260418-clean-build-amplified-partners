"""Self-tests for the public-data validation framework.

Stdlib-only. No live HTTP. Run with:

    python3 -m unittest discover -s 02_build/validators -p 'test_validators.py'

Or directly:

    python3 02_build/validators/test_validators.py

These tests cover the mechanics — verdict bands, the four test classes, the
CLI plumbing, the cache key derivation. Live-HTTP integration tests for the
fetchers themselves are run separately on Beast (not in CI) so the test
suite stays hermetic.

Signed-by: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Make the 02_build directory importable so `validators` resolves regardless
# of the test runner's cwd.
_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR.parent))

from validators import cli as validators_cli  # noqa: E402
from validators.cache import _cache_key  # noqa: E402
from validators.core import (  # noqa: E402
    EvidenceBundle,
    EvidenceItem,
    TestClass,
    Verdict,
    VerdictBand,
    _default_signed_by,
    catalogue_line,
    write_verdict,
)
from validators.tests.base_rate import BaseRateClaim, base_rate_test  # noqa: E402
from validators.tests.correlation import correlation_test, pearson_r  # noqa: E402
from validators.tests.distribution import distribution_test  # noqa: E402
from validators.tests.existence import ExistenceCheck, existence_test  # noqa: E402
from validators.validations.profservices import RUNNERS  # noqa: E402

VERTICAL = "profservices"


def _evidence(summary: str = "synthetic") -> EvidenceItem:
    return EvidenceItem(
        source="synthetic",
        url="https://example.invalid/synthetic",
        accessed_at="2026-05-03T00:00:00Z",
        content_sha256="0" * 64,
        summary=summary,
        raw_path="/dev/null",
    )


class CacheKeyTest(unittest.TestCase):
    def test_param_order_is_canonical(self) -> None:
        a = _cache_key("https://x", {"a": "1", "b": "2"})
        b = _cache_key("https://x", {"b": "2", "a": "1"})
        self.assertEqual(a, b)

    def test_url_difference_changes_key(self) -> None:
        a = _cache_key("https://x", None)
        b = _cache_key("https://y", None)
        self.assertNotEqual(a, b)

    def test_param_difference_changes_key(self) -> None:
        a = _cache_key("https://x", {"a": "1"})
        b = _cache_key("https://x", {"a": "2"})
        self.assertNotEqual(a, b)


class ExistenceTestClass(unittest.TestCase):
    def test_proven_when_all_required_substrings_present(self) -> None:
        body = b"<html>Companies House publishes UK company accounts</html>"
        verdict = existence_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            body=body,
            evidence_item=_evidence(),
            checks=[
                ExistenceCheck("CH mention", ("Companies House",)),
                ExistenceCheck("accounts mention", ("accounts",)),
            ],
        )
        self.assertEqual(verdict.band, VerdictBand.PROVEN)

    def test_disproven_when_any_substring_missing(self) -> None:
        body = b"<html>Just talking about beans</html>"
        verdict = existence_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            body=body,
            evidence_item=_evidence(),
            checks=[
                ExistenceCheck("CH mention", ("Companies House",)),
            ],
        )
        self.assertEqual(verdict.band, VerdictBand.DISPROVEN)


class BaseRateTestClass(unittest.TestCase):
    def test_proven_when_median_in_range(self) -> None:
        body = b"Q1 was 9.4%, Q2 was 9.6%, Q3 was 10.1%, Q4 was 10.3%."
        claim = BaseRateClaim(
            description="services PPI is in 9-11%",
            pattern=r"(\d+\.\d+)%",
            low=9.0,
            high=11.0,
            units="percent",
        )
        verdict = base_rate_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            body=body,
            evidence_item=_evidence(),
            claim=claim,
        )
        self.assertEqual(verdict.band, VerdictBand.PROVEN)
        self.assertGreaterEqual(verdict.statistic["matches"], 2)

    def test_disproven_when_median_out_of_range(self) -> None:
        body = b"The numbers were 50.0% and 55.0%."
        claim = BaseRateClaim(
            description="services PPI is in 9-11%",
            pattern=r"(\d+\.\d+)%",
            low=9.0,
            high=11.0,
            units="percent",
        )
        verdict = base_rate_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            body=body,
            evidence_item=_evidence(),
            claim=claim,
        )
        self.assertEqual(verdict.band, VerdictBand.DISPROVEN)

    def test_median_for_even_length_list_averages_two_middle(self) -> None:
        """Regression: even-length lists must average the two middle values.

        With four values [9.0, 9.5, 10.5, 11.0] the true median is 10.0.
        The pre-fix code returned `numbers_sorted[len // 2]` = 10.5
        (upper-middle), which would mis-band a claim like high=10.2 as
        PROVEN when the correct verdict is DISPROVEN.
        """
        body = b"9.0%, 9.5%, 10.5%, 11.0%."
        claim = BaseRateClaim(
            description="median falls inside 9-10.2",
            pattern=r"(\d+\.\d+)%",
            low=9.0,
            high=10.2,
            units="percent",
        )
        verdict = base_rate_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            body=body,
            evidence_item=_evidence(),
            claim=claim,
        )
        # True median of [9.0, 9.5, 10.5, 11.0] is 10.0 → in [9.0, 10.2]
        # so PROVEN. Pre-fix would have picked 10.5 → DISPROVEN.
        self.assertEqual(verdict.statistic["median"], 10.0)
        self.assertEqual(verdict.band, VerdictBand.PROVEN)

    def test_median_for_odd_length_list_picks_middle(self) -> None:
        body = b"5.0%, 7.0%, 11.0%."
        claim = BaseRateClaim(
            description="middle value 7%",
            pattern=r"(\d+\.\d+)%",
            low=6.0,
            high=8.0,
            units="percent",
        )
        verdict = base_rate_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            body=body,
            evidence_item=_evidence(),
            claim=claim,
        )
        self.assertEqual(verdict.statistic["median"], 7.0)
        self.assertEqual(verdict.band, VerdictBand.PROVEN)


class CorrelationTestClass(unittest.TestCase):
    def test_pearson_perfect_positive(self) -> None:
        self.assertAlmostEqual(pearson_r([1, 2, 3, 4], [2, 4, 6, 8]), 1.0)

    def test_pearson_perfect_negative(self) -> None:
        self.assertAlmostEqual(pearson_r([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)

    def test_pearson_zero_variance_returns_zero(self) -> None:
        self.assertEqual(pearson_r([1, 1, 1, 1], [4, 3, 2, 1]), 0.0)

    def test_pearson_short_series_returns_zero(self) -> None:
        self.assertEqual(pearson_r([1.0], [2.0]), 0.0)

    def test_correlation_proven_when_strong_and_powered(self) -> None:
        x = list(range(10))
        y = [2 * v + 1 for v in x]
        verdict = correlation_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            series_a=x,
            series_b=y,
            threshold=0.7,
            evidence=EvidenceBundle(items=[_evidence("series-a"), _evidence("series-b")]),
        )
        self.assertEqual(verdict.band, VerdictBand.PROVEN)

    def test_correlation_plausible_when_underpowered(self) -> None:
        x = [1, 2, 3]
        y = [2, 4, 6]
        verdict = correlation_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            series_a=x,
            series_b=y,
            threshold=0.7,
            evidence=EvidenceBundle(items=[_evidence("series-a"), _evidence("series-b")]),
        )
        self.assertEqual(verdict.band, VerdictBand.PLAUSIBLE)

    def test_correlation_disproven_when_no_signal(self) -> None:
        x = list(range(10))
        y = [1.0, -1.0] * 5
        verdict = correlation_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            series_a=x,
            series_b=y,
            threshold=0.7,
            evidence=EvidenceBundle(items=[_evidence("series-a"), _evidence("series-b")]),
        )
        self.assertEqual(verdict.band, VerdictBand.DISPROVEN)


class DistributionTestClass(unittest.TestCase):
    def test_proven_when_share_within_tolerance(self) -> None:
        # 70% of samples > 10
        samples = [12.0] * 7 + [3.0] * 3
        verdict = distribution_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            samples=samples,
            threshold=10.0,
            expected_share_above=0.7,
            tolerance=0.1,
            evidence=EvidenceBundle(items=[_evidence("dist")]),
        )
        self.assertEqual(verdict.band, VerdictBand.PROVEN)

    def test_disproven_when_share_outside_tolerance(self) -> None:
        # observed share = 0% but expected 70%
        samples = [3.0] * 10
        verdict = distribution_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            samples=samples,
            threshold=10.0,
            expected_share_above=0.7,
            tolerance=0.1,
            evidence=EvidenceBundle(items=[_evidence("dist")]),
        )
        self.assertEqual(verdict.band, VerdictBand.DISPROVEN)

    def test_plausible_when_underpowered(self) -> None:
        verdict = distribution_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            samples=[12.0, 3.0],
            threshold=10.0,
            expected_share_above=0.5,
            tolerance=0.1,
            evidence=EvidenceBundle(items=[_evidence("dist")]),
        )
        self.assertEqual(verdict.band, VerdictBand.PLAUSIBLE)


class VerdictSerialisationTest(unittest.TestCase):
    def test_round_trip_to_disk(self) -> None:
        bundle = EvidenceBundle()
        bundle.add(_evidence("src1"))
        verdict = Verdict(
            insight_id="INS-079",
            vertical=VERTICAL,
            band=VerdictBand.PROVEN,
            test_class=TestClass.EXISTENCE,
            method="synthetic",
            finding="ok",
            statistic={"n": 1},
            evidence=bundle,
            notes=["a note"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp)
            written = write_verdict(verdict, output_root)
            self.assertTrue(written.exists())
            payload = json.loads(written.read_text())
            self.assertEqual(payload["band"], "PROVEN")
            self.assertEqual(payload["insight_id"], "INS-079")
            self.assertEqual(len(payload["evidence"]), 1)

    def test_catalogue_line_format(self) -> None:
        bundle = EvidenceBundle()
        bundle.add(_evidence())
        verdict = Verdict(
            insight_id="INS-079",
            vertical=VERTICAL,
            band=VerdictBand.PROVEN,
            test_class=TestClass.EXISTENCE,
            method="synthetic",
            finding="ok",
            statistic={"n": 1},
            evidence=bundle,
            notes=[],
        )
        line = catalogue_line(verdict, "03_shadow/validators/profservices/INS-079/verdict.json")
        self.assertIn("PROVEN", line)
        self.assertIn("existence", line)
        self.assertIn("03_shadow/validators/profservices/INS-079/verdict.json", line)


class RunnerCoverageTest(unittest.TestCase):
    def test_all_sixteen_profservices_runners_registered(self) -> None:
        expected = {f"INS-{n:03d}" for n in range(79, 95)}
        self.assertEqual(set(RUNNERS), expected)


class INS094ConditionalASHETest(unittest.TestCase):
    """run_INS_094's statistic must reflect whether ASHE actually fetched."""

    def test_statistic_reflects_ashe_blocked(self) -> None:
        import urllib.error
        from validators.sources import companies_house, ons
        from validators.validations import profservices

        with mock.patch.object(
            companies_house,
            "bulk_index",
            return_value=(b"<html>company filings</html>", _evidence()),
        ), mock.patch.object(
            ons,
            "nomis_dataset_definition",
            side_effect=urllib.error.URLError("nomis offline"),
        ):
            verdict = profservices.run_INS_094()

        self.assertEqual(verdict.statistic["public_legs_validated"], 1)
        self.assertEqual(verdict.statistic["public_legs_blocked"], 2)
        self.assertIn("Nomis ASHE", verdict.method)
        self.assertIn("unreachable", verdict.method)

    def test_statistic_reflects_ashe_reachable(self) -> None:
        from validators.sources import companies_house, ons
        from validators.validations import profservices

        with mock.patch.object(
            companies_house,
            "bulk_index",
            return_value=(b"<html>company filings</html>", _evidence()),
        ), mock.patch.object(
            ons,
            "nomis_dataset_definition",
            return_value=({"definition": "ok"}, _evidence()),
        ):
            verdict = profservices.run_INS_094()

        self.assertEqual(verdict.statistic["public_legs_validated"], 2)
        self.assertEqual(verdict.statistic["public_legs_blocked"], 1)
        self.assertIn("both reachable", verdict.method)


class SignedByDefaultTest(unittest.TestCase):
    def test_reads_from_env_when_set(self) -> None:
        with mock.patch.dict(os.environ, {"AMP_SIGNED_BY": "Tester | 2099-01-01"}):
            self.assertEqual(_default_signed_by(), "Tester | 2099-01-01")

    def test_unsigned_placeholder_when_env_missing(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIn("unsigned", _default_signed_by())


class CatalogueLineFormatTest(unittest.TestCase):
    def test_evidence_path_is_backticked(self) -> None:
        bundle = EvidenceBundle()
        bundle.add(_evidence())
        verdict = Verdict(
            insight_id="INS-079",
            vertical=VERTICAL,
            band=VerdictBand.PROVEN,
            test_class=TestClass.EXISTENCE,
            method="m",
            finding="f",
            statistic={},
            evidence=bundle,
            notes=[],
        )
        line = catalogue_line(verdict, "03_shadow/validators/profservices/INS-079/verdict.json")
        self.assertIn("`03_shadow/validators/profservices/INS-079/verdict.json`", line)


class ExistenceStatisticConsistencyTest(unittest.TestCase):
    def test_disproven_statistics_count_checks_not_tokens(self) -> None:
        # One check with 3 must_contain tokens, all of which are missing.
        # Old buggy code would compute checks_passed = 1 - 3 = -2.
        body = b"empty"
        verdict = existence_test(
            insight_id="INS-TEST",
            vertical=VERTICAL,
            method="synthetic",
            body=body,
            evidence_item=_evidence(),
            checks=[
                ExistenceCheck("triple-token check", ("alpha", "beta", "gamma")),
            ],
        )
        self.assertEqual(verdict.band, VerdictBand.DISPROVEN)
        self.assertEqual(verdict.statistic["checks_passed"], 0)
        self.assertEqual(verdict.statistic["checks_failed"], 1)
        self.assertEqual(verdict.statistic["tokens_checked"], 3)
        self.assertEqual(verdict.statistic["tokens_missing"], 3)
        self.assertGreaterEqual(verdict.statistic["checks_passed"], 0)


class CacheKeyURLWithExistingQueryTest(unittest.TestCase):
    """Regression test for the `?`/`&` separator bug in `_cache_key`.

    With the buggy code, calling ``_cache_key("https://x?a=1", {"b": "2"})``
    produced a hash of the malformed URL ``https://x?a=1?b=2`` — different
    from the actually-fetched URL ``https://x?a=1&b=2``. The fixed code
    must produce the same hash as the well-formed canonical URL.
    """

    def test_well_formed_canonical_when_url_has_query(self) -> None:
        keyed = _cache_key("https://x.example/path?a=1", {"b": "2"})
        well_formed = hashlib.sha256(
            "https://x.example/path?a=1&b=2".encode("utf-8")
        ).hexdigest()
        self.assertEqual(keyed, well_formed)

    def test_no_query_uses_question_mark(self) -> None:
        keyed = _cache_key("https://x.example/path", {"b": "2"})
        well_formed = hashlib.sha256(
            "https://x.example/path?b=2".encode("utf-8")
        ).hexdigest()
        self.assertEqual(keyed, well_formed)


class CliDisplayPathTest(unittest.TestCase):
    def test_returns_relative_when_path_is_under_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp).resolve()
            inside = repo / "03_shadow" / "x.json"
            inside.parent.mkdir(parents=True)
            inside.write_text("{}")
            self.assertEqual(
                validators_cli._display_path(inside, repo),
                Path("03_shadow/x.json"),
            )

    def test_returns_absolute_when_path_is_outside_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as repo_tmp, tempfile.TemporaryDirectory() as out_tmp:
            repo = Path(repo_tmp).resolve()
            outside = Path(out_tmp).resolve() / "verdicts" / "x.json"
            outside.parent.mkdir(parents=True)
            outside.write_text("{}")
            # Must NOT raise ValueError; must return the absolute path so
            # the caller's print statement still works.
            displayed = validators_cli._display_path(outside, repo)
            self.assertEqual(displayed, outside)


class CliInsightArgTest(unittest.TestCase):
    """Regression test for argparse repeated `--insight` flag handling."""

    def test_repeated_insight_flag_extends(self) -> None:
        parser = validators_cli.build_parser()
        ns = parser.parse_args(
            [
                "run",
                "--vertical",
                "profservices",
                "--insight",
                "INS-079",
                "--insight",
                "INS-093",
            ]
        )
        self.assertEqual(ns.insight, ["INS-079", "INS-093"])

    def test_multi_value_insight_flag(self) -> None:
        parser = validators_cli.build_parser()
        ns = parser.parse_args(
            [
                "run",
                "--vertical",
                "profservices",
                "--insight",
                "INS-079",
                "INS-093",
            ]
        )
        self.assertEqual(ns.insight, ["INS-079", "INS-093"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
