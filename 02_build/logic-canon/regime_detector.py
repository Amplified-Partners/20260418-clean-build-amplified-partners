"""
Regime Detector — Environmental Shift Detection & Response Scaling
===================================================================
WHEN TO USE: You need to detect when the operating environment has
fundamentally changed and automatically scale your system's exposure/
aggressiveness accordingly.

EXAMPLES:
- Business climate: confidence index drops → scale back marketing spend
- Cash flow: reserves drop below threshold → shift to survival mode
- Market volatility: VIX spike → reduce risk exposure
- Customer sentiment: NPS drops sharply → reduce outbound, increase support
- System health: error rate spikes → reduce load, increase monitoring

HOW IT WORKS:
1. Monitor a signal (VIX, cash reserves, NPS, error rate, etc.)
2. Classify into regimes: normal, caution, crisis
3. Apply a scaling factor to all system outputs based on regime
4. Optionally: require N consecutive readings to confirm regime change

INPUTS:
- Current signal value
- Historical signal values (for trend)
- Threshold configuration

OUTPUTS:
- Regime classification: 'normal', 'caution', 'crisis'
- Scale factor to apply to system outputs (0.0 to 1.0+)
- Trend direction

Provenance: Nexus V2 kaizen_l1_reweight.py regime detection + risk_manager.py
vol targeting → generalised.
Devon-b3d8 | 2026-05-15
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class RegimeConfig:
    """Regime detection configuration."""

    # Thresholds (signal values that trigger regime changes)
    # Interpret as: signal > caution_threshold = caution mode
    # For inverted signals (e.g., cash reserves), set invert=True
    caution_threshold: float = 25.0     # Signal above this = caution
    crisis_threshold: float = 37.5      # Signal above this = crisis (1.5× caution)

    # Whether higher signal = worse (True for VIX, error rates)
    # or lower signal = worse (True for cash reserves, NPS)
    invert: bool = False

    # Confirmation (avoid whiplash from single readings)
    confirmation_readings: int = 1      # How many consecutive readings to confirm

    # Scaling factors per regime
    normal_scale: float = 1.0           # Full activity
    caution_scale: float = 0.60         # Reduce to 60%
    crisis_scale: float = 0.20          # Reduce to 20%

    # Volatility-based scaling (optional)
    target_vol: float = 0.12            # Target annualised volatility
    vol_lookback: int = 21              # Window for vol calculation
    vol_scale_min: float = 0.50         # Minimum vol scalar
    vol_scale_max: float = 1.50         # Maximum vol scalar
    annualisation: int = 252


class RegimeDetector:
    """
    Stateful regime detector. Feed it signal readings and it tells you
    what regime you're in and how much to scale your activity.
    """

    def __init__(self, cfg: Optional[RegimeConfig] = None):
        self.cfg = cfg or RegimeConfig()
        self.signal_history: List[float] = []
        self.outcome_history: List[float] = []  # For vol-based scaling
        self.current_regime: str = "normal"
        self.regime_confirmed_count: int = 0

    def update(self, signal_value: float) -> Tuple[str, float]:
        """
        Feed a new signal reading. Returns (regime, scale_factor).

        Args:
            signal_value: Current reading of the monitored signal

        Returns:
            (regime, scale) where:
            - regime: 'normal', 'caution', or 'crisis'
            - scale: float to multiply all system outputs by
        """
        self.signal_history.append(signal_value)

        # Determine raw regime from signal
        raw_regime = self._classify(signal_value)

        # Confirm regime change (avoid whiplash)
        if raw_regime != self.current_regime:
            self.regime_confirmed_count += 1
            if self.regime_confirmed_count >= self.cfg.confirmation_readings:
                self.current_regime = raw_regime
                self.regime_confirmed_count = 0
        else:
            self.regime_confirmed_count = 0

        # Get scale factor
        scale = self._get_scale()

        return self.current_regime, scale

    def record_outcome(self, outcome: float):
        """Record a daily outcome for volatility-based scaling."""
        self.outcome_history.append(outcome)

    @property
    def vol_scale(self) -> float:
        """
        Volatility-based scaling factor.
        If realised vol > target, scale down. If below, scale up.
        """
        if len(self.outcome_history) < self.cfg.vol_lookback:
            return 1.0

        recent = self.outcome_history[-self.cfg.vol_lookback:]
        realised_vol = float(np.std(recent) * np.sqrt(self.cfg.annualisation))

        if realised_vol < 0.001:
            return 1.0

        scalar = self.cfg.target_vol / realised_vol
        return float(np.clip(scalar, self.cfg.vol_scale_min, self.cfg.vol_scale_max))

    def _classify(self, signal_value: float) -> str:
        """Classify signal into regime."""
        if self.cfg.invert:
            # Lower = worse (e.g., cash reserves, NPS)
            if signal_value < self.cfg.crisis_threshold:
                return "crisis"
            elif signal_value < self.cfg.caution_threshold:
                return "caution"
            return "normal"
        else:
            # Higher = worse (e.g., VIX, error rate)
            if signal_value > self.cfg.crisis_threshold:
                return "crisis"
            elif signal_value > self.cfg.caution_threshold:
                return "caution"
            return "normal"

    def _get_scale(self) -> float:
        """Get current scaling factor based on regime."""
        regime_scales = {
            "normal": self.cfg.normal_scale,
            "caution": self.cfg.caution_scale,
            "crisis": self.cfg.crisis_scale,
        }
        return regime_scales.get(self.current_regime, 1.0)
