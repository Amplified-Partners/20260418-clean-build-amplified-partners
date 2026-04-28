from datetime import timedelta
from temporalio import workflow

# Import our activities
with workflow.unsafe.imports_passed_through():
    from temporal.activities.sidecar_activities import (
        emit_sidecar_signal,
        execute_downstream_action,
        log_sidecar_receipt,
    )

@workflow.defn
class SidecarPickToLightWorkflow:
    """
    The Headless Sidecar Workflow (Principle 3: Zero-Friction Entry).
    This workflow waits for an asynchronous human signal (YES/NO) from the Sidecar UI.
    """
    def __init__(self) -> None:
        self.human_decision: str = ""
        self.is_resolved: bool = False

    @workflow.signal
    def submit_decision(self, decision: str) -> None:
        """
        The Sidecar UI sends 'YES', 'NO', 'SNOOZE' back to this signal.
        """
        self.human_decision = decision
        self.is_resolved = True

    @workflow.run
    async def run(self, task_type: str, context: str, primary_action: str, secondary_action: str) -> dict:
        # 1. Emit the signal to the external UI (via DB or webhook)
        # This pushes the task to the React Sidecar
        await workflow.execute_activity(
            emit_sidecar_signal,
            args=[task_type, context, primary_action, secondary_action],
            schedule_to_close_timeout=timedelta(seconds=10),
        )

        # 2. Halt execution until the human presses a button on the UI
        # This is the 'Interruption Tax' eliminated. We wait gracefully without holding compute.
        await workflow.wait_condition(lambda: self.is_resolved)

        # 3. Process the decision
        result = {"decision": self.human_decision, "executed": False}
        if self.human_decision == "YES":
            # Execute the heavy lifting (Xero, DocuSign, etc)
            action_result = await workflow.execute_activity(
                execute_downstream_action,
                args=[task_type, context],
                schedule_to_close_timeout=timedelta(minutes=5),
            )
            result["executed"] = True
            result["details"] = action_result
            
            # Log the receipt (Principle: Ephemeral Processing + Logging)
            await workflow.execute_activity(
                log_sidecar_receipt,
                args=[task_type, "1 hr 9 mins saved"],
                schedule_to_close_timeout=timedelta(seconds=10),
            )

        return result
