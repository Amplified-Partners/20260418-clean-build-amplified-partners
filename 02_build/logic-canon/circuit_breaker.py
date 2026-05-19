"""
Circuit Breaker — Autonomous Damage Prevention
================================================
WHEN TO USE: You have an autonomous system that could cause compounding
damage if left unchecked. You need hard stops that trigger automatically
when things go wrong — before the damage becomes catastrophic.

EXAMPLES:
- Marketing budget: daily spend > £X → pause all campaigns 24h
- AI agent actions: > N irreversible actions today → pause for review
- Customer comms: > 5 messages to one customer/week → stop
- API usage: cost exceeding daily budget → halt
- Content publishing: quality score drops below threshold → hold queue

INPUTS:
- Stream of events (returns, costs, counts, scores)
- Threshold configuration

OUTPUTS:
- is_active: bool (True = system is frozen)
- freeze_until: datetime or None
- adjusted_values: dict (positions scaled or zeroed)

Provenance: Nexus V2 risk_manager.py (163 lines) → generalised.
Devon-b3d8 | 2026-05-15
"""

import datetime as dt
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class BreakerConfig:
    """Circuit breaker thresholds."""

    # Loss thresholds
    max_daily_loss: float = -0.03           # -3% daily → freeze
    max_cumulative_drawdown: float = -0.20  # -20% from peak → hard stop

    # Freeze durations (in cycles — days, hours, whatever your unit is)
    daily_freeze_cycles: int = 1            # 1 cycle freeze on daily breach
    drawdown_freeze_cycles: int = 5         # 5 cycle freeze on cumulative breach

    # Position/exposure limits
    max_single_exposure: float = 0.08       # No single item > 8% of total
    max_total_leverage: float = 1.20        # Max 120% total exposure

    # Volatility targeting
    target_vol: float = 0.12                # 12% annualised target volatility
    vol_lookback: int = 21                  # Days for vol calculation
    vol_scale_min: float = 0.50             # Minimum vol scalar
    vol_scale_max: float = 1.50             # Maximum vol scalar
    annualisation: int = 252                # √252 for daily → annual


class CircuitBreaker:
    """
    Stateful circuit breaker that monitors a stream of outcomes
    and freezes the system when thresholds are breached.
    """

    def __init__(self, cfg: Optional[BreakerConfig] = None):
        self.cfg = cfg or BreakerConfig()
        self.daily_outcomes: List[float] = []
        self.equity_curve: List[float] = [1.0]
        self.peak_equity: float = 1.0
        self.is_active: bool = False
        self.freeze_until: Optional[int] = None  # Cycle number when freeze lifts
        self.cycle_count: int = 0

    def record_outcome(self, daily_return: float):
        """Record one cycle's outcome. Call this every cycle."""
        self.daily_outcomes.append(daily_return)
        new_equity = self.equity_curve[-1] * (1 + daily_return)
        self.equity_curve.append(new_equity)
        self.peak_equity = max(self.peak_equity, new_equity)
        self.cycle_count += 1

    @property
    def current_drawdown(self) -> float:
        """Current drawdown from peak. Negative number."""
        if self.peak_equity <= 0:
            return 0.0
        return (self.equity_curve[-1] - self.peak_equity) / self.peak_equity

    @property
    def realised_vol(self) -> float:
        """Realised annualised volatility over lookback window."""
        if len(self.daily_outcomes) < self.cfg.vol_lookback:
            return 0.0
        recent = self.daily_outcomes[-self.cfg.vol_lookback:]
        return float(np.std(recent) * np.sqrt(self.cfg.annualisation))

    def check(self) -> Tuple[bool, str]:
        """
        Check if circuit breaker should trigger.

        Returns:
            (is_frozen, reason)
        """
        # Already frozen?
        if self.is_active:
            if self.freeze_until and self.cycle_count >= self.freeze_until:
                self.is_active = False
                self.freeze_until = None
                return False, "Circuit breaker released"
            return True, "Circuit breaker ACTIVE — all activity frozen"

        # Check daily loss
        if self.daily_outcomes:
            last = self.daily_outcomes[-1]
            if last < self.cfg.max_daily_loss:
                self.is_active = True
                self.freeze_until = self.cycle_count + self.cfg.daily_freeze_cycles
                return True, f"Daily loss {last:.2%} < {self.cfg.max_daily_loss:.2%}"

        # Check cumulative drawdown
        dd = self.current_drawdown
        if dd < self.cfg.max_cumulative_drawdown:
            self.is_active = True
            self.freeze_until = self.cycle_count + self.cfg.drawdown_freeze_cycles
            return True, f"Drawdown {dd:.2%} < {self.cfg.max_cumulative_drawdown:.2%}"

        return False, "OK"

    def check_exposures(
        self,
        proposed: Dict[str, float],
        total_budget: float,
    ) -> Dict[str, float]:
        """
        Validate and adjust proposed allocations against exposure limits.

        Args:
            proposed: {item: amount} — proposed allocation
            total_budget: total available budget

        Returns:
            Adjusted allocations (capped, scaled if needed)
        """
        # If frozen, return empty
        frozen, reason = self.check()
        if frozen:
            return {}

        adjusted = {}

        # 1. Cap single exposure
        max_single = total_budget * self.cfg.max_single_exposure
        for item, amount in proposed.items():
            if abs(amount) > max_single:
                amount = np.sign(amount) * max_single
            adjusted[item] = amount

        # 2. Cap total leverage
        gross = sum(abs(v) for v in adjusted.values())
        max_gross = total_budget * self.cfg.max_total_leverage
        if gross > max_gross:
            scale = max_gross / gross
            adjusted = {k: v * scale for k, v in adjusted.items()}

        # 3. Volatility targeting
        adjusted = self._vol_target(adjusted, total_budget)

        return adjusted

    def _vol_target(
        self,
        allocations: Dict[str, float],
        total_budget: float,
    ) -> Dict[str, float]:
        """Scale allocations to target volatility."""
        rv = self.realised_vol
        if rv < 0.001:
            return allocations

        # Vol scalar: if realised vol is above target, scale down
        scalar = self.cfg.target_vol / rv
        scalar = np.clip(scalar, self.cfg.vol_scale_min, self.cfg.vol_scale_max)

        if abs(scalar - 1.0) > 0.05:  # Only adjust if meaningful
            return {k: v * scalar for k, v in allocations.items()}

        return allocations
