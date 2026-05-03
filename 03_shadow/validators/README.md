# `03_shadow/validators/` — Public-data verdict bundles (shadow-tier)

Every verdict produced by `02_build/validators/` lands here first. Shadow
tier means **non-authoritative**: the catalogue's literature `STATUS:`
field is the binding statement; the `VALIDATION:` field is data-backed
context that gets re-run as sources update.

## Structure

```
03_shadow/validators/
  <vertical>/
    <INS-NNN>/
      verdict.json          Verdict object — see schema below
    rollup.json             Compact array of {insight, band, test} per run
```

## Verdict schema

Each `verdict.json` is the JSON serialisation of
`02_build/validators/core.py::Verdict`:

```jsonc
{
  "insight_id": "INS-079",
  "vertical": "profservices",
  "band": "PROVEN",                  // PROVEN | PLAUSIBLE | DISPROVEN | BLOCKED
  "test_class": "existence",         // existence | base_rate | correlation | distribution
  "method": "Plain-language description of what the test does",
  "finding": "Plain-language one-line result",
  "statistic": { ... },              // numbers the verdict turns on
  "evidence": [
    {
      "source": "ONS Business Demography",
      "url": "https://www.ons.gov.uk/...",
      "accessed_at": "2026-05-03T20:33:00Z",
      "content_sha256": "<sha>",
      "summary": "Reference-page reachable",
      "raw_path": "/home/.cache/amp-validators/<sha>.bin"
    }
  ],
  "notes": [],
  "run_at": "2026-05-03T20:33:00Z",
  "signed_by": "Devon-ab74 | 2026-05-03 | devin-..."
}
```

## Promotion

When a verdict has been reviewed and the team wants it to be
**authoritative truth**, the evidence summary is moved into
`01_truth/research/validations/` and the catalogue's `VALIDATION:` line
re-points at the truth-tier path. Until then: shadow only.

## Re-running

Verdicts age out as sources update. Re-run a vertical with:

```bash
python3 -m validators --repo-root /path/to/clean-build run --vertical profservices
```

The HTTP cache at `~/.cache/amp-validators/` is keyed by SHA256 of the
canonical URL+params, and respects a one-week TTL by default — pass
`--cache-ttl 0` (when implemented) or delete the cache directory to force
a fresh fetch.

Signed-by: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293
