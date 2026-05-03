"""Allow ``python -m validators run ...`` from the package root.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from .cli import main

raise SystemExit(main())
