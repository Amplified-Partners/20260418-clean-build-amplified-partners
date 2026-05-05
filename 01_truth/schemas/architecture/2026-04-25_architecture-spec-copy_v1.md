---
title: "BEAST INFRASTRUCTURE ARCHITECTURE SPECIFICATION"
id: "architecture-spec-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "architecture"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# BEAST INFRASTRUCTURE ARCHITECTURE SPECIFICATION

## Document Context

**For:** Ewan Bramley, Amplified Partners
**Date:** 16 March 2026
**Server:** Hetzner AX162-R (48-core AMD EPYC, 256GB DDR5 ECC RAM, 2×NVMe SSD, 10Gbps)
**IP:** 135.181.161.131 | **DNS:** *.beast.amplifiedpartners.ai
**OS:** Ubuntu 24.04 LTS
**Status:** Beast wiped clean — building from zero
**First Client Deadline:** Dave Jesmond / Jesmond Plumbing — 25 March 2026

## Core Philosophy (Non-Negotiable)

- AI is NOT the data layer. AI is the catalyst that surfaces data. Deterministic software underneath, MCP → database, known business rubrics. AI presents. Human decides.
- Nobody enters the environment except agents who live there. Everything documented and logged.
- Sovereign data layer: deterministic software, no AI at data storage level.
- Take advantage of prebuilt software wherever available (GitHub, npm, PyPI).
- Just because it's there doesn't mean we know what it's doing — verify everything.

---

## PART 1: CRITICAL FINDING — WHY THE VAULT FAILED 5 TIMES

### Root Cause Analysis

FalkorDB + Graphiti has 10+ active crash bugs. The most likely cause of the 5 failures is Graphiti Issue #1325 (March 2026): a routing bug in `graphiti_core/decorators.py` where `if len(group_ids) > 1` should be `>= 1`. For single group_id (the standard use case), FalkorDB routing falls through to `default_db` which is empty. ALL search, retrieve_episodes, and build_communities calls return empty results silently.

Additional FalkorDB crash bugs:
- Issue #1666: Random crashes when CMD_INFO enabled
- Issue #1572: Use-After-Free crash on node deletion (Feb 2026)
- Issue #1481: Server crashes on nested reduce() (Dec 2025)
- Issue #1240: SIGSEGV on multiple concurrent connections
- Issue #1056: FalkorDB blocks Redis event loop under heavy load
- Issue #1204: RESTORE command crashes FalkorDB (backups unreliable)
- Issue #897: Crash on Bolt protocol disconnect

**Decision: Replace FalkorDB with Neo4j 5.26+. Keep Graphiti framework. Keep Qdrant for vectors.**

---

## PART 2: COMPLETE SOFTWARE STACK

### Layer 1: Operating System & Filesystem

| Component | Choice | Rationale |
|-----------|--------|-----------|
| OS | Ubuntu 24.04 LTS | CIS Benchmark automation available via USG |
| Filesystem | XFS on mdadm RAID-1 mirror | Best SQLite writes, best random reads, Docker overlay2 compatible |
| Docker storage | overlay2 on XFS | Docker-recommended, ~50ms container startup |
| RAID | Software RAID-1 (mdadm) | NVMe drives — no hardware RAID available |
| Backup tool | restic | Append-only mode to Hetzner Storage Box + Backblaze B2 |

**Partition Layout:**
```
nvme0n1 + nvme1n1 (RAID-1 mirror via mdadm)
├── /boot/efi  (1GB, EFI)
├── /boot      (1GB, ext4, RAID-1)
├── swap       (32GB, RAID-1)
├── /          (100GB, XFS, RAID-1)
├── /var       (200GB, XFS, RAID-1) — logs, Docker metadata
├── /var/lib/docker (separate XFS, RAID-1)
└── /data      (remainder, XFS, RAID-1) — database volumes, backups
```

### Layer 2: Security & Anti-Sabotage

| Component | Choice | Purpose |
|-----------|--------|---------|
| OS hardening | CIS Level 1 via Ubuntu Security Guide (USG) | Automated hardening baseline |
| SSH | Key-only, no root, AllowUsers amplified-admin | Eliminate password attacks |
| Firewall | nftables (via Ansible) | Only ports 80, 443, SSH |
| Intrusion detection | Wazuh (SIEM + HIDS) | File integrity, rootkit detection, Docker monitoring |
| Container monitoring | Falco | Runtime container threat detection |
| Audit logging | auditd + eBPF | Kernel-level syscall monitoring |
| GitOps | Webhook-triggered Compose from GitHub | If it's not in git, it doesn't exist |
| Infrastructure as Code | Ansible playbooks in git | Full rebuild from `git clone && ./deploy.sh` in 15 min |
| Container images | Read-only root filesystems where possible | Prevent runtime tampering |
| Docker socket | Never mount to non-privileged containers | Prevent container escape |
| Secrets | git-crypt / SOPS → migrate to Vault later | Encrypted secrets in git |

