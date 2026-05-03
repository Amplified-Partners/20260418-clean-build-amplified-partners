# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""HM Land Registry — Price Paid Data (no authentication required).

Bulk CSV download. ~30 MB per year. Cached on first run.

URL shape:
    http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-{year}.csv
    http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv

Schema (no header in file, columns 1-16):
    1. Transaction unique identifier (UUID)
    2. Price (GBP integer)
    3. Date of Transfer (YYYY-MM-DD HH:MM)
    4. Postcode (full)
    5. Property Type (D=detached, S=semi, T=terrace, F=flat/maisonette, O=other)
    6. Old/New (Y=newbuild, N=established)
    7. Duration (F=freehold, L=leasehold)
    8. PAON, 9. SAON, 10. Street, 11. Locality, 12. Town/City, 13. District, 14. County
    15. PPD Category Type (A=standard, B=other)
    16. Record Status (A/C/D)

OGL — free commercial reuse.
"""

from __future__ import annotations

import io
from collections.abc import Sequence

import pandas as pd

from ..core import SourceRef
from ._http import fetch_bytes

LAND_REGISTRY_BASE = "http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com"

PPD_COLUMNS = [
    "transaction_id",
    "price",
    "date_of_transfer",
    "postcode",
    "property_type",
    "old_new",
    "duration",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status",
]


def fetch_year(year: int) -> tuple[pd.DataFrame, SourceRef]:
    """Yearly CSV file for ``year`` (e.g. 2024)."""
    url = f"{LAND_REGISTRY_BASE}/pp-{year}.csv"
    return _fetch_and_parse(name="land_registry", url=url)


def fetch_monthly_update() -> tuple[pd.DataFrame, SourceRef]:
    """Latest-month update file (small, refreshed monthly)."""
    url = f"{LAND_REGISTRY_BASE}/pp-monthly-update-new-version.csv"
    return _fetch_and_parse(name="land_registry", url=url)


def filter_by_postcode_prefix(
    df: pd.DataFrame, prefixes: Sequence[str]
) -> pd.DataFrame:
    """Keep rows whose outward postcode equals any of ``prefixes``.

    UK postcodes are formatted ``OUTWARD INWARD`` with a single space
    (e.g. ``"NE1 1AA"``). We anchor the prefix on the space or end-of-string
    so ``"NE1"`` matches only NE1-postcodes, not NE10..NE19.
    """
    if df.empty:
        return df
    pattern = "^(" + "|".join(p.upper().strip() for p in prefixes) + r")(\s|$)"
    mask = df["postcode"].fillna("").str.upper().str.match(pattern)
    return df.loc[mask].copy()


def filter_by_date_range(
    df: pd.DataFrame, start: str, end: str
) -> pd.DataFrame:
    """Keep rows with ``date_of_transfer`` in [start, end] inclusive (ISO date strings)."""
    if df.empty:
        return df
    dates = pd.to_datetime(df["date_of_transfer"], errors="coerce")
    mask = (dates >= pd.Timestamp(start)) & (dates <= pd.Timestamp(end))
    return df.loc[mask].copy()


# --------------------------------------------------------------------------- #
# Internals                                                                   #
# --------------------------------------------------------------------------- #


def _fetch_and_parse(*, name: str, url: str) -> tuple[pd.DataFrame, SourceRef]:
    raw, ref = fetch_bytes(name=name, url=url, suffix=".csv")
    df = pd.read_csv(
        io.BytesIO(raw),
        names=PPD_COLUMNS,
        header=None,
        encoding="latin-1",
        low_memory=False,
        on_bad_lines="skip",
    )
    return df, ref
