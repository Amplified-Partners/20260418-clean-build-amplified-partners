---
title: "Synthesis Data"
id: "synthesis-data"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "synthesis-data.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# SYNTHESIS DATA — Unified System Design
## All Software Mapped to Amplified Partners Frameworks

### FRAMEWORK → SOFTWARE MAPPING

#### 1. SOVEREIGN ENGINE (Architecture Layer)
- **Temporal** (18.9k⭐, MIT) — Cove backbone, durable workflow orchestration
  - GitHub: https://github.com/temporalio/temporal
- **Neo4j Community** (GPL v3) — Knowledge graph DB, replacing FalkorDB
  - GitHub: https://github.com/neo4j/neo4j
- **Graphiti** (22.4k⭐, Apache 2.0) — Temporal knowledge graph on Neo4j
  - GitHub: https://github.com/getzep/graphiti
- **Qdrant** — Vector embeddings, semantic search
- **PostgreSQL 17** — Structured business data, RLS multi-tenancy
- **Redis 7** — Caching, sessions, queues, Streams for event bus
- **Traefik** — SSL termination, reverse proxy (existing)

#### 2. COMPOUND ENGINEERING (Cove Build Pipeline)
- **Every.to Compound Plugin** (6.8k⭐, MIT) — Plan→Work→Review→Compound loop
  - GitHub: https://github.com/EveryInc/compound-engineering-plugin
- **bkit Vibecoding Kit** (399⭐, Apache 2.0) — PDCA + Evaluator-Optimizer loop
  - GitHub: https://github.com/popup-studio-ai/bkit-claude-code
- **SICA** (131⭐, MIT) — Self-improving coding agent research reference
  - GitHub: https://github.com/MaximeRobeyns/self_improving_coding_agent
- **OpenHands** (65.5k⭐, MIT) — AI software agent platform
  - GitHub: https://github.com/OpenHands/OpenHands
- **MCP Memory Server** (MIT) — Persistent agent knowledge graph
  - GitHub: https://github.com/modelcontextprotocol/servers/tree/main/src/memory
- **Mem0** (42k⭐, Apache 2.0) — Universal memory layer
  - GitHub: https://github.com/mem0ai/mem0

#### 3. BUILD QUALITY FRAMEWORK (Review + Quality Gates)
- **SonarQube Community** (10k⭐, LGPL-3.0) — Static analysis quality gates
  - GitHub: https://github.com/SonarSource/sonarqube
- **Qodo Merge / PR-Agent** (10.6k⭐, AGPL-3.0) — AI code review
  - GitHub: https://github.com/Codium-ai/pr-agent
- **Langfuse** (23.3k⭐, MIT) — LLM observability + rubric scoring
  - GitHub: https://github.com/langfuse/langfuse
- **Hillfog** (53⭐, Open source) — KPI/OKR/PDCA tracking
  - GitHub: https://github.com/billchen198318/hillfog

#### 4. PUDDING TECHNIQUE (Knowledge Discovery)
- **Neo4j + GDS Library** — Graph algorithms for pattern discovery
- **Graphiti** — Temporal edges for knowledge evolution
- **LangGraph** (22.5k⭐, MIT) — Conditional edges = Quorum logic, hierarchical subgraphs = Octopus pattern
  - GitHub: https://github.com/langchain-ai/langgraph
- **neo4j-graphrag-python** (v1.10, MIT) — Official Neo4j RAG toolkit
  - GitHub: https://github.com/neo4j/neo4j-graphrag-python

#### 5. BIOLOGICAL DECISION LOGIC (Agent Orchestration)
- **LangGraph** — Best fit: conditional edges map to biological routing patterns
- **Anthropic Multi-Agent Patterns** — Orchestrator-workers, evaluator-optimizer
- **CrewAI** (27.5k⭐, MIT) — Role-based agent teams
  - GitHub: https://github.com/crewAIInc/crewAI
- **Google ADK** (20.8k⭐, Apache 2.0) — Agent Development Kit
  - GitHub: https://github.com/google/adk-python

