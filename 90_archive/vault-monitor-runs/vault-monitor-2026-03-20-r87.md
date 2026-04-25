# Vault Monitor — 2026-03-20 r87 (21:53 UTC)

## 1. Claude Code Output
- **_working/**: 86 monitor reports today (r1–r86). No other new files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **Beast SSH**: CONNECTION REFUSED on port 22. Cannot reach server.
- **Last known status (r85)**: Ingestion COMPLETE. 293 errors (stable/historic). 4,973 nodes in graph.

## 3. Porch Status
- **Beast SSH**: DOWN — unable to check. Last known: empty incoming queue (r85).

## 4. Vault Health
- **Beast SSH**: DOWN — unable to check Qdrant or FalkorDB.
- **Last known (r85)**: Qdrant DOWN (previously 57,434 points). FalkorDB UP with 4,973 nodes.

## Flags
- **ALERT: Beast SSH DOWN (persisting since r86).** Port 22 connection refused for ~10+ minutes now. Could be SSH service crash, firewall change, or server reboot. Needs manual investigation.
- **ALERT: Qdrant still DOWN** (persisting from earlier runs). Needs `docker start qdrant` once Beast is reachable.
- No new local file activity outside monitor reports.
