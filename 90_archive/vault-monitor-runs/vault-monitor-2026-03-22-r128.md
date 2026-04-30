# Vault Monitor — 2026-03-22 r128

## 1. Claude Code Output
- **_working/**: Monitor reports only (r1–r118 + this). No new non-monitor files.
- **_master-docs/**: Empty.

## 2. FalkorDB Ingestion
- **Status**: COMPLETED. Process not running (finished successfully).
- **Last log**: "Done! Your Business Brain is being built."
- **Errors**: 293 (historical, unchanged from previous checks)
- **Nodes**: 4,973

## 3. Porch
- **Status**: CLEAR. 0 files in incoming/.

## 4. Vault Health
- **Qdrant**: UP (green) — **57,434 points** in `amplified_knowledge`
- **FalkorDB**: UP — **4,973 nodes** in `business_knowledge`
- **Qdrant container**: Running (11 days uptime), port not bound to host localhost — only accessible via Docker network (172.18.0.7:6333)

## Flags
- **RESOLVED**: Beast SSH is back online. Previous SSH outage (reported r108–r118) has cleared.
- **RESOLVED**: Qdrant is running and healthy (was reported as unreachable — issue was localhost binding, not container health).
- **NOTE**: `ch-pipeline` container showing **unhealthy** status (up 9 days). May warrant investigation.
- **INFO**: Qdrant not bound to host port 6333 — `curl localhost:6333` from host fails. Access via Docker network IP (172.18.0.7:6333) works fine. This is config, not a bug, but worth noting for future monitoring scripts.
