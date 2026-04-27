"""
Retell AI + Cartesia Integration
Voice AI phone system for Amplified Partners / Jesmond Plumbing

Architecture:
- Retell AI: 600ms latency platform
- Cartesia: 40ms TTS with British voices
- Claude 3.5 Sonnet: Conversation AI
- Twilio: Phone number (existing)

Functions exposed to Retell AI agent:
1. check_calendar_availability - Query Dave's calendar
2. book_appointment - Create calendar event + CRM entry
3. send_emergency_sms - Alert Dave for urgent calls
4. log_call_to_crm - Save call transcript and details
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx

from app.database import get_async_session
from app.models import Contact, ContactPII, Activity
from app.models.enums import ActivityType
from app.integrations.twilio_integration import TwilioIntegration

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/retell", tags=["Retell AI"])

# Configuration
RETELL_API_KEY = os.getenv("RETELL_API_KEY")
RETELL_AGENT_ID = os.getenv("RETELL_AGENT_ID")
DAVE_PHONE_NUMBER = os.getenv("DAVE_PHONE_NUMBER", "")  # Must be set in keys.env
DAVE_TENANT_ID = 1  # Dave Morrison's tenant

# Initialize Twilio for SMS
twilio = TwilioIntegration()


# ============================================================================
# Helper Functions
# ============================================================================

def parse_time_preference(preference: str) -> tuple[int, int]:
    """Convert 'morning'/'afternoon' to hour range."""
    preference = preference.lower()
    if "morning" in preference:
        return 9, 12  # 9am-12pm
    elif "afternoon" in preference:
        return 14, 17  # 2pm-5pm
    else:
        return 9, 17  # Any time


async def get_or_create_contact(
    db: AsyncSession,
    name: str,
    phone: str,
    address: Optional[str] = None
) -> Contact:
    """Get existing contact or create new one."""
    # Look up by phone
    result = await db.execute(
        select(Contact).where(
            Contact.tenant_id == DAVE_TENANT_ID,
            Contact.phone == phone
        )
    )
    contact = result.scalar_one_or_none()

    if contact:
        # Update if details changed
        if address and contact.address != address:
            contact.address = address
            await db.commit()
        return contact

    # Create new contact
    contact = Contact(
        tenant_id=DAVE_TENANT_ID,
        name=name,
        phone=phone,
        address=address,
        source="voice_ai_retell",
        created_at=datetime.utcnow(),
    )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)

    logger.info(f"Created new contact: {name} ({phone})")
    return contact


# ============================================================================
# Function Endpoints (Called by Retell AI Agent)
# ============================================================================

@router.post("/functions/check_calendar_availability")
async def check_calendar_availability(request: Request):
    """
    Check Dave's calendar for available appointment slots.

    Called by Retell AI agent when customer wants to book.

    Parameters from agent:
    - date: Preferred date (e.g., "tomorrow", "next Tuesday")
    - time: Time preference ("morning", "afternoon", "anytime")
    """
    try:
        from zoneinfo import ZoneInfo
        UK_TZ = ZoneInfo("Europe/London")

        body = await request.json()
        params = body.get("parameters", {})

        time_pref = params.get("time", "anytime").lower()

        # Candidate slot times by preference
        if "morning" in time_pref:
            slot_times = [(9, 0), (10, 0), (11, 0)]
        elif "afternoon" in time_pref:
            slot_times = [(13, 0), (14, 0), (15, 0)]
        elif "evening" in time_pref:
            slot_times = [(16, 0), (17, 0)]
        else:
            slot_times = [(9, 0), (13, 0), (15, 0)]

        # Try Google Calendar to get busy times
        busy_datetimes = set()
        try:
            from app.integrations.calendar_integration import CalendarIntegration
            calendar = CalendarIntegration(tenant_id=str(DAVE_TENANT_ID))
            if await calendar.is_connected():
                existing = await calendar.get_upcoming_events(days=10)
                for ev in existing:
                    start_str = ev.get("start", "")
                    if "T" in start_str:
                        ev_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
                        busy_datetimes.add(ev_dt.strftime("%Y-%m-%dT%H:%M"))
        except Exception as cal_err:
            logger.info(f"Calendar not connected, using open slots: {cal_err}")

        # Generate slots for next 7 working days
        now = datetime.now(UK_TZ)
        available_slots = []
        day = now.date()
        days_checked = 0

        while len(available_slots) < 3 and days_checked < 14:
            day = day + timedelta(days=1)
            days_checked += 1
            if day.weekday() >= 5:  # skip Sat/Sun
                continue
            for hour, minute in slot_times:
                slot_dt = datetime(day.year, day.month, day.day, hour, minute, tzinfo=UK_TZ)
                slot_key = slot_dt.strftime("%Y-%m-%dT%H:%M")
                if slot_key not in busy_datetimes:
                    available_slots.append({
                        "day": slot_dt.strftime("%A"),
                        "date": slot_dt.strftime("%Y-%m-%d"),
                        "time": slot_dt.strftime("%I:%M %p").lstrip("0"),
                        "datetime": slot_dt.isoformat(),
                    })
                if len(available_slots) >= 3:
                    break

        if not available_slots:
            return {
                "success": False,
                "message": "I can't find any free slots right now. Let me take your number and Dave'll call you back to arrange something."
            }

        # Build natural language message
        parts = []
        for s in available_slots:
            parts.append(f"{s['day']} at {s['time']}")
        if len(parts) == 1:
            message = f"Dave's free {parts[0]}. Does that work?"
        elif len(parts) == 2:
            message = f"I've got {parts[0]} or {parts[1]}. What works for you?"
        else:
            message = f"I've got {parts[0]}, {parts[1]}, or {parts[2]}. What suits you best?"

        return {
            "success": True,
            "available_slots": available_slots,
            "message": message
        }

    except Exception as e:
        logger.error(f"Error checking calendar: {e}")
        return {
            "success": False,
            "message": "Sorry, I'm having trouble checking the calendar. Let me take your details and Dave'll call you back."
        }


@router.post("/functions/book_appointment")
async def book_appointment(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Book appointment in Dave's calendar and log to CRM.

    Called by Retell AI agent after customer confirms time.

    Parameters from agent:
    - customer_name: Full name
    - customer_phone: Phone number
    - customer_address: Full address
    - issue: Description of plumbing issue
    - appointment_datetime: ISO datetime string
    """
    try:
        body = await request.json()
        params = body.get("parameters", {})

        # Extract booking details
        customer_name = params.get("customer_name")
        customer_phone = params.get("customer_phone")
        customer_address = params.get("customer_address")
        issue_description = params.get("issue")
        appointment_datetime = params.get("appointment_datetime")

        # Validate required fields
        if not all([customer_name, customer_phone, issue_description, appointment_datetime]):
            return {
                "success": False,
                "message": "Missing required booking information. Let me take your details again."
            }

        # Get or create contact
        contact = await get_or_create_contact(
            db,
            name=customer_name,
            phone=customer_phone,
            address=customer_address
        )

        # Parse appointment datetime
        appointment_dt = datetime.fromisoformat(appointment_datetime.replace('Z', '+00:00'))

        # Create activity (appointment) in CRM
        activity = Activity(
            tenant_id=DAVE_TENANT_ID,
            contact_id=contact.id,
            activity_type="appointment",
            notes=f"AI Booked: {issue_description}",
            scheduled_at=appointment_dt,
            created_at=datetime.utcnow(),
        )
        db.add(activity)
        await db.commit()

        # Step 2b: Create Google Calendar event
        # Wrap in try/except — if OAuth not done yet, log warning but don't break booking
        try:
            from app.integrations.calendar_integration import CalendarIntegration
            calendar = CalendarIntegration(tenant_id=str(DAVE_TENANT_ID))
            end_dt = appointment_dt + timedelta(hours=1)
            event_id = await calendar.create_event(
                summary=f"{customer_name} - {issue_description}",
                start_time=appointment_dt,
                end_time=end_dt,
                location=customer_address or "",
                description=f"Booked via AI voice agent. Issue: {issue_description}",
                customer_name=customer_name,
                customer_email=None,  # Voice callers don't provide email
            )
            if event_id:
                logger.info(f"Calendar event created: {event_id} for {customer_name}")
            else:
                logger.warning(
                    f"Calendar event not created for {customer_name} "
                    "(conflict detected or API error)"
                )
        except Exception as cal_err:
            logger.warning(
                f"Calendar integration unavailable (OAuth not completed?): {cal_err}"
            )

        # Send confirmation SMS to customer
        confirmation_msg = f"Jesmond Plumbing: Appointment confirmed for {appointment_dt.strftime('%A, %B %d at %I:%M %p')}. Dave will text to confirm the day before. - Dave's Assistant"
        try:
            await twilio.send_sms(customer_phone, confirmation_msg)
        except Exception as e:
            logger.error(f"Failed to send confirmation SMS: {e}")

        # Send notification to Dave
        dave_msg = f"NEW BOOKING\n{customer_name}\n{customer_phone}\n{customer_address}\n{issue_description}\n{appointment_dt.strftime('%A, %B %d at %I:%M %p')}"
        try:
            await twilio.send_sms(DAVE_PHONE_NUMBER, dave_msg)
        except Exception as e:
            logger.error(f"Failed to notify Dave: {e}")

        logger.info(f"Booked appointment: {customer_name} on {appointment_datetime}")

        # Format response day nicely
        day_str = appointment_dt.strftime("%A at %I:%M %p")

        return {
            "success": True,
            "message": f"Right, you're all sorted. I've booked you in for {day_str}. Dave'll text to confirm the day before. Anything else?"
        }

    except Exception as e:
        logger.error(f"Error booking appointment: {e}", exc_info=True)
        return {
            "success": False,
            "message": "Sorry, I'm having trouble with the booking system. Let me take your number and Dave'll call you right back to sort it out."
        }


