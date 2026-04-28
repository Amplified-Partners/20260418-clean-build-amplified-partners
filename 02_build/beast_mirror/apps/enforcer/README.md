# The Enforcer — Production-Grade Compliance & Health System

**Version**: 1.0.0  
**Status**: Production Ready  
**Environment**: Hetzner "The Beast" (AX162-R, 135.181.161.131)  
**Built by**: Amplified Partners  

---

## What Is This?

The Enforcer is the **base layer** that ensures Amplified Partners infrastructure runs "the right way." It's Ewan's vision made real:

> *"I think the first thing to set up is the sort of base layer that makes us do it the right way so that every 10 minutes the enforcer's checking that it's being done right."*

Every 10 minutes, The Enforcer runs five deterministic health checks:

1. **Docker Health** — Are all expected containers running?
2. **Database Health** — Can we reach FalkorDB, PostgreSQL, Redis, Qdrant?
3. **Traefik Health** — Is the reverse proxy routing correctly?
4. **Session Hygiene** — Is SESSION-STATE.md current (baton-pass protocol)?
5. **Security** — Is fail2ban active, firewall up, SSH keys configured?

If anything fails, it alerts (via webhook), and the system degrades gracefully. No containers restart, no LLM needed—just deterministic Python checks running as a Docker service.

---

## Architecture

### File Structure

```
enforcer/
├── enforcer.py                 # Main FastAPI application (370 lines)
├── checks/
│   ├── __init__.py
│   ├── docker_health.py        # Check Docker containers
│   ├── database_health.py      # Check database connectivity
│   ├── traefik_health.py       # Check reverse proxy
│   ├── session_hygiene.py      # Check baton-pass protocol
│   └── security_check.py       # Check security baseline
├── Dockerfile                  # Alpine Python 3.12 image
├── requirements.txt            # 8 Python dependencies
├── config.yaml                 # Full configuration
├── docker-compose-entry.yml    # Docker Compose service definition
├── ENFORCER-SPEC.md            # Detailed specification
├── .dockerignore                # Exclude files from Docker build
└── .gitignore                  # Exclude files from git
```

### Check Execution Flow

```
START EVERY 10 MINUTES
↓
Run 5 checks concurrently:
  1. Docker health          (100-200ms)
  2. Database health        (200-400ms)
  3. Traefik health         (150-300ms)
  4. Session hygiene        (10-50ms)
  5. Security checks        (200-500ms)
↓
Gather results (worst severity determines overall status)
↓
Log JSON structured output
↓
If critical issues: POST to alert webhook
↓
If healthy: return 200 to /health endpoint
If unhealthy: return 503 to /health endpoint
```

---

## Quick Start

### 1. Copy to Hetzner Beast

```bash
# On The Beast, create the directory
ssh root@135.181.161.131
mkdir -p /opt/amplified/apps/enforcer
cd /opt/amplified/apps/enforcer

# Copy all files from this directory
# (assuming you've cloned the agent-stack repo)
cp -r /path/to/agent-stack/enforcer/* /opt/amplified/apps/enforcer/
```

### 2. Add to docker-compose.yml

```bash
# On The Beast, edit your docker-compose.yml
cat docker-compose-entry.yml >> /opt/amplified/docker-compose.yml
```

### 3. Build and Deploy

```bash
# On The Beast
cd /opt/amplified
docker-compose build enforcer
docker-compose up -d enforcer

# Verify it's running
docker ps | grep enforcer
docker logs enforcer
```

### 4. Test the Endpoints

```bash
# Quick health check
curl http://enforcer.beast.amplifiedpartners.ai:8000/health

# Detailed report
curl http://enforcer.beast.amplifiedpartners.ai:8000/health/detailed

# Prometheus metrics
curl http://enforcer.beast.amplifiedpartners.ai:8000/metrics
```

---

## Development Locally

### Prerequisites

- Python 3.12+
- Docker (with docker-compose)
- Packages: redis, postgres, etc. (optional for local testing)

### Setup

```bash
# Clone agent-stack repo
cd agent-stack/enforcer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and configure
cp .env.example .env
# Edit .env with your local Docker container IPs
```

### Run

```bash
# Start Docker containers (if you have docker-compose running locally)
docker-compose up -d

# Run enforcer
python enforcer.py

# In another terminal, test
curl http://localhost:8000/health
curl http://localhost:8000/health/detailed
```

