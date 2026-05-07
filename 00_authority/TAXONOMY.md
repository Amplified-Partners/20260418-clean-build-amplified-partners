---
title: Taxonomy — Amplified Partners entity definitions and agent roles
date: 2026-05-07
version: 4
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

This file is the single canonical reference for:

1. The Amplified Partners company structure — what each entity is and is not
2. The agent roster — who does what, where the boundaries are
3. Terminology — locked definitions so agents do not confuse similarly-named things

If a name is not in this file, treat it as `[SOURCE REQUIRED]`.

## What this taxonomy is not

This file defines **entities, agents, and locked terminology**. It does **not** assign **cost tiers** to agents (e.g. "Devon = always-Sonnet", "Cassian = always-Haiku"). Cost-tier classification is the job of `cost-tools/token_proxy.py`, which routes per-call based on prompt content (see `01_truth/SYSTEMS-AND-API-REGISTER.md` § 14 and `02_build/INFRASTRUCTURE.md` § AI / ML services). Agent-layer routing (which agent runs which task) lives in `00_authority/AGENT_ROUTING.md`. The two layers stack and are deliberately independent of this file.

---

## Company structure

**Amplified Partners** is the umbrella. Everything below is a function or product within it — not a separate legal entity (unless noted). The legal registration is in progress as of 2026-04-29. Until registration is confirmed, treat `[LOGIC TO BE CONFIRMED]` as the legal status of all sub-entities.

| Entity | Type | What it is | What it is not |
|--------|------|------------|----------------|
| **Amplified Partners** | Umbrella / parent | The business. The brand. The operating entity. | A product. A legal subdivision (yet). |
| **Amplified Core** | Infrastructure | The Hetzner AX162-R server (`amplified-core`, `135.181.161.131`). The physical compute home. See `00_authority/CANONICAL_ESTATE.md` for full service topology. | A team, a product, or a department. Strictly infrastructure. |
| **Amplified Marketing** | Function | The content pipeline and marketing engine. Runs on the Core. Produces social, GMB, LinkedIn content. Evaluated by Bob/Lisa/Marcus synthetic avatars. | The marketing *team* or strategy. The engine that executes the strategy. |
| **Amplified Central Ops** | Function | AI-native governance layer. The clean-build workspace, agent operating contracts, decision logs, authority hierarchy. The spine of how the business runs. | A tech team. Not code. Not infrastructure. The rules and governance that infrastructure runs under. |
| **Amplified Client** | Product tier | The client-facing advisory product for businesses — Bob, Lisa, Marcus. The CRM, the Interview Engine, the federated architecture, the PicoClaw sidecar. | Internal tooling. Does not include personal/consumer products. |
| **Cove** | Product | The WhatsApp-native AI interface for clients. Conversational, channel-based. Where Bob talks to the system. | The Core. Not a server. A product surface. |
| **Covered AI** | Product | `[DECISION REQUIRED]` — distinct from Cove. Definition to be provided by Ewan. Do not conflate with Cove. | Cove. These are separate. |
| **Amplified Personal** | Product | Consumer/public product. Data sovereignty for individuals. Secure personal vault hosting — Amplified cannot see inside it, one click to leave and take everything. | The client business product. This is for individuals, not SMBs. |

**On naming conflicts:**
- **Amplified Core** (the server) ≠ **Amplified Central Ops** (governance). Core = hardware. Central Ops = rules.
- **Amplified Client** (the product) ≠ **client** (a customer of Amplified Partners). Context distinguishes.
- **Cove** ≠ **Covered AI**. These are separate products. Do not use interchangeably. Covered AI definition is `[DECISION REQUIRED]`.

---

## Agent roster

The operating model: each agent is self-contained. Projects are independent. Coordination is not needed day-to-day — clarity of role is what prevents collision. Agents communicate asynchronously through GitHub (STATUS.md) and Slack, not in real time.

| Agent | Name | Core responsibility | Access scope | Reports to |
|-------|------|---------------------|--------------|------------|
| **Antigravity / AG** | — | COO and Business Arbiter. Strategic decisions for the firm. Directs the business, not agent cognition. Primary author of constitutional and architectural documents. | Full (SSH to Beast), all repos, Cursor (M5) | Ewan |
| **Devin** | Devon | Infrastructure & systems coordinator. Writes code to Amplified Core and production systems. Maintains GitHub. Keeps repos clean, cohesive, and canonical. Deploys updates. Sets schedules. | Core (SSH), GitHub, Linear, Slack | Ewan |
| **Perplexity** | Computer | Researcher and enterprise intelligence. External research, synthesis, brainstorm inputs. Strategic planning support. | External web, Linear, GitHub | Ewan |

**Retired agents** (no longer in the active roster):

| Agent | Status |
|-------|--------|
| OpenClaw / Sam / Clawd / Cassian | Retired. Container (`openclaw-agents`) remains on Beast but agent is decommissioned. |
| Cursor (standalone) | Subsumed into Antigravity's toolchain (Cursor is the IDE, not a separate agent). |
| Qwen | Retired from escalation routing role. |
| Kimmy | Status to be confirmed by Antigravity. |
| Eli | Retired. |

---

## Operating model (agent coordination)

The operating model is **isolation with visibility**, not orchestration.

