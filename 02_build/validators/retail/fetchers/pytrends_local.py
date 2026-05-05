# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Google Trends via pytrends (lazy import).

Used for INS-066 (local search demand vs paid-ad efficiency) and INS-074
(category share-of-voice). pytrends is unofficial and rate-limited, so we
catch all exceptions and return a structured 'skipped' Fetched rather than
failing the verdict pipeline.

`pip install pytrends` to enable. If pytrends is not installed, calls return
_skipped with reason='pytrends not installed' and the runner downgrades.
"""
from __future__ import annotations

import time

from .common import Fetched


def is_available() -> bool:
    try:
        import pytrends  # noqa: F401
        return True
    except ImportError:
        return False


def interest_over_time(keywords: list[str], geo: str = "GB", timeframe: str = "today 12-m") -> Fetched:
    """Return a Fetched whose body is a list of {date, keyword: value} rows."""
    try:
        from pytrends.request import TrendReq
    except ImportError:
        return Fetched(
            source="pytrends",
            url="https://trends.google.com/trends/api",
            params={"keywords": keywords, "geo": geo, "timeframe": timeframe},
            body={"_skipped": True, "reason": "pytrends not installed"},
        )
    try:
        py = TrendReq(hl="en-GB", tz=0)
        py.build_payload(keywords, timeframe=timeframe, geo=geo)
        df = py.interest_over_time()
        if df.empty:
            return Fetched(
                source="pytrends",
                url="https://trends.google.com/trends/api",
                params={"keywords": keywords, "geo": geo, "timeframe": timeframe},
                body={"_skipped": True, "reason": "empty response (rate-limited or no data)"},
            )
        rows = []
        for ts, row in df.iterrows():
            r = {"date": ts.strftime("%Y-%m-%d")}
            for kw in keywords:
                r[kw] = int(row[kw])
            rows.append(r)
        accessed = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return Fetched(
            source="pytrends",
            url="https://trends.google.com/trends/api",
            params={"keywords": keywords, "geo": geo, "timeframe": timeframe},
            accessed_utc=accessed,
            status=200,
            body=rows,
        )
    except Exception as e:
        return Fetched(
            source="pytrends",
            url="https://trends.google.com/trends/api",
            params={"keywords": keywords, "geo": geo, "timeframe": timeframe},
            body={"_skipped": True, "reason": f"pytrends error: {e}"},
        )
