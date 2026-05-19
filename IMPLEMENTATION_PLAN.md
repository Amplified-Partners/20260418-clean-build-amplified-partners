---
title: Integrated Architecture — Implementation Plan
date: 2026-05-19
version: 2
status: draft — awaiting Ewan review
revision-note: v2 incorporates DeepSeek V4 review corrections (P0 definition, route terminology, Vellum receipt prior art)
epistemic_tier: STRUCTURED
signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
source: Amplified Integrated Architecture Handoff (Antigravity synthesis, May 2026)
---

# Integrated Architecture — Implementation Plan

## Executive Summary

The ingestion pipe is done. The task is to apply sensors — wire epistemic validation, Vellum listening, Brain MCP guardrails, and make downstream consumers (marketing, sidecar, research) use shared substrate rather than creating parallel systems.

This plan maps what already exists in `clean-build`, identifies duplication risks, and proposes an 8-PR incremental sequence. No code changes until Ewan approves.

**Prior art (live):** Porch-to-Brain bridge v3 is running on Beast with Vellum JSONL receipts (`/opt/amplified/logs/vellum_porch.jsonl`). Every porch route decision, quarantine, ingest start/complete/fail emits a receipt. This is the starting pattern for PR 5's formalised VellumEvent model.

---

## 1. Existing Repo Findings

### 1.1 What Already Exists (repo-grounded)

