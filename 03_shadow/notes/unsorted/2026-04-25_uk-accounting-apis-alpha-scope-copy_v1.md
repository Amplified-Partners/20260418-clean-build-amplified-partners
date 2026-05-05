---
title: "UK Accounting APIs + National Enrichers — Alpha Scope and Evidence Pack"
id: "uk-accounting-apis-alpha-scope-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# UK Accounting APIs + National Enrichers — Alpha Scope and Evidence Pack

## Executive Summary

For a UK SMB-focused alpha, three commercial accounting platforms justify standardising on: **Xero**, **QuickBooks Online**, and **Sage Business Cloud Accounting**. These win on the three selection criteria (UK SMB adoption, API/documentation quality, off-the-shelf connector availability). FreeAgent is a credible fourth but has materially narrower adoption outside freelancers and NatWest/RBS-bundled accounts; defer to a later phase.

On the enricher side, **Companies House** and **ONS** are both free, well-documented, and cover every UK client with minimal marginal complexity per new customer. Trade-body APIs are almost universally sector-specific and should be researched per-customer rather than baked into the platform.

This report is the evidence pack behind those choices, with the integration-level specifics you need before writing a line of connector code.

## A. Scope and Success Criteria

### A1. The three shortlisted systems

The shortlist is **Xero, QuickBooks Online, and Sage Business Cloud Accounting**. Evidence:

