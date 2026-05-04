# enforcer

Health monitoring and enforcement for Amplified Partners infrastructure on Beast.

## What It Does

Runs 5 health checks on 10-minute cycles across all Beast services. Monitors container health, API responsiveness, database connectivity, session hygiene, and security posture. Alerts on degradation before failures cascade.

See `ENFORCER-SPEC.md` for the canonical spec and `enforcer.py:142-166` for the check list.

## Monitored Services

The enforcer's `EXPECTED_CONTAINERS` is configurable. As deployed in `docker-compose.yml:31` it monitors 11 containers; the fallback in `config.yaml:72-79` lists 7. The actual list runs at runtime via the `EXPECTED_CONTAINERS` env var.

`docker-compose.yml` (currently-deployed list, 11 containers):

- `traefik` — reverse proxy
- `falkordb` — graph database
- `postgres` — relational database
- `redis` — cache / message broker
- `qdrant` — vector database
- `langfuse` — LLM observability
- `portainer` — container UI
- `openclaw-agents` — agent runtime
- `litellm` — LLM routing proxy
- `searxng` — metasearch
- `ollama` — local LLM inference

Plus database-connectivity probes for FalkorDB, PostgreSQL, Redis, Qdrant; HTTP/TCP probe for Traefik (ports 80/443/8080); session-state freshness on `SESSION_STATE_PATH`; security checks (firewall, SSH key auth — note `fail2ban_enabled` flag is currently a no-op, see Known Issue below).

## Known Issue (flagged for follow-up)

The five check functions (`_check_redis`, `_check_falkordb`, `_check_postgres`, `_check_qdrant` in `checks/database_health.py`, `check_docker_health` in `checks/docker_health.py`, `check_security` in `checks/security_check.py`) are declared `async` but use **synchronous, blocking I/O** inside (`redis.Redis.ping`, `socket.connect_ex`, `docker.from_env`, `subprocess.run`). When scheduled via `asyncio.gather` in `enforcer.py:179`, the blocking calls prevent the event loop from making progress — so checks effectively run sequentially, and the FastAPI `/health` endpoint cannot respond while a cycle is in flight.

This contradicts the documented behaviour in `ENFORCER-SPEC.md` ("All checks run concurrently, so total time is the slowest check, not the sum").

**Production impact:** under degraded conditions (services timing out at 2s each) total cycle time can be ~10s instead of ~2s; Docker's own healthcheck on this container can also flap during that window. Source-repo bug, preserved verbatim by the AMP-77 merge so behaviour is unchanged from what is currently deployed on Beast.

**Fix path:** swap to `redis.asyncio.Redis`, `asyncio.open_connection`, `asyncio.create_subprocess_exec`, or wrap blocking calls in `loop.run_in_executor`. Tracked separately from this merge.

### `fail2ban_enabled` config flag is accepted but ignored

`checks/security_check.py:check_security` accepts a `fail2ban_enabled` argument (passed from `config.yaml` and `enforcer.py:166`) but never references it in the function body. The function only checks firewall and SSH-key auth — fail2ban is silently skipped regardless of the flag. `ENFORCER-SPEC.md` lists fail2ban as one of the security checks, so the spec and implementation disagree.

**Production impact:** the `fail2ban_enabled: true` config setting on Beast does nothing today. Fail2ban status is not actually monitored by the enforcer.

**Fix path:** add a `subprocess.run(['systemctl', 'is-active', 'fail2ban'], ...)`-style probe (or, since the enforcer runs in-container, a host-mount or DBus call) when `fail2ban_enabled` is true; merge its result into the security details. Tracked separately from this merge.

### `config.yaml` is not loaded — env vars are the only configuration source

`enforcer.py:29` imports `yaml` but never reads `config.yaml`. `EnforcerConfig.__init__` (`enforcer.py:59-91`) populates every setting from environment variables only. `ENFORCER-SPEC.md` and `IMPLEMENTATION-SUMMARY.md` describe `config.yaml` as an active configuration source, but it is documentation-only at runtime.

**Production impact:** an operator editing `config.yaml` (e.g. to change check intervals, expected containers, or thresholds) sees no behavioural change — the file is inert. All deployed config flows through `docker-compose.yml`'s `environment:` block.

**Fix path:** either implement YAML loading in `EnforcerConfig.__init__` as a fallback when env vars are not set, or remove the unused `import yaml` and update the spec to call `config.yaml` documentation-only. Tracked separately from this merge.

### Docker check has no WARN tier — single missing container flips `/health` to 503

`ENFORCER-SPEC.md:151-153` defines three severity tiers for the Docker check (PASS, WARN, FAIL), but `checks/docker_health.py:75-96` collapses WARN and FAIL: any non-empty `missing or unhealthy` list returns `status='fail', severity='critical'`. There is no code path that returns `status='warn'`. Note that `checks/database_health.py:128` *does* implement the two-tier split (`severity='critical' if len(failed) >= 2 else 'warning'`), so the Docker check is inconsistent with its sibling and with the spec.

**Production impact:** a single non-critical container going down (e.g. `portainer`, `langfuse`) immediately sets `severity='critical'`; `enforcer.py:190-191` flips `is_healthy=False`; `/health` returns HTTP 503 instead of the spec's intended warning-only behaviour. This makes the enforcer noisier than designed and can flap Docker's own healthcheck on the enforcer container.

**Fix path:** mirror `database_health.py:128` — `severity='critical' if (len(missing) + len(unhealthy)) >= 2 else 'warning'`, and `status='fail' if (...) >= 2 else 'warn'`. Tracked separately from this merge.

---

*Extracted from Beast `/opt/amplified/apps/enforcer/` by Devon | 2026-04-30 | session `aa4d863ad679468692e75a40b8825358`*
*Merged into `02_build/enforcer/`: Devon | 2026-05-04 | session devin-1bdaf31798874921940598bed17ca9e3 | AMP-77 spine cleanup*