| Component | Location | Status | Lines | Tests |
|-----------|----------|--------|-------|-------|
| **Epistemic Status (Layer 0)** | `02_build/routing/epistemic_status.py` | Working — 543 lines, stdlib-only | 543 | Part of shapes suite |
| **Shapes Epistemic Bridge** | `02_build/shapes/_epistemic.py` | Working — self-contained copy of tiers + min-rule | 185 | 20 tests (`test_epistemic.py`) |
| **Vellum Gate Models** | `02_build/vellum/gate/models.py` | Working — third copy of EpistemicStatus | 164 | Transfer gate tests |
| **brain_curator (PR #147)** | `02_build/brain_curator/` | Working — 10 modules, migration 008 | ~1,500 | 56 tests |
| **Huf Haus Shapes** | `02_build/shapes/` | Working — 15 base classes + spine enforcement | ~2,500 | 138 tests |
| **Vellum (contact surface)** | `02_build/vellum/` | Working — Brief/Council/Intent/Baton modes | ~2,000 | 95 tests |
| **Brain MCP Server** | `02_build/brain-migration/brain_mcp_server.py` | Working — read-only, 7 tools, SSE | 889 | Manual |
| **Cove Orchestrator** | `02_build/cove-orchestrator/` | Working — Temporal workflows, email agent, MCP servers | Large | ~10 test files |
| **APDS Ingestion Workflow** | `cove-orchestrator/temporal/workflows/apds_ingestion_workflow.py` | Working — 5 stages + optional Stage 6 (curation) | 299 | `test_canonical_ingestion.py` |
| **Sidecar-to-Label Adapter** | `02_build/routing/sidecar_to_label.py` | Working — routes non-harvest content into PUDDING labeller | 313 | None found |
| **Research Pipe Config** | `02_build/scripts/config_research_pipe.py` | Config only — no durable jobs/state machine | 57 | None |
| **Pattern Transfer Gate** | `02_build/vellum/gate/transfer.py` | Working — bridge candidate evaluation with min-rule | 190 | `test_transfer_gate.py` |
| **Beast Control MCP** | `02_build/beast-control-mcp/` | Working — filesystem, inventory, logs, classification tools | ~500 | None found |

### 1.2 What Does NOT Exist Yet

| Component | Handoff Requirement | Current State |
|-----------|-------------------|---------------|
| **Unified epistemic_core module** | Single canonical source for tiers, min-rule, P0Policy, promotion records | Three separate copies (routing, shapes, vellum gate) |
| **P0Policy enforcement** | Production HALT; DEGRADE for backfill only | brain_curator has P0Policy enum; routing/epistemic_status.py raises P0Incident but has no policy switch |
| **Promotion record persistence** | Append-only, resolvable by any consumer | PromotionRecord exists in routing but ephemeral (in-memory only) |
| **19-field runtime context packet** | Wraps brain_packet_id + evidence + permissions + tier | Does not exist as a Pydantic model |
| **Brain MCP guardrails** | Permission block, PII minimisation, purpose scoping | Brain MCP is read-only but has no permission/tier filters |
| **Vellum event contract** | Every meaningful action emits to Vellum | Vellum is a contact surface + council; not yet a system-wide event bus |
| **Research job state machine** | intake_open → research_running → implemented_verified etc. | Config script only; no durable jobs, no closure evidence |
| **Marketing governed consumer** | AMP-358 references brain_packets, dry-run default | Marketing engine exists in separate repo; no packet references |
| **Sidecar ephemeral lifecycle** | TTL, deletion receipts, crash scavenger | sidecar_to_label routes content but has no session lifecycle |

### 1.3 Migrations (existing chain)

```
001_initial_schema.sql
002_nightscout_schema.sql
003_email_agent_schema.sql
004_pipeline_runs_postgresql.sql
005_brain_lockdown.sql
006_compound_design_schema.sql
007_canonical_schema_v0.3.sql  (+ rollback)
008_brain_curator_tables.sql   (PR #147)
```

---

## 2. Duplication Risks and Naming Drift

### 2.1 CRITICAL: EpistemicStatus defined in THREE places

| File | Class Name | Type |
|------|-----------|------|
| `02_build/routing/epistemic_status.py` | `EpistemicStatus` | `enum.IntEnum` |
| `02_build/shapes/_epistemic.py` | `EpistemicTier` | `enum.IntEnum` |
| `02_build/vellum/gate/models.py` | `EpistemicStatus` | `enum.IntEnum` |

All three are semantically identical (INTUITED=1, STRUCTURED=2, MEASURED=3, PROVEN=4) but:
- Different names (`EpistemicStatus` vs `EpistemicTier`)
- Different module paths
- Different companion types (StatusedValue vs StatusedOutput vs plain Pydantic models)
- shapes copy has `from_string()`, routing copy does not
- Vellum gate copy lacks staleness/precondition checks

**Risk:** If one copy changes semantics and the others don't follow, the min-rule diverges across subsystems. This is a P0-class structural risk.

**PR 1 fix:** Extract canonical `epistemic_core` module; other modules re-export from it.

### 2.2 P0 enforcement gap

`routing/epistemic_status.py` raises `P0Incident` on bare values and tier skipping (correct). But:
- **CRITICAL (DeepSeek V4 review):** DriftDetector treats gap≥2 as RED — but **any silent promotion across a boundary is P0, even one tier**. Gap size is severity metadata, not the P0 trigger. The current code only flags gap≥2, which means a single-tier silent promotion escapes detection.
- No `P0Policy` switch — it's always-raise, with no DEGRADE path for backfill
- `brain_curator/config.py` has P0Policy but doesn't import from routing
- No promotion record persistence (PromotionRecord constructed but lost)

### 2.3 Naming drift

| Concept | routing/ | shapes/ | brain_curator/ | vellum/ |
|---------|----------|---------|---------------|---------|
| Tier enum | `EpistemicStatus` | `EpistemicTier` | String constants | `EpistemicStatus` |
| Wrapped value | `StatusedValue` | `StatusedOutput` | N/A (Packet model) | N/A |
| Audit record | `StatusRecord` | `ShapeAuditRecord` | `CurationRun` | N/A |
| Demotion | `_demote()` | `_demote()` | `tier_min()` | `min_status()` |
| P0 exception | `P0Incident` | N/A | `P0TierViolation` | N/A |

### 2.4 Non-forking risks identified

| Risk | Where | Severity |
|------|-------|----------|
| Marketing engine (separate repo) could fork packet schema | `Amplified-Partners/marketing-engine` | HIGH — no reference to brain_packets today |
| CRM has 153+ endpoints, no Brain MCP mediation | `Amplified-Partners/crm` | MEDIUM — not yet deployed to Beast |
| Research pipe is config-only, no durable state | `02_build/scripts/config_research_pipe.py` | MEDIUM — could grow ad-hoc |
| Sidecar-to-label routes content but has no governed lifecycle | `02_build/routing/sidecar_to_label.py` | LOW — only adapter, no state |
| Vellum is a contact surface, not yet system-wide event bus | `02_build/vellum/` | HIGH — handoff requires Vellum as witness for everything |

---

## 3. Proposed PR Sequence

Each PR is designed to be safe, independently testable, and to compound into the next.

### PR 1: Epistemic Core Hardening

**Goal:** Single canonical source for tiers, min-rule, P0Policy, promotion records. Eliminate the three-copy drift risk.

**Scope:**
- Create `02_build/epistemic_core/` with:
  - `tiers.py` — canonical `EpistemicTier` IntEnum (single definition)
  - `min_rule.py` — `StatusedValue`, `effective_status()`, `_demote()`
  - `p0_policy.py` — `P0Policy` enum + `P0Incident` exception + policy enforcement
  - `promotion.py` — `PromotionRecord` + one-step promotion gates + persistence adapter interface
  - `audit.py` — `AuditLog` with thread-safe append, hook support, persistence adapter
  - `drift.py` — `DriftDetector` where **any** silent promotion = P0Incident (gap size is severity metadata only)
- Refactor `02_build/routing/epistemic_status.py` to re-export from `epistemic_core`
- Refactor `02_build/shapes/_epistemic.py` to import from `epistemic_core`
- Refactor `02_build/vellum/gate/models.py` to import from `epistemic_core`
- Refactor `02_build/brain_curator/config.py` and `epistemic_tier.py` to import from `epistemic_core`
- Property tests: min-rule is associative, commutative, idempotent (meet-semilattice)
- Regression tests: all defects from v2 falsification register

**Tests required:**
- min-rule cannot promote
- tier skipping fails (raises P0Incident)
- bare untiered values fail at boundaries
- P0 HALT stops production path
- DEGRADE mode is labelled and cannot write operational truth
- stale values demote
- failed preconditions demote
- **Any** silent promotion across a boundary raises P0Incident (gap size is severity metadata only, not the P0 trigger)
- promotion records are persistent via adapter
- LLM/runtime values cannot silently become MEASURED or PROVEN

**Deliberately NOT changed:** No changes to brain_curator's curation logic, no new database tables, no Vellum wiring. Pure epistemic infrastructure.

**Epistemic tier of new rules:** STRUCTURED (governance design, not empirically calibrated yet).

### PR 2: brain_curator Stage 4 Compatibility

**Goal:** Make brain_curator consume `epistemic_core` semantics rather than its own string constants.

**Scope:**
- Replace `brain_curator/config.py` string constants (TIER_INTUITED etc.) with `epistemic_core.EpistemicTier`
- Replace `brain_curator/epistemic_tier.py` P0TierViolation with `epistemic_core.P0Incident`
- Ensure route decisions reference canonical tier comparisons
- Verify `assign_tier_for_packet()` uses the same min-rule as `epistemic_core`
- Map PUDDING/Curator frontmatter fields to `epistemic_core` types where applicable

**Tests required:**
- No raw mutation of canonical truth by agents (existing — verify still passes)
- Evidence required for active operational packets (existing)
- INTUITED excluded from default agent retrieval (existing)
- Route decisions deterministic (existing)
- Validation samples emitted (existing)
- Promotion records resolvable via `epistemic_core` adapter

**Deliberately NOT changed:** No new curation stages, no schema changes.

### PR 3: Runtime Context Packet Wrapper

**Goal:** Define the 19-field packet as a runtime envelope, not a second curation system.

**Scope:**
- Create `02_build/epistemic_core/context_packet.py` with Pydantic model:
  - `runtime` block: record_id, source_uri, source_type, source_owner, content_hash, client_scope, project_scope, domain, summary, verbatim_excerpt, epistemic_tier, provenance_chain, valid_until, recommended_use
  - `canonical_refs` block: brain_packet_id, source_document_id, evidence_chunk_ids, curation_run_id
  - `curator` block: mapped from brain_curator Packet model
  - `pudding` block: mapped from PUDDING frontmatter
  - `permissions` block: pii_class, allowed_uses, forbidden_uses, approval_required
- Mapper functions: `Packet → ContextPacket`, `ContextPacket → Curator frontmatter`
- Validation: rejects packets without canonical_refs (must reference real brain_packet_id)
- Validation: rejects packets with untiered epistemic metadata

**Tests required:**
- Runtime packet cannot exist without canonical refs
- Malformed YAML/frontmatter is quarantined
- Mapper round-trips: Packet → ContextPacket → Curator frontmatter → validates

**Deliberately NOT changed:** No changes to brain_curator database schema, no Vellum integration.

### PR 4: Brain MCP Gateway Guardrails

**Goal:** Enforce single governed access to Brain, CRM, Linear, GitHub context.

**Scope:**
- Add permission filter to `brain-migration/brain_mcp_server.py`:
  - Tier filter: exclude INTUITED from default retrieval (configurable)
  - PII filter: strip/tokenise PII fields before returning
  - Purpose scoping: callers declare `purpose` parameter
  - Freshness filter: exclude expired content (valid_until check)
- Add CRM adapter interface (behind Brain MCP, not direct access):
  - Returns permission-safe, PII-minimised, purpose-scoped packets
  - No raw CRM access unless explicitly privileged
- Wrap existing `run_query` tool with read-only SQL validation (already exists but add tier/permission checks)

**Tests required:**
- CRM direct access is blocked or flagged outside privileged adapters
- INTUITED content excluded from default results
- PII-containing results are stripped/tokenised
- Permission block enforced at retrieval boundary
- Forbidden uses denied

**Deliberately NOT changed:** No changes to CRM codebase (separate repo). No changes to Brain database schema.

### PR 5: Vellum System-Wide Listening Layer

**Goal:** Make Vellum the witness for every meaningful system action.

**Prior art:** Porch-to-Brain bridge v3 (live on Beast) already emits JSONL receipts for: `watcher_started`, `routed_agent_layer`, `routed_human_layer`, `quarantined`, `ingest_started`, `ingest_completed`, `ingest_failed`, `batch_start`, `batch_complete`. This PR formalises that pattern into a typed `VellumEvent` model with idempotency keys and wires it across the whole system.

**Scope:**
- Define `VellumEvent` Pydantic model with standard fields:
  - event_type, actor, component, subject_id, previous_state, new_state
  - epistemic_tier, provenance_refs, evidence_refs
  - idempotency_key, correlation_id, workflow_id, timestamp
  - permission_scope, expected_next_state
- Create `02_build/epistemic_core/vellum_emitter.py`:
  - `emit_event()` — writes to Vellum permanently (Vellum is the witness; no dry-run compromise)
  - Fallback: if Vellum is temporarily unreachable, buffer to local JSONL and replay on reconnect
  - Idempotency: duplicate events (same idempotency_key) are no-ops
- Wire emitter into:
  - brain_curator (packet create/route/freeze/reopen)
  - epistemic_core (promotion records, P0 incidents)
  - Pattern Transfer Gate (bridge decisions)
- Reconciler stub: flags pending-too-long and state-without-witness

**Tests required:**
- Vellum idempotency prevents duplicate receipts
- Events carry all required fields
- Events are persisted to Vellum permanently
- Fallback JSONL buffer replays correctly on reconnect
- Reconciler detects pending-too-long events

**Acceptance rule (from handoff):** If a component is built and Vellum cannot tell what happened, who did it, what changed, what evidence was used, and what should happen next — the component is incomplete.

**Deliberately NOT changed:** No changes to existing Vellum contact surface / UI / council modes.

### PR 6: Research Pipe and Portable Spine MVP

**Goal:** Prevent "research done" from masquerading as completion.

**Scope:**
- Create `02_build/research_pipe/` with:
  - `models.py` — research_job, research_question, evidence_item, claim_evidence_link, lift_result
  - `state_machine.py` — closure states: intake_open → research_running → research_done_implementation_pending → implemented_verified | parked_verified | rejected_verified | no_action_verified
  - `closure.py` — no `complete` state without closure evidence
- Portable spine generator stub:
  - Explicit includes (current_state, evidence, constraints, allowed_tools, open_questions, approval_tier)
  - Explicit excludes (raw transcript, stale packets, unscoped opinions, direct CRM records)
  - `valid_until` on every spine
- Migration 009: research_jobs, research_questions, research_evidence_items, claim_evidence_links tables

**Tests required:**
- Research job cannot close without closure evidence
- State machine enforces valid transitions only
- Portable spine carries explicit omissions and valid_until

**Needs Ewan:** Portable spine shape approval before merging. I will produce the proposal answering all 10 questions from the handoff checkpoint. Default: proceed with stub that satisfies the state machine tests, but do NOT commit canonical spine shape without Ewan sign-off.

### PR 7: AMP-358 Marketing Dry-Run Proof Loop

**Goal:** Marketing as first downstream consumer of shared substrate, not forked substrate.

**Scope:**
- Create `02_build/marketing_consumer/` with:
  - `models.py` — marketing artifact carrying context_packet_id, brain_packet_id, evidence_refs
  - `guardrails.py` — Radical Honesty checks: permission basis, no fake persona, attribution, unsourced factual claim detection
  - `state_machine.py` — publication states: draft → reviewed → approved → dry_run → sent (approval gate between approved and sent)
  - `dry_run.py` — Brevo adapter defaults to dry-run; real send requires explicit approval signal
- Vellum events for: draft created, reviewed, approved, dry-run executed, sent (or blocked)
- Marketing-Kaizen emits candidates, never canonical truth

**Tests required:**
- Marketing publish/send remains dry-run without approval
- Marketing artifacts reference brain_packet_id (no forked schema)
- Guardrail checks block unsourced claims
- Vellum events emitted for each state transition

**Deliberately NOT changed:** No changes to existing `marketing-engine` repo. This is a governed consumer interface.

### PR 8: Sidecar Ephemeral Context Proof

**Goal:** Just-in-time assistance without creating a shadow CRM.

**Scope:**
- Create `02_build/sidecar/` with:
  - `models.py` — ephemeral session, stable preference context (separate from SaaS context)
  - `lifecycle.py` — session open/use/close with TTL enforcement
  - `cleanup.py` — deletion on normal completion, exception path, expired TTL, startup scavenger
  - `receipts.py` — Vellum deletion receipts
- Signals extracted from sessions are candidate-only and permission-scoped

**Tests required:**
- Sidecar cleanup works on: normal completion, exception path, expired TTL, startup scavenger
- No raw SaaS context persists after expiry
- Deletion receipts created in Vellum
- Sidecar never becomes source of record for customer/contact data

---

## 4. Decisions Taken (reversible)

| # | Decision | Confidence | Rationale |
|---|----------|-----------|-----------|
| 1 | `epistemic_core` as new canonical module (not refactoring routing/epistemic_status.py in place) | OPINION 88% | Three consumers need a shared import; the routing module is too tightly coupled to Layer.__call__ semantics |
| 2 | PostgreSQL + Apache AGE + pgvector only — no FalkorDB/Qdrant compatibility | OPINION 95% | Confirmed deprecated per DATA_ARCHITECTURE.md v1, .cursorrules, Brain Architecture v8 |
| 3 | ~~Vellum events start in dry-run/append-only mode~~ **SUPERSEDED:** Vellum is permanent — events go to Vellum properly, no dry-run compromise | OPINION 95% | Ewan confirmed (2026-05-19): "Vellum is permanent. It's on the Beast. It's in the Brain." |
| 4 | brain_curator keeps its own database tables; epistemic_core is logic-only | OPINION 85% | brain_curator tables are already in production (migration 008); moving them would be destructive |
| 5 | PR sequence is ordered by dependency, not by business priority | OPINION 92% | Each PR builds on the previous; reordering creates incomplete foundations |
| 6 | DriftDetector: **any** silent promotion = P0Incident. Gap size is severity metadata only (DeepSeek V4 review correction) | OPINION 95% | Confirmed by DeepSeek V4 review: "any silent promotion across a boundary is P0, even one tier" |
| 7 | Sample size floor = 30 for MEASURED promotion | OPINION 95% | Ewan confirmed 30 (2026-05-19). Brain Architecture v8 is authoritative. |

## 5. Resolved (formerly "Needs Ewan" — answered 2026-05-19)

| # | Question | Resolution |
|---|----------|------------|
| 1 | **Portable spine shape** | Stub with state machine tests for now. Components: teddy stomach, Five Rods, the Amplified Weight, portable brain. Canonical shape to be defined in a dedicated session. |
| 2 | **Sample size floor** | **30** confirmed by Ewan. Brain Architecture v8 is authoritative. |
| 3 | **Vellum event persistence** | **Vellum is permanent.** No dry-run, no append-only compromise. Events go to Vellum properly. Vellum is on Beast and in the Brain. |

---

## 6. Explicit Non-Goals

- **No production sending, publishing, deletion, CRM mutation, campaign launch, or Brain truth write** in any PR
- **No changes to the existing ingestion pipeline** (stages 1-5 are done)
- **No FalkorDB or Qdrant work** — deprecated, confirmed
- **No CRM codebase changes** — CRM is a separate repo, not yet on Beast
- **No Templar implementation** — Templar definition still open (code module vs Temporal convention vs future build compiler)
- **No Remotion/video work** — sequences after marketing proof loop
- **No raw research into corpus-raw** — research lands in corpus-raw, promoted via review
- **No destruction of existing duplicate cleanup work** — 124 groups already cleaned, 7 PRs created; verify merge status before any new cleanup

---

## 7. Test Strategy

### Per-PR testing

Each PR includes unit tests for its acceptance criteria (listed above per PR). Tests run with `pytest` in CI. No database required for PRs 1-3 (pure logic). PRs 4-8 use test fixtures with mocked database connections.

### Cross-cutting tests (added incrementally)

| Test | Added In |
|------|----------|
| min-rule cannot promote | PR 1 |
| tier skipping fails | PR 1 |
| bare untiered values fail at boundaries | PR 1 |
| P0 HALT stops production path | PR 1 |
| DEGRADE mode labelled, cannot write truth | PR 1 |
| stale values demote | PR 1 |
| failed preconditions demote | PR 1 |
| runtime packet requires canonical refs | PR 3 |
| malformed YAML/frontmatter quarantined | PR 3 |
| CRM direct access blocked/flagged | PR 4 |
| Vellum idempotency prevents duplicates | PR 5 |
| research job cannot close without evidence | PR 6 |
| marketing dry-run without approval | PR 7 |
| Sidecar cleanup (4 paths) | PR 8 |

### Property tests

PR 1 includes property tests (hypothesis or similar) for:
- min-rule meet-semilattice properties: associative, commutative, idempotent
- Promotion is monotonically upward and single-step only
- Demotion is bounded (never below INTUITED)

---

## 8. First PR Scope — PR 1: Epistemic Core Hardening

This is the safe first slice. It creates the shared foundation without changing any existing logic or database state.

**Files created:**
- `02_build/epistemic_core/__init__.py`
- `02_build/epistemic_core/tiers.py`
- `02_build/epistemic_core/min_rule.py`
- `02_build/epistemic_core/p0_policy.py`
- `02_build/epistemic_core/promotion.py`
- `02_build/epistemic_core/audit.py`
- `02_build/epistemic_core/drift.py`
- `02_build/epistemic_core/tests/__init__.py`
- `02_build/epistemic_core/tests/test_min_rule.py`
- `02_build/epistemic_core/tests/test_p0_policy.py`
- `02_build/epistemic_core/tests/test_promotion.py`
- `02_build/epistemic_core/tests/test_drift.py`
- `02_build/epistemic_core/tests/test_properties.py`

**Files modified (re-export, no logic change):**
- `02_build/routing/epistemic_status.py` — imports from epistemic_core
- `02_build/shapes/_epistemic.py` — imports from epistemic_core
- `02_build/vellum/gate/models.py` — imports from epistemic_core
- `02_build/brain_curator/config.py` — imports from epistemic_core
- `02_build/brain_curator/epistemic_tier.py` — imports from epistemic_core

**Safe because:**
- No database changes
- No existing logic changes — existing modules become re-exporters
- All existing tests must still pass
- New tests are additive
- Fully reversible — if epistemic_core is wrong, revert and the three copies still work

**Residual risks:**
- Import path changes could break downstream consumers not in clean-build (low risk — these modules are internal)
- shapes/ tests depend on `EpistemicTier` name; we'll re-export `EpistemicTier = EpistemicStatus` for backward compat

---

*This plan does not edit the original handoff document. Implementation notes are additive only.*

*Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f*
