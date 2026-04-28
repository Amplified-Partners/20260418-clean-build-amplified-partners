---
status: parked
handoff_from: Antigravity (MacBook Session)
handoff_to: Antigravity (Mac Mini Session)
date: 2026-04-28
---

# BATON PASS: TO THE MINI

## Context
We are migrating to the Mac Mini strictly because it holds the active SSH connection to the Hetzner Beast. 

## Architectural State (The Spine)
- **Charter & Logic**: Locked. *They hold the database at the edge. We run the logic centrally. We are the aggregator.* 
- **Privacy Absolute**: The Sidecar connects locally, pulls context into ephemeral working memory (last 20 emails, first name), executes, and instantly forgets the raw data.
- **Hardware Correction**: The Beelink N100 edge-NLP constraint was a historical echo and is officially struck. Edge compute is no longer a bottleneck because we run the heavy logic.

## Execution State
- **Brick 2 (Wired)**: `clean-build/02_build/cove-orchestrator/email_agent/drafter.py` is fully wired to Brevo v3. It contains the logic for the Day 0, Day 3, and Day 7 drip sequence. `config.py` holds the `BREVO_API_KEY` slot.
- **Tri-Council Dogfood**: `StaffUI.jsx` now has a "Tri-Council Consult" input box to test the logic, fully wired to the Temporal worker (`main.py` imports fixed).

## Your Immediate Orders upon Wake-up (The Next Bricks)

### 1. BRICK 1: END THE SINGLE POINT OF FAILURE
Your first action on the Mini is to use its SSH pipe to pull the ~80,000 lines of marketing-system Python off the Beast server and into `clean-build/02_build/marketing_engine/`. Get it into version control immediately. 

### 2. BRICK 3: REMOTION RENDER PIPELINE
Once the Beast code is safe, move `Sidecar-Remotion-Studio` into the `clean-build` repo. Render the first parametric video template server-side and validate the L4-WA (WhatsApp) distribution mechanism.

---
*Resume mission.*
