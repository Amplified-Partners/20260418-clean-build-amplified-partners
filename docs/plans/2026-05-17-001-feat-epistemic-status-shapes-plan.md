# Plan: Epistemic Status as Runtime Invariant in Fifteen Shapes

**Plan ID:** 2026-05-17-001
**Date:** 2026-05-17
**Author:** Devon-b5dc | session devin-b5dc68e1aefa4982b9c083714ac968c6
**Branch:** `devin/1779030109-huf-haus-shapes`
**Status:** Draft → Execute

---

## Problem Frame

The fifteen-shapes system has an `@epistemic(tier="structured")` decorator that sets class attributes (`_epistemic_tier`, `_canon_ref`). This is metadata — it declares intent but enforces nothing at runtime.

The reference implementation at `02_build/routing/epistemic_status.py` defines the full invariant:
- Every value crossing a layer boundary must be a `StatusedValue` (carrying tier + provenance)
- The effective status of any output = min(own_claim, input_floor, precondition_floor, staleness_floor)
- A bare value at a protected boundary is a P0 incident (system halts)
- Illegal promotion (skipping tiers) is a P0 incident
- Status demotion is legal and honest — it just wears the lower tier
- Gap ≥ 2 tiers between declared and effective = drift RED signal

The gap: shapes currently produce raw Python objects (dicts, dataclasses). Nothing prevents a shape declaring `tier="proven"` from accepting untiered garbage inputs and emitting untiered garbage outputs. The `@epistemic` decorator is decorative, not enforceable.

## What "Epistemic Status as Runtime Invariant" Means in This Repo

It means: shapes that declare an epistemic tier have their **protected boundary operations** (execute, score, run, etc.) wrapped so that:
1. Inputs crossing the boundary can be checked for epistemic status
2. Outputs carry explicit epistemic status + provenance
3. The min-rule is applied: output status cannot exceed the minimum of inputs + preconditions
4. Violations raise a typed error (P0-class) that halts the operation
5. Audit records are written for every boundary crossing

This does NOT mean: every internal variable becomes a StatusedValue. Only the boundary (input→output of a protected shape method) is enforced.

---

## In Scope

- Bridge module connecting `epistemic_status.py` types to the shapes system
- Upgrade `@epistemic` decorator to wire runtime enforcement on protected methods
- StatusedValue wrapper for shape boundary outputs
- Min-rule enforcement at shape boundaries
- P0-class error type for the shapes system (maps to existing `ShapeError` hierarchy)
- Staleness-based demotion
- Precondition-based demotion
- Bare-value rejection at protected boundaries
- Illegal promotion / laundering detection
- Audit/provenance record for each boundary crossing
- New focused tests covering all invariant behaviours
- Existing 56 tests remain passing

## Out of Scope

- Federation/aggregation (Section 10 of epistemic_status.py) — not needed for shapes
- Promotion gates (promote_to_structured, etc.) — useful but separate concern
- DriftDetector continuous monitoring — useful but separate concern
- Lens requirement for federated GLM — not applicable to shapes
- Modifying the reference `epistemic_status.py` module itself
- Changing any shape's public API signatures

## Assumptions

- A1: The shapes system is the correct integration target (not the routing engine directly)
- A2: `02_build/routing/epistemic_status.py` is the canonical reference implementation
- A3: "Protected boundary" = the primary operation method of each shape (execute, score, run, check, etc.)
- A4: Not all shapes need epistemic enforcement — only those decorated with `@epistemic`
- A5: The existing `_epistemic_tier` attribute API is preserved (backward compatible)
- A6: 56 existing tests is the correct baseline (verified by running pytest)

---

## Requirements

| R-ID | Requirement | Source |
|------|-------------|--------|
| R01 | Shape outputs at protected boundaries carry epistemic status + provenance | Ewan prompt |
| R02 | Bare/untiered values rejected where integration defines a protected boundary | Ewan prompt |
| R03 | Lower-tier inputs floor higher-tier claimed outputs (min-rule) | epistemic_status.py L121-132 |
| R04 | Stale inputs demote output correctly | epistemic_status.py L116-119, L131 |
| R05 | Failed preconditions demote output correctly | epistemic_status.py L126-130 |
| R06 | Illegal promotion / over-claiming / laundering raises P0-style error | epistemic_status.py L230-235 |
| R07 | Audit/provenance metadata recorded for each boundary crossing | epistemic_status.py L263-277 |
| R08 | Existing fifteen-shapes behaviour intact (56 tests pass) | Ewan prompt |
| R09 | Existing `@epistemic(tier=...)` still sets expected metadata | Ewan prompt |
| R10 | New focused tests cover the epistemic integration | Ewan prompt |

