# Vault Monitor Report — 2026-03-21 R28

**Timestamp:** 2026-03-21 ~06:12 UTC

## 1. Local Directories
- **_working/**: 27 monitor reports today (R1–R27). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. Beast SSH
- **SSH: DOWN** — Connection refused on port 22. Both keys tried. Persistent failure since R27.

## 3. Ingestion (from last successful check R26)
- **Process:** Not running (completed).
- **Errors:** 293 (stable).
- **Status:** Ingestion finished.

## 4. Porch (from last successful check R26)
- **Incoming:** Empty.

## 5. Vault Health (from last successful check R26)
- **Qdrant:** Container UP, port 6333 not host-bound (known issue).
- **FalkorDB:** 4,973 nodes.

## Flags
- **ALERT:** Beast SSH still down (port 22 refused). Ongoing since R27. 9th+ SSH failure today.
- **PERSISTENT:** Qdrant port 6333 not host-accessible (known).

## Summary
Beast SSH remains down (connection refused). All cached stats from R26: ingestion complete, 293 errors (stable), FalkorDB 4,973 nodes, porch empty. No new local files. SSH instability continues — needs investigation when Ewan is available.
