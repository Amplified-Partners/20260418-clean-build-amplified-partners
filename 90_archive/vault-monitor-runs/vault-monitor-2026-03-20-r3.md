# Vault Monitor Report — 2026-03-20 R3

**Timestamp:** 2026-03-20 ~00:45 UTC

---

## 1. Local Files (_working / _master-docs)

- **_working/**: 4 files. Latest: `vault-monitor-2026-03-20-r2.md` (00:33 UTC). No new files since last check.
- **_master-docs/**: Empty.

## 2. FalkorDB Ingestion

- **Process running:** NO — ingestion has completed.
- **Log says:** "Done! Your Business Brain is being built."
- **Log lines:** 8,545 total
- **Error count:** 293 (Failed/Error/timed out entries)
- **Status:** ✅ Ingestion finished. 293 errors noted — worth reviewing but not blocking.

## 3. Porch Status

- **Incoming queue:** EMPTY — nothing waiting to be processed.
- No action needed.

## 4. Vault Health

| Store | Count | Status |
|-------|-------|--------|
| **Qdrant** | 57,434 points | ✅ Healthy (container up 8 days, note: port not mapped to host — only accessible via Docker network 172.18.0.7:6333) |
| **FalkorDB** | 4,973 nodes | ✅ Healthy |

## Flags

- ⚠️ **Qdrant port mapping:** Qdrant container exposes 6333 internally only (no `-p` host bind). `curl localhost:6333` fails from host. Accessed via container IP 172.18.0.7. Consider adding `-p 6333:6333` if host-level access is needed.
- ⚠️ **293 ingestion errors:** Ingestion complete but logged 293 errors. Recommend reviewing the log for patterns: `grep "Failed\|Error\|timed out" /opt/backups/agent-stack/graphiti-ingestion/ingestion_output_beast_r3.log | head -20`
- ✅ Everything else looks stable. No processes hung, no queue backlog.
