# Vault Monitor — 2026-03-25 02:05 UTC

## 1. Claude Code Output
- **_working/**: 20+ vault-monitor reports present. Latest: `vault-monitor-2026-03-24-r94.md` (23:42 UTC yesterday)
- **_master-docs/**: Empty / not found

## 2. FalkorDB Ingestion
- **Process**: NOT RUNNING (completed)
- **Status**: "Done! Your Business Brain is being built."
- **Errors**: 293 (Failed/Error/timed out in log)
- **Note**: Ingestion finished — no active process. 293 errors may need review.

## 3. Porch Status
- **Incoming queue**: EMPTY — nothing waiting

## 4. Vault Health
| Store | Count | Status |
|-------|-------|--------|
| Qdrant | **57,434** points | ✅ UP (13 days) |
| FalkorDB | **4,973** nodes | ✅ UP (9 days) |

## ⚠️ Flags
- **Qdrant port not mapped to host** — localhost:6333 unreachable from host. Only accessible via Docker network IP (172.18.0.7:6333). This could break any scripts expecting `localhost:6333`.
- **293 ingestion errors** — ingestion complete but nearly 300 failures logged. Worth reviewing.
- **Ingestion not running** — expected if complete, but confirm no remaining files need processing.
