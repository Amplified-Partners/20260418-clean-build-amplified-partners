# Vault Monitor Report — 2026-03-21 R14

**Timestamp:** 2026-03-21 ~02:52 UTC

## 1. Local Directories
- **_working/**: 13 prior monitor reports today (r1–r13). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **Process:** NOT running (completed).
- **Log tail:** "Done! Your Business Brain is being built." — ingestion finished.
- **Errors in log:** 293 (unchanged from previous reports).
- **FalkorDB nodes:** 4,973

## 3. Porch
- **Incoming:** Empty. No files waiting.

## 4. Vault Health
- **Qdrant:** 57,434 points (stable). Container up 9 days. NOTE: No host port binding — only accessible via Docker network (172.18.0.7:6333), not localhost:6333.
- **FalkorDB:** 4,973 nodes (stable). Container up 5 days.
- **ch-pipeline:** Marked **unhealthy** (up 7 days).

## 5. SSH Status
- **RESTORED.** Beast SSH now reachable via `claude-code-beast-key-2`. Previous ~23hr outage resolved.
- The original key (`~/.ssh/claude-code-beast-key`) is still not in the session; using key from Downloads.

## Flags
- **Qdrant port not mapped to host.** Works fine internally but `curl localhost:6333` fails. If any host-side scripts need Qdrant, they'll break.
- **ch-pipeline unhealthy** — worth investigating if ClickHouse pipeline is critical.
- All other services nominal. 27 containers running.
