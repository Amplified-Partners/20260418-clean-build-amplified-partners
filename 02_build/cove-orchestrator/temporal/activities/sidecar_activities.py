from temporalio import activity
import logging

logger = logging.getLogger(__name__)

@activity.defn
async def emit_sidecar_signal(task_type: str, context: str, primary_action: str, secondary_action: str) -> str:
    """
    Pushes the payload to the external Sidecar UI (e.g. via FalkorDB or Redis).
    """
    logger.info(f"SIDECAR SIGNAL EMITTED: [{task_type}] {context}")
    # In reality, this would push to a Redis stream or Webhook that the React UI listens to.
    return "Signal Emitted"

@activity.defn
async def execute_downstream_action(task_type: str, context: str) -> str:
    """
    The actual heavy lifting. If Xero needs updating, it happens here.
    """
    logger.info(f"EXECUTING HEAVY LIFTING FOR: {task_type}")
    # Integration with Cove MCP servers would go here
    return "Action Executed Successfully"

@activity.defn
async def log_sidecar_receipt(task_type: str, time_saved: str) -> str:
    """
    Generates the daily receipt metric for the Sidecar UI.
    """
    logger.info(f"RECEIPT LOGGED: {task_type} - {time_saved}")
    return "Receipt Logged"
