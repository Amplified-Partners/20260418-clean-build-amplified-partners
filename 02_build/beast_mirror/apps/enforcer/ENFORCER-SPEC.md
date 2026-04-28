# The Enforcer — Production Compliance & Health Checking System

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2026-03-11  
**Environment**: Hetzner "The Beast" (AX162-R, 135.181.161.131)

---

## Overview

The Enforcer is Ewan's vision: *"the sort of base layer that makes us do it the right way so that every 10 minutes the enforcer's checking that it's being done right."*

It's a deterministic, Docker-native health checking system that validates infrastructure, data integrity, agent compliance, and operational hygiene—all without needing an LLM. It runs every 10 minutes (configurable) and reports structured results via FastAPI HTTP endpoints.

---

## Architecture

### Core Principles

1. **Deterministic**: No LLM, no external dependencies beyond core services
2. **Fast**: All checks complete in <30 seconds
3. **Graceful Degradation**: One check failing doesn't block others
4. **Structured Logging**: JSON format for machine parsing and alerting
5. **Docker-Native**: Reads Docker socket for container status
6. **Production-Ready**: Error handling, timeouts, retry logic

### Check Modules

| Module | Checks | Status Levels |
|--------|--------|---------------|
| `docker_health.py` | All expected containers running, status=running | pass/fail/warn |
| `database_health.py` | FalkorDB, PostgreSQL, Redis, Qdrant connectivity | pass/fail/warn |
| `traefik_health.py` | Traefik API responds, routes configured | pass/fail |
| `session_hygiene.py` | SESSION-STATE.md freshness and structure | pass/warn |
| `security_check.py` | fail2ban, firewall, SSH key authentication | pass/warn/fail |

### HTTP Endpoints

- **`GET /health`** — Quick health check (200 if healthy, 503 if critical issues)
- **`GET /health/detailed`** — Full check results with all details
- **`GET /metrics`** — Prometheus-compatible metrics

---

## Deployment

### Docker Compose Entry

```yaml
enforcer:
  build: /opt/amplified/apps/enforcer
  container_name: enforcer
  restart: unless-stopped
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
    - /opt/amplified/logs:/logs
  networks:
    - amplified-net
  environment:
    - CHECK_INTERVAL=600           # 10 minutes
    - ALERT_WEBHOOK_URL=          # Optional: Slack, PagerDuty, etc.
    - LANGFUSE_HOST=http://langfuse:3000
    - FALKORDB_HOST=falkordb
    - FALKORDB_PORT=6379
    - POSTGRES_HOST=postgres
    - POSTGRES_PORT=5432
    - REDIS_HOST=redis
    - REDIS_PORT=6379
    - QDRANT_HOST=qdrant
    - QDRANT_PORT=6333
    - SESSION_STATE_PATH=/opt/amplified/vault/00-handover/SESSION-STATE.md
    - MAX_SESSION_STATE_AGE_HOURS=24
    - FAIL2BAN_ENABLED=true
    - LOG_LEVEL=INFO
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.enforcer.rule=Host(`enforcer.beast.amplifiedpartners.ai`)"
    - "traefik.http.routers.enforcer.tls.certresolver=letsencrypt"
    - "traefik.http.services.enforcer.loadbalancer.server.port=8000"
  depends_on:
    - falkordb
    - postgres
    - redis
    - qdrant
    - traefik
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 5s
    retries: 3
    start_period: 10s
```

### Build and Run Locally

```bash
# Build the Docker image
docker build -t enforcer:latest /path/to/enforcer

# Run with environment variables
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e CHECK_INTERVAL=600 \
  -e FALKORDB_HOST=localhost \
  -e POSTGRES_HOST=localhost \
  -e REDIS_HOST=localhost \
  -e QDRANT_HOST=localhost \
  -p 8000:8000 \
  enforcer:latest
```

