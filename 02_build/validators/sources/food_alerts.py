"""FSA Food Alerts (allergen / withdrawal) — open RSS.

Docs: https://www.food.gov.uk/news-alerts/list/alerts
RSS: https://www.food.gov.uk/news-alerts/rss/alerts

Used by:
- INS-041 (Allergen Risk Scoring — FSA Food Allergy alert system)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient

ALERTS_RSS = "https://www.food.gov.uk/news-alerts/rss/alerts"
ALERTS_HTML = "https://www.food.gov.uk/news-alerts/list/alerts"


def fetch_alerts_rss(client: HttpClient) -> CachedResponse:
    return client.get(ALERTS_RSS)


def fetch_alerts_landing(client: HttpClient) -> CachedResponse:
    return client.get(ALERTS_HTML)
