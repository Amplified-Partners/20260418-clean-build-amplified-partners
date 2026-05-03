---
title: "Vertical Retail — public-data validation rollup (AMP-66)"
id: "vertical-retail-validation-rollup-v1"
version: 4
created: 2026-05-03
last_validated: 2026-05-03
type: document
topic_type: reference
status: candidate
ticket: AMP-66
parent_ticket: AMP-59
schema_doc: "01_truth/schemas/2026-05_public-data-validation_v1.md"
implementation: "02_build/validators/retail/"
signed_by: "Devon-9a6b, 2026-05-03, devin-9a6bd256bd7c4a90a083a471fa94a810"
---

<!-- markdownlint-disable-file MD013 -->

# Vertical Retail — public-data validation rollup (AMP-66)

**Date:** 2026-05-03
**Author:** Devon-9a6b (session `devin-9a6bd256bd7c4a90a083a471fa94a810`)
**Companion to:** `06-vertical-retail-profservices_v1.md` (descriptive vertical
profile — unchanged), `2026-05_public-data-validation_v1.md` (verdict scheme),
`00-insight-catalogue_v1.md` (per-entry `VALIDATION (AMP-66)` lines).

## 1. Headline

| Verdict     | Count | Notes                                                                  |
|-------------|-------|------------------------------------------------------------------------|
| `PROVEN`    | 9     | Public data fully reachable at claimed granularity                      |
| `PLAUSIBLE` | 9     | Underpowered, key-gated, or internal-only-with-research-support         |
| `DISPROVEN` | 0     |                                                                        |
| `DEFERRED`  | 1     | INS-077 — ToS-bound competitor scraping; held outside automated runs    |
| **Total**   | **19**|                                                                        |

Run reproducibility: every verdict file under
`02_build/validators/retail/results/INS-NNN/verdict.json` carries
`run_at_utc`, `git_sha`, `session_id`, `signed_by`, and SHA-256 hashes of every
source response.

## 2. Per-insight rollup

| ID        | Title                                                                                              | Verdict     | Test class                | Confidence |
|-----------|-----------------------------------------------------------------------------------------------------|-------------|---------------------------|------------|
| INS-060   | Footfall Forecasting × Met Office × Local Events × Transport Disruption                             | PLAUSIBLE   | existence                 | 70         |
| INS-061   | Stock-Out Risk × Shipping Port Dwell × HMRC Trade Data × FX                                         | PROVEN      | existence                 | 80         |
| INS-062   | Price Elasticity from ONS CPI × Sector CPI × Own Historical Prices                                  | PROVEN      | existence                 | 90         |
| INS-063   | Land Registry Commercial Voids as Neighbourhood Demand Signal                                       | PLAUSIBLE   | existence                 | 65         |
| INS-064   | Competitor Death-Spiral Detection via Companies House + Gazette                                     | PLAUSIBLE   | existence                 | 65         |
| INS-065   | Shopify Cohort × ONS Wages × Local IMD → LTV Segmentation                                           | PROVEN      | existence                 | 88         |
| INS-066   | Google Trends Local × Ad Spend Efficiency                                                           | PLAUSIBLE   | existence                 | 65         |
| INS-067   | Shrinkage Detection × Police.uk Crime × CCTV Event Logs                                             | PROVEN      | existence + distribution  | 88         |
| INS-068   | Marketplace Fee Leakage × FBA Storage Ageing × Demand Signals                                       | PLAUSIBLE   | existence                 | 75         |
| INS-069   | Category Cannibalisation × Cross-Sell Graph Analysis                                                | PROVEN      | existence                 | 80         |
| INS-070   | Supplier Concentration Risk × Piotroski Score Proxies                                               | PLAUSIBLE   | existence                 | 70         |
| INS-071   | Energy-Cost-per-Transaction × ONS Sub-National Energy × Tariff Switching                            | PROVEN      | existence                 | 85         |
| INS-072   | Return-Fraud Scoring × Postcode IMD (Ethically Framed)                                              | PROVEN      | existence                 | 85         |
| INS-073   | ROI on Loyalty Program with Control-Group Analysis                                                  | PROVEN      | existence                 | 90         |
| INS-074   | Google Shopping Share-of-Voice × Keyword Bid Efficiency                                             | PROVEN      | existence                 | 80         |
| INS-075   | Review Text Topic Drift × SKU Returns Clustering → Product-Quality Early Warning                    | PLAUSIBLE   | manual (research-backed)  | 70         |
| INS-076   | Support-Ticket Sentiment × Repeat-Purchase Cohort → Pre-Churn Detection                             | PLAUSIBLE   | manual (research-backed)  | 70         |
| INS-077   | Product-Description Semantic Match vs Competitor Listings → Relevance-Gap Insight                   | DEFERRED    | manual (ToS gate)         | 75         |
| INS-078   | Customer-Service Chat Sentiment Turn-by-Turn → Rebook/Repurchase Rate Predictor                     | PLAUSIBLE   | manual (research-backed)  | 70         |

## 3. Public sources actually reached

All sources below returned 2xx during this validation run; raw responses are
cached under `02_build/validators/retail/cache/` with SHA-256 hashes
recorded in each verdict.

