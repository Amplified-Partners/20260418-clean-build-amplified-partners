"""
Correlation Monitor — Redundancy Detection Between Channels
=============================================================
WHEN TO USE: You have N channels/features/agents that you believe are
independent, and you want to detect when two of them are actually doing
the same thing (wasting resources on duplication).

EXAMPLES:
- Marketing channels: are LinkedIn and email attracting the same people?
- Intelligence features: are two CRM features producing the same insights?
- Content topics: are you publishing the same message in different words?
- Team members: are two people doing overlapping work?
- Products: are two offerings cannibalising each other?

HOW IT WORKS:
1. Collect outcome streams from each channel (daily returns, engagement, etc.)
2. Calculate pairwise Pearson correlation over a rolling window
3. Flag pairs where |correlation| > threshold (default 0.70)
4. Recommend: reduce combined weight or cut one

INPUTS:
- Dictionary of {channel_name: list_of_outcomes}
- Minimum history required
- Correlation warning threshold

OUTPUTS:
- Full correlation matrix
- Warning pairs (above threshold)

Provenance: Nexus V2 kaizen_l1_reweight.py check_correlations → generalised.
Devon-b3d8 | 2026-05-15
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


@dataclass
class CorrelationConfig:
    """Correlation monitoring configuration."""

    window: int = 60                    # Rolling window (cycles) for correlation
    min_history: int = 60               # Minimum data points required
    warning_threshold: float = 0.70     # |corr| above this = redundancy warning
    critical_threshold: float = 0.90    # |corr| above this = strong redundancy


def check_correlations(
    channel_outcomes: Dict[str, List[float]],
    cfg: Optional[CorrelationConfig] = None,
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Check pairwise correlations between channels.

    Args:
        channel_outcomes: {channel_name: [outcome_1, outcome_2, ...]}
        cfg: Configuration (None = defaults)

    Returns:
        (correlation_matrix, warnings) where:
        - correlation_matrix: full NxN correlation DataFrame
        - warnings: {pair_name: correlation} for pairs above threshold

    Example:
        outcomes = {
            "linkedin": [0.02, 0.01, -0.01, 0.03, ...],  # daily engagement
            "email": [0.01, 0.02, -0.02, 0.04, ...],
            "google_ads": [0.05, -0.01, 0.02, 0.01, ...],
        }
        corr_matrix, warnings = check_correlations(outcomes)
        # warnings might be: {"linkedin_vs_email": 0.85}
    """
    if cfg is None:
        cfg = CorrelationConfig()

    # Filter to channels with enough history
    valid = {
        name: outcomes[-cfg.window:]
        for name, outcomes in channel_outcomes.items()
        if len(outcomes) >= cfg.min_history
    }

    if len(valid) < 2:
        return pd.DataFrame(), {}

    df = pd.DataFrame(valid)
    corr = df.corr()

    # Find warning pairs
    warnings = {}
    names = list(valid.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            c = corr.iloc[i, j]
            if np.isfinite(c) and abs(c) > cfg.warning_threshold:
                pair = f"{names[i]}_vs_{names[j]}"
                warnings[pair] = round(float(c), 3)

    return corr, warnings


def find_redundant_pairs(
    channel_outcomes: Dict[str, List[float]],
    cfg: Optional[CorrelationConfig] = None,
) -> List[Tuple[str, str, float]]:
    """
    Convenience function: returns list of (channel_a, channel_b, correlation)
    for all pairs above the warning threshold, sorted by correlation strength.
    """
    if cfg is None:
        cfg = CorrelationConfig()

    _, warnings = check_correlations(channel_outcomes, cfg)

    pairs = []
    for pair_name, corr_val in warnings.items():
        parts = pair_name.split("_vs_")
        if len(parts) == 2:
            pairs.append((parts[0], parts[1], corr_val))

    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    return pairs
