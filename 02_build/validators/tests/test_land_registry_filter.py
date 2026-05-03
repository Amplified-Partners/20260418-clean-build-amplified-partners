# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Regression tests for ``land_registry.filter_by_postcode_prefix``.

UK postcodes are ``OUTWARD INWARD`` with a single space (e.g. ``"NE1 1AA"``).
The first version of the filter used a pure ``startswith``-style regex which
matched ``"NE1"`` against ``"NE10 ..."``, ``"NE12 ..."`` etc. — inflating
test counts ~10x. These tests pin the corrected boundary behaviour.
"""

from __future__ import annotations

import pandas as pd

from validators.sources.land_registry import filter_by_postcode_prefix


def _df(postcodes: list[str]) -> pd.DataFrame:
    return pd.DataFrame({"postcode": postcodes})


def test_ne1_does_not_match_ne10_or_ne12() -> None:
    """The whole point: ``NE1`` must not pull in NE10-NE19 etc."""
    df = _df(["NE1 1AA", "NE10 5BB", "NE12 3CC", "NE1 7XY"])
    out = filter_by_postcode_prefix(df, ["NE1"])
    assert sorted(out["postcode"].tolist()) == ["NE1 1AA", "NE1 7XY"]


def test_ne2_does_not_match_ne20_ne28() -> None:
    df = _df(["NE2 4AB", "NE20 9PP", "NE28 7QQ"])
    out = filter_by_postcode_prefix(df, ["NE2"])
    assert out["postcode"].tolist() == ["NE2 4AB"]


def test_multiple_prefixes_combined() -> None:
    df = _df(["NE1 1AA", "NE2 2BB", "NE3 3CC", "NE10 0DD", "NE33 5EE", "SW1A 1AA"])
    out = filter_by_postcode_prefix(df, ["NE1", "NE2", "NE3"])
    assert sorted(out["postcode"].tolist()) == ["NE1 1AA", "NE2 2BB", "NE3 3CC"]


def test_outward_only_postcode_matches() -> None:
    """Some Land Registry rows store only the outward part with no inward."""
    df = _df(["NE1", "NE10"])
    out = filter_by_postcode_prefix(df, ["NE1"])
    assert out["postcode"].tolist() == ["NE1"]


def test_empty_dataframe_is_a_passthrough() -> None:
    df = pd.DataFrame(columns=["postcode"])
    out = filter_by_postcode_prefix(df, ["NE1"])
    assert out.empty


def test_case_insensitive() -> None:
    df = _df(["ne1 1aa", "Ne2 2bb"])
    out = filter_by_postcode_prefix(df, ["NE1", "NE2"])
    assert sorted(out["postcode"].tolist()) == ["Ne2 2bb", "ne1 1aa"]
