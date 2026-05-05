---
title: Retail vertical — public-data validators
date: 2026-05-03
version: 1
status: draft
ticket: AMP-66
parent_ticket: AMP-59
signed_by: "Devon-9a6b, 2026-05-03, devin-9a6bd256bd7c4a90a083a471fa94a810"
---

<!-- markdownlint-disable-file MD013 -->

# Retail vertical validators

Self-contained module that turns the 19 retail-vertical insights
(`INS-060` → `INS-078` in `01_truth/schemas/research-index/00-insight-catalogue_v1.md`)
into verdicts backed by real UK public data.

This package is **vertical-scoped** so it ships in isolation while the four
sibling tickets (AMP-64 trades, AMP-65 hospitality, AMP-67 prof-services,
AMP-68 universal) build their own equivalents in parallel. Once all five land,
the shared fetchers can be promoted to a common `02_build/validators/sources/`
location per the AMP-59 plan.

## Verdict scheme

Three bands, per ticket:

| Verdict      | Condition                                                                                               |
|--------------|----------------------------------------------------------------------------------------------------------|
| `PROVEN`     | Public data quantitatively confirms the claim at the granularity claimed (e.g. r ≥ 0.6 + p < 0.01, base-rate within stated range, distribution exceeds threshold by ≥ 1σ). |
| `PLAUSIBLE`  | Data is consistent with the claim but underpowered, OR one leg of the recipe is open-data-confirmable while the other requires client data, OR the insight is purely semantic and has published research support. |
| `DISPROVEN`  | Public data contradicts the claim (signal absent; correlation null; distribution does not show the claimed pattern). |

`INCONCLUSIVE` from validation methodology v2 folds into `PLAUSIBLE`;
`REFUTED` equals `DISPROVEN`.

## Test classes

Four reusable test classes live in `tests/`:

- `existence.py` — endpoint reachable + claimed granularity present (cheapest, runs first).
- `base_rate.py` — population proportion against a stated range, with binomial CI.
- `correlation.py` — Pearson + Spearman across two time series.
- `distribution.py` — quantile / threshold check.

Each returns `(verdict, evidence_bundle)` where `evidence_bundle` is a JSON-serialisable
dict with: source URL, date accessed, query params, response hash, summary stats, raw
sample. The bundle is written to `results/<INS-NNN>/`.

## Sources used

Implemented (no key required, no PII):

| Source                                | File                          | Used by                        |
|---------------------------------------|-------------------------------|--------------------------------|
| ONS Beta API (datasets, observations) | `fetchers/ons_beta.py`        | INS-062, 069, 071, 073, 074    |
| Nomis (labour market, ASHE)           | `fetchers/nomis.py`           | INS-065                        |
| Police.uk Crime Data API              | `fetchers/police_uk.py`       | INS-067, 072                   |
| Insolvency Service stats (GOV.UK)     | `fetchers/insolvency_stats.py`| INS-064, 070                   |
| HM Land Registry CCOD                 | `fetchers/land_registry.py`   | INS-063                        |

Stubbed (need a free key — request once, fetch on next run):

| Source                                | File                          | Used by                        |
|---------------------------------------|-------------------------------|--------------------------------|
| Companies House REST + Streaming      | `fetchers/companies_house.py` | INS-064, 070 (augmenting)      |
| Met Office DataPoint                  | `fetchers/met_office.py`      | INS-060                        |
| EPC register                          | `fetchers/epc.py`             | (retail-adjacent only)         |

Lazy-import (no system dependency):

| Source                                | File                          | Used by                        |
|---------------------------------------|-------------------------------|--------------------------------|
| Google Trends (`pytrends`)            | `fetchers/pytrends_local.py`  | INS-066, 074                   |

## Layout

```
02_build/validators/retail/
├── README.md                      # this file
├── cli.py                         # python -m validators.retail run [--ins INS-NNN ...]
├── fetchers/                      # one file per public source
├── tests/                         # base_rate / correlation / distribution / existence
├── insights/                      # one runner per INS-NNN that composes fetchers + tests
├── results/                       # verdict + evidence bundle per insight
└── cache/                         # raw API responses keyed by query hash
```

## Reproducibility

Every verdict file records:

- source URL
- access timestamp (UTC ISO-8601)
- query params
- SHA-256 of the raw response
- session id (`devin-9a6bd256bd7c4a90a083a471fa94a810`)
- code git SHA (filled at run time)

## How to run

```bash
# from repo root
PYTHONPATH=02_build python -m validators.retail.cli run               # all 19
PYTHONPATH=02_build python -m validators.retail.cli run --ins INS-067 # one
PYTHONPATH=02_build python -m validators.retail.cli list              # show insights + status
PYTHONPATH=02_build python -m validators.retail.cli summary           # rollup of last run
```

Network is required for live runs. Cached responses under `cache/` make
re-runs deterministic.

---

Signed,

**Devon-9a6b**
Devin session `9a6bd256bd7c4a90a083a471fa94a810`
2026-05-03
