---
title: "Database Architecture Context — Amplified Partners"
id: "database-architecture-context-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Database Architecture Context — Amplified Partners
**Compiled:** 16 March 2026  
**Scope:** All vault documents + GitHub repository evidence  
**Purpose:** Complete intelligence brief on database decisions, architecture patterns, addition pipeline, and rubrics for technology decisions  
**Sources:** FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md, Sovereign-OS-architecture-and-MVP-validation-2026-03-07.md, Unified-sovereign-engine-specification-2026-02-27.md, Local-and-cloud-infrastructure-2026-01-18.md, Data-quality-and-ethical-mining-principles-2026-01-20.md, Unified-Deployment-Briefing-2026-02-28.md, research-database-architecture.md, research-knowledge-graph-systems.md, GitHub repo ewan-dot/amplified-partners (all vault categories)

---

## SECTION 1: Current State of Database Decisions

### What Is Decided (Locked)

| Decision | Choice | Decided | Evidence |
|---|---|---|---|
| Primary graph engine | **FalkorDB** (specified) | COV-173, 2026-03-11 | FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md; DEPLOY_GUIDE.md shows live Railway instance |
| Knowledge graph framework | **Graphiti by Zep** | COV-173, 2026-03-11 | FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md |
| Vector database policy | **Drop Qdrant** (decommission) | 2026-03-11 | "FalkorDB + Graphiti. Drop Qdrant. Not a combination of all three." |
| Multi-tenancy model | Per-customer named graph (`kg_bob_plumber`) | COV-173 | Schema design documented: 10,000+ isolated graphs per instance |
| Graph storage port | Redis-compatible port 6379 | DEPLOY_GUIDE.md | Live: `https://falkordb-production-3bb7.up.railway.app` |
| Query language | OpenCypher (Cypher-compatible) | Arch spec | Same as Neo4j tooling — community compatibility |
| Temporal framework | Graphiti bi-temporal edges (`valid_at` / `invalid_at`) | Arch spec | Financial Autopsy engine — "what was true in March 2024?" |
| Agent runtime | OrbStack on Mac Mini M4 (NOT Docker Desktop) | DEPLOY_GUIDE.md | Docker Desktop crashes on Apple Silicon — switched to OrbStack |
| Relational layer | **PostgreSQL** on Railway | DEPLOY_GUIDE.md | `postgresql://...@hopper.proxy.rlwy.net:57736/railway` — LIVE |
| PostgreSQL multi-tenancy | Row-Level Security (RLS) + tenant_id | research-database-architecture.md | Default; schema-per-tenant for large clients |

### What Is In Tension (The Honest Picture)

The architecture documents are in direct conflict. Two separate research tracks reached opposing recommendations:

**Track A — Architecture Specification (COV-173, March 2026):** FalkorDB + Graphiti, drop Qdrant. Rationale: single engine, sub-10ms queries, native multi-tenancy, GraphBLAS performance, FalkorDB is the sole living Redis graph module.

**Track B — Deep Research Report (March 2026, research-knowledge-graph-systems.md):** Replace FalkorDB with Neo4j, retain Graphiti, add Qdrant back. Rationale: FalkorDB has failed five times, multiple open crash bugs, Graphiti+FalkorDB multi-tenancy routing bug makes normal operation fail silently.

**The gap: COV-173 specifies the system as if FalkorDB is stable. The research report documents why it is not.** This is the core open question.

---

## SECTION 2: FalkorDB Crash Bug Evidence

This is the complete catalogue from research-knowledge-graph-systems.md (March 2026):

### Confirmed Open Crash Bugs in FalkorDB (GitHub Issues as of March 2026)

