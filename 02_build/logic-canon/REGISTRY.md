# Logic Canon — Pattern Registry

> **What is this?** A toolbox of solved algorithmic patterns. Each module solves one problem. If you're building something and the problem matches, import the module — don't reinvent it.
>
> **Design rule:** Python holds the safety net. AI holds the intelligence. These modules are deterministic guards — they detect, they stop, they constrain. They do not think.
>
> **How to use:** Find your problem below → import the module → pass your data.
>
> **Provenance:** Extracted from Nexus V2 (production trading engine, 6,500+ lines). Domain-specific language removed. Maths identical. Patterns universal.
>
> **Dependencies:** numpy, pandas (already in every Amplified system).

---

## Problem → Module Lookup

| I need to... | Module | Function |
|---|---|---|
| **Stop an autonomous system before it causes damage** | `circuit_breaker` | `CircuitBreaker.check()` |
| **Cap exposure / prevent over-concentration** | `circuit_breaker` | `CircuitBreaker.check_exposures()` |
| **Test new approaches without real-world risk** | `shadow_tester` | `generate_variants()` + `check_promotions()` |
| **Detect when the environment has shifted** | `regime_detector` | `RegimeDetector.update()` |
| **Scale system activity based on volatility** | `regime_detector` | `RegimeDetector.vol_scale` |
| **Detect redundancy between channels** | `correlation_monitor` | `check_correlations()` |
| **Convert scores into proportional budget splits** | `signal_normaliser` | `normalise()` |
| **Make constraints tamper-evident / immutable** | `ulysses_clause` | `UlyssesClause.check_constraint()` |
| **Audit-chain any sequence of actions** | `ulysses_clause` | `UlyssesClause.audit_chain` |

---

## Module Summaries

### 1. `circuit_breaker` — Autonomous Damage Prevention
**Problem:** Autonomous system could compound damage. Need hard stops.
**Key maths:** Daily loss > threshold → freeze N cycles. Cumulative drawdown > threshold → longer freeze. Vol targeting: `target_vol / realised_vol` scalar.
**Config knobs:** `max_daily_loss`, `max_cumulative_drawdown`, `target_vol`, `max_single_exposure`

### 2. `shadow_tester` — Risk-Free A/B Testing
**Problem:** Want to test new approaches without risk. Only promote when statistically better.
**Key maths:** Generate variants (±20% parameter perturbation). Track for 30+ days. Promote when: Sharpe beats live by ≥0.30 AND return beats by ≥3% AND max DD < 15%.
**Config knobs:** `num_variants`, `param_range`, `min_days`, `sharpe_beat_threshold`

### 3. `regime_detector` — Environmental Shift Detection
**Problem:** Detect when operating environment has fundamentally changed. Scale activity.
**Key maths:** Signal > threshold → regime change. Confirmation readings prevent whiplash. Vol scalar = `target_vol / realised_vol`.
**Config knobs:** `caution_threshold`, `crisis_threshold`, `caution_scale`, `crisis_scale`, `invert`

### 4. `correlation_monitor` — Redundancy Detection
**Problem:** Two channels you thought were independent are doing the same thing.
**Key maths:** Pairwise Pearson correlation over rolling window. |corr| > 0.70 = redundant.
**Config knobs:** `window`, `warning_threshold`, `critical_threshold`

### 5. `signal_normaliser` — Opinions to Proportional Allocations
**Problem:** Convert scores of varying strength into proportional budget splits.
**Key maths:** `allocation = (signal / sum_of_all_signals) × budget`. Cap at max%. Floor at minimum useful size.
**Config knobs:** `max_allocation_pct`, `signal_threshold`, `min_allocation`

### 6. `ulysses_clause` — Tamper-Evident Constraints
**Problem:** Prevent operator (including future-you) from weakening rules under pressure.
**Key maths:** HMAC-SHA256 signed manifest. SHA-256 hash-chained audit log. Any modification detected.
**Config:** constraints dict + signing key

---

## Cross-Cutting Patterns

These modules compose. Common combinations:

| Use Case | Modules |
|---|---|
| **Agent orchestration** | `circuit_breaker` (halt runaway agents) + `regime_detector` (scale activity by system health) + `ulysses_clause` (enforce governance) |
| **Marketing engine** | `shadow_tester` (test new strategies) + `correlation_monitor` (detect overlap) + `signal_normaliser` (budget splits) |
| **Self-improving system** | `shadow_tester` (test variants) + `regime_detector` (know when to scale back) + `circuit_breaker` (hard stops) |

---

## What's NOT here (and why)

The following are deliberately left to AI:

- **Ranking N items** — AI should weigh criteria and rank. Python cleans the data.
- **Finding optimal parameters** — AI should reason about what to try. Python caps the damage if it's wrong.
- **Deciding resource allocation** — AI should think. These modules hold the safety net around whatever AI decides.

Rule: **Python with AI with human equals Amplified.**

---

*Devon-b3d8 | 2026-05-15 | Logic Canon v1.1*
*Provenance: Nexus V2 on Beast (Hetzner AX162-R) → domain-agnostic extraction*
