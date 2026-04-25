# Vault Monitor Report — 2026-03-20 r36

## 1. Local Files (_working/)
- **Status:** Monitor reports only (r1–r35). No new Claude Code working files.
- **_master-docs/:** Empty — no changes.

## 2. FalkorDB Ingestion
- **⛔ UNABLE TO CHECK** — SSH connection refused (port 22) on Beast (135.181.161.131).
- **Last known (r35):** Ingestion completed. 8,545 log lines. 293 errors.

## 3. Porch Status
- **⛔ UNABLE TO CHECK** — SSH connection refused.
- **Last known (r35):** Incoming queue empty.

## 4. Vault Health
- **⛔ UNABLE TO CHECK** — SSH connection refused.
- **Last known (r35):** Qdrant: 57,434 points | FalkorDB: 4,973 nodes

## 5. Infrastructure
- **Beast server:** PINGABLE (1.9ms latency) but **SSH PORT 22 REFUSED**
- SSH daemon (sshd) appears to be down or has been reconfigured/firewalled.
- All remote checks blocked.

## Flags
1. **🔴 CRITICAL: SSH access to Beast is down.** Server responds to ping but refuses SSH on port 22. sshd may have crashed, been stopped, or a firewall rule changed. This blocks ALL remote monitoring. Needs immediate investigation — check via Hetzner console or out-of-band access.
2. **⚠️ Ongoing from r35:** 293 ingestion errors still unreviewed.
3. **⚠️ Ongoing from r35:** ch-pipeline container unhealthy (6+ days).
4. **⚠️ Ongoing from r35:** Qdrant port 6333 not host-mapped.
