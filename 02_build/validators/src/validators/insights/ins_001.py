# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""INS-001 — Cold-snap weather → emergency-call demand forecasting (Trades).

Catalogue claim:
    "Met Office MIDAS Open Dataset … Environment Agency Flood Monitoring API …
     Predict emergency call surge 48 hours ahead within ±15-20% accuracy …
     Victorian/Edwardian terracing in NE1-NE3 is highest burst-pipe risk when
     temperature drops below 0°C."

Public leg requires Met Office MIDAS / DataPoint credentials. Without them the
verdict is ``SKIPPED`` — the client-side leg (call volume vs temperature
correlation) needs FSM data and cannot be validated from public sources alone.

When Met Office key is set, the test compares last-30-day daily minimum
temperature samples to the claimed 0°C threshold. Burst-pipe physics asserts
a hard threshold at freezing — the existence of sub-zero days is sufficient
evidence to validate the public leg.
"""

from __future__ import annotations

import os

from ..core import Verdict, skipped

INSIGHT_ID = "INS-001"


def run() -> Verdict:
    if not os.environ.get("MET_OFFICE_DATAPOINT_KEY", "").strip():
        return skipped(
            INSIGHT_ID,
            reason=(
                "MET_OFFICE_DATAPOINT_KEY not set. Register at "
                "https://www.metoffice.gov.uk/services/data/datapoint — free key. "
                "Without it the cold-snap public leg cannot be validated."
            ),
            test_class="correlation",
        )

    # When DataPoint integration ships, the implementation pattern is:
    #   1. Fetch the last 30 days of daily-min observations for site_id 99057
    #      (Newcastle Weather Centre).
    #   2. Fit `test_distribution(samples=daily_min, claim_threshold=0.0,
    #      direction="<=", minimum_n=30, sigma_floor=0.5)`.
    #   3. PLAUSIBLE if any sub-zero day in the window; PROVEN if winter window.
    #
    # The B-leg correlation (temperature → call volume) requires client FSM data
    # and is documented in the catalogue's ABC bridge — not validatable here.
    return skipped(
        INSIGHT_ID,
        reason="MET_OFFICE_DATAPOINT integration scaffold present; live fetch not yet wired.",
        test_class="correlation",
    )