#### 6. OBSERVABILITY + DEATH SPIRAL DETECTION
- **Langfuse** — LLM traces, costs, evals, rubric scoring
- **Prometheus** (~56k⭐, Apache 2.0) — Metrics collection
  - GitHub: https://github.com/prometheus/prometheus
- **Grafana** (~66k⭐, AGPL-3.0) — Dashboards
  - GitHub: https://github.com/grafana/grafana
- **cAdvisor** (~17k⭐, Apache 2.0) — Container metrics
  - GitHub: https://github.com/google/cadvisor
- **Loki** (~24k⭐, AGPL-3.0) — Log aggregation
  - GitHub: https://github.com/grafana/loki
- **OpenLLMetry** (6.5k⭐, Apache 2.0) — OTel SDK for LLMs
  - GitHub: https://github.com/traceloop/openllmetry
- **Dozzle** (13k⭐, MIT) — Real-time Docker log viewer
  - GitHub: https://github.com/amir20/dozzle
- **Portainer** (31k⭐, zlib) — Container management UI
  - GitHub: https://github.com/portainer/portainer

#### 7. MCP ECOSYSTEM (Sovereign Data Bridge)
- **LiteLLM** (39.4k⭐, MIT) — MCP gateway + LLM proxy
  - GitHub: https://github.com/BerriAI/litellm
- **Xero MCP** (127⭐, MIT, Official) — Accounting
  - GitHub: https://github.com/XeroAPI/xero-mcp-server
- **Sage (CData)** (MIT read-only) — UK accounting
  - GitHub: https://github.com/CDataSoftware/sage-cloud-accounting-mcp-server-by-cdata
- **QuickBooks MCP** (113⭐, Apache 2.0, Official) — Accounting
  - GitHub: https://github.com/intuit/quickbooks-online-mcp-server
- **GitHub MCP** (27.1k⭐, MIT, Official) — Dev tools
  - GitHub: https://github.com/github/github-mcp-server
- **WhatsApp MCP** (5.4k⭐, MIT) — Messaging
  - GitHub: https://github.com/lharries/whatsapp-mcp
- **Linear MCP** (Official remote) — Project management
  - URL: https://mcp.linear.app/sse
- **Companies House MCP** (MIT) — UK business verification
  - GitHub: https://github.com/stefanoamorelli/companies-house-mcp
- **Google Workspace MCP** (800⭐, MIT) — Productivity
  - GitHub: https://github.com/taylorwilsdon/google_workspace_mcp
- **Stripe MCP** (Official) — Payments
  - URL: https://mcp.stripe.com
- **GoCardless MCP** (Official) — UK direct debit
  - URL: https://developer.gocardless.com/developer-tools/mcp/
- **Calendly MCP** (Official) — Scheduling
  - URL: https://mcp.calendly.com
- **HubSpot MCP** (MIT) — CRM
  - GitHub: https://github.com/peakmojo/mcp-hubspot

#### 8. CONTENT ENGINE (Overnight Factory)
- **Ghost CMS** (51.7k⭐, MIT) — Blog + newsletter (Substack replacement)
  - GitHub: https://github.com/TryGhost/Ghost
- **Postiz** (Apache 2.0) — Social media scheduling, 25 platforms
  - GitHub: https://github.com/gitroomhq/postiz-app
- **Listmonk** (18k⭐, AGPL-3.0) — Newsletter/email
  - GitHub: https://github.com/knadh/listmonk
- **Langflow** (145k⭐, MIT) — Visual AI pipeline builder
  - GitHub: https://github.com/langflow-ai/langflow
- **faster-whisper** (14.9k⭐, MIT) — CPU-optimised transcription
  - GitHub: https://github.com/SYSTRAN/faster-whisper
- **RSSHub** (39.5k⭐, MIT) — Content monitoring via RSS
  - GitHub: https://github.com/DIYgod/RSSHub
- **Directus** (33.7k⭐, BSL) — Database-first headless CMS
  - GitHub: https://github.com/directus/directus

