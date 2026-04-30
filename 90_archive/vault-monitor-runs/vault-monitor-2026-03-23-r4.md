# Vault Monitor — 2026-03-23 R4 (~12:20 UTC)

## 1. Claude Code Output
- **_working/**: 49+ monitor reports accumulated (latest: r3 at 12:02). No new non-monitor files.
- **_master-docs/**: Empty. No new deliverables.

## 2. FalkorDB Ingestion
- **Process**: COMPLETED (not running)
- **Result**: 120 success / 32 failed out of 152 files, 920 chunks
- **Time**: 232.8 minutes
- **Errors in log**: 293 (mostly "Invalid duplicate_name" for currency values like £12.09M, plus some "Target entity not found" edges)
- **FalkorDB nodes**: 4,973

## 3. Porch
- **Incoming files**: 0 — nothing queued.

## 4. Vault Health
- **Qdrant**: 57,434 points — status GREEN. Note: not host-accessible (Docker network only)
- **FalkorDB**: 4,973 nodes

## Flags
- Ingestion complete — 32/152 files failed (21% failure rate). Worth reviewing.
- Qdrant port not mapped to host — only reachable via Docker network IP 172.18.0.7:6333.
- 293 log errors — mostly benign duplicate_name warnings on currency strings.
