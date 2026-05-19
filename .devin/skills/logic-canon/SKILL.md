---
name: logic-canon
description: Python safety-net toolbox for all Amplified Partners systems. Use when you need circuit breakers, A/B testing, regime detection, correlation monitoring, signal normalisation, or tamper-evident constraints. These modules protect — they do not think.
---

# Logic Canon — Python Safety Net Toolbox

**Location:** `02_build/logic-canon/`
**Registry:** `02_build/logic-canon/REGISTRY.md` (full problem→module lookup table)
**Dependencies:** numpy, pandas

## Design rule

**Python holds the safety net. AI holds the intelligence. Human holds the decision.**

These modules are deterministic guards. They detect thresholds, enforce constraints, and prevent damage. They do not rank, optimise, or decide — that's AI's job.

## When to reach for this

Before writing any of the following patterns from scratch, check if Logic Canon already solves it:

- Stopping a system before it causes cascading damage → `circuit_breaker`
- Testing new approaches in parallel without real-world risk → `shadow_tester`
- Detecting environmental regime shifts → `regime_detector`
- Detecting redundancy / overlap between channels → `correlation_monitor`
- Converting confidence scores into proportional allocations → `signal_normaliser`
- Enforcing tamper-evident constraints → `ulysses_clause`

## Quick import

```python
from logic_canon import circuit_breaker, shadow_tester, regime_detector
from logic_canon import correlation_monitor, signal_normaliser, ulysses_clause
```

## What's NOT here (AI's job)

- Ranking items by multiple criteria — AI reasons, Python cleans the data
- Finding optimal parameters — AI thinks, Python caps the damage
- Deciding resource allocation — AI decides, Python holds the safety net

## Key design principles

- **Zero infrastructure dependencies.** Pure functions + simple classes. No database, no API, no config files.
- **Domain-agnostic.** No trading language. Works for marketing, agents, CRM, content, anything.
- **Composable.** Modules work independently or together. Combine as needed.
- **All maths documented.** Every formula is in the module docstring. No black boxes.
- **Deterministic.** Same input = same output. No randomness, no LLM calls.
