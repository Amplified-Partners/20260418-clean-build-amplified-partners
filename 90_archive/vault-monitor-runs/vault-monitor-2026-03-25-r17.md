# Vault Monitor — 2026-03-25 R17

## 1. Local Files
- **_working/**: 16 monitor reports today (r1–r16). No new non-monitor files.
- **_master-docs/**: Empty — no changes.

## 2. FalkorDB Ingestion
- **Status**: UNKNOWN — Beast unreachable (SSH connection refused).
- **Last known**: Ingestion completed. 293 errors (stable). 4,973 nodes.

## 3. Porch
- **Status**: UNKNOWN — Beast unreachable.
- **Last known**: Empty (0 files queued).

## 4. Vault Health
- **Qdrant**: UNKNOWN — Last known: 57,434 points.
- **FalkorDB**: UNKNOWN — Last known: 4,973 nodes.

## Flags
- 🔴 **BEAST SSH DOWN — MULTI-DAY OUTAGE** — `ssh: connect to host 135.181.161.131 port 22: Connection refused`. Persisting since Mar 24. Now Day 2+. SSH key also missing from this Cowork session environment.
- All remote metrics stale — relying on last known values from Mar 20.
- No new local file output detected.

## Action Needed
- **Critical**: Beast SSH has been down for 24+ hours. Requires manual intervention via Hetzner console or out-of-band access to restart sshd.