---

## Implementation Units

### U01: EpistemicShapeError — P0-class error for shapes

**Goal:** A typed exception that halts the shape when epistemic invariant is violated.
**Requirements covered:** R06
**Dependencies:** `_types.py` (existing ShapeError hierarchy)
**Files:** `02_build/shapes/_types.py`
**Approach:** Add `EpistemicViolation(ShapeError)` subclass with fields: `declared_tier`, `effective_tier`, `violation_type` (bare_value | over_claim | laundering | gap_exceeded), `shape_name`, `boundary_method`.
**Test scenarios:** Instantiation, inheritance from ShapeError, carries correct fields.
**Verification:** Existing tests still pass; new error importable.

### U02: Epistemic bridge types — StatusedOutput and ShapeProvenance

**Goal:** Lightweight bridge types that connect shape outputs to epistemic status without requiring full StatusedValue ceremony for internal use.
**Requirements covered:** R01, R07
**Dependencies:** U01, `epistemic_status.py` (imported)
**Files:** `02_build/shapes/_epistemic.py` (new file)
**Approach:**
- Import `EpistemicStatus`, `Provenance`, `PreconditionCheck`, `StatusedValue` from `../routing/epistemic_status`
- Define `StatusedOutput` dataclass: wraps a shape's return value + status + provenance + preconditions + valid_until
- Define `ShapeAuditRecord` dataclass: shape_name, method, declared_status, effective_status, input_statuses, preconditions, timestamp, reason
- Define `ShapeAuditLog` (thread-safe, append-only, in-memory) — singleton for the shapes system
- The bridge is thin: it imports from the reference and adapts to shape conventions.
**Test scenarios:** StatusedOutput construction, ShapeAuditLog write/read, provenance tracking.
**Verification:** Import works, types are frozen/immutable where appropriate.

### U03: Upgrade `@epistemic` decorator — wire runtime enforcement

