---
version: 1.0.0
status: active
authority: "schema reference for the public-data validators pipeline"
related:
  - 01_truth/schemas/2026-03_validation-methodology_v2.md
  - 01_truth/schemas/research-index/00-insight-catalogue_v1.md
  - 01_truth/schemas/research-index/02-public-datasets-uk_v1.md
  - 02_build/validators/
signed-by: Devon-4234 | 2026-05-03 | session devin-4234e1c8afbe42f2aff84a29ce139809
changelog:
  - 2026-05-03 — Devon-4234: initial draft (AMP-65 hospitality sweep).
---

# Public-Data Validation — Schema (v1)

<!-- markdownlint-disable-file MD013 MD024 -->

## Purpose

Specifies the contract between the validators pipeline (`02_build/validators/`)
and any consumer that wants to know whether a catalogued insight (INS-NNN) has
been confirmed against real UK public data.

This document is reference. It does not introduce policy. It captures the field
shapes, verdict semantics, and test-class definitions used by the pipeline so
that downstream tooling (catalogue rendering, recipe routing, status dashboards,
client-facing diagnostics) can rely on a stable surface.

## 1. Verdict bands (three-band scheme + key gate)

| Band | Meaning |
|------|---------|
| `PROVEN` | Public data quantitatively confirms the claim at the granularity the recipe needs. Examples: r ≥ 0.6 with p < 0.01 over n ≥ 8 paired observations; distribution z ≥ 1σ above the claim threshold; existence-class probes 100% pass for a fully-public-leg recipe. |
| `PLAUSIBLE` | Public data is consistent with the claim but the public-only sample is underpowered, OR one leg of a recipe is open-data-confirmable while the other leg requires client data. Most hospitality recipes land here because they fuse a public signal (weather, FHRS, ONS) with a client signal (POS, rota, reservations). |
| `DISPROVEN` | Public data contradicts the claim — required signal is absent, correlation is null, or the distribution is wrong. Recipe must be revised before it is offered to clients. |
| `PENDING-API-KEY` | Validation requires a registered key (Met Office DataPoint, Companies House, EPC) that is not yet provisioned. Verdict deferred — not a failure. |

The three bands are a **fold** of the four-band scheme in
`2026-03_validation-methodology_v2.md`: the legacy `INFERRED` band is collapsed
into `PLAUSIBLE` because, for the validators pipeline, "consistent but
underpowered" and "consistent but partly client-side" are the same operational
signal — they both mean *do not promote to a billable claim without client data*.

## 2. Test classes

The pipeline supports four reusable test classes. Every per-insight validator
picks one (or composes several via the existence runner).

| Class | Decision rule | Default thresholds |
|-------|---------------|--------------------|
| `existence` | Run a list of probes; `PROVEN` if all pass, `PLAUSIBLE` if at least one passes, `DISPROVEN` if zero pass. | n/a |
| `base_rate` | Compare measured rate `m` from a public source to a claimed rate `c`. `PROVEN` if `\|m − c\| / c ≤ 0.20` (default tolerance) and direction matches; `DISPROVEN` if outside tolerance and direction matters; `PLAUSIBLE` if measured is `None`. | tolerance=0.20 |
| `correlation` | Pearson r over paired numeric series, expected sign supplied by recipe. `\|r\| ≥ 0.6` → `PROVEN`; `0.3 ≤ \|r\| < 0.6` → `PLAUSIBLE`; `\|r\| < 0.3` → `DISPROVEN`; `n < 8` → `PLAUSIBLE`. | n_min=8, r_high=0.6, r_low=0.3 |
| `distribution` | Compute `z = (observed_quantile − claim) / sigma`. `z ≥ 1.0` → `PROVEN`; `−1 < z < 1` → `PLAUSIBLE`; `z ≤ −1` → `DISPROVEN`; `n < 5` → `PLAUSIBLE`. | n_min=5, z_high=1.0, z_low=−1.0 |

Thresholds are knobs, not invariants. A validator may override them for an
insight where the recipe is sensitive to a tighter / looser bar; the override
must be passed as an argument to `tests/<class>.run` and recorded in the
`metrics` field of the `Verdict` so the chosen threshold is reproducible.

## 3. Verdict bundle

Every validator emits a `Verdict` object. The on-disk JSON shape (one file per
insight at `03_shadow/validators/<vertical>/<INS-NNN>.json`):

```json
{
  "insight_id": "INS-034",
  "title": "Food Hygiene Score vs Review Sentiment vs Competitor Mapping",
  "vertical": "hospitality",
  "band": "PROVEN",
  "test_class": "existence",
  "rationale": "Free text, ≤300 words, explaining why the band was assigned.",
  "evidence": [
    {
      "source": "fsa.fhrs",
      "url": "https://api.ratings.food.gov.uk/Establishments?...",
      "accessed_at": "2026-05-03T20:46:01.123456+00:00",
      "http_status": 200,
      "response_sha256": "f1e2…",
      "query_params": {"localAuthorityId": "260"},
      "summary": "260 establishments in Newcastle upon Tyne LA"
    }
  ],
  "metrics": {"establishments_in_la": 260, "rating_diversity": 5},
  "run_at": "2026-05-03T20:46:01.123456+00:00",
  "code_sha": "c8863e8",
  "agent": "Devon-4234",
  "notes": ""
}
```