### Layer 3: Databases

| Database | Version | Port | Purpose | Multi-tenancy |
|----------|---------|------|---------|---------------|
| **Neo4j** | 5.26+ Enterprise (or Community + DozerDB) | 7687/7474 | Knowledge graphs | Per-client databases (Enterprise) or DozerDB multi-DB plugin |
| **Qdrant** | Latest stable | 6333 | Vector embeddings | Collections per client + payload filtering |
| **PostgreSQL** | 17 | 5432 | Structured business data, rubrics, metrics | RLS + tenant_id (default); schema-per-tenant for large clients |
| **Redis** | 7.x | 6379 | Caching, sessions, queues | Separate from FalkorDB — clean Redis for caching only |

**Neo4j Configuration (256GB server):**
```
server.memory.heap.initial_size=8g
server.memory.heap.max_size=16g
server.memory.pagecache.size=64g
ulimit -n 65536 (prevent "too many open files" at 250+ databases)
```

**Critical: Pin Neo4j to 5.26+ — required for Graphiti vector index support. Never use `latest` tag.**

### Layer 4: Knowledge Graph Framework

| Component | Choice | Purpose |
|-----------|--------|---------|
| Framework | Graphiti by Zep (pinned version) | Temporal/bi-temporal knowledge graph, episodic ingestion |
| Graph backend | Neo4j (primary, most tested by Graphiti) | Replaces FalkorDB |
| Vector backend | Qdrant | High-recall semantic search |
| MCP server | Graphiti MCP Server (port 8000) | Agent access to knowledge graph |

**Pre-Solved Known Issues:**
1. Graphiti singleton: instantiate ONCE at startup, never per-request (prevents 30-40s delays)
2. build_communities: disable during ingestion, run as nightly background job (prevents OOM at 1000+ entities)
3. Pin version in requirements.txt — v0.18.x broke FalkorDB, v0.30.x broke Neo4j
4. Entity deduplication: add UNIQUE constraints on name+type combinations
5. Temporal decay: build manual pruning job (set t_invalid on old edges)
6. LLM reranking: disable for search — reduces latency from 16s to <2s

### Layer 5: MCP Servers (Pre-Built — Use What Exists)

**Accounting:**
| System | MCP Server | Source | Status |
|--------|------------|--------|--------|
| Xero | @xeroapi/xero-mcp-server (official) | github.com/XeroAPI/xero-mcp-server | Production — 30+ tools |
| QuickBooks | intuit/quickbooks-online-mcp-server (official) | github.com/intuit/quickbooks-online-mcp-server | Production |
| Sage 50 UK | CData sage-50-uk-mcp-server | github.com/CDataSoftware/sage-50-uk-mcp-server-by-cdata | Beta (read-only, needs licence) |

**Communication:**
| System | MCP Server | Source |
|--------|------------|--------|
| Gmail | GongRzhe/Gmail-MCP-Server | Python, OAuth 2.0, full CRUD |
| IMAP/SMTP | gomcpgo/email | Go, any IMAP server |
| Slack | modelcontextprotocol/servers (official) | Reference implementation |

**CRM:**
| System | MCP Server | Source |
|--------|------------|--------|
| HubSpot | peakmojo/mcp-hubspot | Python, FAISS vector cache, Docker |
| Salesforce | kablewy/salesforce-mcp-server | TypeScript, jsforce |

**Storage & Code:**
| System | MCP Server | Source |
|--------|------------|--------|
| Google Drive | modelcontextprotocol/servers | Official reference |
| GitHub | modelcontextprotocol/servers | Official reference |
| Filesystem | modelcontextprotocol/servers | Official reference |
| PostgreSQL | modelcontextprotocol/servers | Official reference |

**Payments:**
| System | MCP Server | Source |
|--------|------------|--------|
| Stripe | stripe/agent-toolkit | Official vendor |

**Custom builds needed:**
1. Sage Business Cloud MCP (REST API, FastMCP 2.0)
2. HMRC MTD MCP (Making Tax Digital API)
3. Companies House MCP (business verification)
4. WhatsApp Business MCP (message delivery)
5. TrueLayer/Plaid Open Banking MCP (financial data)

