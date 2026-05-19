"""
Shadow Tester — Risk-Free A/B Testing for Autonomous Systems
=============================================================
WHEN TO USE: You want to test N variants of a strategy/approach in
parallel with the live system, without any real-world risk, and only
promote a variant when it's statistically proven better.

EXAMPLES:
- Email subject lines: run 10 variants in shadow, promote winner after 30 days
- Agent prompt configurations: test in parallel, promote when Sharpe beats live
- Pricing tiers: simulate 10 pricing structures, promote when proven
- Content strategies: shadow-test cadence/topic variants before switching

INPUTS:
- Base parameters (current live configuration)
- Daily outcomes for each variant (simulated)
- Live system performance (to compare against)

OUTPUTS:
- Updated variant stats (Sharpe, return, drawdown)
- Promotion candidates (statistically better than live)
- Recommended promotion (best variant, if any qualifies)

Provenance: Nexus V2 kaizen_l2_shadow.py (359 lines) → generalised.
Devon-b3d8 | 2026-05-15
"""

import copy
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class ShadowConfig:
    """Shadow testing configuration."""

    # Variant generation
    num_variants: int = 10              # How many variants to test simultaneously
    param_range: float = 0.20           # Vary parameters ±20% from live

    # Promotion criteria (ALL must be met)
    min_days: int = 30                  # Minimum days before promotion eligible
    sharpe_beat_threshold: float = 0.30 # Must beat live Sharpe by this much
    return_beat_threshold: float = 0.03 # Must beat live annualised return by 3%
    max_drawdown_gate: float = -0.15    # Reject if max DD exceeds 15%

    # Cleanup
    max_age_days: int = 90              # Remove variants older than this

    # Annualisation
    annualisation: int = 252


@dataclass
class Variant:
    """A shadow variant being tested."""
    variant_id: str
    parameters: dict
    description: str
    daily_outcomes: List[float] = field(default_factory=list)
    cumulative_return: float = 0.0
    sharpe: float = 0.0
    max_dd: float = 0.0
    days_active: int = 0
    promoted: bool = False


def generate_variants(
    base_params: dict,
    cfg: Optional[ShadowConfig] = None,
    prefix: str = "v",
) -> List[Variant]:
    """
    Generate N parameter variants by perturbing numeric values.

    Each numeric parameter is randomly scaled within ±param_range.
    Non-numeric parameters are kept unchanged.
    """
    if cfg is None:
        cfg = ShadowConfig()

    variants = []
    for i in range(cfg.num_variants):
        variant_params = {}
        mutations = []

        for key, value in base_params.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                perturbation = random.uniform(
                    1 - cfg.param_range,
                    1 + cfg.param_range,
                )
                new_value = value * perturbation

                if isinstance(value, int):
                    new_value = max(1, int(round(new_value)))
                else:
                    new_value = round(new_value, 6)

                variant_params[key] = new_value
                if new_value != value:
                    mutations.append(f"{key}: {value} → {new_value}")
            else:
                variant_params[key] = value

        variant = Variant(
            variant_id=f"{prefix}_{i}",
            parameters=variant_params,
            description="; ".join(mutations[:3]) if mutations else "no changes",
        )
        variants.append(variant)

    return variants


def update_variant(variant: Variant, daily_outcome: float, annualisation: int = 252):
    """
    Record one day's outcome for a variant and update its statistics.
    Call this every cycle with the simulated result.
    """
    variant.daily_outcomes.append(daily_outcome)
    variant.days_active = len(variant.daily_outcomes)

    # Cumulative return
    variant.cumulative_return = float(
        np.prod([1 + r for r in variant.daily_outcomes]) - 1
    )

    # Sharpe (need at least 20 days)
    if len(variant.daily_outcomes) >= 20:
        mean_r = np.mean(variant.daily_outcomes)
        std_r = np.std(variant.daily_outcomes) or 1e-8
        variant.sharpe = float((mean_r / std_r) * np.sqrt(annualisation))

    # Max drawdown
    if len(variant.daily_outcomes) >= 2:
        equity = np.cumprod([1 + r for r in variant.daily_outcomes])
        peak = np.maximum.accumulate(equity)
        dd = (equity - peak) / (peak + 1e-8)
        variant.max_dd = float(np.min(dd))


def check_promotions(
    variants: List[Variant],
    live_sharpe: float,
    live_return: float,
    cfg: Optional[ShadowConfig] = None,
) -> List[Variant]:
    """
    Check which variants qualify for promotion to live.

    Promotion criteria (ALL must be met):
    1. Minimum days of shadow testing
    2. Sharpe ratio beats live by threshold
    3. Annualised return beats live by threshold
    4. Max drawdown within acceptable limit

    Returns promotable variants sorted by Sharpe (best first).
    """
    if cfg is None:
        cfg = ShadowConfig()

    promotable = []

    for variant in variants:
        if variant.promoted or variant.days_active < cfg.min_days:
            continue

        sharpe_beat = variant.sharpe - live_sharpe

        # Annualise the return difference
        return_beat = variant.cumulative_return - live_return
        if variant.days_active > 0:
            ann_return_beat = return_beat * (cfg.annualisation / variant.days_active)
        else:
            ann_return_beat = 0.0

        # Drawdown gate
        if variant.max_dd < cfg.max_drawdown_gate:
            continue

        # Must beat on both Sharpe AND return
        if (sharpe_beat >= cfg.sharpe_beat_threshold and
                ann_return_beat >= cfg.return_beat_threshold):
            promotable.append(variant)

    promotable.sort(key=lambda v: v.sharpe, reverse=True)
    return promotable
