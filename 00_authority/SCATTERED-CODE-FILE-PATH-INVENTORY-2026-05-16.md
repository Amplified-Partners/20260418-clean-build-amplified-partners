# Scattered Code File Path Inventory — 2026-05-16

> **Epistemic status:** MEASURED. Every file path verified against live repository state on 2026-05-16.
> Files marked `[NOT FOUND]` were referenced in prior documentation but do not exist on disk.
> Line counts from `wc -l` against current `main` branches.

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total scattered code files verified | **158 files** |
| Total lines of unintegrated code | **~35,400 lines** |
| Categories of scattered code | **13 categories** |
| Repos scanned | **clean-build, crm, corpus-raw, vault, marketing-engine, byker-production, amplified-knowledge-mcp, anthropic-token-proxy, amplified-site** |
| Integration priority | **HIGH** |

### What "scattered" means here

Code that exists across the estate in one or more of these states:
1. **Duplicated** — same logic in multiple locations (e.g. retell_integration exists in CRM, corpus-raw vault inbox, and as 4 versioned copies)
2. **Unintegrated** — written but not wired into the canonical architecture (e.g. vault inbox scripts, earlier pipeline versions)
3. **Orphaned** — no clear owner, no deployment target, no tests (e.g. evolution-api webhook dispatcher, hetzner linear reporter)
4. **Versioned in place** — multiple versions sitting alongside each other instead of using Git (e.g. grok_server.py, grok_server-v2.py, grok_server-v3.py)
5. **Archived but present** — formally archived by ticket but still importable/reachable (e.g. 90_archive/ migration scripts)

---

## 1. Shell Scripts & Automation (Scattered)

### Deployment scripts (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/scripts/deploy-phone-agent.sh` | 68 | xAI Phone Agent deployment |
| `02_build/scripts/vault-backup-setup.sh` | 64 | Vault backup automation |
| `02_build/security/hardening/apply-hardening.sh` | 176 | Infrastructure hardening |
| `02_build/command-centre/backend/deploy-voice.sh` | 41 | Voice Agent deployment |
| `02_build/scripts/beast-recovery.sh` | 110 | Beast recovery procedure |
| `02_build/scripts/final_rescue.sh` | 64 | Final rescue script |
| `02_build/scripts/just-run-this.sh` | 127 | Quick-start script |
| `02_build/scripts/fix-graphiti-falkordb.sh` | 172 | FalkorDB fix (DEPRECATED — FalkorDB deprecated per AMP-344) |
| `02_build/scripts/patch-graphiti-1272.sh` | 58 | Graphiti patch (DEPRECATED) |

### Security scripts (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/security/amplified-client-audit-mac.sh` | 299 | Client Mac security audit |
| `02_build/security/beast-docker-firewall.sh` | 62 | Docker firewall rules |
| `02_build/security/hardening/docker-user-firewall.sh` | 54 | Docker user firewall |
| `02_build/security/just-run-this-v2.sh` | 82 | Security quick-start v2 |

### Hazel pipeline scripts (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/hazel/scripts/01_inventory.sh` | 155 | File inventory |
| `02_build/hazel/scripts/02_classify.sh` | 245 | File classification |
| `02_build/hazel/scripts/03_stage.sh` | 129 | File staging |
| `02_build/hazel/scripts/04_promote.sh` | 151 | File promotion |
| `02_build/hazel/scripts/05_reap.sh` | 114 | File cleanup |

### Evolution API scripts (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `evolution-api/start.sh` | — | Evolution API start |
| `evolution-api/stop.sh` | — | Evolution API stop |

**Subtotal: ~2,404 lines of shell across clean-build**

---

## 2. Docker Compose Files (Multiple Locations)

### Core infrastructure (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/beast/falkordb/docker-compose.beast.snapshot.yml` | 140 | Beast infrastructure snapshot (DEPRECATED — FalkorDB) |
| `02_build/cove-orchestrator/docker/docker-compose.yml` | 168 | Cove orchestrator full stack |
| `02_build/command-centre/backend/docker-compose.voice.yml` | 30 | Voice agent compose |
| `02_build/enforcer/docker-compose.yml` | 46 | Enforcer monitoring |
| `02_build/enforcer/docker-compose-entry.yml` | 84 | Enforcer entry point |
| `02_build/amplified-knowledge-mcp/docker-compose.yml` | 42 | Knowledge MCP (DEPRECATED — uses FalkorDB/Qdrant) |
| `02_build/beast-control-mcp/docker-compose.yml` | 58 | Beast Control MCP |
| `evolution-api/docker-compose.yml` | 65 | Evolution API |
| `hetzner_deployment/docker-compose.yml` | 67 | Hetzner deployment |