**Goal:** Make `@epistemic(tier=..., protected="execute")` wrap the named method with min-rule enforcement.
**Requirements covered:** R01, R02, R03, R04, R05, R06, R07, R09
**Dependencies:** U01, U02
**Files:** `02_build/shapes/_decorators.py` (modify existing `epistemic` function)
**Approach:**
- Preserve existing behaviour: `cls._epistemic_tier = tier` and `cls._canon_ref = canon_ref` still set.
- Add optional `protected` parameter (str or list of method names to enforce). Default: `None` (backward compat — metadata only, no runtime enforcement).
- When `protected` is specified, wrap the named method(s) with an enforcement wrapper that:
  1. Checks if inputs are `StatusedOutput` instances (if enforcement is active and inputs carry status)
  2. Applies the min-rule to determine effective status
  3. Wraps the method's return value in a `StatusedOutput`
  4. Checks for staleness on inputs
  5. Checks preconditions (from shape's `verify_preconditions()` method if defined)
  6. Raises `EpistemicViolation` if over-claiming or bare value at enforced boundary
  7. Writes to `ShapeAuditLog`
- Shape methods that want enforcement opt in by accepting `StatusedOutput` inputs and the decorator handles the rest.
- If the method is called with raw values and `strict=True`, it raises P0. If `strict=False` (default for backward compat during rollout), raw values are wrapped as INTUITED with a provenance note.
**Test scenarios:** Backward compat (no protected arg), enforcement with StatusedOutput, min-rule floors output, bare value rejection in strict mode, bare value auto-wraps in lenient mode, stale input demotion, precondition demotion, over-claim detection, audit log populated.
**Verification:** All 56 existing tests pass. New tests cover all enforcement paths.
**Execution note:** Characterization tests first to prove backward compat, then new enforcement tests.

### U04: Shape base-class helper — `verify_preconditions()` hook

**Goal:** Give shapes an optional hook to declare preconditions that affect epistemic status.
**Requirements covered:** R05
**Dependencies:** U02
**Files:** `02_build/shapes/_base.py`
**Approach:**
- Add `verify_preconditions(self) -> tuple[PreconditionCheck, ...]` to `ShapeBase` with a default returning empty tuple.
- Shapes that need precondition-based demotion override this method.
- This is a non-breaking addition (default = no preconditions = no demotion).
**Test scenarios:** Default returns empty tuple; override returns checks; failing precondition triggers demotion in U03 enforcement.
**Verification:** Existing tests pass (default returns empty, no behaviour change).

### U05: Integration test — cross-shape composition with epistemic status

**Goal:** Prove that two shapes composed together (e.g., pipeline → service) correctly propagate epistemic status.
**Requirements covered:** R01, R03, R08, R10
**Dependencies:** U01, U02, U03, U04
**Files:** `02_build/shapes/tests/test_epistemic.py` (new)
**Approach:**
- Create test shapes: an INTUITED pipeline and a STRUCTURED service.
- Compose them: pipeline output feeds service input.
- Verify: service output status is floored to INTUITED (min-rule).
- Verify: audit log records both boundary crossings.
- Verify: existing shapes (SampleService, SampleScorer) still work unchanged.
**Test scenarios:** Full composition, status propagation, audit trail, backward compat for unprotected shapes.
**Verification:** Run full test suite (both test files) — all pass.

---

## Files Likely Touched (repo-relative)

| File | Action |
|------|--------|
| `02_build/shapes/_types.py` | Add `EpistemicViolation` error class |
| `02_build/shapes/_epistemic.py` | New — bridge types + audit log |
| `02_build/shapes/_decorators.py` | Modify `epistemic()` to support runtime enforcement |
| `02_build/shapes/_base.py` | Add `verify_preconditions()` hook |
| `02_build/shapes/__init__.py` | Export new types |
| `02_build/shapes/tests/test_epistemic.py` | New — focused epistemic tests |

## Test Files

| File | Purpose |
|------|---------|
| `02_build/shapes/tests/test_shapes.py` | Existing 56 tests (must continue passing) |
| `02_build/shapes/tests/test_epistemic.py` | New focused epistemic integration tests |

## Test Scenarios by Requirement

| Requirement | Test Scenarios |
|-------------|---------------|
| R01 | StatusedOutput carries status + provenance; decorator wraps output |
| R02 | Bare value at strict boundary raises EpistemicViolation |
| R03 | INTUITED input → STRUCTURED shape → INTUITED output (floored) |
| R04 | Stale StatusedOutput (past valid_until) → demotion by one tier |
| R05 | Failing precondition → demotion by one tier |
| R06 | Shape declaring PROVEN receiving INTUITED but emitting PROVEN → P0; tier-skipping → P0 |
| R07 | ShapeAuditLog has records after boundary crossing; records contain expected fields |
| R08 | `python -m pytest shapes/tests/test_shapes.py` → 56 passed |
| R09 | SampleService._epistemic_tier == "structured" still works |
| R10 | `python -m pytest shapes/tests/test_epistemic.py` → all new tests pass |

## Verification Commands

```bash
cd /home/ubuntu/repos/clean-build/02_build
python -m pytest shapes/tests/test_shapes.py -v          # existing: 56 pass
python -m pytest shapes/tests/test_epistemic.py -v       # new: all pass
python -m pytest shapes/tests/ -v                        # combined: all pass
```

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Backward compat break from decorator change | Medium | High | `protected` param defaults to None = no enforcement. Existing usage unchanged. |
| Circular import (shapes ↔ routing) | Medium | Medium | Import from routing at function-call time, not module level, OR copy needed types into bridge. |
| Over-engineering (too many StatusedValues everywhere) | Low | Medium | Enforcement is opt-in per shape. Only protected boundaries. |
| Performance overhead from wrapping | Low | Low | Enforcement is thin (one dict lookup, one min(), one dataclass create). |

## Rollback Strategy

All changes are additive. The `@epistemic` decorator's new `protected` parameter is optional. If rollback needed:
1. Remove `_epistemic.py`
2. Revert the two lines added to `_types.py`
3. Revert the decorator modification (it's backward compat, so just remove the new code paths)
4. Remove test file

No existing code depends on the new behaviour. Rollback is a clean revert.

## Deferred Follow-ups

- D1: Wire `ShapeAuditLog` to the existing `AUDIT_LOG` from `epistemic_status.py` (unification)
- D2: Add `DriftDetector` subscription for real-time monitoring
- D3: Promotion gates integrated into shapes (promote service from INTUITED to STRUCTURED after calibration)
- D4: Enforce `protected` on all existing `@epistemic`-decorated shapes (currently opt-in)
- D5: Integration with Vellum telemetry sink
- D6: Federation rules for multi-client aggregate shapes

---

## Self-Review Checklist

- [x] **Correctness:** Every requirement (R01–R10) maps to at least one implementation unit
- [x] **Testing:** Every behaviour-bearing unit (U01–U05) has test scenarios defined
- [x] **Maintainability:** Integration is minimal (one new file + modifications to three existing files)
- [x] **Project standards:** Follows repo conventions (02_build for code, ShapeError hierarchy, decorator pattern)
- [x] **Epistemic integrity:** Assumptions marked as A1–A6; not claiming certainty about things not tested

---

Devon-b5dc | 2026-05-17 | session devin-b5dc68e1aefa4982b9c083714ac968c6