#### 9. BUSINESS OS (Client-Facing SMB Tools)
- **ERPNext** (30.9k⭐, GPL-3.0) — Full ERP for UK SMBs
  - GitHub: https://github.com/frappe/erpnext
- **Twenty CRM** (38.8k⭐, AGPL) — Modern CRM
  - GitHub: https://github.com/twentyhq/twenty
- **Cal.com** (39.9k⭐, AGPLv3) — Scheduling/booking
  - GitHub: https://github.com/calcom/cal.com
- **Documenso** (12.5k⭐, AGPL) — E-signatures
  - GitHub: https://github.com/documenso/documenso
- **Invoice Ninja** (9.2k⭐, Elastic) — Invoicing + UK VAT
  - GitHub: https://github.com/invoiceninja/invoiceninja
- **Plane** (45.1k⭐, AGPL) — Project/job management
  - GitHub: https://github.com/makeplane/plane
- **AppFlowy** (68.6k⭐, AGPL) — Wiki/knowledge base
  - GitHub: https://github.com/AppFlowy-IO/AppFlowy

#### 10. AUTOMATION + INTEGRATION LAYER
- **n8n** (177k⭐, Sustainable Use) — Central workflow automation
  - GitHub: https://github.com/n8n-io/n8n
- **Activepieces** (20.6k⭐, MIT) — n8n alternative, MCP-native
  - GitHub: https://github.com/activepieces/activepieces
- **Nango** (6k⭐, Elastic) — Unified OAuth for 700+ APIs
  - GitHub: https://github.com/NangoHQ/nango
- **Kong Gateway** (42.6k⭐, Apache 2.0) — API management
  - GitHub: https://github.com/Kong/kong

### FRAMEWORK CROSS-REFERENCES

| Amplified Framework | PUDDING Label | Software Layer | Key Software |
|---|---|---|---|
| AMF (Amplified Management Framework) | M.=.5.∞ | Sovereign Engine + Business OS | Neo4j, Graphiti, ERPNext, Twenty CRM |
| PUDDING 2026 Taxonomy | M.=.0.∞ | Knowledge Graph + AI Pipelines | Neo4j GDS, Graphiti, LangGraph, Langflow |
| Build Quality Framework | C.=.5.l | Quality Gates + Observability | SonarQube, Qodo Merge, Langfuse |
| Biological Decision Logic | P.>.3.i → P.=.0.i | Agent Orchestration | LangGraph, Temporal, Anthropic patterns |
| Operational Protocol (8 Laws) | C.=.5.∞ | Observability + GitOps | GitHub MCP, Langfuse, Prometheus, Linear |
| RIC (Radical Innovation Canvas) | P.+.4.l | Content Engine + PUDDING | Langflow, RSSHub, Ghost, Postiz |
| Sovereign Engine Spec | E.=.5.p | Full Infrastructure | All Docker-hosted software |
| SOUL Principles | C.=.6.∞ | Governance Layer | Ulysses Clause, LiteLLM access control |
| Radical Attribution | I.=.0.∞ | Document Layer | YAML frontmatter, Langfuse metadata |
| Gap Analysis & Finite Lenses | P.~.4.m | Research + Discovery | PUDDING, LangGraph, Graphiti |

### IDENTIFIED GAPS (Software Needed But Not Yet Available)

1. **Sage MCP Server** — No official exists. Build custom using Sage REST API + MCP SDK, modelled on Xero MCP
2. **Checkatrade/MyBuilder/Rated People Integration** — No public APIs. Need partnership or web interaction layer
3. **Acoustic Forensics Pipeline** — No prebuilt software for boiler/machinery audio analysis via ML. Custom build required
4. **Haggis Gamification System** — Custom build (no prebuilt gamification fits the Amplified Partners spec)
5. **P2 Tokenisation Engine** — Custom build using spaCy NER + Diceware token generation
6. **Financial Autopsy Generator** — Custom build combining Altman Z-Score + deterministic rubrics + PDF generation
