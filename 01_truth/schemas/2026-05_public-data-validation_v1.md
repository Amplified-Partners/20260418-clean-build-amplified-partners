---
title: "Public-Data Validation v1"
id: "public-data-validation-v1"
version: 1
created: 2026-05-03
last_validated: 2026-05-03
type: document
topic_type: reference
status: candidate
signed_by: "Devon-ab74, 2026-05-03, devin-ab740f2c78ee477a9c16ea3b6ed15293"
parent: AMP-59
ticket: AMP-67
---

# Public-Data Validation v1

## What this is

The data-backed companion to the literature-class `STATUS:` field on every
catalogue entry in `01_truth/schemas/research-index/00-insight-catalogue_v1.md`.

Insights start their life HYPOTHESIS / CONFIRMED-EXTERNAL / PROVEN against
the academic literature. That tells us the *idea* survived peer review. It
does not tell us whether the *implementation* actually works on UK public
data — whether a Companies House query returns the right SIC code at the
right granularity, whether ONS Business Demography publishes births and
deaths on the cadence the recipe assumes, whether the Self Assessment
deadline is still 31 January.

The `VALIDATION:` field answers that second question. It is **additive** —
the literature `STATUS:` is preserved verbatim.

## Three bands

| Band | Meaning |
|------|---------|
| **PROVEN** | Public data quantitatively confirms the claim at the granularity the recipe needs. Reserved for fully-public-data recipes (e.g. HMRC tax calendar dates, ONS sector births/deaths, Gazette insolvency feed, EPC band distribution). |
| **PLAUSIBLE** | Either (a) the public leg of an A-B-C bridge validates and the client-side leg has published research support, (b) the recipe is internal-only and public data is not the right validator, or (c) the data is consistent with the claim but underpowered. |
| **DISPROVEN** | Public data contradicts the claim — the published figure is outside the claimed range, or a required source no longer publishes the breakdown. |

A fourth band, **BLOCKED**, is recorded when validation cannot be attempted
in the current environment because a required credential isn't yet
provisioned (e.g. the live Companies House REST API key). BLOCKED is not a
verdict on the insight; it's a gap in our access layer that we surface so it
gets fixed rather than hidden.

## Four reusable test classes

Implemented in `02_build/validators/tests/`:

1. **existence** — does the source publish the data the recipe needs at the
   granularity claimed? Cheapest test, runs first.
2. **base_rate** — does a published headline figure match the catalogue's
   numeric claim within tolerance? (e.g. "20% WIP write-off rate", "average
   £748 recovered per £1,000 billed".)
3. **correlation** — do two series move together at the strength claimed?
   Pearson r with an n ≥ 8 power floor.
4. **distribution** — does the empirical distribution exceed the claimed
   threshold at the claimed share? (e.g. "60% of EPC band E or worse".)

A validator is free to compose multiple test classes in a single Verdict.
The four classes cover ~95% of the catalogue's recipes; new classes get
added when an insight needs one.

## How a verdict is recorded

Every verdict is a JSON object at
`03_shadow/validators/<vertical>/<INS-NNN>/verdict.json`. Required fields:

- `insight_id`, `vertical`, `band`, `test_class`, `method`, `finding`
- `statistic` — the numbers the verdict turns on
- `evidence` — list of `{source, url, accessed_at, content_sha256, summary}`
- `run_at`, `signed_by` — reproducibility metadata

Every fetcher routes through `02_build/validators/cache.py`, which sha256s
the response body and caches it on disk. The sha256 is captured in the
evidence bundle so re-runs are reproducible even if the upstream source
changes.

A one-line summary is written to the catalogue:

```
**VALIDATION:** PROVEN | existence | accessed 2026-05-03 | evidence: 03_shadow/validators/profservices/INS-079/verdict.json
```

The literature `STATUS:` line above it is unchanged.

## Promotion path

1. **03_shadow/validators/** — every verdict lands here first. Shadow tier
   means non-authoritative; promotion happens after human review (by the
   ticket reviewer or a follow-up `!validate` ticket).
2. **01_truth/** — when a verdict has been reviewed and we want it to be
   authoritative truth, the relevant evidence summary moves into
   `01_truth/research/validations/` and the catalogue line is updated to
   point at the truth-tier file.

This is the same shadow-then-promote dance as everything else in
`02_build/` and is intentional — public-data verdicts can age out (a CSV
gets republished, a source moves) and we want the literature `STATUS:` to
remain stable while the validation can be re-run on a fresh fetch.

## Relation to existing methodology docs

- `2026-03_validation-methodology_v2.md` — defines the four-band literature
  validation taxonomy (PROVEN / PARTIALLY_SUPPORTED / REFUTED /
  INCONCLUSIVE). That methodology applies to the `STATUS:` field. This
  doc applies to the new `VALIDATION:` field.
- The two are deliberately decoupled. An insight can be CONFIRMED-EXTERNAL
  on literature and PLAUSIBLE on public data, or HYPOTHESIS on literature
  and PROVEN on public data. Both records are kept.

## Escalation

When public-data validation contradicts the literature claim
(STATUS=PROVEN but VALIDATION=DISPROVEN, or similar), the catalogue entry
is flagged and the conflict is logged to `00_authority/DECISION_LOG.md`
for Ewan's review. The literature is not silently overwritten by a fetch.

## Reference implementation

- `02_build/validators/` — fetchers, test classes, CLI orchestrator.
- `02_build/validators/validations/profservices.py` — runners for the
  16 ProfServices entries (INS-079..INS-094) per AMP-67.
- `03_shadow/validators/profservices/rollup.json` — verdict summary.
- AMP-64 / AMP-65 / AMP-66 / AMP-68 use the same machinery for trades,
  hospitality, retail, universal.

## Changelog

- 2026-05-03 — v1 — initial schema. Three-band PROVEN/PLAUSIBLE/DISPROVEN
  scheme + BLOCKED gap-marker; four reusable test classes; shadow-tier
  storage with promotion path. Devon-ab74.
