---
title: "The Outcomes Suite — Express Layer v1"
id: "outcomes-suite-briefing"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# The Outcomes Suite — Express Layer v1

**Companion to:** `alpha-scope-briefing.md` (Ingest) + `Data Driven Insights for Small Business` (Library)
**Status:** Draft for colleague review — 19 Apr 2026
**Framing:** *Reasonable data in → rich, deterministic outcomes out. Uncertainty lives only in the mathematics, never in the data.*

---

## 1. Why this document exists

The **Data Driven Insights** report is the library — 136 fusion recipes, 50+ frameworks, 4 verticals, 88k words. It is what *could* be produced if we had everything.

The **alpha-scope briefing** is the ingestion contract — 3 accounting systems, Companies House, ONS, one trade body per customer. It is what we *will actually have* on a customer site in v1.

This document is the bridge: **which named deliverables do we actually ship, from ~10 connected data sources, so that a plumber in Benton or a florist in Jesmond reads something on Monday morning that changes a decision that week?**

It is deliberately a *suite* — seven named products, each one a deterministic artefact — not a dashboard.

> *"A dashboard is a filing cabinet with the drawers open. A briefing is a letter."* — house principle

---

## 2. The Three Stages — restated as a contract

| Stage | What it produces | Where uncertainty is allowed |
|-------|------------------|------------------------------|
| **1. Ingest** | Immutable `raw_<provider>` tables. Row-for-row equal to source. | **None.** If the number in Xero is £4,217.43, the number in our warehouse is £4,217.43. Reconciliation report or the period doesn't close. |
| **2. Quality** | Cleaned, joined, typed `clean_<tenant>` tables. Contract defined in onboarding interview. | **None.** Quality issues are failed tests, not soft warnings. Data either passes the contract or is quarantined. |
| **3. Express** | `insight_<tenant>` — named outcome artefacts. | **Yes, and only here.** Every rubric emits a number *and* an uncertainty band *and* an explanation log. |

Rule: **if a number is ever uncertain, it is because the maths is uncertain, not because the data is.** No agent ever "estimates" a receivable balance. Agents only estimate things like *probability of customer churn* — where estimation is the point.

---

## 3. The Outcomes Suite — seven named products

Each product is a **file**, not a screen. Markdown first, PDF optional. Sent on a cadence. Cross-referenced. Explainable.

| # | Product | Cadence | Length | First reader | Data it needs (v1) |
|---|---------|---------|--------|--------------|---------------------|
| **1** | **The Monday Briefing** | Weekly, 07:00 Mon | 1 side A4 | Owner | Accounting + ONS |
| **2** | **The Period Close Pack** | Monthly or quarterly | 4–6 pages | Owner + accountant | Accounting + Companies House |
| **3** | **The Cashflow Horizon** | Weekly | 1 page + chart | Owner | Accounting + BoE base rate |
| **4** | **The Concentration & Risk Map** | Monthly | 2 pages | Owner | Accounting + Companies House |
| **5** | **The Sector Mirror** | Quarterly | 2 pages | Owner | Accounting + ONS + trade body |
| **6** | **The Early Warning Dossier** (Death-Spiral rubric) | Weekly, light — monthly, full | 1 page weekly / 4 pages monthly | Owner | All v1 sources |
| **7** | **The Decision Memo** | On demand | 1–2 pages | Owner + specific colleague | Any |

**Design principle:** every product starts with a one-line headline, a traffic light, and a *single recommended action*. The maths lives in the appendix. Owners read the top; accountants read the bottom.

---

## 4. Product specs

### Product 1 — The Monday Briefing

**Purpose:** The owner reads this with their first coffee. It replaces opening seven tabs.

**Structure (always this order):**
1. **Headline** — one sentence, generated deterministically from the top-ranked rubric delta.
2. **Traffic light** — Green / Amber / Red, from the Early Warning Dossier's composite score.
3. **Cash this week** — opening balance, expected in, expected out, closing forecast, uncertainty band.
4. **One thing worth doing** — the single highest-£-impact action from the rubric deltas.
5. **What changed since last Monday** — diff of top-10 rubrics.
6. **Appendix** — every number, every formula, every source.

