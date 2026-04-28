import asyncio
import argparse
from temporalio.client import Client
from temporal.workflows.sidecar_workflow import SidecarPickToLightWorkflow

async def main():
    parser = argparse.ArgumentParser(description="Trigger a Headless Sidecar Pick-to-Light Task")
    parser.add_argument('--task', type=str, default="HANDOVER DETECTED")
    parser.add_argument('--context', type=str, default="Sarah just quoted the Jesmond job. Mirror quote amount (£450) to Xero?")
    parser.add_argument('--primary', type=str, default="YES")
    parser.add_argument('--secondary', type=str, default="NO")
    parser.add_argument('--signal', type=str, help="Send a signal (YES/NO/SNOOZE) to an existing workflow ID")
    parser.add_argument('--workflow_id', type=str, default="sidecar-task-002")
    
    args = parser.parse_args()

    # Connect to the local Temporal cluster
    client = await Client.connect("localhost:7233")
    
    if args.signal:
        print(f"[SIDECAR] Sending '{args.signal}' signal to workflow {args.workflow_id}...")
        handle = client.get_workflow_handle(args.workflow_id)
        await handle.signal(SidecarPickToLightWorkflow.submit_decision, args.signal)
        print("[SIDECAR] Signal sent successfully. Workflow resuming.")
        return

    print(f"[SIDECAR] Dispatching Headless Workflow: {args.workflow_id}")
    # Start the workflow
    handle = await client.start_workflow(
        SidecarPickToLightWorkflow.run,
        args=[args.task, args.context, args.primary, args.secondary],
        id=args.workflow_id,
        task_queue="cove-task-queue",
    )
    
    print(f"[SIDECAR] Workflow started. Waiting for human signal... (Run this script with --signal YES --workflow_id {args.workflow_id} to resolve)")
    
    # Wait for completion
    result = await handle.result()
    print(f"\n[SIDECAR] Workflow Completed!\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())
