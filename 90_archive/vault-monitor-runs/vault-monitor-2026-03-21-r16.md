# Vault Monitor Report — 2026-03-21 R16

**Timestamp:** 2026-03-21 ~03:26 UTC

## 1. Local Directories
- **_working/**: 15 prior monitor reports today (r1–r15). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **Status:** UNKNOWN — SSH unreachable.

## 3. Porch
- **Status:** UNKNOWN — SSH unreachable.

## 4. Vault Health
- **Qdrant:** UNKNOWN — SSH unreachable.
- **FalkorDB:** UNKNOWN — SSH unreachable.

## 5. SSH Status
- **DOWN.** Beast (135.181.161.131) refusing SSH connections on port 22. Connection refused on both key attempts.
- SSH has been down since R15 (~03:07 UTC), now ~20 min. Was also down at R15. Last successful connection was R14 (~02:52 UTC).

## Flags
- **BEAST SSH STILL DOWN** — Connection refused persisting for ~35 min now (since after R14). SSH daemon not listening or firewall blocking port 22. Check via Hetzner console if this continues.
- Last known good values (from R14): Qdrant 57,434 points, FalkorDB 4,973 nodes, ingestion complete, porch empty, 27 containers running, ch-pipeline unhealthy.
