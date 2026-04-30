---
title: "OS Solutions Research"
id: "os-solutions-research"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "os-solutions-research.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# GitHub Open-Source Solutions Research
**Infrastructure Build — 7 Segments**
*Researched: Monday, 16 March 2026*

---

## Overview

This document evaluates the best open-source GitHub repositories for each of 7 infrastructure segments. For each, the primary recommendation is assessed for direct use vs. pattern harvesting, with LOC-savings estimates.

---

## SEGMENT 1 — Foundation: Docker Server Hardening + CIS Benchmark Automation

### PRIMARY RECOMMENDATION

**dev-sec/ansible-collection-hardening**
- **URL:** https://github.com/dev-sec/ansible-collection-hardening
- **Stars:** 5,300+ | **Forks:** 823
- **Last Update:** Actively maintained (latest activity Nov 2025)
- **What it does:** Battle-tested Ansible collection covering OS hardening (Linux, SSH, nginx, MySQL) with CIS-aligned controls. Covers kernel hardening, filesystem permissions, auditd, PAM, and service configuration. Used in production by enterprises globally.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Run as Ansible roles against your Ubuntu 24.04 Docker host. Combine with the Ubuntu24-CIS role for full CIS coverage.
- **Estimated LOC saved:** ~2,000–3,500 LOC (hardening playbooks, audit rules, sysctl config)

---

### SECONDARY RECOMMENDATION

**ansible-lockdown/UBUNTU24-CIS**
- **URL:** https://github.com/ansible-lockdown/UBUNTU24-CIS
- **Stars:** 100 | **Forks:** 27
- **Last Update:** Latest release Aug 2025
- **What it does:** Automated CIS Benchmark v1.0.0 compliance remediation specifically for Ubuntu 24.04 LTS, implemented as an Ansible role. Remediates the full CIS control set with configurable skips for controls that conflict with Docker.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Run this after the dev-sec collection above for Ubuntu-layer CIS compliance. Requires tuning `defaults/main.yml` to exclude Docker-conflicting controls (e.g., some network namespace controls).
- **Estimated LOC saved:** ~1,800 LOC

---

### SUPPORTING RECOMMENDATION

**MVladislav/ansible-docker**
- **URL:** https://github.com/MVladislav/ansible-docker
- **Stars:** 3 | **Forks:** 2
- **Last Update:** Mar 2025
- **What it does:** Ansible role implementing CIS Docker Benchmark v1.4.0, sections 1–3 (host config, daemon config, daemon configuration files). Tested on Ubuntu 22.04–24.04. 52 of 119 controls implemented/automated; detailed compliance table in README.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — Low star count but highly relevant control-set mapping. Use the detailed compliance table and partial role as a reference for controls not covered by the MITRE repo. Layer on top of the two recommendations above.
- **Estimated LOC saved:** ~800 LOC (daemon.json templates, auditd rules, systemd hardening)

**MVladislav/ansible-cis-ubuntu-2404**
- **URL:** https://github.com/MVladislav/ansible-cis-ubuntu-2404
- **Stars:** 27 | **Forks:** 11
- **Last Update:** Sep 2024
- **What it does:** Ansible role for CIS Ubuntu Linux Benchmark v1.0.0 on Ubuntu 24.04. Companion to the docker role above by the same author — covers OS layer that the docker role does not.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — Use alongside ansible-lockdown/UBUNTU24-CIS as a cross-reference and gap-filler.
- **Estimated LOC saved:** ~500 LOC

---

### Segment 1 Summary
| Priority | Repo | Stars | Use / Harvest |
|----------|------|-------|---------------|
| 1st | dev-sec/ansible-collection-hardening | 5.3k | Direct use |
| 2nd | ansible-lockdown/UBUNTU24-CIS | 100 | Direct use |
| 3rd | MVladislav/ansible-docker | 3 | Harvest patterns |

**Total estimated LOC saved: ~5,100 LOC**

---

## SEGMENT 2 — Core Services: Traefik + Monitoring Stack (Prometheus/Grafana/Loki)

### PRIMARY RECOMMENDATION

