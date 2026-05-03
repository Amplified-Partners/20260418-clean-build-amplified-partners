# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""One module per insight in the trades vertical.

Each module exposes a ``run() -> Verdict`` callable. The CLI imports them and
sequences runs by vertical or by ID.
"""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module

from ..core import Verdict

# Trades pilot — public-data-driven where possible, auth-aware where needed.
TRADES_PILOT = [
    "INS-006",  # Land Registry transactions → new-mover refurbishment lead
    "INS-007",  # Planning applications → refurbishment leading indicator
    "INS-018",  # EPC boiler distribution → boiler upgrade demand
    "INS-022",  # VOA business rates → commercial prospecting universe
    "INS-001",  # Cold-snap weather → emergency call demand
    "INS-002",  # Supplier PPI → margin death-spiral
]


def runner_for(insight_id: str) -> Callable[[], Verdict]:
    """Return the ``run`` function for ``insight_id`` (e.g. ``INS-006``)."""
    module_name = "ins_" + insight_id.split("-")[1]
    mod = import_module(f"validators.insights.{module_name}")
    runner: Callable[[], Verdict] = mod.run
    return runner
