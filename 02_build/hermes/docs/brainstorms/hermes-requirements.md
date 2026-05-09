---
title: Amplified Hermes — Requirements (what good looks like)
date: 2026-05-09
version: 1
status: draft
parent: 02_build/hermes/STRATEGY.md
audience: Antigravity (arbiter pass), Cursor daughters (build target), Ewan (final review)
ce_phase: Plan (40%)
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

This document defines, atomically, what Amplified Hermes v1 must do, with each requirement tied to an acceptance test, observable signals, and known failure modes. It is the contract. The plan (next artefact) decomposes these into U-IDs daughters can build against.

Every requirement here:

- has an ID (`F` for functional, `N` for non-functional)
- has at least one **acceptance test** that can be written before the code
- names the **observable signal** (what we look at to know it works in the wild)
- names the **failure modes** we expect, with the routing for each

## Functional requirements

### F1 — Owns the work board (Linear state machine)

**What:** Hermes opens, advances, and closes Linear issues representing build work units (U-IDs). Each issue moves through `open → claimed → pr-open → review-pending → review-done → ready-to-merge → merged`.

**Acceptance tests:**
- F1.A1 Given a plan file with N U-IDs, on first wake Hermes creates exactly N Linear issues with title `[HERMES-RUN-<id>] U-NN: <slug>`, labelled by dependency state (`unblocked` or `blocked-by-U-NN`).
- F1.A2 When a Cursor daughter opens a PR referencing `U-NN`, Hermes transitions the issue from `claimed` to `pr-open` within one tick.
- F1.A3 An issue cannot skip a state. Attempts to (e.g. `open → pr-open`) are rejected and logged as `[HERMES-INVALID-TRANSITION]` events.
- F1.A4 State changes are idempotent: replaying the same webhook event twice produces exactly one Linear update.

**Observable signal:** Linear issue list filtered by `[HERMES-RUN-<id>]`; states match plan; no `[HERMES-INVALID-TRANSITION]` errors in the run-log.

**Failure modes:**
- Linear API outage → retry with exponential backoff, surface as a Slack `#hermes-ops` warning after 3 failed retries; do not block other issues.
- Webhook drops → reconcile via `GET /issues` poll on each tick.
- Two Hermeses fighting over the same issue → impossible by N3 (singleton lock).

---

### F2 — Dispatches specialists

**What:** When an issue becomes unblocked, Hermes pings the right specialist for that lane. Routing rules live in `02_build/hermes/config/channels.yaml` and follow the agent roster in `clean-build/00_authority/AGENT_ROUTING.md`.

**Acceptance tests:**
- F2.A1 An `open` issue with no unmet dependencies is dispatched to a Cursor daughter via the configured channel within one tick.
- F2.A2 A `pr-open` event triggers a dispatch to DeepSeek-Critic; if the PR diff includes a previously-unseen external library import (heuristic: import path not in `agents/hermes/skills/known-imports.txt`), DeepSeek-Researcher is also dispatched.
- F2.A3 A dispatch records `dispatched_to`, `dispatched_at`, `channel`, `correlation_id` in the run-log.
- F2.A4 If a specialist is configured but unavailable (channel returns 5xx), Hermes attempts the configured fallback before escalating.

**Observable signal:** Run-log shows `[HERMES-DISPATCH]` events with correlation IDs that match later `[HERMES-RECEIVED]` events from specialists.

**Failure modes:**
- All channels for a lane down → escalate per F4.
- Specialist accepts but never replies → handled by F3 (deadlines).
- Two daughters claim the same issue → first claim wins, second receives a `[HERMES-CLAIM-REJECTED]` reply with the winner's ID.

---

### F3 — Watches deadlines

**What:** Hermes enforces three time-based rules: `claimed → pr-open` ≤ 90 min, `pr-open → review-done` ≤ 30 min after dispatch to critic, any single edge blocked > 2 h triggers escalation. These thresholds are per-lane configurable.

**Acceptance tests:**
- F3.A1 An issue in `claimed` for > 90 min without a PR triggers exactly one nudge (per the configured nudge channel) and one `[HERMES-NUDGE]` run-log event.
- F3.A2 A second nudge does not fire on the same issue until either the state advances or a manual `/hermes reset-nudge U-NN` command is received.
- F3.A3 Two consecutive nudge cycles without progress on the same edge promote the situation to escalation per F4 (this is the "two attempts → stop" rule from `SPINE.md` § STUCK).
- F3.A4 Thresholds are per-lane: a daughter doing infra work might get 180 min; a critic doing a security pass gets 30 min; values come from `config/hermes.yaml`, not hard-coded.

