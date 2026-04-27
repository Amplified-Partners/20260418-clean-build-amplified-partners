"""
Client Provisioning Service - Automated setup for new clients

When onboarding completes:
1. Create Vapi assistant with client-specific config
2. Assign or provision Twilio number
3. Configure webhook endpoints
4. Send welcome email
5. Create first invoice (if not trial)
6. Schedule follow-up check-in
"""

import os
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import uuid

from prisma import Prisma

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE_URL = "https://api.vapi.ai"
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "https://covered-ai-production.up.railway.app")
FROM_EMAIL = os.getenv("FROM_EMAIL", "Ewan from Covered AI <ewan@covered.ai>")


@dataclass
class ProvisioningStep:
    name: str
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class ProvisioningResult:
    success: bool
    client_id: str
    vapi_assistant_id: Optional[str] = None
    twilio_number: Optional[str] = None
    steps: List[ProvisioningStep] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# System prompts by vertical
VERTICAL_PROMPTS = {
    "plumber": """You are Gemma, the AI receptionist for {business_name}, a plumbing company. You have a warm Northern British accent.

Your role:
- Answer calls professionally and warmly
- Capture caller's name, phone number, and the plumbing issue
- For emergencies (burst pipes, flooding, gas leaks), mark as URGENT and offer to contact the plumber immediately
- For routine jobs (dripping taps, boiler service), book the enquiry and confirm callback
- Be helpful, friendly, and efficient

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Emergency keywords: flood, flooding, burst, leak, gas, no hot water, no heating, sewage
Always ask: "Is this an emergency or something that can wait for a callback?"

End calls by confirming you have their details and someone will be in touch shortly.""",

    "electrician": """You are Gemma, the AI receptionist for {business_name}, an electrical company. You have a warm Northern British accent.

Your role:
- Answer calls professionally and warmly
- Capture caller's name, phone number, and the electrical issue
- For emergencies (sparks, burning smell, no power), mark as URGENT
- For routine jobs (socket installation, light fitting), book the enquiry
- Be helpful, friendly, and efficient

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Emergency keywords: sparks, burning, smoke, no power, exposed wires, electric shock
Always ask: "Is this an emergency situation right now?"

End calls by confirming you have their details and someone will be in touch shortly.""",

    "salon": """You are Gemma, the AI receptionist for {business_name}, a salon. You have a warm Northern British accent.

Your role:
- Answer calls professionally and warmly
- Help with appointment enquiries
- Capture caller's name, phone number, and what service they're interested in
- Note any specific stylist requests
- Be helpful, friendly, and welcoming

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Common services: haircut, colour, highlights, blow dry, styling, treatments
Always ask: "Do you have a preferred stylist or are you happy with whoever is available?"

End calls by confirming you have their details and someone will call back to confirm the appointment.""",

    "vet": """You are Gemma, the AI receptionist for {business_name}, a veterinary practice. You have a warm Northern British accent.

Your role:
- Answer calls professionally and with empathy
- Capture caller's name, phone number, pet's name, and the concern
- For emergencies (breathing difficulty, bleeding, collapse, poisoning), mark as URGENT
- Be calm, reassuring, and efficient

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Emergency keywords: breathing, choking, bleeding, collapse, unconscious, poison, hit by car, seizure
Always ask: "Is your pet showing any signs of distress right now?"

End calls by confirming you have their details and a vet will be in touch.""",

    "dental": """You are Gemma, the AI receptionist for {business_name}, a dental practice. You have a warm Northern British accent.

Your role:
- Answer calls professionally and warmly
- Help with appointment enquiries and emergencies
- Capture caller's name, phone number, and the dental concern
- For emergencies (severe pain, swelling, knocked out tooth), mark as URGENT
- Be helpful, friendly, and reassuring

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Emergency keywords: severe pain, swelling, abscess, knocked out, broken tooth, bleeding
Always ask: "Are you in severe pain right now?"

End calls by confirming you have their details and someone will be in touch.""",

    "physio": """You are Gemma, the AI receptionist for {business_name}, a physiotherapy practice. You have a warm Northern British accent.

Your role:
- Answer calls professionally and warmly
- Help with appointment enquiries
- Capture caller's name, phone number, and what they need treatment for
- Be helpful, friendly, and understanding

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Common issues: back pain, neck pain, sports injury, post-surgery rehab, shoulder pain
Always ask: "Is this a new issue or are you an existing patient?"

End calls by confirming you have their details and someone will call back to book an appointment.""",

    "default": """You are Gemma, the AI receptionist for {business_name}. You have a warm Northern British accent.

Your role:
- Answer calls professionally and warmly
- Capture caller's name, phone number, and reason for calling
- For urgent matters, offer to contact someone immediately
- For enquiries, confirm someone will call back
- Be helpful, friendly, and efficient

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Always end calls by confirming you have their details and someone will be in touch.""",
}


