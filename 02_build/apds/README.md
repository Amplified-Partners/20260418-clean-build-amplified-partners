---
title: APDS Stage-1 (Pudding ingestion pipe) — what's running on Beast
date: 2026-05-05
agent: Devon-9f21
session_id: devin-9f2104fb06624b009f2879c50957c647
linear: AMP-104
status: shadow-of-prod (mirror of /opt/amplified/apds on Beast)
---

<!-- markdownlint-disable-file MD013 -->

# APDS Stage-1 — version-controlled mirror

This directory is the **version-controlled mirror** of the APDS Stage-1 scripts that ran on Beast (`/opt/amplified/apds/{harvest,label}/`) on 2026-05-05 to satisfy Hazel Gate 3 (Pudding ingestion pipe flowing). The **harvester** is byte-identical to what ran in production except for an added attribution header per `00_authority/SIGNATURES.md`. The **labeller** adds three minimal hardening edits over the Beast copy (Cypher escaping of label values, `float()` cast on confidence, idempotency-check fix) flagged by Devin Review on PR #52 — see `apds_labeller.py` docstring and § Files below for details. The Beast copy is therefore one revision behind this file.

This is **not** the canonical clean-build labeller. See § Schema divergence below.

## Pipeline (as it ran)

```
SearXNG (8 queries × 11 engines)
        │  harvester_mvp.py
        ▼
/opt/amplified/apds/harvest/harvest_20260505_033410.json   (88 blocks, 250 results)
        │  apds_labeller.py
        ▼
Ollama llama3.1:8b  →  PUDDING JSON  →  FalkorDB
        │
        ▼
FalkorDB graph `business_knowledge`:
  250 × :Document {source: 'APDS', WHAT, HOW, SCALE, TIME, PATTERN, confidence}
```

Run log: `/opt/amplified/apds/logs/labeller_20260505_094115.log` (46 KB; final line `Done. Successful: 250, Failed: 0`).

## Hazel Gate 3 status

**Functional pass.** 250 PUDDING-labelled documents are queryable in FalkorDB right now. Hazel can read them.

**Production hardening — not done.** The labeller ran as a one-shot `python3 apds_labeller.py`. There is no `apds-labeller` container, no Temporal schedule, no idempotency check beyond the in-script "already labelled" guard. A follow-on Linear ticket should pick up containerisation; suggest doing this **after** the schema divergence below is resolved, so the productionised version uses whichever vocabulary becomes canonical.

## Schema divergence — three live PUDDING vocabularies

There are now three "PUDDING" implementations in the workspace, all using overlapping dimension names with non-overlapping vocabularies:

| Source | Dimensions | Example `WHAT` codes | Production status |
|---|---|---|---|
| **Spec** — `01_truth/schemas/2026-03_pudding-discovery-system_v1.md` | 4: `WHAT.HOW.SCALE.TIME` | (per spec, 7 codes) | candidate authority, no code that follows it exactly |
| **Repo script** — `02_build/scripts/pudding_labeler.py` | 5: `+ PATTERN` | `E / R / P / S / C / I / M` (single-letter symbolic) | runnable, not running |
| **Beast script (this dir)** — `apds_labeller.py` | 5: `+ PATTERN` | `FIN / OPS / MKT / TECH / PPL / GOV / EXT` (functional business categories) | **running**, 250 production docs labelled |

`HOW`, `SCALE`, `TIME`, `PATTERN` vocabularies also differ across the three. See [`03_shadow/state-2026-05-05-amp-104-pre-pudding.md`](../../03_shadow/state-2026-05-05-amp-104-pre-pudding.md) for the full divergence table.

**Decision parked** in `00_authority/DECISION_LOG.md` v17 with a `[DECISION REQUIRED]` token. Two questions for Ewan:

1. 4-dim (per spec) or 5-dim (per both implementations)?
2. Symbolic vocab (clean-build canonical script) or functional vocab (Beast running script + 250 production docs)?

Devon-9f21 will not resolve unilaterally — these are truth/world-shaping (Pudding taxonomy is foundational methodology per the org-wide knowledge note "The Pudding Technique"). Reversibility is medium-to-low: 250 docs already exist with the Beast vocab, and any vocabulary that becomes canonical will determine how every future Match/Score stage interprets bridges between concepts.

## Files

| File | What it does | Provenance |
|---|---|---|
| `harvester_mvp.py` | SearXNG harvester. 8 UK-SMB queries × 11 engines, top-5 hits per. | Hand-deployed to Beast by Kimmy 2026-05-05; promoted to repo by Devon-9f21 (this PR). |
| `apds_labeller.py` | Ollama (llama3.1:8b) PUDDING labeller + FalkorDB writer. Idempotent — skips already-labelled doc IDs (this version actually skips; see below). | Hand-deployed to Beast by Kimmy 2026-05-05; promoted to repo by Devon-9f21 (this PR) **+ three hardening edits per Devin Review** (escape PUDDING label values into Cypher; cast `confidence` to float; fix the idempotency check that compared a list to an int and was always False on Beast). Beast copy is now one revision behind — see file docstring for sync note. |
| `README.md` | This file. | Devon-9f21. |

## How to re-run on Beast

```bash
ssh root@135.181.161.131
cd /opt/amplified/apds
python3 harvest/harvester_mvp.py    # writes harvest_<run_id>.json
python3 label/apds_labeller.py      # reads hardcoded harvest path, writes to FalkorDB
```

Cost: zero (Ollama is local; SearXNG is local; FalkorDB is local).

Time: ~17 minutes for 250 results on Beast (Ollama llama3.1:8b on CPU).

## Out of scope for this directory

- Stages 2–5 of APDS (Extract, Match, Score, Kaizen) — directory stubs exist on Beast at `/opt/amplified/apds/{extract,match,score,kaizen,dashboard}/` but are empty. Not Hazel-gating.
- Container packaging — see "Hazel Gate 3 status" above.
- The CRM-side knowledge routes that read these labelled docs back out of FalkorDB — those live in the `crm` repo (`/api/knowledge/graph/query` etc.). AMP-109 tracks getting the CRM container starting cleanly so the routes are reachable from outside Beast.

---

*Devon-9f21 | 2026-05-05 | session `devin-9f2104fb06624b009f2879c50957c647`*
