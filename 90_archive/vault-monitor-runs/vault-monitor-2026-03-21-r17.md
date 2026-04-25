# Vault Monitor Report — 2026-03-21 R17

**Timestamp:** 2026-03-21 ~03:42 UTC

## 1. Local Directories
- **_working/**: 16 prior monitor reports today (r1–r16). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **Status:** UNKNOWN — SSH unreachable.

## 3. Porch
- **Status:** UNKNOWN — SSH unreachable.

## 4. Vault Health
- **Qdrant:** UNKNOWN — SSH unreachable.
- **FalkorDB:** UNKNOWN — SSH unreachable.

## 5. SSH Status
- **DOWN.** Beast (135.181.161.131) refusing SSH on port 22. Tried both key files.
- SSH has been down since after R14 (~02:52 UTC) — now ~50 minutes.
- Last known good values (from R14): Qdrant 57,434 points, FalkorDB 4,973 nodes, ingestion complete, porch empty, 27 containers running, ch-pipeline unhealthy.

## Flags
- **BEAST SSH DOWN ~50 MIN** — Connection refused persisting. SSH daemon likely stopped or firewall blocking. Recommend checking via Hetzner console if not already done.
- ch-pipeline was unhealthy as of last successful check (R14).
