"""
Three-Layer Failsafe Webhook Server for Telnyx → Retell AI Integration

Architecture:
- Layer 1 (Primary): Retell AI agent (UK region)
- Layer 2 (Secondary): Backup Retell AI agent (US region) OR recorded message + callback
- Layer 3 (Tertiary): Direct forward to owner's mobile

Philosophy: "These are people's businesses. Why not?"
"""
import os
import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from fastapi import FastAPI, Request, BackgroundTasks
import httpx
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Three-Layer Failsafe Webhook Server")

# ============================================================================
# Configuration
# ============================================================================

# Layer 1: Primary Retell AI Agent (UK/EU region)
RETELL_API_KEY = os.getenv("RETELL_API_KEY", "key_REDACTED-RETELL")
RETELL_AGENT_ID_PRIMARY = os.getenv("RETELL_AGENT_ID", "agent_1e0b55aa699c7b55cc8b1ef24a")

# Layer 2: Backup Retell AI Agent (US region) - create this in Retell dashboard
RETELL_AGENT_ID_BACKUP = os.getenv("RETELL_AGENT_ID_BACKUP", "agent_backup_placeholder")

# Layer 3: Owner's mobile for direct forwarding
OWNER_PHONE_NUMBER = os.getenv("OWNER_PHONE_NUMBER", "+447970140373")  # Dave's number
OWNER_NAME = os.getenv("OWNER_NAME", "Dave")

# Telnyx Configuration
TELNYX_API_KEY = os.getenv("TELNYX_API_KEY", "KEY-REDACTED-TELNYX")

# Twilio Configuration (for SMS alerts)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "AC-REDACTED-TWILIO-SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "REDACTED-TWILIO-AUTH-TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+14155238886")

# Retry Configuration
MAX_RETRIES_PER_LAYER = 3
RETRY_DELAY_SECONDS = 2
HEALTH_CHECK_INTERVAL = 60  # seconds
FAILURE_THRESHOLD = 3  # failures before triggering alert

# ============================================================================
# System State
# ============================================================================

class SystemLayer(Enum):
    """Current active layer"""
    LAYER_1_PRIMARY = "layer_1_primary"
    LAYER_2_BACKUP = "layer_2_backup"
    LAYER_3_DIRECT = "layer_3_direct"

class SystemHealth:
    """Track system health and failures"""
    def __init__(self):
        self.layer_1_failures = 0
        self.layer_2_failures = 0
        self.layer_3_failures = 0
        self.current_layer = SystemLayer.LAYER_1_PRIMARY
        self.last_health_check = datetime.utcnow()
        self.total_calls_handled = 0
        self.calls_by_layer = {
            SystemLayer.LAYER_1_PRIMARY: 0,
            SystemLayer.LAYER_2_BACKUP: 0,
            SystemLayer.LAYER_3_DIRECT: 0,
        }
        self.alert_sent_at: Optional[datetime] = None

system_health = SystemHealth()

# ============================================================================
# SMS Alerting
# ============================================================================

async def send_sms_alert(message: str, urgent: bool = False):
    """Send SMS alert to owner via Twilio"""
    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        prefix = "🚨 URGENT: " if urgent else "⚠️ Alert: "
        full_message = f"{prefix}{message}"

        message = client.messages.create(
            body=full_message,
            from_=TWILIO_PHONE_NUMBER,
            to=OWNER_PHONE_NUMBER
        )

        logger.info(f"📱 SMS alert sent: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send SMS alert: {e}")
        return False

# ============================================================================
# Layer 1: Primary Retell AI Agent
# ============================================================================

async def create_retell_call_layer1(
    from_number: str,
    to_number: str,
    call_control_id: str
) -> Optional[Dict[str, Any]]:
    """
    Layer 1: Primary Retell AI agent (UK/EU region)
    Returns: Retell call data if successful, None if failed
    """
    logger.info("🟢 Layer 1: Trying primary Retell AI agent...")

    for attempt in range(MAX_RETRIES_PER_LAYER):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.retellai.com/create-phone-call",
                    headers={
                        "Authorization": f"Bearer {RETELL_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from_number": to_number,  # Our number
                        "to_number": from_number,   # Customer
                        "agent_id": RETELL_AGENT_ID_PRIMARY,
                        "metadata": {
                            "telnyx_call_id": call_control_id,
                            "layer": "primary",
                            "attempt": attempt + 1
                        }
                    }
                )

                if response.status_code in [200, 201]:
                    retell_data = response.json()
                    call_id = retell_data.get("call_id")
                    logger.info(f"✅ Layer 1 SUCCESS: Retell call created: {call_id}")

                    # Reset failure count on success
                    system_health.layer_1_failures = 0
                    system_health.calls_by_layer[SystemLayer.LAYER_1_PRIMARY] += 1

                    return retell_data
                else:
                    logger.warning(f"⚠️ Layer 1 attempt {attempt + 1} failed: {response.status_code} - {response.text}")

        except Exception as e:
            logger.warning(f"⚠️ Layer 1 attempt {attempt + 1} error: {e}")

        if attempt < MAX_RETRIES_PER_LAYER - 1:
            await asyncio.sleep(RETRY_DELAY_SECONDS)

    # All retries failed
    system_health.layer_1_failures += 1
    logger.error(f"❌ Layer 1 FAILED after {MAX_RETRIES_PER_LAYER} attempts")

    # Alert if failures exceed threshold
    if system_health.layer_1_failures >= FAILURE_THRESHOLD:
        await send_sms_alert(
            f"Layer 1 (Primary Retell AI) has failed {system_health.layer_1_failures} times. "
            f"System is using backup layers.",
            urgent=False
        )

    return None