- Each agent works in a self-contained project. No real-time coordination needed.
- Every agent reads `ground-truth` (the portable spine) before acting — so principles and state are shared.
- Every agent writes a handover to `STATUS.md` in `clean-build` when they finish significant work.
- **All agents have Beast access.** No "I don't have access" as a reason to stop. See `00_authority/CANONICAL_ESTATE.md` Rule 5.
- **Linear** is the record. Each department/function has its own project. Independent. Status visible to all.
- **GitHub** is for code and governance. PRs for changes, reviews for quality.
- Draft→Sync→Rebuild→Execute protocol is absolute. See `00_authority/CANONICAL_ESTATE.md` Rule 6.

The principle: one person does one thing. Clean boundaries. No stepping on each other. The STATUS.md is the handshake point — versioned, structured, no ambiguity about who said what and when.

---

## Terminology locked

| Term | Canonical meaning | Do not confuse with |
|------|------------------|---------------------|
| **the Core / Beast** | Hetzner AX162-R server, `amplified-core`, `135.181.161.131`. Full topology: `00_authority/CANONICAL_ESTATE.md` | "Core" as in "core product" or "core team" |
| **the vault** | `/opt/amplified/vault/` on the Core — 4,891 files, 7M words, 30 folders | real-vault (local Obsidian on the Mac) |
| **real-vault** | `/Users/ewanbramley/Manual Library/real-vault/` — local Obsidian vault | the Core vault |
| **clean-build** | The governed agent workspace at `/Users/ewanbramley/AG/clean-build/` and `Amplified-Partners/20260417-clean-build-amplified-partners` | The Core. Not infrastructure — governance. |
| **ground-truth** | The portable spine repo at `Amplified-Partners/ground-truth`, local at `/Users/ewanbramley/Manual Library/Projects/open-claw-build/` | clean-build. Different purpose: spine vs governed workspace. |
| **Chit** | The ghost sidecar product for multi-person SMBs | The CRM. Not the data store — the UI/interaction layer that sits beside existing tools. |
| **Cove** | The WhatsApp-native product surface (conversational interface to AI for clients) | The Core. Not hardware. Not Covered AI. |
| **Covered AI** | Separate product — definition `[DECISION REQUIRED]`, to be provided by Ewan | Cove. Do not use interchangeably. |
| **Byker** | Codename for the production system on Railway. The factory runtime. | The Core. Different infrastructure. |
| **Pudding** | The cross-client anonymised discovery technique | A specific tool or library. It is a methodology. |
| **PicoClaw** | Beelink N150 mini PC placed physically on-site at Tier 3+ clients | The Core. Client-side hardware, not central infrastructure. |
| **Devon** | Devin's name within the Amplified Partners ecosystem | Any other agent |
| **Computer** | Perplexity's name within the ecosystem | Other agents |
| **Sam / Clawd / Cassian / OpenClaw** | Retired agent's names (all aliases for the same agent). Historically: partner and coordinator on Ewan's Mac. Now decommissioned. | Devon |

---

## What is not decided yet (as of 2026-04-29)

- `[DECISION REQUIRED]` — Legal registration of Amplified Partners Ltd. Required before Google My Business can be set up under the brand.
- `[DECISION REQUIRED]` — The confirmed product name for Amplified Personal (content captured in `ground-truth/PERSONAL-VAULT.md` `[SOURCE REQUIRED — not in this repo]`; name deferred by Ewan).
- `[LOGIC TO BE CONFIRMED]` — Legal sub-entity structure for each department/product (currently all functions of one entity).

---

*Written by: Devon (Devin) | 2026-04-29 | ground-truth session*

---

## Changelog

### v4 — 2026-05-07

- **Agent roster updated** per Ewan's instruction (2026-05-07): active roster is now Antigravity, Devon, Perplexity (Computer). Retired agents moved to a separate table: OpenClaw/Sam/Clawd/Cassian, Cursor (standalone), Qwen, Kimmy, Eli.
- Added pointer to `00_authority/CANONICAL_ESTATE.md` in the Amplified Core row and "the Core" terminology entry.
- Updated operating model section: removed references to retired agents, added Beast access rule and Draft→Sync→Rebuild→Execute protocol references.
- Added **Computer** to locked terminology table.
- Source: AMP-180.

Signed-by: Devon-f473 | 2026-05-07 | session devin-f473301112514d75be796be926a54923

### v3 — 2026-05-03

- Added **Cassian** as a canonical alias for OpenClaw (alongside the existing **Sam / Clawd**) in both the agent-roster row and the locked-terminology table. Ewan uses "Cassian" interchangeably with "OpenClaw" / "Clawd" / "Sam" in chat and knowledge notes; this brings the locked terminology in line with established usage so `AGENT_ROUTING.md` and other authority files can use "Cassian" without violating bibliography integrity. **No changes to the company structure or agent roster** — same agent, additional canonical alias.
- Frontmatter `version` bumped to v3.

Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### v2 — 2026-05-03

- Added § "What this taxonomy is not": an explicit lock that cost-tier classification is the job of `cost-tools/token_proxy.py`, not this file. Agent-layer routing rules live in `00_authority/AGENT_ROUTING.md`. The two layers (model-layer routing in the proxy + agent-layer routing in `AGENT_ROUTING.md`) stack and are independent of this taxonomy.
- No changes to the company structure or agent roster.

Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`
