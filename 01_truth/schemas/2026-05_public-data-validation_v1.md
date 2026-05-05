---
title: "Public-Data Validation v1"
id: "public-data-validation-v1"
version: 1
created: 2026-05-03
last_validated: 2026-05-03
type: document
topic_type: reference
status: candidate
signed_by: "Devon-ab74, 2026-05-03, devin-ab740f2c78ee477a9c16ea3b6ed15293; Devon-9a6b, 2026-05-03, devin-9a6bd256bd7c4a90a083a471fa94a810"
parent: AMP-59
ticket: AMP-67
sister_ticket: AMP-66
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

Two additional bands exist for situations the three bands above don't cover:

- **BLOCKED** — validation cannot be attempted in the current environment
  because a required credential isn't yet provisioned (e.g. the live
  Companies House REST API key). BLOCKED is not a verdict on the insight;
  it's a gap in our access layer that we surface so it gets fixed rather
  than hidden. Resolves to PROVEN/PLAUSIBLE/DISPROVEN once the credential
  lands.
- **DEFERRED** — validation **must not** be attempted from an automated
  session for policy reasons (ToS-bound scraping, legal review pending,
  PII risk). Distinct from BLOCKED: BLOCKED means "we'd run this if we
  could"; DEFERRED means "we're refusing to run this here at all". Used
  by AMP-66 INS-077 (competitor pricing scraping). Resolves to a verdict
  only after Ewan signs off on the legal/policy posture.

The `INCONCLUSIVE` band from `2026-03_validation-methodology_v2.md` folds
into `PLAUSIBLE`. `REFUTED` equals `DISPROVEN`. The five-band scheme is
deliberately coarser than the methodology v2 RAEI/PRS/AMPS rubrics — it
answers a different question (data presence) and runs cheaper.

## Four reusable test classes

Implemented in `02_build/validators/tests/` (shared) and in
`02_build/validators/retail/tests/` (AMP-66 self-contained variant
pending lift to the shared layer):

1. **existence** — does the source publish the data the recipe needs at the
   granularity claimed? Cheapest test, runs first.
2. **base_rate** — does a published headline figure match the catalogue's
   numeric claim within tolerance? (e.g. "20% WIP write-off rate", "average
   £748 recovered per £1,000 billed".)
3. **correlation** — do two series move together at the strength claimed?
   Pearson r with an n ≥ 8 power floor.
4. **distribution** — does the empirical distribution exceed the claimed
   threshold at the claimed share? (e.g. "60% of EPC band E or worse";
   `z_min = 1.0` standard-deviation floor by default).

A validator is free to compose multiple test classes in a single Verdict.
The four classes cover ~95% of the catalogue's recipes; new classes get
added when an insight needs one.

## How a verdict is recorded

Every verdict is a JSON object. Two storage conventions coexist while the
shared layer matures:

- **Shared (AMP-67 onward):** `03_shadow/validators/<vertical>/<INS-NNN>/verdict.json`.
- **Self-contained (AMP-66 retail):** `02_build/validators/retail/results/<INS-NNN>/verdict.json`.
  Will be lifted to the shared shadow tier when the retail validators
  promote to the shared `sources/` + `tests/` layer.

Required fields:

- `insight_id`, `vertical`, `band` / `verdict`, `test_class`, `method`, `finding`
- `statistic` — the numbers the verdict turns on
- `evidence` — list of `{source, url, accessed_at, content_sha256, summary}`
- `run_at` / `run_at_utc`, `signed_by`, `git_sha`, `session_id` — reproducibility metadata

Every fetcher routes through a hashing cache (`02_build/validators/cache.py`
shared; `02_build/validators/retail/fetchers/common.py` retail), which
sha256s the response body and caches it on disk. The sha256 is captured in
the evidence bundle so re-runs are reproducible even if the upstream source
changes. Secret-bearing query params (`key`, `api_key`, `token`,
`authorization`, etc.) are redacted before persistence and never derived
into cache filenames in clear text (CodeQL `py/clear-text-storage-sensitive-data`
clean — see `02_build/validators/retail/tests/test_redaction.py`).

A one-line summary is written to the catalogue:

```text
**VALIDATION (AMP-67):** PROVEN | existence | accessed 2026-05-03 | evidence: 03_shadow/validators/profservices/INS-079/verdict.json
**VALIDATION (AMP-66):** verdict=PROVEN | test=existence | conf=88 | run=2026-05-03 | signed_by=Devon-9a6b — <one-sentence summary>
```

The literature `STATUS:` line above it is unchanged.

## Promotion path

1. **03_shadow/validators/** (or vertical-self-contained `02_build/validators/<vertical>/results/`)
   — every verdict lands here first. Shadow tier means non-authoritative;
   promotion happens after human review (by the ticket reviewer or a
   follow-up `!validate` ticket).
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

## Reference implementations

- `02_build/validators/` — shared fetchers, test classes, CLI orchestrator
  (AMP-67).
- `02_build/validators/validations/profservices.py` — runners for the
  16 ProfServices entries (INS-079..INS-094) per AMP-67.
  `03_shadow/validators/profservices/rollup.json` — verdict summary.
- `02_build/validators/retail/` — self-contained retail validator package
  (AMP-66) for the 19 retail entries (INS-060..INS-078). Self-contained
  while the shared scaffold matures; will lift its fetchers and test
  classes to the shared layer.
  `01_truth/schemas/research-index/06a-vertical-retail-validation-rollup_v1.md`
  — verdict rollup table.
- AMP-64 / AMP-65 / AMP-68 use the same machinery for trades, hospitality,
  universal.

## Changelog

- 2026-05-03 — v1 (Devon-ab74, AMP-67) — initial schema. Three-band
  PROVEN/PLAUSIBLE/DISPROVEN scheme + BLOCKED gap-marker; four reusable
  test classes; shadow-tier storage with promotion path.
- 2026-05-03 — v1 merge (Devon-9a6b, AMP-66) — added DEFERRED policy band
  (distinct from BLOCKED: BLOCKED = waiting on creds, DEFERRED = refusing
  on ToS/legal grounds; first DEFERRED entry is INS-077 retail competitor
  scraping); added the AMP-66 retail self-contained reference
  implementation; documented the secret-redaction discipline (CodeQL
  `py/clear-text-storage-sensitive-data` clean) introduced by the AMP-66
  cache layer; documented the dual storage convention while the shared
  layer matures. No removal of AMP-67 content.
