---
title: "Beast Hardening Phase 2 — Docker Firewall Bypass Fix + Port Isolation"
date: 2026-05-09
version: 1
status: active
linear: AMP-289
signed-by: "Devon-7ac0 | 2026-05-09 | devin-7ac006f9572f4fbc88862a485bff90d4"
---

# Beast Hardening Phase 2

Continuation of Phase 1 hardening (completed by Ewan + Kimmy). This phase
addresses Docker's iptables firewall bypass and binds all internal service
ports to localhost or Tailscale only.

## Audit findings (2026-05-09 05:25 UTC)

### Ports globally exposed to the internet (`0.0.0.0`)

| Port | Container | Service | Risk |
|------|-----------|---------|------|
| 5432 | `docker-postgres-1` | PostgreSQL (cove-orchestrator stack) | **CRITICAL** — database directly reachable from internet |
| 8081 | `cove-api` | Cove API Gateway | HIGH — internal API exposed |
| 8092 | `cove-translator` | Cove Translation layer | HIGH — internal service exposed |
| 8001 | `amplified-crm` | CRM (dev/staging) | HIGH — application API exposed |
| 8003 | `amplified-crm-dev` | CRM dev instance | HIGH — application API exposed |

### Ports correctly bound to `127.0.0.1`

| Port | Container | Service |
|------|-----------|---------|
| 4000 | `litellm` | LLM proxy |
| 5433 | `cove-postgres` | Cove TimescaleDB (cove-repo stack) |
| 6333 | `qdrant-temp` | Qdrant (legacy) |
| 6379 | `falkordb-temp` | FalkorDB (legacy) |
| 7233 | `cove-temporal` | Temporal gRPC |
| 8080 | `traefik` | Dashboard |
| 8088 | `token-proxy` | Anthropic cost proxy |
| 8090 | `brain-mcp-readonly` | Brain MCP |
| 8091 | `brain-mcp-writer` | Brain MCP |
| 8233 | `cove-temporal-ui` | Temporal UI |
| 11434 | `ollama` | Local LLM inference |

### Ports correctly public (by design)

| Port | Container | Purpose |
|------|-----------|---------|
| 80 | `traefik` | HTTP redirect → HTTPS |
| 443 | `traefik` | HTTPS ingress |
| 22 | `sshd` | SSH access |

### DOCKER-USER iptables chain (pre-existing, partially correct)

```
ACCEPT  state RELATED,ESTABLISHED     (good — return traffic)
RETURN  tcp dports 80,443 in=ext_nic  (good — web traffic)
DROP    in=ext_nic                     (good — block external)
RETURN  (catch-all for internal)       (good — docker bridge traffic)
```

The existing rules block external access to Docker-forwarded ports. However:
- No explicit Tailscale interface allowance
- Rules are not persisted across reboots
- No `iptables-persistent` installed

### Tailscale status

Container running (`tailscale/tailscale:latest`) on `openclaw_default` network.
**Not authenticated** — `TS_AUTHKEY` is empty. Waiting for interactive login.

Auth URL: `https://login.tailscale.com/a/d9d7654016e6c`

Container has `CAP_NET_ADMIN` and `CAP_SYS_MODULE` with `/dev/net/tun` mounted.

## Changes made

### 1. Compose files — bind internal ports to `127.0.0.1`

**`02_build/cove-orchestrator/docker/docker-compose.yml`** (version-controlled):
- PostgreSQL: `5432:5432` → `127.0.0.1:5432:5432`
- Temporal gRPC: `7233:7233` → `127.0.0.1:7233:7233`
- Temporal UI: `8080:8080` → `127.0.0.1:8080:8080`
- Polish Gate: `8090:8090` → `127.0.0.1:8090:8090`
- LiteLLM: `4000:4000` → `127.0.0.1:4000:4000`
- Langfuse: `3000:3000` → `127.0.0.1:3000:3000`

**Applied live on Beast:**
- `docker-postgres-1` (port 5432): restarted with `127.0.0.1` binding
- `amplified-crm` (port 8001): restarted with `127.0.0.1` binding
- `amplified-crm-dev` (port 8003): restarted with `127.0.0.1` binding
- `cove-api` (port 8081): restarted with `127.0.0.1` binding
- `cove-translator` (port 8092): restarted with `127.0.0.1` binding

### 2. DOCKER-USER iptables — Tailscale-aware + persistent

Script: `02_build/security/beast-docker-firewall.sh`

Rules:
1. ACCEPT established/related
2. RETURN tcp 80,443 from external NIC (public web traffic)
3. RETURN from `tailscale0` interface (trusted mesh)
4. DROP from external NIC (block everything else)
5. RETURN (docker internal traffic)

### 3. PostgreSQL `pg_hba.conf` hardening

Template: `02_build/security/pg_hba.beast.conf`

Restricts connections to:
- Unix socket (local)
- `127.0.0.1/32` (localhost)
- `172.16.0.0/12` (Docker bridge networks)
- `100.64.0.0/10` (Tailscale CGNAT range)

Rejects all other sources.

## Blockers for Ewan

### Tailscale authentication

The Tailscale container needs interactive login. Two options:

**Option A — Interactive auth (one-time):**
```bash
docker exec -it tailscale tailscale login
```
Then visit the auth URL in a browser signed into the Tailscale account.

**Option B — Auth key (headless):**
Generate a reusable auth key at https://login.tailscale.com/admin/settings/keys
and set `TS_AUTHKEY` in the container environment.

### Tailscale network integration

Once authenticated, the Tailscale container should be moved to `amplified-net`
so internal services can be reached via the Tailscale IP. Current network is
`openclaw_default` which is isolated.

### Credential rotation (carried forward from Phase 1)

Ewan to rotate: OpenAI, Anthropic, DeepSeek API keys.

---

*Devon-7ac0 | 2026-05-09 | devin-7ac006f9572f4fbc88862a485bff90d4*
