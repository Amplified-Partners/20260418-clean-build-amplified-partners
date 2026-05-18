---
name: testing-vellum
description: Test the Vellum (Ledger) FastAPI app end-to-end. Use when verifying Vellum API routes, cron automation, baton pass, dashboard UI, or any changes to 02_build/vellum/.
---

# Testing Vellum

## Prerequisites

```bash
pip install fastapi uvicorn pydantic jinja2 httpx pytest pytest-asyncio
```

## Start the Server

```bash
cd /home/ubuntu/repos/clean-build
PYTHONPATH=02_build VELLUM_DEV_MODE=1 python -m uvicorn vellum.app:app --host 0.0.0.0 --port 8000
```

`VELLUM_DEV_MODE=1` generates a demo morning brief at startup so the dashboard has data.

## Run Unit Tests

```bash
PYTHONPATH=02_build python -m pytest 02_build/vellum/tests/ -v
```

Expected: 62+ tests pass.

## Run Lint

```bash
ruff check 02_build/vellum/
```

## Key API Endpoints

| Method | Path | Purpose |
|--------|------|--------|
| POST | /api/v1/baton | Receive baton pass from finishing agent |
| GET | /api/v1/baton/latest?tenant_id=ewan | Read most recent baton |
| POST | /api/v1/sheets/generate | Generate a new brief sheet |
| GET | /api/v1/sheets | List all sheets |
| GET | /api/v1/sheets/{id} | Get sheet with entries |
| GET | / | Dashboard UI |
| GET | /sheet/{id} | Sheet detail UI |
| GET | /docs | Swagger UI |

## Testing Baton Pass Round-Trip

1. POST a baton:
```bash
curl -X POST http://localhost:8000/api/v1/baton \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "agent_id": "Devon-test", "tenant_id": "ewan", "what_happened": "Test", "implications": "None", "actions_required": ["Verify"]}'
```

2. Read it back:
```bash
curl http://localhost:8000/api/v1/baton/latest?tenant_id=ewan
```

3. Verify on dashboard: navigate to http://localhost:8000/ and click into the sheet.

## Common Pitfalls

- **Store not initialised in API tests:** When using `AsyncClient` with `ASGITransport`, the lifespan context manager does NOT run. You must call `await init_store()` in your test fixture before creating the client.
- **Self-POST during startup:** In dev mode, the cron tries to POST to itself during lifespan startup. This always fails (server not ready yet). This is expected — graceful degradation logs the error and continues.
- **AsyncMock warnings:** Cron automation tests may emit `RuntimeWarning: coroutine was never awaited` from AsyncMock — these are cosmetic, not functional failures.
- **Port 8000 already in use:** Kill old processes with `kill -9 $(lsof -ti :8000)` before starting.

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|--------|
| VELLUM_DEV_MODE | 0 | Set to 1 for demo data generation |
| VELLUM_LEDGER_URL | http://localhost:8000 | Ledger endpoint for cron POST |
| VELLUM_POST_TIMEOUT | 10 | Timeout in seconds for httpx.post |

## Devin Secrets Needed

None required for local testing. For production/Beast deployment, `VELLUM_LEDGER_URL` would need to be configured.
