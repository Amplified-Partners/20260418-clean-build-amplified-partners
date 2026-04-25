---
title: "Cross-Mac Automation Guardrails"
id: "cross-mac-automation-guardrails"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "2026-04-23-amplified-partners-cross-mac-automation-guardrails.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — cross-Mac automation guardrails (Hazel, Shortcuts, folder actions)

**Document date (ISO 8601):** 2026-04-23  
**Author (AI assist):** Rowan  

**Audience:** You, future you, and anyone deploying **the same discipline on every Mac**. This is the **precision layer** on top of the organisation proposal and the north-star checks — not a product tutorial.

**Why this exists (plain):** Rule engines (**Hazel**, **Shortcuts**, **Folder Actions** / legacy Automator chains) are **powerful**. Power without hard guardrails **eats valuable things** — moves you did not mean, “helpful” dedupes that kept the wrong file, races with iCloud, or rules that matched too broadly. You already paid that tuition once (including building **Convergence** at Eli after **losing data to Hazel**). These rules are written so **nothing valuable gets in the way of automation** — automation **yields** when in doubt.

---

## 1. One ruleset, many Macs

| MUST | Detail |
|------|--------|
| **M1 — Single canonical text** | This file (plus linked org / goal docs) is the **source of truth** for what automation may do. Copy it into each Mac’s doc home (e.g. `~/AmplifiedPartners/reference/` or your git repo); **do not fork** divergent “local Hazel only” policies without a dated decision. |
| **M2 — Version every change** | Any edit to automation rules gets **`YYYY-MM-DD`** in the commit message, doc header, or a `RULESET_VERSION=2026-04-23` line Hazel/Shortcuts cannot read but **humans** use to confirm parity across machines. |
| **M3 — Dry-run before widen** | New or changed rules: **observe only** (move to a quarantine folder, or log-only) for a **minimum window you choose** (e.g. 7 days) before turning on delete, trash, or cross-volume moves. |

---

## 2. Formal shape of an allowed rule (all engines)

Every automation rule you ship **MUST** be expressible in this skeleton. If it does not fit, **do not ship it** until it does.

```text
RULE_ID:           AP-AUTO-<short-name>   (unique)
TRIGGER:           <folder + pattern + optional metadata>
ACTION:            <exactly one primary outcome>
PRECONDITIONS:     <all must be true>
STOP_IF:           <any true → rule does not run>
AUDIT:             <append log line OR Hazel’s built-in history>
```

**STOP_IF is non-negotiable** for anything beyond “copy into quarantine”. Typical `STOP_IF` clauses appear in §4 and §5.

---

## 3. Engines (how this doc maps)

| Engine | Strength | Risk |
|--------|-----------|------|
| **Hazel** | Deep conditions, nested logic, runs in background | Broad matches; trash/delete; cross-folder moves hard to reason about at scale |
| **Shortcuts** | Good for explicit flows, shareable, iCloud | Easier to leave “ask every time” off by mistake |
| **Folder Actions** | Folder-scoped | Legacy; harder to review centrally |

**Same rules, different syntax:** translate each `RULE_ID` into Hazel rules / Shortcut steps **one-to-one**. Do not “simplify” in translation — that is where drift eats data.

---

## 4. Global NEVER (hard deny — all Macs, all engines)

Automation **MUST NOT** perform these **primary** actions (move to Trash, permanent delete, strip extension, flatten tree) on paths matching **any** row unless a **human-named exception** rule exists with its own `RULE_ID` and expiry review.

| # | Pattern / condition | Rationale |
|---|---------------------|-----------|
| N1 | Any path under **`.git/`** or file named **`.git`** (file or dir at tree root) | Repository corruption; history loss |
| N2 | **`.env`**, **`.env.*`**, `**/*credentials*`, `**/*secret*`** (filename heuristics only — tune per org) | Secret leakage or breakage |
| N3 | **`node_modules/`**, **`.venv/`**, **`vendor/`** at rule match root | Regenerated but huge; wrong move = broken builds and sync hell |
| N4 | **`Library/`**, **`Photos Library.photoslibrary`**, mail store bundles | System/user data outside Amplified scope |
| N5 | **`*.photoslibrary`**, **`*.sparsebundle`**, **`Time Machine`** destinations | Obvious |
| N6 | Any folder name matching **`YYYY-MM-DD-*`** **that already existed before the rule** (dated workspaces, vault extractions) | Treat as **archive class** — classify before any “cleanup” match |
| N7 | **`Desktop/`** or **`Documents/`** root containing **`.git`** | Unusual layout; manual investigation before automation touches siblings |
| N8 | Files inside **`Manual Library`** (Sparkle) or your declared **`DO_NOT_AUTOMATE/`** sentinel dirs | Human intent: leave alone |
| N9 | **Primary** action = **delete** or **empty Trash** on anything not in an explicit **quarantine** path | Org policy: **no silent loss**; see §6 |

**Moves** (not deletes) that cross **from** a NEVER path **into** quarantine still violate N1–N8 unless you have written a **narrow, reviewed** exception — default is **do not move**.

