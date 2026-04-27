"""
Provisioning API Routes - Client onboarding automation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from prisma import Prisma
from src.db.client import get_prisma
from src.services.client_provisioning import (
    provision_client,
    ProvisioningResult,
    VERTICAL_PROMPTS,
)

router = APIRouter(prefix="/provisioning", tags=["provisioning"])


class ProvisioningStepResponse(BaseModel):
    name: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class ProvisioningResponse(BaseModel):
    success: bool
    client_id: str
    vapi_assistant_id: Optional[str] = None
    twilio_number: Optional[str] = None
    steps: List[ProvisioningStepResponse] = []
    errors: List[str] = []
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# Store results for async lookups (in-memory, would use Redis in production)
provisioning_results: Dict[str, ProvisioningResult] = {}


def _result_to_response(result: ProvisioningResult) -> ProvisioningResponse:
    """Convert dataclass result to Pydantic response model."""
    return ProvisioningResponse(
        success=result.success,
        client_id=result.client_id,
        vapi_assistant_id=result.vapi_assistant_id,
        twilio_number=result.twilio_number,
        steps=[
            ProvisioningStepResponse(
                name=s.name,
                status=s.status,
                result=s.result,
                error=s.error,
                started_at=s.started_at,
                completed_at=s.completed_at,
            )
            for s in result.steps
        ],
        errors=result.errors,
        started_at=result.started_at,
        completed_at=result.completed_at,
    )


@router.post("/provision/{client_id}")
async def start_provisioning(
    client_id: str,
    background_tasks: BackgroundTasks,
    db: Prisma = Depends(get_prisma),
):
    """
    Trigger provisioning for a client (async).
    Usually called automatically when onboarding completes.
    """
    # Verify client exists
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    async def run_provisioning():
        result = await provision_client(db, client_id)
        provisioning_results[client_id] = result
        if not result.success:
            print(f"Provisioning failed for {client_id}: {result.errors}")

    background_tasks.add_task(run_provisioning)

    return {
        "message": "Provisioning started",
        "client_id": client_id,
        "status_url": f"/api/v1/provisioning/status/{client_id}",
    }


@router.post("/provision/{client_id}/sync", response_model=ProvisioningResponse)
async def provision_client_sync(
    client_id: str,
    db: Prisma = Depends(get_prisma),
):
    """
    Trigger provisioning synchronously (for testing/debugging).
    Waits for completion and returns full result.
    """
    # Verify client exists
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    result = await provision_client(db, client_id)
    provisioning_results[client_id] = result

    return _result_to_response(result)


@router.get("/status/{client_id}")
async def get_provisioning_status(client_id: str):
    """Check provisioning status for a client."""
    if client_id in provisioning_results:
        result = provisioning_results[client_id]
        return {
            "status": "completed" if result.success else "failed",
            "success": result.success,
            "errors": result.errors,
            "vapi_assistant_id": result.vapi_assistant_id,
            "twilio_number": result.twilio_number,
            "started_at": result.started_at,
            "completed_at": result.completed_at,
        }

    return {
        "status": "pending",
        "message": "Provisioning in progress or not started",
    }


@router.post("/reprovision/{client_id}", response_model=ProvisioningResponse)
async def reprovision_client(
    client_id: str,
    db: Prisma = Depends(get_prisma),
):
    """
    Re-run provisioning (useful if something failed).
    Runs synchronously.
    """
    # Verify client exists
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    result = await provision_client(db, client_id)
    provisioning_results[client_id] = result

    return _result_to_response(result)


@router.get("/verticals")
async def list_verticals():
    """List available verticals and their prompts."""
    return {
        "verticals": list(VERTICAL_PROMPTS.keys()),
        "default": "default",
    }


@router.get("/verticals/{vertical}")
async def get_vertical_prompt(vertical: str):
    """Get the system prompt template for a vertical."""
    if vertical not in VERTICAL_PROMPTS:
        raise HTTPException(status_code=404, detail=f"Vertical not found: {vertical}")

    return {
        "vertical": vertical,
        "prompt_template": VERTICAL_PROMPTS[vertical],
    }
