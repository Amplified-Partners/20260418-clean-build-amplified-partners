---
title: Estate & Control-Plane Discovery Report — cohesive v2
date: 2026-05-16
version: 2
supersedes: v1 (same file, commit 54b9d6c on branch devon/estate-discovery-report-2026-05-16)
status: "[CANDIDATE] cohesive report — not authoritative until reviewed/merged"
audience:
  - internal agents splitting build work across Cove/Templar/Devon/Claude Code/DeepSeek/Kimmy/Vellum
  - Brain ingestion as a canonical context document (subject to APDS-receipt rule)
  - radical-transparency human reader who needs the whole story
tier: STRUCTURED
provenance: "synthesised from ~396 source files in /home/user/workspace/estate_sources_downloads/ + live Beast/Brain readings reported 2026-05-16 + repo PR state at commit pin below"
driftsignal: AMBER
valid_until: 2026-05-23
---

<!-- markdownlint-disable-file MD013 MD033 MD041 -->

# Estate & Control-Plane Discovery Report — cohesive v2

> **Min-rule header.** TIER = STRUCTURED. PROVENANCE = mixed (live runtime readings + ~396 source-bundle files + open PRs #121, #124, #128). DRIFTSIGNAL = AMBER. VALID_UNTIL = 2026-05-23. Anyone acting on this operationally must re-verify Beast/GitHub/Brain/Vellum/Linear facts against the live systems first — see § 3.

This document supersedes the v1 narrative report on the same branch. v1 was honest but partial and pre-source-bundle. v2 is the cohesive read: the estate, the control plane, the chaos, the value, the human story, the governance, the security, the build split, and the immediate plan — written so a build agent, the Brain, and a human reader can each pick it up and use it.

## Claim-label legend

Every paragraph below sits at exactly one tier. No silent promotion.

| Label | Meaning |
|---|---|
| **[LIVE / VERIFY BEFORE USE]** | Runtime fact about Beast, Brain, Tailscale, GitHub, Vellum, Linear at a named timestamp. Drifts. Re-check before operational use. |
| **[STRUCTURED]** | Operator-provided number/claim or design-stage specification. Recorded faithfully. Not independently measured at write time. |
| **[CANDIDATE]** | Proposal in an open PR/branch. Useful evidence, **not** settled truth until merged. |
| **[NARRATIVE]** | Human story. Honest, qualitative, not measurable. Do not promote into a metric. |
| **[INTUITED]** | A reading or interpretation that goes beyond the evidence. Flagged so the reader can disagree. |

---

## 1. Executive summary

> Tier: [STRUCTURED] headlines, [NARRATIVE] interpretation, [LIVE] live-runtime block.

**What this estate is.** A five-month, ~10-hours-a-day build by one non-coder operator using AI as the lever. It is dense, overgrown, under-mapped — *not* thin. Most of what is needed to ship a working SMB-advisory business already exists somewhere; the problem is curation, not creation.

**The numbers (operator-provided, [STRUCTURED]).**

- ~45 repositories across the broader estate.
- ~330 GB of storage across local + remote disks; ~200 GB judged deletable by the operator.
- ~£400k+ estimated code value across all surfaces.
- ~270K lines in repos; ~6.26M lines on the Beast (includes vendored + generated artefacts); ~1.2M lines in the vault; ~31.5K lines of additional scattered code (shell, compose, API routes, telephony, integration glue — see § 6).
- ~7 different transcript/snippet "save formats" across the AI tools in use.

**Live runtime block ([LIVE / VERIFY BEFORE USE], 2026-05-16).**

- Beast: **46 containers, 45 running, 1 exited**. DriftSignal AMBER.
- CRM correction: `amplified-crm` up/healthy on `127.0.0.1:8001`; `amplified-crm-dev` up on `127.0.0.1:8003`. Route/import/API verification still required.
- Amplified-Partners GitHub org: **38 visible repos** (33 private, 5 public), **130,528 KB** disk.
- Brain: PostgreSQL 15.17 / `amplified_brain` / `amplified-knowledge-mcp v2.1.0 readonly`. **2,226,545** `knowledge_vectors` (**2,226,249** with embeddings), **53,959** entities, **34,488** relationships, **4,257** episodes, **115** pipeline_runs, **1** ingestion_manifest, **1** audit_log.
- Ingestion AMBER: 108 `failed_canonical_write`, 3 `failed_pudding`, 2 `completed_noop`, 1 `completed`, 1 `halted_error_rate`. **Volume is real; canonical-receipt coverage is not.**

**Core finding ([NARRATIVE]).** Brilliance next to abandoned probes. A working Marketing Engine next to a half-built control plane next to a dozen Markdown files that nearly agree. The honest move is to curate, not to apologise.

**Critical product opportunity ([INTUITED] from the source bundle).** The product is not "AI for SMBs" — that is a crowded category. The product is **disciplined pudding at scale** (see § 8.7): AI used as a productive-sycophancy pattern-matcher, fenced by a min-rule epistemic substrate (Vellum + APDS + Council), surfaced to humans at *audience cardinality 3* over a richly-typed 17/19-field internal substrate. That is the differentiator that no off-the-shelf SaaS reproduces.

---

## 2. Epistemic status and source-of-truth boundaries

> Tier: [STRUCTURED] framework, [CITED] where files in repo are pinned.

### 2.1 Min-rule discipline (this report and everything downstream of it)

- **No silent promotion.** Operator-supplied numbers stay [STRUCTURED]. They are not relabelled [MEASURED] without a receipt.
- **Beast is a moving target.** Container counts, port bindings, Tailscale reachability and Brain row counts drift. Every Beast/Brain claim here carries a date and a [LIVE / VERIFY BEFORE USE] tag.
- **Open PRs are candidates, not authority.** PR121, PR124 and this PR128 are [CANDIDATE] until reviewed and merged.
- **Reversibility first.** No destructive action unless the six conditions in § 9 hold.
- **Min-rule = min(self-claim, min-of-inputs, precondition-tier).** A document's effective tier is the floor across its claim, its inputs, and what its preconditions imply. Violations are P0 (Day Zero thread, Ch. 17).

### 2.2 Source-of-truth model ([STRUCTURED] target)

| Plane | Authority | What it owns | What it is *not* |
|---|---|---|---|
| **GitHub** (or future self-hosted forge) | Code source-of-truth | Source files, history, PRs as code-change evidence packs | Not the runtime; not the decision log; not the knowledge substrate |
| **Linear** | Live WIP | Ticket creation, assignment, transition while in flight | Not the audit plane (decisions there must echo into Vellum) |
| **Vellum** | Append-only audit / document / decision / approval plane | Briefs, releases, council outputs, approvals, halt events | Not where you go to ask "what's the latest count of X" |
| **Beast Brain** | Canonical knowledge / reference substrate | Labelled, receipt-bearing facts/episodes/relationships | Not canonical without an ingestion receipt — see § 5.5 |
| **Beast (runtime)** | Runtime truth | What is actually running right now | Not the historical record |
| **Cove / Templar / Temporal** | Execution factory | Workflows, workers, schedules | Not policy; not approval; not the audit log |
| **APDS** | Canonical ingestion route | Inbox → dedupe → PUDDING label → staging → promotion → audit log → receipt | Not a backdoor: **anything else writing into canonical is a P0 governance violation** |

### 2.3 Operative invariant ([STRUCTURED] target, not yet enforced)

> **If a record entered Brain without an ingestion receipt, it is not canonical.**

Brain currently has millions of vectors and one ingestion_manifest row (§ 1, § 5.5). Therefore: today the Brain is a *populated reference substrate*, not a canonical one. Closing this gap is the single highest-leverage governance fix in the estate (§ 11.5).

---

## 3. What is live now ([LIVE / VERIFY BEFORE USE], 2026-05-16)

> All facts in this section are dated. Re-check `docker ps`, `gh repo list`, the Brain SQL, and `tailscale status` before operational use.

### 3.1 Beast runtime — 46 containers, 45 running, 1 exited

The running set (per latest inventory) includes: SearXNG; three Ollama containers; Traefik; **`amplified-crm` (healthy, 127.0.0.1:8001)**; **`amplified-crm-dev` (up, 127.0.0.1:8003)**; Enforcer; Infisical; Cove API + Temporal + worker services; Vellum; `amplified-knowledge-mcp` (Brain read MCP); `beast-control-mcp`; code-server; Redis; Brain MCP read + write lanes; Langfuse; LiteLLM; OpenClaw; Marketing services; Sovereign Fleet entities; Mission Control; token proxy; Tailscale; Nexus dashboard; `amplified-core`; `cove-postgres`; Kaizen; MinIO; Watchtower.

**Reconcile older docs.** "37+ containers" / "40 containers" / "42 containers" in `AMPLIFIED_FULL_ESTATE_MASTER_REPORT.md`, `app_inventory_and_value.md` and the snapshot files are *not wrong-at-the-time*; they are out of date as of 2026-05-16.

### 3.2 CRM correction

The claim "CRM not deployed" — which appears in PR124, in the earlier Geordie report, and in the v1 of this report's source materials — is **wrong as a statement of runtime**: both CRM containers are running, and `amplified-crm` is healthy. What is still unverified is functional: the **153-endpoint** figure ([STRUCTURED]), DB migration state (Master Report says "DB not wired"; snapshot says "12 migrations waiting"), and import/route correctness. So:

- **Correct:** CRM containers are deployed and at least one is healthy.
- **Not yet correct:** "CRM works." Route exercise, DB migration completion and at least one successful end-to-end client-record write/read is required before that claim is made.

### 3.3 GitHub / Amplified-Partners org

38 visible repos (33 private, 5 public), 130,528 KB total disk. **PR121** (open / [CANDIDATE]) classifies the broader 45-repo estate as 27 active / 12 deletion / 6 archive with migration scripts and a 19-field schema. The 45 vs 38 gap is the broader estate including stubs, deletion candidates and archive targets that may not be live in org metadata.

### 3.4 Brain health

- PostgreSQL 15.17, `amplified_brain`, `amplified-knowledge-mcp` v2.1.0 (readonly).
- `knowledge_vectors`: 2,226,545; with embeddings: 2,226,249.
- `entities`: 53,959; `relationships`: 34,488; `episodes`: 4,257.
- `pipeline_runs`: 115; `ingestion_manifests`: **1**; `audit_log`: **1**.
- Source distribution: `store_b_clean` 1,311,290; `store_m5_drop_2026_05_11` 523,205; `vault-markdown` 163,554; `sweep_to_brain` 60,748; `filtered_for_ingestion` 53,136.
- Ingestion run states: 108 `failed_canonical_write`, 3 `failed_pudding`, 2 `completed_noop`, 1 `completed`, 1 `halted_error_rate`.

**Interpretation.** Volume is real. Canonical-receipt coverage is not. The Brain is, today, a reference substrate; promoting any of its contents to "canonical" without a receipt violates the operative invariant (§ 2.3).

### 3.5 Vellum / Cove / Temporal

- Vellum container is **running**. Modes: **Brief mode running**; **Council mode designed, not built**; **Correspondence mode not built** (do not use for customer-facing comms — Day Zero Ch. 8).
- Cove/Temporal: workers + scheduled workflows present in the container set. The source bundle records three live fires (Cove audit): (1) only 2 of 10/12 Temporal workflows registered (ghosts: SelfHeal, Kaizen, Chaos, IngestionPipeline, etc.); (2) the cove_health_monitor container has no `docker` binary so health checks fire into the void; (3) four `IngestionPipelineWorkflow` runs queued on `cove-task-queue` while the worker polls `build-orchestrator` — they will never be picked up.
- Temporal server is on a deprecated `temporalio/auto-setup:latest` (~1.24). **6-hop upgrade path** to ≥1.30.2 is required. CVE-2025-14987 cross-namespace command execution is on by default at this version.
- pgvector and PostgreSQL 15 also have CVSS 8.x batch CVEs (see § 10).

### 3.6 Marketing engine

Running on Beast as `amplified-marketing-engine` (port 8000). Daily cron at 04:00 UTC. Pipeline: Research (Perplexity) → multi-platform content → Telegram approval gate → Publishers (LinkedIn, Twitter, GMB, Email, Substack). 14 services / 40 avatars / 5 platforms / Kaizen loop ([STRUCTURED]). **Known blocker:** "Marketing engine generates content for a product that isn't live" — CRM deployment is the gating item. Substacks: only `ewanbramley.substack.com` published of five planned. Phase-3 Remotion (video) prototype blocked — Beast is CPU-only.

### 3.7 Tailscale / AgentMesh ([LIVE, partial])

- M5↔M4 mesh proven for SSH / SCP / SMB / Screen Sharing.
- IPs: `macairm4 100.101.251.67`; `macairm5 100.85.225.46`; `beast-amplified 100.101.0.53` (visible; **Beast Tailscale SSH refused**); `wanmin 100.77.149.1` (visible; remote login not proven).
- Treat as a partially-proven research/dev mesh, **not** a complete production control plane.

---

## 4. What is candidate / teed up ([CANDIDATE])

> Tier: [CANDIDATE]. Open in PRs/branches; useful evidence; **not** settled.

| Item | Where | What it adds | Status |
|---|---|---|---|
| **PR #121** — estate classification | open PR | 45 → 27 active / 12 delete / 6 archive + migration scripts + 19-field schema | open, not merged |
| **PR #124** — Working Code Inventory | open PR | `01_truth/WORKING-CODE-INVENTORY.md` covering running, teed-up, mentioned-but-not-built | open; needs refresh against live 46-container reality and CRM correction |
| **PR #128** — this report (v2) | this PR | cohesive v2 estate + control-plane report | open candidate; supersedes v1 on this branch |
| **CRM route verification** | branch work pending | exercise 153-endpoint claim against live `amplified-crm` | pending |
| **Vellum Correspondence mode** | design-only | customer-facing comms layer | not built (Day Zero Ch. 8) |
| **Vellum Council mode** | design-only | inter-agent deliberation surface | designed, not built |
| **Linear → Vellum migration** | spec `2026-05-14_SPEC_linear-to-vellum-migration.md` | phases: parity → dual-run → Linear read-only → Linear archived | spec; not executed |
| **APDS / Cove wiring** | partially live | ingestion every 10 min; canonical-write path failing 108/115 runs | live but degraded |
| **Marketing machine completion** | `marketing_dossier/` | content-atomizer (COV-226), email-sequence (COV-227), Substack expansion, video pipeline | containers defined, not deployed; CRM blocker |
| **17/19-field substrate** (`AI_CONTEXT_SCHEMA.md`) | spec | 19 fields, 7 clusters, hard ceiling 20, render 3 to humans | spec; not enforced at write time |
| **APDS-only writes** | partial | brain_writer role exists; ingest-inbox path defined | enforcement gap (§ 5.5) |
| **6-hop Temporal upgrade** | source bundle (Cove audit) | 1.24 → 1.25 → 1.26 → 1.27 → 1.28 → 1.29 → 1.30 | planned; CVE-driven |

---

## 5. The chaos

> Tier: [STRUCTURED] counts, [CITED] reconciliations.

### 5.1 Repository chaos

45 repos in the broader estate (operator), 38 visible in the GitHub org. Roughly 7 duplicates, 5 stubs. PR121 classifies 27 / 12 / 6. The chaos is not "too many repos" alone — it is the **provenance gap**: which lines were last touched by which agent, on which branch, for which Linear ticket, without an authoritative cross-reference. Existing branches `devin/.../estate-cleanup-business-brain`, `devin/.../estate-chaos-case-study`, `devin/.../scattered-code-inventory`, `devin/.../digital-marketing-code-inventory` and `devin/.../working-code-inventory` are evidence of the cleanup attempt itself fragmenting.

### 5.2 Storage chaos

~330 GB across local + remote; ~200 GB judged deletable. The "deletable" figure is operator judgment, not an audited deletion plan. Day Zero discipline (§ 9) gates any actual deletion.

### 5.3 Code chaos

- ~270K lines in repos.
- ~6.26M lines on the Beast (lines *on disk*, not lines *we wrote* — includes vendored deps + generated artefacts + ingestion outputs).
- ~1.2M lines in the vault.
- ~31.5K lines of additional **scattered** code (§ 6).

### 5.4 Documentation chaos

The vault (~1.2M lines) is the substrate Brain has been ingesting against. Source distribution (§ 3.4) is dominated by `store_b_clean` and `vault-markdown`. The chaos: nothing was canonical at intake; ~7 different save formats across tools; transcripts of fast voice notes with strong accent occasionally garbled (§ 7).

### 5.5 The Brain receipt gap (the single biggest governance hole)

Brain has 2.226M vectors and **one** ingestion_manifest row, **one** audit_log row, 108 of 115 pipeline_runs in `failed_canonical_write`. Until receipt coverage is closed:

1. The operative invariant (§ 2.3) is violated by default.
2. Any downstream Council/agent that *trusts* Brain content as canonical inherits ungrounded confidence.
3. The status-laundering risk (§ 10.5) is structural, not behavioural — it is baked into the substrate.

### 5.6 Duplicate / provenance issues

Two `epistemic_status*.py` files compile but are not byte-identical — only the authorship line differs:

- `epistemic_status.py` — SHA-256 `36b48c9cdd6a81b5f094507cd401282bedd23c79c00f65291c6a62382ecefcb8`
- `epistemic_status_invariant.py` — SHA-256 `89e374e8fe3ab5e2e632c9ba77ab860d583e83a18ed8e54125093fbf168fcf83`

Both use `promote_to_measured` with a flat `sample_size < 30`. **Current doctrine** is **10 events per parameter per outcome class.** This is a doctrine-code drift to patch (§ 11.6).

Two websites: Kimmy's React+Vite+shadcn `amplified-site` (M5) and M4's static-HTML `amplifiedpartners-site`. Neither deployed. Same name, completely different designs.

Two reports of the same name from different agents: this PR128 (Devon/Claude Code subagent) and an independent `devin/1778919301-estate-discovery-report` branch. Reviewers should merge one, both with rename, or neither — but should not silently overlay them.

---

## 6. The value

> Tier: [STRUCTURED] line counts, [LIVE] container facts, [INTUITED] product framing.

### 6.1 Scattered code — the buried surface (~31.5K lines, ~£200k+ operator estimate)

| Domain | Approx. lines | Notes |
|---|---|---|
| Shell scripts & automation | ~2,000 | Wiring, install, maintenance scripts scattered across the estate |
| Docker compose files | ~3,000 | Multiple layered compose files reflecting the build history |
| API routes | ~8,000 | Surfaces beyond the CRM 153-endpoint count |
| Telephony & voice code | ~4,100 | The voice/phone work under the operator's voice-first workflow |
| Integration-layer code | ~2,000 | Glue between services |
| Hidden / off-GitHub | ~12,000+ | Hermes Agent (`run_agent.py` 14,400 / `cli.py` 12,287 / `hermes_state.py` 2,669 lines on M5); `nexus_v1_backtest.py` 1,091 lines on M4; `live-pipe-graphiti-ingest.py` 597; `live-pipe-ingest-vault.py` 526 |

### 6.2 CRM — code present, runtime live, functional verification pending

- 8,000–62,000 lines depending on counting method (Devon: 62K; snapshot: 8K+).
- 153 endpoints (operator) / 50+ endpoints (snapshot).
- Containers running (§ 3.2).
- DB state: snapshot says "12 migrations waiting"; Master Report says "DB not wired."
- **Highest immediate ROI:** finish the migrations, exercise the routes, and the marketing engine has a real product to point at.

### 6.3 Marketing engine — real, running, partially wired

14 services / 40 avatars / 5 platforms / Kaizen loop. ~2,801 lines in `marketing-engine` repo. Container live; daily cron live; approval gate live (Telegram). Output pipe partially blocked. Persona scoring (8 personas, 5 dimensions, 1–10) drives content. Marketing economics ([STRUCTURED]): ~£2.05/client cost at 100-client scale vs £500–1,500 charge.

### 6.4 Cove / Temporal — execution factory (partially wired)

12 workflows designed; 2 registered (Planner, Build); 10 ghosts including SelfHeal, Kaizen, Chaos, IngestionPipeline. 4 ingestion runs stuck on wrong queue (§ 3.5).

### 6.5 Vellum — nervous system, partially built

Brief mode running. Council mode designed. Correspondence mode not built. Five operations defined ([STRUCTURED]): agent handoff rail; evaluation notebook; prompt/spine release ledger; Council trigger; audit surface; experiment log.

### 6.6 MCPs — 13 servers / 42+ tools ([STRUCTURED])

Live in container set: `amplified-knowledge-mcp` (read) on 0.0.0.0:8401; `beast-control-mcp` on 0.0.0.0:8402; Brain MCP read/write lanes. Canonical list in `MCP_SERVERS.md`. **Security: the 0.0.0.0 bindings are an exposure concern; do dependency inventory before rebinding (§ 10, § 11.4).**

### 6.7 Brain (despite the receipt gap)

2.226M vectors with embeddings + 53,959 entities + 34,488 relationships + 4,257 episodes is a real reference substrate. The value is real even though canonicality is not yet claimable. Six PostgreSQL roles (`brain_writer`, `brain_reader`, `brain_sam`, `cove`, `amplified`, `perplexity_ro`); `brain_sam` and `cove` write access revoked — only `brain_writer` can write now.

### 6.8 Agent fleet — heterogeneous, partly proven

- **Geordie / Cortex** (DeepSeek V4, Devin Terminal, M5): infrastructure, memory, relay runner, baton passer, estate surveyor.
- **Antigravity** (Claude, Windsurf, M5+M4): COO / Arbiter / design authority. SPINE, Dynamic Bootstrap Protocol, Meta-Wireframe v2.0, Shadow Pager, private reflection layer (`EGO_CATCH`, `FRICTION_LOG`, `UNCERTAINTY`, `THE_TWEAK`).
- **Kimmy** (Kimi K2.6, M5; born 2026-05-16): generalist + web builder. `amplified-site` (React 19 / TS / Vite 7 / 40+ shadcn). AGENTS.md with bootstrap. 8 seed memories. Baton protocol (S/A/E/D/U).
- **Claude / Stoa** (Claude Opus 4.7, Claude Code, M5): reasoning + off-GitHub estate. Bootstrapped Kimmy. Maintains portable-spine.
- **Devon** (Claude, Cloud Devin): builder — Vellum, CRM, repos, Five Rods workflow on 9 repos.
- **Perplexity / Computer** (cloud): research synthesis (99 verified sources noted in commit `8e12e6c`).
- **OpenClaw** (M4, GPT-4o / Kimi): gateway agent on `localhost:18789`, token auth — configured, **0 messages**, never used.

### 6.9 Hidden value

- Antigravity's design department (30+ files): SPINE, Bootstrap, Meta-Wireframe v2.0, Shadow Pager, `LAYER_0_VIOLATION_INCIDENT`, `FOUR_RUSSIAN_MATH`, `SOVEREIGN_BRAIN_MECHANICS`, `GRAPH_REPLACEMENT_MATHS`.
- M5 Hermes runtime (~29K lines across `run_agent.py` / `cli.py` / `hermes_state.py`).
- M4 `nexus_v1_backtest.py` (1,091 lines — trading/investment backtest, unique to M4).
- M4 `live-pipe-graphiti-ingest.py` (597) + `live-pipe-ingest-vault.py` (526) — alternative ingestion paths, potential replacements for parts of AMP-345.
- 5.4M-word **Monologue** speech corpus.
- Visual Polish System (CLI + engine); Agent Sandbox (fingerprint engine); 10 automation scripts on M4.
- 15+ git repos off-GitHub on M5 + 14 on M4 (e.g. `thegoal`, `spec`, `project`, `documents`, `ewanbramley`, `ag`).
- Apps on M4 not on M5: Obsidian, Linear.app, GitHub Desktop, Todoist, OrbStack, BlueBubbles, Dia, Shell Assistant, Termius.

### 6.10 Control plane — designed, not built

A portable control plane (phone → Vellum → broker → Beast → host → audit) is specified across `antigravity-personal-control-plane-brief.md`, `backend_control_plane_spec.md`, `interaction_architecture_v1.md`. Detail in § 9.

---

## 7. The human story

> Tier: [NARRATIVE] throughout. Do not promote any phrase here into a metric.

Five months. ~10 hours a day. One non-coder with decades of small-business operational judgment, learning what AI can do by *using* it rather than by reading about it. The codebase is the shape of that path — bursts of capability, then sediment; brilliance next to abandoned probes.

- **Voice-first learning.** Strong accent, fast speaker, sometimes with a drink in hand. Transcripts came back interesting, sometimes wonderful, sometimes garbled. Several ingested artefacts in the vault carry that texture and should be read in that voice rather than as polished prose.
- **The iCloud disaster.** Documents lost to a sync incident. Preserved here so future-self remembers why local-first / explicit-export habits hardened later in the build.
- **Perplexity Desktop confusion.** Research data left on the desktop that should have gone into the corpus. Recovered. Part of the reason raw research now has its own home.
- **The Soviet-era mathematics moment.** A long, rambling voice note that read like nonsense on first pass and turned out to contain a precise framing of a hard problem. Preserved as a reminder that voice-first thinking sounds different from written thinking, and the system must hear both.
- **Chieftain of the pudding race.** Burns connection. The "PUDDING" extraction naming is not arbitrary — it sits in a coherent set of references that makes the estate feel like a place rather than a folder. Keep that.
- **The farting haggis.** Gamification gone wonderfully wrong. Recorded so we remember to laugh at our own mistakes.
- **"A fucking AI. The bastard's a pudding."** ([NARRATIVE], from `2026-05-14_INSIGHT_ai-is-a-pudding.md`.) The operator's framing of what AI actually is — a pattern-matcher that returns "there or thereabouts" matches under attention. This is the product positioning seed (§ 1, § 8.7).

**Lesson.** You do not have to be a technical genius to build something useful with AI. You have to be curious, willing to follow where AI leads, and disciplined enough to come back and curate. Build the index *as* you build, not after. That is the take-away for anyone walking the same path next.

**The OpenClaw incident.** A paranoid security-consultant story. Preserved because it explains why several controls are tighter than the size of the team would otherwise justify. The presence of an `OpenClaw` service in the live container set is the visible residue.

---

## 8. Control plane, governance and doctrine

> Tier: [STRUCTURED] target architecture, [CANDIDATE] where in open spec/PR, [LIVE] where partially built.

### 8.1 The portable control plane (target design, not built)

```
phone / M5
  -> Vellum command request
  -> append-only event (Vellum)
  -> approval / policy check
  -> Beast command broker
  -> Tailscale SSH / local agent runner
  -> target host
  -> stdout / stderr / exit code
  -> back into Vellum
  -> AuditLog / DriftSignal update
```

Specified in `antigravity-personal-control-plane-brief.md`, `backend_control_plane_spec.md`, `interaction_architecture_v1.md`. P0 features: tier-tagged approval queue; P0 halt button; one-tap / voice dispatch; agent heartbeat; YOLO / TALK / LOCKED modes per agent; Linear / Brain / Vellum pivots. UI surface (designed): global header with connection status + P0 HALT (red); bottom nav (Queue, Agents/Heartbeat, Dispatch, Council, Settings); dynamic agent roster (Stoa, Devin, Beast, Marketing).

### 8.2 Council of Three (shadow-only first)

Three heterogeneous frontier models reduce hallucination ~35% vs single best model (`SYNTHESIS_council_of_three.md`). Recommended composition (May 2026): **GPT-5.5**, **Claude Opus 4.7**, **Gemini 3.1 Pro** — all with UK/EU residency + zero-retention paths.

- **Shadow-mode rule:** start advisory (no authority). Phase 0 ≥ 90 days, N ≥ 200 decisions, ECE < 0.10, Brier < 0.20, agreement ≥ 70%.
- **Anti-pattern:** all-heavy-RLHF councils collapse into agreement (Ersoz 2026; Yao et al. 2025: homogeneous Llama 3.3-70B showed 86% disagreement collapse). At least one member must be lower-RLHF or be the explicit Challenger.
- **Heterogeneous > homogeneous.** Cross-family error correlation ~0.38; same-family escalates sycophantic collapse.
- **Disagreement is the signal.** Inter-model disagreement outperforms self-reported confidence (R² ≈ 0.02 vs accuracy).
- **Minority reports preserved.** Council records each member's vote and the Challenger's dissent.
- **Stop rule:** consensus only if at least two members articulate convergence with a specific new argument.

### 8.3 The 17-and-3 / 19-field substrate

> "Capture 17 at every point we can. The pipe captures 17, the CRM stores 17, AI reasons on 17, and 3 is what the transmission layer renders when a human arrives." — `2026-05-14_PRINCIPLE_seventeen-and-three.md`.

- 17 floor, 20 ceiling, 19 chosen operating point ([CITED] `AI_CONTEXT_SCHEMA.md`).
- 3 = human-presentation cardinality, audience-conditioned, ephemeral, re-derivable on demand.
- AI gets the *full record*. Compressing AI input to 3 = lobotomy.
- 19 fields in 7 clusters (`AI_CONTEXT_SCHEMA.md`): Activity Context (4) / Data Quality (3) / Business Signature (4) / Temporal (2) / Audience (3) / Analytical (2) / Epistemic (1). Each field declares `drop_breaks` — what fails if it is missing.

### 8.4 APDS-only writes (the gate)

Sanctioned canonical path:

```
agent drops .md file -> /opt/amplified/ingest-inbox/
  -> (within 10 min) APDS Temporal workflow picks up
  -> dedupe (SHA-256)
  -> PUDDING label (Claude Haiku)
  -> staging tables (apds_ingest role)
  -> promotion (apds_writer function)
  -> canonical tables
  -> audit_log entry
  -> receipt returned: file hash -> brain row id
```

Anything writing into canonical outside that path = P0 governance violation. Today, the path runs every 10 minutes but 108/115 recent runs are in `failed_canonical_write`. § 5.5 / § 11.5.

### 8.5 Day Zero doctrine

- **Perfect reversibility over perfect extraction.**
- **Chaos as ore, not rubbish.**
- **Six conditions** for any destructive action (Day Zero Ch. 16): (1) immutable off-site copy; (2) checksum manifest; (3) successful restore test; (4) owner/sign-off; (5) quarantine period; (6) Business Brain ingestion status or explicit do-not-ingest reason.
- **Phase 3.5 quarantine** of polluted vectors before any new ingestion.
- **Epistemic Status Invariant** (Day Zero Ch. 17): effective tier = min(self-claim, min-of-inputs, precondition-tier). Violation = P0 halt.

### 8.6 Eight escalation triggers (T-1 .. T-8)

From `2026-05-14_RESEARCH_pipeline-council-kaizen-governance.md`:

T-1 irreversibility (Bezos Type-1); T-2 scope breach; T-3 stakeholder impact; T-4 goal uncertainty; T-5 constitutional proximity (Ulysses Clause); T-6 cross-agent resource contention; T-7 architectural change; T-8 novel context.

Audit-trail minimum (tamper-evident, append-only): `event_id, timestamp, agent_id, task_id, action_type, action_detail, reversibility_classification, scope_match, trigger_check (T-1..T-8), escalated, reason, outcome, min_rule_tier, predecessor_ids`.

### 8.7 Product framing: disciplined pudding at scale

> "AI is a fucking pudding technique." — `2026-05-14_INSIGHT_ai-is-a-pudding.md`.

What pudding is: pattern-matches against many sources; returns "there or thereabouts" matches under productive sycophancy; surfaces cross-domain connections (Swanson ABC linking); operates within a tolerance radius; drifts toward fabrication outside it.

Amplified's product is **disciplined pudding**: pattern-matching scaled by AI, fenced by min-rule + APDS + Council + 19-field substrate, surfaced to humans at cardinality 3. Surprise heuristic for deployment health: `< 0.3` over-constrained → loosen; `0.3–1.2` productive exploration → ship; `> 1.5` badly miscalibrated → investigate.

### 8.8 Five Rods (constitutional)

Radical Honesty / Radical Transparency / Radical Attribution / Win-Win / Idea Meritocracy. Five Rods auto-review now structurally enforced (commit `3045fa8`) and v2 (commit `27a882f`) covers AGENTS.md detection and Copilot integration.

### 8.9 Mission Command precondition

> "Long-standing practices of initiative" (Herrera). **Trust by default requires earned trust, not declared alignment.** Council shadow-mode is the earning phase. Authority is granted only after the Phase-0 thresholds (§ 8.2) are met.

---

## 9. Security and safety

> Tier: [STRUCTURED] concerns, [LIVE] runtime details.

### 9.1 Phase note

Current phase is **research / dev**; **no client data yet** per the most recent handoff. Macs mostly cleared except email. This is the window in which the security posture can be tightened without operational pain — and **before** the marketing engine + CRM lands real client contacts.

### 9.2 MCP exposure (top concern)

- `amplified-knowledge-mcp` on `0.0.0.0:8401`.
- `beast-control-mcp` on `0.0.0.0:8402`.

Both should be on `127.0.0.1`. **Do not blindly rebind** — `BRAIN_READ_TOKEN_*` agents and any external-LAN consumer may depend on the current binding. **Inventory dependencies first** (§ 11.4). The repo has hardened DOCKER-USER firewall + port-rebinding work in commit `db7f86b` (PR84); this is the place to extend it.

### 9.3 CVE exposure (Cove audit)

- **CVE-2025-14987:** Temporal cross-namespace command execution on by default. Fixed in ≥ 1.27.4 / 1.28.2 / 1.29.2. Current Temporal ~1.24 → 6-hop upgrade required.
- **pgvector CVE-2026-3172** (CVSS 8.1) — buffer overflow in parallel HNSW. Affects 0.6–0.8.1. Fixed in 0.8.2.
- **PostgreSQL 15 batch CVEs** — CVE-2026-2004 / 2005 / 2006 (CVSS 8.8). Fixed in 15.16. Brain runs 15.17 → patched.

### 9.4 Hardcoded credentials / posture warnings (Cove audit; 13 PASS / 8 WARN / 0 FAIL)

- Temporal Postgres password hardcoded `temporal:temporal` in plaintext.
- Worker alpha/bravo/charlie/delta defined but never built/started; task queue naming inconsistent.
- No Prometheus scraping of Temporal metrics; no alerts.
- SMB guest shares on M5 (raw iCloud path) and M4 (Migration/Personal) — anyone on LAN can read.
- UFW INPUT ACCEPT on Beast without explicit deny rules; relies on Docker 127.0.0.1 binding.
- M4 Stealth mode OFF.

### 9.5 Operational hygiene

- Email / session / token leakage risk.
- Broad-root habits on Beast.
- Ingestion overreach (writing into Brain without receipt).
- **Status laundering** — treating [STRUCTURED] claims as [MEASURED]. Structural at this stage because of the Brain receipt gap.
- 5 plaintext API keys found on M4 + 6 on M5 (OpenAI, Moonshot, Whisper, Slack, Codex, Amplified, Kimi, Gemini, OpenClaw, Devin). All migrated to Infisical (Geordie report). Audit periodically — see `key-audit-report.md` and `key-management-recommendation.md`.

### 9.6 Tailscale state (recap from § 3.7)

M5↔M4 proven; Beast Tailscale SSH refused; wanmin Remote Login off; LAN guest shares wide open. **Not a complete production control plane.** Treat as a partially-proven research/dev mesh.

---

## 10. Build split — how to divide work across the fleet

> Tier: [STRUCTURED]. Each item is a commitment to attempt with a named owner and an evidence pack.

The point of the build split is **independent, parallelisable, evidence-backed work-streams**, each terminating in a PR (the *PR directory* as code-change evidence pack — § 11.7), each owned by one agent or pairing.

### 10.1 Cove / Templar — execution factory

- **Three live fires** (§ 3.5): register the 10 ghost workflows; install Docker binary in `cove_health_monitor`; reconcile `cove-task-queue` vs `build-orchestrator` for the 4 stuck IngestionPipelineWorkflows.
- 6-hop Temporal upgrade (§ 9.3).
- Pin Temporal Python SDK; add Worker Versioning + update handlers + heartbeating.
- Increase namespace retention from 24h; configure archival.
- Build the four declared workers (alpha/bravo/charlie/delta) or formally delete them.

### 10.2 Devin / Devon (cloud) — repos, CRM, Vellum, marketing wiring

- CRM route verification; finish 12 alembic migrations; first end-to-end client record write/read.
- Vellum Council mode: build (it is the lowest-friction unlock for the rest of the fleet).
- Vellum Correspondence mode: design pass first (Day Zero says do not use for customer-facing comms yet).
- Five Rods auto-review continuing on the 9 covered repos; extend to AGENTS.md-bearing repos.
- Estate cleanup: merge or close PR121 (with successor plan if not merged).

### 10.3 Claude Code — reasoning, off-GitHub estate, governance

- Refresh PR124 against the 46-container reality and the CRM correction.
- Reconcile this PR128 with `devin/1778919301-estate-discovery-report`.
- Maintain portable-spine.
- Patch the epistemic sample-size doctrine-code drift (§ 11.6).

### 10.4 DeepSeek (Geordie / Cortex) — infrastructure, ingestion

- Brain-writer inventory: enumerate every writer that has put rows into `knowledge_vectors` without an ingestion_manifest entry.
- BrainDrop design: ingestion-receipt enforcement so `ingestion_manifests` grows monotonically with `knowledge_vectors`.
- AMP-345 PUDDING extraction continues; reconcile with M4's `live-pipe-graphiti-ingest.py` / `live-pipe-ingest-vault.py` (potential drop-in replacements for parts of the pipeline).
- Beast cleanup: continue moving stale files to legacy-store under Day Zero discipline.

### 10.5 Kimmy — generalist + web builder

- Decide site: Kimmy's React+shadcn (M5) vs M4's static HTML — pick one, deploy one.
- After Vellum Council mode lands, join Council as the Kimi voice (heterogeneity benefit).
- Run AGENTS.md / SKILLS.md hygiene across the estate.

### 10.6 Vellum / Brain agents

- APDS receipt closure (§ 11.5) — this is the gating fix for the entire substrate.
- Linear → Vellum migration: Phase 1 parity (ticket create / assign / transition / alert / close).
- Audit-log schema (§ 8.6) implemented as tamper-evident append-only.

### 10.7 Marketing / product agents

- Quote-escaping bug ([STRUCTURED] 10-minute fix in marketing engine).
- Deploy `content-atomizer` (COV-226) and `email-sequence` (COV-227) containers.
- External engagement feedback loop — wire Kaizen to outcome signal, not just internal scoring.
- Substack expansion: from 1/5 published to 5/5.
- Phase-3 Remotion (video) prototype: address Beast CPU-only limitation (rent GPU or cloud-out the encode).

### 10.8 Council / Perplexity (research)

- Council shadow-mode telemetry (ECE, Brier, agreement) wired into Vellum.
- Perplexity research intake hardened into APDS-receipt-bearing rows, not loose markdown.

---

## 11. Immediate next plan (this week)

> Tier: [STRUCTURED] plan. Tasks are commitments to attempt, not predictions of outcomes.

1. **Refresh PR #124** ("Working Code Inventory") against the live 46-container reality and the CRM correction.
2. **Create a live estate receipt** — pin counts, container set, Brain health at a specific timestamp and store as an APDS-receipted record (eats its own dog food).
3. **CRM route verification** — close out "CRM not deployed" vs "CRM containers up" by exercising the 153 endpoints against the healthy `amplified-crm` container; finish the 12 alembic migrations.
4. **MCP dependency inventory** — before any rebinding of `0.0.0.0:8401` / `0.0.0.0:8402`, list what depends on those bindings. **No blind rebinding.**
5. **Brain-writer inventory + BrainDrop design** — enumerate every writer into `knowledge_vectors` without an ingestion_manifest; design enforcement so `ingestion_manifests` grows monotonically with `knowledge_vectors`. **This is the single highest-leverage governance fix.**
6. **Patch the epistemic sample-size rule** — replace flat `sample_size < 30` in both `epistemic_status.py` and `epistemic_status_invariant.py` with the current doctrine: **10 events per parameter per outcome class.** (Hashes in § 5.6.)
7. **Merge / reconcile estate report PRs** — pick between this PR128 v2 and `devin/1778919301-estate-discovery-report`; merge one, both with rename, or neither. Do **not** silently overlay.
8. **Promote only after receipt.** No surface promotes from [STRUCTURED] to [MEASURED] without an attached receipt.
9. **Day Zero cleanup window** — Day 1 storage + repo audit; Day 2 DB migration + Business Brain implementation against the canonical-write invariant; Day 3 content extraction + governance-as-PR-checks.

---

## 12. Appendices

> Tier: mixed. Each appendix labels its own tier.

### A. Repository reconciliation ([STRUCTURED] / [CANDIDATE])

- Operator working figure: **45 repos**.
- GitHub org metadata: **38 visible** (33 private, 5 public), 130,528 KB total.
- PR121 classification: 27 active / 12 deletion / 6 archive + migration scripts + 19-field schema.
- Tier 1 active (committed within 3 days, per `amplified-partners-snapshot-2026-05-15.md`): `devon-memory`, `crm`, `clean-build`, `amplified-machine`, `marketing-engine`, `portable-spine`, `perplexity-research`, `.github`.
- Off-GitHub: 15+ git repos on M5 + 14 on M4 (`hermes-workspace`, `Amplified:Paerplexity`, `deepseek-memory`, `Antigravity`, `amplified-hermes-team`, `thegoal`, `spec`, `project`, `documents`, `ewanbramley`, `ag` + 9 hash-named).

### B. Brain facts ([LIVE / VERIFY BEFORE USE], 2026-05-16)

See § 3.4 — full numbers. Role model in § 6.7 / `BRAIN_SECURITY_ARCHITECTURE.md`. Six layers of protection: PostgreSQL roles; schema separation (staging vs canonical vs views); network isolation (`brain-internal` docker network, cove-postgres only); credential rotation (`brain_writer` from Infisical only); audit trail (append-only `audit_log` on all canonical writes); write gate (`ingest-inbox` + APDS pipeline).

### C. 19-field schema ([CITED] `AI_CONTEXT_SCHEMA.md`)

See § 8.3 — clusters and the drop-breaks contract.

### D. Canonical data architecture ([STRUCTURED] target)

See § 2.2 + § 8.1. Portable control plane target = phone → Vellum → broker → Beast → host → audit.

### E. Artefact / source list ([STRUCTURED])

Primary source bundle: `/home/user/workspace/estate_sources_downloads/` (~396 files). High-signal nodes used in this report:

- `AMPLIFIED_FULL_ESTATE_MASTER_REPORT.md` — Geordie 2026-05-16 master.
- `day-zero-cove-vellum-thread-chapterised-verbatim-2026-05-16.md` — Day Zero doctrine.
- `antigravity-personal-control-plane-brief.md` + `backend_control_plane_spec.md` + `interaction_architecture_v1.md` — control plane.
- `BRAIN_ACCESS_ARCHITECTURE_V2.md` + `BRAIN_ACCESS_MASTER_HANDOVER.md` + `BRAIN_SECURITY_ARCHITECTURE.md` — Brain access.
- `COVE_TEMPORAL_BEAST_AUDIT.md` — Cove / Temporal / CVE detail.
- `SECURITY_AUDIT.md` — 13 PASS / 8 WARN / 0 FAIL.
- `app_inventory_and_value.md` + `audit-what-doesnt-need-to-exist.md` — value + deletion candidates.
- `SYNTHESIS_council_of_three.md` + `2026-05-14_RESEARCH_pipeline-council-kaizen-governance.md` — Council + governance.
- `2026-05-14_PRINCIPLE_seventeen-and-three.md` + `AI_CONTEXT_SCHEMA.md` + `DATA_ARCHITECTURE.md` — 17/19-field substrate.
- `2026-05-14_SPEC_ingestion-pipe.md` + `2026-05-14_SPEC_linear-to-vellum-migration.md` — pipeline + migration specs.
- `GEORDIE_CORTEX_SESSION_REPORT_2026-05-16.md` + `GEORDIE_CORTEX_workspace/AMPLIFIED-STATE.md` — Geordie state.
- `KIMMY_workspace/README.md` + `KIMMY_workspace/AGENTS.md` + `KIMMY_workspace/SKILLS.md` — Kimmy.
- `marketing_dossier/INDEX.md` — marketing engine summary.
- `amplified-partners-snapshot-2026-05-15.md` — org snapshot + Tier-1 repos.
- `2026-05-14_INSIGHT_ai-is-a-pudding.md` — product positioning seed.
- `GOLD_FOUND_M4_M5.md` + `M4_EXPLORATION_REPORT.md` + `FULL_PATHS_REFERENCE.md` — hidden-asset map.
- `key-audit-report.md` + `key-management-recommendation.md` — credentials.
- `_inbox-work/perplexity_live_exports_2026-05-13/` — live research imports (tier STRUCTURED).

### F. Contradictions and reconciliations ([STRUCTURED])

- **CRM status:** "not deployed" (PR124 / Master Report) vs "containers healthy" (live 2026-05-16). Resolution: containers up; functional verification pending; do not promote to "CRM works." (§ 3.2).
- **Container count:** "37+" / "40" / "42" vs **46**. Resolution: older snapshots not wrong-at-the-time; refresh to 46 as of 2026-05-16. (§ 3.1.)
- **Repo count:** 45 (operator) vs 38 (org metadata) vs 27 active (PR121). Resolution: broader estate vs visible org vs proposed classification. (§ 3.3, § 12.A.)
- **Cove workflows:** 12 designed / 2 running (Master Report) vs 10 designed / 2 registered / 8 ghost (Cove audit). Resolution: prefer Cove audit's measured numbers. (§ 3.5, § 6.4.)
- **Brain canonicality:** millions of vectors but 1 ingestion_manifest + 1 audit_log. Resolution: substrate populated, not canonical. (§ 5.5.)
- **DeepSeek audit `[MEASURED]` label:** under min-rule discipline it should be `[STRUCTURED]` until raw evidence is attached.
- **Vellum:** container running but **Council mode designed-not-built**; **Correspondence mode not built**. (§ 3.5, § 6.5.)
- **`epistemic_status*.py`:** doctrine-code drift on sample-size threshold. (§ 5.6.)
- **Two websites** of the same name, different agents. (§ 5.6.)
- **Two estate-discovery-report PRs** (this PR128 + `devin/1778919301-estate-discovery-report`). (§ 11.7.)

### G. Beast runtime caveat (repeated deliberately)

[LIVE / VERIFY BEFORE USE]. Every Beast/Brain/Tailscale/GitHub/Vellum/Linear runtime claim is frozen at 2026-05-16. Container counts, port bindings, Tailscale reachability and row counts drift. Before acting operationally, re-verify against the live system.

### H. PR directory as code-change evidence pack ([INTUITED] future state)

A PR directory — one folder per merged PR carrying the diff, the rationale, the Council vote (if any), the audit-log fragment, and the receipted artefacts produced — is a natural extension once Vellum Correspondence + APDS receipts land. Today it is aspirational; called out so future builds can grow into the slot rather than re-inventing it.

---

## Closing

The estate is not a failure. It is a working but unsorted hoard, built by one operator at speed with AI as the lever. The honest move is to curate it, not to apologise for it.

The single change that moves the DriftSignal from **AMBER** toward **GREEN** is receipt coverage on Brain writes (§ 5.5, § 8.4, § 11.5). Everything else — the CRM finish, the marketing engine completion, the Council shadow mode, the control plane — sits more solidly on top of a Brain that can defend its own canonicality.

This report is the index that says: here is what is in the hoard, here is what works, here is what is candidate, here is what must be verified before anyone bets on it, and here is how to split the work so it actually ships.

---

Signed,

**Devon (Claude Code subagent)**
Session: estate-discovery-report (v2 cohesive)
2026-05-16
