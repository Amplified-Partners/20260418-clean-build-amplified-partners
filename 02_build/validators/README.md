# `02_build/validators/` — Public-data validation framework

Reference implementation of the schema at
`01_truth/schemas/2026-05_public-data-validation_v1.md`.

## What this does

For every insight in the catalogue, ask: **does the public UK data the
recipe assumes actually exist, at the granularity the recipe needs, today?**

The literature `STATUS:` field already tells us whether the *idea* survived
peer review. This package adds a `VALIDATION:` field that tells us whether
the *implementation* actually works on Companies House / ONS / HMRC / the
Gazette / gov.uk today.

## Usage

```bash
# Run every ProfServices runner (INS-079..INS-094)
python3 -m validators run --vertical profservices

# Run a subset
python3 -m validators run --vertical profservices --insight INS-079 --insight INS-093

# Print the rollup of the most-recent run
python3 -m validators rollup --vertical profservices

# Run from any cwd by passing the repo root
python3 -m validators --repo-root /path/to/clean-build run --vertical profservices
```

Verdicts land in `03_shadow/validators/<vertical>/<INS-NNN>/verdict.json`
plus a per-vertical `rollup.json`. Shadow-tier means non-authoritative;
they get reviewed and promoted into `01_truth/` after a human review pass.

## Layout

```
validators/
  cache.py            HTTP fetcher with on-disk SHA256 cache (stdlib-only)
  cli.py              `python3 -m validators ...` entrypoint
  core.py             Verdict / EvidenceBundle / VerdictBand types
  sources/            Per-publisher fetchers
    companies_house.py  Bulk index + accounts ZIPs (live API blocked w/o key)
    gazette.py          Insolvency notices JSON API
    gov_uk.py           Generic gov.uk pages (FCA, ICO, Law Society, ET, etc.)
    hmrc.py             HMRC deadlines + statistics collections
    ons.py              ONS / Nomis SDMX-JSON + statistical releases
  tests/              Reusable test classes
    base_rate.py        "Headline figure within claim range?"
    correlation.py      "Two series correlate at threshold r?"
    distribution.py     "Empirical share above threshold matches claim?"
    existence.py        "Does the source publish what the recipe needs?"
  validations/        Per-vertical runners
    profservices.py     16 ProfServices runners (INS-079..INS-094)
  test_validators.py  Stdlib-only self-tests (offline)
```

## Design choices

- **Stdlib only.** No requests / scipy / pandas. Validates on any clean
  Python 3.10+ box, including Beast cron and CI runners with no extras.
- **Reproducible by SHA256.** Every fetch is sha256'd and cached. The
  evidence bundle records the hash so re-runs are cheap and auditable.
- **Three-band scheme + BLOCKED gap-marker** — see the schema doc for
  semantics. PROVEN is reserved for fully-public-data recipes. PLAUSIBLE
  covers ABC bridges where the public leg validates and the client-side
  leg has published research support.
- **Vertical-agnostic.** ProfServices is the pilot. AMP-64 (Trades),
  AMP-65 (Hospitality), AMP-66 (Retail), AMP-68 (Universal/Semantic) reuse
  the same machinery — add a `validators/validations/<vertical>.py` module
  with a `RUNNERS: dict[str, Callable[[], Verdict]]`.
- **No live HTTP in self-tests.** `test_validators.py` is hermetic — it
  exercises the verdict types, the four test classes, the cache key
  derivation, and runner registration. Live-HTTP integration tests run on
  Beast on a schedule, not in CI.
- **Browser-shaped User-Agent.** Some publishers (Law Society, SRA) front
  their public docs with WAFs that 403 anything containing "amp" or
  "validator" in the UA. Provenance is recorded in every Verdict's
  `signed_by` field instead.

## Tickets

- AMP-67 (this PR) — ProfServices vertical pilot.
- AMP-64 / AMP-65 / AMP-66 — Trades / Hospitality / Retail (reuse).
- AMP-68 — Universal/Semantic (reuse).
- Parent: AMP-59 — vertical-validation programme.

Signed-by: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293
