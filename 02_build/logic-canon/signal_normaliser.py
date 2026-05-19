"""
Signal Normaliser — Convert Opinions into Proportional Allocations
===================================================================
WHEN TO USE: You have a bunch of scores/opinions/signals of varying
strength and you need to convert them into proportional allocations
of a fixed budget (money, time, attention, compute).

EXAMPLES:
- Budget: confidence scores per channel → pound amounts across channels
- Time: priority scores per task → hours allocated per task
- Compute: usage scores per feature → CPU/memory allocation
- Attention: urgency signals → notification priority ordering
- Content: quality scores → publishing cadence allocation

HOW IT WORKS:
1. Clean signals (remove NaN, inf, non-numeric)
2. Filter by minimum threshold (ignore noise)
3. Normalise: position = (signal / sum_of_all_signals) × total_budget
4. Cap: no single allocation > configured maximum
5. Floor: ignore allocations below minimum useful size

INPUTS:
- Dictionary of {item: signal_strength} (any scale)
- Total budget to allocate
- Config (max per item, threshold, minimum size)

OUTPUTS:
- Dictionary of {item: allocated_amount}

Provenance: Nexus V2 engines.py BaseEngine.signals_to_positions → generalised.
Devon-b3d8 | 2026-05-15
"""

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np


@dataclass
class NormaliserConfig:
    """Signal normalisation configuration."""

    max_allocation_pct: float = 0.10    # Max single allocation as % of budget
    signal_threshold: float = 0.0       # Ignore signals weaker than this
    min_allocation: float = 100.0       # Minimum useful allocation (in budget units)


def normalise(
    signals: Dict[str, float],
    total_budget: float,
    cfg: Optional[NormaliserConfig] = None,
) -> Dict[str, float]:
    """
    Convert signal strengths into proportional budget allocations.

    Args:
        signals: {item: signal_strength} — any numeric scale, pos or neg
        total_budget: total amount to distribute
        cfg: configuration (None = defaults)

    Returns:
        {item: allocated_amount} — proportional to signal strength,
        respecting caps and minimums

    Example:
        signals = {"linkedin": 0.8, "email": 0.5, "google": 0.3, "referral": 0.1}
        allocations = normalise(signals, total_budget=10000)
        # Returns: {"linkedin": 4706, "email": 2941, "google": 1765, "referral": 588}
    """
    if cfg is None:
        cfg = NormaliserConfig()

    if not signals or total_budget <= 0:
        return {}

    # 1. Clean signals — drop NaN, inf, non-numeric
    clean: Dict[str, float] = {}
    for item, signal in signals.items():
        if signal is None:
            continue
        try:
            s = float(signal)
        except (TypeError, ValueError):
            continue
        if not np.isfinite(s):
            continue
        clean[item] = s

    if not clean:
        return {}

    # 2. Filter by threshold
    filtered = {k: v for k, v in clean.items() if abs(v) >= cfg.signal_threshold}
    if not filtered:
        return {}

    # 3. Normalise by total signal mass
    signal_sum = sum(abs(s) for s in filtered.values()) or 1.0

    allocations = {}
    max_alloc = total_budget * cfg.max_allocation_pct

    for item, signal in filtered.items():
        # Scale by signal proportion
        raw = (signal / signal_sum) * total_budget

        # Cap
        capped = np.clip(raw, -max_alloc, max_alloc)

        # Floor
        if abs(capped) >= cfg.min_allocation:
            allocations[item] = round(float(capped), 2)

    return allocations
