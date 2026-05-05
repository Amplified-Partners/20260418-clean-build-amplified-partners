# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Insight runners — one function per retail INS-NNN.

Each runner takes no args and returns a Verdict. The CLI iterates over
INSIGHTS in catalogue order. Adding a new runner is a matter of writing the
function + registering it here.
"""
from __future__ import annotations

from collections.abc import Callable

from ..verdict import Verdict
from .ins_060_footfall import run as ins_060
from .ins_061_stockout import run as ins_061
from .ins_062_price_elasticity import run as ins_062
from .ins_063_commercial_voids import run as ins_063
from .ins_064_competitor_death_spiral import run as ins_064
from .ins_065_ltv_postcode import run as ins_065
from .ins_066_google_trends import run as ins_066
from .ins_067_shrinkage_crime import run as ins_067
from .ins_068_marketplace_fees import run as ins_068
from .ins_069_category_cannibalisation import run as ins_069
from .ins_070_supplier_concentration import run as ins_070
from .ins_071_energy_cost import run as ins_071
from .ins_072_return_fraud import run as ins_072
from .ins_073_loyalty_roi import run as ins_073
from .ins_074_share_of_voice import run as ins_074
from .ins_075_review_text_drift import run as ins_075
from .ins_076_support_ticket_churn import run as ins_076
from .ins_077_product_description_match import run as ins_077
from .ins_078_chat_sentiment import run as ins_078

INSIGHTS: dict[str, Callable[[], Verdict]] = {
    "INS-060": ins_060,
    "INS-061": ins_061,
    "INS-062": ins_062,
    "INS-063": ins_063,
    "INS-064": ins_064,
    "INS-065": ins_065,
    "INS-066": ins_066,
    "INS-067": ins_067,
    "INS-068": ins_068,
    "INS-069": ins_069,
    "INS-070": ins_070,
    "INS-071": ins_071,
    "INS-072": ins_072,
    "INS-073": ins_073,
    "INS-074": ins_074,
    "INS-075": ins_075,
    "INS-076": ins_076,
    "INS-077": ins_077,
    "INS-078": ins_078,
}
