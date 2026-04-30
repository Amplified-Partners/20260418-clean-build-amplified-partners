<!-- Transfer metadata -->
<!-- Status: [NON-AUTHORITATIVE] -->
<!-- Sanitisation: done — no PII detected in source -->
<!-- Source: Amplified-Partners/beautiful-and-golden sibling repo, copied before tombstoning (2026-04-26) -->

# Technical Architecture: The Gentle Sidecar

## Overview
A decoupled, event-driven architecture designed for **safety** and **observability**.

## Components

### 1. The Ghost (The Listener)
- **Language**: Python
- **Role**: Read-Only observer of Legacy Logs/DBs.
- **Mechanism**: Tail logs, read replica DBs, listen to TCP packets (if strictly needed and allowed).
- **Safety**: **NEVER WRITES** to the Legacy System.

### 2. The Miner (The Analyst)
- **Language**: Python (Pandas, NumPy)
- **Role**: Process raw data from The Ghost and SaaS APIs.
- **Output**: Clean, structured JSON/Parquet models.
- **Consent**: Requires explicit API keys/Database credentials from the user.

### 3. The Scout (The Context)
- **Language**: Python
- **Role**: Fetch public market data, benchmarks, and trends.
- **Source**: Public APIs, Open Data sets.

### 4. The Bridge (The API)
- **Language**: Go (for concurrency/stability) or Fast API (Python) for speed of dev.
- **Role**: Serves the Clean Data to the UI or 3rd party apps.
- **Security**: Air-gapped from direct Write access to Legacy.

### 5. The Watchdog (The Failsafe)
- **Language**: Bash / Minimal Python
- **Role**: External monitoring process.
- **Action**: Kills "The Ghost" or "The Bridge" if CPU usage spikes > 5% or if any unauthorized write is detected.

## Tech Stack (Tentative)
- **Glue**: Python 3.11+
- **Database (Sidecar)**: SQLite (simple, file-based) or DuckDB (analytical).
- **API**: FastAPI (Python).
- **Frontend**: HTML5 / Vanilla JS (Lightweight).

---

Archived by **Devon** (Devin session `devin-ab66d8a5c2b64927b65a4ab87acc47ee`) — 2026-04-26