**vegasbrianc/prometheus**
- **URL:** https://github.com/vegasbrianc/prometheus
- **Stars:** 4,500+ | **Forks:** 1,600+
- **Last Update:** 2024 (last seen active)
- **What it does:** Docker Compose stack for Prometheus + Grafana monitoring. Includes full Traefik integration example (docker-traefik-stack.yml), node-exporter, cAdvisor, and pre-configured Grafana dashboards. One of the most referenced Prometheus+Docker setups on GitHub.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** (as a base template) — The Traefik + Prometheus compose files and Grafana dashboard JSON files are plug-and-play. Will need updating to current versions.
- **Estimated LOC saved:** ~2,500 LOC (compose files, prometheus.yml, alertmanager config, Grafana dashboards)

---

### SECONDARY RECOMMENDATION

**haenno/traefik-docker-compose-grafana-prometheus-loki-promtail-portainer**
- **URL:** https://github.com/haenno/traefik-docker-compose-grafana-prometheus-loki-promtail-portainer
- **Stars:** ~50 (smaller repo)
- **Last Update:** Mar 2023
- **What it does:** Single repository that wires together the exact stack you need: Traefik 2.x + Prometheus + Grafana + Loki + Promtail + Portainer in a Docker Compose setup, with working examples of the metrics/log collection pipeline.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — Config is not production-ready (missing TLS, non-root setup) but the wiring between Traefik's metrics endpoint → Prometheus → Grafana, and Promtail → Loki → Grafana is exactly what you need to replicate. Treat as reference architecture.
- **Estimated LOC saved:** ~1,200 LOC (promtail config, loki config, grafana datasource provisioning)

---

### SUPPORTING RECOMMENDATION

**OneUptime/docker-compose-observability (article reference)**
- **URL:** https://oneuptime.com/blog/post/2026-02-06-docker-compose-observability-stack/view
- **What it does:** A Feb 2026 complete reference for OpenTelemetry Collector + Tempo + Loki + Prometheus + Grafana in Docker Compose. Not a GitHub repo, but the compose files are copy-paste ready and up-to-date.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — Excellent current reference for OTel-native stack wiring. If your stack is OTel-forward (recommended), use this as the primary reference.
- **Estimated LOC saved:** ~800 LOC

---

### Segment 2 Summary
| Priority | Repo | Stars | Use / Harvest |
|----------|------|-------|---------------|
| 1st | vegasbrianc/prometheus | 4.5k | Direct use (template base) |
| 2nd | haenno/traefik…portainer | ~50 | Harvest patterns |
| 3rd | OneUptime OTel article | N/A | Harvest patterns |

**Total estimated LOC saved: ~4,500 LOC**

---

## SEGMENT 3 — Data Layer: Neo4j + Qdrant + PostgreSQL Multi-Tenant

### PRIMARY RECOMMENDATION — PostgreSQL RLS

**aws-samples/aws-saas-factory-postgresql-rls**
- **URL:** https://github.com/aws-samples/aws-saas-factory-postgresql-rls
- **Stars:** ~200
- **Last Update:** 2019 (AWS SaaS Factory reference; patterns remain valid for PostgreSQL RLS)
- **What it does:** Complete demonstration of multi-tenant data isolation using PostgreSQL Row Level Security (RLS). Shows tenant onboarding, RLS policy creation, per-tenant role management, and cross-tenant access prevention. AWS-specific infrastructure but the SQL patterns are universal.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — The CloudFormation infrastructure is AWS-specific, but the RLS SQL patterns, tenant isolation policies, and connection management model translate directly to any PostgreSQL deployment.
- **Estimated LOC saved:** ~600 LOC (RLS migration templates, policy SQL, connection management patterns)

**ricofritzsche/multi-tenant-rls-demo**
- **URL:** https://github.com/ricofritzsche/multi-tenant-rls-demo
- **Stars:** ~10
- **Last Update:** May 2025
- **What it does:** Complete SQL script for a multi-tenant PostgreSQL setup with RLS. Lean, focused, Docker-native — exactly the bootstrapping SQL needed.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — The SQL init scripts can be used as-is. Ideal as the database initialisation layer for your Docker Compose PostgreSQL setup.
- **Estimated LOC saved:** ~400 LOC

---

### PRIMARY RECOMMENDATION — Neo4j Multi-Tenant