# ============================================================================
# Layer 2: Backup Retell AI Agent (or Recorded Message)
# ============================================================================

async def create_retell_call_layer2(
    from_number: str,
    to_number: str,
    call_control_id: str
) -> Optional[Dict[str, Any]]:
    """
    Layer 2: Backup Retell AI agent (US region) or recorded message + callback
    Returns: Retell call data if successful, None if failed
    """
    logger.info("🟡 Layer 2: Trying backup Retell AI agent...")

    # Check if backup agent is configured
    if RETELL_AGENT_ID_BACKUP == "agent_backup_placeholder":
        logger.warning("⚠️ Layer 2: No backup agent configured, skipping to Layer 3")
        return None

    for attempt in range(MAX_RETRIES_PER_LAYER):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.retellai.com/create-phone-call",
                    headers={
                        "Authorization": f"Bearer {RETELL_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from_number": to_number,
                        "to_number": from_number,
                        "agent_id": RETELL_AGENT_ID_BACKUP,
                        "metadata": {
                            "telnyx_call_id": call_control_id,
                            "layer": "backup",
                            "attempt": attempt + 1
                        }
                    }
                )

                if response.status_code in [200, 201]:
                    retell_data = response.json()
                    call_id = retell_data.get("call_id")
                    logger.info(f"✅ Layer 2 SUCCESS: Backup Retell call created: {call_id}")

                    # Reset failure count on success
                    system_health.layer_2_failures = 0
                    system_health.calls_by_layer[SystemLayer.LAYER_2_BACKUP] += 1

                    # Alert owner that backup layer is being used
                    await send_sms_alert(
                        f"Using backup system (Layer 2) for incoming call. "
                        f"Primary system may be degraded.",
                        urgent=False
                    )

                    return retell_data
                else:
                    logger.warning(f"⚠️ Layer 2 attempt {attempt + 1} failed: {response.status_code}")

        except Exception as e:
            logger.warning(f"⚠️ Layer 2 attempt {attempt + 1} error: {e}")

        if attempt < MAX_RETRIES_PER_LAYER - 1:
            await asyncio.sleep(RETRY_DELAY_SECONDS)

    # All retries failed
    system_health.layer_2_failures += 1
    logger.error(f"❌ Layer 2 FAILED after {MAX_RETRIES_PER_LAYER} attempts")

    return None

# ============================================================================
# Layer 3: Direct Forward to Owner
# ============================================================================

async def forward_to_owner_layer3(
    from_number: str,
    call_control_id: str
) -> bool:
    """
    Layer 3: Forward call directly to owner's mobile
    This is the guaranteed-to-work fallback.
    Returns: True if successful, False if failed
    """
    logger.info("🔴 Layer 3: Forwarding call directly to owner...")

    try:
        # Send urgent SMS alert FIRST
        await send_sms_alert(
            f"SYSTEM DOWN - Forwarding call from {from_number} to you now. "
            f"Both AI layers failed.",
            urgent=True
        )

        # Forward call via Telnyx
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"https://api.telnyx.com/v2/calls/{call_control_id}/actions/transfer",
                headers={
                    "Authorization": f"Bearer {TELNYX_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "to": OWNER_PHONE_NUMBER
                }
            )

            if response.status_code in [200, 201]:
                logger.info(f"✅ Layer 3 SUCCESS: Call forwarded to {OWNER_NAME}")
                system_health.calls_by_layer[SystemLayer.LAYER_3_DIRECT] += 1
                return True
            else:
                logger.error(f"❌ Layer 3 FAILED: Telnyx transfer failed: {response.status_code} - {response.text}")
                return False

    except Exception as e:
        logger.error(f"❌ Layer 3 FAILED: {e}")
        system_health.layer_3_failures += 1

        # If even Layer 3 fails, this is catastrophic
        await send_sms_alert(
            f"CATASTROPHIC FAILURE - Could not forward call from {from_number}. "
            f"All three layers failed. Check system immediately.",
            urgent=True
        )

        return False

