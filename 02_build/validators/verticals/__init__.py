"""Per-vertical insight registries.

Each vertical module exposes a ``REGISTRY: dict[str, Validator]`` mapping
``INS-NNN`` to a callable that runs one or more probes / tests and returns a
``Verdict`` instance.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""