| Issue | Severity | Status | Description |
|---|---|---|---|
| **#1666** | High | Open | Random crashes when `CMD_INFO` Redis config is enabled — crashes in the info reporting code path |
| **#1572** | Critical | Open (Feb 2026) | Use-after-free crash on node deletion — deleting a node then accessing its relationship in same query causes SIGSEGV |
| **#1481** | Critical | Open (Dec 2025) | Server crashes on nested `reduce()` operations — memory corruption at 3-level nesting |
| **#1321** | Medium | Closed (Oct 2025) | Crash on `DISTINCT + SKIP + LIMIT + WHERE` inside subquery — any one element removed prevents crash |
| **#1240** | Critical | Open (Aug 2025) | Multiple concurrent connections → crash with signal 11 (SIGSEGV) — **high-probability failure in multi-agent systems** |
| **#1231** | High | Open (Aug 2025) | Signal 11 crash after upgrade to v4.10.1 / v4.12.3 |
| **#1204** | Critical | Open | RESTORE command itself crashes FalkorDB — backup/restore operations unreliable |
| **#1158** | Medium | Open | Sequence of normal queries causes crash (not reproducible with individual queries) |
| **#897** | High | Open (Jan 2025) | Crash on Bolt protocol client disconnect |

### Graphiti + FalkorDB Integration Bugs

| Issue | Severity | Status | Description |
|---|---|---|---|
| **#1325** | Critical | Open (March 2026) | `handle_multiple_group_ids` routing bug — `if len(group_ids) > 1` should be `>= 1`. For single group_id (the standard case), routing falls through to `default_db` which is empty. **This causes silent failure on every normal query.** |
| **#1161** | Critical | Open (Jan 2026) | FalkorDB search fails with single group_id — driver not cloned. Related to #1325. |

### What This Means