# ============================================================================
# Main Call Handler with Three-Layer Fallback
# ============================================================================

@app.post("/retell/webhook/call-incoming")
async def handle_incoming_call_with_failsafe(request: Request, background_tasks: BackgroundTasks):
    """
    Main webhook handler with three-layer failsafe architecture

    Flow:
    1. Try Layer 1 (Primary Retell AI) - 3 attempts
    2. If fails, try Layer 2 (Backup Retell AI) - 3 attempts
    3. If fails, trigger Layer 3 (Direct forward to owner)
    """
    try:
        body = await request.json()
        logger.info(f"📞 Incoming call from Telnyx")

        # Extract call details
        payload = body.get("data", {}).get("payload", {})
        call_control_id = payload.get("call_control_id")
        from_number = payload.get("from")
        to_number = payload.get("to")

        if not call_control_id:
            logger.error("❌ No call_control_id in webhook")
            return {"status": "error", "message": "No call_control_id"}

        logger.info(f"📞 Call: {from_number} → {to_number} (Control ID: {call_control_id})")

        system_health.total_calls_handled += 1

        # ====================================================================
        # LAYER 1: Primary Retell AI Agent
        # ====================================================================
        retell_data = await create_retell_call_layer1(from_number, to_number, call_control_id)

        if retell_data:
            # Success! Answer the Telnyx call
            await answer_telnyx_call(call_control_id)
            return {
                "status": "ok",
                "layer": "layer_1_primary",
                "call_id": retell_data.get("call_id"),
                "telnyx_call_id": call_control_id
            }

        # ====================================================================
        # LAYER 2: Backup Retell AI Agent
        # ====================================================================
        logger.warning("⚠️ Layer 1 failed, escalating to Layer 2...")
        retell_data = await create_retell_call_layer2(from_number, to_number, call_control_id)

        if retell_data:
            # Success! Answer the Telnyx call
            await answer_telnyx_call(call_control_id)
            return {
                "status": "ok",
                "layer": "layer_2_backup",
                "call_id": retell_data.get("call_id"),
                "telnyx_call_id": call_control_id
            }

        # ====================================================================
        # LAYER 3: Direct Forward to Owner
        # ====================================================================
        logger.error("❌ Layer 2 failed, escalating to Layer 3 (DIRECT FORWARD)...")
        success = await forward_to_owner_layer3(from_number, call_control_id)

        if success:
            return {
                "status": "ok",
                "layer": "layer_3_direct",
                "message": f"Call forwarded directly to {OWNER_NAME}",
                "telnyx_call_id": call_control_id
            }
        else:
            # Catastrophic failure - all three layers failed
            logger.error("💀 CATASTROPHIC FAILURE - All three layers failed")
            return {
                "status": "catastrophic_failure",
                "message": "All three layers failed",
                "telnyx_call_id": call_control_id
            }

    except Exception as e:
        logger.error(f"❌ Unhandled error in call handler: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

# ============================================================================
# Helper: Answer Telnyx Call
# ============================================================================

async def answer_telnyx_call(call_control_id: str) -> bool:
    """Answer the Telnyx call after Retell AI is ready"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"https://api.telnyx.com/v2/calls/{call_control_id}/actions/answer",
                headers={
                    "Authorization": f"Bearer {TELNYX_API_KEY}",
                    "Content-Type": "application/json"
                }
            )

            if response.status_code in [200, 201]:
                logger.info(f"✅ Telnyx call answered")
                return True
            else:
                logger.error(f"❌ Failed to answer Telnyx call: {response.status_code}")
                return False
    except Exception as e:
        logger.error(f"❌ Error answering Telnyx call: {e}")
        return False

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns system status and statistics
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system_health": {
            "current_layer": system_health.current_layer.value,
            "total_calls_handled": system_health.total_calls_handled,
            "calls_by_layer": {
                "layer_1_primary": system_health.calls_by_layer[SystemLayer.LAYER_1_PRIMARY],
                "layer_2_backup": system_health.calls_by_layer[SystemLayer.LAYER_2_BACKUP],
                "layer_3_direct": system_health.calls_by_layer[SystemLayer.LAYER_3_DIRECT],
            },
            "failures": {
                "layer_1": system_health.layer_1_failures,
                "layer_2": system_health.layer_2_failures,
                "layer_3": system_health.layer_3_failures,
            },
            "last_health_check": system_health.last_health_check.isoformat()
        }
    }

# ============================================================================
# Status Endpoint (Detailed Monitoring)
# ============================================================================

@app.get("/status")
async def system_status():
    """
    Detailed system status for monitoring dashboard
    """
    total_calls = system_health.total_calls_handled
    layer_1_calls = system_health.calls_by_layer[SystemLayer.LAYER_1_PRIMARY]
    layer_2_calls = system_health.calls_by_layer[SystemLayer.LAYER_2_BACKUP]
    layer_3_calls = system_health.calls_by_layer[SystemLayer.LAYER_3_DIRECT]

    layer_1_success_rate = (layer_1_calls / total_calls * 100) if total_calls > 0 else 0

    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "statistics": {
            "total_calls": total_calls,
            "layer_1_calls": layer_1_calls,
            "layer_2_calls": layer_2_calls,
            "layer_3_calls": layer_3_calls,
            "layer_1_success_rate": f"{layer_1_success_rate:.2f}%",
        },
        "failures": {
            "layer_1": system_health.layer_1_failures,
            "layer_2": system_health.layer_2_failures,
            "layer_3": system_health.layer_3_failures,
        },
        "configuration": {
            "primary_agent": RETELL_AGENT_ID_PRIMARY,
            "backup_agent": RETELL_AGENT_ID_BACKUP,
            "owner_phone": OWNER_PHONE_NUMBER[-4:],  # Last 4 digits only
            "max_retries_per_layer": MAX_RETRIES_PER_LAYER,
            "health_check_interval": HEALTH_CHECK_INTERVAL,
        }
    }

# ============================================================================
# Telnyx Call Status Updates
# ============================================================================

@app.post("/retell/webhook/call-status")
async def telnyx_call_status(request: Request):
    """Handle Telnyx call status updates"""
    try:
        body = await request.json()
        event_type = body.get("data", {}).get("event_type")
        logger.info(f"📊 Telnyx status: {event_type}")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling status: {e}")
        return {"status": "error"}

# ============================================================================
# Background Health Monitoring
# ============================================================================

async def continuous_health_monitoring():
    """
    Background task that runs continuous health checks
    Checks system health every 60 seconds
    """
    logger.info("🔍 Starting continuous health monitoring...")

    while True:
        try:
            system_health.last_health_check = datetime.utcnow()

            # Check if Layer 1 is degraded (>20% failure rate)
            if system_health.total_calls_handled > 10:  # Only after 10 calls
                layer_1_calls = system_health.calls_by_layer[SystemLayer.LAYER_1_PRIMARY]
                total_calls = system_health.total_calls_handled
                layer_1_rate = (layer_1_calls / total_calls * 100)

                if layer_1_rate < 80:
                    logger.warning(f"⚠️ Layer 1 degraded: {layer_1_rate:.1f}% success rate")

                    # Alert owner if not alerted recently
                    if (system_health.alert_sent_at is None or
                        (datetime.utcnow() - system_health.alert_sent_at).seconds > 3600):
                        await send_sms_alert(
                            f"Primary system degraded: {layer_1_rate:.1f}% success rate. "
                            f"Backup layers are handling calls.",
                            urgent=False
                        )
                        system_health.alert_sent_at = datetime.utcnow()

            logger.info(f"✅ Health check passed. Calls: {system_health.total_calls_handled}, "
                       f"Layer 1 success: {system_health.calls_by_layer[SystemLayer.LAYER_1_PRIMARY]}")

        except Exception as e:
            logger.error(f"❌ Health monitoring error: {e}")

        await asyncio.sleep(HEALTH_CHECK_INTERVAL)

@app.on_event("startup")
async def startup_event():
    """Start background monitoring on startup"""
    asyncio.create_task(continuous_health_monitoring())
    logger.info("🚀 Three-Layer Failsafe System started")
    logger.info(f"📞 Owner: {OWNER_NAME} ({OWNER_PHONE_NUMBER})")
    logger.info(f"🟢 Layer 1: Primary Agent ({RETELL_AGENT_ID_PRIMARY})")
    logger.info(f"🟡 Layer 2: Backup Agent ({RETELL_AGENT_ID_BACKUP})")
    logger.info(f"🔴 Layer 3: Direct Forward to Owner")

# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("🚀 THREE-LAYER FAILSAFE WEBHOOK SERVER")
    print("="*80)
    print(f"🟢 Layer 1: Primary Retell AI Agent ({RETELL_AGENT_ID_PRIMARY})")
    print(f"🟡 Layer 2: Backup Retell AI Agent ({RETELL_AGENT_ID_BACKUP})")
    print(f"🔴 Layer 3: Direct Forward to {OWNER_NAME} ({OWNER_PHONE_NUMBER})")
    print("="*80)
    print(f"Port: 8000")
    print(f"Health Check: http://localhost:8000/health")
    print(f"Status: http://localhost:8000/status")
    print("="*80)
    uvicorn.run(app, host="127.0.0.1", port=8000)