### Field semantics

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `insight_id` | string | yes | `INS-NNN` |
| `title` | string | yes | Catalogue title (no truncation). |
| `vertical` | string | yes | One of `hospitality`, `trades`, `retail`, `prof_services`. |
| `band` | enum | yes | One of the four bands in §1. |
| `test_class` | enum | yes | One of `existence`, `base_rate`, `correlation`, `distribution`. |
| `rationale` | string | yes | Plain English. State which leg (public / client) is being validated and what the verdict means. |
| `evidence` | array | yes | One entry per upstream HTTP fetch. Empty only if the band is `PENDING-API-KEY`. |
| `evidence[i].source` | string | yes | Slug, dotted: `fsa.fhrs`, `ons.cpih_food`, `met_office.datapoint`. |
| `evidence[i].url` | string | yes | Final URL hit (after redirects). |
| `evidence[i].accessed_at` | ISO-8601 | yes | UTC. |
| `evidence[i].http_status` | int | yes | Response status (cached responses preserve original status). |
| `evidence[i].response_sha256` | hex string | yes | Of the raw response body bytes; lets reviewers cross-check the cached payload at `02_build/validators/.cache/`. |
| `evidence[i].query_params` | object | optional | The query string sent. |
| `evidence[i].summary` | string | yes | One-line interpretation. |
| `metrics` | object | yes | Test-class-specific numerics: counts, rates, r, z, n, etc. |
| `run_at` | ISO-8601 | yes | Verdict creation time. |
| `code_sha` | string | yes | Short git SHA of the validators code at run time. |
| `agent` | string | yes | Devon session signature, e.g. `Devon-4234`. |
| `notes` | string | optional | Free-text follow-up notes. |

### Versioning

The bundle shape is versioned with this schema document. A change that adds
fields is non-breaking and bumps the minor version. A change that removes or
renames fields bumps the major version and requires a coordinated update to
catalogue rendering and recipe routing.

## 4. Caching contract

- Every HTTP fetch that produces evidence is cached on disk under
  `02_build/validators/.cache/`.
- The cache key is `sha256(method | url | sorted query_params)`.
- Cached entries store: response status, headers, body bytes, original UTC
  fetch time, and a `from_cache` flag in the deserialised `CachedResponse`.
- Re-runs use the cache by default. `--no-cache` forces re-fetch.
  `--no-network` raises `CacheMiss` instead of touching the network — used in
  CI / offline review contexts.
- The `response_sha256` recorded in the evidence is the SHA of the body bytes,
  computed at fetch time and re-used on cache hits. Reviewers can byte-compare
  the cached payload against the recorded SHA to verify provenance.

## 5. Catalogue surface

Catalogue entries (`01_truth/schemas/research-index/00-insight-catalogue_v1.md`)
gain a single new field, additive to existing structure:

```text
**STATUS:** HYPOTHESIS | CONFIRMED-EXTERNAL | CONFIRMED-INTERNAL
**VALIDATION:** PROVEN | PLAUSIBLE | DISPROVEN | PENDING-API-KEY (test_class=…, run YYYY-MM-DD; see 03_shadow/validators/<vertical>/<INS-NNN>.json)
```

`STATUS` and `VALIDATION` are orthogonal:

- `STATUS` is editorial — does the insight exist in the catalogue and has it
  been confirmed by literature / domain expert review.
- `VALIDATION` is empirical — does the public-data leg of the recipe actually
  return the data we said it would, at the granularity claimed.

A `CONFIRMED-EXTERNAL` insight can still be `PENDING-API-KEY` if the publisher
gates the data behind a key we have not yet provisioned. A `HYPOTHESIS`
insight can still be `PROVEN` if the public-data leg is all we are claiming and
it lands.

## 6. Promotion rule

Verdict bundles live in `03_shadow/validators/<vertical>/` until reviewed.

- Reviewer (Ewan or designated partner) opens the JSON, inspects `evidence[]`
  and `metrics`, and either:
  - Approves — the catalogue VALIDATION line is committed as-is and the bundle
    promotes (by reference, not by move) into the canonical catalogue layer.
  - Disputes — the bundle stays in `03_shadow/`, a follow-up validator is
    scheduled with a tighter probe, and the catalogue VALIDATION line either
    stays unchanged or is reverted.
- Bundles are never deleted. Disputes append to `notes`; reruns produce a new
  bundle alongside the old one with a new `run_at` and `code_sha`.

## 7. Reproducibility

Re-running the sweep against the same cache deterministically produces the same
verdict bundle modulo `run_at`. Re-running with `--no-cache` re-fetches
upstream data; if the upstream data has shifted (e.g. ONS revised an index, a
local authority was added to FHRS), the verdict can legitimately change. This
is captured in the `code_sha` + `run_at` pair on the bundle.

For deterministic CI checks: pin to a recorded cache snapshot (the
`02_build/validators/.cache/` tree at a known SHA) and run with `--no-network`.
The validators raise on cache miss instead of producing partial verdicts.

---

*Devon-4234 | 2026-05-03 | AMP-65 hospitality public-data validation.*