**getzep/graphiti (see also Segment 4)**
- **URL:** https://github.com/getzep/graphiti
- **Stars:** 22,400+ | **Forks:** 2,200+
- **Last Update:** Jan 2026 (v0.26.3)
- **What it does:** Graphiti uses Neo4j as its primary backend and implements a `custom database name` per Neo4j driver instance. Each `group_id` effectively creates tenant isolation within a shared Neo4j 5.x instance. The driver configuration patterns for multi-database Neo4j are directly usable.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — For Neo4j multi-tenancy in an open-source context, Neo4j Community Edition does not natively support multiple databases (Enterprise only). Graphiti's pattern of using `group_id` namespacing with a shared Neo4j Community instance is the practical open-source approach. Harvest this pattern.
- **Estimated LOC saved:** ~1,000 LOC (Neo4j driver config, index/constraint setup, namespace management)

**neo4j-examples/sdn6-reactive-multidatabase**
- **URL:** https://github.com/neo4j-examples/sdn6-reactive-multidatabase
- **Stars:** ~30
- **Last Update:** Aug 2024
- **What it does:** Official Neo4j example for multi-database (Enterprise) using Spring Data Neo4j 6. Demonstrates the multi-database setup, Fabric configuration, and tenant routing pattern.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — Requires Neo4j Enterprise for true multi-database. Valuable for understanding the routing architecture, but in a community/open-source deployment you will use the Graphiti group_id pattern instead.
- **Estimated LOC saved:** ~300 LOC (routing patterns)

---

### Qdrant Note

No dominant open-source multi-tenant Qdrant template was found. Qdrant's built-in collection-level isolation (one collection per tenant) is the standard pattern. The official Qdrant Docker Compose is at https://github.com/qdrant/qdrant — use it directly. The multi-tenancy is implemented via collection naming convention (`tenant_{id}_vectors`) rather than a separate library.

---

### Segment 3 Summary
| Priority | Repo | Stars | Use / Harvest |
|----------|------|-------|---------------|
| 1st (PG) | ricofritzsche/multi-tenant-rls-demo | ~10 | Direct use |
| 2nd (PG) | aws-samples/aws-saas-factory-postgresql-rls | ~200 | Harvest patterns |
| 1st (Neo4j) | getzep/graphiti | 22.4k | Harvest patterns (group_id model) |
| 2nd (Neo4j) | neo4j-examples/sdn6-reactive-multidatabase | ~30 | Harvest patterns |

**Total estimated LOC saved: ~2,300 LOC**

---

## SEGMENT 4 — Knowledge Graph: Graphiti MCP Server

### PRIMARY RECOMMENDATION

**getzep/graphiti**
- **URL:** https://github.com/getzep/graphiti
- **Stars:** 22,400+ | **Forks:** 2,200+
- **Last Update:** Jan 2026 (v0.26.3) — actively maintained
- **What it does:** The canonical open-source framework for building real-time, temporally-aware knowledge graphs for AI agents. Built and maintained by Zep. Includes:
  - A fully-featured MCP server (`mcp_server/` directory) that exposes Graphiti's graph capabilities to Claude, Cursor, VS Code Copilot
  - Bi-temporal data model (event time + ingestion time)
  - Hybrid retrieval: semantic (embeddings) + BM25 keyword + graph traversal
  - Supports Neo4j, FalkorDB, Kuzu, Amazon Neptune as backends
  - Docker Compose deployment included
  - Multi-tenant support via `group_id` parameter
  - Episode management, entity/relationship management, semantic search
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — This is the solution. The MCP server in `getzep/graphiti/mcp_server/` can be deployed directly via Docker Compose with Neo4j. The `group_id` system provides the multi-tenant isolation you need across clients.
- **Estimated LOC saved:** ~8,000–12,000 LOC (the entire knowledge graph + MCP server stack)

---

### SECONDARY RECOMMENDATION

**rawr-ai/mcp-graphiti**
- **URL:** https://github.com/rawr-ai/mcp-graphiti
- **Stars:** 74 | **Forks:** 15
- **Last Update:** Apr 2025
- **What it does:** Fork of the official Graphiti MCP server with a focus on multi-project support. Adds a CLI (`graphiti`) that generates docker-compose.yml with a root server (port 8000) plus per-project MCP servers (ports 8001+), all sharing a single Neo4j instance. Each project gets its own `group_id`, entities, and model config.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — This is the multi-tenant / multi-project deployment pattern you need for your infrastructure. Each client gets their own project container; knowledge graphs stay isolated; one database backing all of them. Directly deployable.
- **Estimated LOC saved:** ~1,500 LOC (CLI tooling, multi-compose generation, project init scaffolding)

