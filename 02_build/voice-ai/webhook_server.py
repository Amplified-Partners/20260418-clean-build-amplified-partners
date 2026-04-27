"""
Simple webhook server for Telnyx → Retell AI integration
Runs standalone without full CRM dependencies
"""
import os
import logging
from fastapi import FastAPI, Request
import httpx
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telnyx Webhook Server")

# Configuration — load from environment only (never hardcode credentials)
RETELL_API_KEY = os.getenv("RETELL_API_KEY")
RETELL_AGENT_ID = os.getenv("RETELL_AGENT_ID")
TELNYX_API_KEY = os.getenv("TELNYX_API_KEY")

if not all([RETELL_API_KEY, RETELL_AGENT_ID, TELNYX_API_KEY]):
    raise ValueError("Missing required environment variables: RETELL_API_KEY, RETELL_AGENT_ID, TELNYX_API_KEY")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/retell/webhook/call-incoming")
async def telnyx_incoming_call(request: Request):
    """
    Webhook called by Telnyx when customer calls our number.
    """
    try:
        body = await request.json()
        logger.info(f"📞 Incoming call from Telnyx: {body.get('data', {}).get('event_type')}")

        # Extract call details
        payload = body.get("data", {}).get("payload", {})
        call_control_id = payload.get("call_control_id")
        from_number = payload.get("from")
        to_number = payload.get("to")

        logger.info(f"Call: {from_number} → {to_number}")
        logger.info(f"Call Control ID: {call_control_id}")

        if not call_control_id:
            logger.error("❌ No call_control_id in webhook")
            return {"status": "error", "message": "No call_control_id"}

        # Create Retell AI phone call
        logger.info("🤖 Creating Retell AI call...")
        async with httpx.AsyncClient() as client:
            retell_response = await client.post(
                "https://api.retellai.com/create-phone-call",
                headers={
                    "Authorization": f"Bearer {RETELL_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "from_number": to_number,  # Our number
                    "to_number": from_number,   # Customer
                    "agent_id": RETELL_AGENT_ID,
                    "metadata": {
                        "telnyx_call_id": call_control_id
                    }
                },
                timeout=10.0
            )

            logger.info(f"Retell response: {retell_response.status_code}")

            if retell_response.status_code in [200, 201]:
                retell_data = retell_response.json()
                call_id = retell_data.get("call_id")
                logger.info(f"✅ Retell call created: {call_id}")

                # Answer the Telnyx call
                logger.info("📞 Answering Telnyx call...")
                answer_response = await client.post(
                    f"https://api.telnyx.com/v2/calls/{call_control_id}/actions/answer",
                    headers={
                        "Authorization": f"Bearer {TELNYX_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=10.0
                )

                logger.info(f"Telnyx answer: {answer_response.status_code}")

                return {
                    "status": "ok",
                    "call_id": call_id,
                    "telnyx_call_id": call_control_id
                }
            else:
                error_text = retell_response.text
                logger.error(f"❌ Retell call failed: {error_text}")
                return {"status": "error", "message": error_text}

    except Exception as e:
        logger.error(f"❌ Error handling call: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@app.post("/retell/webhook/call-status")
async def telnyx_call_status(request: Request):
    """Telnyx call status updates"""
    try:
        body = await request.json()
        event_type = body.get("data", {}).get("event_type")
        logger.info(f"📊 Telnyx status: {event_type}")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"status": "error"}


if __name__ == "__main__":
    print("="*60)
    print("🚀 Starting Telnyx → Retell AI Webhook Server")
    print("="*60)
    print(f"Agent ID: {RETELL_AGENT_ID}")
    print(f"Port: 8000")
    print("="*60)
    uvicorn.run(app, host="127.0.0.1", port=8000)
