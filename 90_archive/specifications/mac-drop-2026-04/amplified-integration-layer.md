Status: [NON-AUTHORITATIVE]
Sanitisation: done — no client data, credentials, or PII found in source specifications
Source: Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB), ingested 2026-04-29

# Amplified Partners: The Integration Layer

## How We Link Into Their Existing IT Infrastructure

**Author:** Ewan Bramley / Amplified Partners
**Date:** 20 March 2026
**Status:** Architecture Specification — Ready for Content Creation

---

## The Question We Are Answering

We have the data extraction methodology (DocBench, the 89-to-99 percent pipeline). We have the voice-first interface (Cartesia, Whisper, command words). We have the sovereign knowledge base (SQL for binary truth, FalkorDB for graph relationships, Qdrant for vector search). We have the business brain.

What we have not formally defined is the integration layer: the piece that physically connects to the client's existing IT infrastructure, runs in parallel so they can verify that our data matches theirs, and presents a unified screen that is not a CRM, not a replacement, but a window into the intelligence we have built from their own data.

This document specifies that layer.

---

## Core Design Principle: The AI Sidecar

We do not touch their systems. We do not modify their Xero. We do not rewrite their CRM. We do not migrate their data. We sit beside it.

The architectural pattern for this is called the **AI Sidecar** — a term drawn from the same pattern used in Kubernetes and microservice architecture, but applied here to legacy SMB systems. The sidecar is an independent, lightweight service that runs alongside the primary application without being part of it ([Baytech Consulting](https://www.baytechconsulting.com/blog/minimize-risk-maximize-roi-with-sidecars), [Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar)).

In our context, the sidecar is the Amplified Partners intelligence layer. It observes. It reads. It analyses. It presents. It never writes back to their systems unless explicitly commanded to do so by the business owner.

### Why This Pattern Fits

Survey data from 2025 shows that 62 percent of organisations still rely heavily on legacy systems for daily operations. When asked why these systems have not been upgraded, 50 percent state the primary reason is simply that the current system still works ([Baytech Consulting](https://www.baytechconsulting.com/blog/minimize-risk-maximize-roi-with-sidecars)). This describes every SMB client we will onboard. Their Xero works. Their spreadsheet works. Their booking system works. They do not want us to replace any of it.

The sidecar pattern respects this. The key properties:

- **Language independence**: The sidecar runs independently from the client's systems. Their software can be written in anything — PHP, Visual Basic, AS/400, cloud SaaS — it does not matter ([Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar)).
- **Read-only access**: We connect via strictly read-only connectors. This is a one-way mirror. No AI hallucination or rogue query can overwrite, drop, or corrupt their core data ([Baytech Consulting](https://www.baytechconsulting.com/blog/minimize-risk-maximize-roi-with-sidecars)).
- **Shared resource access**: The sidecar can observe the same data the client sees, but processes it separately.
- **Low latency**: Because it sits adjacent to the client's data (on their machine, their network, or via a secure tunnel), communication is fast.
- **Decoupled failure**: If our sidecar has a problem — an update, a bug, a restart — their core business systems are completely unaffected.

### Cost Advantage

Incremental modernisation via the sidecar approach costs approximately 33 percent of a full rewrite, with positive ROI arriving 15 months earlier than a big-bang replacement ([Baytech Consulting](https://www.baytechconsulting.com/blog/minimize-risk-maximize-roi-with-sidecars)). For Amplified Partners, this is not even about modernisation. We are not replacing anything. We are adding an intelligence layer. The cost is even lower.

---

## The Connection Architecture

### How We Physically Link In

There are four connection methods, mapped to the pricing tiers. The method depends on what the client has.

#### Method 1: API Connectors (All Tiers, Primary Method)

For cloud-based SaaS tools, we connect via their published APIs. This is the cleanest, most reliable method.

| Client Tool | Connection Method | Access Type | Notes |
|---|---|---|---|
| Xero | OAuth 2.0 API | Read-only (write for invoicing if client opts in) | 5 years of accounting data, real-time bank feeds |
| QuickBooks Online | OAuth 2.0 API | Read-only | Similar to Xero, slightly different export structure |
| Sage Business Cloud | REST API | Read-only | Per-section data access, less mature API than Xero |
| FreeAgent | REST API | Read-only | True "export everything" capability |
| Companies House | Public REST API | Read-only | Free. Company data, director data, filing history |
| HMRC MTD | Government Gateway API | Read-only (write for MTD submissions if opted in) | Making Tax Digital compliance data |
| Open Banking (Plaid/TrueLayer) | OAuth API | Read-only | Bank transactions, 0.01-0.05 per transaction |
| Google Workspace | Google APIs | Read-only | Calendar, email metadata, contacts (with consent) |
| WhatsApp Business | WhatsApp Business API | Read + write (with consent) | The primary communication channel for Tier 1-2 |

These APIs do not hallucinate. The Xero API returns the exact data that exists in Xero. Our extraction methodology (the export-first, API-second principle) means that for roughly 80 percent of a typical SMB client's business data, we get 100 percent accuracy at zero extraction cost.

#### Method 2: MCP Servers (Tier 3+, For Existing IT Infrastructure)

The Model Context Protocol (MCP) is an open-source standard that defines how an AI system connects to external applications and data sources. It has become the default interoperability layer for AI-to-tool connections in 2025-2026 ([Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025), [Fenxi](https://fenxi.fr/en/blog/mcp-model-context-protocol-connecting-ai-business-tools-2026/)).

For Tier 3+ clients who have existing IT infrastructure — a server, a desktop PC running Sage 50, a local database, legacy software — we deploy MCP servers that wrap access to their existing tools.

The MCP architecture has three components ([Fenxi](https://fenxi.fr/en/blog/mcp-model-context-protocol-connecting-ai-business-tools-2026/)):

1. **The Host**: Our Amplified Partners intelligence layer (The Pulse, the Command Centre). This is what the client interacts with.
2. **The Client**: The connector inside our host that manages communication with MCP servers.
3. **The MCP Server**: A lightweight service that exposes the client's existing tools — their CRM, their document store, their back office, their internal API — in a standard format that our AI agents can query.

The critical point: you build an MCP server for a client's CRM once, and that server can work with any compatible host. We are not building bespoke integrations for every tool. We are building standardised connectors that slot into a protocol ([Fenxi](https://fenxi.fr/en/blog/mcp-model-context-protocol-connecting-ai-business-tools-2026/)).

For common tools (Notion, GitHub, Google Workspace, databases), open-source MCP servers already exist and can be deployed directly. For trade-specific tools (ServiceM8, Commusoft, SimPRO, job management systems), we build MCP servers once and reuse them across all clients in that vertical.

#### Method 3: Secure Tunnel (Tier 3+, For On-Premise Systems)

When the client has data that lives only on their local network — a desktop accounting package, a local database, a legacy system with no API — we use a Cloudflare Tunnel to create a secure connection between their infrastructure and ours.

Cloudflare Tunnel runs a lightweight daemon (cloudflared) on the client's machine. It creates outbound-only connections to Cloudflare's global network. No inbound ports need to be opened. No publicly routable IP address is required ([Cloudflare Docs](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)).

This means:

- Their firewall stays closed to incoming traffic.
- All traffic is encrypted and routed through Cloudflare's network.
- We can access their local services (a web dashboard, an SSH server, a database) securely without exposing them to the internet.
- They can configure their firewall to allow only these outbound connections and block everything else — effectively ensuring that nothing reaches their systems except through the tunnel ([Cloudflare Docs](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)).

Combined with Cloudflare Access (Zero Trust), we can add authentication so that only authorised Amplified Partners agents and the client themselves can access the tunnel. This is enterprise-grade security at zero cost for the basic tunnel.

#### Method 4: Direct Database Read (Tier 3+, For Legacy Databases)

For clients with data locked in older databases (SQL Server, MySQL, PostgreSQL, Access, even flat files), the sidecar connects via a read-only database connection.

The connection is architected as a one-way mirror. The AI sidecar is granted strictly read-only access. This air-gap prevents any possibility of an AI hallucination or a rogue generated query from accidentally overwriting, dropping, or corrupting the core transactional database tables ([Baytech Consulting](https://www.baytechconsulting.com/blog/minimize-risk-maximize-roi-with-sidecars)).

For Text-to-SQL queries (where an agent generates SQL from natural language), we execute against a read-only replica, never the live database.

---

## The Parallel Running Pattern: Shadow Mode

This is the part you identified as critical: the system needs to run in unison with the existing IT first so they can check that we are right.

The industry term for this is **shadow mode** (also called **parallel running** or **shadow deployment**). It is a deployment practice where the new system runs alongside the live system, receives the same inputs, produces its own outputs, but those outputs do not affect the live system. The new version's output is compared against the existing system's output, not used to replace it ([DevOps.com](https://devops.com/what-is-a-shadow-deployment/)).

### How Shadow Mode Works for Amplified Partners

When we onboard a client (during the 72-hour training period and the first month), the Amplified Partners system runs in shadow mode:

1. **We read their data** from existing systems (Xero, booking system, CRM, bank feeds) via the API/MCP/tunnel connectors described above.
2. **We build the business brain** — the FalkorDB graph, the SQL sovereign knowledge base, the vector store.
3. **We present our version of reality** on The Pulse / the Command Centre screen.
4. **The client compares** what we show them against what their existing systems show them.
5. **Discrepancies are flagged and investigated** — every single one, during the shadow period.
6. **Only when the client is satisfied that our data matches theirs** do we move from shadow mode to live mode.

During shadow mode:

- Our system **reads** from their systems. It does not write.
- Our system **presents** data. It does not act on it (no auto-invoicing, no auto-scheduling, no auto-communications) unless the client explicitly asks for it.
- Every piece of data we present has a **provenance trail** — the client can see exactly where it came from (which system, which API call, which timestamp).
- **Reconciliation reports** run automatically: our data versus their data, field by field, with any mismatches highlighted and investigated.

### The Reconciliation Engine

Automated reconciliation is how we prove that our data matches theirs. The principles from data reconciliation best practice apply ([Monte Carlo Data](https://www.montecarlodata.com/blog-data-reconciliation/)):

1. **Record matching**: We match records between our system and theirs using deterministic keys (invoice number, transaction ID, customer reference).
2. **Field-by-field comparison**: For matched records, we compare every field — amounts, dates, names, statuses.
3. **Discrepancy classification**: Mismatches are classified:
   - **Timing differences** (e.g., our system ingested 10 minutes after their system updated — expected, not an error)
   - **Format differences** (e.g., "Robert Smith" vs "Bob Smith" — semantically identical, flagged for review)
   - **Genuine errors** (e.g., amount mismatch — investigated immediately)
4. **Pattern detection**: If the same type of mismatch keeps appearing, we fix the root cause. A consistent timezone offset, a rounding difference, a field mapping error — these get fixed once and do not recur.
5. **Match rate tracking**: We track reconciliation health with a simple metric: what percentage of records match perfectly. The target is 100 percent for financial data (the 100 Percent Rule from our extraction methodology). For non-financial data (names, descriptions, notes), 98 percent or above is acceptable.

The reconciliation runs on a schedule tied to data criticality ([Monte Carlo Data](https://www.montecarlodata.com/blog-data-reconciliation/)):

| Data Type | Reconciliation Frequency | Match Rate Target |
|---|---|---|
| Financial (invoices, payments, bank transactions) | Every sync cycle (real-time or hourly) | 100% |
| Customer records (names, contacts, addresses) | Daily | 98%+ |
| Job/booking data | Every sync cycle | 99%+ |
| Compliance data (certs, licences, dates) | Daily | 100% |
| Communications (email metadata, WhatsApp logs) | Weekly | 95%+ |

### The Trust Ramp

Shadow mode is not permanent. It is a trust-building mechanism. The ramp looks like this:

**Week 1-2 (Full Shadow)**: Everything is read-only. The Pulse shows data, the client verifies it against their existing systems. Reconciliation reports run daily. Every discrepancy is investigated and resolved.

**Week 3-4 (Assisted Shadow)**: Once the match rate is consistently at target, we begin offering actions — but the client must confirm every one. "Shall I send this invoice?" "Shall I schedule this appointment?" "Shall I post this content?" The client says yes or no. Every action is logged.

**Month 2 (Supervised Autonomy)**: For actions where the client has consistently said yes (e.g., auto-invoicing, appointment confirmations), we propose moving to automatic execution with post-hoc review. The client can review what we did each morning. They can reverse any action.

**Month 3+ (Trusted Autonomy)**: For actions with a proven track record of accuracy and client approval, we execute automatically. The client still has full visibility and can override anything. The confidence-gating system (greater than 95 percent confidence: auto-execute, 70-95 percent: logged for review, below 70 percent: escalated to human) governs which actions auto-execute and which wait for approval.

This ramp aligns with the design principle from COV-39 (guided quick wins, gradually remove training wheels) and the BJ Fogg Behavior Model (B = MAP: motivation, ability, prompt — build the prompt only after the ability and motivation are established).

---

## The Screen: Not a CRM, But a Command Centre

You identified this correctly. It is not a CRM. A CRM is a system of record — it stores customer data, manages pipelines, tracks interactions. We are not replacing their system of record. Their Xero, their booking system, their contact list — those remain the source of truth.

What we are building is a **Command Centre**: a single screen that aggregates intelligence from all their systems into one view. The industry calls this a "single pane of glass" — a unified dashboard that pulls data from multiple sources and displays it in one place ([IBM](https://www.ibm.com/think/topics/single-pane-of-glass)).

### What the Command Centre Is

- A **read layer** on top of their existing systems
- A **presentation layer** for the intelligence our business brain has derived
- A **voice-first interface** with keyboard fallback for when they need to type
- A **reconciliation dashboard** during shadow mode, showing our data versus theirs
- A **decision support tool** that presents scored options (rubrik scores, not opinions) and lets the business owner choose
- A **templated action interface** where every action follows the ISO 9001 process structure they have already approved

### What the Command Centre Is Not

- Not a replacement for Xero, Sage, QuickBooks, or any other system they already use
- Not a system of record — it does not store the canonical version of their data
- Not a CRM with pipelines, deal stages, or sales funnels (unless they want that)
- Not an interpretation engine — it presents data, scored by deterministic rubrics, and the human decides

### The Five Tabs

The Command Centre is structured into five tabs (as specified in COV-230):

| Tab | Purpose | What It Shows |
|---|---|---|
| **Ops** | Operational overview | Today's schedule, active jobs, compliance reminders, weather alerts, staff assignments |
| **Content Studio** | Marketing and communications | Content queue, draft posts for approval, review requests sent, campaign performance |
| **Fund** | Financial intelligence | Cash position, cash runway, invoice status, payment tracking, rubrik scores (Altman Z, Cash Conversion, Quick Ratio) |
| **Validator** | Reconciliation and trust | Data match rates, discrepancies under investigation, system sync status, audit trail |
| **Accountability** | Life goals and Kaizen | Life Goals progress, 0.5% daily Kaizen tracking, staff meeting outcomes, action item status |

### The Voice-First, Keyboard-Second Interface

The interface is voice-first by design. The voice interface uses command words — short, specific phrases that trigger deterministic actions. This is not free-form conversation with an AI. This is a structured command interface with natural language understanding on top.

The design principles for voice-first interfaces that work for non-technical users ([Koru UX](https://www.koruux.com/ux-voice/), [Naskay Tech](https://naskay.com/blog/voice-user-interfaces-2025-smarter-touchless-design/), [TheFinch Design](https://thefinch.design/voice-user-interface-design-best-practices-2026/)):

1. **Context awareness**: The system remembers the last spoken command and uses it to resolve ambiguous references ("Call him" — it knows who "him" is from the previous sentence).
2. **Clear feedback**: Every voice command gets an auditory confirmation. "Invoice sent to Bob at J&J Heating. Amount: £485. Due: 14 days." The user hears exactly what happened.
3. **Progressive disclosure**: Start with a small set of core commands (5-10) and expand as the user becomes comfortable. Do not overwhelm on day one.
4. **Keyboard fallback**: When the user needs to make corrections, enter specific numbers, or edit text, the keyboard is always available. Voice-first does not mean voice-only.
5. **Rejection of uncertain inputs**: If the system is not confident it understood correctly, it asks the user to repeat rather than guessing. This is the accuracy-first principle.

The command word structure:

| Voice Command | Action | Confirmation |
|---|---|---|
| "Invoice Bob, J&J Heating, four eight five pounds, boiler service" | Creates invoice, auto-populates customer details from knowledge graph | "Invoice created. Bob at J&J Heating. Amount £485. Boiler service. Shall I send it?" |
| "Schedule Tuesday 2pm, Mrs Williams, annual boiler check" | Creates calendar entry, checks for conflicts, allocates travel time | "Booked: Mrs Williams, annual boiler check. Tuesday at 2pm. Travel time: 25 minutes from previous job." |
| "How's cash?" | Retrieves current cash position from Fund tab | "Cash today: £12,340. Expected in next 7 days: £3,200 from 4 invoices. Cash runway: 47 days at current spend." |
| "Who owes me?" | Retrieves overdue invoices | "Three overdue invoices totalling £2,180. Bob Smith: £950, 14 days late. Janet Lee: £830, 7 days late. Park Dental: £400, 3 days late." |
| "Morning" | Triggers the Morning Briefing flow | Delivers: overnight wins, today's schedule, cash position, any compliance reminders, any content needing approval |

Every voice interaction is logged, transcribed, and stored (with consent) as part of the business audit trail.

---

## The Technical Stack for the Integration Layer

### For Phone-Only Clients (Tier 1-2: £99-£295/month)

```
Client's Phone
  └── WhatsApp Business API (primary channel)
  └── Voice interface (Cartesia + Whisper)
  └── PWA (Progressive Web App) for The Pulse dashboard
        └── Installable from browser, no app store needed
        └── Offline-capable (cached data, queued actions)
        └── Syncs when back online
  └── Connects to:
        └── Amplified Partners Cloud (Beast / Railway)
              └── API connectors to Xero/QB/Sage (read-only)
              └── FalkorDB tenant (kg_{client_namespace})
              └── SQL sovereign knowledge base
              └── Agent swarm (marketing, finance, ops)
```

The PWA approach is critical for phone-first clients. Progressive Web Apps are faster and lighter than native apps, require no app store installation, and can be used across different devices. Users open the PWA website in their browser, add a desktop shortcut, and use it as an app ([Monterail](https://www.monterail.com/blog/pwa-examples)). PWAs can deliver offline functionality, push notifications, and app-like features ([Unified Infotech](https://www.unifiedinfotech.net/blog/pwa-revolution-in-modern-businesses/)).

For our Next.js + Tailwind + shadcn/ui stack, PWA support is native. With Serwist (the service worker library), we get true offline support: the app caches the UI shell, stores data locally with IndexedDB, and syncs changes when connectivity returns ([LogRocket](https://blog.logrocket.com/nextjs-16-pwa-offline-support/), [Next.js Docs](https://nextjs.org/docs/app/guides/progressive-web-apps)).

This matters for tradespeople. A plumber in a basement with no signal can still check their schedule, log a job note, and create an invoice. When they come back into signal range, everything syncs.

### For IT-Based Clients (Tier 3+: £595+/month)

```
Client's Existing IT Infrastructure
  ├── Accounting software (Xero/Sage/QB) ─── API connectors (read-only)
  ├── CRM / spreadsheets / job management ─── MCP servers (read-only)
  ├── Legacy databases (SQL Server/Access/flat files) ─── Direct DB read (read-only)
  ├── Email / calendar / contacts ─── Google/Microsoft APIs (read-only)
  └── Local file storage ─── DocBench extraction pipeline
        │
        └── All read via one-way mirror connectors
              │
              ▼
  Cloudflare Tunnel (outbound-only, encrypted)
              │
              ▼
  Amplified Partners Intelligence Layer
  ├── PicoClaw (on-premise, runs on their machine or Beelink N100)
  │     ├── Local data extraction and processing
  │     ├── P2 tokenisation (sensitive data never leaves)
  │     ├── MCP servers for legacy tool access
  │     └── Cloudflared daemon (tunnel to Beast)
  │
  └── Beast Server / Railway (cloud intelligence)
        ├── FalkorDB tenant (kg_{client_namespace})
        ├── SQL sovereign knowledge base
        ├── Agent swarm (marketing, finance, ops, enforcer)
        ├── Reconciliation engine
        └── Command Centre API (serves The Pulse / dashboard)
              │
              ▼
  Client's Browser / Phone
  └── The Pulse (PWA / web dashboard)
        ├── Command Centre (5 tabs)
        ├── Voice interface + keyboard
        ├── Reconciliation dashboard (shadow mode)
        └── Offline-capable, auto-sync
```

### The PicoClaw Component

PicoClaw is the on-premise sidecar. It runs on the client's own hardware — a Beelink N100 (£150, passively cooled, silent), their existing server, or even their desktop PC. It handles:

1. **Local data extraction**: Reads from legacy systems, local databases, file shares.
2. **P2 tokenisation**: Sensitive data (PII, financial figures) is tokenised before it leaves the client's network. Raw values never cross the tunnel.
3. **MCP server hosting**: Runs the MCP servers that expose the client's local tools to our intelligence layer.
4. **Offline intelligence**: Can run basic queries and present cached data even if the tunnel to Beast is down.
5. **Cloudflared**: The tunnel daemon that maintains the secure outbound connection to our cloud infrastructure.

PicoClaw respects the Schumacher Principle — it is right-sized for the client. A solo plumber does not get a PicoClaw. They get their phone. A 10-person business with a server room gets PicoClaw running in a Docker container. The technology is appropriate to the business.

---

## The Strangler Fig: Long-Term Integration Strategy

For clients who want to go further — who, over time, want to consolidate their tools and reduce their SaaS sprawl — we offer the Strangler Fig pattern.

The Strangler Fig Pattern is named after a vine that grows around a tree, gradually replacing it without killing it abruptly. In software, the pattern works the same way: instead of rewriting a legacy system wholesale, you place a routing layer in front of it, incrementally build new functionality outside the legacy codebase, redirect specific requests to the new system over time, and eventually retire the legacy system once nothing depends on it ([Technori](https://technori.com/news/strangler-fig-pattern/), [Kai Waehner](https://www.kai-waehner.de/blog/2025/03/27/replacing-legacy-systems-one-step-at-a-time-with-data-streaming-the-strangler-fig-approach/), [Future Processing](https://www.future-processing.com/blog/strangler-fig-pattern/)).

At no point does the system stop working. At no point is there a big bang cutover.

### How This Applies to Amplified Partners Clients

This is entirely optional and client-driven. We never push it. But here is what it looks like:

**Phase 1 (Months 1-3)**: Sidecar mode. We read from their existing systems. The Command Centre is a read layer. Their existing tools remain the system of record.

**Phase 2 (Months 3-6)**: The client notices they are checking The Pulse more than they check their old systems. Some actions (invoicing, scheduling) start being initiated through The Pulse rather than through the old tools. The Command Centre begins to handle some write operations (with full audit trail).

**Phase 3 (Months 6-12)**: The API gateway / routing layer begins to route more requests through The Pulse. The client's MCP servers provide bi-directional access — not just reading from old tools, but writing back to them from The Pulse. The old tools are still running, still being synced, still the system of record for audit purposes.

**Phase 4 (12+ months)**: If the client chooses, the old tools handle fewer and fewer tasks. The Pulse has become the primary interface. The old tools are there for compliance and historical record. Eventually, they may be decommissioned entirely — but only when the client is ready, and only if they want to.

The Strangler Fig pattern ensures 100 percent operational continuity throughout. Because both systems coexist, the client can always fall back to their old tools if needed. There is zero risk of a failed migration ([Technori](https://technori.com/news/strangler-fig-pattern/)).

This is the Amplified Partners way: their business, their pace, their choice. We do not drive the car. We de-friction the journey.

---

## Data Consistency: Solving the Dual-Write Problem

When a system reads from one place and writes to another, you get the dual-write problem: what happens if one write succeeds and the other fails? Your data becomes inconsistent ([Confluent](https://www.confluent.io/blog/dual-write-problem/), [AuthZed](https://authzed.com/blog/the-dual-write-problem)).

For Amplified Partners, this manifests when a client starts using The Pulse to initiate actions (Phase 2-3 of the Strangler Fig). If they create an invoice through The Pulse, it needs to appear in both our system and their Xero.

### Our Solution: The Transactional Outbox Pattern

We use the transactional outbox pattern, which is a well-established solution to the dual-write problem ([Confluent](https://www.confluent.io/blog/dual-write-problem/)):

1. When the client initiates an action through The Pulse (e.g., create an invoice), we write the action to our database AND to an outbox table in the same database transaction.
2. A separate process reads the outbox and sends the action to the client's external system (e.g., Xero API).
3. If the external write fails, we retry until it succeeds. The action is never lost because it is persisted in the outbox.
4. Once the external write is confirmed, we mark the outbox entry as completed.

The result: eventual consistency. There may be a brief period (seconds to minutes) where our system has the invoice and Xero does not yet. But the invoice will get there. It is guaranteed by the retry mechanism.

For financial data, where 100 percent accuracy is non-negotiable, the reconciliation engine (described above) runs a comparison after every sync cycle to confirm both systems agree.

---

## Security Architecture for the Integration Layer

### The Principle: Privacy First, Security Second

| Layer | Protection | Implementation |
|---|---|---|
| **Client network boundary** | No inbound ports opened | Cloudflare Tunnel (outbound-only connections) |
| **Data in transit** | Encrypted | TLS 1.3 via Cloudflare Tunnel |
| **Data at rest** | Encrypted | FalkorDB encrypted storage, P2 tokenisation |
| **API authentication** | OAuth 2.0 + API keys | Per-client credentials, stored in secrets/ (never in vault) |
| **Access control** | Zero Trust | Cloudflare Access — only authorised agents and client can access tunnel |
| **Read-only enforcement** | Database-level | Read-only database users, read-only API scopes |
| **AI safety** | Prompt injection prevention | AI firewall layer between sidecars and core systems |
| **Audit trail** | Complete provenance | Every data read, every action, every reconciliation logged with timestamp and source |
| **Data sovereignty** | Client owns their data | Client can disconnect, export, or delete at any time. No lock-in. |

### PicoClaw as the Security Boundary

For Tier 3+ clients, PicoClaw acts as the Gatekeeper. It sits on the client's own infrastructure and enforces:

1. **P2 tokenisation**: Personal data (names, addresses, phone numbers, financial figures) is tokenised before crossing the tunnel. Raw values stay on the client's machine.
2. **Data cleaning**: Extracted data is validated and cleaned at source, not in the cloud.
3. **Consent enforcement**: PicoClaw logs what data it has accessed, when, and why. The client can review this log at any time.
4. **Kill switch**: The client can shut down PicoClaw at any time. The tunnel closes. Our cloud agents lose access to their systems immediately. Their data remains on their machine.

---

## Mapping to Pricing Tiers

| Integration Feature | FREE | £99 | £295 | £595 | £1,595 | £2,995 |
|---|---|---|---|---|---|---|
| API connectors (Xero, QB, etc.) | Companies House only | Yes (read-only) | Yes (read-only) | Yes (read + write) | Yes (read + write) | Yes (read + write) |
| WhatsApp Business API | No | Yes | Yes | Yes | Yes | Yes |
| Voice interface | No | Yes | Yes | Yes | Yes | Yes |
| PWA (The Pulse, phone) | Financial Autopsy only | Yes | Yes | Yes | Yes | Yes |
| Web dashboard (Command Centre) | No | No | No | Yes | Yes | Yes |
| MCP server connections | No | No | No | Yes | Yes | Yes |
| Cloudflare Tunnel | No | No | No | Yes | Yes | Yes |
| PicoClaw on-premise | No | No | No | Yes | Yes | Yes |
| Direct database read | No | No | No | Yes | Yes | Yes |
| Shadow mode reconciliation | In Financial Autopsy | Basic (API match) | Basic (API match) | Full (all sources) | Full (all sources) | Full (all sources) |
| Strangler Fig migration | No | No | No | Optional | Optional | Optional |
| P2 tokenisation | No | No | No | No | Yes | Yes |
| Multi-location sync | No | No | No | No | Yes | Yes |

---

## Implementation Priority for Jesmond Plumbing Pilot

Dave Jesmond. Deadline 25 March 2026. STABLE classification. Death spiral score: 10.

For Dave, the integration layer is simple:

1. **Xero OAuth** — Connect to Dave's Xero. Read-only. Pull 5 years of accounting data. (This is already partially done per COV-256.)
2. **WhatsApp Business API** — Dave's primary communication channel. Voice + text commands.
3. **PWA** — Install The Pulse on Dave's phone. Morning Briefing flow. Cash position. Invoice status. Schedule.
4. **Shadow mode** — Week 1-2: The Pulse shows Dave his data. He checks it against his Xero app. Reconciliation report runs daily. Any discrepancy investigated.
5. **Trust ramp** — Week 3-4: "Shall I send this invoice?" "Shall I schedule this appointment?" Dave says yes or no.
6. **Supervised autonomy** — Month 2: Auto-invoicing with morning review. Auto-scheduling confirmations with override.

Dave does not get PicoClaw. Dave does not get MCP servers. Dave does not get a Cloudflare Tunnel. Dave gets his phone, his voice, and a screen that shows him his business clearly for the first time.

That is the Schumacher Principle applied: right-sized technology, appropriate to the business.

---

## Summary: What the Integration Layer Actually Is

It is a sidecar. It reads from their existing systems through API connectors, MCP servers, secure tunnels, and read-only database connections. It builds an intelligence layer (the business brain) from that data. It presents that intelligence on a screen (The Pulse / Command Centre) that runs alongside their existing tools. It runs in shadow mode first so they can verify we are right. It uses automated reconciliation to prove data accuracy. It ramps trust gradually, from read-only observation to assisted action to supervised autonomy. It never replaces their systems unless they choose to replace them. It is their data, their business, their decision.

We do not touch their infrastructure. We sit beside it.

---

## Sources

All claims in this document are backed by research. Full URLs included inline throughout.

| Source | What It Covers |
|---|---|
| [Baytech Consulting — AI Sidecar Pattern](https://www.baytechconsulting.com/blog/minimize-risk-maximize-roi-with-sidecars) | Sidecar architecture, read-only connectors, RAG pipeline, cost comparison vs full rewrites |
| [Microsoft Azure Architecture Center — Sidecar Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar) | Formal sidecar pattern definition, language independence, shared resource access |
| [Thoughtworks — MCP Impact 2025](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025) | MCP as the key integration story of 2025 |
| [Fenxi — MCP Connecting AI to Business Tools 2026](https://fenxi.fr/en/blog/mcp-model-context-protocol-connecting-ai-business-tools-2026/) | MCP architecture (host, client, server), practical business integration |
| [Cloudflare Docs — Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/) | Secure outbound-only tunnel, zero inbound ports, firewall configuration |
| [DevOps.com — Shadow Deployment](https://devops.com/what-is-a-shadow-deployment/) | Shadow deployment definition, parallel running, output comparison without risk |
| [Confluent — The Dual-Write Problem](https://www.confluent.io/blog/dual-write-problem/) | Dual-write problem, transactional outbox pattern, event sourcing |
| [AuthZed — The Dual-Write Problem](https://authzed.com/blog/the-dual-write-problem) | Event sourcing, CQRS, durable execution environments |
| [Technori — Strangler Fig Pattern](https://technori.com/news/strangler-fig-pattern/) | Incremental modernisation, routing layer, zero-risk migration |
| [Kai Waehner — Replacing Legacy Systems with Data Streaming](https://www.kai-waehner.de/blog/2025/03/27/replacing-legacy-systems-one-step-at-a-time-with-data-streaming-the-strangler-fig-approach/) | Strangler Fig with Kafka/Flink, enterprise case studies |
| [Future Processing — Strangler Fig Pattern](https://www.future-processing.com/blog/strangler-fig-pattern/) | Gradual modernisation, routing layer, data consistency during coexistence |
| [IBM — Single Pane of Glass](https://www.ibm.com/think/topics/single-pane-of-glass) | Unified dashboard definition, SPOG benefits, integration with third-party apps |
| [Monte Carlo Data — Data Reconciliation Guide](https://www.montecarlodata.com/blog-data-reconciliation/) | Reconciliation methodology, match rates, discrepancy classification, automation |
| [LogRocket — Next.js 16 PWA with Offline Support](https://blog.logrocket.com/nextjs-16-pwa-offline-support/) | Offline-capable PWA, IndexedDB local storage, auto-sync on reconnect |
| [Next.js Docs — Progressive Web Apps](https://nextjs.org/docs/app/guides/progressive-web-apps) | PWA support in Next.js, Serwist integration, security considerations |
| [Monterail — PWA Examples 2026](https://www.monterail.com/blog/pwa-examples) | PWA business results, cross-device capability, no app store needed |
| [Unified Infotech — PWAs in 2026](https://www.unifiedinfotech.net/blog/pwa-revolution-in-modern-businesses/) | PWA market size ($7B+ by 2033), AI integration, offline evolution |
| [Koru UX — Voice UX Design](https://www.koruux.com/ux-voice/) | Voice interface design for B2B, real-world use cases |
| [Naskay Tech — Voice User Interfaces 2025](https://naskay.com/blog/voice-user-interfaces-2025-smarter-touchless-design/) | VUI design principles, context awareness, feedback loops |
| [TheFinch Design — VUI Best Practices 2026](https://thefinch.design/voice-user-interface-design-best-practices-2026/) | Voice UI testing, usability, enterprise deployment |
| [Microservices.io — API Gateway Pattern](https://microservices.io/patterns/apigateway.html) | API gateway as single entry point, request aggregation, backend-for-frontend |
| [Microsoft Learn — API Gateway vs Direct Client Communication](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/architect-microservice-container-applications/direct-client-to-microservice-communication-versus-the-api-gateway-pattern) | Gateway routing, request aggregation, cross-cutting concerns, Strangler Fig integration |
| [Getint — Integration Middleware Guide](https://www.getint.io/blog/what-is-integration-middleware) | Hub-and-spoke architecture, format translation, hybrid/legacy integration |
| [Acceldata — Agentic AI Reconciliation](https://www.acceldata.io/blog/the-future-of-recon-workflows-how-agentic-ai-delivers-autonomous-data-reconciliation) | Shadow mode validation, autonomous reconciliation, pattern matching |

---

*"Their business. Their smell. Their signature. We de-friction the journey. We don't drive the car."*