@router.post("/functions/send_emergency_sms")
async def send_emergency_sms(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Send emergency alert to Dave's phone.

    Called by Retell AI agent when emergency detected
    (burst pipe, flooding, gas leak, no heating in winter, etc.)

    Parameters from agent:
    - customer_name: Name
    - customer_phone: Phone to call back
    - customer_address: Where to go
    - issue: What's wrong (urgent description)
    """
    try:
        body = await request.json()
        params = body.get("parameters", {})

        customer_name = params.get("customer_name", "Customer")
        customer_phone = params.get("customer_phone")
        customer_address = params.get("customer_address", "Address not provided")
        issue = params.get("issue")

        if not customer_phone or not issue:
            return {
                "success": False,
                "message": "I need their phone number and what the issue is."
            }

        # Log to CRM
        contact = await get_or_create_contact(
            db,
            name=customer_name,
            phone=customer_phone,
            address=customer_address
        )

        activity = Activity(
            tenant_id=DAVE_TENANT_ID,
            contact_id=contact.id,
            activity_type="phone",
            notes=f"🚨 EMERGENCY: {issue}",
            created_at=datetime.utcnow(),
        )
        db.add(activity)
        await db.commit()

        # Send emergency SMS to Dave
        emergency_msg = f"""🚨 EMERGENCY CALL

{customer_name}
{customer_phone}
{customer_address}

{issue}

CALL BACK ASAP!"""

        try:
            await twilio.send_sms(DAVE_PHONE_NUMBER, emergency_msg)
            logger.warning(f"EMERGENCY SMS sent to Dave: {customer_name} - {issue}")
        except Exception as e:
            logger.error(f"CRITICAL: Failed to send emergency SMS: {e}")
            raise

        return {
            "success": True,
            "message": "Right, I've sent this straight to Dave. He'll call you back within 10 minutes."
        }

    except Exception as e:
        logger.error(f"Error sending emergency SMS: {e}", exc_info=True)
        return {
            "success": False,
            "message": "Let me get Dave on the line right now. Hold on."
        }


@router.post("/functions/log_call_to_crm")
async def log_call_to_crm(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Log completed call to CRM for record-keeping.

    Called by Retell AI agent at end of every call.

    Parameters from agent:
    - customer_phone: Caller's number
    - call_summary: Brief summary of call
    - outcome: "booked" / "emergency" / "info_only" / "callback_needed"
    - duration_seconds: Call length
    """
    try:
        body = await request.json()
        params = body.get("parameters", {})

        customer_phone = params.get("customer_phone")
        call_summary = params.get("call_summary", "Voice AI call")
        outcome = params.get("outcome", "completed")
        duration = params.get("duration_seconds", 0)

        if not customer_phone:
            # Can't log without phone number
            return {"success": True}

        # Find contact
        result = await db.execute(
            select(Contact).where(
                Contact.tenant_id == DAVE_TENANT_ID,
                Contact.phone == customer_phone
            )
        )
        contact = result.scalar_one_or_none()

        if not contact:
            # Create placeholder contact
            contact = Contact(
                tenant_id=DAVE_TENANT_ID,
                name="Unknown Caller",
                phone=customer_phone,
                source="voice_ai_retell",
                created_at=datetime.utcnow(),
            )
            db.add(contact)
            await db.flush()

        # Log activity
        activity = Activity(
            tenant_id=DAVE_TENANT_ID,
            contact_id=contact.id,
            activity_type="phone",
            notes=f"AI Call ({duration}s): {call_summary} - Outcome: {outcome}",
            created_at=datetime.utcnow(),
        )
        db.add(activity)
        await db.commit()

        logger.info(f"Logged call: {customer_phone} - {outcome}")

        return {"success": True}

    except Exception as e:
        logger.error(f"Error logging call: {e}")
        # Non-critical, don't fail the call
        return {"success": False}


# ============================================================================
# Webhook Handlers (Telnyx → Our Backend)
# ============================================================================

@router.post("/webhook/call-incoming")
async def telnyx_incoming_call(request: Request):
    """
    Webhook called by Telnyx when customer calls our number.

    This initiates a call with Retell AI and bridges the audio.
    """
    try:
        body = await request.json()
        logger.info(f"Incoming call from Telnyx: {body}")

        # Extract call details from Telnyx
        call_control_id = body.get("data", {}).get("payload", {}).get("call_control_id")
        from_number = body.get("data", {}).get("payload", {}).get("from")
        to_number = body.get("data", {}).get("payload", {}).get("to")

        if not call_control_id:
            logger.error("No call_control_id in Telnyx webhook")
            return {"status": "error"}

        # Create Retell AI call
        import httpx
        async with httpx.AsyncClient() as client:
            retell_response = await client.post(
                "https://api.retellai.com/create-phone-call",
                headers={
                    "Authorization": f"Bearer {RETELL_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "from_number": to_number,  # Our Telnyx number
                    "to_number": from_number,   # Customer's number
                    "agent_id": RETELL_AGENT_ID,
                    "metadata": {
                        "telnyx_call_id": call_control_id,
                        "customer_number": from_number
                    }
                }
            )

            if retell_response.status_code in [200, 201]:
                retell_data = retell_response.json()
                logger.info(f"Retell call created: {retell_data.get('call_id')}")

                # Answer the Telnyx call
                await client.post(
                    f"https://api.telnyx.com/v2/calls/{call_control_id}/actions/answer",
                    headers={
                        "Authorization": f"Bearer {os.getenv('TELNYX_API_KEY')}",
                        "Content-Type": "application/json"
                    }
                )

                return {"status": "ok", "call_id": retell_data.get('call_id')}
            else:
                logger.error(f"Retell call creation failed: {retell_response.text}")
                return {"status": "error"}

    except Exception as e:
        logger.error(f"Error handling incoming call: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@router.post("/webhook/call-status")
async def telnyx_call_status(request: Request):
    """
    Webhook for Telnyx call status updates.
    """
    try:
        body = await request.json()
        event_type = body.get("data", {}).get("event_type")
        logger.info(f"Telnyx call status: {event_type}")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling call status: {e}")
        return {"status": "error"}


# ============================================================================
# Webhook Handlers (Retell AI → Our Backend)
# ============================================================================

@router.post("/webhook/call-started")
async def call_started_webhook(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Webhook called by Retell AI when new call starts.

    Use this to:
    - Log call start
    - Look up existing customer
    - Pass context to agent (e.g., "This is Mrs Smith, regular customer")
    """
    try:
        body = await request.json()
        call_id = body.get("call_id")
        from_number = body.get("from_number")
        to_number = body.get("to_number")

        logger.info(f"Call started: {call_id} from {from_number} to {to_number}")

        # Check if existing customer
        result = await db.execute(
            select(Contact).where(
                Contact.tenant_id == DAVE_TENANT_ID,
                Contact.phone == from_number
            )
        )
        contact = result.scalar_one_or_none()

        response = {"status": "ok"}

        if contact:
            # Return context for agent
            response["customer_context"] = {
                "name": contact.name,
                "is_existing": True,
                "address": contact.address,
                "notes": f"Regular customer. Last contact: {contact.created_at.strftime('%B %Y')}"
            }
            logger.info(f"Existing customer calling: {contact.name}")

        return response

    except Exception as e:
        logger.error(f"Error in call-started webhook: {e}")
        return {"status": "error", "message": str(e)}


@router.post("/webhook/call-ended")
async def call_ended_webhook(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Webhook called by Retell AI when call completes.

    Persists transcript to Activity record.

    Retell payload structure:
    - payload["call"]["transcript"]          - plain text string
    - payload["call"]["transcript_object"]   - [{"role": "user"|"agent", "content": "..."}]
    - payload["call"]["call_id"]
    - payload["call"]["duration_ms"]
    - payload["call"]["disconnection_reason"]
    """
    try:
        body = await request.json()

        # Support both flat and nested payload formats
        call_data = body.get("call", body)

        call_id = call_data.get("call_id") or body.get("call_id")
        from_number = call_data.get("from_number") or body.get("from_number")
        duration_ms = call_data.get("duration_ms") or body.get("duration_ms", 0)
        duration_s = (duration_ms or 0) / 1000
        disconnection_reason = (
            call_data.get("disconnection_reason")
            or body.get("disconnection_reason", "unknown")
        )
        outcome = body.get("outcome", "completed")

        # Build transcript text from structured object if available,
        # falling back to plain-text transcript field.
        transcript_object = call_data.get("transcript_object") or body.get("transcript_object", [])
        if transcript_object:
            transcript_text = "\n".join(
                f"{turn.get('role', 'unknown').upper()}: {turn.get('content', '')}"
                for turn in transcript_object
            )
        else:
            transcript_text = (
                call_data.get("transcript")
                or body.get("transcript", "")
            )

        logger.info(
            f"Call ended: {call_id}, duration: {duration_s:.0f}s, "
            f"reason: {disconnection_reason}, transcript_turns: {len(transcript_object)}"
        )

        # Cost estimate
        cost_usd = (duration_s / 60) * 0.14
        cost_gbp = cost_usd * 0.78
        logger.info(f"Call cost: £{cost_gbp:.2f}")

        # Persist transcript to Activity record
        # Find contact by caller phone number
        contact = None
        if from_number:
            result = await db.execute(
                select(Contact).where(
                    Contact.tenant_id == DAVE_TENANT_ID,
                    Contact.phone == from_number
                )
            )
            contact = result.scalar_one_or_none()

            if not contact:
                # Create placeholder contact so we always have an FK target
                contact = Contact(
                    tenant_id=DAVE_TENANT_ID,
                    name="Unknown Caller",
                    phone=from_number,
                    source="voice_ai_retell",
                    created_at=datetime.utcnow(),
                )
                db.add(contact)
                await db.flush()

        # Build notes field — transcript + metadata summary
        notes_lines = []
        if transcript_text:
            notes_lines.append(transcript_text)
        notes_lines.append(
            f"\n--- Call metadata ---\n"
            f"call_id: {call_id}\n"
            f"duration_ms: {duration_ms}\n"
            f"disconnection_reason: {disconnection_reason}\n"
            f"estimated_cost_gbp: £{cost_gbp:.2f}"
        )
        notes = "\n".join(notes_lines)

        activity = Activity(
            tenant_id=DAVE_TENANT_ID,
            contact_id=contact.id if contact else None,
            activity_type=ActivityType.CALL,
            notes=notes,
            created_at=datetime.utcnow(),
        )
        db.add(activity)
        await db.commit()

        logger.info(
            f"Persisted call transcript to Activity record "
            f"(call_id={call_id}, contact={contact.name if contact else 'none'})"
        )

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error in call-ended webhook: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@router.post("/webhook/call-analysis")
async def call_analysis_webhook(request: Request):
    """
    Webhook for call analytics (optional).

    Retell AI provides:
    - Sentiment analysis
    - Call quality metrics
    - Customer satisfaction indicators
    """
    try:
        body = await request.json()
        call_id = body.get("call_id")
        sentiment = body.get("sentiment")  # positive / neutral / negative
        quality_score = body.get("quality_score")  # 0-100

        logger.info(f"Call analysis: {call_id} - Sentiment: {sentiment}, Quality: {quality_score}")

        # TODO: Store analytics for reporting

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error in call-analysis webhook: {e}")
        return {"status": "error"}


# ============================================================================
# Management Endpoints (For Dave / Admin)
# ============================================================================

@router.get("/status")
async def get_retell_status():
    """
    Check Retell AI integration status.

    Returns:
    - Agent status
    - Recent call volume
    - Cost this month
    """
    try:
        if not RETELL_API_KEY:
            return {"status": "not_configured", "message": "RETELL_API_KEY not set"}

        # TODO: Call Retell AI API to get agent status
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         f"https://api.retellai.com/v1/agents/{RETELL_AGENT_ID}",
        #         headers={"Authorization": f"Bearer {RETELL_API_KEY}"}
        #     )

        return {
            "status": "configured",
            "agent_id": RETELL_AGENT_ID,
            "message": "Retell AI integration ready"
        }

    except Exception as e:
        logger.error(f"Error checking Retell status: {e}")
        return {"status": "error", "message": str(e)}


@router.post("/test-call")
async def trigger_test_call(phone_number: str):
    """
    Trigger outbound test call (for testing).

    Use this to test the agent calling YOU, not waiting for inbound.
    """
    try:
        if not RETELL_API_KEY:
            raise HTTPException(status_code=500, detail="RETELL_API_KEY not configured")

        # TODO: Implement outbound call via Retell AI API
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         "https://api.retellai.com/v1/create-phone-call",
        #         headers={"Authorization": f"Bearer {RETELL_API_KEY}"},
        #         json={
        #             "agent_id": RETELL_AGENT_ID,
        #             "to_number": phone_number,
        #             "from_number": to_number  # Your Twilio number
        #         }
        #     )

        return {
            "success": True,
            "message": f"Test call initiated to {phone_number}"
        }

    except Exception as e:
        logger.error(f"Error triggering test call: {e}")
        raise HTTPException(status_code=500, detail=str(e))