- **Police.uk crimes-street API** (`https://data.police.uk/api`) — 10 England+Wales retail anchor postcodes, March 2026 shoplifting incidents, street-level granularity. (Glasgow + Edinburgh excluded — Police Scotland is a separate organisation that does not publish to data.police.uk; the master `RETAIL_AREAS` list still includes them for use with non-Police.uk sources.)
- **ONS Beta API** (`https://api.beta.ons.gov.uk/v1`) — `cpih01` (CPI/CPIH), `retail-sales-index`, `retail-sales-index-all-businesses`, `uk-spending-on-cards`, family-spending categories.
- **Nomis** (`https://www.nomisweb.co.uk/api/v01`) — ASHE earnings dataset metadata.
- **DLUHC IMD 2019** (`https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019`) — LSOA-level deprivation index page reachable.
- **Land Registry CCOD service page** (`https://use-land-property-data.service.gov.uk/datasets/ccod`) — service page reachable; download link is gated and goes to follow-up.
- **GOV.UK content API** (`https://www.gov.uk/api/content/...`) — Insolvency Service release collection, school term dates, DESNZ sub-national energy collection, DfT maritime/port stats collection.
- **Bank of England** (`https://www.bankofengland.co.uk/boeapps/database`) — statistical database root reachable (FX leg).
- **Amazon Seller Central** (`https://sellercentral.amazon.co.uk/help/...`) — fee-schedule documentation page (HTML doc, not an API).

## 4. Key-gated sources (downgraded to PLAUSIBLE without keys)

| Source                  | Env var                       | Affected runners                  |
|-------------------------|-------------------------------|-----------------------------------|
| Companies House API     | `COMPANIES_HOUSE_API_KEY`     | INS-064, INS-070                  |
| Met Office DataPoint    | `MET_OFFICE_DATAPOINT_KEY`    | INS-060                           |
| EPC Open Data           | `EPC_API_AUTH`                | INS-071 (optional second leg)     |

Adding any key auto-upgrades the next run without code changes — runners read
keys lazily and downgrade rather than crash when keys are absent.

## 5. Held back by policy (`DEFERRED`)

- **INS-077** — Product-description scraping of Amazon/Etsy/Google Shopping
  competitor listings sits inside platform ToS + legal-review boundaries.
  Public-data validation is **not** attempted from automated sessions; the
  recipe is gated until Ewan + legal review approve a deployment context.

## 6. Reproducibility

```bash
# from repo root
PYTHONPATH=02_build python -m validators.retail.cli list
PYTHONPATH=02_build python -m validators.retail.cli run            # all 19
PYTHONPATH=02_build python -m validators.retail.cli run --ins INS-067
PYTHONPATH=02_build python -m validators.retail.cli summary        # table view
PYTHONPATH=02_build python -m validators.retail.cli ticket-comment # markdown summary
```

Re-running with cached responses is deterministic; deleting
`02_build/validators/retail/cache/` triggers a clean re-fetch. Each verdict
records the git SHA at run time so downstream pipelines can pin to a specific
commit.

## 7. Cross-references

- Schema: `01_truth/schemas/2026-05_public-data-validation_v1.md`
- Catalogue: `01_truth/schemas/research-index/00-insight-catalogue_v1.md` (retail entries carry `**VALIDATION (AMP-66):**` lines)
- Implementation: `02_build/validators/retail/`
- Vertical profile (descriptive, unchanged): `01_truth/schemas/research-index/06-vertical-retail-profservices_v1.md`

## 8. Changelog

- v1 (2026-05-03, Devon-9a6b) — initial rollup; 8 PROVEN / 10 PLAUSIBLE / 1 DEFERRED.
- v2 (2026-05-03, Devon-9a6b) — Devin Review fixes:
  - INS-067: distribution-test `z_min` corrected from 0.5 to 1.0 to match the schema default and the runner's own docstring; verdict downgrades to PLAUSIBLE (z=0.93 < 1.0).
  - INS-069: substring-match heuristic on ONS Beta search results was inflating to PROVEN against unrelated tax/benefits dataset; replaced with a publication-route check against the canonical Family Spending Workbook 1 page (still PROVEN, but on a real signal).
  - Headline counts updated: 7 PROVEN / 11 PLAUSIBLE / 1 DEFERRED.
- v3 (2026-05-03, Devon-9a6b) — Devin Review fix:
  - INS-065: ASHE detection heuristic was assuming Nomis SDMX `name` was a string. The Nomis API actually returns it as a dict (`{"value": "annual survey of hours and earnings - workplace analysis", "lang": "en"}`), so the substring match always failed and the runner fell through to PLAUSIBLE. Fixed to handle dict shape, list-of-dicts shape, AND annotations (`Mnemonic` / `contenttype/sources` carry the canonical `ashe` tag). Verdict upgrades to PROVEN (conf 88).
  - Headline counts updated: 8 PROVEN / 10 PLAUSIBLE / 1 DEFERRED.
- v4 (2026-05-03, Devon-9a6b) — Devin Review fix:
  - INS-067: Police.uk anchor list silently included Glasgow (G1) and Edinburgh (EH1). Police.uk only covers the 43 territorial forces in England + Wales — Police Scotland is a separate organisation that does not publish to data.police.uk, so those two anchors always returned `[]`. The two structural zeros pulled the distribution mean from 184.2 down to 153.5 and inflated stdev, dropping z below the 1.0 threshold and producing a spurious PLAUSIBLE. Split `RETAIL_AREAS` into a canonical master list (still includes Scotland for use with non-Police.uk sources) and a `RETAIL_AREAS_POLICE_UK` England+Wales subset; INS-067 now uses the latter. New result: n=10, mean=184.2, σ=158.2, z=1.13 ≥ 1.0 → PROVEN (conf 88). Manchester returns 0 in March 2026 (Greater Manchester Police data lag, not a coverage gap) and is kept — it's real signal, not noise.
  - Headline counts updated: 9 PROVEN / 9 PLAUSIBLE / 1 DEFERRED.

---

Signed,

**Devon-9a6b**
Devin session `9a6bd256bd7c4a90a083a471fa94a810`
2026-05-03
