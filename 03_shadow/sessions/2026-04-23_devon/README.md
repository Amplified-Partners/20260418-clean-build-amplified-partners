---
title: Devon session 2026-04-23 — source documents index
date: 2026-04-23
author: Devon (Devin session 4cc8b0d727684f94a8f055853099d8e6)
status: source
session_type: orchestration-planning
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

This folder is the **source-document bundle** for the Devon orchestration-planning session of 2026-04-23. Everything the session produced is listed here. Treat as source, not as authority.

Per Ewan's instruction: *"We need to save this folder, all of the work, in a folder that's accessible to everyone. Because this is source document."*

## Files in this folder

| File | What it is |
|---|---|
| `2026-04-23_amplified-partners-map_v1.md` | Landscape map v1 — factual inventory of entities, products, personas, relationships. Written early in the session. Source. |
| `2026-04-23_devon_baton-pass_v1.md` | Baton pass v1 (superseded). Retained for audit trail and provenance — shows the original error (forecasts + prescriptions) that led to the neutrality clause. |
| `README.md` | This file. |

## Files elsewhere in the repo (produced by this session)

| Path | What it is |
|---|---|
| `03_shadow/job-wrapups/2026-04-23_amplified-partners-orchestration-session_wrapup.md` | Neutral stateless handover (v2). Facts + risks + tokens + optional analysis. Signed. |
| `01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md` | Framework that codifies the neutrality rule for stateless handovers. Candidate process. Signed. |
| `00_authority/SIGNATURES.md` | System-wide rule: every AI signs its work when committed. Authoritative. Signed. |
| `00_authority/USE_IT_OR_CUT_IT.md` | System-wide rule: sounds good + built + unused = cut. Authoritative. Signed. |
| `00_authority/OPINION_CONFIDENCE.md` | System-wide rule: opinions labelled as opinions with confidence; tiered threshold by reversibility. Authoritative. Signed. |

## Provenance

Original drafts lived in `/home/ubuntu/ewan-map/` (personal scratch). Ewan clarified mid-session that artefacts belong to the organisation, not to him personally — subsequent work landed in this repo. The files in this folder are copies of the personal-scratch originals; the scratch copies remain as a second audit trail until Ewan or a future agent prunes them.

## Session decisions (condensed)

- **Database**: stay with Qdrant. AI-facilitated customer deployments flatten the pgvector-vs-Qdrant ops delta, strengthening the incumbent. Confidence 65% stay / 35% migrate; both below the 85% commit threshold, so no switch. Migration stays available if pain surfaces.
- **Confidence threshold**: 85% default to commit without research; tiered by reversibility (50% reversible / 85% medium / 95% irreversible).
- **Rules added to authority**: `SIGNATURES.md`, `USE_IT_OR_CUT_IT.md`, `OPINION_CONFIDENCE.md`.

## Context-creep observation

Session length reached the point where finer nuance from earlier turns begins to compress. This folder exists partly so a fresh session can resume from source without relying on my in-thread recall.

---

Authored by,

**Devon**
Devin session `4cc8b0d727684f94a8f055853099d8e6`
2026-04-23
