import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from temporalio.client import Client
from temporal.workflows.sidecar_workflow import SidecarPickToLightWorkflow
from temporal.workflows.dogfood_workflow import CouncilWorkflow

app = FastAPI(title="Sidecar Headless API")

# Allow React UI to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, this is locked down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")

class SignalRequest(BaseModel):
    decision: str

@app.post("/task/{workflow_id}/signal")
async def signal_task(workflow_id: str, request: SignalRequest):
    """
    Sends the YES/NO/SNOOZE signal to the waiting Temporal workflow.
    """
    try:
        client = await Client.connect(TEMPORAL_ADDRESS)
        handle = client.get_workflow_handle(workflow_id)
        # Send the signal to the workflow
        await handle.signal(SidecarPickToLightWorkflow.submit_decision, request.decision)
        return {"status": "success", "message": f"Signal '{request.decision}' sent to {workflow_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/task/dispatch")
async def dispatch_task(task_type: str, context: str, primary: str = "YES", secondary: str = "NO"):
    """
    Utility endpoint to manually dispatch a Sidecar task for testing the UI.
    """
    try:
        client = await Client.connect(TEMPORAL_ADDRESS)
        workflow_id = f"sidecar-task-{os.urandom(4).hex()}"
        await client.start_workflow(
            SidecarPickToLightWorkflow.run,
            args=[task_type, context, primary, secondary],
            id=workflow_id,
            task_queue="cove-task-queue",
        )
        return {"workflow_id": workflow_id, "message": "Task Dispatched"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CouncilRequest(BaseModel):
    prompt: str
    perplexity_key: str = ""
    antigravity_key: str = ""
    claude_key: str = ""

@app.post("/council")
async def consult_council(request: CouncilRequest):
    """
    Consults the Tri-Council (Perplexity, Antigravity, Claude) in parallel.
    """
    try:
        client = await Client.connect(TEMPORAL_ADDRESS)
        workflow_id = f"council-{os.urandom(4).hex()}"
        
        # execute_workflow waits for it to finish and returns the result!
        result = await client.execute_workflow(
            CouncilWorkflow.run,
            args=[request.prompt, request.perplexity_key, request.antigravity_key, request.claude_key],
            id=workflow_id,
            task_queue="cove-task-queue",
        )
        return {
            "status": "success", 
            "perplexity": result.perplexity,
            "antigravity": result.antigravity,
            "claude": result.claude
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn sidecar_api:app --reload --port 8001