### Environment Variables

Create `.env` file:

```
CHECK_INTERVAL=600
ALERT_WEBHOOK_URL=
FALKORDB_HOST=localhost
POSTGRES_HOST=localhost
REDIS_HOST=localhost
QDRANT_HOST=localhost
SESSION_STATE_PATH=/Users/amplifiedpartners/vault/00-handover/SESSION-STATE.md
LOG_LEVEL=DEBUG
```

---

## Check Specifications

### Docker Health

**What**: Are all expected containers running?  
**Status**:
- ✅ PASS — All expected containers in "running" state
- ⚠️ WARN — One container unhealthy
- 🔴 FAIL — Multiple containers missing

**Config**: Set `EXPECTED_CONTAINERS` env var (default: traefik, falkordb, postgres, redis, qdrant, langfuse, portainer)

### Database Health

**What**: Can we ping all database services?  
**Databases checked**:
- FalkorDB (Redis module on :6379)
- PostgreSQL (:5432)
- Redis (:6379)
- Qdrant (:6333)

**Status**:
- ✅ PASS — All 4 databases reachable
- ⚠️ WARN — 1 database unreachable
- 🔴 FAIL — 2+ databases unreachable

**Timeout**: 2 seconds per database

### Traefik Health

**What**: Is the reverse proxy responding and routing?  
**Checks**:
- Traefik API endpoint responds (`/ping`)
- HTTP status 200
- Routes configured (via `/api/overview`)

**Status**:
- ✅ PASS — API responsive, routes loaded
- ⚠️ WARN — API responding, no routes
- 🔴 FAIL — API not responding

**Timeout**: 3 seconds

### Session Hygiene

**What**: Is SESSION-STATE.md current (baton-pass protocol)?  
**Checks**:
1. File exists
2. Last updated timestamp <24 hours old
3. Contains required sections

**Status**:
- ✅ PASS — File current and complete
- ⚠️ WARN — File stale or sections missing
- 🔴 FAIL — File doesn't exist

**Why it matters**: Ewan's rule—every session ends with updated SESSION-STATE.md. This check enforces it.

### Security

**What**: Is the security baseline met?  
**Checks**:
1. fail2ban installed and running (if enabled)
2. UFW firewall active
3. SSH authorized_keys configured

**Status**:
- ✅ PASS — All security measures active
- ⚠️ WARN — One security measure misconfigured
- 🔴 FAIL — Critical security tool down

---

## HTTP Endpoints

### `GET /health` — Quick Health Check

Returns 200 if healthy, 503 if critical issues.

```bash
curl -i http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-03-11T18:00:00Z",
  "last_check": "2026-03-11T17:59:30Z",
  "checks": [
    {
      "name": "docker_health",
      "status": "pass",
      "severity": "info",
      "duration_ms": 125
    }
  ]
}
```

### `GET /health/detailed` — Full Report

```bash
curl http://localhost:8000/health/detailed
```

Response:
```json
{
  "timestamp": "2026-03-11T18:00:00Z",
  "overall_health": "healthy",
  "last_check": "2026-03-11T17:59:30Z",
  "checks": [
    {
      "name": "docker_health",
      "status": "pass",
      "message": "All 7 expected containers running",
      "severity": "info",
      "timestamp": "2026-03-11T17:59:30Z",
      "duration_ms": 125,
      "details": {
        "total_containers": 7,
        "expected": 7,
        "running": ["traefik", "falkordb", "postgres", ...]
      }
    }
  ],
  "config": {
    "check_interval_seconds": 600,
    "expected_containers": [...]
  }
}
```

### `GET /metrics` — Prometheus Metrics

```bash
curl http://localhost:8000/metrics
```

Output (text format):
```
# HELP enforcer_healthy Overall system health (1=healthy, 0=unhealthy)
# TYPE enforcer_healthy gauge
enforcer_healthy 1

# HELP enforcer_checks_total Total number of checks run
# TYPE enforcer_checks_total counter
enforcer_checks_total 5

enforcer_check_status{check="docker_health"} 1
enforcer_check_duration_ms{check="docker_health"} 125
enforcer_check_status{check="database_health"} 1
enforcer_check_duration_ms{check="database_health"} 280
...
```

---

## Logging

All logs are JSON-formatted for easy machine parsing:

