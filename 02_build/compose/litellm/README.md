# LiteLLM compose (mirror)

Mirror of `/opt/amplified/apps/litellm/docker-compose.yml` on Beast (`135.181.161.131`). Beast is the source-of-truth; this is for version control, review, and recovery.

## What it does

- Single `litellm` container on the `amplified-net` external network — proxy/gateway in front of every LLM provider used on Beast.
- `127.0.0.1:4000:4000` — host-loopback only, no LAN/WAN exposure (added by AMP-71).
- Reads secrets from `./.env` via `env_file:` (added by AMP-72 — see "Why no secrets here").
- `litellm_config.yaml` mounted at `/app/config.yaml` (model list, fallback chains).
- Redis cache host/port set inline (non-secret connection metadata).
- Traefik labels publish `litellm.beast.amplifiedpartners.ai` (HTTPS via Let's Encrypt).
- 2 GB memory cap.

## Why no secrets here

Before AMP-72, this compose embedded seven plaintext secrets (the LiteLLM master key, the Postgres URL with password, and five provider API keys) directly in the `environment:` block. That blocked version-control mirroring and made any `/opt/amplified/` snapshot a secret-leak.

The cleaned compose references `./.env` via `env_file:`. That file:

- Lives next to the compose at `/opt/amplified/apps/litellm/.env`.
- Mode `600`, owner `root` — readable only by root.
- **Not** committed to this repo and **not** mirrored anywhere outside Beast.
- Is the new target for the existing rotation script at `/opt/amplified/secrets/rotation/rotate-keys.sh` (also updated by AMP-72).

## How clients reach LiteLLM

| Caller location | URL |
|---|---|
| Container on `amplified-net` | `http://litellm:4000` (Docker DNS — canonical) |
| Process on the Beast host | `http://127.0.0.1:4000` |
| External (HTTPS, public) | `https://litellm.beast.amplifiedpartners.ai` |

## Reversibility

The pre-AMP-72 compose (with inline secrets) is backed up on Beast at `/opt/amplified/apps/litellm/docker-compose.yml.bak.20260504-amp72`. The pre-existing two-key `.env` is backed up at `.env.bak.20260504-amp72`. Reverting is a `cp` of either backup over the live file followed by `docker compose up -d --force-recreate litellm`.

## Updating this mirror

If you edit the compose on Beast, re-mirror with:

```bash
scp beast:/opt/amplified/apps/litellm/docker-compose.yml \
    02_build/compose/litellm/docker-compose.yml
```

Then commit. **Never** mirror `.env`. Mirror staleness is a known risk — Beast is canonical.

## Why the LiteLLM compose, not LiteLLM as a whole

The compose is the only file in the LiteLLM stack that's structural and re-creatable from scratch. The `litellm_config.yaml` (model list, fallback chains) is a separate concern — it doesn't reference any secret directly (every key is `os.environ/...`) so it could in principle also be mirrored, but it isn't yet because it's still iterating quickly and Beast is the working copy. Worth a follow-up ticket if change-tracking demands it.

---
*Devon-a9a7 | 2026-05-04 | AMP-72 LiteLLM secrets-to-env mirror*