### Layer 6: Data Extraction Tools

| Tool | Purpose | Status |
|------|---------|--------|
| Docling (IBM) | Document extraction (PDF, DOCX, PPTX) | Open source, primary |
| Apache Tika | Broad format support (fallback) | Mature, 400+ formats |
| PaddleOCR | OCR for complex layouts | Best for invoices, receipts |
| Tesseract | OCR for clean text | Simpler, lighter |
| FastMCP 2.0 | Custom MCP server framework | 23,700+ stars, Python |

### Layer 7: Intelligence Pipeline (NightCrawler)

**Collection Tier:**
| Component | Purpose |
|-----------|---------|
| RSSHub | Universal feed generator (GitHub, Reddit, TikTok, Substack) |
| Miniflux | RSS aggregation and storage |
| Kill-the-Newsletter | Convert email newsletters to RSS |
| SearXNG (existing) | Ad-hoc deep search, gap-filling |

**Sources to Monitor (20+):**
- GitHub trending + release feeds for 200 key repos
- Hacker News top/show/best stories (every 6 hours)
- Reddit: r/MachineLearning, r/LocalLLaMA, r/selfhosted, r/docker, r/netsec + 10 more
- 25 AI/security newsletters via RSS (Import AI, The Batch, Interconnects, tl;dr sec, etc.)
- arXiv: cs.AI, cs.CL, cs.LG, cs.CR categories
- Product Hunt daily feed
- CVE/NVD security advisories

**Processing Tier:**
1. Collect → Miniflux aggregates all feeds
2. Classify → LLM triage into: Content Creation | R&D | Security | Ignore
3. Enrich → Entity extraction, PUDDING taxonomy labelling
4. Store → Neo4j (graph relationships) + PostgreSQL (structured records)
5. Route → Push to department-specific queues

### Layer 8: Networking & Tunneling

| Component | Purpose |
|-----------|---------|
| Traefik | Reverse proxy, auto-TLS via Let's Encrypt, wildcard *.beast.amplifiedpartners.ai |
| Tailscale | Private mesh between client connectors and Beast (NAT traversal, 20-40MB RAM) |
| Cloudflare Tunnel | Public-facing services (DDoS protection, outbound-only) |
| WireGuard | Direct VPN to Mac Mini M4 (OpenClaw) |

### Layer 9: Monitoring & Observability

| Component | Purpose |
|-----------|---------|
| Prometheus | Metrics collection (CPU, RAM, disk, container stats) |
| Grafana | Dashboards and alerting |
| Loki | Log aggregation |
| Wazuh | Security event monitoring (SIEM) |
| Uptime Kuma | Service health checks and uptime monitoring |

---

## PART 3: CONTAINER ARCHITECTURE (36+ Services)

### Core Infrastructure
1. traefik — Reverse proxy + TLS
2. neo4j — Knowledge graph database
3. qdrant — Vector database
4. postgresql — Relational data
5. redis — Caching + queues
6. wazuh-manager — Security monitoring
7. falco — Container runtime security
8. prometheus — Metrics
9. grafana — Dashboards
10. loki — Logs
11. uptime-kuma — Health checks

### Knowledge Graph & AI
12. graphiti-mcp — Graphiti MCP server (port 8000)
13. neo4j-mcp — Neo4j official MCP server
14. ollama — Local LLM inference (Llama 3, Mistral)
15. litellm — LLM API gateway (OpenAI, Anthropic, local models)

### Intelligence Pipeline (NightCrawler)
16. miniflux — RSS aggregation
17. rsshub — Universal feed generator
18. kill-the-newsletter — Newsletter → RSS converter
19. searxng — Meta-search engine (existing)
20. nightcrawler-collector — Custom: feed → classify → store
21. nightcrawler-router — Custom: route signals to departments

### Client Data Connectors
22. mcp-xero — Xero MCP server
23. mcp-quickbooks — QuickBooks MCP server
24. mcp-gmail — Gmail MCP server
25. mcp-hubspot — HubSpot MCP server
26. mcp-stripe — Stripe MCP server
27. mcp-sage — Custom Sage MCP (to build)
28. mcp-hmrc — Custom HMRC MTD MCP (to build)
29. mcp-companies-house — Custom Companies House MCP (to build)

### Data Processing
30. docling — Document extraction service
31. paddleocr — OCR service
32. tika — Apache Tika extraction (fallback)

