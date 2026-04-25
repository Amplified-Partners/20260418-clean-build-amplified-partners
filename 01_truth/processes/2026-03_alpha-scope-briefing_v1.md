---
title: "Alpha Scope Briefing"
id: "alpha-scope-briefing"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "alpha-scope-briefing.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Alpha Scope Briefing — UK Accounting APIs + Enrichers

Short-form companion to `uk-accounting-apis-alpha-scope.pplx.md`. Built for colleague ingestion, not exhaustive — refer to the full report for evidence and citations.

## The goal (Ewan's framing)

The alpha is a **minimal viable product that produces actionable insights for the business**. Three stages:

1. **Ingest** — bring data in from the client's real systems (accounting + public enrichers)
2. **Quality** — define "good enough" per client via an onboarding interview (rubrics owned by humans)
3. **Express** — deterministic mathematics turns ingested data into actionable insights; uncertainty lives in the maths, never in the data

Keep stages 1 and 2 wide. Narrow only at stage 3 and only where maths demands it.

## Stage 1 — Ingestion scope

### Three commercial systems for alpha

| Rank | Product | Why it's in | UK market signal |
|------|---------|-------------|------------------|
| 1 | **Xero** | Best docs, dlt verified source, accountant-channel strength | #2 UK adoption; #1 for accountant-recommended |
| 2 | **QuickBooks Online** | Largest pure SMB base; mature Airbyte source; native CDC endpoint | #1 UK adoption for sole-trader + micro |
| 3 | **Sage Business Cloud Accounting** | Covers Sage migrants; gap in OSS connectors = moat once built | #3 UK cloud; strong in accountant channel + Sage-50 upgraders |

**Deferred:** FreeAgent (v2 — narrow outside NatWest/RBS bundle). **Not in scope:** Sage 50 (desktop, different API), Sage 200 (ERP-class, different API), Sage Intacct (enterprise, XML).

### Per-product one-line gotchas

- **Xero** — 5,000 calls/day/tenant is tight; `xero-tenant-id` header on every request; `If-Modified-Since` is your friend.
- **QuickBooks Online** — use the `CDC` endpoint for incremental (max 30-day look-back); `realmId` in URL path.
- **Sage** — 5-minute access tokens + refresh-rotates-on-use = **distributed lock required around every token refresh** or you permanently disconnect customers; **no webhooks**, polling only; `X-Business` header mandatory.

### National enrichers (all clients, low marginal cost)

| Enricher | Auth | Limits | Licence | Key join keys |
|----------|------|--------|---------|---------------|
| **Companies House** | API key, HTTP Basic | 600 / 5 min | OGL v3.0 | company number, officer ID |
| **ONS** | None (open) | None published | OGL v3.0 | GSS code, SIC 2007, SOC |
| **Regulatory registers** (FCA, Gas Safe, Ofgem, Ofcom, NHS Digital) | Varies | Varies | Mostly OGL | Firm/engineer/org ID |

### Trade bodies

No cross-sector API exists. Per-customer choice during onboarding. Research method: classify by SIC → find dominant UK body → prefer regulatory register over membership body → document in that customer's SPEC.md.

### Connector framework by product

| Product | Framework | Licence | Effort |
|---------|-----------|---------|--------|
| Xero | **dlt** (verified source) | Apache 2.0 | 2–3 days to adapt |
| QuickBooks Online | **Airbyte** (source-quickbooks) | ELv2 (self-host OK) | 1 day to deploy |
| Sage | **dlt** (build on `rest_api` source) | Apache 2.0 | 1–2 weeks including token lock |

**Licence stance:** dlt-heavy keeps the majority under Apache 2.0; ELv2 is fine for self-host on the Beast (Airbyte's restrictions don't bind our business model).

### v1 minimum entity set (applies to all three)

Organisation profile · Chart of Accounts · Contacts (customers + suppliers) · Invoices (AR) · Bills (AP) · Payments · Bank Accounts · Bank Transactions · Journals · Tax Rates.

Sufficient to produce: trial balance, P&L, balance sheet, AR/AP aging, cash position.

## Stage 2 — Quality (onboarding interview)

Quality is **not** a technical property of the ingestion — it's a **contract established with the client during onboarding**. The ingestion layer simply enforces what the contract says.

### The onboarding interview establishes

