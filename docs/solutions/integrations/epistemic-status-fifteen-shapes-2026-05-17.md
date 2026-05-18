---
title: "Epistemic status integration for fifteen shapes"
category: integrations
date: 2026-05-17
module: 02_build/shapes
component: _epistemic.py, _decorators.py
tags: [epistemic-status, fifteen-shapes, min-rule, runtime-invariant]
severity: medium
description: "How epistemic status was made enforceable at runtime in the fifteen-shapes system."
---

# Epistemic Status Integration for Fifteen Shapes

## Context

The fifteen-shapes system had an `@epistemic(tier="structured")` decorator that set
class attributes (`_epistemic_tier`, `_canon_ref`) but enforced nothing at runtime.
The reference implementation at `02_build/routing/epistemic_status.py` defines the full
Layer 0 invariant: StatusedValues, min-rule, P0 halt on laundering, audit log.

The gap: a shape could declare "proven" and accept garbage inputs. No enforcement.

## Guidance

**To add epistemic enforcement to a shape:**
```python
@epistemic(tier="structured", protected="execute")
class MyService(ServiceBase):
    def execute(self, input_data):
        return {"result": process(input_data)}
```

- `protected="execute"` wraps the method with min-rule enforcement
- Without `protected`, backward compat is preserved (metadata only)
- `strict=True` rejects bare values (P0). Default is lenient (auto-wraps as INTUITED)

**To pass epistemic status between shapes:**
```python
from shapes import StatusedOutput, EpistemicTier, ShapeProvenance

inp = StatusedOutput(
    value=data,
    status=EpistemicTier.STRUCTURED,
    provenance=ShapeProvenance(shape_name="upstream", method="produce"),
)
result = my_service.execute(inp)  # result is StatusedOutput with effective tier
```

## Why This Matters

- Without enforcement, tier declarations are aspirational — they don't prevent laundering
- The min-rule prevents upward laundering across shapes: output cannot exceed input quality
- Gap >= 2 (e.g. MEASURED shape receiving INTUITED input) raises P0 — this prevents connecting incompatible shapes
- Staleness check prevents laundering across time (old valid data used as if fresh)
- Precondition check prevents claiming tier when conditions changed since last verification

## What Was Non-Obvious

1. **The gap check IS the design.** MEASURED(3) + INTUITED(1) = gap 2 = P0. This is not an
   error in the implementation — it's the invariant correctly preventing shapes from being
   connected to inputs too far below their claimed tier. You must route INTUITED through
   STRUCTURED first.

2. **Backward compatibility via `protected=None` default.** The existing `@epistemic(tier=...)`
   API is completely unchanged unless you opt into enforcement with `protected=`.

3. **Lenient mode as rollout strategy.** Setting `strict=False` (default) auto-wraps bare
   values as INTUITED with provenance noting "auto-wrapped". This allows gradual adoption
   without breaking all callers at once.

4. **The decorator wraps methods post-class-creation.** Because `@epistemic` is a class
   decorator (not a method decorator), it wraps named methods via `setattr` after the class
   body is defined. This works because Python class decorators see the complete class.

## What Worked

- Self-contained bridge module (`_epistemic.py`) avoids circular imports with routing
- Re-defining `EpistemicTier` locally (same values as routing module) prevents import dependency
- Thread-safe `ShapeAuditLog` singleton matches the existing `REGISTRY` pattern
- All 56 existing tests pass unchanged — zero backward compat regression
- 28 new tests covering every requirement from the controlling prompt

## What Did Not Work

- Initial test expectations assumed gap=2 should floor (not P0). The invariant is stricter:
  gap >= 2 halts. Tests were corrected to match the actual invariant behaviour.
- Chain composition tests needed shapes with compatible tiers (within 1 tier of each other).

## When to Apply This Pattern Again

- Any time a system has "declared quality levels" that are not enforced at runtime
- Any time values cross boundaries between components with different trust levels
- When building pipelines where downstream components shouldn't silently accept degraded inputs
- When you need an audit trail of quality decisions for regulatory or governance purposes

## Examples

```python
# Strict boundary — rejects bare values
@epistemic(tier="measured", protected="score", strict=True)
class CreditScorer(ScorerBase):
    def score(self, input_data):
        return {"score": calculate_clv(input_data)}

# Precondition-aware shape
@epistemic(tier="structured", protected="execute")
class FreshnessService(ServiceBase):
    def verify_preconditions(self):
        return (PreconditionCheck(name="data_fresh", holds=self._data_age < 3600),)

    def execute(self, input_data):
        return {"analysed": input_data}
```

## Follow-ups

- D1: Unify `ShapeAuditLog` with `AUDIT_LOG` from `epistemic_status.py`
- D2: Add `DriftDetector` subscription for gap-2 monitoring
- D3: Integrate promotion gates so shapes can be promoted after calibration
- D4: Opt all existing `@epistemic`-decorated shapes into enforcement (currently opt-in)
- D5: Wire audit log to Vellum telemetry sink for production observability

---

Devon-b5dc | 2026-05-17 | session devin-b5dc68e1aefa4982b9c083714ac968c6
