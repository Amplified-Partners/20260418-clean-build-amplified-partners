"""
Webhooks Routes - Vapi, Trigger.dev callbacks
Enterprise Grade v2.0 - With latency tracking, priority routing, compliance

Changes from v1:
- Added TTFA (Time to First Audio) tracking
- Emergency/Urgent/Routine SMS templates
- AI disclosure compliance logging
- Full transcript storage for audit
"""
from fastapi import APIRouter, HTTPException, Request, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from src.db.client import get_prisma
from src.db import queries
from src.services.lead_service import LeadService
from src.services.notification_service import NotificationService
from src.services.demo_numbers import get_demo_number_service
from src.services.event_log import get_event_log_service, EventSource

router = APIRouter()
logger = logging.getLogger("webhooks")

# =============================================================================
# LATENCY THRESHOLDS (Enterprise Requirement)
# =============================================================================
TTFA_WARNING_MS = 500   # Target: < 500ms
TTFA_CRITICAL_MS = 800  # Alert threshold


# =============================================================================
# SMS TEMPLATES (Enterprise Requirement - Priority Routing)
# =============================================================================

def get_sms_template(urgency: str, client_name: str, customer_name: str, 
                     phone: str, address: str, postcode: str, 
                     job_type: str, summary: str) -> tuple[str, str]:
    """
    Return (subject, message) based on urgency level.
    Enterprise requirement: Clear priority differentiation.
    """
    timestamp = datetime.now().strftime("%H:%M")
    location = f"{address or ''} {postcode or ''}".strip() or "Not provided"
    
    if urgency == "emergency":
        subject = f"🚨 EMERGENCY - {client_name}"
        message = f"""🚨 EMERGENCY - {client_name}

Caller: {customer_name or 'Unknown'}
Phone: {phone}
Issue: {job_type or summary[:100] if summary else 'Not specified'}

⚠️ CALL BACK IMMEDIATELY

{timestamp}"""
    
    elif urgency == "urgent":
        subject = f"⚡ URGENT - {client_name}"
        message = f"""⚡ URGENT LEAD - {client_name}

Caller: {customer_name or 'Unknown'}
Phone: {phone}
Address: {location}
Issue: {job_type or summary[:100] if summary else 'Not specified'}

Respond within 2 hours.

{timestamp}"""
    
    else:  # routine
        subject = f"📞 New Lead - {client_name}"
        message = f"""📞 New Lead - {client_name}

Caller: {customer_name or 'Unknown'}
Phone: {phone}
Address: {location}
Issue: {job_type or summary[:100] if summary else 'Not specified'}

{timestamp}"""
    
    return subject, message


class VapiCallComplete(BaseModel):
    """Vapi call completion webhook payload."""
    call_id: str
    phone_number: str
    caller_phone: str
    duration: Optional[int] = None
    transcript: Optional[str] = None
    summary: Optional[str] = None
    recording_url: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None


