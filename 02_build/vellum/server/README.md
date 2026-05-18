# Vellum Backend Server

Run locally. Never expose externally. Privacy, Security, Sovereignty.

## Start

```bash
cd 02_build
python -m uvicorn vellum.server.app:app --port 8000
```

Antigravity's React app (at localhost:5173) polls `http://localhost:8000/api/v1/workpackets/pending`.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v1/health` | Gate status, record count, chain head |
| GET | `/api/v1/workpackets/pending` | Antigravity's UI contract (packets + rubric_checks) |
| POST | `/api/v1/submit` | Submit a record to the ingestion gate |
| GET | `/api/v1/records` | All signed records (full detail) |
| GET | `/docs` | Interactive API docs (Swagger) |

## Principles

- Runs on YOUR iron only (Mac or Beast)
- No tunnels, no third-party exposure
- CORS allows localhost:5173 and localhost:3000 only
- All data stays local

Devon-b5dc | 2026-05-14