---

### MCP Server Documentation Reference

**Zep Documentation — Graphiti MCP Server**
- **URL:** https://help.getzep.com/graphiti/getting-started/mcp-server
- **Last Updated:** Mar 2026
- **What it does:** Official documentation for setting up the Graphiti MCP server. Covers FalkorDB (default, Redis-based) and Neo4j backends, all LLM providers (OpenAI, Anthropic, Gemini, Groq, Azure), client configuration for Claude Desktop, Cursor, VS Code.
- **Use for:** Configuration reference during deployment.

---

### Segment 4 Summary
| Priority | Repo | Stars | Use / Harvest |
|----------|------|-------|---------------|
| 1st | getzep/graphiti | 22.4k | Use directly |
| 2nd | rawr-ai/mcp-graphiti | 74 | Use directly (multi-project deployment) |

**Total estimated LOC saved: ~13,500 LOC**

---

## SEGMENT 5 — Client Connectors: MCP Servers for Xero, Gmail, HubSpot, Sage

### MASTER DIRECTORY (Start Here)

**punkpeye/awesome-mcp-servers**
- **URL:** https://github.com/punkpeye/awesome-mcp-servers
- **Stars:** 80,500+ | **Forks:** 7,100+
- **Last Update:** Continuously updated (as of Mar 2026)
- **What it does:** The definitive curated list of MCP servers across all categories. Contains 1,000+ servers with categorisation. When looking for a connector, search this list first before building your own.
- **Direct Use or Harvest?** ⚠️ **REFERENCE DIRECTORY** — Not deployable itself; use as the discovery layer.

**modelcontextprotocol/servers**
- **URL:** https://github.com/modelcontextprotocol/servers
- **Stars:** 79,700+ | **Forks:** 9,700+
- **Last Update:** Jan 2026
- **What it does:** Anthropic's official MCP servers repository. The reference implementations for the MCP protocol. Includes officially supported connectors and links to the MCP Registry.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Use for any official connector implementations.

---

### XERO

**XeroAPI/xero-mcp-server** ← OFFICIAL
- **URL:** https://github.com/XeroAPI/xero-mcp-server
- **Stars:** 208 | **Forks:** 98
- **Last Update:** Mar 2025 (official Xero release)
- **What it does:** Official Xero MCP server. Implements the MCP protocol as a bridge to Xero's API. Supports OAuth authentication and exposes Xero accounting operations to MCP-compatible AI clients.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Official, maintained by XeroAPI. Will require OAuth app registration in Xero developer portal. For multi-tenant use, each client needs their own OAuth token; the multi-tenant wrapper (mcp_plexus or rawr-ai/mcp-graphiti pattern) handles token injection per-tenant.
- **Estimated LOC saved:** ~2,000–3,000 LOC (full Xero API integration)

---

### GMAIL

**GongRzhe/Gmail-MCP-Server**
- **URL:** https://github.com/GongRzhe/Gmail-MCP-Server
- **Stars:** 778 | **Forks:** 205
- **Last Update:** Dec 2024
- **What it does:** Full-featured Gmail MCP server with OAuth2 auto-authentication. Supports send/read/search/label management, attachments, batch operations, HTML emails. Docker deployable. Published on npm as `@gongrzhe/server-gmail-autoauth-mcp`.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Most complete community Gmail MCP server. Has Docker deployment support. Per-tenant OAuth token management required for multi-tenant use.
- **Estimated LOC saved:** ~2,500 LOC

**MarkusPfundstein/mcp-gsuite** (alternative)
- **URL:** https://github.com/MarkusPfundstein/mcp-gsuite
- **Stars:** ~500 (estimated)
- **What it does:** Gmail + Google Calendar in one MCP server. Supports multiple Google accounts simultaneously.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — Use as a supplement if calendar integration is also needed.

---

### HUBSPOT

**HubSpot Official MCP Server (Remote)**
- **URL:** https://mcp.hubspot.com (remote endpoint) / https://developers.hubspot.com/mcp
- **What it does:** HubSpot's official hosted MCP server. Provides CRM access (contacts, companies, deals, tasks) via OAuth 2.0. No self-hosting required.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — For multi-tenant use, each client connects their own HubSpot account via OAuth. The MCP client points to `mcp.hubspot.com` with their OAuth token.

