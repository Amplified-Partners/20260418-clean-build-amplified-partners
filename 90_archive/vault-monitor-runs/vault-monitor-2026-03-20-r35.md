# Vault Monitor Report — 2026-03-20 r35

## 1. Local Files (_working/)
- **Status:** Monitor reports only (r1–r34). No new Claude Code working files.
- **_master-docs/:** Empty — no changes.

## 2. FalkorDB Ingestion
- **Process:** NOT RUNNING (completed)
- **Log:** 8,545 lines in `ingestion_output_beast_r3.log`
- **Final log output:** "Done! Your Business Brain is being built."
- **Errors:** 293 (Failed/Error/timed out entries)
- **Note:** Ingestion run 3 has finished. 293 errors to review.

## 3. Porch Status
- **Incoming queue:** EMPTY — nothing waiting to process.

## 4. Vault Health
| Store | Count | Status |
|-------|-------|--------|
| Qdrant (amplified_knowledge) | **57,434 points** | GREEN |
| FalkorDB (business_knowledge) | **4,973 nodes** | OK |

## 5. Infrastructure
- **Qdrant:** Running (8 days uptime) — ⚠️ port 6333 NOT mapped to host (accessible only on Docker network 172.18.0.7:6333)
- **FalkorDB:** Running (4 days uptime)
- **ch-pipeline:** ⚠️ UNHEALTHY (6 days uptime)
- All other core services UP.

## Flags
1. **⚠️ Qdrant port not host-mapped** — `localhost:6333` won't work from host. Only reachable via Docker network IP. Consider re-deploying with `-p 6333:6333`.
2. **⚠️ 293 ingestion errors** — worth reviewing `ingestion_output_beast_r3.log` for patterns.
3. **⚠️ ch-pipeline unhealthy** — has been unhealthy for 6 days. Needs investigation.