The FalkorDB architecture specification (COV-173) was written assuming stability that the implementation does not yet have. The stack has "failed five times" per the research report. The most dangerous bug (#1325) means single-tenant queries silently return empty results — the kind of failure that looks like a code problem, not a database problem.

**The production risk:** Any of issues #1240 (multi-connection SIGSEGV), #1572 (use-after-free), or #1325 (routing bug) can cause system failures that are difficult to diagnose. The RESTORE crash (#1204) means that if a FalkorDB instance goes down, recovery from backup may also fail.

---

## SECTION 3: Neo4j Migration Path

### The Research Report Recommendation (research-knowledge-graph-systems.md)

**Replace FalkorDB with Neo4j Enterprise 5.26+.** Rationale (from comparison table, score 27/30 vs FalkorDB's lower score):

1. FalkorDB has active SIGSEGV crash bugs making it unsuitable for mission-critical data
2. Graphiti's primary and most-tested backend is Neo4j — not FalkorDB
3. The FalkorDB+Graphiti multi-tenancy routing bug (#1325) causes silent failure on normal operation
4. Neo4j has full ACID transactions; FalkorDB inherits Redis's weaker consistency model
5. Neo4j has online hot backup in Enterprise; FalkorDB's RESTORE command crashes

### Neo4j vs FalkorDB Comparison (from research-database-architecture.md)

| Dimension | FalkorDB | Neo4j |
|---|---|---|
| Architecture | In-memory, Redis-native, sparse matrices | Native graph engine, disk-backed |
| Multi-tenancy | Native 10,000+ isolated graphs | Enterprise only (RBAC + separate databases) |
| Query language | OpenCypher compatible | Cypher (authoritative) |
| P50 latency | 55ms | 577ms |
| P99 latency | 136ms | 46,923ms |
| Known crash bugs | **YES — multiple open** | Minor (JVM OOM on misconfiguration) |
| ACID transactions | Redis semantics (not full ACID) | Fully ACID-compliant |
| Production readiness | LOW-MEDIUM (active crash bugs) | HIGH (17-year track record) |
| Open source | Yes (Apache 2.0) | Community + paid Enterprise |

### Neo4j Failure Modes to Mitigate

These must be configured against if migrating:

- **Community Edition — single database only:** Neo4j Community cannot create multiple databases. Use Enterprise or DozerDB plugin (free, GPL) to add multi-database to Community.
- **Too many open files at 250+ databases:** OS-level fix — `ulimit -n 65536` in container.
- **OutOfMemoryError on JVM:** Configure `server.memory.heap.max_size=16g` + `server.memory.pagecache.size=64g` on Hetzner 256GB server.
- **GC pause storms:** Use G1GC or ZGC, keep heap under 16GB.
- **Volume mount permissions:** Neo4j runs as UID 7474 — host directories must be `chown 7474:7474`.
- **Graphiti+Neo4j latency:** `build_indices_and_constraints` must be called once at startup, not per request. Users report 50-second retrievals when called per request.

### Documented Migration Path (research-knowledge-graph-systems.md)

**Phase 1 (Week 1):** Deploy Neo4j Enterprise 5.26+ in Docker alongside existing FalkorDB. Validate Graphiti connects to Neo4j backend with `group_id` multi-tenancy.

**Phase 2 (Weeks 2-3):** Switch Graphiti backend from FalkorDB to Neo4j. Parallel-run both. New ingestion goes to Neo4j.

**Phase 3 (Weeks 3-4):** Re-ingest episodes through Graphiti with Neo4j backend (`reference_time` parameter preserves temporal metadata). Validate entity and relationship counts match.

**Phase 4:** Decommission FalkorDB. Keep Qdrant as dedicated vector layer for high-recall semantic search.

**Cost Note:** Neo4j Enterprise ~$36,000/year OR use DozerDB (free, GPL) to add multi-database to Community Edition at $0 software cost.

---

## SECTION 4: Qdrant Status

### In COV-173 Architecture Specification (March 2026)
**Decommission Qdrant.** Reasoning:
- FalkorDB's native HNSW vector search makes Qdrant redundant
- Running both means two databases doing overlapping work
- Two containers to maintain, two failure modes
- Cross-system latency on combined graph+vector queries (common query pattern)
- "Two queries, two engines, network roundtrip between them" vs "one query, one engine, sub-10ms"

### In Research Report (March 2026, research-knowledge-graph-systems.md)
**Reinstate Qdrant.** Reasoning:
- Qdrant written in Rust — no GC pauses, no memory corruption bugs
- If migrating away from FalkorDB, vector search capability must come from somewhere
- Qdrant + Neo4j = the recommended production stack
- pgvector + pgvectorscale recommended as first choice up to ~50M vectors (471 QPS vs Qdrant's 41 QPS at 50M vectors), then Qdrant for beyond

### Current Live Status
Qdrant is **still running** on Railway at `https://qdrant-production-5c39.up.railway.app` (v1.17.0) — it has not been decommissioned. It remains in the infrastructure reference (vault/09-infrastructure/INFRASTRUCTURE_REFERENCE.md).

### Early History
Qdrant was the original vector database (Jan 2026). The Local-and-cloud-infrastructure doc references 14,581 vectors already indexed (expert principles from Godin, Dalio, Kennedy, Gerber, Ziglar, Lund; Business Bible; session transcripts; CRM docs; voice memos). This live data exists in Qdrant and has not been migrated.

---

## SECTION 5: Graphiti Status

### What Graphiti Is
Graphiti by Zep is a temporal knowledge graph framework that sits on top of a graph database (Neo4j or FalkorDB). It handles:
- Episodic ingestion — feed it conversations, documents, events; it extracts entities, relationships, and facts automatically
- Bi-temporal edges — every relationship has `valid_at` (when it became true) and `invalid_at` (when it stopped being true)
- Entity resolution — "Bob Smith", "Bob", "Mr Smith", "the plumber" all resolve to the same node
- Contradiction detection — new data that contradicts old data invalidates old edge, creates new one

### Graphiti Decision: Retained in All Scenarios
Both the FalkorDB-first architecture and the Neo4j migration path retain Graphiti as the framework layer. It is the only element that is uncontested across both tracks.

### Graphiti Current Status
- Ingestion scripts built and committed to GitHub (`agent-stack/graphiti-ingestion/ingest_vault.py`)
- Linear issue COV-152 (Set up Graphiti + FalkorDB on Mac Mini) listed as backlog
- Vault ingestion not yet run — scripts ready but not executed
- Active bug #1325 (FalkorDB backend, group_id routing) affects current setup
- With Neo4j backend, #1325 does not apply

### Graphiti Framework-Level Bugs (Backend-Agnostic)
- Singleton anti-pattern: instantiate ONCE at startup — creates new indexes/constraints on every request if not done
- `build_communities` OOM: issues one query per entity — at 1,000+ entities, causes OOM kill
- Duplicate entities: entity deduplication is imperfect; duplicates accumulate over time
- Retrieval latency: 16-second retrievals remain even after singleton fix; full investigation needed

---

## SECTION 6: Architecture Patterns and Rubrics for Technology Addition

### The Addition Principle (Documented in Multiple Sources)

The core principle from the Sovereign OS architecture and operating model is:
> "We don't optimise the graph for our convenience — we optimise it for the customer's life goals."

Architecture addition decisions flow through a deterministic rubric before entering the stack. No new component enters without being tested against the system it replaces or augments.

### RUBRIC-REPLACE-OR-FIX (vault/03-frameworks-and-rubriks/RUBRIC-REPLACE-OR-FIX.md)
The explicit documented rubric for technology addition decisions:

**Trigger:** Something breaks for the third time.

**The Five Questions:**
1. Have we diagnosed the actual cause of failure?
2. Is this a fixable config issue, or is it the tool being the tool?
3. What does the community say — is this a known problem with this tool?
4. Is there a better alternative with a stronger track record?
5. What's the cost of switching vs cost of continued failures?

**Decision rule:** If answers to 2, 3, and 4 all point the same way — switch. If uncertain — diagnose properly before deciding.

**Applied to FalkorDB:** Questions 2 (yes, it's the tool — C memory bugs), 3 (yes — community confirms SIGSEGV issues), and 4 (yes — Neo4j has 17-year track record) all point the same way. The rubric says: switch.

**Current Docker Desktop example from the doc:** Kept going down on Mac Apple Silicon. Community confirmed known issue. OrbStack adopted as replacement. This switch has already happened.

### ATTRIBUTION-FIRST RUBRIC SYSTEM (vault/20-staging-archive/00-rubric-multiplier-v2.md)
The master rubric for all technology and data additions — uses multiplication not addition:

```
MULTIPLIER = Attribution × Expert × Logic × Discovery × Validation
           = (Source × Date × Method) × Expert × (Presence × Completeness) × Tags × Status
```

**Maximum possible score: 26,244 (3×3×3×3×3×3×3×3×4)**

**Tiers:**
| Tier | Score Range | Action |
|---|---|---|
| GOLD | 5000+ | Deploy to production |
| SILVER | 1000-4999 | Ready for testing |
| BRONZE | 100-999 | Needs enrichment |
| RAW | 1-99 | Triage, human review |
| VOID | 0 | Cannot proceed — any zero in attribution zeros everything |

**Why multiplication, not addition:** A zero at any layer zeros the result. Partial data has partial value. Complete data has exponential value. This forces completeness across all five layers.

### The Five Multiplication Layers for Technology Decisions

**Layer 1 — Attribution (Foundation):** Can we trace WHERE this technology recommendation came from, WHEN the benchmark was run, and HOW the comparison was done?

**Layer 2 — Expert Source (Authority):** Is this recommendation backed by recognised experts? (Graphiti/Zep team, Neo4j docs, independent benchmarks — not vendor marketing alone)

**Layer 3 — Decision Logic (Automation layer):** Is there a clear IF-THEN logic? (IF FalkorDB crashes 3 times AND community confirms bug → SWITCH)

**Layer 4 — Semantic Tags (Discovery):** Does this technology plug into the existing domain tags? (graph, temporal, multi-tenant, GDPR-sovereign)

**Layer 5 — Synthesis/Validation:** Has this been tested? (Hypothesis → Tested Internal → Tested Client → Proven → Canonical)

### Master Rubric: Law Alignment (from Data Quality doc)

| Criterion | Question | Score 1-5 |
|---|---|---|
| Friction Reduction | Does this make life easier? | |
| Vision Alignment | Does this serve their goals? | |
| Joy Factor | Does this add or remove stress? | |
| Excellence Impact | Does this help them be better? | |
| Transparency | Can they see how it works? | |
| Honesty | Does it tell the truth? | |
| Measurability | Can we tell if it's working? | |

**Total: /35**
- 28+ → Core, automate it
- 21-27 → Active, use with care
- 14-20 → Review, improve or remove
- Below 14 → Archive or delete

---

## SECTION 7: The Addition Pipeline — How New Software Gets Tested

### Documented Pipeline Stages (from multiple vault sources)

The "addition pipeline" is not named explicitly as a single document but is the composite of documented processes:

**Stage 0: Principle Check**
Any new software addition must pass the Law alignment rubric first. Does it reduce friction? Does it serve customer life goals? Does it maintain data sovereignty?

**Stage 1: Research Before Invention**
Operating principle #12 from The Law: "Research before invention." Before building or buying, Perplexity (Kimmy) and Claude do exhaustive research. The research-database-architecture.md and research-knowledge-graph-systems.md files are examples of this stage running.

**Stage 2: Attribution-First Scoring**
Every evaluated technology gets scored on the RUBRIC-REPLACE-OR-FIX and attributed with source, date, and method. No technology enters without a score.

**Stage 3: Dog-Food Principle**
From FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md:
> "What we build for ourselves IS the product. Our internal knowledge graph (`kg_internal`) uses exactly the same schema, the same Graphiti ingestion, the same rubriks, the same MCP servers that customers will use. If it doesn't work for us, it doesn't ship."

New software must first prove itself on `kg_internal` before entering customer-facing infrastructure.

**Stage 4: Shadow Phase**
From Sovereign OS architecture — the Shadow Alpha model:
- New technology runs silently in parallel with existing (shadow, no action)
- Outcomes are observed without interfering with live system
- Validated before cutover

**Stage 5: Validation Against Failure Modes**
The knowledge graph research report demonstrates this stage — it catalogues every known failure mode of every evaluated technology before a final recommendation. Nothing is adopted without understanding its crash modes.

**Stage 6: Migration Path with Rollback**
All migrations documented with parallel-run phases. Example from FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md (Qdrant → FalkorDB migration path):
- Phase 1: Parallel running (weeks 1-3)
- Phase 2: Gradual cutover (weeks 3-6) — old system becomes read-only fallback
- Phase 3: Decommission (week 7+) only after full verification

**Stage 7: Kaizen Loop**
From SOUL.md principle: "Digital Kaizen / PDCA for AI Ops." Continuous improvement loop. Failures are published (Principle 6 from SOUL.md: "Shock test results published every Monday. Failures included.").

### Documented Addition Pipeline Applied to FalkorDB (Historical)

| Stage | What Happened | Evidence |
|---|---|---|
| Research | Perplexity confirmed FalkorDB is the sole living Redis graph module; verified RedisGraph EOL Jan 2025 | Sovereign OS doc — "Radical Transparency Check" |
| Attribution | FalkorDB capabilities attributed to FalkorDB team; Graphiti attributed to Zep; benchmarks cited with source | FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md attribution block |
| Dog-food | `kg_internal` designed to use the same stack as customer graphs | COV-173 spec |
| Failure mode analysis | 10 open crash bugs catalogued; Graphiti routing bug identified | research-knowledge-graph-systems.md |
| Rubric check | RUBRIC-REPLACE-OR-FIX: all three questions point to switch | Implicit — not yet formally applied to FalkorDB |

**Status:** The pipeline has been run and has returned a "switch" verdict. The switch has not yet been executed.

---

## SECTION 8: Database Technology Timeline (Chronological)

Understanding the history prevents repeating it:

| Date | Technology | Status | Notes |
|---|---|---|---|
| Jan 2026 | Neo4j AuraDB + Qdrant + Pinecone + Weaviate | Setup | Four separate databases for expert principles, graphs, vectors |
| Jan 2026 | Neo4j (local Docker) | Installed | M4 chip compatibility fix applied |
| Jan 2026 | 14,581 vectors | Indexed in Qdrant | Expert principles (6 experts), Business Bible, voice memos |
| Jan 2026 | Neo4j considered for GraphRAG | Active | 1.5-3.4× better accuracy than vector-only on complex queries |
| Feb 2026 | OpenClaw architecture specified | Active | Qdrant + Neo4j + Postgres |
| Feb 2026 | FalkorDB confirmed sole Redis graph module | Decision | RedisGraph EOL confirmed; FalkorDB is the only fork |
| Feb 2026 | FalkorDB + Graphiti adopted as stack | Decision COV-173 | Replaces Neo4j + Qdrant |
| Feb 2026 | Railway deployment | Live | FalkorDB + Qdrant + PostgreSQL all deployed on Railway |
| Mar 2026 | Qdrant decommission planned | Specified | COV-173 migration path documented |
| Mar 2026 | FalkorDB fails 5 times | Evidence | Crash bugs catalogued in research-knowledge-graph-systems.md |
| Mar 2026 | Neo4j migration path researched | Research complete | research-knowledge-graph-systems.md — Neo4j recommended |
| Mar 2026 | Graphiti ingestion scripts built | COV-165, ready | Not yet run; scripts in agent-stack/graphiti-ingestion/ |
| Mar 2026 | **Current state** | Unresolved | FalkorDB live, known bugs, migration path documented but not executed |

---

## SECTION 9: Scoring Frameworks for Technology Decisions

### The Word of the Pudding — Data Quality Rubric

Governs how any new data (including technology benchmarks) enters the system:

**A. Every Piece Is Scored**
| Score | Meaning | Minimum for |
|---|---|---|
| 5 | Gold — primary source, verified, actionable, reusable | Client-facing use |
| 4 | Strong — reliable source, minor gaps | Automation |
| 3 | Usable — needs context, some inference | Use in system |
| 2 | Weak — secondhand, partial | Not for automation |
| 1 | Raw — unverified fragment | Triage only |

**B. Every Piece Is Attributed** (WHO, WHEN, HOW — all mandatory)

**C. Neutral Labelling** — functional, descriptive labels only; no loaded terms

**D. Transparent Process** — provenance chain traceable from source through every transformation

### Data Quality Rubric (Scoring for Approval)

| Criterion | Score 1-5 |
|---|---|
| Attribution completeness (source, date, method present) | |
| Attribution confidence (how certain is the provenance) | |
| Content clarity (meaning unambiguous) | |
| Actionability (can someone act on this) | |
| Reusability (applies beyond one case) | |
| **Total: /25** | |

Thresholds:
- 20+ = Green — ready for use
- 15-19 = Amber — needs review
- Below 15 = Red — re-gather or discard

### RAG Quality Rubric (for knowledge chunks entering the system)

From vault/21-infra-research/rubric-system-complete-v1.md — three rubrics for three content types, refined through Claude + Perplexity collaboration.

**Chunk Quality Test:**
| Criterion | Question |
|---|---|
| Completeness | Does it stand alone? |
| Coherence | Makes sense without context? |
| Right Size | Not too big, not too small? |
| Sticky | Will it cluster with related chunks? |

---

## SECTION 10: Architecture Decisions Still Open (Gaps)

### Gap 1: FalkorDB vs Neo4j — No Final Verdict Executed

**What's documented:** Both the keep-FalkorDB spec (COV-173) and the switch-to-Neo4j research report exist. The RUBRIC-REPLACE-OR-FIX, when applied, points to switching. The migration path is documented. But no commit has been made to execute the switch.

**Decision needed:** Is FalkorDB staying or going? The answer determines whether Qdrant returns, whether existing Railway FalkorDB instance becomes the migration source or the target, and whether COV-152 (Graphiti + FalkorDB Mac Mini setup) should be paused.

### Gap 2: Qdrant — Decommission or Reinstate

**What's documented:** COV-173 says decommission. The research report says reinstate (as the vector layer if switching to Neo4j). Qdrant is currently still live on Railway with 14,581+ vectors already indexed.

**Decision needed:** Does Qdrant stay? If FalkorDB stays, it goes. If Neo4j replaces FalkorDB, it stays and grows.

### Gap 3: Graphiti Vault Ingestion — Not Yet Run

**Status:** COV-165 scripts are built and committed. COV-152 (Graphiti+FalkorDB on Mac Mini) is in backlog. The 517 vault files (1.8M words) have not been ingested into any graph database yet.

**Blocker:** Running ingestion on a FalkorDB backend with active bug #1325 means the data may ingest but queries will fail silently. If switching to Neo4j, ingestion should wait for the new backend.

### Gap 4: Neo4j Enterprise vs Community + DozerDB

**What's documented:** Enterprise costs ~$36,000/year. DozerDB (GPL, free) adds multi-database to Community. The research report recommends Enterprise but acknowledges DozerDB as a viable alternative.

**Decision needed:** Budget decision. For <100 customers, DozerDB + Community is likely sufficient.

### Gap 5: Hetzner vs Railway for Production Graph Layer

**What's documented:** Hetzner AX162-R (48-core EPYC, 256GB RAM, 135.181.161.131) is available and sized for production (256GB RAM handles all SMB client graphs with room). Railway is the current host of FalkorDB but is a cloud PaaS with less control.

**Decision needed:** When does the graph layer migrate from Railway to Hetzner bare metal? The research architecture spec assumes Hetzner as the central server.

### Gap 6: PostgreSQL Role vs Graph Layer

**What's documented:** PostgreSQL on Railway is live and tested (14/14 tests passing as of March 2026). The relational layer handles CRM, call webhook, accountability agent, and structured transactional data. The graph layer handles knowledge graph, temporal business intelligence, and entity relationships.

**No conflict here** — both are needed and their roles are distinct. The open question is whether pgvector+pgvectorscale should replace Qdrant for the sub-50M vector range (research shows 11× higher throughput than Qdrant at 50M vectors, and PostgreSQL is already deployed).

### Gap 7: The Addition Pipeline Is Not Formally Documented as a Single Process

The pipeline is implied across multiple documents but never written as one SOP. The RUBRIC-REPLACE-OR-FIX gives the decision logic. The "eating our own dog food" principle gives the validation stage. The Shadow Alpha model gives the parallel-run stage. But there is no single canonical "how a new piece of software enters the Amplified Partners stack" document.

---

## SECTION 11: Database Schema Reference (COV-173 Design)

Five domains of the knowledge graph — documented in FALKORDB-GRAPHITI-ARCHITECTURE-2026-03-11.md:

**Domain 1: Conversations (Episodic Memory)**
- Nodes: Episode, Person, Topic, Decision, Action, Sentiment
- Edges: DISCUSSED, DECIDED, ASSIGNED_TO, FOLLOWS_UP, RELATES_TO
- Temporal: Every edge has `valid_at`, episodes chronologically linked

**Domain 2: Documents (Versioned Knowledge)**
- Nodes: Document, Version, Entity, Amount, Date, Category
- Edges: HAS_VERSION, MENTIONS, INVOICED_TO, PAID_BY, CATEGORISED_AS
- Temporal: Versions tracked with `valid_at`/`invalid_at`; superseded documents marked

**Domain 3: Operational Data (State Transitions)**
- Nodes: Business, Metric, State, Alert, RubrikScore
- Edges: HAS_METRIC, SCORED_BY, TRIGGERED, TRANSITIONED_TO
- Temporal: Every state change is a new edge; old states invalidated, never deleted

**Domain 4: Expert Frameworks (Principle Hierarchies)**
- Nodes: Expert, Principle, Rubrik, Domain, Metric
- Edges: AUTHORED, APPLIES_TO, SCORES_WITH, DERIVED_FROM
- Temporal: Principles timeless (no invalid_at); their application to specific businesses is temporal

**Domain 5: Cross-Domain (PUDDING Labels)**
- Nodes: PuddingLabel, Concept, Connection
- Edges: LABELLED_AS, CONNECTS_TO, MASHUP_SCORE
- Temporal: Connections discovered over time; scores evolve

**Multi-Tenant Isolation:**
```
FalkorDB Instance
├── kg_internal          # Dog-food graph (our own business)
├── kg_bob_plumber       # Customer 1 graph
├── kg_janes_restaurant  # Customer 2 graph
├── kg_federated         # Anonymised aggregates (Tier 3)
└── kg_expert_library    # Shared: 27 experts, principles, rubriks (read-only)
```

---

## SECTION 12: Live Infrastructure State (March 2026)

### Railway (Cloud PaaS) — Currently Live
| Service | URL / Connection | Status |
|---|---|---|
| PostgreSQL | `postgresql://...@hopper.proxy.rlwy.net:57736/railway` | LIVE (14/14 tests passing) |
| FalkorDB | `https://falkordb-production-3bb7.up.railway.app` | LIVE (crash bugs unresolved) |
| Qdrant | `https://qdrant-production-5c39.up.railway.app` (v1.17.0) | LIVE (14,581+ vectors) |
| Redis | Internal Railway service | LIVE |
| Call Webhook | Railway-deployed Flask app | LIVE |
| Accountability Agent | Railway-deployed Flask app | LIVE |

### Mac Mini M4 (Local Dev / Agent Runtime)
- OrbStack installed (Docker Desktop replacement)
- Node.js v25.8.0, Railway CLI
- Agent stack: `~/amplifiedpartners/agent-stack/` — not yet started
- Graphiti ingestion scripts: ready but not run
- 2FA Railway lockout: email team@railway.com to resolve

### Hetzner
- AX162-R: 135.181.161.131 (48-core EPYC, 256GB RAM) — provisioned, role in production not yet defined
- Cloud server: 46.225.6.228

---

## SECTION 13: Recommended Next Actions (Synthesised from All Sources)

Based on all evidence, applying the RUBRIC-REPLACE-OR-FIX and Law alignment rubric:

**Priority 1 — Make the FalkorDB decision formally**
Apply RUBRIC-REPLACE-OR-FIX explicitly. FalkorDB has crashed 5+ times. Bugs #1240 (multi-connection SIGSEGV), #1572 (use-after-free), and #1325 (routing bug) are all open. Community confirms these are known issues. Neo4j alternative has been researched. The rubric says: switch.

**Priority 2 — If switching to Neo4j: use DozerDB for Community Edition**
Avoids the $36k/year Enterprise cost. DozerDB adds multi-database to Neo4j Community for free. This is the production-viable zero-cost path.

**Priority 3 — Pause Graphiti ingestion (COV-152) until graph backend is decided**
Running 517 files through Graphiti into a FalkorDB with active routing bugs (#1325) produces a graph that queries will silently fail on. Better to wait one week for the Neo4j decision, then ingest once into the correct backend.

**Priority 4 — Qdrant: keep it**
14,581 vectors already indexed. Railway instance is live. If switching from FalkorDB to Neo4j, Qdrant becomes the vector layer again (as the research report recommends). The Qdrant decommission plan was premised on FalkorDB being stable — that premise has failed.

**Priority 5 — Document the addition pipeline as a single SOP**
The rubric exists, the stages exist, but they need to be codified as one canonical process. Every new software addition should run through this SOP before being committed to the architecture spec.

---

## APPENDIX: Rubriks Currently in Production (vault/rubriks/ and Unified Deployment Briefing)

These are the 7 operational rubriks committed to GitHub:

| ID | Name | Trigger | Confidence Band |
|---|---|---|---|
| TRUST-IMMUTABLE-RUBRIK-11 | Immutable Truth Layer | Any output from the swarm | Non-negotiable |
| DANGER-SPIRAL-EXIT-12 | Death Spiral Early Warning | Any 2 of: revenue -10% MoM, footfall -15%, staff hours cut, owner below min wage, no marketing 30 days | High detection, Medium recovery |
| WOW-ZIGLAR-LUND-01 | Contagious Experience Architecture | Customer experience inconsistent | Medium-High |
| WOW-KENNEDY-GODIN-02 | Respectful Scarcity Campaign | Promotion response rates <8% | High |
| OPS-DALIO-GERBER-03 | Principles-First Franchise Loop | Owner is bottleneck (>80% open hours) | High |
| OFFER-HORMOZI-LUND-04 | Critical Non-Essential Grand Slam Offer | Conversion <20% or ATV stagnant 90+ days | Medium |
| MKTG-CIALDINI-GARYVEE-05 | Compounding Proof Engine | <5 new reviews in 30 days | High |

**Rubrik confidence threshold:** 0.98 (per `.env.example` — `RUBRIK_CONFIDENCE_THRESHOLD=0.98`)

---

*Compiled by research subagent, 16 March 2026. All findings sourced directly from vault documents and GitHub repository. Attribution: vault-docs/, research-database-architecture.md, research-knowledge-graph-systems.md, ewan-dot/amplified-partners GitHub repository.*
