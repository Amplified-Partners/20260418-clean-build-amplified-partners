# SKILL_EXECUTION.md (The Operations Spine)

**Purpose**: This is the skill of *how to build and type*. Agents load this into context only when assigned to write code, execute deployment commands, or manipulate the file system.

---

## Operational Architecture

**1. IBAC-First (Identity-Based Access Control)**
Replacing rigid determinism. Models operate flexibly, but only within strict identity, scope, and boundary policies. Governance by identity, not just hardcoded SQL schemas. Cedar policies define what actions an agent can take (e.g., `prod.cedar`).

**2. Tripartite Data Architecture**
1. **GitHub (Lightweight)**: Contains only the current active version of the codebase and recent history. Keep it lean and fast.
2. **The Vault (The Truth)**: The true source of deep context. Heavily curated.
3. **The Archive/Bloat Vault (Off-site)**: Raw dumps and uncurated bloat. Never mix bloat with the main Vault.

**3. Frictionless Execution**
Ewan's got fat fingers and he's slow. The AI is the IT expert. Make it frictionless. Agents must understand that file paths are nothing to an AI, but humans have to negotiate them. Do not force Ewan to negotiate file paths, look around, click links, or hunt for files. Bring the completed work directly to him, immediately.

**4. Shadow-First & Privacy-First**
- Novel improvements live in `03_shadow/` until proven, then promoted.
- No client PII in core. Tokenised at edge. Working memory deleted on task completion.

---

## The Folder Contract

- `00_authority/` — policy spine (minimum)
- `01_truth/` — truth-shaped candidates (schemas, interfaces, processes)
- `02_build/` — runnable artifacts
- `03_shadow/` — experiments, Kaizen probes (never authoritative)
- `90_archive/` — reference and provenance (never authoritative)

---

## Hard Stop Tokens (Use Literally)

- `[LOGIC TO BE CONFIRMED]` — incomplete logic; proceed via options
- `[SOURCE REQUIRED]` — missing provenance; not truth
- `[DECISION REQUIRED]` — fork unresolved inside frame
- `[NON-AUTHORITATIVE]` — reference only
- `[CURRENT BEST EVIDENCE]` — external lookup at search time; not promoted fact

---

## Read Order for New Agents
1. `PORTABLE-SPINE.md` (The Bootloader)
2. `OPENCLAW.md` — your role, config, operating principles
3. `CANONICAL.md` — repos, paths, services
4. `SIDECAR.md` — Ghost Sidecar product
5. `STATE.md` — full current state
