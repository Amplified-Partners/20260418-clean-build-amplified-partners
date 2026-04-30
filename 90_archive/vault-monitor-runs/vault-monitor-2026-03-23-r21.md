# Vault Monitor — 2026-03-23 r21

**Timestamp:** 2026-03-23 ~04:12 UTC

## 1. Claude Code Output
- **_working/**: 20 monitor reports today (r1–r20). No new non-monitor files.
- **_master-docs/**: Empty.

## 2. FalkorDB Ingestion
- **Status**: UNKNOWN — Beast unreachable
- **Last known (r17, ~03:32 UTC)**: Process completed. 4,973 nodes. 293 historic errors.

## 3. Porch Status
- **Status**: UNKNOWN — Beast unreachable

## 4. Vault Health
- **Qdrant**: UNKNOWN — Beast unreachable
- **FalkorDB**: UNKNOWN — Beast unreachable
- **Last known (r17)**: Qdrant 57,434 points / FalkorDB 4,973 nodes

## Flags
- 🔴 **Beast SSH DOWN** — Connection refused on port 22. SSH key copied from Downloads successfully but server not accepting connections. Beast has been intermittently unreachable all day — last confirmed up at r17 (~03:32 UTC), down again since r18 (~03:42 UTC). Pattern: SSH drops every ~30-60 min, comes back briefly, drops again.
- ⚠️ ch-pipeline container UNHEALTHY (9+ days, ongoing).
- ⚠️ Qdrant port 6333 not bound to localhost (must use Docker network IP 172.18.0.7).
- All vault metrics were stable at last successful check.