**Observable signal:** Run-log nudge events with timestamps; `hermes.deadline_breach_total` counter exposed at `/metrics`.

**Failure modes:**
- Clock skew on Beast → use UTC + monotonic clocks; deadlines stored as absolute UTC timestamps.
- Specialist replies "still working" → resets the nudge timer if response is structured (`{"status":"working","eta_minutes":N}`); otherwise treated as silence.

---

### F4 — Escalates by category

**What:** Hermes routes escalations by category, never by drama. Categories: `routine_progress`, `cross_unit_conflict`, `high_security_finding`, `customer_facing`, `policy_violation`, `unknown`.

**Acceptance tests:**
- F4.A1 `routine_progress` → Linear comment on the relevant issue; no human ping.
- F4.A2 `cross_unit_conflict` (e.g. PR for U-7 invalidates U-11's stated assumptions) → page synthesiser via the configured channel; halt affected U-IDs in `paused` substate until resolution.
- F4.A3 `high_security_finding` → page Ewan immediately on his configured channel (Telegram / WhatsApp), include CVE/CWE if known, halt the affected PR.
- F4.A4 `customer_facing` or any change touching the outside world → page Ewan; do not auto-merge regardless of Cedar tier-3 token state. (Per Eight Laws Law 5 and `00_authority/OPINION_CONFIDENCE.md` 95% threshold.)
- F4.A5 `policy_violation` (Cedar deny) → halt the action, log `[HERMES-CEDAR-DENY]`, page Antigravity.
- F4.A6 `unknown` → park to OpenClaw with full context and stateless handover packet per `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`.

**Observable signal:** Each escalation carries `category`, `routed_to`, `ack_received_at`. Outstanding escalations visible at `/state`.

**Failure modes:**
- No ack from Ewan within 15 min on a `high_security_finding` → second-channel page (e.g. fallback from Telegram to WhatsApp); after 30 min total, fall back to OpenClaw with `urgent` flag.
- Wrong category assigned by Hermes → reviewable via the run-log; correctable post-hoc via `/hermes recategorise <event_id> <new_category>`; mistake feeds Compound (F8) so the heuristic improves.

---

### F5 — Logs everything to a run-doc

**What:** Every dispatch, finding, state transition, nudge, escalation, and merge appends an event to a single per-run markdown file at `clean-build/03_shadow/hermes-runs/<run-id>.md`. Format is structured (YAML frontmatter + sequential event log + final summary section).

**Acceptance tests:**
- F5.A1 The run-doc is created at run start with frontmatter (`run_id`, `started_at`, `plan_path`, `hermes_instance` e.g. `Hermes-7019`).
- F5.A2 Every event is append-only; no edit-in-place. Events have a `seq` counter, ISO-8601 timestamp, type, payload.
- F5.A3 The run-doc is fsync'd on every write; a crash mid-write leaves the file valid up to the last fully-written event.
- F5.A4 At run end, Hermes writes a summary section (counts per category, candidate skills extracted, parking notes if any) and signs it per `00_authority/SIGNATURES.md`.

**Observable signal:** `ls 03_shadow/hermes-runs/` shows one file per run; `wc -l` matches `seq` count; final summary parses as YAML.

**Failure modes:**
- Disk full → escalate per F4 (`policy_violation`-like), pause new dispatches, keep accepting `interrupt`.
- Concurrent writes → impossible by N3 (singleton).
- Bad UTF-8 in a payload from a daughter → escape and continue; never crash on input.

---

### F6 — Knows when to stop

**What:** When all U-IDs reach `merged` and the configured "round-trip green" check passes (e.g. CI on `main`), Hermes posts a summary, closes the run-doc, fires the Compound phase (F8), and pages the synthesiser for review.

**Acceptance tests:**
- F6.A1 Stop is detected within one tick of the last `merged` transition + green check.
- F6.A2 Stop sequence: write summary → invoke skill_extractor (F8) → notify synthesiser → enter `idle` mode (5 min tick).
- F6.A3 No new dispatches occur after stop until a new run is initialised.

**Observable signal:** Run-doc has a `summary` section; Hermes' `/state` reports `mode: idle`.

**Failure modes:**
- "Round-trip green" never goes green → Hermes does not stop; this is correct behaviour; eventually F4 escalates the stuck PR rather than auto-stopping.

---

### F7 — Persistent memory across sessions

**What:** Hermes stores episodic events, decisions, and active intent tokens in SQLite under `02_build/hermes/state/hermes.sqlite`. The Nous Hermes runtime provides FTS5 indexing over the episodic table. On flush, durable rows go to Postgres on Beast.

**Acceptance tests:**
- F7.A1 SQLite schema matches `01_truth/hermes_architecture_design.md` (episodic, decisions, intent_tokens) — verified by integration test with synthetic data.
- F7.A2 Restarting the container preserves all three tables; the new instance reads them on wake.
- F7.A3 FTS5 query over episodic returns matching events for "what did Hermes do about U-7 last Tuesday?" semantic-equivalent queries.
- F7.A4 Postgres flush happens on run end (F6) and is idempotent — running it twice produces no duplicates.

**Observable signal:** Two databases exist with consistent row counts; FTS5 query latency < 100 ms on typical run sizes.

**Failure modes:**
- SQLite corruption → restore from latest Postgres flush; replay events from run-doc since last flush.
- Postgres unavailable on flush → retry with backoff; queue locally; never block the run.

---

### F8 — Skill creation + self-improvement

**What:** At run end (F6), `skill_extractor.py` reads the run-doc and asks a small LLM (Haiku via `cost-tools/token_proxy.py`) whether Hermes solved a recurring problem worth turning into a reusable skill. Candidates land in `agents/hermes/skills/<slug>-candidate.md` for OpenClaw's weekly review.

**Acceptance tests:**
- F8.A1 Given a synthetic run-doc with a known compoundable pattern, the extractor produces a candidate skill in the agreed schema (trigger, action, why-it-worked, when-not-to-use).
- F8.A2 No candidate is produced when nothing novel happened (extractor must distinguish — false positives are worse than false negatives).
- F8.A3 Candidates carry full attribution: source run-id, source events (by `seq`), extracting-Hermes-instance, model used.
- F8.A4 OpenClaw's promotion or rejection is recorded; rejected candidates move to `_rejected/` with a one-line reason.
- F8.A5 On wake, Hermes loads all approved skills as part of his Layer 2 config.

**Observable signal:** `agents/hermes/skills/` grows over time; ratio of approved : rejected is tracked in `/metrics`.

**Failure modes:**
- Extractor LLM hallucinates a skill from noise → rejection rate climbs; this is the signal; revise the extractor prompt as part of next Compound cycle.
- Approved skill turns out to be wrong in production → demote via PR; record the demotion as a negative signal per slime-mold learning in `ONBOARDING.md`.

---

### F9 — Multi-channel notifications

**What:** Hermes can reach Linear, Slack, Telegram, and WhatsApp (via `clean-build/evolution-api/`). Routing rules per category in `config/channels.yaml`. iMessage is explicitly v2.

**Acceptance tests:**
- F9.A1 Each channel has a configured `send()` and a configured `receive()` (where applicable: Linear webhook, Slack webhook, Telegram bot, Evolution API webhook).
- F9.A2 A `high_security_finding` page reaches Ewan on his primary channel within 30 s of categorisation in the happy path.
- F9.A3 WhatsApp messages prefixed `@hermes` route through the existing dispatcher in `clean-build/evolution-api/webhook-dispatcher.py`. Dispatcher rule for `@hermes` is added in this build.
- F9.A4 Each outbound message carries a correlation ID matching the originating run-log event.

**Observable signal:** Per-channel send/receive counts at `/metrics`; correlation IDs traceable end-to-end.

**Failure modes:**
- Channel down → fallback chain per F4.A6.
- Message rate-limited → respect the platform's rate limit; queue; do not retry-storm.

---

### F10 — Health endpoint and audit log

**What:** A FastAPI service exposes `POST /task`, `GET /state`, `GET /health`, `POST /interrupt`, `GET /metrics`. mTLS or header-key auth. Full audit trail written to the run-doc and to a separate immutable audit log in Postgres.

**Acceptance tests:**
- F10.A1 OpenAPI spec lives at `01_truth/interfaces/hermes_api_v1.md`; the live service matches it (verified by Schemathesis-style fuzz test).
- F10.A2 `GET /health` returns 200 + JSON when all dependencies are reachable; 503 otherwise; never hangs.
- F10.A3 `POST /interrupt` halts the current loop within one tick and writes a `[HERMES-INTERRUPTED]` event with the caller's identity.
- F10.A4 Every authenticated call writes an audit row with `(timestamp, principal, action, resource, allow_or_deny, cedar_decision_id)`.

**Observable signal:** `/health` green; audit row count grows monotonically; sample audit rows match Cedar log decisions.

**Failure modes:**
- Auth bypass attempt → Cedar denies, audit row written, Antigravity paged per F4.A5.
- API down → Hermes still runs his loop; only external control surface is degraded; surfaced via `/metrics` scraped by Prometheus.

---

## Non-functional requirements

### N1 — Layer 0 immutable

**What:** The Eight Laws and RODS are enforced in code, not just convention. Disallowed operations cannot be invoked even with a valid Cedar token.

**Acceptance test:** N1.A1 The action registry in `actions.py` includes a `forbidden` set covering Eight Laws Law 1 (no harm), Law 2 (no HR), Law 3 (no telling people off). Any registered action that would invoke a forbidden category fails closed at registration time, not at call time.

**Source:** `00_authority/EIGHT_LAWS.md`; `portable-spine/SPINE.md` § RODS.

---

### N2 — IBAC-gated

**What:** Every outbound action is checked against `02_build/hermes/config/policies/hermes.cedar` (overlay on `hetzner_deployment/policies/prod.cedar`) before execution. Three Cedar tiers; tier 3 also requires a valid intent token.

**Acceptance tests:**
- N2.A1 A tier-3 action without a valid intent token is denied; audit row written.
- N2.A2 A tier-3 action with a token issued by Antigravity, scoped to that resource, within 24 h, is allowed.
- N2.A3 Cedar policy file is read-only to Hermes; any attempt by Hermes to write the policy file is denied at the filesystem layer (not just at Cedar).

**Source:** `01_truth/hermes_architecture_design.md` § IBAC; `hetzner_deployment/policies/prod.cedar`.

---

### N3 — Singleton with crash safety

**What:** At most one Hermes instance can hold the build-coordinator role at any time, enforced by a Postgres advisory lock. Crash recovery: on start, the new instance reads the latest run-doc + database, resumes the run from the last persisted state, and posts a `[HERMES-RESUMED]` event.

**Acceptance tests:**
- N3.A1 Starting a second container while one holds the lock → the second container exits 0 with `[HERMES-LOCK-HELD]` log line; no Linear or channel writes.
- N3.A2 Killing the active container mid-run → next container resumes within 30 s, no events lost, no events duplicated (idempotent state machine per F1.A4).

---

### N4 — Stateless handover

**What:** Every wake reads `portable-spine/SPINE.md` then `agents/hermes/`. Every sleep updates `agents/hermes/handovers/<timestamp>-<instance>.md`. The next Hermes instance resumes at full speed without ambient context.

**Acceptance test:** N4.A1 A simulated cold-start (delete process, keep filesystem + database) produces a Hermes who picks up the run within 30 s and whose first action matches the parked plan from the previous handover.

**Source:** `portable-spine/SPINE.md` § BATON; `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md`.

---

### N5 — Privacy first

**What:** No client PII enters Hermes' core. Tokenised at the edge per `00_authority/SKILL_EXECUTION.md` § Shadow-First & Privacy-First. Working memory is purged at task completion unless a downstream skill explicitly needs the trace.

**Acceptance tests:**
- N5.A1 Static check: `grep -r` for known PII patterns in any persisted database returns zero.
- N5.A2 The audit log captures *who said* a thing, not *what they said*, when the payload contains PII tokens.

---

### N6 — Radical Attribution

**What:** Every Hermes-authored artefact (Linear comment, run-doc, skill, audit row) is signed in the `Hermes-NNNN | YYYY-MM-DD | session <id>` form per `00_authority/SIGNATURES.md`.

**Acceptance test:** N6.A1 No artefact written by Hermes is missing the signature footer; verified by the existing signature linter in `.github/workflows/pr-validation.yml` (extended for Hermes paths).

---

### N7 — Cost-bounded

**What:** Every LLM call from Hermes routes through `cost-tools/token_proxy.py`. The skill-extractor uses Haiku-tier by default; only categorisation uncertainty escalates to Sonnet.

**Acceptance test:** N7.A1 Integration test verifies all calls have `ANTHROPIC_BASE_URL=http://token-proxy:8088` and that the proxy logs show classification decisions for each call.

**Source:** `01_truth/SYSTEMS-AND-API-REGISTER.md` § cost-tools; `02_build/INFRASTRUCTURE.md` § AI/ML services.

---

### N8 — Observable

**What:** All actions emit Langfuse traces with the run-id as the trace name. Container metrics are scraped by Prometheus on Beast. A Grafana dashboard at `monitoring.internal/d/hermes` is provisioned.

**Acceptance tests:**
- N8.A1 A simulated run produces a single Langfuse trace with all child spans linked.
- N8.A2 Prometheus has live scrape targets for `hermes:9100/metrics` reporting at minimum: `hermes_dispatches_total`, `hermes_nudges_total`, `hermes_escalations_total{category}`, `hermes_deadline_breach_total`, `hermes_skill_candidates_total`.

---

### N9 — Reversible (lives in shadow until proven)

**What:** Hermes v1 lives in `clean-build/03_shadow/hermes-runs/` for at least one full proving run before promotion. Promotion requires `00_authority/PROMOTION_GATE.md` checks pass, signed by Antigravity + Ewan.

**Acceptance test:** N9.A1 The PROMOTION_GATE checklist is documented in the v1 plan and is the explicit gate between "v1 done" and "indexed in MANIFEST.md as Authoritative now".

---

### N10 — Portable + crash-safe deployment

**What:** Lives behind Traefik on Beast at `hermes.internal`. Docker-composed. State on Postgres + SQLite (the SQLite file is on a Beast-backed-up volume). One-command deploy, one-command rollback.

**Acceptance tests:**
- N10.A1 `make deploy` brings up a clean Hermes from a tagged image.
- N10.A2 `make rollback` returns to the previously-tagged image with state preserved.
- N10.A3 Beast reboot → Hermes auto-starts and resumes within 60 s of the host being up.

---

## Out-of-band items the requirements depend on

These exist already, but Hermes' acceptance tests assume them:

- `cost-tools/token_proxy.py` — running on Beast as `token-proxy` per `MANIFEST.md` v55.
- `clean-build/evolution-api/` — running, with the existing dispatcher pattern.
- `hetzner_deployment/policies/prod.cedar` — the tier-1/2/3 base policy.
- `clean-build/.github/workflows/pr-validation.yml` — extended to lint Hermes paths.
- Postgres on Beast with a `hermes` schema (added by Devon at deploy time).

If any of those is not in the state described here, the v1 plan flags it as a `[BLOCKER]` U-ID rather than working around it silently.

## Acceptance summary (the contract daughters build to)

| ID | Requirement | Acceptance count | Highest-leverage test |
|---|---|---|---|
| F1 | Linear state machine | 4 | F1.A1 (issue creation matches plan exactly) |
| F2 | Dispatch | 4 | F2.A2 (researcher invoked on novel imports) |
| F3 | Deadlines | 4 | F3.A3 (two-attempts → escalate) |
| F4 | Escalation by category | 6 | F4.A3 (security finding pages Ewan) |
| F5 | Run-doc | 4 | F5.A3 (crash-safe append) |
| F6 | Stop detection | 3 | F6.A2 (stop sequence ordering) |
| F7 | Persistent memory | 4 | F7.A2 (restart preserves state) |
| F8 | Skill extraction | 5 | F8.A2 (no false-positive skills) |
| F9 | Channels | 4 | F9.A3 (`@hermes` WhatsApp routing) |
| F10 | API + audit | 4 | F10.A4 (audit row per call) |
| N1 | Layer 0 enforced in code | 1 | N1.A1 (registration-time check) |
| N2 | IBAC | 3 | N2.A2 (tier-3 with token allowed) |
| N3 | Singleton + crash safety | 2 | N3.A2 (crash mid-run resumes) |
| N4 | Stateless handover | 1 | N4.A1 (cold start within 30 s) |
| N5 | Privacy | 2 | N5.A1 (no PII in databases) |
| N6 | Attribution | 1 | N6.A1 (signature linter) |
| N7 | Cost | 1 | N7.A1 (proxy classification) |
| N8 | Observability | 2 | N8.A2 (Prometheus targets live) |
| N9 | Reversible | 1 | N9.A1 (PROMOTION_GATE in plan) |
| N10 | Deployment | 3 | N10.A3 (auto-resume after reboot) |

Total: 60 acceptance tests across 20 requirements. The v1 plan turns these into U-IDs.

## Sign-off

`[CURRENT BEST EVIDENCE]` — promotion to authority requires Antigravity arbiter pass + Ewan signature.

Signed-by: Perplexity Computer | 2026-05-09 | session 2026-05-08-hermes-research
Parent: `02_build/hermes/STRATEGY.md` v1
For Antigravity arbiter pass before plan is opened.
