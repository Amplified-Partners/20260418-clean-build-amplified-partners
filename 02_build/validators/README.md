# `02_build/validators/`

Public-data validators for the insight catalogue.

Status: candidate authority — see `01_truth/schemas/2026-05_public-data-validation_v1.md` for the verdict scheme and evidence requirements.

## What this is

Code that turns the 136 hypothesis entries in `01_truth/schemas/research-index/00-insight-catalogue_v1.md` into data-backed verdicts. One per insight. Three bands: `PROVEN | PLAUSIBLE | DISPROVEN`.

Open-data only. No client data ever. No API keys committed.

## Quick start

```bash
cd 02_build/validators
python -m pip install -r requirements.txt
python -m validators run --vertical trades
python -m validators run --insight INS-006
python -m validators report --vertical trades
```

`run` writes verdicts to `02_build/validators/results/<INS-NNN>.json` and evidence bundles to `03_shadow/validators/<INS-NNN>/`.

`report` aggregates verdicts into a markdown summary.

## Sources

| Source | Auth | Status |
|--------|------|--------|
| HM Land Registry — Price Paid Data | none | implemented (INS-006) |
| Planning.data.gov.uk | none | implemented (INS-007) |
| VOA Business Rates Rateable Values | none | implemented (INS-022, existence check only) |
| ONS Beta API | none | scaffolded (generic fetcher in `sources/ons.py`, not yet wired to an insight) |
| Bank of England IADB (PPI) | none | scaffolded (INS-002 wires this; full CSV emit needs the gov.uk session round-trip not yet implemented) |
| Insolvency Service Statistics | none | not yet wired |
| DLUHC Live Tables (housing supply) | none | not yet wired |
| Companies House REST API | API key | scaffolded — set `COMPANIES_HOUSE_API_KEY` (used by INS-022 leg B) |
| EPC Domestic Register | API key | scaffolded — set `EPC_API_KEY` (INS-018 SKIPPED without it) |
| Met Office DataPoint | API key | not yet wired (INS-001 SKIPPED pending key + fetcher) |
| MIDAS Open / CEDA | login | not yet wired |

If an auth-required source is missing its key, the relevant insight's verdict is `SKIPPED` with `reason: AUTH_REQUIRED`. Other insights in the run continue.

## Layout

```
validators/
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/validators/
│   ├── __init__.py
│   ├── cli.py              # orchestrator
│   ├── core.py             # Verdict / Evidence / cache / catalogue helpers
│   ├── sources/            # one fetcher per source
│   ├── tests/              # four reusable test classes
│   └── insights/           # one module per insight (wires source + test → verdict)
└── results/                # generated verdict JSON
```

Caches live in `03_shadow/validators/cache/` keyed by query hash. Treat the cache as the canonical evidence store — never delete without a re-run.

## Re-validation cadence

Verdicts expire on the source's refresh cycle:

- Companies House — quarterly (a stale verdict is rerun after 90 days).
- Land Registry Price Paid — monthly.
- ONS Business Demography — annual.
- BoE PPI — monthly.
- DLUHC live tables — quarterly.

A scheduled Devon session re-runs verdicts approaching expiry.

## Conventions

- Every verdict file is signed (per `00_authority/SIGNATURES.md`).
- Every test records `code_sha`, `accessed_at`, and `response_hash` for reproducibility.
- Failures (network, schema drift, rate limit) produce a `SKIPPED` or source-absent verdict, never a silent false positive or false negative. Inside multi-source insights, individual fetch failures are caught so the surviving sources can still contribute, but the verdict notes which leg failed.
- The cache is content-addressed; identical query params produce identical cache keys.

---

Signed-by: Devon-6264, 2026-05-03, devin-6264b0ba42c6453b86b166bebc3d868a
