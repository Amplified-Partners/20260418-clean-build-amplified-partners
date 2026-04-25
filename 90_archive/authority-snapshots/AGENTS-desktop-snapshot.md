---
layer: 1
layer_name: internal-build
version: 1.0
status: active
date: 2026-04-15
inherits:
  - ../AGENTS.md
---

## Amplified/ — build the business

**Scope:** Internal build work (tools, methods, experiments, marketing systems).

**Inherits:** Root `AGENTS.md` is the canonical AI operating guide.

**Adds (internal build):**

-   Prefer fast iteration **with** deterministic checks (tests, small diffs).
-   Default stance: build reusable primitives; avoid overfitting to a single future
  client shape before diversity shows up.
-   Any artifacts that could become client-facing must be re-checked against the
  stricter rules under `partners/` before they ship externally.