```json
{
  "timestamp": "2026-03-11T18:00:00Z",
  "level": "INFO",
  "event": "check_cycle_complete",
  "total_checks": 5,
  "critical_issues": 0,
  "overall_health": "healthy",
  "duration_ms": 1250
}
```

View logs:

```bash
# Real-time logs
docker logs -f enforcer

# Pretty-print JSON logs
docker logs enforcer | jq .

# Filter by severity
docker logs enforcer | jq 'select(.level=="ERROR")'
```

---

## Alert Webhooks

When critical issues occur, POST to a webhook:

```bash
export ALERT_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
docker-compose up -d enforcer
```

Payload sent to webhook:

```json
{
  "timestamp": "2026-03-11T18:00:00Z",
  "severity": "critical",
  "check": "docker_health",
  "message": "Container 'falkordb' is not running",
  "details": {
    "missing_containers": ["falkordb"],
    "total_containers": 6,
    "expected": 7
  }
}
```

Supported webhook platforms:
- **Slack**: Incoming Webhooks
- **PagerDuty**: Webhook integration
- **Custom**: Any HTTP endpoint

---

## Performance

### Execution Time

| Check | Typical | Max |
|-------|---------|-----|
| Docker | 100-200ms | 5s |
| Databases | 200-400ms | 2s/db |
| Traefik | 150-300ms | 3s |
| Session | 10-50ms | 2s |
| Security | 200-500ms | 2s |
| **Total** | **~700-1500ms** | **<30s** |

All checks run **concurrently**, so total time ≈ slowest check, not sum.

### Resource Usage

- **CPU**: <5% during checks (0% idle)
- **Memory**: ~50-80MB (Alpine Python)
- **Network**: Negligible (~1KB per check cycle)
- **Disk**: Logs only (configure rotation)

---

## Troubleshooting

### Enforcer won't start

```bash
# Check Docker logs
docker logs enforcer

# Verify Docker socket is mounted
docker inspect enforcer | grep -A5 Mounts

# Test Docker connectivity manually
docker run -v /var/run/docker.sock:/var/run/docker.sock:ro \
  docker:latest docker ps
```

### Health checks always failing

```bash
# SSH into The Beast
ssh root@135.181.161.131

# Check individual services
redis-cli -h redis ping
psql -h postgres -U postgres -c "SELECT 1"
curl -i http://traefik:8080/ping

# View detailed enforcer logs
docker logs -f enforcer | jq .
```

### SESSION-STATE.md not found

```bash
# Verify the file exists
ls -la /opt/amplified/vault/00-handover/SESSION-STATE.md

# Update docker-compose.yml
SESSION_STATE_PATH=/correct/path/SESSION-STATE.md

# Redeploy
docker-compose up -d enforcer
```

---

## Configuration

See `config.yaml` for full configuration options.

Key environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CHECK_INTERVAL` | 600 | Seconds between checks |
| `LOG_LEVEL` | INFO | DEBUG, INFO, WARNING, ERROR |
| `ALERT_WEBHOOK_URL` | "" | URL for critical alerts |
| `FALKORDB_HOST` | falkordb | FalkorDB hostname |
| `SESSION_STATE_PATH` | `/opt/amplified/vault/00-handover/SESSION-STATE.md` | Path to baton-pass file |
| `MAX_SESSION_STATE_AGE_HOURS` | 24 | Max acceptable file age |

---

## Future Enhancements

Planned for v1.1+:

- **Alert history** — Track which checks are flaky
- **Custom plugins** — User-defined Python check modules
- **Auto-remediation** — Restart containers, restart services
- **Grafana dashboard** — Visualize check results over time
- **Email summaries** — Daily/weekly reports
- **Slack threading** — Group related alerts
- **Langfuse integration** — Correlate with LLM observability

---

## References

- **Full Spec**: See `ENFORCER-SPEC.md`
- **Docker Compose Entry**: See `docker-compose-entry.yml`
- **Configuration**: See `config.yaml`
- **Baton-Pass Protocol**: `/vault/00-handover/BATON-PASS-PROTOCOL.md`
- **Hetzner Beast**: `135.181.161.131` (AX162-R Ultra, Helsinki)

---

## Support

**Questions?** See ENFORCER-SPEC.md for detailed technical documentation.

**Issues?** Check Docker logs with `docker logs enforcer | jq .`

**Ewan**: This is the foundation. Use it. Depend on it. It keeps the lights on.