@router.post("/vapi/call-complete")
async def vapi_call_complete(request: Request, db=Depends(get_prisma)):
    """
    Handle Vapi call completion webhook.
    
    Enterprise v2.0 Flow:
    1. Log event with full payload (compliance)
    2. Extract call data and metrics
    3. Track latency (TTFA) if available
    4. Find client by covered number
    5. Find/create customer
    6. Create lead with urgency classification
    7. Create nurture sequence
    8. Trigger nurture job
    9. Notify owner with priority SMS template
    10. Store full transcript for audit
    """
    body = await request.json()

    # Log the incoming event (compliance requirement)
    event_log = get_event_log_service(db)
    event_id = await event_log.log(
        source=EventSource.VAPI,
        event_type="end-of-call-report",
        payload=body,
    )

    # Extract data from Vapi payload
    message = body.get("message", {})
    call = message.get("call", {})

    call_id = call.get("id")
    phone_number = call.get("phoneNumber", {}).get("number", "")
    caller_phone = call.get("customer", {}).get("number", "")
    duration = call.get("duration")
    transcript = message.get("transcript", "")
    summary = message.get("summary", "")
    recording_url = message.get("recordingUrl", "")
    
    # Extract latency metrics (Enterprise requirement)
    # Vapi provides startedAt and firstResponseAt in some payloads
    started_at = call.get("startedAt")
    first_response_at = call.get("firstResponseAt")
    ttfa_ms = None
    latency_acceptable = True
    
    if started_at and first_response_at:
        try:
            start = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            first = datetime.fromisoformat(first_response_at.replace('Z', '+00:00'))
            ttfa_ms = int((first - start).total_seconds() * 1000)
            latency_acceptable = ttfa_ms <= TTFA_WARNING_MS
            
            if ttfa_ms > TTFA_CRITICAL_MS:
                logger.warning(f"⚠️ High latency: {ttfa_ms}ms for call {call_id}")
            elif ttfa_ms > TTFA_WARNING_MS:
                logger.info(f"Elevated latency: {ttfa_ms}ms for call {call_id}")
        except Exception as e:
            logger.debug(f"Could not calculate TTFA: {e}")

    # Extract structured data from analysis
    analysis = message.get("analysis", {})
    structured_data = analysis.get("structuredData", {})

    customer_name = structured_data.get("customerName") or analysis.get("customerName")
    address = structured_data.get("address") or analysis.get("address")
    postcode = structured_data.get("postcode") or analysis.get("postcode")
    job_type = structured_data.get("jobType") or analysis.get("jobType")
    urgency = structured_data.get("urgency") or analysis.get("urgency", "routine")

    # Normalize urgency (must be one of these three)
    if urgency not in ["emergency", "urgent", "routine"]:
        # Try to detect emergency keywords
        transcript_lower = (transcript or "").lower()
        if any(word in transcript_lower for word in ["gas", "leak", "smell", "flooding", "burst"]):
            if "gas" in transcript_lower and "smell" in transcript_lower:
                urgency = "emergency"
            elif "burst" in transcript_lower or "flooding" in transcript_lower:
                urgency = "urgent"
            else:
                urgency = "routine"
        else:
            urgency = "routine"

    logger.info(f"📞 Vapi call complete webhook received")
    logger.info(f"   Call ID: {call_id}")
    logger.info(f"   Covered Number: {phone_number}")
    logger.info(f"   Caller: {caller_phone}")
    logger.info(f"   Duration: {duration}s")
    logger.info(f"   TTFA: {ttfa_ms}ms" if ttfa_ms else "   TTFA: Not available")
    logger.info(f"   Urgency: {urgency}")

    # 1. Find client by covered number
    client = await queries.get_client_by_covered_number(db, phone_number)

    if not client:
        logger.warning(f"   No client found for covered number: {phone_number}")
        await event_log.mark_failed(event_id, f"No client found for phone number {phone_number}")
        return {
            "status": "error",
            "message": f"No client found for phone number {phone_number}",
            "call_id": call_id,
            "lead_created": False,
            "nurture_started": False,
            "owner_notified": False,
        }

    logger.info(f"   Found client: {client.businessName} ({client.id})")

    # 2-5. Create lead with customer and nurture sequence
    lead_service = LeadService(db)

    try:
        lead = await lead_service.create_from_call(
            client=client,
            caller_phone=caller_phone,
            call_id=call_id,
            call_duration=duration,
            recording_url=recording_url,
            transcript=transcript,
            summary=summary,
            customer_name=customer_name,
            address=address,
            postcode=postcode,
            job_type=job_type,
            urgency=urgency
        )

        logger.info(f"   Created lead: {lead.id}")
        logger.info(f"   Customer: {lead.customerName or 'Unknown'}")
        logger.info(f"   Urgency: {lead.urgency}")

    except Exception as e:
        logger.error(f"   Error creating lead: {e}")
        await event_log.mark_failed(event_id, str(e))
        return {
            "status": "error",
            "message": str(e),
            "call_id": call_id,
            "lead_created": False,
            "nurture_started": False,
            "owner_notified": False,
        }

    # 6. Trigger nurture sequence
    nurture_started = await lead_service.trigger_nurture_sequence(lead, client)

    # 7. Notify owner with priority SMS template (Enterprise requirement)
    notification_service = NotificationService(db)

    # Use enterprise SMS templates
    subject, sms_message = get_sms_template(
        urgency=urgency,
        client_name=client.businessName,
        customer_name=customer_name,
        phone=caller_phone,
        address=address,
        postcode=postcode,
        job_type=job_type,
        summary=summary
    )

    owner_result = await notification_service.notify_owner(
        client_id=client.id,
        lead_id=lead.id,
        message=sms_message,
        subject=subject
    )

    owner_notified = owner_result.get("success", False)

    logger.info(f"   Nurture started: {nurture_started}")
    logger.info(f"   Owner notified: {owner_notified}")
    if not owner_notified:
        logger.warning(f"   Notification result: {owner_result}")

    # Mark event as processed with full metrics (compliance requirement)
    result = {
        "status": "received",
        "call_id": call_id,
        "lead_id": lead.id,
        "lead_created": True,
        "nurture_started": nurture_started,
        "owner_notified": owner_notified,
        "urgency": urgency,
        "metrics": {
            "ttfa_ms": ttfa_ms,
            "latency_acceptable": latency_acceptable,
            "duration_ms": duration * 1000 if duration else None,
        }
    }
    await event_log.mark_processed(event_id, result)

    return result


@router.post("/vapi/call-start")
async def vapi_call_start(request: Request, db=Depends(get_prisma)):
    """
    Handle Vapi call start webhook.
    Enterprise v2.0: Track call initiation for latency measurement.
    """
    body = await request.json()
    
    event_log = get_event_log_service(db)
    await event_log.log(
        source=EventSource.VAPI,
        event_type="call-start",
        payload=body,
    )
    
    call = body.get("message", {}).get("call", {})
    call_id = call.get("id")
    phone_number = call.get("phoneNumber", {}).get("number", "")
    
    logger.info(f"📞 Call started: {call_id} on {phone_number}")
    
    return {"status": "ok", "call_id": call_id}