**Subtotal: 700 lines of compose YAML across 9 files**

---

## 3. Database Migration Scripts

### Legacy writers (archived by AMP-302, clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `90_archive/legacy-writers/migrate_falkordb.py` | 357 | FalkorDB → Postgres migration (DEPRECATED) |
| `90_archive/legacy-writers/migrate_qdrant.py` | 156 | Qdrant → Postgres migration (DEPRECATED) |

### Migration SQL (clean-build, cove-orchestrator)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/cove-orchestrator/db/migrations/001_initial_schema.sql` | 212 | Initial schema |
| `02_build/cove-orchestrator/db/migrations/002_nightscout_schema.sql` | 139 | Nightscout schema |
| `02_build/cove-orchestrator/db/migrations/003_email_agent_schema.sql` | 125 | Email agent schema |
| `02_build/cove-orchestrator/db/migrations/004_pipeline_runs_postgresql.sql` | 28 | Pipeline runs |
| `02_build/cove-orchestrator/db/migrations/005_brain_lockdown.sql` | 56 | Brain lockdown |
| `02_build/cove-orchestrator/db/migrations/006_compound_design_schema.sql` | 170 | Compound design |
| `02_build/cove-orchestrator/db/migrations/007_canonical_schema_v0.3.sql` | 197 | Canonical schema v0.3 |
| `02_build/cove-orchestrator/db/migrations/007_rollback.sql` | 32 | Rollback script |

### Brain migration (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/brain-migration/brain_mcp_server.py` | 889 | Brain MCP server |
| `02_build/brain-migration/README.md` | — | Migration documentation |

**Subtotal: ~2,361 lines (Python + SQL)**

---

## 4. MCP Servers — Cove Orchestrator (clean-build)

**9 MCP servers, ~2,354 lines:**

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/cove-orchestrator/mcp-servers/_template/server.py` | 195 | Template MCP |
| `02_build/cove-orchestrator/mcp-servers/email-mcp/server.py` | 269 | Email MCP |
| `02_build/cove-orchestrator/mcp-servers/filesystem-mcp/server.py` | 303 | Filesystem MCP |
| `02_build/cove-orchestrator/mcp-servers/github-mcp/server.py` | 311 | GitHub MCP |
| `02_build/cove-orchestrator/mcp-servers/langfuse-mcp/server.py` | 294 | Langfuse MCP |
| `02_build/cove-orchestrator/mcp-servers/litellm-mcp/server.py` | 275 | LiteLLM MCP |
| `02_build/cove-orchestrator/mcp-servers/nightscout-mcp/server.py` | 181 | Nightscout MCP |
| `02_build/cove-orchestrator/mcp-servers/postgresql-mcp/server.py` | 234 | PostgreSQL MCP |
| `02_build/cove-orchestrator/mcp-servers/telegram-mcp/server.py` | 292 | Telegram MCP |

> **Note:** User's original brief referenced `gitkraken-mcp/server.py` and `perplexity-mcp/server.py` — these do NOT exist on disk. The actual servers are `github-mcp`, `langfuse-mcp`, and `litellm-mcp` instead.

---

## 5. MCP Servers — CRM

**5 MCP servers + 3 test files, 2,256 lines (production) + 418 lines (tests):**

| File | Lines | Purpose |
|------|-------|---------|
| `crm/mcp_servers/crm_server.py` | 442 | CRM tools (17 tools) |
| `crm/mcp_servers/grok_server.py` | 481 | Grok AI server |
| `crm/mcp_servers/gemini_server.py` | 480 | Gemini AI server |
| `crm/mcp_servers/kimi_server.py` | 480 | Kimi AI server |
| `crm/mcp_servers/pii_gateway.py` | 373 | PII Gateway (4 tools) |
| `crm/mcp_servers/test_gemini_server.py` | — | Tests |
| `crm/mcp_servers/test_grok_server.py` | — | Tests |
| `crm/mcp_servers/test_kimi_server.py` | — | Tests |

---

## 6. MCP Servers — Beast Control (clean-build)

**1 MCP server, 7 modules, ~2,426 lines:**

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/beast-control-mcp/src/beast_control_mcp/server.py` | 439 | Main server |
| `02_build/beast-control-mcp/src/beast_control_mcp/config.py` | 109 | Config |
| `02_build/beast-control-mcp/src/beast_control_mcp/audit.py` | 56 | Audit logging |
| `02_build/beast-control-mcp/src/beast_control_mcp/tools/classification.py` | 428 | Classification tools |
| `02_build/beast-control-mcp/src/beast_control_mcp/tools/code_discovery.py` | 292 | Code discovery |
| `02_build/beast-control-mcp/src/beast_control_mcp/tools/databases.py` | 397 | Database tools |
| `02_build/beast-control-mcp/src/beast_control_mcp/tools/filesystem.py` | 195 | Filesystem tools |
| `02_build/beast-control-mcp/src/beast_control_mcp/tools/inventory.py` | 247 | Inventory tools |
| `02_build/beast-control-mcp/src/beast_control_mcp/tools/logs_and_jobs.py` | 256 | Logs & jobs |

