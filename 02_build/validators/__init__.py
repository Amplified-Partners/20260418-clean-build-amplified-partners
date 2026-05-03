"""Public-data validators for the insight catalogue.

See ``README.md`` for the verdict scheme, layout, and run instructions.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
Ticket: AMP-65 (Hospitality vertical) implementing the AMP-59 plan.
"""

from .verdict import Verdict, VerdictBand

__all__ = ["Verdict", "VerdictBand"]
