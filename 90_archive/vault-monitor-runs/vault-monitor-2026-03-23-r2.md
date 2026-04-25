# Vault Monitor — 2026-03-23 r2 (11:02 UTC)

## 1. Claude Code Output
- **_working/**: 47+ monitor reports today (r1–r46). No other new files.
- **_master-docs/**: Does not exist.

## 2. FalkorDB Ingestion
- **Beast SSH**: REFUSED — host pings fine (0.3ms avg) but port 22 closed.
- **Process/Log/Errors**: Cannot check — SSH down.
- Last known state (r150 yesterday): Ingestion complete, 293 errors (static), 4,973 nodes.

## 3. Porch
- Cannot check — SSH down.
- Last known state: 0 incoming files.

## 4. Vault Health
- **Qdrant**: Cannot check — SSH down. Last known: 57,434 points.
- **FalkorDB**: Cannot check — SSH down. Last known: 4,973 nodes.

## Flags
- **🔴 Beast SSH DOWN (persistent)** — Port 22 has been refusing connections since ~r145 yesterday (~23:00 UTC Mar 22). Host responds to ICMP. Now 12+ hours of SSH downtime. Likely sshd service crash — needs console/IPMI restart or Hetzner rescue.
- All vault data was stable at last successful check. No data loss risk (services are still running, just SSH access lost).