### Development (Local Testing)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run enforcer
python enforcer.py
```

Environment variables (in `.env`):
```
CHECK_INTERVAL=600
ALERT_WEBHOOK_URL=
FALKORDB_HOST=localhost
POSTGRES_HOST=localhost
REDIS_HOST=localhost
QDRANT_HOST=localhost
LOG_LEVEL=DEBUG
```

---

## Check Specifications

### Docker Health Check

**What it checks:**
- All expected containers (from `EXPECTED_CONTAINERS` env var) are present
- All containers have status = "running"
- No unexpected container restarts

**Severity levels:**
- ✅ **PASS**: All containers running
- ⚠️ **WARN**: One container unhealthy
- 🔴 **FAIL**: Multiple containers missing or unhealthy

**Timeout**: 2 seconds per check
**Fallback**: Reads Docker socket directly (no daemon API)

---

### Database Health Check

Checks connectivity to four critical services:

| Service | Protocol | Port | Check Method |
|---------|----------|------|--------------|
| FalkorDB | Redis | 6379 | PING command |
| PostgreSQL | TCP | 5432 | Connection attempt |
| Redis | Redis | 6379 | PING command |
| Qdrant | HTTP | 6333 | GET /health |

**Severity:**
- ✅ **PASS**: All 4 databases reachable
- ⚠️ **WARN**: 1 database unreachable
- 🔴 **FAIL**: 2+ databases unreachable

**Timeout**: 2 seconds per database

---

### Traefik Health Check

**What it checks:**
- Traefik API endpoint responds (`/ping`)
- HTTP status 200 received
- Router and service configuration loaded (via `/api/overview`)

**Severity:**
- ✅ **PASS**: API responding, routes configured
- ⚠️ **WARN**: API responds but no routes
- 🔴 **FAIL**: API not responding or timeout

**Timeout**: 3 seconds

---

### Session Hygiene Check

**Purpose**: Enforce the baton-pass protocol—ensures SESSION-STATE.md is current

**What it checks:**
1. File exists at configured path
2. Last updated timestamp is recent (default <24 hours)
3. Contains required sections:
   - "What Happened This Session"
   - "What This Means"
   - "Ewan Needs To Do"

**Severity:**
- ✅ **PASS**: File current, structure complete
- ⚠️ **WARN**: File is 24+ hours old, or missing sections
- 🔴 **FAIL**: File doesn't exist or can't be parsed

**Timestamp Parsing**: Extracts from line like:
```
> Last updated: 2026-03-11 ~18:00 UTC
```

---

### Security Check

**What it checks:**

1. **fail2ban** (if enabled)
   - Is fail2ban installed and running?
   - Are SSH jails active?

2. **Firewall (UFW)**
   - Is UFW active?
   - Are default policies set?

3. **SSH Key Authentication**
   - Is `~/.ssh/authorized_keys` present?
   - Does it contain keys?

**Severity:**
- ✅ **PASS**: All configured security measures active
- ⚠️ **WARN**: One security tool misconfigured
- 🔴 **FAIL**: Critical security tool down (fail2ban, firewall)

---

## Alert Webhooks

When critical issues are detected, The Enforcer can POST alerts to:

- **Slack**: Incoming Webhooks API
- **PagerDuty**: Webhook integration
- **Custom**: Any HTTP endpoint

**Alert Payload Format**:

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

To configure:
```bash
export ALERT_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## Observability

### Health Endpoints

**Quick health check** (used by Traefik health checks):
```bash
curl http://enforcer.beast.amplifiedpartners.ai:8000/health
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

**Detailed report**:
```bash
curl http://enforcer.beast.amplifiedpartners.ai:8000/health/detailed
```

### Prometheus Metrics

Available at `/metrics`:

```
enforcer_healthy 1                           # 1=healthy, 0=unhealthy
enforcer_checks_total 5                      # Total checks run
enforcer_check_status{check="docker_health"} 1
enforcer_check_duration_ms{check="docker_health"} 125
```

Scrape with:
```yaml
- job_name: enforcer
  static_configs:
    - targets: ['enforcer:8000']
  metrics_path: '/metrics'
  scrape_interval: 60s
