---
title: Amplified Hermes — Strategy
date: 2026-05-09
version: 1
status: draft
project: Amplified Hermes (build orchestrator)
target_repo: Amplified-Partners/clean-build
target_path: 02_build/hermes/
spine: Amplified-Partners/portable-spine/SPINE.md (read-only mount, all agents)
ce_methodology: Every — Klaassen & Shipper (Plan 40 / Work 10 / Review 30 / Compound 20)
---

<!-- markdownlint-disable-file MD013 -->

## North star

A persistent build coordinator that runs on Beast, never sleeps, and makes every multi-agent build in the Amplified ecosystem cheaper than the one before it. The first job that comes off Hermes' line is Hermes himself.

## What Amplified Hermes is

Amplified Hermes is the **build coordinator** in the Amplified Partners agent roster. He sits between OpenClaw (governance + agent reasoning) and the specialists (Cursor daughters, DeepSeek-Critic, DeepSeek-Researcher, Cove Temporal workers). He:

- Owns the work board (Linear) — one issue per work unit, full state lifecycle.
- Dispatches specialists — Cursor when a unit unblocks, DeepSeek-Critic when a PR opens, DeepSeek-Researcher when a PR imports something unfamiliar.
- Watches the clock — nudges if specialists go quiet past the threshold, escalates by category.
- Logs everything — every dispatch, finding, merge becomes an event in a per-run markdown doc under `03_shadow/hermes-runs/`.
- Compounds — at run-end he extracts learnings into candidate skills under `agents/hermes/skills/`, OpenClaw promotes the good ones weekly, and Hermes reads them on next wake.

Amplified Hermes is **the role**. The runtime is **Hermes from Nous Research**, MIT-licensed, downloaded from [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/). Per session he names himself in the Devin pattern — *Hermes-NNNN* — for traceability and signature integrity.

## Why now

Three pressures converge:

