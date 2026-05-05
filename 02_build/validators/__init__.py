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
               Resolves to PROVEN/PLAUSIBLE/DISPROVEN once the credential lands.
- DEFERRED   — validation must NOT be attempted from an automated session for
               policy reasons (ToS-bound scraping, legal review pending, PII
               risk). Distinct from BLOCKED: BLOCKED = "we'd run if we could";
               DEFERRED = "we refuse to run on policy grounds". Resolves to a
               verdict only after Ewan signs off on the legal posture.

Per AMP-67 / AMP-59. Vertical-agnostic by design so AMP-64/65/66/68 reuse the
same machinery.

Vertical sub-packages (each self-contained until the shared layer matures):
  retail      AMP-66  (this PR — `validators/retail/`)
  prof_svcs   AMP-67  (`validators/validations/profservices.py`, shared scaffold)
  trades      AMP-64  (sibling)
  hospitality AMP-65  (sibling)
  universal   AMP-68  (sibling)

Once all five land, the AMP-66 retail self-contained subpackage will lift its
fetchers + test classes into the shared `sources/` + `tests/` layer to match
the AMP-67 convention.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
Signed-by: Devon-9a6b | 2026-05-03 | devin-9a6bd256bd7c4a90a083a471fa94a810 (merge)
"""

from .core import EvidenceBundle, Verdict, VerdictBand, write_verdict

__all__ = ["EvidenceBundle", "Verdict", "VerdictBand", "write_verdict"]
