"""HTTP trigger for `PolishGateWorkflow` (AMP-73).

GitHub Actions on each gated repo POST `pr_id`/`pr_url`/`preview_url` here.
This service starts the Temporal workflow, waits for the result (the
workflow itself screenshots → scores → comments), and returns pass/fail
so the Action can mark the GitHub status check accordingly.

Run:
    uvicorn api.polish_gate:app --host 0.0.0.0 --port 8090

Auth: a single shared secret in `COVE_POLISH_GATE_TOKEN`. Set it on the
Cove side and as a repo / org secret on each gated repo.

Devon-29bf | 2026-05-04 | AMP-73 wire visual-polish-system into Cove
"""

from __future__ import annotations

import hmac
import os
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from temporalio.client import Client

from temporal.workflows.polish_gate_workflow import (
    PolishGateInput,
    PolishGateResult,
    PolishGateWorkflow,
)

TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TASK_QUEUE = os.getenv("COVE_TASK_QUEUE", "cove-build-queue")
SHARED_SECRET = os.getenv("COVE_POLISH_GATE_TOKEN", "")
DEFAULT_THRESHOLD = float(os.getenv("POLISH_GATE_THRESHOLD", "0.65"))
DEFAULT_RUBRIC = os.getenv(
    "POLISH_GATE_RUBRIC_PATH",
    "/opt/visual-polish-system/principles/references/rubric.json",
)
DEFAULT_RULES = os.getenv(
    "POLISH_GATE_RULES_PATH",
    "/opt/visual-polish-system/principles/rules/core.rules.json",
)
DEFAULT_REFS = os.getenv("POLISH_GATE_REFERENCES_DIR", "")


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Open one Temporal client at startup and reuse it for every request —
    # the gRPC channel is multiplexed, so a fresh connect per call would
    # waste a full TCP + HTTP/2 handshake under sustained PR load.
    app.state.temporal_client = await Client.connect(TEMPORAL_ADDRESS)
    try:
        yield
    finally:
        # temporalio.Client has no explicit close(); GC handles the channel.
        app.state.temporal_client = None


app = FastAPI(title="Cove Polish Gate", version="0.1.0", lifespan=_lifespan)


class PolishGateRequest(BaseModel):
    pr_id: str = Field(..., description="'owner/repo#number'")
    pr_url: str
    preview_url: str
    threshold: Optional[float] = None
    rubric_path: Optional[str] = None
    rules_path: Optional[str] = None
    references_dir: Optional[str] = None
    hard_check_results: dict[str, bool] = Field(default_factory=dict)
    wait: bool = True


class PolishGateResponse(BaseModel):
    workflow_id: str
    pr_id: str
    passed: Optional[bool]
    composite: Optional[float]
    threshold: float
    summary: Optional[str]
    error: Optional[str] = None


def _check_auth(token: Optional[str]) -> None:
    if not SHARED_SECRET:
        # In dev, no secret configured ⇒ allow all. In prod the env must set it.
        return
    # Constant-time comparison — the API is internet-facing once Beast's
    # firewall opens 8090, so naive `!=` would leak the secret one byte at a
    # time under timing analysis. (Layer 0: Privacy and Security First.)
    if token is None or not hmac.compare_digest(token, SHARED_SECRET):
        raise HTTPException(status_code=401, detail="invalid token")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/polish-gate", response_model=PolishGateResponse)
async def trigger_polish_gate(
    body: PolishGateRequest,
    x_cove_token: Optional[str] = Header(default=None, alias="X-Cove-Token"),
) -> PolishGateResponse:
    _check_auth(x_cove_token)

    client: Client = app.state.temporal_client
    workflow_id = f"polish-gate-{body.pr_id.replace('/', '_').replace('#', '-')}-{uuid.uuid4().hex[:8]}"

    handle = await client.start_workflow(
        PolishGateWorkflow.run,
        PolishGateInput(
            pr_id=body.pr_id,
            pr_url=body.pr_url,
            preview_url=body.preview_url,
            rubric_path=body.rubric_path or DEFAULT_RUBRIC,
            rules_path=body.rules_path or DEFAULT_RULES,
            references_dir=body.references_dir or DEFAULT_REFS,
            threshold=body.threshold if body.threshold is not None else DEFAULT_THRESHOLD,
            hard_check_results=body.hard_check_results,
        ),
        id=workflow_id,
        task_queue=TASK_QUEUE,
    )

    if not body.wait:
        return PolishGateResponse(
            workflow_id=workflow_id,
            pr_id=body.pr_id,
            passed=None,
            composite=None,
            threshold=body.threshold if body.threshold is not None else DEFAULT_THRESHOLD,
            summary=None,
        )

    result: PolishGateResult = await handle.result()
    return PolishGateResponse(
        workflow_id=workflow_id,
        pr_id=result.pr_id,
        passed=result.passed,
        composite=result.composite,
        threshold=result.threshold,
        summary=result.summary,
        error=result.error,
    )
