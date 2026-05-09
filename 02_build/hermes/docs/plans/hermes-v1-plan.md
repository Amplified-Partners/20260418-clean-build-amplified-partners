---
title: Amplified Hermes — v1 Plan (U-IDs ready to build)
date: 2026-05-09
version: 1
status: draft
parent: 02_build/hermes/docs/brainstorms/hermes-requirements.md
audience: DeepSeek-Researcher (scaffold), Cursor daughters (build), DeepSeek-Critic (review)
ce_phase: Plan (40%) — handoff to Work (10%)
---

<!-- markdownlint-disable-file MD013 -->

## How to use this plan

This is the build plan. It decomposes the requirements (F1–F10 + N1–N10, 60 acceptance tests) into **U-IDs** — atomic work units, each sized for a single Cursor daughter session, with explicit dependencies. The flow:

1. **DeepSeek-Researcher + Terminal** runs the **scaffold pass** in §1 (one prompt, one commit).
2. **Cursor daughters** claim U-IDs in dependency order from the **U-ID register** in §2. One PR per U-ID.
3. **DeepSeek-Critic** reviews each PR per §3.
4. **Synthesiser (Perplexity Computer / Claude session)** triages findings per §4.
5. **Hermes himself**, once unit U-30 ships, takes over coordination for the remaining U-IDs. (Yes — he builds himself from U-30 onwards. That's the point.)

Each U-ID block carries: **Approach** (how), **Verification** (which acceptance tests it satisfies + how to demonstrate), **Dependencies** (other U-IDs that must be `merged` first), **Estimated session size** (small / medium / large), **Lane** (which specialist pool).

## §1. Scaffold pass — DeepSeek-Researcher prompt

Run this once. Output is a single PR titled `AMP-XXX: Hermes v1 scaffold` with one commit signed `DeepSeek-Researcher | 2026-05-09 | <session-id>`.

```text
You are DeepSeek-Researcher running on Terminal. Read these in order:

  1. Amplified-Partners/portable-spine/SPINE.md
  2. Amplified-Partners/clean-build/AGENTS.md (root)
  3. Amplified-Partners/clean-build/00_authority/MANIFEST.md
  4. Amplified-Partners/clean-build/00_authority/EIGHT_LAWS.md
  5. Amplified-Partners/clean-build/00_authority/SIGNATURES.md
  6. Amplified-Partners/clean-build/02_build/hermes/STRATEGY.md
  7. Amplified-Partners/clean-build/02_build/hermes/docs/brainstorms/hermes-requirements.md
  8. Amplified-Partners/clean-build/02_build/hermes/docs/plans/hermes-v1-plan.md  (this file)

Then create the folder structure exactly as listed in §1.1 below, with empty
files containing only:
  - YAML frontmatter (where appropriate per Amplified file conventions)
  - A one-line purpose comment
  - The signature footer pre-filled

Do NOT implement logic. Do NOT write tests yet. Stub functions with `pass` and
`raise NotImplementedError("U-NN")` referencing the U-ID that owns each file.

Then create one Linear issue per U-ID (U-01 through U-32) with:
  title:  [HERMES] U-NN: <slug>
  body:   the U-ID block from §2 verbatim (including Approach + Verification +
          Dependencies + Lane)
  labels: cursor-daughter | deepseek-critic | deepseek-researcher (per Lane);
          plus 'unblocked' (no unmet deps) or 'blocked-by-U-NN' (otherwise)
  team:   <Amplified Partners Linear team id from clean-build/hetzner_deployment/linear_reporter.py>

Open one PR titled "AMP-XXX: Hermes v1 scaffold" against main. Sign the PR
description with your DeepSeek-Researcher session id. Do NOT request a review;
that's the next step.

If anything in steps 1–8 is unclear or contradicts the spine, STOP and write
a Linear issue titled "[HERMES] BLOCKER: <one-line>" with full context, and
exit. Do not invent. Do not patch. Do not push.
```

### §1.1 — Folder structure to scaffold

```
clean-build/
├── 02_build/hermes/
│   ├── README.md                                # purpose: map for the next agent
│   ├── STRATEGY.md                              # already exists (this work)
│   ├── docs/
│   │   ├── brainstorms/hermes-requirements.md   # already exists (this work)
│   │   └── plans/hermes-v1-plan.md              # already exists (this work)
│   ├── docker-compose.yml                       # U-02
│   ├── Dockerfile                               # U-02
│   ├── pyproject.toml                           # U-02
│   ├── Makefile                                 # U-02
│   ├── config/
│   │   ├── hermes.yaml                          # U-04
│   │   ├── spine.mount                          # U-04 (read-only mount of portable-spine/SPINE.md → /spine/SPINE.md)
│   │   ├── policies/hermes.cedar                # U-05
│   │   └── channels.yaml                        # U-12
│   ├── src/hermes/
│   │   ├── __init__.py
│   │   ├── main.py                              # U-08
│   │   ├── state_machine.py                     # U-09
│   │   ├── ticker.py                            # U-10 (cron loop, 60s active / 5min idle)
│   │   ├── singleton.py                         # U-11 (Postgres advisory lock)
│   │   ├── dispatch/
│   │   │   ├── __init__.py
│   │   │   ├── router.py                        # U-13
│   │   │   ├── cursor_daughters.py              # U-14
│   │   │   ├── deepseek_critic.py               # U-15
│   │   │   └── deepseek_researcher.py           # U-16
│   │   ├── escalation/
│   │   │   ├── __init__.py
│   │   │   ├── thresholds.py                    # U-17
│   │   │   ├── categoriser.py                   # U-18
│   │   │   └── routes.py                        # U-19
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   ├── episodic.py                      # U-20 (SQLite)
│   │   │   ├── decisions.py                     # U-21
│   │   │   ├── intent_tokens.py                 # U-22
│   │   │   └── postgres_flush.py                # U-23
│   │   ├── compounding/
│   │   │   ├── __init__.py
│   │   │   ├── run_doc_writer.py                # U-24
│   │   │   ├── skill_extractor.py               # U-25
│   │   │   └── known_imports.py                 # U-26
│   │   ├── connectors/
│   │   │   ├── __init__.py
│   │   │   ├── linear.py                        # U-27 (extends hetzner_deployment/linear_reporter.py)
│   │   │   ├── github.py                        # U-28
│   │   │   ├── slack.py                         # U-29
│   │   │   ├── telegram.py                      # U-29
│   │   │   ├── whatsapp.py                      # U-29 (Evolution API plug-in)
│   │   │   └── token_proxy.py                   # U-07 (forces ANTHROPIC_BASE_URL)
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── server.py                        # U-30 (FastAPI: /task /state /interrupt /health /metrics)
│   │       ├── auth.py                          # U-31
│   │       └── audit.py                         # U-32
│   ├── state/                                   # gitignored; created at deploy time
│   │   └── .gitkeep
│   ├── tests/
│   │   ├── conftest.py                          # U-03
│   │   ├── fixtures/
│   │   │   ├── synthetic_run.json               # U-03
│   │   │   └── synthetic_plan.md                # U-03
│   │   ├── unit/                                # one test_*.py per U-ID, owned by that U-ID
│   │   ├── integration/
│   │   │   ├── test_state_persists.py           # owned by U-20+U-23
│   │   │   ├── test_singleton_lock.py           # owned by U-11
│   │   │   ├── test_resume_after_crash.py       # owned by U-10+U-11+U-24
│   │   │   └── test_cedar_tier3.py              # owned by U-05+U-22
│   │   └── e2e/
│   │       └── test_synthetic_proving_run.py    # U-32
│   └── scripts/
│       ├── start.sh                             # U-02
│       ├── deploy.sh                            # U-02 (Devon-only at runtime)
│       └── seed_spine.sh                        # U-02
│
├── agents/hermes/                               # working memory; agent-writable
│   ├── role.md                                  # U-06 (primary role, scope-of-session)
│   ├── skills/
│   │   ├── README.md                            # schema spec
│   │   └── known-imports.txt                    # U-26 (seeded list)
│   ├── handovers/
│   │   └── README.md                            # baton-pass log convention
│   └── runs/
│       └── README.md                            # pointer to 03_shadow/hermes-runs/
│
├── 01_truth/
│   ├── hermes_architecture_design.md            # bump v1→v2 in U-01 (acceptance criteria added)
│   └── interfaces/
│       └── hermes_api_v1.md                     # U-30 (OpenAPI spec)
│
├── 03_shadow/
│   ├── hermes-runs/
│   │   └── README.md                            # run-doc convention
│   └── research/
│       └── 2026-05-09_hermes-compound-engineering_v1.md  # MOVED from RESEARCH_HERMES_AND_COMPOUND_ENGINEERING.md (root)
│
├── hetzner_deployment/
│   └── policies/
│       └── (no changes; hermes.cedar lives under 02_build/hermes/config/policies/)
│
└── 00_authority/
    ├── AGENT_ROUTING.md                          # PATCH in U-01 (new Rule 9: build coordination → Hermes)
    ├── DECISION_LOG.md                           # APPEND in U-01 (Hermes v1 + name decision)
    └── MANIFEST.md                               # APPEND in U-01 (index new files; bump version)
```

## §2. U-ID register

Lanes:
- **CD** = Cursor Daughter (writes code + tests)
- **DR** = DeepSeek-Researcher (scaffold + research-y patches)
- **DC** = DeepSeek-Critic (review only)
- **DV** = Devon (deploy / production-touching)
- **AG** = Antigravity (arbiter pass)

Sizes: **S** ≤ 1 daughter session (~30 min), **M** = 1–2 sessions, **L** = 2+ sessions (split if it threatens to be L).

### U-01 — Authority patches (3 files)
- **Approach:** Bump `01_truth/hermes_architecture_design.md` to v2 with the F/N acceptance criteria from `hermes-requirements.md` inlined; add Rule 9 to `00_authority/AGENT_ROUTING.md` (build coordination → Amplified Hermes); append a `DECISION_LOG.md` entry recording D1–D10 from `STRATEGY.md`; append a `MANIFEST.md` v56 entry indexing all new paths under `02_build/hermes/`, `agents/hermes/`, `03_shadow/hermes-runs/`, `01_truth/interfaces/hermes_api_v1.md`.
- **Verification:** Bibliography integrity check passes (all referenced files exist); each authority file has a fresh changelog entry signed per `00_authority/SIGNATURES.md`; CODEOWNERS gating at `.github/CODEOWNERS` requires Ewan review (already in place; verify).
- **Dependencies:** none.
- **Lane:** CD. **Size:** S. **Acceptance touched:** N6.A1, N9.A1.

### U-02 — Container + deploy scaffold
- **Approach:** Write `Dockerfile` (Python 3.12 slim, install Nous Hermes, install our package); `docker-compose.yml` extending `hetzner_deployment/docker-compose.yml` (Traefik label `hermes.internal`, mount `portable-spine/SPINE.md` read-only at `/spine/SPINE.md`, mount Cedar policy read-only, mount SQLite volume); `pyproject.toml` (deps: hermes-agent, fastapi, sqlalchemy, asyncpg, httpx, pydantic, slack-sdk, python-telegram-bot, structlog, prometheus-client, langfuse, cedar-py); `Makefile` with `dev / test / build / deploy / rollback`; three shell scripts (`start.sh`, `deploy.sh`, `seed_spine.sh`).
- **Verification:** `make build` produces an image; `make dev` starts a local Hermes that binds 8080; image size sanity-checked (<500 MB); SBOM generated in CI; `seed_spine.sh` creates `agents/hermes/` from a fresh checkout.
- **Dependencies:** U-01 (manifest entry must exist before image is built).
- **Lane:** CD. **Size:** M. **Acceptance touched:** N10.A1, N10.A2.

### U-03 — Test harness
- **Approach:** Set up `pytest` config with markers (`unit`, `integration`, `e2e`); `conftest.py` with fixtures for: temp SQLite, fake Postgres (via `pytest-postgresql`), fake Linear (httpx mock), fake Slack/Telegram/WhatsApp; `tests/fixtures/synthetic_run.json` (sample run with all 7 state-machine transitions + 1 nudge + 1 escalation) and `synthetic_plan.md` (a 5-U-ID plan used as input).
- **Verification:** `make test` runs and passes the empty-but-real harness (asserts Hermes' tooling itself works before any logic is written).
- **Dependencies:** U-02.
- **Lane:** CD. **Size:** S. **Acceptance touched:** prerequisite for every other test.

### U-04 — Runtime config (`hermes.yaml` + `spine.mount`)
- **Approach:** Define the full config schema (Pydantic): tick rates, deadline thresholds per lane, channel routing, model preferences (Haiku for skill extraction, Sonnet for categoriser uncertainty), spine mount path, run-doc directory, audit log destination. Ship a default `hermes.yaml` with values from `STRATEGY.md` D7 (60 s / 5 min). The `spine.mount` file is a one-line declarative spec consumed by `seed_spine.sh` to bind-mount `portable-spine/SPINE.md` read-only at `/spine/SPINE.md`.
- **Verification:** Config schema validates the shipped default; mutation tests confirm rejection on bad values; `start.sh` aborts cleanly if `/spine/SPINE.md` is missing or writable.
- **Dependencies:** U-02.
- **Lane:** CD. **Size:** S. **Acceptance touched:** N1.A1 (spine immutability check), N4.A1 (handover root).

### U-05 — Cedar policy overlay (`hermes.cedar`)
- **Approach:** Write the three-tier overlay from `HERMES_RESEARCH_v1.md` §5.5: tier 1 read + comment + post auto-allow; tier 2 (dispatch / open-issue / request-review) requires analyst approve; tier 3 (merge_pr) requires arbiter approve + valid intent token + `production_lines_touched == 0`. Plus the absolute-deny block for `00_authority/`, `.env`, `host_shell`, `deploy_production`. Add a Cedar action registry under `src/hermes/security/actions.py` with the `forbidden` set per N1.A1.
- **Verification:** Cedar unit tests covering: every tier-1 action allowed; tier-2 without approval denied; tier-3 without token denied; tier-3 with token + arbiter allowed; absolute-deny block tested for each forbidden resource.
- **Dependencies:** U-04.
- **Lane:** CD. **Size:** M. **Acceptance touched:** N1.A1, N2.A1, N2.A2, N2.A3.

### U-06 — `agents/hermes/role.md`
- **Approach:** Write the role description: primary role (build coordination), session-scope declaration template ("this session, I will..."), pointer to `SPINE.md` for the soul, baton-pass discipline. Plus the schema for `agents/hermes/handovers/<timestamp>-<instance>.md`.
- **Verification:** The role file is what a fresh Hermes instance reads after `SPINE.md` and reproduces the orchestrator behaviour without ambient context (tested in U-N4.A1).
- **Dependencies:** U-01 (manifest entry).
- **Lane:** CD. **Size:** S. **Acceptance touched:** N4.A1.

### U-07 — Token-proxy connector
- **Approach:** Force every outbound LLM call through `cost-tools/token_proxy.py`. Centralise in `src/hermes/connectors/token_proxy.py` — every other module that needs an LLM imports `from .token_proxy import call`; direct `anthropic.AsyncAnthropic()` instantiation is banned via a flake8 plugin added in this U-ID.
- **Verification:** Static check (flake8 plugin) fires on any module that imports `anthropic` or `openai` directly outside this connector. Integration test calls Hermes' categoriser and asserts the proxy log shows the classification.
- **Dependencies:** U-04.
- **Lane:** CD. **Size:** S. **Acceptance touched:** N7.A1.

### U-08 — Entrypoint (`main.py`)
- **Approach:** Wires together: read SPINE → read `agents/hermes/` → acquire singleton lock (U-11) → start ticker (U-10) → start API server (U-30) → register signal handlers (SIGTERM → graceful drain → write handover → release lock). Logs structured to stdout for Beast/Loki.
- **Verification:** Smoke test starts main, sends SIGTERM, asserts handover file exists and lock is released.
- **Dependencies:** U-04, U-06.
- **Lane:** CD. **Size:** S. **Acceptance touched:** N4.A1.

### U-09 — State machine
- **Approach:** Pure-Python state machine for the U-ID lifecycle. States = enum; transitions = dict of `(state, event) → new_state`; invalid transitions raise `InvalidTransition`. Idempotency via event de-duplication on `(issue_id, event_type, payload_hash)`. No I/O — pure; tested in isolation. Linear sync is a separate adapter (U-27) that consumes state-machine outputs.
- **Verification:** Property tests (Hypothesis) covering: every valid path through the seven states reaches `merged`; every invalid (state, event) pair raises; replaying any sequence twice produces the same final state and the same set of side-effect events.
- **Dependencies:** U-03.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F1.A3, F1.A4.

### U-10 — Ticker (cron loop)
- **Approach:** Async loop with two cadences: 60 s when `mode=active`, 5 min when `mode=idle`. Each tick: pull events (Linear webhooks queued in Postgres + scheduled timers), pass to state machine, emit dispatches. Tick is interruptible via U-30's `/interrupt`.
- **Verification:** Test simulates 1 hour of synthetic events; assert tick interval matches mode; assert no event missed; assert clean shutdown on `/interrupt`.
- **Dependencies:** U-04, U-09.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F6.A1, F6.A2, F10.A3.

### U-11 — Singleton (Postgres advisory lock)
- **Approach:** `pg_try_advisory_lock(<hermes_role_namespace_id>)` on start. If lock held, exit 0 with the documented log line. Lock auto-releases on connection close (so a crashed Hermes' lock evaporates within Postgres' timeout). Heartbeat every 30 s confirms the holder is alive (visible in `/state` for ops).
- **Verification:** Integration test starts two Hermeses concurrently; asserts exactly one acquires; asserts the second exits 0; asserts that killing the first lets a third acquire within 60 s.
- **Dependencies:** U-04.
- **Lane:** CD. **Size:** M. **Acceptance touched:** N3.A1, N3.A2.

### U-12 — `channels.yaml` schema + loader
- **Approach:** Pydantic schema for channel routing: per-category, per-lane, primary + fallback. Loader caches at start and on SIGHUP reloads. Validator: every category referenced in `escalation/categoriser.py` must have a route here, fails build otherwise (CI-checked).
- **Verification:** Cross-reference test: every `EscalationCategory` enum value is routed.
- **Dependencies:** U-04.
- **Lane:** CD. **Size:** S. **Acceptance touched:** F4.A1–A6 (precondition).

### U-13 — Dispatch router
- **Approach:** Given a state-machine output `Dispatch{lane, payload, correlation_id}`, select the channel from `channels.yaml`, send via the right connector (U-14/U-15/U-16/U-29), log a `[HERMES-DISPATCH]` event with the correlation ID. Implements the fallback-on-5xx path for F2.A4.
- **Verification:** Tests with all four lanes; failure-injection on the primary channel verifies fallback.
- **Dependencies:** U-09, U-12.
- **Lane:** CD. **Size:** S. **Acceptance touched:** F2.A1, F2.A3, F2.A4.

### U-14 — Cursor daughter dispatcher
- **Approach:** Sends a structured task to a Cursor daughter (current convention: Linear comment + label change to `claimed-by:<daughter-id>`). Records claim conflicts (two daughters claim same issue → first wins, F2 acceptance).
- **Verification:** Test with two simulated daughters claiming the same issue; assert deterministic winner; assert loser receives `[HERMES-CLAIM-REJECTED]`.
- **Dependencies:** U-13, U-27.
- **Lane:** CD. **Size:** S. **Acceptance touched:** F2.A1.

### U-15 — DeepSeek-Critic dispatcher
- **Approach:** On `pr-open`, post a structured review request to the configured DeepSeek-Critic channel; await structured response (severity, findings, recommendations); transition state on response.
- **Verification:** Test with synthetic PR + canned critic response; assert transition to `review-done` with attached findings; assert deadline timer started per F3.
- **Dependencies:** U-13, U-28.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F2.A2 (critic part).

### U-16 — DeepSeek-Researcher dispatcher
- **Approach:** On `pr-open` events whose diff includes an import not in `agents/hermes/skills/known-imports.txt`, dispatch a research request alongside the critic dispatch.
- **Verification:** Test with PR diffs that do and don't introduce novel imports; assert dispatch fires only on novel ones; assert `known-imports.txt` is treated as the source of truth.
- **Dependencies:** U-13, U-26, U-28.
- **Lane:** CD. **Size:** S. **Acceptance touched:** F2.A2 (researcher part).

### U-17 — Deadline thresholds engine
- **Approach:** Reads per-lane thresholds from `hermes.yaml`; tracks per-edge timers in Postgres (so they survive crashes); fires nudges at threshold; second-nudge-without-progress promotes to escalation per F3.A3.
- **Verification:** Time-mocked tests covering: nudge fires once at threshold; structured "still working" reply resets; second nudge cycle → escalation; manual reset command works.
- **Dependencies:** U-09, U-04.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F3.A1, F3.A2, F3.A3, F3.A4.

### U-18 — Categoriser
- **Approach:** Given an event (state transition, finding, nudge breach), classify into one of the six categories. Mostly rule-based (Cedar-deny → `policy_violation`; high-severity finding from critic → `high_security_finding`; etc.). Falls back to a small Sonnet call (via U-07) on `unknown` + tags it as `unknown:llm-suggested:<category>` with confidence number per `OPINION_CONFIDENCE.md`.
- **Verification:** Unit tests for each rule; one integration test with the LLM fallback against synthetic ambiguous events.
- **Dependencies:** U-07.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F4.A1–A6 (categorisation).

### U-19 — Escalation routes
- **Approach:** Given a categorised escalation, look up the route in `channels.yaml`, send via the right connector with the correct payload shape per category (security findings carry CWE field; cross-unit conflicts carry the conflicting U-IDs; etc.). Implements the multi-channel fallback chain for security pages (F4.A6).
- **Verification:** End-to-end test for each category with mocked channels; asserts ack semantics (no ack → fallback).
- **Dependencies:** U-12, U-13, U-18.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F4.A1–A6, F9.A2.

### U-20 — Episodic memory (SQLite)
- **Approach:** SQLAlchemy model for the `episodic` table per `01_truth/hermes_architecture_design.md`: `id, timestamp, run_id, observation, action_taken, payload_json`. Use Nous Hermes' built-in FTS5 wiring; if not auto-set, add an `episodic_fts` virtual table with `content=episodic` and triggers.
- **Verification:** Insert 10k synthetic events; FTS5 query returns expected matches in < 100 ms.
- **Dependencies:** U-04.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F7.A1, F7.A3.

### U-21 — Decisions table
- **Approach:** Same pattern, table = `decisions` with `id, timestamp, decision, rationale, alternatives_rejected, run_id, confidence_band`. Confidence band per `OPINION_CONFIDENCE.md` 50/85/95 thresholds.
- **Verification:** Schema test; insert + retrieve sample decisions; confidence-band enum enforced.
- **Dependencies:** U-04, U-20.
- **Lane:** CD. **Size:** S. **Acceptance touched:** F7.A1.

### U-22 — Intent-token table + verifier
- **Approach:** `intent_tokens` table: `token_id, scope, issued_by, issued_at, expires_at, revoked_at`. Verifier: takes `(action, resource, token_id)`, checks scope match + not expired + not revoked. Antigravity issues tokens via a small CLI (`hermes-token issue --scope=... --ttl=24h`); revocation via the same CLI.
- **Verification:** Token round-trip test; expiry test; scope-mismatch test; revoked-token test.
- **Dependencies:** U-05, U-04.
- **Lane:** CD. **Size:** M. **Acceptance touched:** N2.A1, N2.A2.

### U-23 — Postgres flush
- **Approach:** At run end, push episodic + decisions tables to Postgres on Beast (the `hermes` schema Devon provisions). Idempotent: uses (run_id, seq) as natural key on insert. SQLite is the hot store; Postgres is the durable warehouse.
- **Verification:** Flush twice → no duplicate rows; flush after partial flush (mid-network failure) resumes from last successful seq.
- **Dependencies:** U-20, U-21.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F7.A2, F7.A4.

### U-24 — Run-doc writer
- **Approach:** Append-only writer for `03_shadow/hermes-runs/<run-id>.md`. Writes YAML frontmatter at run start; one block per event; `fsync()` after each write; final summary section at `/stop`. File handle held for run lifetime; rotated on run boundary.
- **Verification:** Crash-mid-write test (kill -9 the process during an `os.write`) and assert the file is parseable up to the last fully-written event.
- **Dependencies:** U-04.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F5.A1, F5.A2, F5.A3, F5.A4.

### U-25 — Skill extractor
- **Approach:** At `/stop`, read the run-doc, prompt Haiku (via U-07) with: "given this run, did Hermes solve a recurring problem worth becoming a reusable skill?" Output schema: `{trigger, action, why_it_worked, when_not_to_use, confidence, supporting_seqs}`. Writes candidates to `agents/hermes/skills/<slug>-candidate.md` per F8.A3.
- **Verification:** Two synthetic runs: one obviously compoundable (same nudge pattern resolved twice) → produces a candidate; one with no novelty → produces none. Both attribution-complete.
- **Dependencies:** U-07, U-24.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F8.A1, F8.A2, F8.A3.

### U-26 — Known-imports tracker
- **Approach:** A list (text file + Python helper) of imports Hermes has already seen via researcher passes. Seeded with stdlib + project deps. Updated by U-25's compounding loop when a researcher pass concludes.
- **Verification:** Round-trip: researcher pass on `import scipy` writes `scipy` to the file; next time the same import appears, no researcher dispatch.
- **Dependencies:** U-25.
- **Lane:** CD. **Size:** S. **Acceptance touched:** F2.A2 (researcher trigger).

### U-27 — Linear connector
- **Approach:** Extends `clean-build/hetzner_deployment/linear_reporter.py` (which already creates issues): adds `update_state`, `add_comment`, `add_label`, `webhook_handler`, `poll_reconcile`. Webhook handler verifies signature; reconciler polls every 5 min in case webhooks are dropped.
- **Verification:** Webhook fixture test; signature verification test; reconciler dedupe test; idempotency test (replay same webhook twice).
- **Dependencies:** U-09.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F1.A1, F1.A2, F1.A4.

### U-28 — GitHub connector
- **Approach:** Webhook handler for PR events (opened, ready_for_review, labelled, merged); diff fetch via `gh` CLI authenticated by the runtime's GitHub App credential; repo scope limited to `Amplified-Partners/clean-build` for v1.
- **Verification:** Webhook fixture test; diff parser test (pulls imports correctly across .py and .ts files); scope test (a webhook from a different repo is rejected).
- **Dependencies:** U-09.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F2.A2, F1.A2.

### U-29 — Slack + Telegram + WhatsApp connectors
- **Approach:** Three small adapters with a shared interface (`send(channel, payload, correlation_id)`). Slack via webhook URL; Telegram via bot API; WhatsApp via the existing `clean-build/evolution-api/webhook-dispatcher.py` — add a dispatcher rule for `@hermes` that routes to Hermes' API at `hermes.internal/task`. Per F9.A3, this is the only WhatsApp-side change.
- **Verification:** Three connector unit tests; one integration test for the `@hermes` dispatcher rule against the existing Evolution API.
- **Dependencies:** U-13, plus existing `clean-build/evolution-api/`.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F9.A1, F9.A2, F9.A3, F9.A4.

### U-30 — FastAPI server (`/task /state /interrupt /health /metrics`)
- **Approach:** Five endpoints, mTLS or header-key auth via U-31, audit middleware via U-32, OpenAPI spec generated and committed to `01_truth/interfaces/hermes_api_v1.md`. `/health` reports per-dependency status; `/state` dumps current run + outstanding escalations; `/interrupt` halts within one tick; `/metrics` Prometheus format.
- **Verification:** Schemathesis fuzz test against the live spec; `/health` returns 503 if Postgres is down (verified by failure-injection); `/interrupt` test asserts halt within one tick.
- **Dependencies:** U-08, U-10.
- **Lane:** CD. **Size:** L → split into U-30a (server skeleton + `/health` + `/state`) and U-30b (`/task` + `/interrupt` + `/metrics`).
- **Acceptance touched:** F10.A1, F10.A2, F10.A3.

### U-31 — Auth
- **Approach:** mTLS for service-to-service on `amplified-net`; header-key (HMAC-signed) for human/agent calls from outside. Both checked against the principal table; principal feeds into Cedar context.
- **Verification:** Unit tests for both modes; failed-auth test confirms 401 + audit row.
- **Dependencies:** U-30, U-05.
- **Lane:** CD. **Size:** M. **Acceptance touched:** F10.A4 (auth row), N2.A3 (Cedar principal).

### U-32 — Audit middleware + e2e proving run
- **Approach:** Middleware writes an audit row on every authenticated call: `(timestamp, principal, action, resource, allow_or_deny, cedar_decision_id, http_status)`. Plus the **end-to-end proving test**: a synthetic 5-U-ID plan run from start to `merged`, with one injected nudge, one injected security finding, one Cedar tier-3 attempt, and a mid-run kill. Asserts: all 60 acceptance tests pass; one candidate skill extracted; signature linter clean.
- **Verification:** The e2e test is the gate. If it passes, Hermes v1 is *built* (still needs the proving run on real work for promotion per N9).
- **Dependencies:** all previous U-IDs.
- **Lane:** CD. **Size:** L. **Acceptance touched:** F10.A4 + every other test (e2e).

### Optional: U-33 — Promotion-gate dossier
- **Approach:** After the real proving run (Vellum Phase 1 or substitute), write the promotion dossier: signed checklist against `00_authority/PROMOTION_GATE.md`; index updates to `MANIFEST.md` (Authoritative now); `DECISION_LOG.md` entry signed by Antigravity + Ewan.
- **Verification:** Bibliography integrity check; `MANIFEST.md` v57 entry; `DECISION_LOG.md` signed.
- **Dependencies:** U-32 + one real run.
- **Lane:** AG (with CD assist). **Size:** S. **Acceptance touched:** N9.A1.

## §3. Review pass rules (DeepSeek-Critic)

For each PR:

- **Pass 1 — Spine congruence.** Does the PR violate any line in `portable-spine/SPINE.md`? Common breaks: writing outside `agents/<name>/` or `02_build/hermes/` from inside a daughter; introducing a "must not" or hedging restriction (Eight Laws don't add new restrictions in code); skipping the BATON; missing signature.
- **Pass 2 — Acceptance coverage.** Does the PR include the tests for the U-ID's named acceptance criteria? Every `F*.A*` and `N*.A*` referenced in the U-ID block must have at least one test in the PR.
- **Pass 3 — Security.** Cedar policy unchanged unless this is U-05; secrets not committed; `gitignore` covers `state/`, `.env`, any token files; auth not bypassed.
- **Pass 4 — Cost.** All LLM calls go through `connectors/token_proxy.py`; flake8 plugin from U-07 didn't get disabled.
- **Pass 5 — Idempotency.** State-changing actions are de-duplicated on a stable key; webhook handlers tolerate replay.

Findings format: severity (`low / medium / high / critical`), pass-number, file:line, suggested fix. High and critical findings escalate per F4 (synthesiser triages, Ewan paged on critical).

## §4. Synthesiser triage (Perplexity Computer / Claude session)

When Hermes is not yet alive (U-01 through U-29), I (the synthesiser) take findings in a single sweep:
- Critical/high → halt PR, fix with daughter or Devon, re-review.
- Medium → comment, daughter amends in same PR.
- Low → accept-with-followup-issue.

Once **U-30 is merged**, Hermes can take over the dispatch + nudge layer for U-31 and U-32. He uses real specialists (real Cursor daughters, real DeepSeek-Critic) on his own remaining work. This is the moment Hermes-the-builder *becomes* Hermes-the-coordinator. Every event from U-30 onward lives in the first run-doc: `03_shadow/hermes-runs/2026-05-XX-hermes-self-build_v1.md`.

## §5. Dependency graph (build order)

```
U-01 (authority) ─────────┐
                          ├── U-02 (container) ──┬── U-03 (test harness) ──┐
                          │                       │                          │
                          ├── U-04 (config) ──────┼── U-05 (Cedar) ─────────┤
                          │                       │                          │
                          ├── U-06 (role.md) ─────┘                          │
                          │                                                   │
                          ├── U-07 (token-proxy) ────────────────────────────┤
                          │                                                   │
                          └── U-08 (main) ──── U-11 (singleton) ─────────────┤
                                                                              │
   U-09 (state machine) ──┬── U-10 (ticker) ──┬── U-13 (dispatch router) ──┬─┤
                           │                    │                           │ │
                           ├── U-17 (deadlines)─┘                           │ │
                           │                                                 │ │
                           ├── U-20 (episodic) ─┬── U-23 (flush) ─────────┤ │
                           │                    │                           │ │
                           ├── U-21 (decisions)─┘                           │ │
                           │                                                 │ │
                           └── U-22 (intent tokens) ────────────────────────┤ │
                                                                              │ │
   U-12 (channels.yaml) ──── U-18 (categoriser) ──── U-19 (routes) ─────────┤ │
                                                                              │ │
   U-14 (CD dispatcher) ────────────────────────────────────────────────────┤ │
   U-15 (DC dispatcher) ────────────── U-28 (GitHub) ────────────────────── ┤ │
   U-16 (DR dispatcher) ────── U-26 (known-imports) ── U-25 (skill extract)─┤ │
                                                          │                  │ │
   U-24 (run-doc) ─────────────────────────────────────── ┘                  │ │
                                                                              │ │
   U-27 (Linear) ──────────────────────────────────────────────────────────  ┤ │
   U-29 (Slack/TG/WhatsApp) ────────────────────────────────────────────────┤ │
                                                                              ▼ │
                                                                          U-30 (API)
                                                                              │   │
                                                                          U-31 (auth)
                                                                              │
                                                                          U-32 (audit + e2e)
                                                                              │
                                                                          U-33 (promotion dossier, optional)
```

The **hot path** for the e2e test (U-32) is: U-01 → U-02 → U-03 → U-04 → U-09 → U-10 → U-11 → U-20 → U-24 → U-30 → U-32. Other U-IDs can be parallelised by independent daughters.

## §6. What Cursor daughters do, in order

Daughters claim from Linear (issues labelled `unblocked`). They:

1. Read the Linear issue (the U-ID block).
2. Read the named files in §1.1 of this plan that they will modify.
3. Read the linked acceptance tests in `hermes-requirements.md`.
4. Branch: `feature/hermes-U-NN-<slug>` from `main`.
5. Write tests **first** (the acceptance tests named in the U-ID).
6. Make tests pass.
7. Run the full suite (`make test`) — must pass.
8. Open PR titled `[HERMES] U-NN: <slug>` referencing the Linear issue.
9. Sign per `00_authority/SIGNATURES.md`.
10. Linear label flips to `pr-open` (Hermes does this once alive; until then, daughter does it).
11. Wait for review. Address findings. Merge once green and approved.

## §7. Done means

Hermes v1 is **built** when:
- All 33 U-IDs (32 + optional 33) are merged.
- U-32's e2e test passes in CI.
- A real proving run has been coordinated by Hermes himself (Vellum Phase 1 or a smaller substitute).
- U-33's promotion dossier is signed by Antigravity + Ewan.

Hermes v1 is **promoted to authority** when `MANIFEST.md` v57 indexes him under "Authoritative now" and `DECISION_LOG.md` records the signed promotion. Until then, he runs from `03_shadow/`.

## Sign-off

`[CURRENT BEST EVIDENCE]` — promotion to authority requires Antigravity arbiter pass + Ewan signature on STRATEGY D1–D10.

Signed-by: Perplexity Computer | 2026-05-09 | session 2026-05-08-hermes-research
Parent: `02_build/hermes/docs/brainstorms/hermes-requirements.md` v1
Ready for: DeepSeek-Researcher scaffold pass (§1).
