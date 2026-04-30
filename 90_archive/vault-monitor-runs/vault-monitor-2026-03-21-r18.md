# Vault Monitor Report — 2026-03-21 R18

**Timestamp:** 2026-03-21 ~04:02 UTC

## 1. Local Directories
- **_working/**: 17 prior monitor reports today (r1–r17). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **Process:** Not running (completed).
- **Status:** Done. "Your Business Brain is being built."
- **Errors:** 293 (Failed/Error/timed out lines in log — unchanged from prior checks).

## 3. Porch
- **Incoming:** Empty. Nothing to process.

## 4. Vault Health
- **Qdrant:** 57,434 points (unchanged). Note: port 6333 not mapped to host — only reachable via Docker network IP (172.18.0.7).
- **FalkorDB:** 4,973 nodes (unchanged).
- **Docker:** 36 containers running.

## 5. SSH Status
- **RECOVERED.** Beast SSH is back online after being down ~60+ minutes (down since ~R14 at 02:52 UTC).

## Flags
- **ch-pipeline: UNHEALTHY** — Up 7 days but marked unhealthy. Persistent issue.
- **Qdrant port binding:** localhost:6333 connection refused — container running but port not published to host. Only accessible via Docker internal IP. This may affect external tools expecting localhost access.
- **293 ingestion errors** — stable count, not new, but worth reviewing.