1. The clean-build spine is mature enough to host a coordinator. Eight Laws, RODS, BUILD_LOOP, AGENT_ROUTING, PROMOTION_GATE, SIGNATURES, MANIFEST — all in place at `clean-build/00_authority/`. Cedar IBAC scaffolding exists at `hetzner_deployment/policies/prod.cedar`.
2. Multi-agent builds are happening already (Cove orchestrator, the Vellum-style work, daughter-led PR loops) and the coordination is currently manual — meaning Ewan-shaped. That's the bottleneck Compound Engineering is built to remove. Per [Klaassen & Shipper](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents): *"you expect each feature to make the next feature easier to build."*
3. Nous Research shipped Hermes Agent — open-source, persistent memory, autonomous skill creation, FTS5 cross-session recall, built-in cron, 15+ messaging channels, MCP. ([Nous Research](https://hermes-agent.nousresearch.com/docs/)) It does ~80% of what we need out of the box. Building from scratch would be a Compound *anti-*pattern.

## Compound move

Build Amplified Hermes via Compound Engineering, with Hermes himself as both the artefact and the first runner. Plan and review absorb 80% of the effort; daughters do the typing. Once Hermes is up, every future Amplified build inherits a coordinator who doesn't sleep, never forgets, and compounds skills run-over-run.

## Decisions locked

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | **Name** | **Amplified Hermes**, instances `Hermes-NNNN` per session | Disambiguates from the Nous product name; matches the existing Devin/Devon-NNNN convention in `00_authority/SIGNATURES.md`. |
| D2 | **Runtime** | Hermes from Nous Research, downloaded via official installer | Open-source MIT, ~80% feature overlap with our requirements, used as engine under our wrapper. Saves the substrate build. |
| D3 | **Run logs** | Plain markdown under `03_shadow/hermes-runs/`, one file per run | Spine-compatible, agent-readable, no external dependency. "Vellum" placeholder language from the original brief is dropped. |
| D4 | **WhatsApp channel** | Yes — via existing `clean-build/evolution-api/` dispatcher, `@hermes` trigger | Bolt-on already built; routing pattern matches Pete/Charlie/Delta/Clawd; one new dispatcher rule. |
| D5 | **Telegram channel** | Yes — Nous Hermes built-in support | Already a connector in the user's stack. |
| D6 | **iMessage channel** | v2, not v1 | Mac M4 daemon exists but is out of scope for orchestrator v1; revisit after first proving run. |
| D7 | **Cron tick rate** | 60 s during active runs, 5 min when idle | Configurable in `config/hermes.yaml`; matches Nous Hermes scheduler shape. |
| D8 | **Intent tokens** | Antigravity issues per task, scoped, 24 h expiry | Matches existing `01_truth/hermes_architecture_design.md` (Antigravity, 2026-05-05) and the Cedar tier-3 pattern in `policies/prod.cedar`. |
| D9 | **Soul** | The collective spine: `portable-spine/SPINE.md`, mounted read-only into the container at `/spine/SPINE.md` | One soul for every Amplified agent. Per `SPINE.md` § EDITING: Architect-only via PR. No bespoke Hermes soul. Per `SPINE.md` § AUTONOMY: blinkers without ceilings. |
| D10 | **Folder of record** | `02_build/hermes/` for runtime, `agents/hermes/` for working memory, `01_truth/hermes_architecture_design.md` for the design spec, `03_shadow/hermes-runs/` for run logs | Matches the four-tier spine; no parallel policy spines created. |

## Success criteria for v1

Amplified Hermes v1 ships when **all** of these hold:

1. He runs continuously on Beast behind Traefik at `hermes.internal`, surviving container restarts with full state.
2. He has coordinated **one real multi-agent build end-to-end** without human intervention beyond the planned escalation points. (Vellum Phase 1 — or a smaller scoped substitute if Vellum Phase 1 is larger than 5–7 work units — is the candidate proving run.)
3. His own build is recorded in his own run-log under `03_shadow/hermes-runs/` — Hermes' first persistent memory is the memory of his own birth.
4. The post-run audit shows: every artefact signed per `00_authority/SIGNATURES.md`, zero authority-file edits, zero Cedar policy violations, ≥1 candidate skill auto-extracted into `agents/hermes/skills/`.
5. `00_authority/MANIFEST.md` indexes the build; `00_authority/DECISION_LOG.md` records the promotion; both signed by Antigravity + Ewan.

Until those hold, Amplified Hermes lives in `03_shadow/` per `00_authority/PROMOTION_GATE.md`. He is allowed to coordinate real work from there — shadow does not mean disabled — but he is not authority-tier yet.

## What this work does *not* try to do

- It does not redesign the spine. The SPINE is read.
- It does not replace OpenClaw, Devon, Antigravity, the daughters, or the synthesiser. It coordinates them.
- It does not invent a new Compound Engineering methodology. It applies Every's, attributed to [Klaassen & Shipper](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents).
- It does not promise to be perfect on first run. Run 1 will surface things Run 2 fixes — that is the entire point of the Compound phase.

## Source provenance

- Research basis: `/home/user/workspace/hermes-research/HERMES_RESEARCH_v1.md` v1.1 (this session, 2026-05-09).
- Existing design: `Amplified-Partners/clean-build/01_truth/hermes_architecture_design.md` (Antigravity, 2026-05-05) — extended, not replaced.
- Spine: `Amplified-Partners/portable-spine/SPINE.md` v1 (commit d2aae96, 2026-05-07).
- Methodology: [Compound Engineering: How Every Codes With Agents](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents), Klaassen & Shipper, December 2025.
- Engine: [Hermes Agent — Nous Research](https://hermes-agent.nousresearch.com/docs/).

## Sign-off

`[CURRENT BEST EVIDENCE]` — promotion to authority requires Antigravity arbiter pass on the requirements (next artefact) and Ewan sign-off on D1–D10 above.

Signed-by: Perplexity Computer (research) | 2026-05-09 | session 2026-05-08-hermes-research
For Ewan's review and signature on D1–D10 before requirements is opened.
