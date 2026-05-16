---
name: testing-ingestion-pipeline
description: Test the cove-orchestrator ingestion pipeline (PUDDING labeller, packet structure, Cypher escaping, migrations). Use when verifying changes to ingestion_activities.py or related migrations.
---

# Testing the Ingestion Pipeline

## Environment Setup

```bash
cd 02_build/cove-orchestrator
pip install temporalio pytest pytest-asyncio
```

`temporalio` is required to import from `temporal.activities.ingestion_activities`. The module-level import of `temporalio` will fail without it.

## Importable Functions

The deterministic labeller functions can be imported directly for unit testing without a database:

```python
from temporal.activities.ingestion_activities import (
    _detect_what, _detect_how, _detect_scale, _detect_time,
    _detect_patterns, _extract_bridge_terms, _label_content,
    _HOW_COMPRESSED, _TIME_COMPRESSED,
    SIGNED_BY, PIPELINE_VERSION, PATTERN_CODES,
    PuddingResult, PuddingInput,
)
```

## What Can Be Tested Without a Database

- `_label_content(content, filepath)` — deterministic labelling, returns dict with all dimension fields
- `_extract_bridge_terms(text)` — cross-domain signal detection, returns list (max 10)
- `_detect_what/how/scale/time/patterns` — individual dimension detectors
- `_esc()` — Cypher string literal escaping (defined inside `run_pudding_extraction`, test by mirroring the logic: `val.replace('\\', '\\\\').replace("'", "''")`)
- `PATTERN_CODES` dict (33 entries), `_HOW_COMPRESSED`, `_TIME_COMPRESSED` mappings
- Migration SQL file validation (schema checks, column presence, index correctness)
- Code inspection via `inspect.getsource()` for error handling patterns

## What Requires a Live Database (Beast)

- Packet INSERT + upsert (pudding_packets table)
- AGE graph MERGE (business_brain graph)
- Audit log INSERT
- Recurrence count increment under concurrent load
- Migration execution

## Running Tests

```bash
cd 02_build/cove-orchestrator
python3 -m pytest tests/ -v --tb=short --ignore=tests/test_polish_gate_api_auth.py
```

Note: `test_polish_gate_api_auth.py` requires `fastapi` which might not be installed. Use `--ignore` to skip it if needed.

## Test Patterns Used in This Repo

- `conftest.py` adds repo root to `sys.path` so `temporal.*` imports work
- `pytest.ini` sets `asyncio_mode = auto` and `testpaths = tests`
- Existing tests use class-based organization (`class TestXxx:`) with descriptive docstrings
- Async tests use `@pytest.mark.asyncio` decorator
- Tests are designed to run without live infrastructure (in-memory data)

## Key Constants to Verify

- `SIGNED_BY` should be `"brain_writer_pipeline"` (not a session UUID)
- `PIPELINE_VERSION` should be `"v2-deterministic"`
- `PATTERN_CODES` should have 33 entries, all non-empty string values

## Devin Secrets Needed

None for unit testing. Integration testing on Beast would require:
- `BRAIN_DSN` — PostgreSQL connection string for amplified_brain database
- `ANTHROPIC_API_KEY` — for AI enrichment testing (optional)