### Orchestration & CI/CD
33. temporal — Workflow orchestration (Cove Code Factory)
34. temporal-worker — Cove build workers
35. watchtower — Auto-update containers from registry
36. registry — Private Docker registry

### Client-Facing
37. webhook-receiver — GitHub/CI webhook listener
38. whatsapp-gateway — WhatsApp Business API gateway

---

## PART 4: THREE-TIER ARCHITECTURE

### Tier 1: Client-Local (PicoClaw / Beelink N100)
- Docker Compose stack on client machine
- Local MCP servers (Xero, Sage, IMAP)
- Whisper transcription + P2 tokenisation (PII stripped at edge)
- Only structured, non-PII results sent to Beast via Tailscale
- Watchtower for zero-touch updates
- Cost: ~£200 hardware per client

### Tier 2: Partitioned Cloud (Beast / Hetzner AX162-R)
- Neo4j with per-client databases
- Qdrant with per-client collections
- PostgreSQL with RLS + tenant_id
- Graphiti framework layer
- NightCrawler intelligence pipeline
- All 38+ Docker containers
- Agent orchestration via Temporal

### Tier 3: Federated Hub (Future — Phase 3)
- Anonymised cross-client patterns only
- P2-tokenised aggregate data
- Differential privacy (not federated learning — overkill at SMB scale)
- kg_federated read-only graph
- Network effects: more clients = smarter insights for everyone

---

## PART 5: DEPARTMENT INTELLIGENCE FEEDS

The NightCrawler intelligence pipeline serves ALL 7 departments with tailored feeds:

### 1. R&D / Technology
- GitHub trending + release monitoring
- arXiv papers (cs.AI, cs.LG, cs.CL, cs.CR)
- Hacker News Show HN
- r/MachineLearning, r/LocalLLaMA, r/selfhosted
- Output: Technology evaluation cards, new tool assessments

### 2. Marketing & Content
- Substack newsletters (25 feeds)
- Reddit engagement signals
- TikTok trending (via RSSHub)
- Product Hunt launches
- Output: Content calendar topics, AEO atomic facts, Reddit Ninja opportunities

### 3. Sales & Client Success
- Competitor pricing changes
- Industry news relevant to client verticals
- Companies House new filings
- Output: Prospect intelligence, client talking points

### 4. Security & Compliance
- CVE/NVD advisories
- tl;dr sec, Risky Biz newsletters
- r/netsec, r/cybersecurity
- HMRC/GDPR regulatory updates
- Output: Vulnerability alerts, compliance updates

### 5. Operations & Infrastructure
- Docker/Kubernetes release notes
- Cloud provider status pages
- r/devops, r/sysadmin
- ByteByteGo system design
- Output: Infrastructure upgrade notices, performance advisories

### 6. Finance & Economics
- UK economic indicators
- Bank of England rate decisions
- SMB lending market changes
- Output: Economic context for client financial analysis

### 7. Product Development
- User feedback signals (when live)
- Feature request patterns
- Competitive product launches
- Output: Product roadmap inputs, feature prioritisation signals

---

## PART 6: IMPLEMENTATION TIMELINE

### Phase 0: Foundation (Days 1-3) — Deadline: 19 March
- [ ] Partition drives (RAID-1 mirror, XFS)
- [ ] Harden OS (CIS Level 1 via USG)
- [ ] Install Docker + docker-compose
- [ ] Set up Ansible playbook in git repo
- [ ] Deploy Traefik + wildcard TLS
- [ ] Deploy monitoring stack (Prometheus + Grafana + Loki + Uptime Kuma)

