# Vault Monitor Report — 2026-03-21 R15

**Timestamp:** 2026-03-21 ~03:07 UTC

## 1. Local Directories
- **_working/**: 14 prior monitor reports today (r1–r14). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **Status:** UNKNOWN — SSH unreachable.

## 3. Porch
- **Status:** UNKNOWN — SSH unreachable.

## 4. Vault Health
- **Qdrant:** UNKNOWN — SSH unreachable.
- **FalkorDB:** UNKNOWN — SSH unreachable.

## 5. SSH Status
- **DOWN.** Beast (135.181.161.131) refusing SSH connections on port 22. Tried both keys (`claude-code-beast-key` and `claude-code-beast-key-2`). Error: "Connection refused" — indicates SSH daemon not listening or firewall blocking.
- Last successful connection was R14 (~02:52 UTC), only ~15 min ago.

## Flags
- **BEAST SSH DOWN** — Connection refused. This is new since R14 (~15 min ago SSH was working). Could be SSH service restart, firewall change, or server reboot. Worth checking via Hetzner console if this persists.
- Last known good values (from R14): Qdrant 57,434 points, FalkorDB 4,973 nodes, ingestion complete, porch empty, 27 containers running, ch-pipeline unhealthy.