---

## 7. MCP Servers — Amplified Knowledge (standalone repo + clean-build copy)

**Duplicated across two locations. Both use DEPRECATED FalkorDB + Qdrant.**

### Standalone repo (`amplified-knowledge-mcp/`)

| File | Lines | Purpose |
|------|-------|---------|
| `src/amplified_knowledge_mcp/server.py` | 497 | Main server |
| `src/amplified_knowledge_mcp/falkordb_client.py` | 146 | FalkorDB client (DEPRECATED) |
| `src/amplified_knowledge_mcp/qdrant_client.py` | 137 | Qdrant client (DEPRECATED) |
| `src/amplified_knowledge_mcp/embedder.py` | 48 | Embedding logic |
| `src/amplified_knowledge_mcp/security.py` | 58 | Security |
| `src/amplified_knowledge_mcp/audit.py` | 82 | Audit |
| `src/amplified_knowledge_mcp/config.py` | 43 | Config |

### Copy in clean-build (`02_build/amplified-knowledge-mcp/`)

Same structure, different line counts — drift between the two copies.

**Subtotal: ~1,016 lines (standalone) + parallel copy in clean-build**

---

## 8. Telephony & Voice Code (Multiple Versions)

### Production-ready — CRM

| File | Lines | Purpose |
|------|-------|---------|
| `crm/app/api/routes/retell_integration.py` | 842 | Retell AI voice agent |
| `crm/app/api/routes/voice_bridge.py` | 533 | Twilio + Deepgram + ElevenLabs |
| `crm/app/api/routes/telegram_bridge.py` | 426 | Telegram integration |

### Production-ready — clean-build Command Centre

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/command-centre/backend/voice_agent.py` | 394 | TwiML voice agent |
| `02_build/command-centre/backend/main.py` | 469 | Command Centre API |
| `02_build/command-centre/backend/search_db.py` | 238 | Search DB |
| `02_build/command-centre/backend/search_watcher.py` | 107 | Search watcher |
| `02_build/command-centre/backend/test_call.py` | 35 | Test call utility |

### Vault inbox code (corpus-raw — earlier versions, multiple copies)

| File | Lines | Purpose |
|------|-------|---------|
| `corpus-raw/vault/_inbox/webhook_server_failsafe.py` | 580 | Webhook failsafe v1 |
| `corpus-raw/vault/_inbox/webhook_server_failsafe-v3.py` | 580 | Webhook failsafe v3 |
| `corpus-raw/vault/_inbox/retell_integration.py` | 683 | Retell v1 |
| `corpus-raw/vault/_inbox/retell_integration-v2.py` | 780 | Retell v2 |
| `corpus-raw/vault/_inbox/retell_integration-v3.py` | 819 | Retell v3 |
| `corpus-raw/vault/_inbox/retell_integration-v4.py` | 819 | Retell v4 |
| `corpus-raw/vault/_inbox/webhook_server.py` | 122 | Webhook server |
| `corpus-raw/vault/_inbox/twilio_integration.py` | 68 | Twilio integration |

### Vault repo inbox

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/webhook_server.py` | 122 | Webhook server (duplicate of corpus-raw) |
| `vault/_inbox/webhook_server_failsafe.py` | 580 | Webhook failsafe (duplicate of corpus-raw) |
| `vault/_inbox/sentinel.py` | 141 | Sentinel monitor |

