# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Bank of England Statistical Database (IADB) — no authentication.

Parameterised URL fetch. Returns a long-format DataFrame keyed on series code.

Documented at https://www.bankofengland.co.uk/boeapps/database/

Notable series for the trades vertical:
    CFMHSDE — Bank Rate (used as cost-of-living pressure proxy in INS-013).
    CFMHSDE history goes back decades.

ONS publishes the construction-materials Producer Price Indices; BoE is the
right source for headline rate/yield series. The two are paired in INS-002.
"""

from __future__ import annotations

import io

import pandas as pd

from ..core import SourceRef
from ._http import fetch_bytes

BOE_IADB_URL = "https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp"


def fetch_series(
    *,
    series_codes: list[str],
    date_from: str,
    date_to: str,
) -> tuple[pd.DataFrame, SourceRef]:
    """Fetch one or more series codes between ``date_from`` and ``date_to`` (DD/Mmm/YYYY).

    Returns a DataFrame indexed by date with one column per series code.
    """
    if len(series_codes) > 300:
        raise ValueError("BoE IADB allows at most 300 series codes per request")
    fd, fm, fy = _split_date(date_from)
    td, tm, ty = _split_date(date_to)
    params = {
        "Travel": "NIxAZxSUx",
        "FromSeries": "1",
        "ToSeries": "50",
        "DAT": "RNG",
        "FD": fd,
        "FM": fm,
        "FY": fy,
        "TD": td,
        "TM": tm,
        "TY": ty,
        "FNY": "Y",
        "CSVF": "TT",
        "html.x": "66",
        "html.y": "26",
        "SeriesCodes": ",".join(series_codes),
        "UsingCodes": "Y",
        "Filter": "N",
        "title": "AmplifiedPartnersValidators",
        "VPD": "Y",
    }
    raw, ref = fetch_bytes(name="boe_iadb", url=BOE_IADB_URL, params=params, suffix=".csv")
    df = pd.read_csv(io.BytesIO(raw))
    if "DATE" in df.columns:
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce", dayfirst=True)
        df = df.set_index("DATE")
    return df, ref


def _split_date(iso_or_dmy: str) -> tuple[str, str, str]:
    """Accept ``2024-04-30`` or ``30/Apr/2024`` and return ``(DD, Mmm, YYYY)``."""
    if "-" in iso_or_dmy:
        ts = pd.Timestamp(iso_or_dmy)
    else:
        ts = pd.to_datetime(iso_or_dmy, dayfirst=True)
    return f"{ts.day}", ts.strftime("%b"), f"{ts.year}"