| Question | Determines |
|----------|------------|
| What constitutes "complete" data per entity? | Which fields are required vs optional; which nulls are acceptable |
| How fresh must each entity be? | Freshness SLO per stream (e.g. invoices <1h, chart of accounts <24h) |
| What's the client's reconciliation frequency? | Backfill depth and incremental cadence |
| Who owns correcting upstream errors? | Quarantine-and-alert vs quarantine-and-auto-notify client |
| What's the historical window that matters? | Initial full-refresh depth (12mo / 24mo / full history) |
| Which entities drive their decisions? | Priority order when rate-limited |
| What's the definition of a "customer" / "supplier" / "employee"? | Dedup + classification rules |
| Are there tenant-specific rules (e.g. multi-entity consolidations)? | Whether to ingest 1 tenant or N |

### What Quality looks like in the pipeline

- **Deterministic schema contracts** — OpenAPI/JSON Schema, frozen types, drift quarantined
- **Data-quality assertions** per entity (Great Expectations in dev, Soda in prod)
- **Freshness monitors** per stream, alerted against SLO
- **Quarantine table** — nothing silently dropped; everything reviewable
- **Reconciliation report** per client per period — what was ingested, what was rejected, what's late

The outputs of the onboarding interview become YAML under `clients/<tenant>/quality-rubric.yaml`, version-controlled, and changeable only by a deliberate re-interview.

## Stage 3 — Expression (deterministic mathematics)

Every insight has a **rubric** — a named, documented, deterministic formula. The rubric takes typed inputs, produces a typed output, and declares its own uncertainty bounds.

### Rubric catalogue (starter set — widen freely, narrow later)

This list is intentionally broad. Narrowing happens when we pick the first customer's Life Goals and reason back to which rubrics their business actually needs.

#### Cash & liquidity

- **Cash runway** — cash on hand ÷ average monthly burn. Uncertainty: bounded by burn volatility (σ over 6m).
- **Cash conversion cycle** — DSO + DIO − DPO.
- **Current ratio** — current assets ÷ current liabilities.
- **Quick ratio** — (current assets − inventory) ÷ current liabilities.
- **Operating cash flow / Net income** — quality-of-earnings check.

#### Profitability & margin

- **Gross margin** — (revenue − COGS) ÷ revenue, monthly + trailing-12m.
- **Operating margin** — operating income ÷ revenue.
- **Net margin** — net income ÷ revenue.
- **Contribution margin per product/service line** — when chart-of-accounts supports the cut.

#### Working capital

- **Days Sales Outstanding (DSO)** — (AR ÷ revenue) × days in period.
- **Days Payable Outstanding (DPO)** — (AP ÷ COGS) × days in period.
- **Days Inventory Outstanding (DIO)** — (inventory ÷ COGS) × days in period.
- **AR aging buckets** — 0-30 / 31-60 / 61-90 / 90+.

#### Risk & solvency

- **Altman Z-Score** (you already use this) — deterministic, well-established bankruptcy predictor.
- **Debt-service coverage ratio** — operating income ÷ debt service.
- **Interest cover** — EBIT ÷ interest expense.
- **Customer concentration** — Herfindahl on revenue by customer.
- **Supplier concentration** — Herfindahl on spend by supplier.

#### Unit economics & growth

- **LTV:CAC** (you already use this) — if the data supports it.
- **Revenue growth rate** — MoM, QoQ, YoY; seasonally-adjusted via trailing-12m delta.
- **Customer retention / churn** — via contact activity over periods.
- **Net revenue retention** — expansion minus churn.

#### Operational / ToC

- **Throughput (Goldratt)** — sales − totally variable costs, per period.
- **Investment / Inventory** — capital tied up.
- **Operating expense** — everything else.
- **Throughput per constraint unit** — identifies the bottleneck.

#### Truth filter (your rubric)

- **Truth Filter score** — however you've defined this; surface as deterministic output with documented inputs.

#### Benchmarking (where enrichers earn their keep)

- **Sector percentile** — client's metric vs ONS business demography / ASHE for the same SIC + region.
- **Regional context** — how does client's wage bill compare to ASHE median for their SOC × GSS?
- **Company status flags** — Companies House filing-history derived (late filings, recent director changes, PSC changes).

### Why this list is wide, not narrow

You're right that widening is cheap here — the expensive bit is the data, not the maths. Each rubric is a small pure function. Writing 30 of them is maybe a week; choosing which 5 to *show a given client* is a product-design decision that happens later.

**Rule:** rubrics are always available in the registry; visibility per client is configured. Never delete a rubric because "this customer doesn't need it" — just don't surface it.

### Uncertainty handling

Each rubric declares its uncertainty sources, all mathematical:

| Source | Example | Handling |
|--------|---------|----------|
| Sampling period | Monthly metric on partial month | Annotate as "partial period, n days of 30" |
| Lag | Invoices not yet entered | Bound via historical invoice-entry lag distribution |
| Definitional ambiguity | "Revenue" before/after refunds | Fix definition in rubric; version the definition |
| Rounding / currency FX | Mixed-currency totals | Normalise to GBP at statement date; record rate used |
| Aggregation noise | Small-n cohorts | Return confidence interval alongside point estimate |

**Never:** uncertainty from the data itself. The ingestion + quality stages are responsible for making the data deterministic before it reaches the maths. If the data is uncertain, that's a Stage 2 problem, not a Stage 3 one.

## Strategic additions (what else to think about)

Beyond what you asked, five things worth adding explicitly to alpha scope:

### 1. A deterministic reconciliation report per client per period

Before any "insight" surfaces to the client, produce a monthly reconciliation showing: ingested rows per entity, quarantined rows with reasons, freshness per stream vs SLO, schema drift events, API quota used. This is cheap to build, expensive to retrofit, and earns immediate trust. It's the receipt for Stage 1 + Stage 2.

### 2. Baseline "currency" entities in the warehouse

Alongside the accounting primitives, ingest **FX rates** (ECB / Bank of England daily rates) and **Bank of England base rate**. Tiny ingestion cost; unlocks correct GBP-normalisation across rubrics and avoids re-doing this when a multi-currency client lands.

### 3. HMRC / Bank registers as free enrichers

Already flagged regulatory registers, but worth spelling out for alpha:
- **HMRC MTD VAT status** — whether a firm is MTD-registered (via their API if the customer authorises it)
- **VIES** — EU VAT number validation, still relevant for cross-border UK trade
- **Gas Safe / FCA / NHS ODS** — when sector-relevant

Ingesting these once, for free, and storing them per-entity adds context that the commercial accounting APIs cannot.

### 4. An "explanation log" alongside every rubric output

Every rubric output stores not just the value but: the inputs (row IDs in the warehouse), the rubric version, the definitional choices made, the uncertainty bounds. This turns the system from "here's a number" into "here's a number, and here's exactly how it was computed, and here's what could make it wrong." Critical for trust; trivial to build if baked in from day one.

### 5. A Stage-1 Stage-2 Stage-3 contract — each stage writes to a separate schema

Resist the temptation to mix. Three warehouse schemas (or three Postgres schemas):
- `raw_<provider>` — exactly what the API returned, per tenant, immutable, audited
- `clean_<tenant>` — post-quality contract, deterministic, typed
- `insight_<tenant>` — rubric outputs with explanation logs

Every stage writes to its own schema and reads from the previous. This enforces the "uncertainty lives in maths, not data" rule architecturally — if someone tries to do fuzzy reasoning at stage 1 or 2, the schema separation makes it visible.

### 6. One rubric per customer that is their "North Star"

Each customer's Life Goals Meeting produces one or two rubrics that matter most to them. Everything else is context. Surface the North Star rubric prominently; surface the rest on demand. This keeps the output actionable without narrowing the underlying maths.

### 7. Don't build a dashboard yet

Real insights for SMB owners land better as weekly or monthly narrative (briefing + rubric values) than as a dashboard they won't open. Alpha should emit a structured briefing per client per period — text + a few key numbers — not a UI. Dashboard comes when you've learnt which rubrics actually drive decisions.

## The explicit "don't narrow yet" commitments

- **Ingestion** — 3 accounting products + 2 universal enrichers + regulatory registers per sector. Wide.
- **Entities** — full v1 entity set per product (10 entity classes). Wide.
- **Rubrics** — 25+ in the registry. Wide.
- **Uncertainty handling** — mathematical only. Narrow by construction.
- **Per-customer surfaces** — 1 North Star + on-demand rest. Narrow per client, wide in what's available.

The narrowing happens at the *expression surface*, not the *ingestion ceiling*.

## What I'd do first tomorrow (if this were my build)

1. Write the three SPEC.md files (Xero, QBO, Sage) using your `@connector-spec-template` rule. Half a day.
2. Stand up dlt + Airbyte on the Beast, ingest a Xero test tenant end-to-end. 1 day.
3. Ingest Companies House + ONS against that same test tenant's registered number + GSS. Half a day.
4. Write the first 5 rubrics as pure Python functions with tests. Half a day.
5. Emit the first reconciliation report + briefing PDF for the test tenant. Half a day.

Three days to a vertical slice that proves the stages hang together, before touching a real customer.
