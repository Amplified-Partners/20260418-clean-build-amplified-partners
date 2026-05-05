---
title: Decision log
date: 2026-05-05
version: 20
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## How to use

One entry per decision. Keep it short. Link out to supporting docs.

## Entries

### 2026-05-05 — CODEOWNERS added to clean-build (governance enforcement via GitHub)

- **Decision**: Add `.github/CODEOWNERS` to `Amplified-Partners/clean-build` requiring `@ewanbramley` as a reviewer for all changes to `00_authority/**` and `01_truth/**`. No default `*` owner — other paths remain open for any reviewer.
- **Why**: `00_authority/` and `01_truth/` contain governance and truth-layer documents. Changes to these paths are significant or irreversible and should require Ewan's review before merge. GitHub's CODEOWNERS mechanism enforces this automatically at PR time.
- **Where encoded**: `.github/CODEOWNERS`; `00_authority/MANIFEST.md` v51; this entry.
- **Status**: active (pending PR merge).
- **Signed-by**: Devon-codeowners-daughter | 2026-05-05 | devin-487f10ace93b4cdfbcc49f9bb5c300b0

### 2026-05-04 — LiteLLM secrets moved to `.env` + compose mirrored (AMP-72)

- **Decision**: Move all seven secret values out of `/opt/amplified/apps/litellm/docker-compose.yml` (`LITELLM_MASTER_KEY`, `DATABASE_URL` with embedded Postgres password, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `MOONSHOT_API_KEY`, `DEEPSEEK_API_KEY`, `XAI_API_KEY_BEAST`) into a sibling `.env` file at `/opt/amplified/apps/litellm/.env` (mode 600, owner root, gitignored, never mirrored anywhere). Compose now references via `env_file: - .env`; non-secret connection metadata (`REDIS_HOST`, `REDIS_PORT`) stays inline. Mirror the cleaned compose into `02_build/compose/litellm/docker-compose.yml` with a README following the AMP-46 Ollama precedent. Update the existing rotation script at `/opt/amplified/secrets/rotation/rotate-keys.sh` to also write the new `.env` (it already updates `.env` files for the cove-orchestrator stack).
- **Why**: Linear ticket [AMP-72](https://linear.app/amplifiedpartners/issue/AMP-72/) — surfaced during AMP-71 implementation. Plaintext secrets in source-of-truth files are a one-way ratchet: every backup, snapshot, accidental scp, or cross-agent fix attempt copies them. The compose was readable by anything with root on Beast and could not be mirrored into version control without committing secrets. Moving to an `env_file` reference is the standard 12-factor pattern, fully reversible until any subsequent rotation, and unblocks version-control mirroring of the compose itself.
- **Where encoded**:
  - Live config: `/opt/amplified/apps/litellm/docker-compose.yml` on Beast (no inline secrets remaining; signed leading comment).
  - Live secrets: `/opt/amplified/apps/litellm/.env` on Beast (mode 600, root-owned, gitignored).
  - Rotation: `/opt/amplified/secrets/rotation/rotate-keys.sh` updated with `LITELLM_ENV_FILE` variable + `update_litellm_env` function + backup hook (signed comments mark the AMP-72 additions).
  - Repo mirror: `02_build/compose/litellm/docker-compose.yml` + `02_build/compose/litellm/README.md` (this PR).
  - Manifest: `02_build/INFRASTRUCTURE.md` v5 — LiteLLM row updated, compose-file-locations table updated, changelog entry signed.
- **Verification**: After `docker compose up -d --force-recreate litellm`, all 9 expected env vars (7 secrets + `REDIS_HOST` + `REDIS_PORT`) resolve inside the container. `curl http://127.0.0.1:4000/health/liveliness` (host loopback), in-net DNS via `http://litellm:4000/health/liveliness`, and `https://litellm.beast.amplifiedpartners.ai/health/liveliness` (Traefik public) all return 200. End-to-end provider smoke test against `/chat/completions`: 5 of 6 providers return PONG (Anthropic via `claude-haiku`, Moonshot via `kimi-k2.6`, DeepSeek via `deepseek-v4-flash`, xAI via `grok-fast`, local/Ollama via `local/llama3.1-8b`). OpenAI returns `AuthenticationError: Incorrect API key` — verified pre-existing (the same key value in `docker-compose.yml.bak.20260503-amp71` is byte-identical to the one now in `.env`, and the same key fails when called directly against `https://api.openai.com/v1/models`); AMP-72 migration did not change a byte. Tracked separately for Ewan; not blocking.
- **Status**: active
- **Reversible**: yes — backups at `/opt/amplified/apps/litellm/docker-compose.yml.bak.20260504-amp72` + `.env.bak.20260504-amp72`; restore is a `cp` of either backup over the live file followed by `docker compose up -d --force-recreate litellm`.
- **Out of scope (deliberate)**: Key rotation. The original AMP-72 description called for rotating every key after the move. Rotation has non-trivial blast radius — the LiteLLM master key gates 3 virtual keys in the LiteLLM Postgres DB plus consumers across `agent-stack/cove-orchestrator/` and `agent-stack/vault-ingestion/` — and the existing monthly rotation script (`rotate-keys.sh`, last ran 2026-05-01) is the right channel for it. The `.env` migration alone delivers the structural fix (compose mirror unblocked, root-only file mode, gitignored). Rotation will follow on the next monthly cron or under a dedicated ticket once consumers are inventoried.
- **Signed-by**: Devon-a9a7 | 2026-05-04 | devin-a9a78d0c72d9491aa3a70b18cb741936

### 2026-05-03 — LiteLLM host-loopback port mapping + pudding-testing env-driven base URLs (AMP-71)

- **Decision**: Add a host-loopback port mapping (`127.0.0.1:4000:4000`) to the LiteLLM container's `docker-compose.yml` on Beast (`/opt/amplified/apps/litellm/docker-compose.yml`). Loopback only — not bound to `0.0.0.0`. Refactor `/opt/amplified/pudding-testing/src/llm.py` (Beast-side test harness, not in any repo) to read base URLs from environment variables (`LITELLM_BASE_URL`, `OLLAMA_BASE_URL`) with host-loopback defaults. **Do not** mirror the LiteLLM compose into version control: the live file embeds plaintext API keys for five providers plus the LiteLLM master key and a Postgres URL with embedded password (see related ticket [AMP-72](https://linear.app/amplifiedpartners/issue/AMP-72/)).
- **Why**: Linear ticket [AMP-71](https://linear.app/amplifiedpartners/issue/AMP-71/) — surfaced during AMP-46 review. The same brittleness pattern AMP-46 fixed for Ollama also affected LiteLLM and the pudding-testing harness: hardcoded Docker bridge IPs (`172.18.0.9` for LiteLLM, `172.18.0.14` for Ollama) that change on container recreation. Closing the loop on the bridge-IP class of bug across all in-repo and Beast-side touchpoints. Env-driven defaults are deliberate so the same script works whether run on the host (loopback) or inside a container on `amplified-net` (override to `litellm:4000` / `ollama:11434`).
- **Where encoded**:
  - Live config: `/opt/amplified/apps/litellm/docker-compose.yml` on Beast (signed leading comment).
  - Beast-side script: `/opt/amplified/pudding-testing/src/llm.py` — `LLMConfig.base_url` and `EmbeddingClient.__init__` are now env-driven.
  - Manifest: `02_build/INFRASTRUCTURE.md` v4 — LiteLLM row updated, changelog entry signed.
  - Repo mirror of compose: **not done deliberately** — gated on AMP-72.
- **Verification**: `ss -tlnp | grep ':4000 '` shows `LISTEN 127.0.0.1:4000` (loopback only). `curl http://127.0.0.1:4000/health/liveliness` (host) → 200. `curl http://litellm:4000/health/liveliness` from a container on `amplified-net` → 200 (no DNS regression). `curl https://litellm.beast.amplifiedpartners.ai/health/liveliness` → 200 (Traefik route still works). Smoke test on the refactored `llm.py` confirms defaults resolve to `127.0.0.1:4000` and `127.0.0.1:11434`, env overrides work, and explicit positional override on `EmbeddingClient` still works (back-compat).
- **Status**: active
- **Reversible**: yes — remove the `ports:` block on Beast and `docker compose up -d litellm` returns to in-network-only.
- **Signed-by**: Devon-a9a7 | 2026-05-03 | devin-a9a78d0c72d9491aa3a70b18cb741936

### 2026-05-03 — cost-tools (token_proxy.py) deployed on Beast and indexed in spine

- **Decision**: Deploy `cost-tools/token_proxy.py` on Beast as the `token-proxy` container on `amplified-net`, with `restart: always` + healthcheck on `/proxy/stats`. Index it in the authority spine via `01_truth/SYSTEMS-AND-API-REGISTER.md` v2 (cost-tools section), `02_build/INFRASTRUCTURE.md` v2 (token-proxy row under AI / ML services), and this entry. The proxy adds Sonnet→Haiku model-layer routing for extractive/classificatory prompts, prompt caching, semantic similarity cache (Qdrant `llm_cache`, 0.95 threshold, 24h TTL), native context compaction, and a daily $100 budget circuit-breaker.
- **Why**: AMP-28 verification revealed the optimiser was on disk at `/opt/amplified/apps/real/token_proxy.py` since 2026-03-12 but had never been deployed (Mac-specific code paths, no Dockerfile, no compose, no RUNBOOK), and was not indexed anywhere in the authority spine. Verification (n=69 calls, 100% routing accuracy on the labelled set, 30.7% saved on the test sample, 5× latency drop, 0 failures) showed the routing logic works on real Anthropic traffic; live canary calls on Beast confirmed Sonnet→Haiku for extractive prompts and Sonnet retained for strategic prompts. Indexing it in the spine prevents the same code from going dormant again.
- **Where encoded**: `Amplified-Partners/cost-tools#2` (Linux portability patch + Dockerfile + docker-compose + RUNBOOK + README); `01_truth/SYSTEMS-AND-API-REGISTER.md` v2; `02_build/INFRASTRUCTURE.md` v2; `00_authority/MANIFEST.md` v49; `03_shadow/job-wrapups/2026-05-03_cost-tools-resurrection_v1.md`.
- **Status**: active (proxy running on Beast; canary agents not yet wired — held until cost-tools PR is reviewed).
- **Signed-by**: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### 2026-05-03 — Agent routing rule established (AGENT_ROUTING.md)

- **Decision**: Create `00_authority/AGENT_ROUTING.md` v1 (`[LOGIC TO BE CONFIRMED]`) as the agent-layer routing rule — which agent (Devon, Cassian/OpenClaw, Cursor, Antigravity, Perplexity, Qwen) runs which class of task. Eight rules covering live-infrastructure code, clean-build edits, vault content, strategic decisions, external research, novel decisions, scheduled tasks, and customer-facing change. Stacks on top of `cost-tools/token_proxy.py` (the model-layer routing) and references but does not duplicate `00_authority/TAXONOMY.md` (the agent roster).
- **Why**: AMP-28 asked for a routing rule. Without an explicit rule, agents inferred their own routing (which led to the cost-tools proxy being lost — nobody owned its deployment). This file is the missing coordination contract. Cost-tier classification is explicitly the proxy's job, not the taxonomy's job, so this file does not assign cost tiers per agent.
- **Where encoded**: `00_authority/AGENT_ROUTING.md` v1; `00_authority/MANIFEST.md` v49 § Candidate authority.
- **Status**: candidate (pending Ewan review).
- **Signed-by**: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### 2026-05-03 — Public-data validation framework + ProfServices pilot (AMP-67)

- **Decision**: Create `01_truth/schemas/2026-05_public-data-validation_v1.md` defining the 3-band PROVEN / PLAUSIBLE / DISPROVEN public-data verdict scheme + BLOCKED gap-marker, and an additive `VALIDATION:` field on the insight catalogue (literature `STATUS:` field unchanged). Build the reference implementation at `02_build/validators/` (vertical-agnostic; fetchers in `sources/`, reusable test classes in `tests/`, CLI orchestrator). Land verdicts in `03_shadow/validators/<vertical>/<INS-NNN>/verdict.json` first; promote to `01_truth/research/validations/` after human review. Run the framework against the 16 ProfServices catalogue entries (INS-079 .. INS-094) as the first vertical. All 16 came back PROVEN or PLAUSIBLE; zero DISPROVEN.
- **Why**: AMP-67 (under parent AMP-59) directed real-public-data validation of the ProfServices vertical, with the framework reusable across the four other verticals (AMP-64/65/66/68). The shadow-then-promote path keeps verdicts non-authoritative until reviewed; the schema is the contract every vertical follows.
- **Where encoded**: `01_truth/schemas/2026-05_public-data-validation_v1.md` v1, `02_build/validators/` (framework + ProfServices runners), `03_shadow/validators/profservices/` (16 verdict JSONs + `rollup.json`), `01_truth/schemas/research-index/00-insight-catalogue_v1.md` (16 `VALIDATION:` lines added), `01_truth/research/validations/README.md` (truth-tier promotion stub), `00_authority/MANIFEST.md` v45–v48 changelog entries.
- **Status**: candidate (pending Ewan review of the PR + verdicts)
- **Signed-by**: Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293

### 2026-05-03 — Ollama port-mapping fix on Beast (AMP-46)

- **Decision**: Add a host-loopback port mapping (`127.0.0.1:11434:11434`) to the Ollama container's `docker-compose.yml` on Beast (`/opt/amplified/apps/ollama/docker-compose.yml`). Mirror the compose file into version control at `02_build/compose/ollama/docker-compose.yml`. Loopback only — not bound to `0.0.0.0`. Public access remains only via the existing Traefik HTTPS route at `ollama.beast.amplifiedpartners.ai`.
- **Why**: Linear ticket [AMP-46](https://linear.app/amplifiedpartners/issue/AMP-46/beast-ops-fix-ollama-container-port-mapping). Ollama was reachable inside `amplified-net` (via Docker DNS `ollama:11434`) but not from the Beast host itself, which broke Beast-side scripts. The Arbiter shipped a workaround that pointed `pudding_extractor.py` at the bridge IP `172.18.0.3:11434` — brittle, because Docker bridge IPs churn on container restart. Loopback is the canonical, stable host-side address.
- **Where encoded**:
  - Live config: `/opt/amplified/apps/ollama/docker-compose.yml` on Beast (signed leading comment).
  - Repo mirror: `02_build/compose/ollama/docker-compose.yml` + `02_build/compose/ollama/README.md`.
  - Manifest: `02_build/INFRASTRUCTURE.md` v3 — Ollama row updated, changelog entry signed.
  - Workaround revert: `/opt/amplified/pudding_extractor.py` on Beast — bridge IP `172.18.0.3` swapped back to canonical `127.0.0.1`. Beast-side only, not in any repo.
- **Verification**: `curl http://127.0.0.1:11434/api/tags` (host) → 200, 4 models. `curl http://ollama:11434/api/tags` from a container on `amplified-net` → 200 (no DNS regression). `curl https://ollama.beast.amplifiedpartners.ai/api/tags` → 200 (Traefik route still works).
- **Status**: active
- **Reversible**: yes — remove the `ports:` block and `docker compose up -d ollama` returns to in-network-only.
- **Signed-by**: Devon-a9a7 | 2026-05-03 | devin-a9a78d0c72d9491aa3a70b18cb741936

### 2026-05-01 — Systems and API Register created as candidate authority

- **Decision**: Create `01_truth/SYSTEMS-AND-API-REGISTER.md` — a single register documenting all pre-built APIs, MCP servers, telephony systems, and code modules across all Amplified Partners repos. Indexed in MANIFEST.md v40 as `[LOGIC TO BE CONFIRMED]`.
- **Why**: Architect directed ("we need a register somewhere ... a document that tells us what's where because nobody can remember"). Automated scan found 124 CRM REST endpoints, 24 Command Centre endpoints, 19 Marketing Engine endpoints, 13 MCP servers (8 Cove with 37 tools + 5 CRM), and a complete telephony inventory (7 providers, 6 modules across 8 files) — far more than the ~20 originally expected. Without a single register, this knowledge existed only in the codebase and was not discoverable without grepping every repo.
- **Where encoded**: `01_truth/SYSTEMS-AND-API-REGISTER.md` v1, `00_authority/MANIFEST.md` v40 § Candidate authority.
- **Status**: candidate (pending Ewan review)
- **Signed-by**: Devon (Devin session `f32d587cc3e54f959c5309d93f72bc97`) — 2026-05-01

### 2026-04-30 — Infrastructure manifest created as canonical inventory

- **Decision**: Create `02_build/INFRASTRUCTURE.md` as the single source of truth for all infrastructure on Amplified Core (135.181.161.131). Promote to **Authoritative now** in MANIFEST.md. Replace the partial infrastructure table in STATUS.md with a pointer to the manifest.
- **Why**: Architect directed ("we need a central, obvious place where current infrastructure is stored ... single point of truth"). Server runs 40 containers across 16+ compose stacks — no complete inventory existed. STATUS.md had a partial 8-row table that was already stale. The manifest covers every container, scheduled job, compose file location, network topology, and server specs. Written in plain language so anyone (human or AI) can understand what each thing does.
- **Where encoded**: `02_build/INFRASTRUCTURE.md` v1, `00_authority/MANIFEST.md` v44 § Authoritative now, `STATUS.md` v2 (infrastructure section now points to manifest).
- **Status**: active
- **Signed-by**: Devon | 2026-04-30 | devin-66aa3ce48c7e407f8ad9bf066541b604

### 2026-04-29 — Phase 2: 15 additional Mac drop specs ingested to 90_archive/specifications/

- **Decision**: Ingest 15 additional specifications from Ewan's Mac drop (Phase 2) into `90_archive/specifications/mac-drop-2026-04/`. All `[NON-AUTHORITATIVE]`. Total archive now 30 files, 33,153 lines.
- **Why**: Phase 1 covered constitutional and architectural specs. Phase 2 covers operational specs and named systems: APDS (the scientific backbone), AMF, Kaizen Department, Beast rebuild, Visual Polish, Extraction Department, RIC, Watchman, Curator Gate, Insight Catalogue (136 entries × £30k avg), and three safety systems (P7, P8, P10). Without these, agents cannot understand the operational layer of Amplified Partners.
- **Where encoded**: `90_archive/specifications/mac-drop-2026-04/README.md` (updated), `00_authority/MANIFEST.md` v39 § Reference only.
- **Status**: active
- **Signed-by**: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### 2026-04-29 — Mac drop specifications ingested to 90_archive/specifications/

- **Decision**: Ingest 15 major specifications from Ewan's Mac drop ("New Folder With Items 2.zip", 521 files, 125MB) into `90_archive/specifications/mac-drop-2026-04/`. All indexed as `[NON-AUTHORITATIVE]` in MANIFEST.md v38. No document promoted to authority — promotion requires separate review.
- **Why**: These specifications (5 constitutional documents, 2 naming/organisation conventions, 8 architectural specs) represent months of architectural thinking that was previously only on Ewan's Mac. Not in the vault, not in GitHub, not discoverable by any agent. Agents were rediscovering and rebuilding work that already existed. Ingesting as reference makes them discoverable without prematurely granting authority status.
- **What was ingested**: ATTRIBUTION-AND-CURATION-v1, VALIDATION-METHODOLOGY-v2, CODE-TAXONOMY-AND-KAIZEN-v1, SCORING-UNIFICATION-HYPOTHESIS-v2, DOPPELGANGER-TESTING-AND-AGENT-VERSIONING-v1, FILE-NAMING-CONVENTION-v1, DUAL-CODE-ORGANISATION-v1, vault-extraction-pipeline-design, amplified-agents-master, business-brain-framework, process-scaffold-framework, amplified-integration-layer, AMPLIFIED-SEARCH-ORCHESTRATION-METHODOLOGY, PUDDING-VALUE-MATHEMATICAL-MODEL-v1, pudding-taxonomy-synthesis.
- **Where encoded**: `90_archive/specifications/mac-drop-2026-04/README.md`, `00_authority/MANIFEST.md` v38 § Reference only.
- **Status**: active
- **Signed-by**: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### 2026-04-29 — STATUS.md created as Devon↔OpenClaw async operations board

- **Decision**: Create `STATUS.md` in clean-build root as the two-way async handshake between Devon (infrastructure) and OpenClaw (coordination). Devon writes infrastructure status, OpenClaw reads and writes back findings. Versioned handoffs via GitHub — no chat relay through Ewan.
- **Why**: Architect directed (session 2026-04-29). Three agents (Devon, OpenClaw, Cursor) need to coordinate without Ewan copy-pasting between them. GitHub is the single source of truth. Each agent reads, acts, writes back. Asynchronous by default.
- **Where encoded**: `STATUS.md` v1, `00_authority/MANIFEST.md` v37 § Authoritative now, `00_authority/TAXONOMY.md` § Operating model (agent coordination).
- **Status**: active
- **Signed-by**: Devon (Devin session `aa4d863ad679468692e75a40b8825358`) — 2026-04-29

### 2026-04-23 — PR reviewer rules codified in root `AGENTS.md`

- **Decision**: Add a new "PR reviewers (Devin Review, Codex, Copilot, human) — what to flag" section to root `AGENTS.md` that codifies the finding-classes already caught by review on PR #1, plus an explicit "Do not flag" list for style preferences. Seven flag-classes (bibliography, signatures, authority changelog, DECISION_LOG pointer, self-contradicting examples, cross-file factual inaccuracy, MANIFEST indexing) and five don't-flag-classes (voice, hedging, heading order, author/reviewer opinion, line length).
- **Why**: PR #1 review surfaced seven findings, all real, all from the same small set of classes. Codifying them: (a) raises the common bar for every reviewer (Devin Review, Codex, Copilot, human), (b) prevents style bikeshedding, (c) gives agents a predictable target when shipping. This replaces "reviewer discretion" with "defined defect classes".
- **Where encoded**: `AGENTS.md` § "PR reviewers — what to flag" (root file, post-merge tightening PR). Derived from findings on PR #1. Cross-references `00_authority/SIGNATURES.md`, `00_authority/AGENTS.md` (authority changelog rule), `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (DECISION_LOG pointer rule).
- **Status**: active
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-23 — Three authoritative agent-conduct rules added (signatures, use-it-or-cut-it, opinion-confidence)

- **Decision**: Promote three new files to **Authoritative now**: `00_authority/SIGNATURES.md` (every AI signs committed work; minimum content = name + date + session/instance id; format at agent's discretion), `00_authority/USE_IT_OR_CUT_IT.md` (unused implementations are cut; archive/provenance exempt), `00_authority/OPINION_CONFIDENCE.md` (opinions must be labelled + paired with a confidence number; tiered thresholds 50% reversible / 85% medium / 95% irreversible-or-escalate; below-floor triggers bounded research).
- **Why**: Architect-directed (session 2026-04-23). Signatures apply Radical Attribution mechanically. Use-it-or-cut-it is the remediation side of the "is it useful?" prevention question. Opinion-confidence calibrates agent judgement and routes decisions to the right level without pulling Ewan into every call.
- **Where encoded**: `00_authority/SIGNATURES.md` v1, `00_authority/USE_IT_OR_CUT_IT.md` v1, `00_authority/OPINION_CONFIDENCE.md` v1, `00_authority/MANIFEST.md` v34, `AGENTS.md` (first-60-seconds list). Session source documents in `03_shadow/sessions/2026-04-23_devon/`.
- **Status**: active
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-23 — Stateless-handover neutrality clause (candidate)

- **Decision**: Add candidate addendum to the job-wrapup / escalation-note SOP: stateless handovers MUST separate facts from interpretation and MUST NOT prescribe action to the next agent. Required sections: Facts, Open-risks, Tokens, optional Analysis (clearly labelled, non-authoritative, skippable).
- **Why**: Architect flagged that the first baton pass of the session included forecasts and prescriptions, pre-biasing the next agent. Idea-meritocracy applied to handovers: no inherited opinions dressed as facts.
- **Where encoded**: `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` v1 (candidate), `00_authority/MANIFEST.md` v34 § Candidate authority, referenced by `00_authority/OPINION_CONFIDENCE.md`. First handover written under the clause: `03_shadow/job-wrapups/2026-04-23_amplified-partners-orchestration-session_wrapup.md`.
- **Status**: candidate (pending architect decision on promotion to **Authoritative now**)
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-23 — Stay with Qdrant as the vector layer

- **Decision**: No change to the vector database. The Qdrant incumbent stays. Migration to pgvector remains available if pain surfaces.
- **Why**: AI-facilitated customer deployments (not human-operator-facing) flatten the pgvector-vs-Qdrant ops-simplicity delta. Baking pipeline is already targeting Qdrant. Corpus scale (~12.5M tokens, ~2.5–7.5% of pgvector's HNSW comfortable ceiling) doesn't activate Qdrant's scaling advantage but also doesn't make Qdrant wrong. Agent-confidence split 65% stay / 35% migrate — **both below the 85% Medium threshold**. Under `OPINION_CONFIDENCE.md` § "When confidence is below the floor" the agent ran bounded research (Perplexity, one query), did not close the gap, and surfaced both options to the architect in-session with residual uncertainty named. Architect confirmed the reading. Only then was the decision recorded here.
- **Where encoded**: `03_shadow/job-wrapups/2026-04-23_amplified-partners-orchestration-session_wrapup.md` §2.6, `03_shadow/sessions/2026-04-23_devon/README.md`.
- **Status**: active (not contractual — revisit if Baking pipeline reveals Qdrant-specific friction, or if taxonomy/retrieval requirements shift)
- **Signed-by**: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### 2026-04-17 — Agent-primary audience (absolute)

- **Decision:** Authoritative text is **agent-only**. **Forbidden:** parallel
  human-oriented summaries, duplicate “for humans” entry paths, motivational gloss
  that does not change agent routing/constraints/acceptance. Operator behaviour
  blocks are **upstream routing operands** for agents, not documentation the
  operator is expected to consume routinely. Rare human audit uses **ISO-dated
  filenames**, descriptive slugs, folder roles, and **manifest** — no second doc
  layer for findability.
- **Where encoded:** `00_authority/NORTH_STAR.md` v11, root `AGENTS.md`,
  `00_authority/PRINCIPLES.md` v2, `00_authority/PROJECT_INTENT.md` v6,
  `00_authority/README.md` v7; `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md` v9;
  `00_authority/MANIFEST.md` v33.
- **Status:** active

### 2026-04-17 — Canonical agent entry + foundations/constraints/permissions

- **Decision**: Root **`AGENTS.md`** § **Agent session (clean-build) — first 60
  seconds** is the **single canonical entry** for agent read order, autonomy
  bounds, and mistakes-as-signal. `MANIFEST.md` gains an explicit **Permissions**
  section (GitHub org repo creation = human operator; `.cursor/` policy/hook
  changes vs mechanical edits). Human operator voice (questions vs diktats;
  diktats live in committed rules) encoded in `PROJECT_INTENT.md` and `AGENTS.md`
  **Outcome**. `90_archive` clarified as **reference / provenance** (audit
  snapshots not rewritten as “updates”).
- **Why**: Reduces duplicate entry-point drift; makes production safety explicit
  (permissions) while preserving bounded autonomy for partners.
- **Where encoded**: `AGENTS.md`, `README.md`, `00_authority/README.md`,
  `NORTH_STAR.md` (v10), `MANIFEST.md` (v31), `PROJECT_INTENT.md` (v5),
  `PARTNER_TRANSFER_INSTRUCTIONS.md` (v8), `90_archive/README.md`,
  `01_truth/README.md`.
- **Status**: active

### 2026-04-17 — Clean-build file budget (agent clarity default)

- **Decision**: Encode Ewan’s bar as policy text: every path in the clean-build
  workspace must **earn its place** by sharpening agent **routing / constraints /
  acceptance**, by **minimal infrastructure** (README routers, `.cursor/` policy
  surfaces), or by living only under **`03_shadow/`** or **`90_archive/`** with
  correct non-authoritative posture. Bulk `90_archive/inbox/` reads are **not**
  default agent work unless explicitly routed.
- **Why**: Prevents silent bloat and keeps the tree honest for stateless agents.
- **Where encoded**: `00_authority/NORTH_STAR.md` (v9), `01_truth/README.md`,
  `90_archive/README.md`, root `README.md`, `02_build/README.md`, `03_shadow/README.md`,
  `00_authority/MANIFEST.md` (v30).
- **Status**: active

### 2026-04-17 — No Cursor hooks in production (**TESTING NEED** for reinstatement)

- **Decision**: Keep `.cursor/hooks.json` as **`"hooks": {}`** (no registered hooks).
  Document **TESTING NEED** gate in `.cursor/HOOKS_TESTING_NEED.md` before any future
  hook experiment. Handover discipline remains **rule + SOP only**.
- **Why**: Operator request — no hooks; clear separation between production posture
  and any later evaluation of Cursor hook APIs.
- **Where encoded**: `.cursor/hooks.json`, `.cursor/HOOKS_TESTING_NEED.md`,
  `00_authority/MANIFEST.md` (v28), `03_shadow/job-wrapups/README.md`.
- **Status**: active

### 2026-04-16 — Canonical stateless handover checklist (SOP + Cursor)

- **Decision**: Treat the **Stateless handover (mandatory)** prompt set (where,
  name, template, minimum prompts including repulsion + bands + cut/stop,
  artifacts, tokens, smallest next step, decision-log pointer, leverage 0–9
  with **10 reserved** vs repulsion 1–10) as the single canonical checklist across
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (v13),
  `.cursor/rules/stateless-handover-kaizen.mdc`, and `.cursor/hooks/stateless-handover-stop.py`.
- **Why**: One checklist reduces drift between enforcement surfaces and the
  runnable wrap-up spec.
- **Status**: active

### 2026-04-16 — Deliberate slack (agents under the practical limit)

- **Decision**: Treat **production throughput and improvement throughput as
  co-primary** by defaulting to **deliberate slack** (operate meaningfully below
  the practical cognitive/latency ceiling) so wrap-ups, repulsion signals, and
  small process fixes are not squeezed out.
- **Why**: Compounding quality and system improvement beat optimizing for
  marginal speed at the edge, which tends to increase error rate and hides
  process debt.
- **Where encoded**: `00_authority/PRINCIPLES.md` (anchor lineage ≥34; see § Provenance and versioning), `00_authority/NORTH_STAR.md` (v8),
  `AGENTS.md`.
- **Status**: active

### 2026-04-16 — Clean room location and spine

- **Decision**: Create a project-specific clean room under `Amplified Partners/30_WORKING/Amplified-Partners_CleanRoom_Build/`.
- **Why**: Reduce context dilution and speed delivery by constraining scope.
- **Constraints**: No secrets in tracked content; personal data minimised and sanitised.
- **Status**: active

### 2026-04-16 — Approved incompleteness token

- **Decision**: Use the placeholder token `[LOGIC TO BE CONFIRMED]` for any incomplete logic.
- **Why**: Prevent assistants from guessing missing logic (“completeness paradox”).
- **Status**: active

### 2026-04-16 — Research-on-research bootstrap (start Research lane)

- **Decision**: Begin the Research department lane by applying the methodology prospecting + scoring rubric to the Research lane itself, using remit `REM-2026-04-16-ROR-001` (`01_truth/processes/2026-04_research-on-research_bootstrap-remit_v1.md`).
- **Why**: Research will be high-volume early and recurring after testing; the lane should self-improve without bloating authority.
- **Status**: active

### 2026-04-16 — Anti-thrash rule wording (two attempts, not two goals)

- **Decision**: Treat the hard stop as **two attempts** (two goes) per
  `00_authority/NORTH_STAR.md`; “two goals” was a transcription error.
- **Why**: Limits thrash on coherent tries at the problem, not on counting
  separate objectives.
- **Status**: active

### 2026-04-16 — Quick evidence token + SOP (researched ≠ promoted)

- **Decision**: Adopt literal token **`[CURRENT BEST EVIDENCE]`** for external
  lookup results at time of search; index candidate SOP
  `01_truth/processes/2026-04_quick-evidence-search_sop_v1.md` (declare
  parameters; return ≤3 assessed bits; no firehose).
- **Why**: Agents can proceed on small chunks with clear epistemic status;
  merit of ideas over any single voice; promotion remains separate.
- **Status**: active

### 2026-04-16 — Job wrap-up + escalation note (confidence-gated)

- **Decision**: Every job ends with a short wrap-up for learning (not
  criticism). If, after quick evidence search, confidence is still below the
  threshold needed to proceed (roughly \(0.85–0.9\)), stop and write an
  escalation note that preserves where the job is at and the smallest next
  action.
- **Why**: Prevent thrash, enable handoffs without context re-derivation, and
  capture solved problems as reusable “gold”.
- **Status**: active

### 2026-04-16 — Solve it twice → systemize it

- **Decision**: If a problem recurs (or is likely to), encode the fix into the
  smallest artifact that prevents recurrence (process/schema/interface/gate),
  rather than relying on memory.
- **Why**: Captures “gold” as durable leverage and reduces repeated thrash.
- **Status**: active

### 2026-04-16 — Wrap-up score calibration (10 reserved)

- **Decision**: Treat wrap-up scores as **0–9 calibration signals**; **10 is
  intentionally out of reach**; high scores must still name the next smallest
  improvement (see `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`).
- **Why**: Prevents “perfection scoring” from becoming a demotivator; keeps the
  loop oriented to continuous improvement.
- **Status**: active

### 2026-04-16 — Stateless Kaizen handover (wrap-up as mandatory packet)

- **Decision**: Treat job wrap-ups as mandatory **next-agent handover packets**
  (not optional narrative), because agents are stateless across sessions; if the
  next runner cannot resume without re-deriving context, the write-up failed.
- **Why**: Makes per-run calibration (scores + learnings) compound instead of
  evaporating between sessions.
- **Status**: active

### 2026-04-16 — Wrap-up exceptions + Cursor enforcement (consistency)

- **Decision**: If a wrap-up cannot be completed, write
  `YYYY-MM-DD_<short-job>_wrapup-exception.md` capturing blocker + smallest process
  refinement; add Cursor enforcement via `.cursor/rules/stateless-handover-kaizen.mdc`
  (always apply) plus a `stop` hook reminder in `.cursor/hooks.json`.
- **Why**: Consistency needs both **policy** (rule) and **nudges** (hook), with an
  explicit non-blame path when reality blocks completion.
- **Status**: active

### 2026-04-16 — Slime-mold Kaizen (explicit negative feedback + cut reporting)

- **Decision**: Require explicit **negative signals** (dead ends, anti-patterns)
  and a clear **cut / absolute stop** report when a lane ends due to stop rules
  (e.g. quick evidence search insufficient, confidence threshold, two attempts).
- **Why**: Attraction-only learning is slower; repulsion signals prune bad
  process branches quickly without moralizing people/agents.
- **Status**: active

### 2026-04-16 — Repulsion score (1–10) bands for process-noise

- **Decision**: Add a **repulsion score (1–10)** axis separate from the
  **leverage score (0–9)**; use banded routing: 1–3 often minimal noise unless
  repetitive; 4–5 local self-refinement; 6–7 pause + quick evidence search; 8–10
  redesign/remit territory.
- **Why**: Negative feedback needs magnitude so agents can distinguish everyday
  friction from systemic process failure without drowning in logs.
- **Status**: active

### 2026-04-16 — Manifest v24: remit filename + partner instructions indexing

- **Decision**: Treat **`00_authority/REMIT_PARTNER_CURSOR.md`** as the canonical remit path; keep **`00_authority/REMlT_PARTNER_CURSOR.md`** only as a redirect stub. Index **`AGENTS.md`** (repo root) and **`00_authority/AGENTS.md`** under **Authoritative now** in `00_authority/MANIFEST.md` (manifest **v24**).
- **Why**: Removes path ambiguity and aligns the authority index with what Cursor and docs already treat as in-force partner instructions.
- **Where encoded**: `00_authority/MANIFEST.md` (v24 changelog), `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`, `03_shadow/job-wrapups/2026-04-16_debug-authority-congruence_wrapup.md`.
- **Status**: active

### 2026-04-16 — Intent filter baseline for autonomy + self-Kaizen

- **Decision**: Reframe `00_authority/PROJECT_INTENT.md` as an explicit
  autonomy-first execution contract: maximize agent autonomy inside clear
  checks/balances, enforce stop/escalation discipline, and encode slime-mold
  feedback loops (positive + negative) as the default self-improvement engine.
- **Why**: Converts spoken intent into deterministic operating guidance and
  reduces ambiguity about what agents should do, when, and under what
  constraints.
- **Where encoded**: `00_authority/PROJECT_INTENT.md` (v3).
- **Status**: active

### 2026-04-16 — Partner execution contract (intent-confirm then complete)

- **Decision**: Adopt an explicit partner execution contract: confirm user intent
  in runnable terms first, then complete the requested work end-to-end unless
  explicitly paused. Prefer agent-native terminology and encode reusable
  methodology that transfers across scenarios.
- **Why**: Reduces ambiguity for agents, improves consistency across runs, and
  increases portability of process logic beyond one-off cases.
- **Where encoded**: `AGENTS.md`, `00_authority/PRINCIPLES.md` (anchor lineage ≥35; see § Provenance and versioning),
  `00_authority/NORTH_STAR.md`, `00_authority/MANIFEST.md` (v25 changelog).
- **Status**: active

### 2026-04-16 — Foundation hardening for sectional-build planning

- **Decision**: Treat the current workspace phase as foundation-first for a
  partially defined large project; prioritize behavior rules, authority clarity,
  and transfer-ready methodology before expanding `02_build/` delivery scope.
  Tighten manifest completeness to include active tooling surfaces and token
  alignment.
- **Why**: Keeps execution congruent with intent (build in sections later) while
  reducing ambiguity about what agents should do now.
- **Where encoded**: `00_authority/MANIFEST.md` (v26), `00_authority/PROJECT_INTENT.md`,
  `README.md`, `00_authority/README.md`, `02_build/README.md`.
- **Status**: active

### 2026-04-16 — Stop hook reminder vs wrap-up file duty

- **Decision**: Treat the Cursor **`stop` hook** as a **reminder** that may fire
  on every `stop` event; treat creation of `03_shadow/job-wrapups/*_wrapup.md` as
  **conditional** on the wrap-up SOP (finished, or paused / handed off / blocked).
  Do not require a new wrap-up file after every trivial or no-artifact turn unless
  there is an explicit session handoff.
- **Why**: Prevents agent over-compliance and file noise while preserving
  handover discipline for real job boundaries.
- **Where encoded**: `.cursor/hooks/stateless-handover-stop.py`,
  `.cursor/rules/stateless-handover-kaizen.mdc`,
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (v14),
  `AGENTS.md`, `03_shadow/job-wrapups/README.md`.
- **Status**: active

---

## Changelog

This section was added in v17 (the AMP-46 rebase commit, originally drafted as v16 — renumbered during merge with main when CODEOWNERS PR #49 took v16) to satisfy `AGENTS.md` rule #3 (authority files must record version bumps in a changelog). Earlier `version` bumps (v1 — v13) were made without a corresponding changelog entry; that history is preserved in git but not enumerated here. From v14 onward, every bump appends an entry below.

### v20 — 2026-05-05

Fixed signature-date contradiction in the v16 retroactive entry (Devin Review BUG-0001 on PR #46): the entry heads `v16 — 2026-05-05` and records the CODEOWNERS event from 2026-05-05, but the `Signed-by` line previously read `2026-05-04`. Per `00_authority/SIGNATURES.md`, signatures must use the correct ISO date; per `AGENTS.md` rule #6, the heading and signature must agree. Updated to `2026-05-05` (which also matches the merge commit `9087b55` on origin/main). No other entries touched.

Signed-by: Devon-a9a7 | 2026-05-05 | devin-a9a78d0c72d9491aa3a70b18cb741936

### v19 — 2026-05-04

Added the `2026-05-04 — LiteLLM secrets moved to \`.env\` + compose mirrored (AMP-72)` entry to `## Entries` (renumbered from a prior draft v18 during merge with main — main had advanced to v16 with the CODEOWNERS PR #49 between branch creation and merge). Decision is reversible (backups at `/opt/amplified/apps/litellm/docker-compose.yml.bak.20260504-amp72` + `.env.bak.20260504-amp72`). Linked to [AMP-72](https://linear.app/amplifiedpartners/issue/AMP-72/). Manifest pointer references `02_build/INFRASTRUCTURE.md` v5.

Signed-by: Devon-a9a7 | 2026-05-04 | devin-a9a78d0c72d9491aa3a70b18cb741936

### v18 — 2026-05-03

Added the `2026-05-03 — LiteLLM host-loopback port mapping + pudding-testing env-driven base URLs (AMP-71)` entry to `## Entries` (renumbered from v17 during merge with main). Decision is reversible. Linked to [AMP-71](https://linear.app/amplifiedpartners/issue/AMP-71/) and PR #38. Manifest pointer references `02_build/INFRASTRUCTURE.md` v4.

Signed-by: Devon-a9a7 | 2026-05-03 | devin-a9a78d0c72d9491aa3a70b18cb741936

### v17 — 2026-05-03

Added the `2026-05-03 — Ollama port-mapping fix on Beast (AMP-46)` entry to `## Entries` (renumbered from v16 during merge with main; main now holds v16 = CODEOWNERS PR #49). Decision is reversible. Linked to [AMP-46](https://linear.app/amplifiedpartners/issue/AMP-46/beast-ops-fix-ollama-container-port-mapping) and PR #32. Manifest pointer now references `02_build/INFRASTRUCTURE.md` v3.

Signed-by: Devon-a9a7 | 2026-05-03 | devin-a9a78d0c72d9491aa3a70b18cb741936

### v16 — 2026-05-05

Recorded retroactively. The `2026-05-05 — CODEOWNERS added to clean-build (governance enforcement via GitHub)` entry shipped on `main` via PR #49 with a frontmatter version bump to v16 but no changelog entry; preserved here so the audit trail stays complete. Linked to PR #49. Manifest pointer references `00_authority/MANIFEST.md` v51.

Signed-by: Devon-a9a7 | 2026-05-05 | devin-a9a78d0c72d9491aa3a70b18cb741936

### v15 — 2026-05-03

Added two entries to `## Entries`: `2026-05-03 — cost-tools (token_proxy.py) deployed on Beast and indexed in spine` and `2026-05-03 — Agent routing rule established (AGENT_ROUTING.md)`. Recorded retroactively in v17 (originally drafted as v16) because the v15 bump shipped on `main` (PR #39, AMP-28) without a changelog entry — preserved here so the audit trail is complete.

Signed-by: Devon-a9a7 | 2026-05-03 | devin-a9a78d0c72d9491aa3a70b18cb741936

### v14 — 2026-05-03

Added the `2026-05-03 — Public-data validation framework + ProfServices pilot (AMP-67)` entry to `## Entries`. Recorded retroactively in v17 (originally drafted as v16) because the v14 bump shipped on `main` (PR #35) without a changelog entry — preserved here so the audit trail starts at the first observed bump.

Signed-by: Devon-a9a7 | 2026-05-03 | devin-a9a78d0c72d9491aa3a70b18cb741936
