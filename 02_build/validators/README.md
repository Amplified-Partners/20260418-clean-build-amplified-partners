# Public-Data Validators

Pipeline that turns the literature-class `STATUS:` of each insight in the catalogue
(`01_truth/schemas/research-index/00-insight-catalogue_v1.md`) into a data-backed
`VALIDATION:` verdict by querying real UK public datasets.

Verdict bands (three-band, per AMP-59 / AMP-65):

| Band | Meaning |
|------|---------|
| `PROVEN` | Public data quantitatively confirms the claim at the granularity needed (e.g., r ≥ 0.6 with p < 0.01, or distribution exceeds the claimed threshold by ≥ 1σ, or the data the recipe needs is verifiably present at the postcode/sector granularity claimed). |
| `PLAUSIBLE` | Public data is consistent with the claim but underpowered, or one leg of the recipe is open-data-confirmable while the other requires client data. |
| `DISPROVEN` | Public data contradicts the claim (signal absent, correlation null, distribution does not show the claimed pattern). |
| `PENDING-API-KEY` | Validation depends on a registered API (Companies House, Met Office DataPoint, EPC) and the key is not yet provisioned in this environment. Out-of-band action required. |

Folding from the four-band methodology v2 scheme:
`INCONCLUSIVE` → `PLAUSIBLE`,
`PARTIALLY_SUPPORTED` → `PLAUSIBLE`,
`REFUTED` → `DISPROVEN`.

## Layout

```
02_build/validators/
├── sources/         # one HTTP fetcher per public dataset
├── tests/           # four reusable test classes
├── verticals/       # per-vertical mapping: INS-NNN → (test_class, source_args)
├── unit_tests/      # offline unit tests with recorded fixtures
├── cli.py           # `python -m validators run --vertical hospitality`
└── verdict.py       # Verdict dataclass + JSON (de)serialisation
```

Verdict bundles land in `03_shadow/validators/<vertical>/<INS-NNN>.json`
(per `00_authority/PROMOTION_GATE.md` — shadow until reviewed; promote to
`01_truth/` only after Ewan/Clawd review).

## Test classes

| Class | When to use | Output |
|-------|-------------|--------|
| `existence` | "The data needed at the granularity claimed is actually available." | `PROVEN` if a representative query returns a non-empty result with the expected fields; `PLAUSIBLE` if data exists but at coarser granularity; `DISPROVEN` if the endpoint returns no usable data. |
| `base_rate` | "X% of UK <segment> firms exhibit Y." | `PROVEN` when measured rate is within 20% of the claimed rate (or supports the directional claim); `PLAUSIBLE` if data confirms the population exists but rate not yet measurable from public alone; `DISPROVEN` if rate contradicts the claim. |
| `correlation` | "Series A leads / lags / correlates with Series B." | `PROVEN` for `\|r\| ≥ 0.6, p < 0.01`; `PLAUSIBLE` for `0.3 ≤ \|r\| < 0.6`; `DISPROVEN` for `\|r\| < 0.3`. |
| `distribution` | "The distribution of Z over <population> exceeds threshold T." | `PROVEN` when observed quantile/threshold match exceeds claim by ≥ 1σ; `PLAUSIBLE` when within ±1σ; `DISPROVEN` when below. |

## Reproducibility

Every verdict bundle records:

- source URL(s), accessed timestamp (UTC), HTTP status, response hash
- query parameters
- test class + version
- git SHA of the validator code at run time
- agent signature (Devon session id)

Raw API responses are cached locally at `02_build/validators/.cache/` (gitignored)
keyed by `sha256(method|url|sorted(params))`. Re-running the validator returns the
cached body unless `--no-cache` is passed.

## Running

```bash
# whole vertical
python -m validators run --vertical hospitality

# single insight
python -m validators run --insight INS-033

# offline (use cached responses only — useful in CI)
python -m validators run --vertical hospitality --no-network
```

CI runs the unit tests in `unit_tests/` only. Live-call sweeps run on Beast.

## Authority

- Plan: AMP-59 (Devon-21fa, 2026-05-03).
- Vertical implementations: AMP-64 (Trades), **AMP-65 (Hospitality)**, AMP-66
  (Retail), AMP-67 (Professional Services), AMP-68 (Universal).
- Three-band scheme is additive — does not replace the `STATUS:` field.

---

*Devon-4234 | 2026-05-03 | AMP-65 hospitality validator framework + sweep*