- **UK SMB adoption:** Xero and QuickBooks together hold roughly 70% of the UK small-business accounting software market ([Compare the Cloud citing Accounting Web 2024](https://www.comparethecloud.net/articles/essential-business-software-uk-small-business-2025)). Sage retains strong presence especially among accountants and traditional businesses, with Sage 50 / Sage Business Cloud covering the broad SMB base ([Tipalti UK 2026](https://tipalti.com/en-uk/blog/small-business-accounting-software/); [ANNA Money 2025](https://anna.money/blog/guides/best-accounting-software-for-small-business/)).
- **API + documentation quality:** All three publish OpenAPI-style references with OAuth 2.0, clear rate-limit documentation, and active developer portals. Xero and Sage both document rate-limit headers; QuickBooks documents tiered limits per realm and batch endpoint.
- **Off-the-shelf connectors:** All three have maintained Airbyte sources; Xero has a verified dlt context (see Section C).

FreeAgent is intentionally held back: while beloved by UK freelancers and bundled free with NatWest/RBS/Ulster ([MMBA 2024](https://www.mmba.co.uk/blog/top-accounting-software-small-businesses-uk/)), its absolute install base sits well below the big three and its OSS connector coverage is thinner. Add it in v2 once the core three are stable.

### A2. Canonical documentation URLs

| Product | Root documentation | Auth overview |
|---------|--------------------|----------------|
| Xero | [Xero Developer Portal](https://developer.xero.com/) | [OAuth 2.0 guide](https://developer.xero.com/documentation/guides/oauth2/overview/) |
| QuickBooks Online | [Intuit Developer Hub](https://developer.intuit.com/app/developer/qbo/docs/develop) | [OAuth 2.0 + OpenID Connect](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0) |
| Sage Business Cloud Accounting | [Sage Developer Accounting API](https://developer.sage.com/accounting/) | [Authentication guide](https://developer.sage.com/accounting/guides/authenticating/) |

### A3. OAuth/OIDC model, one paragraph per product

**Xero** uses OAuth 2.0 authorization code flow with PKCE for public clients and standard client-secret flow for confidential clients. Scopes are granular (`accounting.transactions`, `accounting.contacts`, etc.). Access tokens are short-lived (30 minutes); refresh tokens are 60 days and **rotate on every use**. Tenant binding happens via a separate `/connections` endpoint that returns a list of authorized tenantIds — every subsequent request must carry an `xero-tenant-id` header identifying which Xero organisation or practice the call targets, because a single user/app pairing can be connected to multiple tenants ([Xero devblog](https://devblog.xero.com/xero-oauth-2-api-whats-new-node-example-94715fc8ff19); [Xero OAuth 2.0 limits](https://developer.xero.com/documentation/guides/oauth2/limits/)).

**QuickBooks Online** uses OAuth 2.0 authorization code flow with OpenID Connect for identity. Scopes include `com.intuit.quickbooks.accounting` and `openid profile email`. Access tokens last 1 hour; refresh tokens last 100 days and rotate periodically (every 24 hours, not per use). Tenant binding is via `realmId` (the Intuit term for a company file), returned at the end of the OAuth flow and included in every request URL: `https://quickbooks.api.intuit.com/v3/company/{realmId}/...`. Intuit's `developer.intuit.com` also requires you to manage production-vs-sandbox environment toggles explicitly.

**Sage Business Cloud Accounting** uses standard three-legged OAuth 2.0 with client secret. The operational quirks are significant: access tokens expire after **just 5 minutes**, and refresh tokens (31 days) **rotate on every use** — meaning concurrent token refreshes from parallel workers will permanently disconnect the customer unless you serialise refreshes with a distributed lock ([Truto Sage integration guide](https://truto.one/blog/how-to-create-a-full-technical-integration-guide-for-sage-business-cloud-accounting/)). Business binding is via an `X-Business` header (the GUID of the specific Sage business entity), selected after a `GET /businesses` call post-authorization. Tokens may reach 2048 bytes; size your DB columns accordingly.

### A4. Rate limits and 429 behaviour

| Product | Published limits | Headers | On 429 |
|---------|------------------|---------|--------|
| Xero | 60 calls/min, 5 concurrent, 5,000/day per tenant; 10,000/min app-wide | `X-DayLimit-Remaining`, `X-MinLimit-Remaining`, `X-AppMinLimit-Remaining` ([Xero Limits FAQ](https://developer.xero.com/faq/limits)) | Back off; respect `Retry-After` when present |
| QuickBooks Online | 500/min per realmId; 10 concurrent per app per realm; batch endpoint 40/min; 800/min combined across non-QBO endpoints | Standard HTTP codes; no dedicated rate headers documented | Wait 60 seconds before retry ([Intuit docs](https://developer.intuit.com/app/developer/qbo/docs/learn/rest-api-features)) |
| Sage Business Cloud Accounting | Two documented regimes — older regions show 100/min + 2,500/day per company; current v3.1 platform documents 1,296,000/day per app and 150 concurrent; UK-specific "200 calls in any 60 seconds per business" documented on the developer portal | `x_request_id` per response (for support correlation) | Exponential backoff; avoid parallel POSTs that generate sequential numbers ([Sage developer portal](https://developer.sage.com/accounting/guides/your_first_request/)) |

The Sage numbers genuinely diverge across documentation sources — plan for the most conservative (200/min per business) and raise if the production API confirms higher.

### A5. Incremental sync

**Xero** uses the `If-Modified-Since` HTTP header on most accounting endpoints (Invoices, Contacts, BankTransactions, ManualJournals, etc.). The connector sends the header with the last-successful-sync timestamp, and Xero returns only records modified since. Soft deletes are surfaced via a `Status` field (e.g. `Invoice.Status = "DELETED"`) rather than row removal. Budgets and a handful of other endpoints do not honour `If-Modified-Since` and require `DateFrom`/`DateTo` query parameters instead ([Stack Overflow 2024](https://stackoverflow.com/questions/78481604/xero-if-modified-since-filter-doesnt-work)).

**QuickBooks Online** uses the `CDC` (Change Data Capture) operation: `GET /v3/company/{realmId}/cdc?entities=Customer,Invoice&changedSince=<ISO8601>`. This is the documented mechanism for incremental pulls across multiple entity types in a single request. Individual entity queries also support `Metadata.LastUpdatedTime` filters in the SQL-like query language. Soft deletes return entities with `status="Deleted"`. Webhooks are available for push-style sync and should be used in parallel with polling for freshness-sensitive entities.

**Sage Business Cloud Accounting** has **no webhooks** ([Truto 2026](https://truto.one/blog/how-to-create-a-full-technical-integration-guide-for-sage-business-cloud-accounting/)) — polling is the only option. Incremental sync uses the `updated_or_created_since` query parameter on list endpoints, which returns records modified since the specified ISO 8601 timestamp. Deletion handling is inconsistent across resources; treat soft deletes as "refresh-on-miss" (if a previously-seen ID no longer appears, verify via GET-by-id).

### A6. Minimum v1 entity set per product

A defensible minimum set for financial-state visibility on an SMB client, consistent across all three providers:

| Entity class | Xero | QuickBooks Online | Sage Accounting |
|--------------|------|-------------------|-----------------|
| Organisation/company profile | `Organisations` | `CompanyInfo` | `businesses` + `settings` |
| Chart of accounts | `Accounts` | `Account` | `ledger_accounts` |
| Contacts (customers + suppliers) | `Contacts` | `Customer` + `Vendor` | `contacts` |
| Invoices (AR) | `Invoices` (Type=ACCREC) | `Invoice` | `sales_invoices` |
| Bills (AP) | `Invoices` (Type=ACCPAY) | `Bill` | `purchase_invoices` |
| Payments | `Payments` | `Payment` + `BillPayment` | `contact_payments` |
| Bank accounts | `Accounts` (where Type=BANK) | `Account` (AccountType=Bank) | `bank_accounts` |
| Bank transactions | `BankTransactions` | `Deposit`, `Transfer`, `Purchase` | `bank_transactions` |
| Journal entries | `ManualJournals`, `Journals` | `JournalEntry` | `journals` |
| Tax rates | `TaxRates` | `TaxRate`, `TaxCode` | `tax_rates` |

This set is sufficient to produce trial balance, P&L, balance sheet, AR/AP aging, and cash-position views — the minimum actionable business-intelligence surface for an SMB. Reports endpoints (where available) can substitute for some of the derived views if you want fewer raw entities in v1, but ingesting the primitives is the more defensible long-term choice.

## B. UK Market Adoption — Directional Evidence

### B1. Relative adoption rank

No single published number is authoritative, but the consensus across multiple UK-oriented sources puts the rank as:

1. **QuickBooks Online** — most-adopted by UK SMBs in aggregate, especially sole traders and micro-businesses ([Tipalti UK 2026](https://tipalti.com/en-uk/blog/small-business-accounting-software/))
2. **Xero** — close second; favoured by accountants and slightly larger SMBs; dominant in ecosystem breadth with 1,000+ integrations ([Fusion Accountants 2024](https://www.fusionaccountants.co.uk/blogs/small-uk-business-accounting-software/))
3. **Sage** — third for pure SMB cloud; still strong among accountants and businesses with legacy Sage 50 desktop history
4. **FreeAgent** — concentrated in freelancers/contractors; huge when bundled free with NatWest/RBS/Ulster, smaller otherwise

Xero + QuickBooks together = ~70% of the UK SMB cloud accounting market per [Compare the Cloud 2024](https://www.comparethecloud.net/articles/essential-business-software-uk-small-business-2025). Treat as bands, not precision: within SMB subsegments the ordering shifts (e.g. QuickBooks leads sole-trader, Xero leads accountant-recommended).

### B2. Material UK-specific differences

Three differences materially affect API choice for UK customers:

**Making Tax Digital (MTD)** — HMRC requires MTD-compatible software for VAT (thresholds now universal) and from 6 April 2026 for Income Tax Self Assessment at turnover >£50,000, rising to more sole traders in subsequent years ([makingtaxdigital.campaign.gov.uk](https://makingtaxdigital.campaign.gov.uk/making-tax-digital-software/); [gov.uk MTD ITSA guidance](https://www.gov.uk/guidance/choose-the-right-software-for-making-tax-digital-for-income-tax)). All four candidates (Xero, QBO, Sage, FreeAgent) are HMRC-recognised, so MTD does not filter the shortlist — but it means your derived outputs (VAT returns especially) must be reconciliable against the client's MTD submission. Plan to ingest `TaxReturns` / VAT liability endpoints where available.

**Bank feeds** — UK bank feeds are well-supported on all three shortlisted products, but via different back-ends. Xero partners with Plaid and TrueLayer for Open Banking; QuickBooks Online uses direct bank feeds where available and Plaid-like aggregators elsewhere; Sage uses its own feed partners. The API-visible artefact is the same (`BankTransaction` entities with a `source` field identifying feed origin), but reconciliation-related UI and statement import endpoints differ across products. This does not change API choice, but it changes how you explain data provenance to the client.

**Product SKU mapping** — Sage's UK portfolio has **three distinct products** that confuse integration scope: *Sage Business Cloud Accounting* (the cloud SMB product, API-first, v3.1 documented above), *Sage 50* (desktop-based with cloud-connected features, different API surface, slower modernisation), and *Sage 200* (medium-business ERP, entirely different API). The shortlisted target is **Sage Business Cloud Accounting** only — do not assume a single "Sage API" serves all three products ([HBP Group 2023](https://thehbpgroup.co.uk/blog/sage-200-vs-sage-50); [F1Group 2026](https://www.f1group.com/sage-200-vs-sage-50/)). For clients on Sage 50 or Sage 200, scope separate adapters or route through a unified layer like Truto / Apideck.

## C. Off-the-Shelf Ingestion

### C1. Airbyte connector coverage

| Product | Airbyte source doc | Status signal |
|---------|--------------------|--------------|
| Xero | [docs.airbyte.com/integrations/sources/xero](https://docs.airbyte.com/integrations/sources/xero-migrations) | Migrated to v2.0.0 with `client_credentials` and `bearer_token` auth; actively maintained |
| QuickBooks Online | [docs.airbyte.com/integrations/sources/quickbooks](https://docs.airbyte.com/integrations/sources/quickbooks) | Supports Full Refresh and Incremental Append/Deduped; published to PyPI as `airbyte-source-quickbooks` ([PyPI 2025](https://pypi.org/project/airbyte-source-quickbooks/)) |
| Sage Business Cloud Accounting | **Not natively supported by Airbyte** | Airbyte offers `sage-hr` (HR product, different API) but not Accounting; `sage-intacct` only via CData Connect Cloud bridge ([cdata.com](https://www.cdata.com/kb/tech/intacct-cloud-airbyte.rst)) |

The Sage gap is the most important finding here. For Sage Business Cloud Accounting you will either (a) write a custom Airbyte CDK connector, (b) build on dlt's REST API source, or (c) route through a unified API provider like Truto or Apideck. Given the operational quirks (5-min tokens, no webhooks, X-Business header), the dlt path is the simplest substrate — see C2.

### C2. dlt coverage

dlt (dltHub, Apache 2.0) provides a [verified Xero source](https://dlthub.com/context/source/xero-finance) with OAuth 2.0 bearer-token authentication and a declarative REST API config that handles pagination and schema evolution. For QuickBooks and Sage there's no verified source, but both fit the `rest_api` source pattern cleanly — the declarative config approach (base_url, auth, per-resource endpoint/data_selector/pagination) handles most of the connector work with ~50 lines of Python. dlt verified sources live at [dlt-hub/verified-sources](https://github.com/dlt-hub/verified-sources) under Apache 2.0.

Recommendation by product:

- **Xero:** use dlt's verified Xero source as the starting fork; customise for your Xero scopes.
- **QuickBooks Online:** use Airbyte's `source-quickbooks` (maintained, handles CDC) OR build on dlt's `rest_api` if you want the code-first control. For the Beast self-host, Airbyte is lower maintenance for this provider.
- **Sage Business Cloud Accounting:** build on dlt's `rest_api` source. The 5-minute token lifecycle and X-Business header are easier to handle in dlt's code-first model than in Airbyte's YAML manifest. Budget 1–2 weeks for a production-grade Sage connector including distributed refresh lock.

### C3. Licence implications

**Airbyte Core** is licensed **Elastic License 2.0 (ELv2)** ([Airbyte Docs license FAQ](https://docs.airbyte.com/community/licenses/license-faq)). Airbyte CDK and Airbyte Protocol are MIT. Individual connectors are either MIT or ELv2 — check each `metadata.yaml`.

ELv2 constraints that matter for the Amplified Partners deployment model:

1. **You cannot offer Airbyte as a managed ETL/ELT product to third parties** — i.e. you cannot resell "hosted Airbyte" as a competing managed service.
2. **You cannot expose Airbyte's UI or API directly to your customers as the product.**
3. **You cannot remove or circumvent license keys.**

**What's allowed** and relevant: self-hosting Airbyte on the Beast to ingest data for your own consulting/SaaS customers, customising connectors, building a product on top of Airbyte where Airbyte is the ETL plumbing (not the user-facing product). ELv2 is functionally equivalent to permissive OSS for this use case ([Workflow Automation 2026](https://workflowautomation.net/reviews/airbyte); [Airbyte ELv2 text](https://docs.airbyte.com/community/licenses/elv2-license)).

**dlt** is **Apache 2.0** ([PyPI](https://pypi.org/project/dlt/)) — no such constraints. If you want to avoid ELv2 consideration entirely, standardising on dlt for all three accounting providers is the cleanest path, at the cost of more connector-authoring work for QuickBooks.

The practical recommendation: **dlt-first for Xero and Sage, Airbyte for QuickBooks**, deployed on the Beast. This combines the strongest connector coverage with the lightest licence footprint, and keeps the majority of the stack under Apache 2.0.

## D. National Enrichers

### D1. Companies House API

**Entry URL:** [developer.company-information.service.gov.uk](https://developer.company-information.service.gov.uk/) (REST) and [developer-specs.company-information.service.gov.uk](https://developer-specs.company-information.service.gov.uk/) (OpenAPI specs).

**Authentication:** HTTP Basic Auth with an API key (no password — key goes in the username field, password blank). Base64-encode `<api_key>:` for the `Authorization: Basic` header. API keys are free; register at the developer portal.

**Rate limits:** 600 requests per 5-minute window per API key; 429 returned for excess, with the window resetting to 600 at the end of the 5 minutes ([Developer Guidelines](https://developer.company-information.service.gov.uk/developer-guidelines); [Rate limiting guide](https://developer-specs.company-information.service.gov.uk/guides/rateLimiting)). The Main API and Document API have independent limits. The Streaming API has its own limit not exposed via headers; back off on 429. Higher limits are available on request.

**Recommended endpoints for entity resolution:**

| Endpoint | Purpose |
|----------|---------|
| `GET /company/{company_number}` | Company profile — name, status, registered address, incorporation date, SIC codes, accounts next-due dates |
| `GET /company/{company_number}/officers` | Directors and secretaries with appointment/resignation dates, nationality, occupation |
| `GET /company/{company_number}/filing-history` | Filings list (annual returns, accounts, director changes); supports `category` filter and `items_per_page`/`start_index` pagination ([CH Guide](https://chguide.co.uk/rest-api/data-endpoints/filing-history)) |
| `GET /search/companies` | Free-text company search for resolution when you have a name but not a number |
| `GET /company/{company_number}/persons-with-significant-control` | PSC register — beneficial ownership |

For standard entity resolution (matching your client's "Acme Ltd" customer to a Companies House record), the sequence is: search by name → pick best match via status + address + incorporation date → pull profile → pull officers + filing-history as needed.

### D2. Companies House — terms and fair use

Companies House data is **Crown copyright** and released under the **Open Government Licence v3.0** (OGL v3.0) ([National Archives OGL](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)). That licence grants worldwide, royalty-free, perpetual use including for commercial purposes.

Product behaviours you must bake in:

1. **Attribution** — wherever Companies House data is displayed, credit must be included. A compact form such as "Company data from [Companies House](https://find-and-update.company-information.service.gov.uk/) under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)" in a data-sources footer meets the requirement.
2. **Rate limit hygiene** — never run unbounded company-name search loops. Cache results; respect the 600/5-min ceiling at a scheduler level, not just per-worker.
3. **Data freshness** — the CH register updates continuously but there is a publication lag (typically hours to days for filings). Do not present derived data as "real-time"; treat cached values as valid for at least 24 hours unless you have a business reason to re-fetch.
4. **Don't re-publish as a competing register** — the OGL permits commercial use including re-distribution, but if you build a product whose primary purpose is re-publishing CH data as a CH-alternative register, you should review the specific licence text and consider whether the spirit matches your intent.

### D3. ONS API and datasets

**Entry URL:** [developer.ons.gov.uk](https://developer.ons.gov.uk) — API base `https://api.beta.ons.gov.uk/v1`. **No API key required**, no authentication; the API is fully open ([ONS Developer Hub](https://developer.ons.gov.uk)).

The API is REST/JSON with two main interaction patterns:
- **Observation-level** — `GET` with one option per dimension (optionally a wildcard dimension) to pull specific data points
- **Filter a dataset** — `POST` to `/filters` with multiple dimension selections, returning CSV/XLSX bulk output

**Datasets best for UK-wide client context:**

| Purpose | Dataset / API | Join key |
|---------|---------------|----------|
| Geography / postcodes | ONS Geography APIs — GSS codes, Output Areas, LSOA, MSOA, LAD hierarchies | GSS code (e.g. `E06000014` for York) or postcode |
| Population / demographics | Census 2021 via `/datasets` — age, ethnicity, occupation, household composition | GSS code + dimension |
| Business demography | UK Business Activity / ONS Business Demography | SIC 2007 code + region |
| Labour market | Labour Force Survey, ASHE (Annual Survey of Hours and Earnings) | SOC + region |
| Economic indicators | CPI, RPI, GDP, inflation time series | Time period + category |
| Deprivation | IMD (via ONS geography layer) | LSOA code |

The stable join keys you'll want to land are **GSS codes** (for geography), **SIC 2007 codes** (for sector), and **SOC codes** (for occupation). Your client's postcode and industry classification map cleanly into all ONS datasets via these.

### D4. ONS — licence and attribution

ONS data is licensed under the **Open Government Licence v3.0** (the response metadata explicitly shows `"license": "Open Government Licence v3.0"` on every dataset — see [ONS /datasets response](https://developer.ons.gov.uk/dataset/datasets/)).

Attribution requirement (same as Companies House): any derived metric displayed to clients must carry a source credit. Recommended form: "Source: [Office for National Statistics](https://www.ons.gov.uk/) licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."

Practical patterns to bake into product behaviour:

1. Store the ONS `dataset_id`, `edition`, and `version` alongside every ingested value. ONS data updates periodically and versions are permanent references; citing version in your UI gives the client reproducibility.
2. Do not modify values in ways that mislead — if you round or aggregate, label it as derived.
3. Respect the "no endorsement" clause: do not imply ONS endorses your product.

### D5. Trade bodies — cross-sector vs sector-specific

**The honest answer:** there is no cross-sector UK trade-body API ecosystem comparable to ONS or Companies House. Trade-body data APIs are overwhelmingly sector-specific, typically available only to members or paying subscribers, and maturity varies from mature (FCA regulated-firm register, NHS Digital for healthcare) to non-existent (most trade associations publish PDFs, not APIs).

For the alpha, **do not attempt cross-sector trade-body integration.** Treat trade-body data as a per-customer enrichment, scoped during onboarding.

**Method to pick the right body for customer #1:**

1. **Classify the customer** by primary SIC 2007 code (you already have this from Companies House).
2. **Identify the dominant UK trade association(s)** for that SIC via: (a) gov.uk business guidance for the sector, (b) `associationsearch.uk` or the [UK Trade Association Forum directory](https://www.taforum.org/), (c) a direct web search for "[sector] UK trade body".
3. **Assess data availability** in order: (a) public website with structured data (scrapeable — fallback only), (b) member API / data portal, (c) paid data partner (Dun & Bradstreet, S&P, BvD), (d) regulatory register (FCA, Ofgem, Ofcom, etc.) if the sector is regulated.
4. **Regulatory registers are usually the best first integration** for regulated sectors because they are free, authoritative, and API-accessible: FCA Financial Services Register, NHS Digital ODS, Ofgem supplier register, Ofcom CLI number blocks, etc.
5. **Document the decision in the customer's Connector SPEC.md** with rationale, access method, and refresh cadence.

For your pilot (Jesmond Plumbing, plumbing/heating sector), the relevant bodies are **Gas Safe Register** (statutory — API access for engineer/business verification available on request), **CIPHE** (Chartered Institute of Plumbing and Heating Engineering — directory only, no public API), and **OFTEC** (for oil-fired heating — member data not publicly APIed). Gas Safe is the high-value integration; the others are reference-only.

## Alpha Scope Summary Table

| Decision area | Chosen | Rationale |
|---------------|--------|-----------|
| Accounting #1 | Xero | Highest accountant-channel adoption; best API docs; dlt verified source available |
| Accounting #2 | QuickBooks Online | Largest pure SMB base in UK; mature Airbyte source; CDC endpoint for clean incremental |
| Accounting #3 | Sage Business Cloud Accounting | Covers Sage migrants and accountant-recommended; gap in OSS connectors = differentiator once built |
| Deferred | FreeAgent | Narrower adoption outside NatWest/RBS bundle; add in v2 |
| Enricher #1 | Companies House | Free, covers all UK clients, OGL-licensed |
| Enricher #2 | ONS | Free, covers all UK-wide context with stable join keys (GSS/SIC/SOC) |
| Enricher #3 | Trade bodies | **Per-customer** during onboarding; start with regulatory registers if applicable |
| Ingestion framework | dlt (Xero, Sage) + Airbyte (QuickBooks) | Minimises ELv2 exposure; leverages verified sources where they exist |
| Licence stance | Apache 2.0 dominant, ELv2 acceptable for self-host | ELv2 does not restrict Amplified's business model |

## Key Risks and Open Questions for Alpha

1. **Sage token concurrency** — the 5-minute token + refresh-rotation requires a distributed lock across all Sage workers on day one, not a bolt-on later. This is the single highest-risk operational detail across the three accounting providers.
2. **Xero daily quota** — 5,000 calls/day per tenant is generous but tight during initial full-refresh of large clients. Plan incremental-first; full-refresh only under explicit job with rate budget.
3. **QuickBooks CDC edge cases** — the CDC endpoint has a documented maximum look-back of 30 days. For longer gaps (after a long pause or first connection), fall back to per-entity queries with `Metadata.LastUpdatedTime` filters.
4. **FreeAgent entry cost** — if a pilot customer is on FreeAgent-via-NatWest, budget 1 week to add a fourth provider since no verified dlt/Airbyte source exists and the API is less well-documented.
5. **Companies House Streaming API** — if you need real-time company-change feeds (e.g. insolvency alerts for credit monitoring), the Streaming API is separate from the REST API and has its own rate regime. Scope only if the product need is explicit.

These are not blockers for alpha — they are implementation-detail items that, if ignored, produce P0 incidents later.
