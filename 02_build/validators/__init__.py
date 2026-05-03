"""Public-data validators for the Amplified Partners insight catalogue.

Tests insights from `01_truth/schemas/research-index/00-insight-catalogue_v1.md`
against UK public datasets and emits one of:

- PROVEN     — public data quantitatively confirms the claim at the granularity
               required.
- PLAUSIBLE  — data is consistent with the claim but underpowered, or one leg
               of the recipe is open-data confirmable while the other requires
               client data with published research support.
- DISPROVEN  — public data contradicts the claim.
- BLOCKED    — required source is unreachable in this environment (e.g. needs
               an API key not yet provisioned). Recorded so the gap is visible.

Per AMP-67 / AMP-59. Vertical-agnostic by design so AMP-64/65/66/68 reuse the
same machinery.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from .core import EvidenceBundle, Verdict, VerdictBand, write_verdict

__all__ = ["EvidenceBundle", "Verdict", "VerdictBand", "write_verdict"]