**peakmojo/mcp-hubspot** (self-hosted alternative)
- **URL:** https://github.com/peakmojo/mcp-hubspot
- **Stars:** 102 | **Forks:** 50
- **Last Update:** Dec 2024
- **What it does:** Self-hosted HubSpot MCP server with built-in FAISS vector storage and caching to overcome HubSpot API rate limits. Docker deployable. Provides contacts, companies, conversations, semantic search over prior interactions.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Preferred for your self-hosted architecture. The vector caching layer is a significant bonus. Docker-first deployment.
- **Estimated LOC saved:** ~2,000 LOC

---

### SAGE (Accounting)

No official Sage-specific MCP server was found on GitHub as of March 2026. Sage Business Cloud (UK SME accounting) does not have a published open-source MCP connector.

**Options:**
1. **Build using FastMCP** — Use `jlowin/fastmcp` (https://github.com/jlowin/fastmcp) to build a thin MCP server wrapping Sage's REST API (Sage Business Cloud API v3). FastMCP provides the scaffolding; you implement the Sage API calls. Estimated build: ~400–600 LOC.
2. **Use the Zapier/Make MCP gateway** — Zapier has a cloud-hosted MCP server (6,000+ integrations including Sage) as a shortcut. Not self-hosted, but unblocks you immediately.
3. **Harvest the Xero MCP pattern** — The XeroAPI server is structurally similar to what a Sage connector would look like. Use it as a blueprint.

---

### MULTI-TENANT MCP WRAPPER

**Super-I-Tech/mcp_plexus**
- **URL:** https://github.com/Super-I-Tech/mcp_plexus
- **Stars:** 14 | **Forks:** 5
- **Last Update:** May 2025
- **What it does:** Multi-tenant MCP server framework built on FastMCP 2.7. Deploys as an ASGI app (Uvicorn). Manages isolated tenant environments, OAuth 2.1 per-tenant authentication, API key management, and tool exposure per-tenant. Exactly the middleware needed to wrap Xero/Gmail/HubSpot/Sage per-client.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — This is the multi-tenant MCP gateway you need. Wraps individual MCP servers and injects per-tenant credentials. Low stars but purpose-built for this exact use case.
- **Estimated LOC saved:** ~3,000 LOC (auth middleware, tenant routing, credential injection)

**ragieai/dynamic-fastmcp**
- **URL:** https://github.com/ragieai/dynamic-fastmcp
- **Stars:** ~50
- **What it does:** Used to power Ragie's multi-tenant Streamable HTTP MCP Server in production. Dynamic FastMCP extends FastMCP for multi-tenant Streamable HTTP deployments.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — If mcp_plexus proves insufficient, use this production-proven pattern.

---

### Segment 5 Summary
| Connector | Repo | Stars | Use / Harvest |
|-----------|------|-------|---------------|
| Directory | punkpeye/awesome-mcp-servers | 80.5k | Reference |
| Xero | XeroAPI/xero-mcp-server | 208 | Use directly |
| Gmail | GongRzhe/Gmail-MCP-Server | 778 | Use directly |
| HubSpot | peakmojo/mcp-hubspot | 102 | Use directly |
| Sage | — | — | Build (FastMCP) |
| MT Wrapper | Super-I-Tech/mcp_plexus | 14 | Use directly |

**Total estimated LOC saved: ~9,500–10,500 LOC**

---

## SEGMENT 6 — Intelligence Pipeline: RSS Aggregation + AI Classification

### PRIMARY RECOMMENDATION — RSS Aggregation

**miniflux/v2**
- **URL:** https://github.com/miniflux/v2
- **Stars:** 8,200+ | **Forks:** 802
- **Last Update:** Sep 2025 (v2.2.13) — actively maintained
- **What it does:** Minimalist, opinionated RSS/Atom/JSON Feed reader written in Go. Self-hosted, Docker-native, PostgreSQL-backed. Includes a full REST API for programmatic access to feeds and articles — critical for piping articles into your AI classification layer. Supports Atom 0.3/1.0, RSS 1.0/2.0, JSON Feed 1.0/1.1, OPML import/export.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Deploy via official Docker Compose (`miniflux/v2/contrib/docker-compose/basic.yml`). The REST API is the integration point: poll for new/unread articles → send to your AI classifier → write classification back as labels.
- **Estimated LOC saved:** ~5,000+ LOC (the entire RSS aggregation engine)

---

### PRIMARY RECOMMENDATION — AI Classification

**umputun/newscope**
- **URL:** https://github.com/umputun/newscope
- **Stars:** 29 | **Forks:** 3
- **Last Update:** Jun 2025
- **What it does:** AI-powered RSS feed curator that automatically classifies and scores articles based on user interests. Self-hosted, uses LLM scoring. Exactly the intelligence pipeline layer you need: ingests feeds → scores/classifies each article → surfaces relevant content. Docker-deployable.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Small repo but purpose-built for this exact use case. The scoring/classification pipeline can be extended to your domain-specific taxonomy (by sector, topic, entity). Combine with Miniflux as the feed source.
- **Estimated LOC saved:** ~1,500–2,000 LOC

---

### SECONDARY RECOMMENDATION — AI Classification

**m0wer/rssfilter**
- **URL:** https://github.com/m0wer/rssfilter
- **Stars:** ~50
- **Last Update:** Mar 2024
- **What it does:** RSS filter that uses LLM embeddings and ML to recommend similar articles based on user reading history. Tracks read articles, computes embeddings, clusters them, and filters/recommends incoming feed items. Self-hosted, Docker Compose deployable, supports GPU.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — The embedding-based classification approach (rather than LLM prompt-per-article) is more scalable at volume. Harvest the embedding pipeline architecture for your intelligence layer.
- **Estimated LOC saved:** ~800 LOC (embedding pipeline, clustering logic)

---

### RSSHub Reference

**DIYgod/RSSHub**
- **URL:** https://github.com/DIYgod/RSSHub
- **Stars:** 37,000+
- **What it does:** Extensible RSS feed generator that creates RSS feeds from websites that don't have them (Twitter, Reddit, YouTube, news sites, etc.). The feed generation layer that feeds into Miniflux.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Deploy as a companion to Miniflux. Miniflux subscribes to RSSHub endpoints to pull feeds from otherwise non-RSS sources.
- **Estimated LOC saved:** ~10,000+ LOC (the entire feed generation engine)

---

### Segment 6 Summary
| Priority | Repo | Stars | Use / Harvest |
|----------|------|-------|---------------|
| 1st (aggregation) | miniflux/v2 | 8.2k | Use directly |
| 1st (AI classify) | umputun/newscope | 29 | Use directly |
| 2nd (AI classify) | m0wer/rssfilter | ~50 | Harvest patterns |
| Feed generation | DIYgod/RSSHub | 37k+ | Use directly |

**Total estimated LOC saved: ~17,000+ LOC**

---

## SEGMENT 7 — Orchestration: Temporal + GitOps + Wazuh/Falco

### PRIMARY RECOMMENDATION — Temporal

**temporalio/docker-compose**
- **URL:** https://github.com/temporalio/docker-compose
- **Stars:** 449 | **Forks:** 262
- **Last Update:** Latest release v1.28.1, Aug 2025 — official Temporal repo
- **What it does:** Official Temporal Docker Compose files from the Temporal team. Provides multiple configurations: default (with Cassandra), PostgreSQL variant, MySQL variant, ElasticSearch for visibility, multi-role deployment, Grafana + Prometheus + Loki monitoring integration, and Temporal Web UI. This is the canonical starting point for self-hosted Temporal.
- **Direct Use or Harvest?** ⚠️ **HARVEST PATTERNS** — Officially flagged as "for local development, not production." For production, the Temporal team recommends Kubernetes + Helm charts. However, for a single-node production deployment, the PostgreSQL compose variant with the multi-role configuration is a well-trodden path. Use with the understanding that you'll need to harden it (persistent volumes, TLS, proper secrets management).
- **Estimated LOC saved:** ~1,500 LOC (compose files, postgres setup, admin tools config)

**tsurdilo/my-temporal-dockercompose**
- **URL:** https://github.com/tsurdilo/my-temporal-dockercompose
- **Stars:** ~150
- **Last Update:** Mar 2022 (patterns still valid for Temporal on Docker Compose)
- **What it does:** Community reference for self-deploying Temporal via Docker Compose and Docker Swarm. Uses PostgreSQL for persistence. Includes gRPC tracing with OTel collector + Jaeger, Loki logging driver, multi-cluster replication examples, and Swarm deployment patterns.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** (as primary production reference) — More production-oriented than the official repo. The PostgreSQL-backed compose files with Loki logging and OTel tracing are exactly what a production single-node deployment needs.
- **Estimated LOC saved:** ~1,200 LOC (production compose config, postgres persistence, monitoring integration)

---

### PRIMARY RECOMMENDATION — GitOps

**fluxcd/flux2**
- **URL:** https://github.com/fluxcd/flux2
- **Stars:** 7,500+ | **Forks:** 686
- **Last Update:** Oct 2025 (v2.7.2) — CNCF Graduated project
- **What it does:** Open and extensible GitOps continuous delivery solution for Kubernetes. Reconciles cluster state from Git repositories. Supports HelmReleases, Kustomizations, multi-tenancy, image automation, and notifications. The industry standard for GitOps on Kubernetes.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — If your infrastructure runs on Kubernetes (or migrates to it). For Docker Compose-based infrastructure, Flux is not directly applicable — in that case, consider Woodpecker CI or Gitea Actions as the GitOps layer.
- **Estimated LOC saved:** ~3,000 LOC (GitOps pipeline config, HelmRelease manifests, Kustomizations)

---

### PRIMARY RECOMMENDATION — Security Monitoring

**wazuh/wazuh-docker**
- **URL:** https://github.com/wazuh/wazuh-docker
- **Stars:** 930+ | **Forks:** 495
- **Last Update:** Actively maintained (2025)
- **What it does:** Official Wazuh Docker deployment repository. Full Wazuh stack via Docker Compose: Wazuh server (HIDS/SIEM), dashboard (OpenSearch Dashboards), and OpenSearch indexer. Supports single-node and multi-node deployment, configurable volumes, production and testing configurations. Wazuh provides: file integrity monitoring, vulnerability detection, log analysis, compliance (PCI-DSS, HIPAA, GDPR), intrusion detection, and active response.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Official repo, well-maintained. The single-node Docker Compose configuration deploys a full Wazuh stack in 15 minutes. Each client's Docker host runs a Wazuh agent that phones home to your Wazuh manager.
- **Estimated LOC saved:** ~4,000 LOC (full SIEM/HIDS deployment)

**falcosecurity/falco**
- **URL:** https://github.com/falcosecurity/falco
- **Stars:** 8,300+ | **Forks:** 944
- **Last Update:** Jul 2025 — CNCF Incubating project
- **What it does:** Cloud-native runtime security tool for Linux. Monitors syscalls and container events in real-time, detecting anomalous behavior (privilege escalation, unexpected network connections, sensitive file access, container escape attempts). Includes Falcosidekick for routing alerts to Slack, PagerDuty, Loki, etc. A demo Docker Compose environment is provided.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — Deploy Falco + Falcosidekick alongside Wazuh for layered security: Wazuh covers HIDS/log analysis/compliance; Falco covers runtime syscall monitoring. The two are complementary and both have Wazuh integration (via Falco→Wazuh ruleset). Stars: 8.3k speaks for production maturity.
- **Estimated LOC saved:** ~2,000 LOC (Falco rules, Falcosidekick config, Docker Compose setup)

**zeinoux/siem-falco-wazuh**
- **URL:** https://github.com/zeinoux/siem-falco-wazuh
- **Stars:** ~20
- **Last Update:** 2022
- **What it does:** Falco + Wazuh integration with pre-built Wazuh decoder and rules for Falco alerts. Includes Wazuh rule files (`0485-falco.xml`, `0685-falco_rules.xml`) that parse Falco JSON output into structured Wazuh alerts.
- **Direct Use or Harvest?** ✅ **USE DIRECTLY** — The Wazuh decoder/rules files are the glue between Falco and Wazuh. Use these files directly in your Wazuh manager configuration.
- **Estimated LOC saved:** ~300 LOC (decoder + rules XML files)

---

### Segment 7 Summary
| Priority | Repo | Stars | Use / Harvest |
|----------|------|-------|---------------|
| 1st (Temporal) | tsurdilo/my-temporal-dockercompose | ~150 | Use directly |
| 2nd (Temporal) | temporalio/docker-compose | 449 | Harvest patterns |
| 1st (GitOps) | fluxcd/flux2 | 7.5k | Use directly (K8s) |
| 1st (Security) | wazuh/wazuh-docker | 930 | Use directly |
| 2nd (Security) | falcosecurity/falco | 8.3k | Use directly |
| Integration | zeinoux/siem-falco-wazuh | ~20 | Use directly |

**Total estimated LOC saved: ~12,000 LOC**

---

## CONSOLIDATED SUMMARY TABLE

| # | Segment | Best Repo | Stars | Use / Harvest | LOC Saved |
|---|---------|-----------|-------|---------------|-----------|
| 1 | Foundation | dev-sec/ansible-collection-hardening | 5.3k | Direct | ~3,500 |
| 1 | Foundation | ansible-lockdown/UBUNTU24-CIS | 100 | Direct | ~1,800 |
| 2 | Core Services | vegasbrianc/prometheus | 4.5k | Direct (base) | ~2,500 |
| 2 | Core Services | haenno/traefik…loki stack | ~50 | Harvest | ~1,200 |
| 3 | Data Layer | getzep/graphiti (Neo4j patterns) | 22.4k | Harvest | ~1,000 |
| 3 | Data Layer | ricofritzsche/multi-tenant-rls-demo | ~10 | Direct | ~400 |
| 4 | Knowledge Graph | getzep/graphiti | 22.4k | Direct | ~10,000 |
| 4 | Knowledge Graph | rawr-ai/mcp-graphiti | 74 | Direct | ~1,500 |
| 5 | Client Connectors | XeroAPI/xero-mcp-server | 208 | Direct | ~2,500 |
| 5 | Client Connectors | GongRzhe/Gmail-MCP-Server | 778 | Direct | ~2,500 |
| 5 | Client Connectors | peakmojo/mcp-hubspot | 102 | Direct | ~2,000 |
| 5 | Client Connectors | Super-I-Tech/mcp_plexus | 14 | Direct | ~3,000 |
| 6 | Intelligence Pipeline | miniflux/v2 | 8.2k | Direct | ~5,000 |
| 6 | Intelligence Pipeline | DIYgod/RSSHub | 37k+ | Direct | ~10,000 |
| 6 | Intelligence Pipeline | umputun/newscope | 29 | Direct | ~1,800 |
| 7 | Orchestration | tsurdilo/my-temporal-dockercompose | ~150 | Direct | ~1,200 |
| 7 | Orchestration | wazuh/wazuh-docker | 930 | Direct | ~4,000 |
| 7 | Orchestration | falcosecurity/falco | 8.3k | Direct | ~2,000 |
| 7 | Orchestration | fluxcd/flux2 | 7.5k | Direct | ~3,000 |

---

## TOTAL ESTIMATED LOC SAVINGS: ~58,900 LOC

*This estimate covers configuration, infrastructure, pipeline, and integration code that would otherwise need to be written from scratch. Core application logic (business rules, tenant-specific workflows, custom AI pipelines) is excluded.*

---

## KEY BUILD DECISIONS FLAGGED

1. **Neo4j Community vs Enterprise:** Neo4j Community Edition does not support multiple databases natively. Either use Graphiti's `group_id` pattern for namespace isolation within Community, or budget for Neo4j Enterprise, or evaluate FalkorDB (Redis-based, Graphiti-supported, open-source alternative with true multi-graph support).

2. **Sage MCP Gap:** No production-ready Sage Business Cloud MCP server exists. Budget ~3–5 days to build one using FastMCP against Sage's REST API. The Xero MCP server is a direct structural blueprint.

3. **Temporal Production Caution:** The official `temporalio/docker-compose` is explicitly marked as non-production. For production single-node: use tsurdilo's PostgreSQL variant + add TLS termination via Traefik, secret management via Docker Secrets, and backup jobs for the temporal and temporal_visibility databases.

4. **Wazuh + Falco Layering:** These are complementary, not redundant. Wazuh = HIDS, log analysis, compliance. Falco = runtime syscall anomaly detection. Both are needed for a complete security posture. The zeinoux integration wires them together in ~300 LOC.

5. **MCP Multi-Tenancy Architecture:** The recommended pattern is: `mcp_plexus` (multi-tenant gateway) → individual MCP servers (Xero, Gmail, HubSpot, Sage) → per-tenant OAuth token storage. The `rawr-ai/mcp-graphiti` CLI pattern handles the Graphiti knowledge graph layer separately with its own per-project isolation.