class ClientProvisioningService:
    """
    Handles the full provisioning workflow for new clients.
    """

    def __init__(self, db: Prisma):
        self.db = db
        self.http_client: Optional[httpx.AsyncClient] = None

    async def provision(self, client_id: str) -> ProvisioningResult:
        """
        Run full provisioning workflow.

        Steps:
        1. Load client data
        2. Create Vapi assistant
        3. Assign Twilio number (use existing or provision new)
        4. Configure webhooks
        5. Send welcome email
        6. Create invoice (if applicable)
        7. Schedule check-in
        8. Update client record
        """
        result = ProvisioningResult(
            success=False,
            client_id=client_id,
            started_at=datetime.utcnow().isoformat(),
        )

        steps = [
            ("load_client", self._load_client),
            ("create_vapi_assistant", self._create_vapi_assistant),
            ("assign_number", self._assign_number),
            ("configure_webhooks", self._configure_webhooks),
            ("send_welcome_email", self._send_welcome_email),
            ("create_invoice", self._create_first_invoice),
            ("schedule_checkin", self._schedule_checkin),
            ("update_client", self._update_client_record),
        ]

        client = None
        assistant_id = None
        number = None

        async with httpx.AsyncClient(timeout=30.0) as http:
            self.http_client = http

            for step_name, step_func in steps:
                step = ProvisioningStep(name=step_name)
                step.started_at = datetime.utcnow().isoformat()
                result.steps.append(step)

                try:
                    step.status = "running"

                    if step_name == "load_client":
                        client = await step_func(client_id)
                        step.result = {"business_name": client.get("business_name")}

                    elif step_name == "create_vapi_assistant":
                        assistant_id = await step_func(client)
                        result.vapi_assistant_id = assistant_id
                        step.result = {"assistant_id": assistant_id}

                    elif step_name == "assign_number":
                        number = await step_func(client)
                        result.twilio_number = number
                        step.result = {"number": number}

                    elif step_name == "configure_webhooks":
                        await step_func(client_id, assistant_id)
                        step.result = {"configured": True}

                    elif step_name == "send_welcome_email":
                        await step_func(client)
                        step.result = {"sent": True}

                    elif step_name == "create_invoice":
                        if not client.get("is_trial"):
                            invoice_id = await step_func(client)
                            step.result = {"invoice_id": invoice_id}
                        else:
                            step.result = {"skipped": "trial account"}

                    elif step_name == "schedule_checkin":
                        await step_func(client_id)
                        step.result = {"scheduled": True}

                    elif step_name == "update_client":
                        await step_func(client_id, {
                            "vapi_assistant_id": assistant_id,
                            "covered_number": number,
                            "provisioned_at": datetime.utcnow().isoformat(),
                            "status": "active",
                        })
                        step.result = {"updated": True}

                    step.status = "completed"
                    step.completed_at = datetime.utcnow().isoformat()

                except Exception as e:
                    step.status = "failed"
                    step.error = str(e)
                    step.completed_at = datetime.utcnow().isoformat()
                    result.errors.append(f"{step_name}: {str(e)}")

                    # Critical steps that should stop provisioning
                    if step_name in ["load_client", "create_vapi_assistant"]:
                        break

        # Check if all critical steps completed
        critical_steps = ["load_client", "create_vapi_assistant", "assign_number"]
        critical_completed = all(
            s.status == "completed"
            for s in result.steps
            if s.name in critical_steps
        )

        result.success = critical_completed
        result.completed_at = datetime.utcnow().isoformat()

        return result

    async def _load_client(self, client_id: str) -> Dict[str, Any]:
        """Load client from database."""
        client = await self.db.client.find_unique(where={"id": client_id})

        if not client:
            raise ValueError(f"Client not found: {client_id}")

        return {
            "id": client.id,
            "business_name": client.businessName,
            "contact_name": client.ownerName,
            "contact_email": client.email,
            "phone": client.phone,
            "vertical": client.vertical or "default",
            "covered_number": client.coveredNumber,
            "is_trial": client.subscriptionStatus == "trialing",
            "plan": client.subscriptionPlan or "standard",
            "plan_price": 297,  # Default price
        }

    async def _create_vapi_assistant(self, client: Dict[str, Any]) -> str:
        """Create Vapi assistant with client-specific config."""
        if not VAPI_API_KEY:
            raise ValueError("VAPI_API_KEY not configured")

        vertical = client.get("vertical", "default")
        business_name = client.get("business_name", "the business")

        # Get vertical-specific prompt
        prompt_template = VERTICAL_PROMPTS.get(vertical, VERTICAL_PROMPTS["default"])
        system_prompt = prompt_template.format(business_name=business_name)

        # Create assistant
        response = await self.http_client.post(
            f"{VAPI_BASE_URL}/assistant",
            headers={
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "name": f"Gemma - {business_name} ({client['id']})",
                "model": {
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                    "systemPrompt": system_prompt,
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": "21m00Tcm4TlvDq8ikWAM",  # British female
                },
                "firstMessage": f"Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?",
                "serverUrl": f"{WEBHOOK_BASE_URL}/api/v1/webhooks/vapi/call-complete",
                "endCallMessage": "Thanks for calling. Someone will be in touch shortly. Goodbye!",
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-2",
                    "language": "en-GB",
                },
                "silenceTimeoutSeconds": 30,
                "maxDurationSeconds": 600,  # 10 minutes max
            }
        )
        response.raise_for_status()
        return response.json().get("id")

    async def _assign_number(self, client: Dict[str, Any]) -> str:
        """Assign a Twilio number to the client."""
        # Use the covered_number from onboarding if already assigned
        if client.get("covered_number"):
            return client["covered_number"]

        # TODO: Implement number pool management or provision new number
        # For now, raise an error if no number assigned during onboarding
        raise ValueError("No covered number assigned during onboarding")

    async def _configure_webhooks(self, client_id: str, assistant_id: str) -> None:
        """Configure Vapi webhooks to point to our API."""
        if not assistant_id or not VAPI_API_KEY:
            return

        webhook_url = f"{WEBHOOK_BASE_URL}/api/v1/webhooks/vapi/call-complete"

        await self.http_client.patch(
            f"{VAPI_BASE_URL}/assistant/{assistant_id}",
            headers={
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "serverUrl": webhook_url,
            }
        )

    async def _send_welcome_email(self, client: Dict[str, Any]) -> None:
        """Send welcome email to new client."""
        try:
            import resend
            resend.api_key = os.getenv("RESEND_API_KEY")

            if not resend.api_key:
                print("RESEND_API_KEY not configured, skipping welcome email")
                return

            html_content = f"""
            <html>
            <body style="font-family: sans-serif; line-height: 1.6; color: #333;">
                <h1 style="color: #2563eb;">Welcome to Covered AI!</h1>

                <p>Hi {client.get('contact_name', 'there')},</p>

                <p>Great news - Gemma is now answering calls for <strong>{client.get('business_name')}</strong>.</p>

                <h2 style="color: #2563eb; font-size: 18px;">What happens now?</h2>

                <ol>
                    <li><strong>Forward your calls</strong> - Set up call forwarding to your Covered number</li>
                    <li><strong>Test it</strong> - Call your number and hear Gemma in action</li>
                    <li><strong>Check your dashboard</strong> - See calls and leads come in</li>
                </ol>

                <p>Your Covered number: <strong>{client.get('covered_number', 'See dashboard')}</strong></p>

                <p>
                    <a href="https://app.covered.ai/dashboard"
                       style="display: inline-block; background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                        Go to Dashboard
                    </a>
                </p>

                <p>Any questions? Just reply to this email - I read every one.</p>

                <p>Ewan<br>Covered AI</p>
            </body>
            </html>
            """

            resend.Emails.send({
                "from": FROM_EMAIL,
                "to": client.get("contact_email"),
                "subject": f"Welcome to Covered AI - Gemma is live for {client.get('business_name')}!",
                "html": html_content,
            })

        except Exception as e:
            print(f"Failed to send welcome email: {e}")
            # Don't fail provisioning for email issues

    async def _create_first_invoice(self, client: Dict[str, Any]) -> Optional[str]:
        """Create first invoice for non-trial clients."""
        if client.get("is_trial"):
            return None

        # TODO: Implement invoice creation via invoice service
        # For now, just return a placeholder ID
        return f"INV-{uuid.uuid4().hex[:8].upper()}"

    async def _schedule_checkin(self, client_id: str, days: int = 3) -> None:
        """Schedule a check-in task for N days from now."""
        # Update client with next check-in date
        next_checkin = datetime.utcnow() + timedelta(days=days)

        await self.db.client.update(
            where={"id": client_id},
            data={"nextCheckinAt": next_checkin}
        )

    async def _update_client_record(self, client_id: str, updates: Dict[str, Any]) -> None:
        """Update client record in database."""
        update_data = {}

        if updates.get("vapi_assistant_id"):
            update_data["vapiAssistantId"] = updates["vapi_assistant_id"]
        if updates.get("covered_number"):
            update_data["coveredNumber"] = updates["covered_number"]
        if updates.get("provisioned_at"):
            update_data["provisionedAt"] = datetime.fromisoformat(updates["provisioned_at"])
        if updates.get("status"):
            update_data["subscriptionStatus"] = "active"

        if update_data:
            await self.db.client.update(
                where={"id": client_id},
                data=update_data
            )


def get_provisioning_service(db: Prisma) -> ClientProvisioningService:
    """Factory function for dependency injection."""
    return ClientProvisioningService(db)


async def provision_client(db: Prisma, client_id: str) -> ProvisioningResult:
    """Helper function to provision a client."""
    service = ClientProvisioningService(db)
    return await service.provision(client_id)