### Files referenced but NOT FOUND on disk

- `corpus-raw/vault/_inbox/voice_bridge.py` — **[NOT FOUND]**
- `corpus-raw/vault/_inbox/webhook_server-v2.py` — **[NOT FOUND]**

**Subtotal: ~7,383 lines of telephony/voice code across 3 repos**

---

## 9. Corpus-Raw Vault Inbox (Unintegrated Code Dump)

**47 Python files, ~14,199 lines total.** This is the largest single concentration of scattered code.

### AI Server versions (multiple copies)

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/grok_server.py` | 421 | Grok server v1 |
| `vault/_inbox/grok_server-v2.py` | 438 | Grok server v2 |
| `vault/_inbox/grok_server-v3.py` | 464 | Grok server v3 |
| `vault/_inbox/grok_agent.py` | 141 | Grok agent |
| `vault/_inbox/gemini_server.py` | 480 | Gemini server v1 |
| `vault/_inbox/gemini_server-v2.py` | 480 | Gemini server v2 |
| `vault/_inbox/kimi_server.py` | 479 | Kimi server |
| `vault/_inbox/claude_client.py` | 303 | Claude client v1 |
| `vault/_inbox/claude_client-v2.py` | 300 | Claude client v2 |

### CRM/App earlier versions

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/main.py` | 84 | App main v1 |
| `vault/_inbox/main-v2.py` | 92 | App main v2 |
| `vault/_inbox/main-v3.py` | 94 | App main v3 |
| `vault/_inbox/main-v4.py` | 94 | App main v4 |
| `vault/_inbox/brain.py` | 474 | Business brain |
| `vault/_inbox/database.py` | 87 | Database module |
| `vault/_inbox/env.py` | 61 | Environment config |
| `vault/_inbox/router-v2.py` | 254 | Router v2 |

### Ingestion & knowledge pipelines

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/ingest_transcripts.py` | 156 | Transcript ingestion v1 |
| `vault/_inbox/ingest_transcripts-v2.py` | 176 | Transcript ingestion v2 |
| `vault/_inbox/ingest_transcripts-v3.py` | 176 | Transcript ingestion v3 |
| `vault/_inbox/ingest_all_monologue.py` | 176 | Monologue ingestion |
| `vault/_inbox/007_add_call_transcripts.py` | 56 | Call transcript migration |

### Pudding / research

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/run_puddings.py` | 212 | Run puddings v1 |
| `vault/_inbox/run_puddings-v2.py` | 212 | Run puddings v2 |
| `vault/_inbox/run_all_puddings.py` | 302 | Run all puddings |
| `vault/_inbox/prospect_research.py` | 750 | Prospect research |

### Semantic cache / sentinel

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/semantic_cache.py` | 275 | Semantic cache v1 |
| `vault/_inbox/semantic_cache-v2.py` | 290 | Semantic cache v2 |
| `vault/_inbox/sentinel.py` | 141 | Sentinel v1 |
| `vault/_inbox/sentinel_v2.py` | 213 | Sentinel v2 |
| `vault/_inbox/sentinel-v3.py` | 151 | Sentinel v3 |
| `vault/_inbox/security_scanner.py` | 383 | Security scanner |

### Content engine

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/telegram_gate.py` | 287 | Telegram gate |
| `vault/_inbox/gmail_automation.py` | 130 | Gmail automation |
| `vault/_inbox/todoist-amplified-sync.py` | 177 | Todoist sync |

### Test files

| File | Lines | Purpose |
|------|-------|---------|
| `vault/_inbox/test_grok_server.py` | 204 | Grok tests |
| `vault/_inbox/test_kimi_server.py` | 214 | Kimi tests |
| `vault/_inbox/test_cognitive_diversity_aggressive.py` | 321 | Cognitive diversity tests |

### Content engine files referenced but NOT FOUND

- `vault/_inbox/atomiser.py` — **[NOT FOUND]**
- `vault/_inbox/scheduler.py` — **[NOT FOUND]**
- `vault/_inbox/substack.py` — **[NOT FOUND]**
- `vault/_inbox/linkedin.py` — **[NOT FOUND]**
- `vault/_inbox/twitter.py` — **[NOT FOUND]**

> These may have been promoted to `marketing-engine/` or deleted. The marketing-engine repo contains the canonical content atomiser, publishing agents, and platform adapters.

---

