"""Reusable statistical test classes.

Each test class implements a small functional API:

    run(*args, **kwargs) -> tuple[VerdictBand, str, dict, list[EvidenceItem]]

Returning band, rationale, metrics, evidence list — sufficient for the CLI
orchestrator to write a Verdict bundle.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""