@router.post("/vapi/speech-update")
async def vapi_speech_update(request: Request, db=Depends(get_prisma)):
    """
    Handle Vapi speech update webhook (optional, for real-time tracking).
    Enterprise v2.0: Can be used for live latency monitoring.
    """
    body = await request.json()
    
    # Lightweight logging - don't store every speech update
    call = body.get("message", {}).get("call", {})
    call_id = call.get("id")
    role = body.get("message", {}).get("role", "")
    
    # Only log assistant responses for TTFA tracking
    if role == "assistant":
        logger.debug(f"   Assistant response in call {call_id}")
    
    return {"status": "ok"}


@router.post("/trigger")
async def trigger_webhook(request: Request, db=Depends(get_prisma)):
    """Handle Trigger.dev callbacks."""
    body = await request.json()

    event_type = body.get("type")
    payload = body.get("payload", {})

    logger.info(f"Trigger event: {event_type}")

    # Handle different event types
    if event_type == "nurture.touch.sent":
        lead_id = payload.get("lead_id")
        touch_number = payload.get("touch_number")

        if lead_id and touch_number:
            await queries.update_nurture_progress(db, lead_id, touch_number)
            logger.info(f"   Updated nurture progress: lead {lead_id}, touch {touch_number}")

    elif event_type == "nurture.completed":
        lead_id = payload.get("lead_id")
        if lead_id:
            lead = await queries.get_lead_by_id(db, lead_id)
            if lead and lead.nurtureSequence:
                await db.nurturesequence.update(
                    where={"id": lead.nurtureSequence.id},
                    data={
                        "status": "completed",
                        "completedAt": datetime.utcnow()
                    }
                )
                logger.info(f"   Marked nurture sequence complete for lead {lead_id}")

    elif event_type == "review.requested":
        job_id = payload.get("job_id")
        if job_id:
            await db.job.update(
                where={"id": job_id},
                data={
                    "reviewRequested": True,
                    "reviewRequestedAt": datetime.utcnow()
                }
            )
            logger.info(f"   Marked review requested for job {job_id}")

    return {"status": "received", "event": event_type}


@router.post("/vapi/assistant-request")
async def vapi_assistant_request(request: Request, db=Depends(get_prisma)):
    """
    Handle Vapi assistant request webhook.
    Returns assistant configuration based on the phone number called.
    """
    body = await request.json()

    message = body.get("message", {})
    call = message.get("call", {})
    phone_number = call.get("phoneNumber", {}).get("number", "")

    logger.info(f"Assistant request for number: {phone_number}")

    # Find client by covered number
    client = await queries.get_client_by_covered_number(db, phone_number)

    if not client:
        logger.info(f"   No client found, using default assistant")
        return {
            "assistantId": None,
            "error": "No client configured for this number"
        }

    logger.info(f"   Found client: {client.businessName}")

    # Return the client's configured assistant
    if client.vapiAssistantId:
        return {
            "assistantId": client.vapiAssistantId
        }
    else:
        return {
            "assistantId": None,
            "message": f"Client {client.businessName} has no configured assistant"
        }


@router.get("/health")
async def webhook_health():
    """Health check for webhooks."""
    return {
        "status": "healthy",
        "service": "webhooks",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/demo-call")
async def demo_call_webhook(request: Request, db=Depends(get_prisma)):
    """
    Handle calls to demo numbers.
    """
    body = await request.json()

    event_log = get_event_log_service(db)
    event_id = await event_log.log(
        source=EventSource.VAPI,
        event_type="demo-call",
        payload=body,
    )

    message = body.get("message", {})
    call = message.get("call", {})

    phone_number = call.get("phoneNumber", {}).get("number", "")
    call_id = call.get("id")
    caller_phone = call.get("customer", {}).get("number", "")
    duration = call.get("duration")
    transcript = message.get("transcript", "")
    summary = message.get("summary", "")

    logger.info(f"Demo call webhook received")
    logger.info(f"   Phone Number: {phone_number}")
    logger.info(f"   Call ID: {call_id}")
    logger.info(f"   Caller: {caller_phone}")
    logger.info(f"   Duration: {duration}s")

    demo_service = get_demo_number_service(db)
    demo_number = await demo_service.get_by_phone(phone_number)

    if not demo_number:
        logger.warning(f"   No demo number found for: {phone_number}")
        await event_log.mark_failed(event_id, f"No demo number found for {phone_number}")
        return {
            "status": "error",
            "message": f"No demo number found for {phone_number}",
            "call_id": call_id,
        }

    await demo_service.record_call(
        demo_number["id"],
        {
            "call_id": call_id,
            "caller_phone": caller_phone,
            "duration": duration,
            "transcript": transcript,
            "summary": summary,
        }
    )

    logger.info(f"   Recorded call for demo: {demo_number['business_name']}")

    result = {
        "status": "ok",
        "demo_id": demo_number["id"],
        "business_name": demo_number["business_name"],
        "call_count": demo_number["call_count"] + 1,
    }
    await event_log.mark_processed(event_id, result)

    return result