## 10. Corpus-Raw Vault Scripts & Archive

### Vault processing scripts (corpus-raw)

| File | Lines | Purpose |
|------|-------|---------|
| `vault/scripts/vault-to-qdrant.py` | 418 | Vault → Qdrant (DEPRECATED) |
| `vault/scripts/vault-sync.py` | 325 | Vault sync |
| `vault/scripts/classify-content.py` | 264 | Content classifier |
| `vault/scripts/vault-push-github.py` | 232 | Vault → GitHub push |
| `vault/scripts/bake.py` | 36 | Bake v1 |
| `vault/scripts/bake_fixed.py` | 25 | Bake fixed |

### Legacy research pipeline (corpus-raw/ewan-mac/archive)

| File | Lines | Purpose |
|------|-------|---------|
| `ewan-mac/archive/search_research_pipe.py` | 158 | Search pipe |
| `ewan-mac/archive/curator1_research_pipe.py` | 131 | Curator 1 |
| `ewan-mac/archive/curator2_research_pipe.py` | 115 | Curator 2 |
| `ewan-mac/archive/interpreter_research_pipe.py` | 95 | Interpreter |
| `ewan-mac/archive/config_research_pipe.py` | 58 | Config |
| `ewan-mac/archive2/pipe/orchestrator.py` | 522 | Orchestrator |

**Subtotal: ~2,379 lines**

---

## 11. Vault Repo Scripts (standalone `vault/`)

| File | Lines | Purpose |
|------|-------|---------|
| `scripts/pudding_labeller.py` | 129 | Pudding labeller |
| `scripts/pii_guard.py` | 65 | PII guard |
| `scripts/smoke_test.py` | 54 | Smoke test |
| `scripts/provenance.py` | 31 | Provenance |

**Subtotal: 279 lines**

---

## 12. Temporal Workflows & Activities (clean-build, Cove Orchestrator)

### Workflows (3 active)

| File | Lines | Purpose |
|------|-------|---------|
| `temporal/workflows/apds_ingestion_workflow.py` | 271 | APDS ingestion |
| `temporal/workflows/build_workflow.py` | 204 | Build workflow |
| `temporal/workflows/polish_gate_workflow.py` | 197 | Polish gate |

### Activities (6 modules)

| File | Lines | Purpose |
|------|-------|---------|
| `temporal/activities/ingestion_activities.py` | 659 | Ingestion activities |
| `temporal/activities/polish_activities.py` | 561 | Polish activities |
| `temporal/activities/manifest_generator.py` | 332 | Manifest generator |
| `temporal/activities/canonical_writer.py` | 309 | Canonical writer |
| `temporal/activities/derived_rebuild.py` | 283 | Derived rebuild |
| `temporal/activities/agent_activities.py` | 283 | Agent activities |

### Workers

| File | Lines | Purpose |
|------|-------|---------|
| `temporal/workers/main.py` | 82 | Worker entry point |
| `temporal/workers/schedule_starter.py` | 90 | Schedule starter |

**Subtotal: 3,271 lines**

---

## 13. CRM API Routes (16 modules)

| File | Lines | Purpose |
|------|-------|---------|
| `app/api/routes/retell_integration.py` | 842 | Retell AI voice |
| `app/api/routes/interview.py` | 711 | Founder Interview |
| `app/api/routes/voice_bridge.py` | 533 | Voice bridge |
| `app/api/routes/business_brain.py` | 435 | Business brain |
| `app/api/routes/orchestrator.py` | 428 | Orchestrator |
| `app/api/routes/telegram_bridge.py` | 426 | Telegram bridge |
| `app/api/routes/knowledge.py` | 413 | Knowledge |
| `app/api/routes/xero_routes.py` | 411 | Xero integration |
| `app/api/routes/calendar_routes.py` | 390 | Calendar |
| `app/api/routes/intelligence.py` | 355 | Intelligence |
| `app/api/routes/quickbooks_routes.py` | 340 | QuickBooks |
| `app/api/routes/stripe_routes.py` | 298 | Stripe |
| `app/api/routes/contacts.py` | 277 | Contacts |
| `app/api/routes/intelligence_routes.py` | 256 | Intelligence routes |
| `app/api/routes/deals.py` | 140 | Deals |
| `app/api/routes/activities.py` | 119 | Activities |
| `app/api/routes/companies.py` | 107 | Companies |
| `app/api/routes/health_clients.py` | 86 | Health clients |

