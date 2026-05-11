"""End-to-end proof that the legacy migration scripts will not run
against the canonical DB without the documented migration protocol.

We invoke `migrate_qdrant.py` and `migrate_falkordb.py` as subprocesses
with a clean environment. They should exit with code 2 (config error)
and emit the migration_guard refusal message on stderr before opening
any network/DB connections.

We deliberately do NOT test the "allowed" path here — that would
require a running Qdrant/FalkorDB/Postgres. The guard's allow-path is
covered by the unit tests in `test_migration_guard.py`; this test
proves the wiring of the guard into the script entrypoints.

Signed-by: Devon-AMP-302-C | 2026-05-11
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
MIGRATE_QDRANT = SCRIPTS_DIR / "migrate_qdrant.py"
MIGRATE_FALKORDB = SCRIPTS_DIR / "migrate_falkordb.py"


def _run_with_clean_env(script: Path) -> subprocess.CompletedProcess:
    # Strip any AMPLIFIED_MIGRATION_* vars that may exist in the
    # ambient test environment so we are truly simulating "operator
    # tried to run the legacy writer without the protocol".
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("AMPLIFIED_MIGRATION_")
    }
    # PYTHONPATH so the script can import migration_guard from package
    # root regardless of cwd.
    env["PYTHONPATH"] = str(SCRIPTS_DIR)
    return subprocess.run(
        [sys.executable, str(script)],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )


@pytest.mark.parametrize("script", [MIGRATE_QDRANT, MIGRATE_FALKORDB])
def test_legacy_writer_refuses_without_protocol(script):
    result = _run_with_clean_env(script)
    assert result.returncode == 2, (
        f"Expected exit 2 from {script.name} when run without protocol, "
        f"got {result.returncode}.\nstdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
    assert "REFUSING TO RUN" in result.stderr, (
        f"Expected the migration_guard refusal message on stderr from "
        f"{script.name}. Got: {result.stderr}"
    )
    assert "amplified_brain" in result.stderr or script.name in result.stderr