### Phase 1: Data Layer (Days 4-6) — Deadline: 22 March
- [ ] Deploy Neo4j 5.26+ (configured for multi-DB)
- [ ] Deploy Qdrant
- [ ] Deploy PostgreSQL 17 with RLS setup
- [ ] Deploy Redis 7.x
- [ ] Deploy Graphiti MCP server with Neo4j backend
- [ ] Test: create kg_dave_jesmond graph, ingest test episodes
- [ ] Verify: multi-tenancy routing works (the fix for Issue #1325)

### Phase 2: Client Connectors (Days 7-9) — Deadline: 25 March (Jesmond deadline)
- [ ] Deploy Xero MCP server
- [ ] Build + deploy Sage MCP server (FastMCP 2.0)
- [ ] Deploy Gmail MCP server
- [ ] Set up Tailscale mesh
- [ ] Prepare PicoClaw Docker Compose for Jesmond Plumbing
- [ ] Run first Financial Autopsy ("The Reveal") for Dave Jesmond

### Phase 3: Intelligence Pipeline (Days 10-14)
- [ ] Deploy Miniflux + RSSHub + Kill-the-Newsletter
- [ ] Configure 200+ RSS feeds (GitHub releases, newsletters, Reddit)
- [ ] Build NightCrawler collector + classifier
- [ ] Set up department routing queues
- [ ] Deploy SearXNG (if not already running)

### Phase 4: Security Hardening (Days 15-17)
- [ ] Deploy Wazuh (SIEM + HIDS)
- [ ] Deploy Falco (container runtime security)
- [ ] Configure auditd + eBPF monitoring
- [ ] Set up immutable logging (append-only to Hetzner Storage Box)
- [ ] Run CIS Docker Benchmark audit
- [ ] Set up 3-2-1 backup (RAID-1 + Hetzner Storage Box + Backblaze B2)

### Phase 5: Agent Infrastructure (Days 18-21)
- [ ] Deploy Temporal (Cove Code Factory)
- [ ] Deploy Ollama + LiteLLM
- [ ] Deploy private Docker registry
- [ ] Configure Watchtower for auto-updates
- [ ] Set up webhook-triggered GitOps deployment

### Phase 6: Full Production (Days 22-28)
- [ ] Deploy remaining MCP servers (HubSpot, Stripe, etc.)
- [ ] Build HMRC MTD MCP
- [ ] Build Companies House MCP
- [ ] Build WhatsApp Business gateway
- [ ] Full integration testing
- [ ] Load test with simulated multi-tenant workload

---

## PART 7: VAULT METHODOLOGY INTEGRATION

The 40 methodologies from the vault all map to this infrastructure:

**Deterministic rubrics (run on PostgreSQL, no AI):**
- Altman Z-Score, Cash Conversion Cycle, Unit Economics, Quick Ratio
- Stored as JSON in /rubriks/ directory
- Executed by scheduled cron jobs, results written to PostgreSQL

**Knowledge graph methodologies (run on Neo4j + Graphiti):**
- PUDDING Technique (cross-domain discovery)
- Universal PUDDING Taxonomy (WHAT.HOW.SCALE.TIME labelling)
- Temporal Synthesis Engine ("The Movie")
- Mycelial Mesh (anonymised cross-client patterns)
- Biological Decision Logic (7 routing patterns)

**Agent governance (enforced by code, not AI):**
- Immutable Foundation Code v1.0 (7 principles)
- Ulysses Clause (circuit-breaker)
- Confidence-Gated Architecture (>95% auto, 70-95% monitor, <70% escalate)
- Radical Attribution Schema v1.0
- Operational Protocol v1.0 (8 laws)

**Products (all share BaseLayer infrastructure):**
- Bob (tradesperson AI), Finance Engine, AI Telephone System
- OpenClaw (Mac Mini M4), PicoClaw (Beelink N100)
- Voice Mirror, Business Bible, HGV Driver System

---

## PART 8: KEY CONFIGURATION FILES

### docker-compose.yml structure (abbreviated)
```yaml
services:
  traefik: ...
  neo4j:
    image: neo4j:5.26-enterprise
    environment:
      - NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
      - NEO4J_server_memory_heap_initial__size=8g
      - NEO4J_server_memory_heap_max__size=16g
      - NEO4J_server_memory_pagecache_size=64g
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
      - neo4j-plugins:/plugins
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant-data:/qdrant/storage
  postgresql:
    image: postgres:17
    environment:
      - POSTGRES_DB=amplified
    volumes:
      - pg-data:/var/lib/postgresql/data
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
  graphiti-mcp:
    image: registry.amplifiedpartners.ai/graphiti-mcp:latest
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - neo4j
      - qdrant
  miniflux:
    image: miniflux/miniflux:latest
    depends_on:
      - postgresql
  rsshub:
    image: diygod/rsshub:latest
  ...
```

---

## SOURCES

All recommendations backed by research in:
- research-server-infrastructure.md (61KB)
- research-anti-sabotage.md (62KB)
- research-database-architecture.md (62KB)
- research-knowledge-graph-systems.md (70KB)
- research-prebuilt-software.md (63KB)
- research-intelligence-pipeline.md (55KB)
- research-rd-creative-departments.md (72KB)
- vault-methodology-catalogue.md (69KB)

Total research: ~514KB of primary research across 8 streams.
