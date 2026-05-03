---
title: "Public-Data Validation — Three-Band Verdict Scheme"
id: "public-data-validation"
version: 1
created: 2026-05-03
last_validated: 2026-05-03
type: document
topic_type: schema
status: draft
signed_by: "Devon-6264, 2026-05-03, devin-6264b0ba42c6453b86b166bebc3d868a"
---

<!-- markdownlint-disable-file MD013 -->

# Public-Data Validation — Three-Band Verdict Scheme

## Why this exists

The 136 entries in `00-insight-catalogue_v1.md` are **literature-backed** (`STATUS: CONFIRMED-EXTERNAL | HYPOTHESIS | PROVEN`). That column reflects published research, not data the system has actually queried.

This document defines the parallel **`VALIDATION:`** field — the verdict that comes from running real public-data tests against each insight.

The two fields coexist:

- `STATUS:` — literature class, set at catalogue authoring time, never overwritten.
- `VALIDATION:` — data-backed verdict, written by `02_build/validators/`, dated, with evidence pointer.

## The three bands

| Band | Meaning | Bar |
|------|---------|-----|
| `PROVEN` | Public data quantitatively confirms the claim at the granularity needed. | Effect size + significance threshold per test class (see below). Recipe is fully testable without client data. |
| `PLAUSIBLE` | Public data is consistent with the claim but the test is **underpowered** OR one leg of an ABC bridge requires client data while the public leg validates and the client-side claim has published research support. | Either: stat test points the right way but n too low / p too high; or public-leg test passes and client-leg has prior literature support in catalogue `FRAMEWORK LINEAGE`. |
| `DISPROVEN` | Public data **contradicts** the claim (signal absent, correlation null at adequate n, distribution rejects claim by ≥1σ). | Significance threshold met in the wrong direction, or data definitively absent at claimed granularity. |

The four-band methodology in `2026-03_validation-methodology_v2.md` (PROVEN / PARTIALLY_SUPPORTED / REFUTED / INCONCLUSIVE) maps cleanly:

- `PROVEN` → `PROVEN`
- `PARTIALLY_SUPPORTED` → `PLAUSIBLE`
- `INCONCLUSIVE` → `PLAUSIBLE` (with `evidence_strength: low` flag)
- `REFUTED` → `DISPROVEN`

## Test classes

Four reusable test classes cover most of the 136 entries. Each returns `(verdict, evidence)`.

| Class | When to use | Pass bar (PROVEN) | Examples |
|-------|-------------|-------------------|----------|
| `existence` | The claim is "X data is available at Y granularity to support Z action." | Source returns ≥ 1 row at the claimed granularity, license permits commercial reuse. | INS-007 (planning data exists per LA), INS-022 (VOA covers all commercial) |
| `base_rate` | The claim is "X% of population Y exhibits trait Z." | Empirical rate within ±20% of claimed rate at n ≥ 100. | INS-019 (MTD compliance), INS-018 (EPC band distribution) |
| `correlation` | The claim is "series A predicts series B with lag L." | Pearson or Spearman r ≥ 0.6, p < 0.01, n ≥ 24 observations. | INS-001 (cold snap → emergency calls), INS-002 (LME copper → BoE PPI) |
| `distribution` | The claim is "the shape of distribution X exceeds threshold T by Δ." | Fitted distribution exceeds threshold by ≥ 1 standard deviation. | INS-006 (sales-per-postcode-per-90-days), INS-008 (NHBC YoY growth) |

Lower bars produce `PLAUSIBLE`; significant deviation in the wrong direction produces `DISPROVEN`.

## ABC bridges with a client-data leg

Most catalogue entries are A–B–C bridges where **C is client data** (job records, FSM, payroll). Public data alone cannot fully prove these.

Convention:

- `PLAUSIBLE` is the default verdict when the public leg validates and the client-side claim has published research support listed in `FRAMEWORK LINEAGE`. **Most catalogue entries land here**, including INS-006 (Land Registry sale counts → conversion-to-refurb is client-side), INS-018 (EPC stock → boiler-replacement uptake is client-side), and INS-022 (VOA + Companies House universe → outreach conversion is client-side). The runner caps these at `PLAUSIBLE` even when the public-leg test passes by a wide margin.
- `PROVEN` is reserved for recipes that are **fully testable from public data with no client-side leg** — e.g. INS-011 (Companies House death-spiral signals on a named competitor list, where every input field — accounts filed late, charges, director churn — is publicly observable). No insight in the present trades pilot meets this bar; the pipeline supports the band so future fully-public recipes can land there.

This is documented per insight in the `VALIDATION:` field's `notes:` line.

## Evidence requirements

Every verdict MUST record:

- `verdict` — one of `PROVEN | PLAUSIBLE | DISPROVEN`. (Runners may also emit `SKIPPED` as a process state when auth is missing or a source is not yet wired — `SKIPPED` results are not verdicts and the evidence fields below may be empty.)
- `test_class` — `existence | base_rate | correlation | distribution`.
- `sources` — list of `{name, url, accessed_at, query_params, response_hash}`.
- `metric` — the test statistic (r, p, n, percentage, count).
- `verdict_at` — ISO date.
- `code_sha` — git SHA of the test code at run time.
- `notes` — short justification, especially for `PLAUSIBLE`.

Verdicts live as machine-readable JSON in `02_build/validators/results/<INS-NNN>.json`.

Evidence bundles (raw API responses, derived series, plots) live in `03_shadow/validators/<INS-NNN>/` — promoted to `01_truth/` once stable per `00_authority/PROMOTION_GATE.md`.

## VALIDATION: field shape (catalogue)

Additive after `STATUS:`. One line, machine-greppable:

```
**VALIDATION:** PLAUSIBLE | test_class=distribution | metric="mean=82.0, sd=29.7, claim_threshold=12.0, sigma_distance=+2.36, n=23, direction=>=; total_residential_sales=1886; window=2024-05-03_to_2026-05-03; postcode_areas=NE1,NE2,NE3" | evidence=03_shadow/validators/INS-006/ | run=2026-05-03
```

For unvalidated entries: leave the line absent. A missing `VALIDATION:` line means "not yet tested" — distinct from `DISPROVEN`.

## What stays out

- Any data crossing the GDPR boundary defined in the data-protection architecture note `[SOURCE REQUIRED]`.
- Client data of any kind. This pipeline is open-data only.
- API keys committed to the repo. All keys live in env vars; missing keys cause graceful skip with `verdict: SKIPPED, reason: AUTH_REQUIRED`.

## Scope and order

1. Trades vertical (32 entries: INS-001 to INS-032). Pilot 6 priority insights, then sweep.
2. Hospitality (27), Retail (19), ProfServices (16), Universal (22), Cross-vertical (20).
3. Quarterly re-validation so verdicts don't go stale as data refreshes.

## Governance

- Three-band scheme is **additive** to the existing `STATUS:` field. No catalogue rewrites, no field renames.
- Verdicts are reproducible: every test records the source URL, query params, raw response hash, and code SHA. A second run with the same inputs produces the same verdict or surfaces the drift.
- Verdicts expire when the underlying data refreshes per the source's published cadence (Companies House: real-time; ONS Business Demography: annual). Rerun policy lives in `02_build/validators/README.md`.

---

Signed,

**Devon-6264**
Devin session devin-6264b0ba42c6453b86b166bebc3d868a
2026-05-03
