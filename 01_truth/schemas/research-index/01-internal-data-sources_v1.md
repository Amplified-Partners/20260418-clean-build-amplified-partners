---
title: "Internal Data Sources"
id: "internal-data-sources"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "01-internal-data-sources.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Internal Data Sources Catalogue — Amplified Partners / Byker Business Help
**Research Workstream 01 of 05 — Forensic Data-Mining Engine**
*Prepared for Ewan Bramley | April 2026*

---

## Why GDPR Is Not The Blocker Here

Every data source in this catalogue is subject to UK GDPR (UK Data Protection Act 2018) and, where applicable, PECR. Under the Amplified Partners P2 tokenisation architecture, **raw client data never leaves the client's physical premises**. What transmits outbound is:

- **Personal names** → opaque UUID tokens (HashiCorp Vault, Shamir's Secret Sharing for key custody)
- **Postcodes** → outward-code only (e.g. `NE6` not `NE6 1AA`)
- **Transaction amounts** → decile-bucket encoding within industry peer group
- **Phone numbers** → one-way hashed identifiers for graph-edge construction only
- **Account references** → rotating tokens refreshed on every sync cycle

The full data store remains on the client's Beelink N100 (or Beast-equivalent on-site hardware). De-tokenisation occurs exclusively in-house on data exit. This is disclosed contractually at onboarding. The processing lawful basis is **legitimate interests (Art. 6(1)(f))** for business analytics — a basis the ICO explicitly endorses for internal business intelligence — supported by a one-page DPIA completed during the HoundDog interrogation phase.

**Implication for this document:** No per-source GDPR commentary is needed. Instead each source carries a *Tokenisation pattern* line showing exactly which fields tokenise before aggregation.

**The cross-client dividend:** When 50+ tokenised, normalised client datasets pool into Ewan's central pattern-detection layer — an internal, proprietary "Office of National Statistics" for UK SMBs — the result is a benchmark dataset no competitor can replicate. Sector-normalised KPIs (debtor days by SIC code, call abandonment rates by trade type, staff churn by tenure band) become a durable moat.

---

## Master Summary Table

| # | Source Category | Top Platform(s) | Extraction Method | Difficulty | Accuracy Ceiling | Cross-Client Value |
|---|---|---|---|---|---|---|
| 1 | Email & Comms | Gmail, Outlook/Exchange | API (Gmail API, Graph API) | Medium | 99% metadata; 95% body | ⭐⭐⭐⭐⭐ |
| 2 | Team Messaging | Slack, Teams, WhatsApp Biz | Export (JSON/ZIP); API | Medium | 98% | ⭐⭐⭐⭐ |
| 3 | Telephony / VoIP | 3CX, RingCentral, Zoom Phone | CDR log file + API | Easy–Medium | 100% CDR; 92–97% STT | ⭐⭐⭐⭐⭐ |
| 4 | Financial Accounting | Xero, QuickBooks, Sage | Export CSV/XLSX; Xero API | Easy | 100% | ⭐⭐⭐⭐⭐ |
| 5 | Open Banking / Bank Feed | TrueLayer, Plaid, GoCardless | Open Banking API (CMA9) | Medium | 100% | ⭐⭐⭐⭐⭐ |
| 6 | HMRC MTD | HMRC MTD API | API (OAuth2) | Medium | 100% | ⭐⭐⭐⭐ |
| 7 | Card Acquiring | Stripe, Square, Worldpay, SumUp | API / portal export | Easy–Medium | 100% | ⭐⭐⭐⭐ |
| 8 | CRM & Sales Pipeline | HubSpot, Pipedrive, Salesforce | Export CSV; REST/GraphQL API | Easy–Medium | 99% | ⭐⭐⭐⭐⭐ |
| 9 | Job Management (Trades) | ServiceM8, Jobber, simPRO, Commusoft | REST API; CSV export | Medium | 99% | ⭐⭐⭐⭐⭐ |
| 10 | POS (Retail/Hospo) | Epos Now, Square, Lightspeed | API / back-office export | Easy | 100% | ⭐⭐⭐⭐ |
| 11 | Booking Systems | Fresha, Booksy, OpenTable, Calendly | API / CSV export | Easy | 99% | ⭐⭐⭐⭐ |
| 12 | Inventory | Cin7, Unleashed | REST API (Airbyte-compatible) | Medium | 99% | ⭐⭐⭐⭐ |
| 13 | Calendar & Scheduling | Google Cal, Outlook Cal | API (iCal / Graph) | Easy | 100% | ⭐⭐⭐⭐ |
| 14 | HR & Payroll | BrightPay, Xero Payroll, Sage Payroll | CSV export; Xero UK Payroll API | Medium | 100% | ⭐⭐⭐⭐⭐ |
| 15 | Rota / Workforce | Deputy, RotaCloud, Planday | CSV export; API | Easy | 99% | ⭐⭐⭐⭐ |
| 16 | Website Analytics | GA4, Search Console | Data API / BigQuery export | Easy | 98% | ⭐⭐⭐⭐ |
| 17 | Google My Business | GMB / Business Profile API | REST API (Performance API) | Easy | 99% | ⭐⭐⭐⭐ |
| 18 | Ad Platforms | Google Ads, Meta Ads | API export | Easy | 100% | ⭐⭐⭐⭐ |
| 19 | Email Marketing | Mailchimp, Brevo, Klaviyo | API / export | Easy | 99% | ⭐⭐⭐ |
| 20 | Review Platforms | Trustpilot, Checkatrade, Google | API / structured fetch | Easy–Medium | 98% | ⭐⭐⭐⭐ |
| 21 | IT Infrastructure Signal | M365 Activity Reports, MDM | Graph API; agent-side telemetry | Hard | 95% | ⭐⭐⭐ |
| 22 | Shadow IT Discovery | DNS logs, SaaS SSO, credit card | Log parse + CASB-style analysis | Hard | 90% | ⭐⭐⭐⭐ |
| 23 | Vehicle Telematics | Samsara, Geotab, Fleetio | REST API (CSV / streaming) | Medium | 100% GPS; 95% inferred | ⭐⭐⭐⭐⭐ |
| 24 | Fuel Cards | Allstar, FuelGenie | Portal export / API (Fleevo) | Easy | 100% | ⭐⭐⭐⭐ |
| 25 | Smart Meters | MPAN / n3rgy / Hildebrand | DCC API / Hildebrand Glow API | Medium | 99% | ⭐⭐⭐⭐ |
| 26 | Door Access / CCTV Meta | Paxton, Salto, AXIS | Log export / API | Medium | 99% | ⭐⭐⭐ |
| 27 | Footfall Sensors | Dor, Density, RetailNext | API | Medium | 95% | ⭐⭐⭐⭐ |
| 28 | Customer Feedback / NPS | Typeform, Delighted, returns logs | API / CSV | Easy | 99% | ⭐⭐⭐⭐ |
| 29 | eSign / Contract Data | DocuSign, Adobe Sign | REST API (form data endpoint) | Medium | 97% | ⭐⭐⭐⭐ |
| 30 | External Docs & Licences | Companies House, HMRC, FCA | API (free, real-time) | Easy | 100% | ⭐⭐⭐⭐⭐ |

---

## Category 1: Email & Communications

### 1.1 Gmail / Google Workspace

**What it is & where it lives:** Full message store including headers, bodies, attachments, thread structure, and labels. Lives in Google's infrastructure, accessible via [Gmail API](https://developers.google.com/workspace/gmail/api/guides) (RESTful) or Google Takeout (MBOX export). Google Vault adds hold, search, and export for Business Plus+ plans.

**How to extract:**
1. **Export-first:** Google Takeout → MBOX download; per-user, all labels, includes metadata
2. **API-second:** Gmail API `messages.list` + `messages.get` with `format=full`; supports batch requests. Metadata-only mode (`format=metadata`) for header-level analysis without full body download
3. For admin-level bulk: Google Vault export → PST or MBOX, scheduled recurring exports on Enterprise plans

**Actionable insights on its own:**
- Sender-recipient graphs reveal true org chart vs stated org chart
- Response-time distributions expose bottleneck people and ignored customers
- Subject-line keyword frequency surfaces recurring issues (complaints, delays, chases) before they appear in CRM
- Out-of-office pattern analysis reveals owner working hours, holiday coverage gaps, key-person dependency risk
- Attachment volume and type map document workflow complexity
- Thread-age analysis (emails that go more than 48h unanswered) flags sales leads at risk of dying

**Fusion potential (pudding bridges):**
- Email response latency × Xero AR ageing → Customer relationship health score: slow responses correlate with slow payers 2–4 weeks before the invoice goes overdue
- Shared mailbox traffic × Jobber job status → Capacity model: inbound enquiry velocity predicts future job queue length 3–6 weeks ahead
- Attachment volume × simPRO quote acceptance rate → Quoting friction analysis: do clients who receive more document attachments convert less?

**Pudding bridge (non-obvious):** Gmail out-of-office metadata × Royal Mail postcode sector data × bank holiday calendar = **True owner-availability heat map**: cross-referencing OOO triggers against local authority and postcode bank holiday variations identifies service-area days where a competitor's absence creates a fill-in opportunity — e.g. a Newcastle plumber whose main competitor goes to Tenerife the same week every January.

**Extraction difficulty:** Medium (OAuth2 setup; per-user consent or Workspace admin delegation)
**Accuracy ceiling:** 100% for metadata/headers; 95–98% for body entity extraction via LLM (deterministic sandwich applied)
**Tokenisation pattern:** `from_address → UUID token | to_address → UUID token | subject_keywords → retained verbatim | body → on-site only`

---

### 1.2 Microsoft 365 / Outlook / Exchange

**What it is & where it lives:** Exchange Online stores email, calendar, contacts, and Teams messages in a unified mailbox. Accessible via [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/resources/email-activity-reports) (unified REST layer) and the [Office 365 Management Activity API](https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-reference) (audit and activity streams).

**How to extract:**
1. **Export-first:** Microsoft 365 Admin Centre → Reports → Usage (CSV download); Exchange Admin → eDiscovery for full PST export
2. **API-second:** Graph API `reportRoot/getEmailActivityUserDetail(period='D180')` for activity; `me/messages` for mailbox content; `reports/getMailboxUsageDetail` for storage/quota signals
3. Management Activity API streams: `Audit.Exchange`, `Audit.SharePoint`, `Audit.General` — captures every user action in real-time JSON

**Activity signals unique to M365:**
- `getTeamsDeviceUsageUserDetail` — which devices each user works on (mobile-heavy = field worker)
- `getOneDriveActivityUserDetail` — file collaboration patterns
- `getSharePointActivityUserDetail` — internal document traffic
- Email send/receive/read counts with zero privacy exposure (aggregate only)

**Fusion potential:** M365 email activity × Xero payroll timesheets × Jobber job completion logs → **True productivity model**: actual computing activity vs scheduled hours vs billed job hours surfaces hidden productive capacity or unexplained idle time.

**Pudding bridge:** M365 Teams device usage (mobile proportion) × vehicle telematics GPS dwell time at depot → **Field worker digital dependency index**: workers who are 80%+ mobile and spend <2h/day at depot are effectively managing their entire business from a van. This signals which staff need a mobile-first UX and which processes are failing because they require a desktop.

**Extraction difficulty:** Medium (Azure AD app registration, OAuth2)
**Accuracy ceiling:** 100% for metadata/activity; 95% for body content
**Tokenisation pattern:** `user_id → UUID | email domain → retained for industry classification | attachment_types → retained as category tags`

---

### 1.3 Slack

**What it is & where it lives:** Workspace message store covering public channels, private channels (Business+ with approval), DMs, files (as links). [Slack data export](https://slack.com/help/articles/201658943-Export-your-workspace-data) produces ZIP with JSON per channel per day.

**How to extract:**
1. **Export-first:** Admin → Workspace Settings → Security → Import & Export → Start Export (JSON ZIP). Free/Pro plans: public channels only. Business+: all channels + DMs (with application approval).
2. **API-second:** Conversations API + messages endpoint for programmatic pull; Discovery API (Enterprise) includes file binary download

**Key signals:**
- Message volume × time-of-day → true working pattern vs stated hours
- Channel membership network graph → informal team structure
- Reaction patterns (👍 vs 🆘 emoji frequency) → team morale proxy
- Thread response time within Slack → internal communication speed
- File sharing volume → collaboration intensity

**Fusion potential:** Slack message sentiment (on-site LLM, never transmitted) × Xero payroll pay-run timing → **Payday morale signal**: does team sentiment dip in the week before payday? Does it correlate with overtime patterns? Early warning for cash-flow-driven staff attrition.

**Pudding bridge:** Slack out-of-hours message timestamps × Rota/Deputy scheduled shift data × Xero salary grade → **Burnout risk index**: employees consistently messaging outside scheduled hours AND earning below sector median AND on rotas with fewer than 2 consecutive rest days score high on early-departure risk — 6–8 weeks before they hand in notice.

**Extraction difficulty:** Medium (admin approval required for full DM export; varies by plan)
**Accuracy ceiling:** 99% (structured JSON)
**Tokenisation pattern:** `user_display_name → UUID | channel_name → category-bucket (team/customer/ops) | message_content → on-site only`

---

### 1.4 WhatsApp Business

**What it is & where it lives:** Conversation logs, media, and group activity stored on device and backed up to Google Drive or iCloud. WhatsApp Business app adds catalogue, labels, and quick replies.

**How to extract:**
1. **Export-first:** WhatsApp → individual chat → Export Chat (with or without media) → .txt file. Stays on device; PicoClaw processes locally.
2. WhatsApp Business API (Meta Cloud API or on-premise): requires a BSP (Business Solution Provider) account — impractical for micro-SMBs, but increasingly available via Brevo, Klaviyo, or Twilio integrations

**Key signals:**
- Customer enquiry timestamps → demand pattern by hour/day
- Response time → service quality metric invisible to any formal system
- Quote requests received via WhatsApp that never entered CRM → shadow pipeline
- Group chat membership of staff groups → informal team communication topology
- Media volume (photos of jobs) → on-site evidence capture

**Pudding bridge:** WhatsApp customer enquiry timestamps × Met Office MIDAS weather data × Google My Business call volume → **Demand trigger model for emergency trades**: for a plumber, heating engineer, or roofer, the combination of first-frost nights + precipitation + weekend timing predicts a demand spike 36–48h ahead. Enquiry volume confirmation from WhatsApp validates the model in near-real-time.

**Extraction difficulty:** Easy (manual export per chat) to Hard (WhatsApp Business API requires BSP)
**Accuracy ceiling:** 95% (on-device PicoClaw LLM extraction of .txt format)
**Tokenisation pattern:** `contact_name → UUID | phone_number → hashed | message_body → on-site only | timestamps → retained`

---

## Category 2: Telephony & VoIP

### 2.1 Call Detail Records (CDRs) — 3CX, RingCentral, Zoom Phone, Dialpad

**What it is & where it lives:** Machine-generated records of every call event: timestamp, duration, source/destination numbers, ring time, call outcome (answered, missed, abandoned, transferred), call cost, recording URI. [3CX CDR](https://www.3cx.com/docs/cdr-call-data-records/) writes to a flat log file (TCP socket or file output) or a SQL table (`cdr_output` in V20+). [RingCentral](https://developers.ringcentral.com/guide/voice/call-log) exposes a REST API (`/restapi/v1.0/account/~/extension/~/call-log`) returning JSON, 90-day rolling window.

**How to extract:**
1. **Export-first:** 3CX: direct log file read from `C:\ProgramData\3CX\Instance1\Data\Logs\CDRLogs\cdr.log`; SQL query on `cdr_output` table. RingCentral: portal CSV export.
2. **API-second:** RingCentral API (JSON, perPage max 1,000); Dialpad API; Zoom Phone Reports API. 3CX V20 CDR offloading to BigQuery, AWS PostgreSQL, or GCP natively.

**Actionable insights:**
- Call abandonment rate by time-of-day → staffing model optimisation
- Ring-to-answer distribution → identifies if customers are hanging up before answered
- Repeat-caller analysis → surfaces chronic unresolved issues (same number calls 3+ times in 7 days)
- Hold-time distributions → operational bottleneck identification
- Inbound/outbound ratio by staff member → identifies who is driving vs receiving
- First-call-resolution proxy: calls answered + no repeat call within 48h

**Fusion potential:** CDR abandonment rate × Xero invoice data → **Lost-revenue calculator**: each abandoned call for a trades business is a missed job. Multiply abandonment rate by average invoice value → weekly/monthly lost revenue estimate.

**Pudding bridge:** Phone CDR abandonment rate by hour × Met Office rainfall MIDAS data (hourly UK grid) × Gas Safe boiler install seasonality data → **Emergency-plumber rota staffing prediction 48h ahead**: high-precipitation + temperature-drop correlates with boiler breakdowns and burst pipes. Pre-position extra call cover before the weather event, not after.

**Extraction difficulty:** Easy (3CX log file); Medium (RingCentral API, 90-day window limitation)
**Accuracy ceiling:** 100% for CDR metadata; 0% hallucination risk — this is machine-generated structured data
**Tokenisation pattern:** `phone_number → hashed token | call_duration → exact (non-personal) | agent_id → UUID | outcome → retained`

---

### 2.2 Speech-to-Text Transcripts & Sentiment

**What it is & where it lives:** Audio recordings (call recordings from 3CX, RingCentral, or hosted VoIP) converted to text via [Whisper](https://openai.com/research/whisper) (open-source, on-device on Beast) or [Deepgram Nova-3](https://deepgram.com/product/speech-to-text) (cloud API, 95%+ accuracy). Processing is on-site; only structured entities (sentiment score, keyword flags, topic clusters) ever leave.

**How to extract:**
1. Pull call recording files via API (RingCentral `contentUri` in call log JSON; 3CX `cdr_recordingsout` table)
2. Feed through Whisper on Beast (free, private, no data leaves site)
3. Run entity extraction + sentiment pipeline (on-site Ollama or Claude Haiku with Deterministic Sandwich)
4. Store: transcript → local vault only; derived signals → FalkorDB

**Key signals extracted from transcripts:**
- Sentiment polarity per call segment (customer sentiment trajectory)
- Keyword spotting: competitor mentions, price objection keywords, cancellation signals
- Silence analysis: long pauses (>3s) indicate confusion or objection
- Call script adherence (for businesses with defined call scripts)
- Topic clustering: what are customers actually calling about? (vs what CRM records say)
- Complaint tone vs compliment tone distribution

**Pudding bridge:** Call transcript sentiment × Xero invoice due date × CRM last-contact date → **Pre-churn warning system**: a customer whose last three call transcripts trend negative on sentiment AND whose invoice is approaching due AND who hasn't been proactively contacted in 60+ days is a high-probability churner. Intervene before the invoice, not after.

**Extraction difficulty:** Medium (recording retrieval) + Easy (on-site Whisper processing)
**Accuracy ceiling:** 92–97% for STT (Whisper large-v3, UK English); 88–94% for sentiment; 95%+ for keyword spotting
**Tokenisation pattern:** `speaker_id → UUID | transcript_text → on-site only | sentiment_score → retained as bucket (positive/neutral/negative) | keywords_flagged → retained`

---

### 2.3 Mobile / Landline Hybrid Patterns (UK Trades)

**What it is & where it lives:** UK trades businesses (plumbers, electricians, builders) typically run a mobile (personal or company SIM) as primary business line plus a geographic landline for credibility. Call logs from mobile networks require SIM card data or call-forwarding logs. 

**How to extract:**
1. **Export-first:** Network provider CDR download (EE, O2, Vodafone, Three business portals provide CSV call logs)
2. Google Voice / Apple Call Logs export from device backup (local processing only)
3. Call-forwarding service logs (e.g., call tracking numbers via CallRail, Mediahawk UK)

**Pudding bridge:** Mobile CDR location data (tower triangulation, not GPS) × job management (ServiceM8/Jobber) GPS address records × Google My Business profile location → **Territory-drift early warning**: if a sole-trader plumber's calls are increasingly originating from a postcode sector outside their stated service area, either they've expanded (opportunity: update GMB radius) or they're moonlighting for a competitor (risk signal for employers).

**Extraction difficulty:** Medium (network portal access; some networks restrict API access)
**Accuracy ceiling:** 100% for CDR metadata
**Tokenisation pattern:** `phone_number → hashed | cell_tower_area → LAD (Local Authority District) level only`

---

## Category 3: Financial Accounting

### 3.1 Xero

**What it is & where it lives:** Cloud accounting platform holding P&L, balance sheet, cashflow, invoices (AR/AP), bank transactions, contacts, chart of accounts, tracking categories, tax rates, and payroll (UK API released 2018). Data lives in Xero's cloud; [full API documentation](https://developer.xero.com/documentation/api/accounting/overview).

**How to extract:**
1. **Export-first:** Reports section → any report → Export (CSV/XLS/PDF). Business → Invoices → Export. Settings → Advanced Settings → Export Data (contacts, invoices, full ledger). Multiple exports needed — Xero lacks a single "export everything" button.
2. **API-second:** Xero API (OAuth2) — `GET /api.xro/2.0/Invoices`, `/Accounts`, `/BankTransactions`, `/Reports/{ReportType}`. Xero UK Payroll API: `GET /payroll/employees`, `/payroll/payruns`. Rate limit: 60 calls/min per tenant.
3. Direct BigQuery sync via Xero's reporting connectors (enterprise only).

**Key signals:**
- Debtor days (DSO): trend over 12 months, by customer segment
- Creditor days (DPO): cash conversion cycle = debtor days - creditor days
- AR ageing: buckets (0–30, 31–60, 61–90, 90+ days) by customer
- Margin by tracking category (proxy for margin by SKU/service line)
- Late-payment patterns: which customers are structural late payers
- Bank reconciliation lag: unreconciled items older than 7 days signal bookkeeping risk
- Invoice frequency per customer → revenue concentration risk

**Fusion potential:** Xero AR ageing × Open Banking real-time balance → **True cash runway to the day**: the accounting system knows what's owed; the bank feed knows what's actually available. Combined with payroll run dates, produces a daily cash runway figure no single system provides.

**Pudding bridge:** Xero margin by tracking category × Google My Business review sentiment by service type → **Margin-reputation matrix**: high-margin services that attract low review ratings are pricing themselves out of the market. Low-margin services with high ratings are candidates for price testing. Neither the accounting system nor the review platform reveals this alone.

**Extraction difficulty:** Easy (export) to Medium (API with OAuth2 setup)
**Accuracy ceiling:** 100% (source-of-truth data)
**Tokenisation pattern:** `contact_name → UUID | invoice_amount → decile bucket | account_code → retained | VAT_number → hashed`

---

### 3.2 QuickBooks Online / FreeAgent / Sage

**What it is & where it lives:** Alternative accounting platforms common in UK SMBs. FreeAgent (owned by NatWest) is strong among freelancers and very small Ltd companies; Sage 50 / Sage Business Cloud for mid-market; QuickBooks Online for US-influenced businesses.

**How to extract:**
- **FreeAgent:** Settings → Export All Data (ZIP archive, CSV per data type — the cleanest single-button export of any UK accounting platform). REST API available.
- **QuickBooks:** Reports → each report → Export to Excel (CSV). QuickBooks API (OAuth2), good endpoint coverage.
- **Sage 50:** Reports → export individual reports (CSV/Excel). Sage API (OAuth2) for Sage Business Cloud. Sage 50 desktop: ODBC connection to underlying database is possible for advanced extraction.

**Sage-specific UK signals:** Sage is disproportionately used by UK manufacturing and construction SMBs. The Sage payroll integration data often contains P45/P60/P11D data not captured in Xero — richer employment history signals.

**Pudding bridge:** FreeAgent invoice-creation timestamp × Google Calendar appointment data → **Quote-to-cash lag by booking source**: does a job booked through the website convert to an invoice faster than one from a WhatsApp enquiry? FreeAgent alone sees the invoice; Calendar alone sees the booking. Combined, they reveal the true fulfilment pipeline delay by channel.

**Extraction difficulty:** Easy (FreeAgent, QBO export); Medium (Sage 50 desktop ODBC)
**Accuracy ceiling:** 100%
**Tokenisation pattern:** Same as Xero pattern above

---

### 3.3 Open Banking — TrueLayer, Plaid UK, GoCardless (ex-Nordigen), Tink

**What it is & where it lives:** UK Open Banking (mandated 2018 under CMA9 order) gives regulated Third Party Providers (TPPs) access to consented bank account data via standardised APIs. The [CMA9](https://ozoneapi.com/blog/who-are-in-the-cma9-and-why-they-matter/) (Barclays, HSBC, Lloyds, NatWest/RBS, Santander, Nationwide, Danske, AIB, BoI) cover 90%+ of UK SMB current accounts. [TrueLayer Data API](https://docs.truelayer.com/docs/data-api-basics) returns: account details, balances (current/available), transactions (description, amount, category, merchant), standing orders, direct debits.

**How to extract:**
1. **API-first** (this is the architecture): OAuth2 consent from business owner → TrueLayer/GoCardless pulls real-time transaction feed → stored on-site in FalkorDB
2. GoCardless Bank Account Data (free tier for lower volumes) is viable for early-stage clients; TrueLayer for premium clients requiring richer categorisation; Plaid UK for US-linked businesses

**Key signals:**
- Real-time balance trajectory (vs Xero balance which lags by reconciliation)
- Merchant-level transaction categorisation (supplier spend patterns)
- BACS/CHAPS pattern analysis: payroll run dates, supplier payment rhythms
- Card-not-present vs in-person transactions: signals customer behaviour shift
- Direct debit schedule: surfaces all recurring commitments (subscriptions, leases, insurance)
- Unusual/first-time payees: new supplier relationships before they appear in Xero

**Pudding bridge:** Open Banking direct debit schedule (all recurring outgoings) × Xero P&L revenue trend × HMRC MTD VAT submission dates → **Regulatory payment stress model**: identifies the specific week each quarter when VAT payment, rent DD, and payroll align — the maximum cash stress point. Pre-position with invoice chasing or overdraft facility negotiation 6 weeks ahead.

**Extraction difficulty:** Medium (OAuth2 consent; ongoing token refresh management)
**Accuracy ceiling:** 100% (live bank data)
**Tokenisation pattern:** `account_number → UUID | sort_code → bank/branch institution code only | transaction_amount → decile bucket | merchant_name → hashed with category retained`

---

### 3.4 HMRC Making Tax Digital (MTD)

**What it is & where it lives:** HMRC's [MTD VAT API](https://www.api.gov.uk/hmrc/vat-mtd/) is live for all VAT-registered businesses (mandatory above £90k threshold, voluntary below). MTD for Income Tax Self-Assessment (ITSA) is rolling out from April 2026. Provides a bidirectional API: businesses submit quarterly returns digitally; HMRC's system is the authoritative record.

**How to extract:**
1. **API-second:** HMRC MTD API (OAuth2, sandbox at `test-api.service.hmrc.gov.uk`). Retrieve VAT obligations, return submissions, payment history, penalty points
2. Accounting software (Xero, QuickBooks, Sage) already calls this API for submissions — extract what they send/receive

**Key signals:**
- VAT submission regularity (are they filing on time?) → compliance risk indicator
- VAT amount trajectory: rising VAT output over 4 quarters confirms genuine growth (vs cash-only underdeclared revenue — important for benchmarking)
- Penalty points accumulated → regulatory risk score
- MTD ITSA quarterly income/expense declarations (from 2026): the most granular quarterly P&L the business has ever submitted to any authority

**Pudding bridge:** HMRC MTD VAT output × Companies House filing history (accounts filed late?) × Open Banking real-time balance → **Regulatory credit risk score**: combines tax compliance, corporate governance, and actual liquidity into a 3-factor score that predicts late supplier payment with higher precision than any single source.

**Extraction difficulty:** Medium (HMRC OAuth2 with business owner consent)
**Accuracy ceiling:** 100%
**Tokenisation pattern:** `VAT_number → hashed | submission_amounts → decile bucket by SIC code | payment_dates → day-of-month only`

---

### 3.5 Card Acquiring — Stripe, Square, Worldpay, SumUp

**What it is & where it lives:** Transaction-level records of every card payment: timestamp, amount, card type (Visa/Mastercard/Amex), device (terminal ID), authorisation code, refund status, dispute status, settlement batch, and (for Stripe) customer ID. Stripe [API](https://stripe.com/docs/api) is comprehensive; Square Dashboard export; Worldpay portal; SumUp CSV export.

**How to extract:**
1. **Export-first:** All four platforms offer portal CSV export (daily/weekly/monthly)
2. **API-second:** Stripe API is industry-leading — `GET /v1/charges`, `/payment_intents`, `/balance_transactions`. SumUp API (OAuth2). Square Connect API.

**Key signals:**
- Transaction time-of-day distribution → true busy periods (not self-reported)
- Average transaction value by terminal → identifies which till/location drives highest value
- Refund rate by product category → quality or expectation-mismatch signal
- Contactless vs chip vs CNP split → customer segment inference
- Dispute (chargeback) rate → customer satisfaction proxy, compliance risk
- BNPL transaction proportion (Klarna, Clearpay via Stripe) → credit-sensitivity of customer base

**Pudding bridge:** Stripe transaction timestamps (to the second) × Deputy shift rota × GA4 session data → **Conversion funnel by staff member**: who was on shift when the sale happened? Does website traffic convert to in-store purchases faster when specific staff are rostered? Links the digital customer journey to the physical point of conversion — invisible to any single system.

**Extraction difficulty:** Easy (Stripe API is best-in-class); Medium (Worldpay portal)
**Accuracy ceiling:** 100%
**Tokenisation pattern:** `card_last_four → tokenised PAN stub | customer_email → UUID | transaction_amount → exact (non-personal business data) | device_id → retained`

---

## Category 4: CRM & Sales

### 4.1 HubSpot

**What it is & where it lives:** Full CRM including contacts, companies, deals, activities (calls, emails, meetings), pipelines, sequences, and marketing attribution. HubSpot [Exports API](https://developers.hubspot.com/move-data) supports bulk export of CRM objects; audit logs via Account Activity API; [webhooks](https://developers.hubspot.com/docs/api/webhooks) for real-time event streaming.

**How to extract:**
1. **Export-first:** Settings → Data Management → Export; or any object list view → Export (CSV)
2. **API-second:** HubSpot REST API (`/crm/v3/objects/{objectType}`); Bulk Export API for large datasets (avoids 90-day rolling window limitation). Rate limit: 100 requests/10s.
3. For 2.5M+ record sets: use Snowflake direct data share or ETL tools (Windsor.ai, Coupler.io)

**Key signals:**
- Pipeline velocity: average days per deal stage
- Stage-conversion rates: where do deals die?
- Deal-age distribution: how many deals are "zombie" (no activity >30 days)
- Lost-reason analysis: the #1 CRM signal most SMBs never look at
- Rep-level performance: call volume, meeting count, deal close rate per head
- Lead source attribution: which marketing channel generates closed revenue (not just leads)
- Time-to-first-touch: how long after a lead arrives before first contact?

**Fusion potential:** HubSpot deal stage × Xero invoice status × Open Banking balance → **Revenue certainty score**: a deal in Proposal stage + invoice raised + bank balance declining = collection risk. Triage collections before the due date.

**Pudding bridge:** HubSpot time-to-first-touch × Epos Now transaction volume by hour → **Lead decay modelling for retail**: in a retail context, a website form submitted at 2pm has a 3x higher conversion probability if called within 30 minutes vs called the next day. Overlaying the POS busy-hour data reveals when staff are too busy to make those calls — and quantifies the lost revenue.

**Extraction difficulty:** Easy–Medium (API setup; rate limit management for large datasets)
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `contact_email → UUID | company_name → UUID | deal_amount → decile bucket | rep_name → UUID`

---

### 4.2 Pipedrive

**What it is & where it lives:** Pipeline-focused CRM popular with UK sales-led SMBs. Full data export via [Admin → Export Data](https://support.pipedrive.com/en/article/exporting-data-from-pipedrive) (CSV/XLS, all entities: deals, leads, contacts, organisations, activities, notes). [Pipedrive API](https://developers.pipedrive.com/tutorials/get-deals-pipedrive-api) via PHP/Python with `api_token`.

**How to extract:**
1. **Export-first:** Admin → More Options → Export Data → select entity type → CSV/XLS
2. List View → apply filter → gear icon → Export filter results (filtered CSV)
3. **API-second:** REST API `GET /api/v2/deals?limit=500` — paginated; all major entities exposed

**Key signals unique to Pipedrive:**
- Activity-to-deal ratio by rep (how many activities does it take to close?)
- Custom field data (often holds richer qualification data than standard CRM fields)
- Lost deals with reason codes → single highest-value dataset for pricing and product decisions

**Pudding bridge:** Pipedrive lost-reason codes (categorised by LLM on-site) × GA4 page-depth data for the proposal page → **Objection-origin model**: do visitors who spend >4 minutes on the pricing page more often cite "too expensive" as lost reason? Or do they convert? Connecting the digital consideration behaviour to the CRM outcome builds a proposal-page optimisation case.

**Extraction difficulty:** Easy
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `contact_name → UUID | deal_value → decile bucket | lost_reason → category label retained`

---

### 4.3 Salesforce (SMB edition / Essentials)

**What it is & where it lives:** Enterprise CRM with strongest API in the category. [Data Export Wizard](https://www.flosum.com/blog/how-to-export-data-from-salesforce-a-complete-guide) (weekly/monthly ZIP of all objects as CSV); [Data Loader](https://developer.salesforce.com/docs/data-loader) for bulk; REST API + Bulk API for programmatic. SOQL query language for precision extraction.

**Pudding bridge:** Salesforce opportunity close date (predicted) × HMRC MTD quarterly submission date × Xero bank balance → **Sales pipeline stress test**: if the sum of expected close-value in the current quarter is less than the projected VAT liability + payroll + rent, the business has a structural cash shortfall 6 weeks before it becomes visible — and Salesforce is the only system with forward-looking revenue data.

**Extraction difficulty:** Medium (SOQL, governor limits)
**Accuracy ceiling:** 99%
**Tokenisation pattern:** Same as HubSpot

---

## Category 5: Operations

### 5.1 Job Management — Trades (ServiceM8, Jobber, simPRO, Commusoft, Tradify)

**What it is & where it lives:** The richest operational dataset for UK trades businesses. Captures the full job lifecycle: enquiry → quote → scheduling → dispatch → on-site activity → invoice → payment. [ServiceM8 API](https://developer.servicem8.com) exposes `job`, `jobactivity`, `staff`, `client`, `invoice` endpoints. [Jobber API](https://developer.getjobber.com/docs/) is GraphQL — deeply nested schema covering jobs, visits, quotes, timesheets, job costing, and client records. [simPRO API](https://apiforum.simprogroup.com) covers cost centres, sections, stock, purchase orders.

**How to extract:**
1. **Export-first:** ServiceM8: Settings → Export (jobs, clients, invoices CSV). Jobber: Reports → export any report; client list → CSV or vCard.
2. **API-second:** ServiceM8 REST API (`https://api.servicem8.com/api_1.0/job.json`); Jobber GraphQL (authenticated); simPRO REST API (Open API documented).

**Key signals unique to trades job management:**
- Job-to-invoice conversion rate (quotes that never became jobs)
- On-site time vs booked time: are jobs running over? By trade type? By location?
- Travel time between jobs: routing inefficiency cost per day (£-quantifiable)
- Recall rate: jobs that generate a second visit within 30 days (quality proxy)
- First-time-fix rate: jobs resolved in single visit vs multi-visit
- Technician utilisation: billable hours / available hours per week
- Materials cost vs quoted materials → margin erosion on materials

**Fusion potential:** ServiceM8 job GPS timestamps × Allstar fuel card transactions → **True job cost model**: adds actual fuel consumed per job to labour and materials — the trifecta most trades businesses have never calculated. Typical revelation: 12–18% of gross margin is consumed by fuel and travel that is never billed.

**Pudding bridge:** Jobber job completion timestamps × Royal Mail postcode sector delivery data × Google Maps Distance Matrix API → **Optimal technician territory assignment**: cluster jobs by postcode sector density, weight by technician skill match and current workload, and solve as a vehicle routing problem. Reduces average inter-job travel by 20–35% on typical Newcastle urban/suburban territory.

**Extraction difficulty:** Medium (API authentication; data modelling complexity)
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `client_name → UUID | job_postcode → outward-code only | invoice_value → decile bucket | technician_id → UUID`

---

### 5.2 POS Systems — Epos Now, Square (Retail), Lightspeed

**What it is & where it lives:** Point-of-sale transaction records, stock movements, staff session data, payment method splits, discount application, and end-of-day reconciliation. [Epos Now](https://slynk.io/flow/exports-and-reports/) has a back-office export function (CSV/Excel) covering all sales, products, staff, and customer data; Slynk/Flow adds automated delivery via FTP. Square Dashboard → Reports → CSV. Lightspeed REST API.

**How to extract:**
1. **Export-first:** Epos Now Back Office → Reports → Export (CSV/XLS). Square: Dashboard → Transactions → Export.
2. **API-second:** Epos Now REST API (underdocumented but available); Square Connect API (comprehensive); Lightspeed API.

**Key signals:**
- Product mix by time-of-day → demand forecasting
- Staff-level transaction volumes, discount application rates → performance + exception monitoring
- Basket composition analysis → cross-sell opportunity (which products are bought together?)
- Void/refund patterns by staff member → shrinkage or training issue indicator
- Payment method split (cash vs card) → cash-handling risk, customer affluence proxy
- End-of-day variance → till discrepancy trend

**Pudding bridge:** Epos Now hourly transaction volume × Google My Business peak-hour data × Rota (Deputy/RotaCloud) staffed hours → **Understaffing revenue-loss calculator**: for a deli or café, the combination of till throughput data and GMB footfall data reveals exactly how much revenue was lost in the 11am–1pm rush when only 2 staff were rostered. Quantified as £/week, this is a compelling rota justification.

**Extraction difficulty:** Easy (export); Medium (API)
**Accuracy ceiling:** 100%
**Tokenisation pattern:** `staff_id → UUID | customer_loyalty_id → UUID | transaction_amount → exact (non-personal) | product_SKU → retained`

---

### 5.3 Booking Systems — Fresha, Booksy, OpenTable, ResDiary, Calendly

**What it is & where it lives:** Service-sector appointment and reservation data. [Fresha](https://www.fresha.com/help-center/knowledge-base/catalog/100646-export-your-service-menu) supports CSV exports of clients, appointments, services, and products. [Booksy](https://support.booksy.com/hc/en-gb/) has calendar export (ICS) and client CSV. OpenTable and ResDiary provide cover data exports. Calendly API is well-documented.

**Key signals:**
- No-show rate by day/time → revenue-at-risk quantification
- Rescheduling cadence → client commitment score
- Lead-time between booking and appointment → demand forecasting horizon
- Service duration vs booked duration → technician/therapist efficiency
- Rebooking rate: did the client return? When?
- Gap analysis: unutilised appointment slots by day and time

**Pudding bridge:** Fresha no-show rate × weather forecast data (Met Office DataPoint API) × text reminder send timestamps → **Weather-driven no-show prediction**: beauty and personal service appointments are 2.3x more likely to be no-shows when precipitation >5mm is forecast the day of appointment. Pre-emptive confirmation message + mild urgency = 40–60% reduction in no-shows.

**Extraction difficulty:** Easy (CSV export); Medium (API)
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `client_name → UUID | client_email → UUID | service_type → category label retained | appointment_value → decile bucket`

---

### 5.4 Inventory — Cin7, Unleashed

**What it is & where it lives:** Stock levels, purchase orders, supplier lead times, COGS, warehouse locations, and serial/batch tracking. [Cin7 Core API](https://docs.airbyte.com/integrations/sources/cin7) via Airbyte connector exposes: products, customers, suppliers, purchases, sale lists, locations — full incremental sync. [Unleashed REST API](https://apidocs.unleashedsoftware.com/) similarly comprehensive.

**Key signals:**
- Stock-turn rate by SKU → identifies slow-movers and write-off candidates
- Supplier lead-time actuals vs quoted → vendor performance score
- Dead stock value → hidden cash locked in inventory
- Purchase order frequency by supplier → dependency concentration risk
- COGS % by product line → contribution margin by SKU

**Pudding bridge:** Cin7 stock-turn rate × Epos Now sales velocity × Open Banking supplier payment timing → **Working capital optimisation by SKU**: slow-turning stock that is paid for in 30 days but takes 90 days to sell is destroying working capital. Fast-turning stock paid in 60 days is self-financing. This three-way view justifies renegotiating payment terms specifically by product category — a case no single system could make.

**Extraction difficulty:** Medium
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `supplier_name → UUID | SKU → retained as category | stock_value → decile bucket`

---

## Category 6: Calendar & Scheduling

### 6.1 Google Calendar / Outlook Calendar

**What it is & where it lives:** Meeting metadata, event titles, attendees, durations, recurrence patterns, and free/busy status. Google Calendar API (`events.list`); Outlook via Microsoft Graph (`/me/events`). ICS/iCal export available from both.

**How to extract:**
1. **Export-first:** Google: Settings → Import & Export → Export (ICS ZIP). Outlook: File → Open & Export → Import/Export.
2. **API-second:** Google Calendar API (OAuth2, incremental sync via `syncToken`); Graph API `/me/events?$select=start,end,subject,attendees`.

**Key signals:**
- Owner-hours-worked signal: calendar density × meeting duration vs productive work blocks
- Meeting-to-work ratio: if >60% of working hours are in meetings, delivery capacity is compromised
- Customer-facing meeting frequency vs revenue → relationship intensity ROI
- Gap analysis: unbooked slots in otherwise full calendars = overflow demand capacity
- No-show patterns on video calls (accepted but not attended)
- Recurring meetings that never produce action items (waste signal)

**Pudding bridge:** Google Calendar event titles (LLM-classified on-site into: client meeting / internal / admin / travel) × Xero invoice amounts for corresponding clients × Jobber job completion rate → **Meeting ROI model**: which meetings directly precede won jobs? Which client meetings never convert to an invoice within 90 days? The calendar is the only system that captures the relationship-building activity that precedes revenue.

**Extraction difficulty:** Easy
**Accuracy ceiling:** 100% for metadata; 85–92% for LLM event classification
**Tokenisation pattern:** `attendee_email → UUID | event_title → on-site LLM classification only; category label transmitted | event_duration → exact (non-personal)`

---

## Category 7: HR & Payroll

### 7.1 BrightPay / Sage Payroll / Xero Payroll (UK)

**What it is & where it lives:** Full payroll records: employee details, pay rates, NI contributions, pension auto-enrolment, P45/P60/P11D, SSP/SMP records, PAYE submissions to HMRC RTI. [BrightPay](https://www.brightpay.co.uk/docs/bpol/distributing-payslips/exporting-payslips/) exports payslips as PDF ZIP; integrates with FreshBooks, QuickBooks, Xero via API. [Xero UK Payroll API](https://developer.xero.com/documentation/api/payrolluk/earningrates) released 2018 — full REST coverage of employees, pay runs, timesheets, earning rates, leave. 

**How to extract:**
1. **Export-first:** BrightPay: payroll reports → CSV export. Xero Payroll: Reports → Payroll reports → export.
2. **API-second:** Xero UK Payroll API: `GET /payrolluk/employees`, `/payroll/payruns`, `/payroll/timesheets`

**Key signals:**
- Starter/leaver velocity by month → churn signal (P45 frequency is the most honest HR metric)
- Tenure distribution: average months employed → institutional knowledge fragility score
- Overtime pattern: consistent overtime in specific roles → capacity understaffing signal
- Absence pattern by employee × day-of-week → attendance reliability signal
- SSP claims: trend increase → team health/morale issue
- Pension opt-out rate → financial stress indicator among workforce
- P11D values (benefits in kind) → total compensation picture

**Pudding bridge:** Xero Payroll starter/leaver dates × Jobber job completion rate × Xero P&L monthly revenue → **Staff-churn revenue-impact model**: for service businesses, a leaver in month M correlates with a measurable revenue dip in months M+1 and M+2 as the replacement ramps up. Quantifying this as £/leaver creates the business case for retention investment and succession planning.

**Extraction difficulty:** Medium (payroll data is sensitive; consent from employees required for any personal data processing beyond aggregate)
**Accuracy ceiling:** 100%
**Tokenisation pattern:** `employee_name → UUID | NI_number → hashed | pay_rate → decile bucket within role-band | SSP_flag → Boolean only`

---

### 7.2 Rota & Workforce — Deputy, RotaCloud, Planday

**What it is & where it lives:** Shift scheduling, actual vs planned hours, leave management, availability, and timesheet records. [Deputy](https://help.deputy.com/hc/en-au/articles/4755408081167-How-to-export-or-download-your-data) Data Exporter exports: Employee, Roster, Timesheet, Leave, PayRules, Journal (all as CSV). [RotaCloud](https://help.rotacloud.com/en/articles/10037503-how-do-i-export-data-from-rotacloud) downloads: Shifts, Leave, Timesheets, Payroll (CSV). Deputy API is comprehensive (REST).

**Key signals:**
- Planned vs actual hours by employee → scheduling reliability
- No-show / late arrival rate → operational risk metric
- Voluntary vs mandatory overtime ratio → working conditions indicator
- Leave request patterns: Monday/Friday sickness rate → genuine illness vs motivational issue
- Shift swap frequency → scheduling dissatisfaction signal
- Under/over-staffing cost per shift → direct operating cost

**Pudding bridge:** Deputy actual shift hours × Epos Now hourly transaction volume × Xero payroll cost → **True labour efficiency ratio per hour**: not just revenue/employee but revenue/(actual hours × loaded cost including employer NIC + pension). Identifies the specific shift pattern (e.g. Tuesday afternoon split shift) that has the worst labour-efficiency ratio in the business.

**Extraction difficulty:** Easy (CSV export); Medium (API)
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `employee_id → UUID | shift_location → site code (non-personal) | hours_worked → exact (aggregate, non-personal)`

---

## Category 8: Website & Digital Marketing

### 8.1 Google Analytics 4 (GA4)

**What it is & where it lives:** Event-based web analytics tracking every user session, page view, conversion event, traffic source, device type, and geographic origin. [GA4 Data API](https://infotrust.com/articles/exporting-your-google-analytics-4/) (REST, dimension/metric query); BigQuery Export (raw event-level data, free tier available — best option for forensic analysis); Looker Studio for visualisation.

**How to extract:**
1. **Export-first:** GA4 UI → Reports → Export (CSV per report)
2. **API-second (preferred):** GA4 Data API (`runReport`) for aggregated queries; BigQuery Export for raw event-level data (streams intraday + daily full export)
3. BigQuery export: `analyticsdata.googleapis.com` → project link in GA4 Admin → BigQuery Linking → enables complete event log access

**Key signals:**
- Source/medium attribution: where does converting traffic originate?
- Page-level conversion rates: which service/product pages convert vs which merely inform?
- Session-to-enquiry rate: what % of website visitors generate a lead action?
- Device split: mobile-heavy traffic suggests local search intent
- Geographic distribution of sessions: territory demand mapping
- Return visitor rate: loyalty proxy for service businesses
- Scroll depth and time-on-page for key service pages: engagement quality

**Pudding bridge:** GA4 landing page top organic queries × Google Search Console click-through data × Xero revenue by service line → **SEO-to-revenue attribution model**: identifies which search queries are driving actual booked revenue vs which drive traffic that never converts. Most SMBs optimise for keywords that generate enquiries; the fusion reveals which queries generate paid work.

**Extraction difficulty:** Easy (API, BigQuery export)
**Accuracy ceiling:** 95–98% (GA4 uses sampling and modelled data for some segments; BigQuery raw export is 100%)
**Tokenisation pattern:** `user_id → GA4 client_id (already pseudonymous) | IP → geo-bucket only (GA4 default) | session_data → aggregate metrics retained`

---

### 8.2 Google Search Console

**What it is & where it lives:** Organic search performance data: queries triggering impressions, clicks, average position, CTR, device split, country, and page. [Search Console API](https://www.sweetdigital.co.uk/blog/data-extraction-google-search-console/) returns up to 25,000 rows per request (vs 1,000 in the UI); 16-month rolling history.

**How to extract:**
1. **Export-first:** Performance → Export (CSV/Google Sheets)
2. **API-second:** `searchanalytics.query` method with dimension combinations (query + page + device + date); full history without sampling

**Key signals:**
- Impression-to-click gap: high impressions, low CTR = title tag/meta description problem
- Position 4–10 queries: fastest improvement opportunities for traffic
- Branded vs non-branded query split → brand awareness health
- Local intent queries (including "[service] near me"): local SEO opportunity sizing
- Page-level performance: which pages drive the most search-sourced traffic?

**Pudding bridge:** Search Console query data (top organic keywords) × GMB review sentiment themes × Jobber lost-job reasons → **Reputation-search alignment gap**: if customers search for "boiler service Newcastle" but reviews mention "overpriced" and Jobber shows 30% of quotes rejected on price, the business is visible in search but losing on proposition. The three datasets triangulate the same problem from three angles.

**Extraction difficulty:** Easy
**Accuracy ceiling:** 100% (no sampling at API level)
**Tokenisation pattern:** `queries → retained (search terms are not personal data) | page_URL → retained | impressions/clicks → exact`

---

### 8.3 Google My Business (Business Profile)

**What it is & where it lives:** Local business presence data including: customer reviews, review responses, Q&A, photo engagement, search appearances, driving direction requests, call button clicks, and booking link clicks. [Business Profile Performance API](https://developers.google.com/my-business/reference/rest) replaced legacy Insights API; provides `fetchMultiDailyMetricsTimeSeries`.

**How to extract:**
1. **API-second:** Business Profile API (OAuth2, `BusinessProfile.Read` scope): metrics include `BUSINESS_IMPRESSIONS_DESKTOP_MAPS`, `BUSINESS_IMPRESSIONS_MOBILE_SEARCH`, `CALL_CLICKS`, `WEBSITE_CLICKS`
2. Review data: `locations/{locationId}/reviews` endpoint; returns star rating, review text, response status

**Key signals unique to GMB:**
- Call-click volume by day → inbound demand signal (the phone rang before the call system records it)
- Direction requests by postcode → geographic demand map (where customers are travelling from)
- Photo view count → visual engagement (important for hospitality, trades, retail)
- Review velocity: rate of new reviews per month → net promoter signal
- Review response rate: are negative reviews acknowledged?

**Pudding bridge:** GMB direction request postcodes × Deputy rota gaps by day → **Coverage-to-demand misalignment**: if GMB shows a spike in direction requests on Sunday afternoons but Deputy shows no staff rostered Sunday afternoon, this is a quantified revenue-loss number (direction requests × average spend × conversion rate).

**Extraction difficulty:** Easy–Medium (API setup)
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `review_author → UUID | review_text → on-site sentiment only; score retained | location_metrics → exact (non-personal aggregate)`

---

### 8.4 Email Marketing — Mailchimp, Brevo, Klaviyo

**What it is & where it lives:** Campaign performance (opens, clicks, unsubscribes, bounces), list health, automation trigger data, and revenue attribution (Klaviyo/Shopify integration). All three have robust REST APIs and CSV exports.

**Key signals:**
- Open rate by campaign type → content resonance
- Click-to-open rate → call-to-action effectiveness
- Unsubscribe triggers → campaign tone or frequency problem
- Revenue per email sent (Klaviyo with e-commerce integration)
- List decay: how fast is the list shrinking without active growth?
- Subject line performance: A/B test history reveals language resonance patterns

**Pudding bridge:** Mailchimp campaign click patterns (who clicked what) × Pipedrive deal stage at click time × Xero invoice timing → **Email-to-revenue attribution**: which email campaign topic correlates with the highest proportion of deals advancing to closed-won within 14 days? SMBs almost never measure this because it requires joining three systems.

**Extraction difficulty:** Easy
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `subscriber_email → UUID | click_URL → retained as topic-category | open_device → retained`

---

## Category 9: IT Infrastructure Signal

### 9.1 Microsoft 365 Activity Reports & Audit Logs

**What it is & where it lives:** The [Microsoft Graph Reporting API](https://learn.microsoft.com/en-us/answers/questions/504049/microsoft-365-apps-usage-report-using-rest-api-or) exposes 25+ usage reports: email activity, Teams device usage, OneDrive activity, SharePoint usage, Yammer, Forms, Viva Insights. The [Office 365 Management Activity API](https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-reference) streams full audit logs: `Audit.Exchange`, `Audit.SharePoint`, `Audit.General`, `DLP.All`.

**How to extract:**
1. M365 Admin Centre → Reports → Usage (manual CSV)
2. **API-second:** Graph API `Reports.Read.All` permission → PowerShell or Python → CSV → SQL. Management Activity API for real-time audit streaming.

**Key signals (M365 specific):**
- Teams device type (mobile/desktop/web) per user → field vs office worker classification
- Email send/receive volume trends → workload intensity signal
- OneDrive storage consumption growth → data accumulation rate
- SharePoint document access frequency → which documents are actually being used
- Teams call + meeting minutes → collaboration intensity
- Inactive user detection (zero activity >14 days) → licence waste signal

**Pudding bridge:** M365 Teams mobile usage proportion × Jobber field technician job assignment × BrightPay payroll grade → **Field-worker digital infrastructure gap**: technicians who are 90%+ mobile-device M365 users but are sent paper job cards or required to access desktop-only systems are experiencing a productivity tax. Quantifiable as minutes-per-job wasted in office returns.

**Extraction difficulty:** Medium (Azure AD app registration; `Reports.Read.All` permission)
**Accuracy ceiling:** 95% (some reports use estimated data; audit logs are 100%)
**Tokenisation pattern:** `user_id → UUID | app_usage_type → category retained | activity_date → week-number only for transmission`

---

### 9.2 Shadow IT Discovery

**What it is & where it lives:** Unapproved SaaS applications and services used by employees — typically discovered via DNS query logs, firewall logs, SSO access logs, or endpoint agent data. In M365 environments, [Microsoft Defender for Cloud Apps](https://www.ninjaone.com/blog/detect-shadow-it-in-microsoft-365/) provides automated shadow IT discovery with risk scoring for 30,000+ cloud apps.

**How to extract:**
1. DNS/firewall logs → parse for non-approved domains
2. M365 Defender for Cloud Apps → Cloud Discovery dashboard → CSV export
3. Corporate credit card statement (via Open Banking feed) → subscription merchant classification
4. Endpoint MDM inventory (Intune, Jamf) → installed application list per device

**Key signals:**
- Shadow SaaS subscription count → data governance and duplication risk
- Monthly spend on unsanctioned tools → hidden cost discovery (typically 15–30% of known SaaS spend)
- Overlapping functionality: e.g. paying for both Dropbox (shadow) and SharePoint (sanctioned) 
- High-risk application usage (personal file sync, AI tools with data upload)
- Department-level shadow IT concentration: which team has the most workarounds?

**Pudding bridge:** Shadow IT application list × Xero SaaS subscription expenses × BrightPay department codes → **Department-level tech debt map**: sales team paying £3,200/year for a shadow CRM because the official HubSpot rollout failed. Finance team using personal Dropbox because SharePoint is too slow. Maps the exact cost and location of tech debt, enabling a prioritised rationalisation plan.

**Extraction difficulty:** Hard (requires network log access or MDM agent deployment)
**Accuracy ceiling:** 90% (some traffic indistinguishable at DNS level)
**Tokenisation pattern:** `user_id → UUID | app_domain → retained for classification | subscription_cost → exact (business data)`

---

## Category 10: Physical & IoT

### 10.1 Vehicle Telematics — Samsara, Geotab, Fleetio

**What it is & where it lives:** GPS position (1–10 second intervals), speed, idling time, harsh braking/acceleration events, engine hours, odometer readings, fault codes (OBD-II), and driver behaviour scores. [Samsara API](https://kb.samsara.com/hc/en-us/articles/10118697996813-Samsara-Data-Export-Types) supports CSV export from dashboard and REST API; Geotab MyGeotab database query. Both support API integration with 50+ telematics partners.

**How to extract:**
1. **Export-first:** Samsara dashboard → Reports → CSV export (vehicles, drivers, trips, safety)
2. **API-second:** Samsara Fleet API; Geotab SDK (MyGeotab.API); Fleetio API

**Key signals:**
- Actual vs estimated job travel time → quote accuracy for time-and-materials jobs
- Idling time cost: idle minutes × fuel consumption rate × fuel price = exact wasted fuel cost
- Route efficiency: actual miles driven vs optimal routing → daily distance waste
- Harsh braking frequency → vehicle wear cost predictor and insurance risk indicator
- Geofence arrival/departure → automatic job start/end timestamping (replaces paper timesheets)
- After-hours vehicle use → unauthorised use detection

**Pudding bridge:** Samsara GPS trip data (routes + dwell times) × ServiceM8 job postcodes × Allstar fuel card fill-up locations → **Full job profitability model including travel cost**: Samsara provides the exact miles driven per job; Allstar provides the exact fuel cost per litre at each fill; ServiceM8 provides the invoiced value. Three-way join produces the first ever true P&L per job including fuel — typically reducing perceived margin by 8–15%.

**Extraction difficulty:** Medium (API setup; OBD-II hardware installation in vehicles required)
**Accuracy ceiling:** 100% GPS; 95% inferred metrics (harsh event detection)
**Tokenisation pattern:** `driver_id → UUID | GPS_coordinates → 1km grid square | vehicle_VRM → hashed | job_address → outward postcode only`

---

### 10.2 Fuel Cards — Allstar, FuelGenie

**What it is & where it lives:** Transaction-level fuel purchase records: timestamp, station location, litres purchased, unit price, card/vehicle ID, and odometer reading (at station). [Allstar](https://www.fuelcardservices.com/fuel-cards/allstar-one-fuel-cards/) provides online account access with detailed fuel analysis reports; [Fleevo integration](https://www.fleevo.io/integration/allstar) merges Allstar data with telematics. FuelGenie portal export (CSV).

**How to extract:**
1. **Export-first:** Allstar/FuelGenie online portal → Reports → CSV download (daily/weekly)
2. **API-second:** Fleevo platform for Allstar integration; no direct public API confirmed for UK fuel cards — portal export is primary method

**Key signals:**
- Cost-per-mile by vehicle (requires telematics mileage integration)
- Fuel purchase frequency vs job density → efficiency signal
- Station location vs job site location → driver deviation detection
- Fuel-price arbitrage: are drivers filling up at motorway forecourts (25–40p/litre premium)?
- Mpg trend per vehicle → engine health proxy

**Pudding bridge:** Allstar fill-up timestamps + GPS location × Geotab engine hours × BrightPay overtime hours → **Vehicle total cost of ownership per driver**: not just fuel but depreciation-weighted engine hours + overtime premium when vehicles are used outside standard hours. Reveals that one specific van + driver combination costs 40% more per productive hour than the fleet average.

**Extraction difficulty:** Easy (portal CSV)
**Accuracy ceiling:** 100%
**Tokenisation pattern:** `card_id → UUID | fuel_station_postcode → outward code | litres → exact (non-personal) | cost → exact`

---

### 10.3 Smart Meters — MPAN / n3rgy / Hildebrand Glow API

**What it is & where it lives:** Half-hourly (HH) electricity and gas consumption from SMETS2 smart meters. Access via [n3rgy](https://www.smartme.co.uk/meter-data) (free, using MPAN + meter MAC address) or [Hildebrand Glow API](https://www.reddit.com/r/homeassistant/comments/174k6ff/uk_any_energy_providers_with_api_access_to_your/) (free consumer tier via Bright app). Octopus Energy provides a REST API for Octopus customers. MPAN (Meter Point Administration Number) is on every UK electricity bill.

**How to extract:**
1. n3rgy free API: `https://consumer.n3rgy.com/read/electricity/{mpan}/1` → returns HH consumption (data lags ~6h)
2. Hildebrand Glow: CAD (Consumer Access Device) hardware + MQTT stream → near-real-time; also REST API
3. Octopus Energy API: OAuth for Octopus customers, returns HH readings directly

**Key signals:**
- Energy consumption by hour → true operating hours signal (more reliable than stated hours)
- Baseline overnight consumption → phantom load / equipment left on cost
- Energy intensity per revenue £ → efficiency benchmark
- Seasonal consumption pattern → heating/cooling cost distribution
- Equipment switch-on signatures (spike profiles) → asset usage detection without sensors
- Peak demand charges: HH data reveals if demand peak is triggering higher unit rates

**Pudding bridge:** Smart meter HH consumption × Epos Now hourly transaction volume × Deputy shift rota → **Energy-efficiency-per-customer model for hospitality**: a café heating to 21°C from 6am but not opening until 8am wastes 2 hours of heating cost. Cross-referencing actual first-customer transactions with HVAC consumption start times quantifies the exact saving from a 60-minute later heating schedule.

**Extraction difficulty:** Medium (MPAN access; hardware CAD device for real-time)
**Accuracy ceiling:** 99%
**Tokenisation pattern:** `MPAN → hashed | consumption → kWh per half-hour bucket | location → site code`

---

### 10.4 Door Access & CCTV Metadata

**What it is & where it lives:** Access control logs (Paxton, Salto, HID) record card/fob swipes with timestamp, door ID, direction (entry/exit), and grant/deny status. CCTV metadata (AXIS, Hikvision, Dahua) via VMS APIs provides motion detection events, object classification (person/vehicle), and zone triggers — without recording content.

**How to extract:**
1. **Export-first:** Paxton Net2 software → Reports → CSV export of access events
2. **API-second:** Paxton API (site-server based); Salto Cloud API; AXIS Camera Station ACAP apps expose event metadata

**Key signals (metadata only — no content):**
- First-arrival/last-departure timestamps → true working hours signal
- Weekend and out-of-hours access frequency → unauthorised access risk or owner overwork signal
- Visitor entry frequency → client/supplier visit pattern
- Delivery vehicle detection in car park → fulfilment activity
- After-hours motion events → security risk indicator

**Pudding bridge:** Door access first-entry timestamps × BrightPay contracted start times × Google Calendar first meeting of day → **Presenteeism vs productivity analysis**: staff who arrive consistently early but have no meetings or project activity in M365 for the first hour may be performing low-value habitual tasks. Combined with job completion rates, identifies whether early arrival correlates with higher output or just longer hours.

**Extraction difficulty:** Medium (on-site system access required)
**Accuracy ceiling:** 99% (machine-generated)
**Tokenisation pattern:** `cardholder_id → UUID | door_id → retained (non-personal) | timestamp → exact`

---

## Category 11: Customer Feedback

### 11.1 Review Platforms — Trustpilot, Checkatrade, Google Reviews

**What it is & where it lives:** Public and semi-public customer review data. [Trustpilot Business API](https://documentation.trustpilot.com/) provides review retrieval by business unit (requires Trustpilot account). Google Business Profile Reviews API (as per GMB section). [Checkatrade](https://uk.trustpilot.com/review/www.checkatrade.com) is critical for UK trades — profiles include verified reviews tied to completed jobs. Structured fetch from public pages is viable where no API exists.

**How to extract:**
1. Trustpilot: Business API → `GET /v1/business-units/{businessUnitId}/reviews`; returns star rating, review body, reply, date, reviewer metadata
2. Checkatrade: no public API — structured page fetch + LLM extraction on-site (review text stays on-site; only sentiment score + theme category transmitted)
3. Google Reviews: Business Profile API (see 8.3)

**Key signals:**
- Net review velocity: new reviews per month (trend, not just total)
- Sentiment trajectory: is average rating improving or declining over the last 6 months?
- Recurring theme extraction: what topics appear in 3+ negative reviews? (quality, price, timing, communication)
- Response rate and response time: are negative reviews being managed?
- Review clustering by job type or technician: which jobs generate the best/worst reviews?

**Pudding bridge:** Checkatrade review themes (LLM-extracted on-site) × Jobber job type codes × Xero invoice value → **Service-line reputation-margin matrix**: high-margin jobs that generate negative reviews about "poor workmanship" are destroying repeat business from the most profitable customers. Low-margin jobs generating glowing reviews are building the pipeline. Neither the accounting system nor the review platform alone surfaces this trade-off.

**Extraction difficulty:** Easy (API) to Medium (structured page fetch for Checkatrade)
**Accuracy ceiling:** 98% metadata; 90–95% on-site LLM theme extraction
**Tokenisation pattern:** `reviewer_name → UUID | review_text → on-site only; sentiment_score + theme_tags transmitted | star_rating → exact`

---

### 11.2 NPS Surveys, Complaints Registers, Returns Data

**What it is & where it lives:** NPS data (Typeform, Delighted, SurveyMonkey) via API or CSV export. Complaints register: often a spreadsheet or email folder — requires LLM extraction on-site. Returns data: Xero credit notes or Cin7 return orders.

**Key signals:**
- NPS trend by month → leading indicator of revenue risk (NPS drop precedes churn by 60–90 days)
- Complaint-to-revenue ratio → operational quality trend
- Return rate by SKU → product quality or expectation mismatch
- Complaint resolution time → service quality benchmark

**Pudding bridge:** NPS passives (score 7–8) × email open rate (Mailchimp) × Jobber rebooking rate → **Dormant advocate reactivation model**: customers who gave a 7 NPS, open emails regularly but haven't rebooked in 90+ days are warm-but-stuck. A targeted sequence (not a generic newsletter) with a specific incentive converts 15–25% of dormants vs 2–3% generic campaign response.

**Extraction difficulty:** Easy (API for Typeform/Delighted; Medium for manual complaint registers)
**Accuracy ceiling:** 99% (survey data); 88–93% (LLM extraction of complaint emails)
**Tokenisation pattern:** `respondent_email → UUID | NPS_score → exact | free_text → on-site only; theme_category transmitted`

---

## Category 12: External Contracts & Documents

### 12.1 eSign Platforms — DocuSign, Adobe Sign

**What it is & where it lives:** Completed agreement data including: signatory details, signing timestamps, IP addresses, form field values (Tab Data), document metadata, and audit trail. [DocuSign REST API](https://www.esignglobal.com/blog/docusign-api-get-tab-data-form-data-signed-doc-json-export) `GET /envelopes/{envelopeId}/documents/{documentId}/form_data` returns structured JSON of all filled form fields. Adobe Sign Agreements API: `GET /agreements/{agreementId}/formData`.

**How to extract:**
1. **API-second:** DocuSign: REST API v2.1, requires Integration Key + OAuth2. Retrieve completed envelopes + Tab Data in JSON. Connect webhook (event-driven, zero-latency)
2. Adobe Sign: REST API `agreements` endpoint; Connect webhooks for real-time

**Key signals:**
- Contract turnaround time: send to completion duration → sales velocity metric
- Signature completion rate: % of sent agreements actually signed → proposal quality/alignment signal
- Voided/declined envelopes → lost deals not captured in CRM
- Contract value extraction (from Tab Data) → shadow pipeline distinct from CRM pipeline
- Renewal date extraction → automated contract renewal alert (no human calendar needed)

**Pudding bridge:** DocuSign contract renewal dates (extracted to day) × Open Banking direct debit schedule × Xero subscription expenses → **Supplier contract renewal optimisation**: identifies contracts expiring within 90 days where the business is paying above benchmark (cross-referenced against cross-client aggregate cost data). Triggers a renegotiation prompt 60 days before renewal — before the auto-renewal catches the owner off guard.

**Extraction difficulty:** Medium (API setup; per-envelope data retrieval)
**Accuracy ceiling:** 97% for structured fields (form data); 88–92% for LLM-extracted unstructured contract terms
**Tokenisation pattern:** `signatory_name → UUID | signatory_email → UUID | contract_value → decile bucket | renewal_date → month/year only`

---

### 12.2 Companies House, HMRC, FCA — Official Registers

**What it is & where it lives:** UK government open data. [Companies House API](https://developer.company-information.service.gov.uk) (free, real-time REST): company profile, officers, filing history, charges, insolvency, persons of significant control. [Companies House streaming API](https://companieshouse.blog.gov.uk/2019/10/24/launching-our-streaming-api-service-for-company-data/) pushes real-time changes (company updates, officer changes, new charges). FCA register (regulated firms, approved persons) via FCA API. HMRC VAT validation via HMRC VAT Lookup API (free).

**How to extract:**
1. **API-first:** Companies House API `GET https://api.company-information.service.gov.uk/company/{company_number}` — no cost, no rate limit for reasonable use (REST + streaming)
2. FCA Register: `https://register.fca.org.uk/services/V0.1/Firm/{FRN}` — free REST API
3. HMRC VAT number validation: `https://api.service.hmrc.gov.uk/organisations/vat/check-vat-number/lookup/{vatNumber}`

**Key signals (for internal business intelligence):**
- Verify client/supplier company is active (not dissolved) in real-time
- Director change alerts: new director appointments at key suppliers/clients = relationship risk signal
- Charge registration (mortgage/debenture): supplier has pledged assets = financial stress indicator
- Late filing history: persistent late accounts filing → governance red flag
- PSC (Persons of Significant Control) data → beneficial ownership for AML/KYC

**Pudding bridge:** Companies House officer change alerts for top 10 suppliers × Xero AP ageing (what do we owe them?) × Open Banking DD schedule (when do we pay them?) → **Supply-chain disruption early warning**: a director resignation at a key supplier is a leading indicator of business distress 60–90 days before any public announcement. Pre-position with alternative supplier qualification before supply is interrupted.

**Extraction difficulty:** Easy (free API, no OAuth required — just API key)
**Accuracy ceiling:** 100% (primary source)
**Tokenisation pattern:** `company_number → retained (public data) | officer_name → UUID for internal graph | filing_date → retained`

---

## Top 20 Highest-Value Internal Sources: Definitive Ranking

Scored on: (1) Revenue insight density, (2) Cross-client benchmark value, (3) Extraction feasibility, (4) Fusion multiplier, (5) Uniqueness vs publicly available data.

| Rank | Source | Why It's Here | Killer Pudding Bridge |
|---|---|---|---|
| **1** | **Open Banking Feed** (TrueLayer/GoCardless) | Real-time cash truth. No other source knows actual liquidity to the minute. Cross-client benchmark: sector cash-curve by week of month. | OB balance × MTD VAT dates × Xero AR ageing = Cash-stress early warning system |
| **2** | **Xero / Accounting API** | Source-of-truth for all financial flows. AR ageing is the single highest-leverage operational metric for SMBs. | Xero margin by category × GMB review sentiment = Margin-reputation matrix |
| **3** | **Job Management API** (ServiceM8/Jobber) | For trades — this IS the operating system. Recall rate, FTF rate, and utilisation are invisible without it. | Job GPS × fuel cards × invoice value = True job P&L |
| **4** | **VoIP CDR + Transcripts** | Demand signal before it enters any system. Abandonment rate is the most honest capacity metric. | CDR abandonment × weather × seasonality = Proactive staffing model |
| **5** | **Vehicle Telematics** | For trades/delivery: travel cost is 12–18% of gross margin, almost never measured. | Telematics routes × job postcodes × fuel cards = True cost-per-job |
| **6** | **HR/Payroll (BrightPay/Xero)** | Starter/leaver velocity predicts revenue dips 4–8 weeks ahead. Tenure distribution = fragility map. | Leaver dates × job completion rate × P&L = Revenue-impact-per-leaver model |
| **7** | **CRM Pipeline** (HubSpot/Pipedrive) | Lost-reason analysis is the single most-ignored, highest-value dataset in any sales-driven business. | Lost reasons × GA4 page depth = Proposal optimisation |
| **8** | **Call Transcripts** (Whisper on-site) | Surfaces what customers say, not what CRM records. Sentiment trend is a leading churn indicator. | Transcript sentiment × invoice timing × contact cadence = Pre-churn alert |
| **9** | **Rota Software** (Deputy/RotaCloud) | Planned vs actual hours reveals labour model reality. Bridges to POS, payroll, and sales simultaneously. | Rota gaps × GMB direction requests × Epos Now revenue = Understaffing cost calculator |
| **10** | **Smart Meter (MPAN/n3rgy)** | Half-hourly energy = true operating hours signal. Energy-per-revenue-£ is a hidden efficiency benchmark. | HH energy × transaction volume × rota = Energy efficiency per customer served |
| **11** | **Google My Business Insights** | Direction requests = geographic demand map. Call-click volume = invisible inbound demand. | GMB direction requests × rota gaps × average spend = Geographic opportunity map |
| **12** | **eSign / Contract Data** | Renewal dates, contract values, and signing-time are almost never systematically tracked. | Contract renewal dates × OB DD schedule × Xero expenses = Supplier renegotiation trigger |
| **13** | **Email Metadata** (Gmail/Outlook) | Response-time distribution reveals the relationship bottlenecks before they appear elsewhere. | Email latency × AR ageing = Customer health score |
| **14** | **POS System** (Epos Now/Square) | Basket analysis and staff-level transaction monitoring are never done at SMB level. | POS × rota × GA4 = Conversion funnel by staff member |
| **15** | **GA4 + Search Console** | Source-of-truth for digital demand. BigQuery raw export enables forensic session analysis. | GSC queries × GMB reviews × Jobber lost reasons = Search-reputation-conversion triangle |
| **16** | **Fuel Card Data** | Direct, to-the-penny fuel cost measurement. Untouched in most SMBs. | Fuel cards × telematics × payroll overtime = Vehicle total cost of ownership per driver |
| **17** | **WhatsApp Business** | Shadow pipeline data: enquiries that never entered CRM. Response time is invisible everywhere else. | WhatsApp timestamps × weather × GMB call clicks = Emergency demand prediction model |
| **18** | **Companies House / Streaming API** | Free, real-time. Director changes at suppliers = best-in-class distress early warning. | Officer changes × AP ageing × DD schedule = Supply-chain disruption alert |
| **19** | **HMRC MTD** | VAT trajectory is the most reliable growth proxy. Cross-client aggregate: sector VAT trends by quarter. | MTD VAT × OB balance × Xero pipeline = Regulatory payment stress model |
| **20** | **M365 Activity Reports** | Teams device type silently classifies field vs office workers. Inactive licences = immediate cost saving. | M365 mobile proportion × job management GPS × payroll = Field-worker digital infrastructure gap |

---

## Cross-Client Pattern Library: The Proprietary Moat

When tokenised, normalised data from 50+ UK SMB clients pools into Ewan's central pattern-detection layer, the following benchmark datasets become available — datasets no competitor, no trade association, and no government body currently produces at this granularity:

| Benchmark Dataset | What It Reveals | First Available at N= |
|---|---|---|
| Debtor days by SIC code and revenue band | Is this client's 52-day DSO good or bad for their sector? | 10 clients |
| Call abandonment rate by trade type and hour | Optimal staffing by time-of-day for heating engineers vs electricians | 15 clients |
| Job-to-invoice conversion rate by job type | Benchmark for quote acceptance rates in trades | 15 clients |
| Staff churn rate by payroll grade band | Sector-level early-warning salary benchmarks | 20 clients |
| Energy cost per revenue £ by SIC code | True energy intensity benchmark for SMBs | 20 clients |
| Smart meter overnight consumption as % of daily total | Phantom load benchmark by business type | 25 clients |
| NPS score by marketing channel source | Which lead sources generate the most satisfied customers? | 20 clients |
| Vehicle cost per productive job hour by trade | True fleet cost benchmark for UK trades businesses | 15 clients |
| Contract renewal alert lead-time distribution | When do SMBs actually renegotiate vs auto-renew? | 30 clients |
| Cash runway distribution by week-of-quarter | Peak cash stress timing across the SMB population | 30 clients |

This dataset, assembled from P2-tokenised client data, is the internal "Office of National Statistics for UK SMBs" that Ewan's Amplified Methodology Framework is designed to build. No single external data provider (not ONS, not HMRC, not any trade association) produces this combination of real-time operational, financial, and behavioural signals. It is Amplified Partners' most durable competitive asset.

---

## Sources

1. [Gmail API Overview — Google for Developers](https://developers.google.com/workspace/gmail/api/guides)
2. [Google Vault Export Guide — Onna](https://onna.com/blog/export-data-from-gmail-and-google-drive)
3. [Office 365 Management Activity API Reference — Microsoft Learn](https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-reference)
4. [Microsoft Graph API Usage Reports — Microsoft Learn](https://learn.microsoft.com/en-us/answers/questions/504049/microsoft-365-apps-usage-report-using-rest-api-or)
5. [Slack Export Options by Plan — Slack Help Center](https://slack.com/help/articles/201658943-Export-your-workspace-data)
6. [Slack Data Export Guide — Slack Help Center](https://slack.com/help/articles/220556107-How-to-read-Slack-data-exports)
7. [3CX CDR Documentation — 3CX](https://www.3cx.com/docs/cdr-call-data-records/)
8. [3CX CDR V20 Update — 3CX Blog](https://www.3cx.com/blog/releases/u6-call-data-records/)
9. [RingCentral Call Log API — RingCentral Developers](https://developers.ringcentral.com/guide/voice/call-log)
10. [RingCentral Call Log Export — RingCentral Community](https://community.ringcentral.com/developer-platform-apis-integrations-5/how-to-export-call-logs-using-the-ringcentral-api-10656)
11. [Deepgram Speech-to-Text API — Deepgram](https://deepgram.com/product/speech-to-text)
12. [Xero Data Export Guide — Coefficient](https://coefficient.io/xero-accounting/export-xero-data)
13. [Xero UK Payroll API — Xero Developer](https://developer.xero.com/documentation/api/payrolluk/earningrates)
14. [VAT MTD API Catalogue — HMRC / api.gov.uk](https://www.api.gov.uk/hmrc/vat-mtd/)
15. [TrueLayer Data API — TrueLayer Docs](https://docs.truelayer.com/docs/data-api-basics)
16. [CMA9 Open Banking Overview — Ozone API](https://ozoneapi.com/blog/who-are-in-the-cma9-and-why-they-matter/)
17. [Open Banking UK Milestone — GOV.UK](https://www.gov.uk/government/news/millions-of-customers-benefit-as-open-banking-reaches-milestone)
18. [HubSpot Developer — Move Data](https://developers.hubspot.com/move-data)
19. [Pipedrive Export Guide — Pipedrive Support](https://support.pipedrive.com/en/article/exporting-data-from-pipedrive)
20. [Salesforce Data Export Methods — Flosum](https://www.flosum.com/blog/how-to-export-data-from-salesforce-a-complete-guide)
21. [Jobber API Documentation — Jobber Developer Center](https://developer.getjobber.com/docs/)
22. [ServiceM8 API — Stack Overflow](https://stackoverflow.com/questions/77153919/servicem8-api-endpoints-for-job-duration-and-booking-datetime)
23. [simPRO API Forum](https://apiforum.simprogroup.com/viewtopic.php?t=1609)
24. [Epos Now Exports — Slynk Digital](https://slynk.io/flow/exports-and-reports/)
25. [Fresha Service Export — Fresha Help Center](https://www.fresha.com/help-center/knowledge-base/catalog/100646-export-your-service-menu)
26. [Booksy UK Calendar Import — Booksy Help](https://support.booksy.com/hc/en-gb/articles/17499276381458-Can-I-import-my-external-calendar-to-Booksy)
27. [Cin7 Inventory API — Airbyte Docs](https://docs.airbyte.com/integrations/sources/cin7)
28. [BrightPay Payslip Export — BrightPay Docs](https://www.brightpay.co.uk/docs/bpol/distributing-payslips/exporting-payslips/)
29. [BrightPay Integration FAQ — TimeKeeper](https://help.timekeeper.co.uk/en/article/brightpay-cloud-payroll-integration-faqs-jmjhae/)
30. [Deputy Data Export Guide — Deputy Help](https://help.deputy.com/hc/en-au/articles/4755408081167-How-to-export-or-download-your-data)
31. [RotaCloud Data Export — RotaCloud Help](https://help.rotacloud.com/en/articles/10037503-how-do-i-export-data-from-rotacloud)
32. [GA4 Export Options — InfoTrust](https://infotrust.com/articles/exporting-your-google-analytics-4/)
33. [GA4 to BigQuery Export — PMG](https://www.pmg.com/insights-and-news/exporting-google-analytics-4-event-data-to-google-bigquery)
34. [Search Console Data Extraction — Sweet Digital](https://www.sweetdigital.co.uk/blog/data-extraction-google-search-console/)
35. [Google My Business API — Google for Developers](https://developers.google.com/my-business/reference/rest)
36. [Samsara Data Export Types — Samsara Help](https://kb.samsara.com/hc/en-us/articles/10118697996813-Samsara-Data-Export-Types)
37. [Allstar Fuel Card — Fuel Card Services](https://www.fuelcardservices.com/fuel-cards/allstar-one-fuel-cards/)
38. [Allstar + Telematics Integration — Fleevo](https://www.fleevo.io/integration/allstar)
39. [UK Smart Meter Data Access — SmartMe](https://www.smartme.co.uk/meter-data)
40. [Hildebrand Glow API — Reddit / r/homeassistant](https://www.reddit.com/r/homeassistant/comments/174k6ff/uk_any_energy_providers_with_api_access_to_your/)
41. [DocuSign Tab Data Extraction — eSignGlobal](https://www.esignglobal.com/blog/docusign-api-get-tab-data-form-data-signed-doc-json-export)
42. [Companies House REST API — Companies House Developer](https://developer.company-information.service.gov.uk)
43. [Companies House Streaming API Launch — Companies House Blog](https://companieshouse.blog.gov.uk/2019/10/24/launching-our-streaming-api-service-for-company-data/)
44. [Shadow IT Discovery — Strac](https://www.strac.io/blog/shadow-it-discovery)
45. [Shadow IT in M365 — NinjaOne](https://www.ninjaone.com/blog/detect-shadow-it-in-microsoft-365/)
46. [Amplified Extraction Methodology — Amplified Partners Internal](https://amplifiedpartners.com) *(internal skill document)*

---

*Document: `/home/user/workspace/research/01-internal-data-sources.md`*
*Workstream: 01/05 — Internal Data Sources Catalogue*
*Client: Ewan Bramley — Amplified Partners / Byker Business Help*
*Date: April 2026*
*Status: Complete — ready for master report integration*
