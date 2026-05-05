# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Police.uk Crime Data API.

Free, no key required. Used for INS-067 (shoplifting) and INS-072 (postcode crime).
Docs: https://data.police.uk/docs/
"""
from __future__ import annotations

from .common import fetch_json, Fetched

BASE = "https://data.police.uk/api"


def crimes_at_location(
    category: str,
    lat: float,
    lng: float,
    date: str | None = None,
) -> Fetched:
    """Crimes within a 1-mile radius of (lat,lng) for the given YYYY-MM date.

    category: 'shoplifting' | 'all-crime' | 'burglary' | etc.
    date: YYYY-MM (defaults to latest available).
    Returns up to ~10,000 crimes per call; 1-mile radius is API default.
    """
    url = f"{BASE}/crimes-street/{category}"
    params: dict = {"lat": lat, "lng": lng}
    if date:
        params["date"] = date
    return fetch_json("police_uk", url, params=params)


def availability() -> Fetched:
    """List of (date, force) pairs available — used to pick a recent month."""
    return fetch_json("police_uk", f"{BASE}/crimes-street-dates")


# Curated retail-postcode anchor points (centroid lat/lng).
# Keep this short and named so verdicts are reproducible by humans.
#
# Coverage caveat: the Police.uk API only covers the 43 territorial police
# forces in **England and Wales**. Police Scotland (covering Glasgow and
# Edinburgh) is a separate organisation that does not currently publish to
# data.police.uk; queries against Scottish coordinates always return `[]`,
# which silently corrupts distribution tests by injecting spurious zeros.
# `RETAIL_AREAS` is kept as the canonical master list (useful for non-
# Police.uk sources later — e.g. Office for National Statistics population/
# crime aggregates, or a future Police Scotland CSV ingest); Police.uk-
# specific tests must use `RETAIL_AREAS_POLICE_UK` (England + Wales only).
RETAIL_AREAS = {
    # Newcastle — Jesmond Plumbing canonical postcodes (NE1-NE3) + Eldon Square retail core
    "NE1_eldon_square": (54.9744, -1.6131),
    "NE2_jesmond_acorn_rd": (54.9929, -1.6092),
    "NE3_gosforth_high_st": (55.0083, -1.6233),
    # Major retail high streets across UK regions (cross-vertical signal)
    "M3_manchester_arndale": (53.4838, -2.2381),
    "B5_birmingham_bullring": (52.4775, -1.8941),
    "L1_liverpool_one": (53.4030, -2.9870),
    "G1_glasgow_buchanan_st": (55.8617, -4.2530),         # Scotland — out of Police.uk coverage
    "BS1_bristol_cabot_circus": (51.4576, -2.5867),
    "LS1_leeds_briggate": (53.7975, -1.5430),
    "EH1_edinburgh_princes_st": (55.9525, -3.1880),       # Scotland — out of Police.uk coverage
    "W1_oxford_st_london": (51.5147, -0.1426),
    "SE1_borough_market_london": (51.5055, -0.0905),
}

# England + Wales subset — anchors that fall within Police.uk territorial-force
# coverage. Use this for any distribution / variance / spike-detection test
# against the Police.uk API. Excludes Scottish anchors (Glasgow, Edinburgh)
# which always return [] and would otherwise inject spurious zeros into the
# distribution.
RETAIL_AREAS_POLICE_UK = {
    name: coords
    for name, coords in RETAIL_AREAS.items()
    if name not in {"G1_glasgow_buchanan_st", "EH1_edinburgh_princes_st"}
}