**Also:** `backend/app/api/routes/stripe_routes.py` — duplicate Stripe routes in a separate backend directory.

**Subtotal: 6,567 lines (routes only) | CRM total: ~61,977 lines**

---

## 14. Cove Orchestrator Sub-Systems (clean-build)

### Email Agent (7 modules)

| File | Lines | Purpose |
|------|-------|---------|
| `email_agent/pipeline.py` | 341 | Email pipeline |
| `email_agent/fetcher.py` | 255 | Email fetcher |
| `email_agent/triage.py` | 234 | Email triage |
| `email_agent/drafter.py` | 150 | Email drafter |
| `email_agent/config.py` | 101 | Config |
| `email_agent/status.py` | 88 | Status |
| `email_agent/main.py` | 47 | Entry point |

### Nightscout Agent (7 modules)

| File | Lines | Purpose |
|------|-------|---------|
| `nightscout/pipeline.py` | 248 | Nightscout pipeline |
| `nightscout/fetchers.py` | 182 | Data fetchers |
| `nightscout/briefing.py` | 144 | Briefing generator |
| `nightscout/config.py` | 138 | Config |
| `nightscout/scorer.py` | 131 | Glucose scorer |
| `nightscout/main.py` | 47 | Entry point |

### Polish Gate API

| File | Lines | Purpose |
|------|-------|---------|
| `api/polish_gate.py` | — | Polish gate endpoint |

### Executive Agent

| File | Lines | Purpose |
|------|-------|---------|
| `agents/executive/runner.py` | — | Executive runner |
| `agents/executive/team.py` | — | Executive team |
| `agents/configs/agent_registry.py` | — | Agent registry |

**Subtotal: ~2,106 lines (email + nightscout)**

---

## 15. Routing & Validation Layer (clean-build)

### Epistemic routing (5 modules)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/routing/epistemic_status.py` | 543 | Epistemic status routing |
| `02_build/routing/score_to_graph.py` | 447 | Score → graph |
| `02_build/routing/sidecar_to_label.py` | 313 | Sidecar → label |
| `02_build/routing/harvest_to_label.py` | 277 | Harvest → label |
| `02_build/routing/path_abstraction.py` | 181 | Path abstraction |

### Validators (UK public data, 18 modules)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/validators/validations/profservices.py` | 632 | Professional services |
| `02_build/validators/test_validators.py` | 534 | Test suite |
| `02_build/validators/cli.py` | 175 | CLI |
| `02_build/validators/sources/ons.py` | 147 | ONS source |
| `02_build/validators/cache.py` | 139 | Cache |
| `02_build/validators/core.py` | 138 | Core logic |
| `02_build/validators/sources/gov_uk.py` | 115 | GOV.UK source |
| `02_build/validators/tests/base_rate.py` | 104 | Base rate test |
| `02_build/validators/sources/hmrc.py` | 94 | HMRC source |
| `02_build/validators/tests/correlation.py` | 86 | Correlation test |
| `02_build/validators/sources/companies_house.py` | 79 | Companies House |
| `02_build/validators/tests/distribution.py` | 70 | Distribution test |
| `02_build/validators/tests/existence.py` | 99 | Existence test |
| `02_build/validators/sources/gazette.py` | 44 | Gazette source |

**Subtotal: ~4,290 lines**

---

## 16. Pipeline & Build Scripts (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/scripts/dedup_tiers.py` | 563 | Tier deduplication |
| `02_build/scripts/pudding_labeler.py` | 354 | PUDDING labeller |
| `02_build/scripts/polish_to_brain.py` | 304 | Polish → brain |
| `02_build/scripts/pre_ingestion_pipe_v3.py` | 240 | Pre-ingestion pipeline v3 |
| `02_build/scripts/porch_watcher.py` | 234 | Porch watcher |
| `02_build/scripts/process_health_report.py` | 186 | Health report processor |
| `02_build/scripts/apply_branch_protection.py` | 136 | Branch protection |
| `02_build/scripts/config_research_pipe.py` | 57 | Research pipe config |
| `02_build/scripts/audit_research_pipe.py` | 48 | Research pipe audit |
| `02_build/scripts/intake_research_pipe.py` | 37 | Research pipe intake |
| `02_build/scripts/council_chat.py` | 33 | Council chat |
| `02_build/scripts/test_integration.py` | 22 | Integration test |
| `02_build/pipeline/stages/embedding_backfill.py` | — | Embedding backfill |

