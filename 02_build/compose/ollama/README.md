# Ollama compose (mirror)

Mirror of `/opt/amplified/apps/ollama/docker-compose.yml` on Beast (`135.181.161.131`). Beast is the source-of-truth; this is for version control, review, and recovery.

## What it does

- Single `ollama` container on the `amplified-net` external network.
- `127.0.0.1:11434:11434` — host-loopback only, no LAN/WAN exposure.
- `OLLAMA_HOST=0.0.0.0` — bind inside the container so Docker's port-proxy can reach it.
- 96 GB memory cap, 48 GB reservation, **48 logical-CPU cap** (added 2026-05-04 per AMP-75 — the 70B runner had been hitting 4806 % CPU and pushing host load >46). Sized for the 70B model on Beast's 252 GB box / 96-thread CPU.
- Traefik labels publish `ollama.beast.amplifiedpartners.ai` (HTTPS via Let's Encrypt).

## How clients reach it

| Caller location | URL |
|---|---|
| Container on `amplified-net` | `http://ollama:11434` (Docker DNS — canonical, see `02_build/routing/path_abstraction.py`) |
| Process on the Beast host | `http://127.0.0.1:11434` |
| External (HTTPS, public) | `https://ollama.beast.amplifiedpartners.ai` |

## Reversibility

Removing the `ports:` block and running `docker compose up -d ollama` reverts to the pre-AMP-46 state (in-network only). Removing the `cpus:` line under `deploy.resources.limits` and re-running the same command reverts the AMP-75 cap (back to unlimited host CPU).

## Updating this mirror

If you edit the compose on Beast, re-mirror with:

```bash
scp beast:/opt/amplified/apps/ollama/docker-compose.yml \
    02_build/compose/ollama/docker-compose.yml
```

Then commit. Mirror staleness is a known risk — Beast is canonical.

---
*Devon-a9a7 | 2026-05-03 | AMP-46 Ollama port-mapping fix mirror*
*Devon-aacb | 2026-05-04 | AMP-75 Ollama CPU cap (`cpus: '48'`)*