**Deterministic rules:**
- Headline template is fixed. The agent picks *which* rubric to headline based on `|z-score of week-over-week change|`, not on judgement.
- Traffic light thresholds are pre-agreed in onboarding and written into the client's YAML config.
- Uncertainty band = 95% prediction interval from the forecasting model, stated in £, not %.

**Sources it depends on:** Xero/QBO/Sage only for v1. Nothing else is required.

---

### Product 2 — The Period Close Pack

**Purpose:** Replaces the "accountant emails a PDF three weeks late" ritual. Closes the period with numbers the owner understands and an accountant can sign.

**Structure:**
1. **P&L** — current period vs prior period vs same period last year, with variance calls.
2. **Balance sheet** — with WC movement.
3. **Cashflow** — direct method, reconciled to bank.
4. **The five ratios that matter for this business** (set in onboarding — e.g. for a plumber: labour ratio, quote-to-win, DSO, gross margin, van-utilisation-proxy).
5. **Reconciliation evidence** — every row sums, every sub-ledger ties.
6. **Companies House deltas** — any filings or officer changes in the period.

**Deterministic rules:**
- P&L must reconcile to trial balance to the penny or the pack does not ship. This is a hard gate.
- Variance calls follow a fixed template: `{metric} moved {direction} by £{amount} ({%}), driven primarily by {top-contributing subaccount by absolute £}`.
- No narrative is generated before numbers reconcile.

---

### Product 3 — The Cashflow Horizon

**Purpose:** 13 weeks forward, rolled weekly. The single most valuable artefact for an SMB.

**Core maths (deterministic):**
- **Opening cash** = current bank balance, taken directly from reconciled AR/AP + bank feed.
- **Expected inflows** = AR aged invoices weighted by a per-customer payment behaviour model (`P(paid within n days | customer history)`). Fallback: DSO-based expectation if <6 months of history.
- **Expected outflows** = AP scheduled + recurring (rent, wages, HMRC MTD VAT due date, loan repayments from Companies House charges register).
- **Stress scenarios** — three fixed: (a) top customer pays 30 days late, (b) BoE base rate +1pp if any variable-rate debt, (c) 10% demand drop.
- **Uncertainty band** — Monte Carlo over AR payment distributions, 1,000 runs, 10th/50th/90th percentile shown.

**Output format:** 13 bars. Green above floor, red below. One line: "You cross your £X minimum balance in week Y under the central scenario; week Z under the stress scenario."

---

### Product 4 — The Concentration & Risk Map

**Purpose:** Make customer, supplier, and staff concentration visible before it bites.

**Deterministic metrics:**
- **Customer Herfindahl-Hirschman Index** on rolling 12m revenue: `HHI = Σ(sᵢ)²` where sᵢ = customer share.
- **Top-5 customer share** (ToC lens — any single constraint >50% is a flag).
- **Supplier HHI** on rolling 12m spend.
- **Single-employee revenue dependency** where payroll data available (percentage of client-facing hours delivered by one person).
- **Companies House enrichment** per top-10 customer: filing history, accounts delinquency, officer changes, charges. If a top customer files a CVA or strikes off, it lights up red immediately.

**Rule:** HHI thresholds are sector-benchmarked against ONS business demography for that SIC code, not universal. A 3-customer plumbing business is normal; a 3-customer marketing agency is not.

---

### Product 5 — The Sector Mirror

**Purpose:** Answer the question every SMB owner actually asks — *"am I normal?"*

**Sources:**
- ONS business demography & regional GDP, joined on SIC 2007 + GSS code.
- ONS labour market stats for wage context.
- Trade body data (one, picked in onboarding — e.g. CheckaTrade for trades, UKHospitality for pubs).

**Metrics shown against sector benchmark:**
- Revenue per employee (FTE).
- Gross margin %.
- Wage bill as % of revenue.
- Customer repeat-visit rate (where POS or CRM data exists).
- Days sales outstanding.

**Rule:** every benchmark number is a **percentile against ONS cohort**, not a single "industry average". *"You are at the 63rd percentile for gross margin vs ONS micro-businesses in SIC 4322 in Tyne & Wear."*

---

### Product 6 — The Early Warning Dossier (the Death-Spiral rubric)