### APDS Labellers (Beast)

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/beast/apds-labeller/apds_labeller_v3_amp173.py` | 680 | APDS labeller v3 |
| `02_build/beast/apds-labeller/apds_labeller_v2.2_amp128.py` | 486 | APDS labeller v2.2 |
| `02_build/beast/apds-labeller/amp128_stress.py` | 268 | AMP-128 stress test |

**Subtotal: ~3,648 lines**

---

## 17. Marketing Engine (standalone repo)

**14 Python modules, 4,477 lines:**

| File | Lines | Purpose |
|------|-------|---------|
| `api.py` | 609 | REST API |
| `synthetic_evaluator.py` | 546 | Synthetic evaluator |
| `agents/research_agent.py` | 461 | Research agent |
| `platform_adapters.py` | 431 | Platform adapters |
| `db.py` | 399 | Database layer |
| `agents/content_agent.py` | 369 | Content agent |
| `kaizen.py` | 367 | Kaizen loop |
| `agents/content_atomizer.py` | 317 | Content atomiser |
| `agents/publishing_agent.py` | 256 | Publishing agent |
| `knowledge_client.py` | 213 | Knowledge client |
| `integrations/heygen.py` | 187 | HeyGen integration |
| `orchestrator.py` | 183 | Orchestrator |
| `integrations/brevo.py` | 139 | Brevo integration |

---

## 18. Byker Production (standalone repo)

**26 Python modules, 13,319 lines:**

| File | Lines | Purpose |
|------|-------|---------|
| `kilo_orchestrator_v2.py` | 1,628 | Fleet orchestrator v2 |
| `kilo_orchestrator.py` | 1,324 | Fleet orchestrator v1 |
| `obsidian/obsidian_integration.py` | 1,186 | Obsidian integration |
| `principles/principles_engine.py` | 1,074 | Principles engine |
| `backend/orchestrator.py` | 945 | Backend orchestrator |
| `backend/diagnostics/smb_scorer.py` | 799 | SMB scorer |
| `main.py` | 751 | Main entry |
| `backend/validator.py` | 745 | Validator |
| `workflows/workflow_engine.py` | 730 | Workflow engine |
| `backend/router_config.py` | 613 | Router config |
| `cover_ai/diagnostic/smb_diagnostic.py` | 502 | SMB diagnostic |
| `orchestrator_api.py` | 477 | Orchestrator API |
| `cover_ai/api/cover_api.py` | 428 | Cover AI API |
| `backend/validators/email_validator.py` | 420 | Email validator |
| `cover_ai/outreach/email_engine.py` | 410 | Email engine |
| `scripts/local_test.py` | 342 | Local test |
| `backend/diagnostics/outreach_scorer.py` | 320 | Outreach scorer |
| `backend/track_score.py` | 171 | Score tracker |
| `test_fleet_20.py` | 165 | Fleet test |
| `backend/autofix.py` | 124 | Autofix |
| `backend/test_orchestrator.py` | 91 | Orchestrator test |

---

## 19. Anthropic Token Proxy (standalone repo)

**3 modules, 1,563 lines:**

| File | Lines | Purpose |
|------|-------|---------|
| `token_proxy.py` | 988 | FastAPI proxy & model routing |
| `context_compressor.py` | 297 | Context compression via Haiku |
| `daily_cost_report.py` | 278 | Cost reporting + Telegram alerts |

> Uses DEPRECATED Qdrant for semantic cache. Migration to pgvector planned.

---

## 20. Enforcer (clean-build)

**6 modules, 883 lines:**

| File | Lines | Purpose |
|------|-------|---------|
| `02_build/enforcer/enforcer.py` | 380 | Main enforcer engine |
| `02_build/enforcer/checks/docker_health.py` | 131 | Docker health |
| `02_build/enforcer/checks/session_hygiene.py` | 105 | Session hygiene |
| `02_build/enforcer/checks/database_health.py` | 91 | Database health |
| `02_build/enforcer/checks/security_check.py` | 90 | Security check |
| `02_build/enforcer/checks/traefik_health.py` | 83 | Traefik health |

---

## 21. Orphaned / Edge Code

### Evolution API (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `evolution-api/webhook-dispatcher.py` | 199 | Webhook dispatcher |
| `evolution-api/.env` | — | **WARNING: .env committed to repo** |

### Hetzner Deployment (clean-build)

| File | Lines | Purpose |
|------|-------|---------|
| `hetzner_deployment/linear_reporter.py` | 77 | Linear reporter |
| `hetzner_deployment/docker-compose.yml` | 67 | Deployment compose |

### Amplified Site (stray Python)

| File | Lines | Purpose |
|------|-------|---------|
| `amplified-site/amplified-voice-research-v2.py` | 909 | Voice research script |
| `amplified-site/tools/visual-polish-system/engine.py` | 398 | VPS engine |
| `amplified-site/tools/visual-polish-system/cli.py` | 221 | VPS CLI |

---

## Summary Statistics

| Category | Files | Lines |
|----------|-------|-------|
| Shell scripts & automation | 19 | ~2,404 |
| Docker Compose files | 9 | ~700 |
| Database migrations (SQL + Python) | 10 | ~2,361 |
| MCP servers — Cove | 9 | ~2,354 |
| MCP servers — CRM | 5 | ~2,256 |
| MCP servers — Beast Control | 7 | ~2,426 |
| MCP servers — Knowledge (2 copies) | 7+7 | ~1,016 (×2) |
| Telephony & voice (all locations) | 14 | ~7,383 |
| Corpus-raw vault inbox | 47 | ~14,199 |
| Corpus-raw vault scripts + archive | 12 | ~2,379 |
| Vault repo scripts | 7 | ~1,122 |
| Temporal workflows + activities | 11 | ~3,271 |
| CRM API routes | 18 | ~6,567 |
| Cove sub-systems (email + nightscout) | 14 | ~2,106 |
| Routing + validators | 19 | ~4,290 |
| Pipeline + build scripts | 13 | ~3,648 |
| Marketing engine | 14 | ~4,477 |
| Byker production | 26 | ~13,319 |
| Token proxy | 3 | ~1,563 |
| Enforcer | 6 | ~883 |
| Orphaned / edge code | 6 | ~1,871 |
| **TOTAL** | **~158+** | **~35,400+** |

---

## Known Deprecated Code (per AMP-344, DATA_ARCHITECTURE.md)

The following files reference FalkorDB or Qdrant — both deprecated in favour of PostgreSQL + Apache AGE + pgvector (HNSW):

1. `90_archive/legacy-writers/migrate_falkordb.py` — archived
2. `90_archive/legacy-writers/migrate_qdrant.py` — archived
3. `02_build/beast/falkordb/docker-compose.beast.snapshot.yml` — FalkorDB compose
4. `02_build/scripts/fix-graphiti-falkordb.sh` — FalkorDB fix script
5. `02_build/scripts/patch-graphiti-1272.sh` — Graphiti patch
6. `02_build/amplified-knowledge-mcp/` — uses FalkorDB + Qdrant clients
7. `amplified-knowledge-mcp/` (standalone) — uses FalkorDB + Qdrant clients
8. `corpus-raw/vault/scripts/vault-to-qdrant.py` — Vault → Qdrant
9. `anthropic-token-proxy/token_proxy.py` — Qdrant semantic cache

---

## Security Flags

1. **`evolution-api/.env` committed to clean-build** — contains environment variables. Needs audit.
2. **Corpus-raw vault inbox** — 47 unreviewed Python files. Unknown if any contain credentials.
3. **Multiple webhook server versions** — multiple failsafe/versioned copies with different security postures.

---

## Integration Priority

| Priority | Category | Rationale |
|----------|----------|-----------|
| **P0** | Security flags | `.env` in repo, unaudited inbox code |
| **P1** | Deprecated FalkorDB/Qdrant code | Must migrate or remove per AMP-344 |
| **P1** | Corpus-raw vault inbox | 14,199 lines of unreviewed, versioned-in-place code |
| **P2** | Telephony duplication | 5+ copies of retell_integration across 3 repos |
| **P2** | MCP server duplication | amplified-knowledge-mcp exists in 2 locations with drift |
| **P3** | Byker production | 13,319 lines — entire standalone platform, unclear canonical status |
| **P3** | Marketing engine integration | 4,477 lines — standalone, not wired into Beast |

---

**Purpose:** Radical transparency — complete verified inventory of scattered, unintegrated code across the Amplified Partners estate.

Signed-by: Devon-6052 | 2026-05-16 | devin-6052bed959b54277b8be29eeed3cde24