---

## 5. STOP_IF clauses (attach to every destructive or broad rule)

Minimum set; merge into Hazel “If **any** of the following are true, do not proceed”:

1. **File size** outside bounds you set (e.g. zero-byte **or** unexpectedly huge) → log, do not move.  
2. **Modified time** newer than **24 hours** (tunable) → **Recents / human first**; no auto-sort into deep archive.  
3. **More than one hardlink or alias** to the same inode → skip (dedupe mistakes love this).  
4. **Extended attributes / quarantine flag** you do not recognise → skip or copy-only.  
5. **Path depth** beyond N (e.g. 8) from allowed root → skip (avoid eating nested project internals).

---

## 6. Quarantine-first pipeline (nothing “disappears”)

| Stage | MUST behaviour |
|-------|----------------|
| **Q1 — Quarantine root** | Single known folder per volume, e.g. `~/AmplifiedPartners/inbox/_automation-quarantine/YYYY-MM-DD/` (create dated subfolder per day or per rule run). |
| **Q2 — Primary action** | For “cleanup” rules: **copy** or **move into Q1** only — never straight to Trash for first-generation rules. |
| **Q3 — Retention** | Files sit in Q1 for **≥ human-chosen days** before a **separate**, **slower** rule may suggest Trash — and duplicates use **hash match + explicit UI** (Hazel duplicate stage or manual). |
| **Q4 — Narrative / retrieval** | Anything tagged for **graph+vector / narrative store** is **out of scope** for delete rules — **export** path is separate from **filesystem delete**. |

This is the operational cousin of **Convergence**: **converge on safety first**, then delete only what is **provably redundant**.

---

## 7. MAY — allowed automation (examples, tighten per Mac)

These are **classes** of rules that **can** be approved if every instance has `RULE_ID`, `STOP_IF`, and `AUDIT`.

| Class | Example trigger | Example action | Notes |
|-------|-----------------|----------------|-------|
| **A — Typed inbox** | `Downloads/*.pdf` older than 7d | Move to `~/AmplifiedPartners/inbox/pdfs/` | No delete |
| **B — Screenshot decay** | `Desktop/Screenshot*.png` older than 30d | Move to `media/screenshots/YYYY-MM/` | Never match non-screenshot PNGs |
| **C — Exact duplicate** | Same size + hash (Hazel duplicate tool) | **Flag only** until human picks keeper | Never auto-pick keeper for non-trivial dirs |
| **D — Empty junk** | True empty **files** 0 bytes in `Downloads/` only | Optional delete — only if explicit sub-rule and Q window satisfied | Many 0-byte files are placeholders; prefer skip |

---

## 8. Duplicates and “helpful” dedupe (where people lose data)

| MUST | Detail |
|------|--------|
| **D1** | **Byte-identical only** for auto-action; “looks the same” is **human**. |
| **D2** | If two files differ **at all**, **both stay** until a named memo says otherwise. |
| **D3** | For `(1)` duplicate filenames: never delete both; **surface** in duplicate UI. |

---

## 9. iCloud and multi-volume (nothing “wrong way” via sync)

| MUST | Detail |
|------|--------|
| **I1** | Prefer rules scoped to **fully local** paths Every documents as supported; avoid cloud-only targets. |
| **I2** | Do not run **competing** Hazel + Shortcuts + Sparkle on the **same** folder without a **single** owner doc that says who wins. |
| **I3** | After rule change: wait **one full sync cycle** before judging “missing” files. |

---

## 10. Review cadence (prevents rule rot)

| Cadence | Action |
|---------|--------|
| **Monthly** | Open Hazel (or export rule list); confirm each `RULE_ID` still matches intent. |
| **After any OS major upgrade** | Re-test STOP_IF; Apple changes paths and sandboxing. |
| **After “I lost a file”** | **Pause all** automation for that root; restore from backup; add STOP_IF; resume only after Q1 proof. |

---

## Related (same spine)

- **Mac Air 1 — runnable dummy run + Hazel starter rules** (use before full cross-Mac rollout): [`2026-04-23-hazel-mac-air-1-dummy-run-pack.md`](2026-04-23-hazel-mac-air-1-dummy-run-pack.md)  
- North star, ISO checks, collaborator context: [`2026-04-23-amplified-partners-goal-and-iso-verification.md`](2026-04-23-amplified-partners-goal-and-iso-verification.md)  
- Folder tree, narrative tiers, GitHub vs narrative: [`2026-04-23-amplified-partners-organization-proposal.md`](2026-04-23-amplified-partners-organization-proposal.md)  
- Parallel agents, exclusive roots: [`2026-04-23-amplified-partners-parallel-agents-playbook.md`](2026-04-23-amplified-partners-parallel-agents-playbook.md)

**Attribution note:** Convergence / Eli / Hazel loss — **your** lived context, recorded here only so future rule authors **do not repeat the failure mode**; correct any factual detail if the name or place was misheard in chat.