This is the most important product. Direct import from the Data Driven Insights report, adapted to v1 data availability.

**Structure:** 25 leading indicators across 5 dimensions. Each indicator is a traffic light + direction-of-travel arrow.

| Dimension | v1 indicators (data we will have) |
|-----------|-----------------------------------|
| **Financial** | Altman Z'' score, cash conversion cycle, retained earnings / total assets trend, DSO trend, gross margin trend |
| **Operational** | Quote-to-win ratio (from invoice-vs-estimate if present), billable utilisation proxy, AR aging bucket mix, work-in-progress days |
| **Customer** | Customer HHI, top-5 share, new-customer rate, repeat rate (from invoice cadence), churn rate |
| **Staff** | Payroll % of revenue, wage growth vs revenue growth, headcount trend, Bradford Factor *if* HR data connected (v1.5) |
| **Marketing** | Deferred to v1.5 — requires GMB / ads connection |

**Altman Z'' for UK private non-manufacturing SMBs** (the correct variant):
\[ Z'' = 6.56 X_1 + 3.26 X_2 + 6.72 X_3 + 1.05 X_4 \]
where \(X_1\)=working capital/total assets, \(X_2\)=retained earnings/total assets, \(X_3\)=EBIT/total assets, \(X_4\)=book equity/total liabilities. Zones: Z''>2.6 safe, 1.1–2.6 grey, <1.1 distress. ([Wall Street Prep](https://www.wallstreetprep.com/knowledge/altman-z-score/), [Wikipedia](https://en.wikipedia.org/wiki/Altman_Z-score)).

**Bradford Factor** (for HR, v1.5): \( B = S^2 \times D \) over a rolling 52-week window, where S = spells of absence, D = total days absent ([Wikipedia](https://en.wikipedia.org/wiki/Bradford_Factor)). Trigger points configured per client, not universal.

**Little's Law** (for operational flow where job-ticket data exists): \( L = \lambda W \) — average jobs in the system = arrival rate × average time in system. Useful for trades and professional services WIP ([Wikipedia](https://en.wikipedia.org/wiki/Little%27s_law)).

**Scoring:** each indicator gets 0 (green), 1 (amber), 2 (red). Composite score 0–50. Bands are set per vertical in the client's config, not globally.

---

### Product 7 — The Decision Memo

**Purpose:** On-demand. Owner asks: *"Should I hire someone?"* / *"Should I take this contract?"* / *"Should I drop this supplier?"*

**Structure (always):**
1. The decision, stated as a question.
2. The option set (at least three: do it, don't, wait).
3. For each option: expected £ impact, cash impact (tied to the Cashflow Horizon), concentration impact (tied to the Risk Map), rubric deltas.
4. What would have to be true for each option to be the right one.
5. Recommendation, with the confidence level and the specific rubrics that drove it.

**Determinism rule:** the agent writing this memo can never invent a number. Every number must trace to either (a) a rubric output, or (b) a scenario run against the Cashflow Horizon model. If a number is needed that doesn't exist, the memo explicitly flags "this is an owner judgement, not a calculation".

---

## 5. Cross-product architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  INGEST                                                          │
│  Xero  /  QBO  /  Sage   →  raw_<provider>_<tenant>             │
│  Companies House  /  ONS  /  trade body  →  raw_public          │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│  QUALITY (contract defined in onboarding interview)              │
│    • Reconciliation gate (sums tie or period doesn't close)      │
│    • Typed & joined → clean_<tenant>                             │
│    • Quality report shipped alongside every period pack          │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│  EXPRESS — the rubric engine                                     │
│    pure-python functions, fully tested, versioned               │
│    each rubric: (inputs, formula, output, uncertainty, log)     │
│           ↓                                                      │
│    → insight_<tenant> tables                                     │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│  OUTCOMES SUITE — named artefacts                                │
│  Monday Briefing │ Period Close Pack │ Cashflow Horizon │        │
│  Concentration Map │ Sector Mirror │ Early Warning Dossier │     │
│  Decision Memo                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Shared machinery used by all seven products:**
- **The rubric engine** — one pure function per rubric, tested, typed, no I/O.
- **The explanation log** — every rubric output carries its inputs and formula.
- **The attribution register** — every external data point carries its source URL, licence, and fetch timestamp.
- **The templating layer** — Markdown templates with fixed placeholders, no free-form LLM generation inside numbers.
- **The PDF renderer** — Pandoc or WeasyPrint, one theme, zero layout logic per product.

---

## 6. What we ship in v1 vs what waits

### v1 (3–6 months, three pilots: plumber, florist, hairdresser)

**Ingest:** Xero OR QBO OR Sage (one per client) + Companies House + ONS + one trade body. Reconciliation gate working.
**Rubrics:** 25 deterministic rubrics across the five Dossier dimensions (financial + operational + customer, partial on staff & marketing).
**Outcomes shipped:** Monday Briefing, Period Close Pack, Cashflow Horizon (central scenario only, no Monte Carlo), Concentration & Risk Map, Early Warning Dossier (light weekly + full monthly), Decision Memo on demand.
**Deferred:** Sector Mirror (needs ONS join reliability + trade body coverage), Cashflow Horizon stress scenarios, Bradford Factor, marketing dimension.

### v1.5 (months 6–12)

Add: HR/payroll connector → Bradford Factor + staff dimension. GMB / ads → marketing dimension. Monte Carlo on cashflow. Weather (Met Office) → demand forecasting for trades + hospitality. POS integration for retail/hospo verticals.

### v2

Add: Pudding-bridge outputs (the cross-domain recipes from the Data Driven Insights catalogue — e.g. Met Office → emergency-call surge). Sentiment & semantics layer. Consent-anchored persuasion layer applied to the Decision Memo.

---

## 7. Design principles (enforced across the suite)

1. **No dashboards in v1.** Named artefacts with cadence. A dashboard invites browsing; a briefing demands reading.
2. **The headline is always deterministic.** The owner must be able to predict what triggers which headline.
3. **The appendix always contains the maths.** Every number traceable to a formula and a source.
4. **One recommended action per artefact.** If we can't pick one, we don't ship.
5. **Traffic-light thresholds are client-specific.** Set in onboarding YAML, not hardcoded.
6. **The uncertainty band is always in £, never in %.** Owners don't calibrate to percentages.
7. **Reconciliation is a hard gate.** No artefact ships on broken data.
8. **Attribution is mandatory.** Every external datum carries its URL, licence, timestamp.
9. **The rubric engine is pure Python + tests.** No agents inside the maths. Agents only write the prose around the numbers, from fixed templates.
10. **Every outcome has a "why not this other number" line.** Explains what was considered and discarded.

---

## 8. What this gives us that the Library alone didn't

The Data Driven Insights report gives us 136 recipes; it does not tell us *which file lands in the owner's inbox on Monday*. The Outcomes Suite is the **product surface** over the library:

- It makes ambition concrete — *"we ship seven named things."*
- It makes v1 scope small without narrowing the library — *"we still have 136 recipes; we just only surface the subset that the v1 data supports."*
- It preserves the wide design — the library can grow sideways (more recipes, more verticals) without changing the seven products.
- It makes the onboarding interview obvious — we know exactly what to ask the client about, because we know exactly what we will ship back to them.

The library is the kitchen. The Outcomes Suite is the menu.

---

## 9. What I'd like colleagues to push back on

1. **Seven is a guess.** Is it six? Eight? Are any of these really the same product wearing two hats (e.g. Concentration Map folded into Period Close)?
2. **Weekly + monthly + quarterly is three cadences.** Too many? Should everything be weekly with monthly roll-ups?
3. **Owner vs accountant reader.** The Period Close Pack has two readers with different needs. Should it be two documents?
4. **Delivery format.** Markdown + PDF only in v1? Or do we need WhatsApp-native summaries from day one (consistent with the Byker Business Help positioning)?
5. **Decision Memo.** This is the highest-value product but also the hardest to keep deterministic. Is it v2 territory?
6. **"Sector Mirror" naming.** Better name welcome.

---

## 10. One-line recap

> *"Three connected systems, one onboarding interview, seven named artefacts, 25 rubrics in v1, 136 in the library, zero uncertainty in the data."*

— EOD —
