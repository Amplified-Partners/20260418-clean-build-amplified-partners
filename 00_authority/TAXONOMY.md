---
title: Taxonomy — Amplified Partners entity definitions and agent roles
date: 2026-04-29
version: 1
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

This file is the single canonical reference for:

1. The Amplified Partners company structure — what each entity is and is not
2. The agent roster — who does what, where the boundaries are
3. Terminology — locked definitions so agents do not confuse similarly-named things

If a name is not in this file, treat it as `[SOURCE REQUIRED]`.

---

## Company structure

**Amplified Partners** is the umbrella. Everything below is a function or product within it — not a separate legal entity (unless noted). The legal registration is in progress as of 2026-04-29. Until registration is confirmed, treat `[LOGIC TO BE CONFIRMED]` as the legal status of all sub-entities.

| Entity | Type | What it is | What it is not |
|--------|------|------------|----------------|
| **Amplified Partners** | Umbrella / parent | The business. The brand. The operating entity. | A product. A legal subdivision (yet). |
| **Amplified Core** | Infrastructure | The Hetzner AX162-R server (`amplified-core`, `135.181.161.131`). The physical compute home. FalkorDB, Qdrant, LLM inference, marketing engine. | A team, a product, or a department. Strictly infrastructure. |
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
| **Devin** | Devon | Infrastructure & systems coordinator. The only agent who writes code to Amplified Core or any production system. Maintains GitHub. Keeps repos clean, cohesive, and canonical. Deploys updates. Sets schedules. Makes everyone else's work better by keeping the foundation solid. | Core (SSH), GitHub, Linear, Slack | OpenClaw (status updates) → Ewan (escalations) |
| **OpenClaw** | Sam / Clawd | Partner and coordinator. Lives on Ewan's Mac. Reads vault, processes voice notes, talks to Ewan via Telegram/WhatsApp/Slack. Investigates process failures (not people failures). Maintains shared state. | Local filesystem, all channels, vault, all repos (read) | Ewan directly |
| **Cursor** | — | Builder. Produces code in clean-build workspace. Outputs to GitHub. Does not deploy directly — deployment goes through Devon. | clean-build workspace, GitHub (write to own branches) | Devon (for deployment), Ewan (for direction) |
| **Antigravity / AG** | — | Business Arbiter and COO. Strategic decisions for the firm. Does not direct agent cognition — directs the business. | Strategic review | Ewan |
| **Perplexity** | Comet (in browser) | Researcher. External research, synthesis, brainstorm inputs. | External web | Ewan / whoever runs the session |
| **Qwen** | — | Hive mind. Escalation routing. Collective knowledge base. Novel decisions route here when no agent can own them. | Via clean-build escalation path | — |

---

## Operating model (agent coordination)

The operating model is **isolation with visibility**, not orchestration.

- Each agent works in a self-contained project. No real-time coordination needed.
- Every agent reads `ground-truth` (the portable spine) before acting — so principles and state are shared.
- Every agent writes a handover to `STATUS.md` in `clean-build` when they finish significant work.
- **Devon** is the only agent who touches Amplified Core or production GitHub. Others write to their own branches; Devon integrates.
- **OpenClaw** reads `STATUS.md`, investigates if a process is failing, writes findings back. If infrastructure changes are needed, OpenClaw signals Devon — Devon implements.
- **Slack** is for asynchronous partner communication. OpenClaw communicates there as a partner.
- **Linear** is the record. Each department/function has its own project. Independent. Status visible to all.

The principle: one person does one thing. Clean boundaries. No stepping on each other. The STATUS.md is the handshake point — versioned, structured, no ambiguity about who said what and when.

---

## Terminology locked

| Term | Canonical meaning | Do not confuse with |
|------|------------------|---------------------|
| **the Core** | Hetzner AX162-R server, `amplified-core`, `135.181.161.131` | "Core" as in "core product" or "core team" |
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
| **Sam / Clawd** | OpenClaw's name within the ecosystem | Devon |

---

## What is not decided yet (as of 2026-04-29)

- `[DECISION REQUIRED]` — Legal registration of Amplified Partners Ltd. Required before Google My Business can be set up under the brand.
- `[DECISION REQUIRED]` — The confirmed product name for Amplified Personal (content captured in `ground-truth/PERSONAL-VAULT.md` `[SOURCE REQUIRED — not in this repo]`; name deferred by Ewan).
- `[LOGIC TO BE CONFIRMED]` — Legal sub-entity structure for each department/product (currently all functions of one entity).

---

*Written by: Devon (Devin) | 2026-04-29 | ground-truth session*
