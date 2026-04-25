# Vault Monitor Report — 2026-03-21 R27

**Timestamp:** 2026-03-21 ~05:42 UTC

## 1. Local Directories
- **_working/**: 26 monitor reports today (R1–R26). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. Beast SSH
- **SSH: DOWN** — Connection refused on port 22. Port 2222 timed out. Both keys tried. Was online at R26 (~05:32), now down again.

## 3. Ingestion (from last successful check R26)
- **Process:** Not running (completed).
- **Errors:** 293 (stable).
- **Status:** Ingestion finished.

## 4. Porch (from last successful check R26)
- **Incoming:** Empty.

## 5. Vault Health (from last successful check R26)
- **Qdrant:** Container was UP, port 6333 not bound to host (known issue). Internal health OK.
- **FalkorDB:** 4,973 nodes.

## Flags
- **ALERT:** Beast SSH down again after brief restoration at R26. Port 22 connection refused — suggests SSH daemon crashed or was stopped. This is the 8th+ SSH failure today.
- **PERSISTENT:** Qdrant port 6333 not host-accessible (known).

## Summary
Beast SSH down again (port 22 refused). Was briefly online at R26. All other stats from last good check: ingestion complete, 293 errors (stable), FalkorDB 4,973 nodes, Qdrant internal-only, porch empty. No new local files. SSH instability is a recurring issue today — may need investigation.
