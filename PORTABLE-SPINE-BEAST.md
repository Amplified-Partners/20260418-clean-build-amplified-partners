# The Portable Spine — Beast Operations

**Target Agent:** Antigravity (Mac Mini / Beast Operations)
**Date:** 27 April 2026
**Purpose:** Instant context-restoration for the Antigravity instance booting on the Mac Mini to work on the Sovereign Vault (Hetzner Beast).

---

## 1. The Core Directives
*   **The Ulysses Clause:** We are anchored to the owner's stated goals. We do not drift into unnecessary AI bloat. We protect the main business.
*   **The Air-Gap Strategy:** This instance (on the Mini) is solely responsible for the "Big Boy" (The core Beast architecture, `cove-orchestrator`, `hound_dog`, Sovereign SQL). The Marketing Swarm (`remotion-renderer`) is handled by a separate agent on the MacBook Air. We do not mix the two.
*   **The Three-Brain Isolation Model:** 
    1.  **Amplified Brain** (Sovereign core knowledge)
    2.  **Client Brain** (Hard-isolated raw client PII and data)
    3.  **Network Brain** (Anonymised PUDDING patterns and APQC codes only)

## 2. Our Current State
We have successfully hardened the `cove-orchestrator` pipeline:
*   `hound_dog.py` is locked down with strict OOM protections, file size limits (5MB), and robust error handling to prevent API crashes during large data mining runs.
*   The system is transitioning to a headless, terminal-based orchestrator utilizing `Makefile` workflows and Docker.

## 3. Immediate Priority Tasks for the Mac Mini
Based on the `amplified-technology-stack.md` and `security-implementation-runbook.md`, the next targets for the Beast are:

1.  **PCO (Progressive Context Optimizer):** The critical missing piece that sits between our agents and LiteLLM to compress context while verifying facts with a Quality Veto. This is Priority 1.
2.  **Beast Server Security Hardening:**
    *   Fix 007: Beast SSH Audit & Hardening (Key-only access, no root password).
    *   Fix 008: Beast Firewall (UFW) configuration.
    *   Fix 009: Docker Network Isolation (Ensuring only Traefik exposes ports to 0.0.0.0).

## 4. How to Operate
*   **No GUI Reliance:** We are building for headless execution.
*   **Gatekeeper First:** No agent touches the Sovereign SQL or FalkorDB directly. Everything goes through the FastAPI/Gatekeeper.
*   **Radical Transparency:** If an error occurs, we log it. We do not hallucinate fixes without checking the architecture.

*When the new Antigravity instance reads this file, it will instantly inherit the soul of the previous session and be ready to conquer the Beast.*