```

### Structured Logging

All logs are JSON-formatted for easy parsing:

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

Stream logs:
```bash
docker logs -f enforcer | jq .
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHECK_INTERVAL` | 600 | Seconds between checks |
| `ALERT_WEBHOOK_URL` | "" | Webhook for critical alerts |
| `LOG_LEVEL` | INFO | DEBUG, INFO, WARNING, ERROR |
| `FALKORDB_HOST` | falkordb | FalkorDB hostname |
| `POSTGRES_HOST` | postgres | PostgreSQL hostname |
| `REDIS_HOST` | redis | Redis hostname |
| `QDRANT_HOST` | qdrant | Qdrant hostname |
| `SESSION_STATE_PATH` | `/opt/amplified/vault/00-handover/SESSION-STATE.md` | Path to baton-pass file |
| `MAX_SESSION_STATE_AGE_HOURS` | 24 | Max acceptable staleness |
| `FAIL2BAN_ENABLED` | true | Enable fail2ban checks |

### config.yaml

Full configuration with descriptions in `/enforcer/config.yaml`

---

## Performance Characteristics

### Typical Execution Times

| Check | Typical Time | Timeout |
|-------|--------------|---------|
| Docker health | 100-200ms | 5s |
| Database health | 200-400ms | 2s per database |
| Traefik health | 150-300ms | 3s |
| Session hygiene | 10-50ms | 2s |
| Security | 200-500ms | 2s per check |
| **Total** | **~700-1500ms** | **<30s guarantee** |

All checks run concurrently, so total time is the slowest check, not the sum.

---

## Error Handling

### Graceful Degradation

If a check fails:
1. Error is logged to JSON
2. Result marked as "fail" with error details
3. Other checks continue running
4. Overall health determined by worst severity

### Timeouts

Each check has a timeout (varies by check type). If timeout exceeded:
1. Check returns FAIL status
2. Error message includes "timeout"
3. Details section shows which service was unreachable

### Container Not Running

If enforcer container itself crashes:
1. Docker restart policy: `unless-stopped`
2. Healthy up/down cycle keeps service available
3. Health endpoint returns 503 if internal errors

---

## Troubleshooting

### Enforcer won't start

```bash
# Check logs
docker logs enforcer

# Verify Docker socket is mounted
docker inspect enforcer | grep docker.sock

# Test Docker connectivity
docker run -v /var/run/docker.sock:/var/run/docker.sock:ro \
  docker:latest docker ps
```

### Health check always failing

```bash
# SSH into The Beast, then:

# Check if all services are running
docker ps -a

# Test each database manually
redis-cli -h redis ping
psql -h postgres -U postgres -c "SELECT 1"

# Check Traefik
curl -i http://traefik:8080/ping

# View enforcer logs
docker logs -f enforcer
```

### SESSION-STATE.md not found

```bash
# Verify path
ls -la /opt/amplified/vault/00-handover/SESSION-STATE.md

# Update environment variable in docker-compose.yml
SESSION_STATE_PATH=/correct/path/to/SESSION-STATE.md

# Redeploy
docker-compose up -d enforcer
```

---

## Testing Locally

```bash
# Start Docker containers (if needed)
docker-compose up -d

# Run enforcer in virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python enforcer.py

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/detailed
curl http://localhost:8000/metrics
```

---

## Future Enhancements

Potential additions for v1.1+:

- Alert history and trending (which checks are flaky?)
- Custom check plugins (user-defined Python modules)
- Automatic remediation (restart containers, restart services)
- Langfuse integration for observability correlation
- Graph of check results over time (Grafana dashboard)
- Email alerts for summary reports (daily, weekly)
- Slack threading for related alerts

---

## References

- **Baton-Pass Protocol**: `/vault/00-handover/BATON-PASS-PROTOCOL.md`
- **Infrastructure Spec**: `/vault/09-infrastructure/`
- **Docker Compose**: `/opt/amplified/docker-compose.yml`
- **Hetzner Beast**: `135.181.161.131` (AX162-R)
