"""
Demo Number Service - Provision and manage personalized demo numbers

Features:
- Provision Twilio UK numbers on demand
- Configure Vapi assistant per number with business name
- Track calls and conversions
- Auto-expire after 14 days
- Release numbers back to pool
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import httpx
import uuid

from prisma import Prisma

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE_URL = "https://api.vapi.ai"
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "https://covered-ai-production.up.railway.app")


class DemoNumberService:
    def __init__(self, db: Prisma):
        self.db = db
        self._twilio_client = None

    @property
    def twilio(self):
        """Lazy-load Twilio client."""
        if self._twilio_client is None and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            from twilio.rest import Client as TwilioClient
            self._twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        return self._twilio_client

    async def provision(
        self,
        business_name: str,
        contact_name: Optional[str] = None,
        contact_email: Optional[str] = None,
        vertical: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Provision a new demo number for a lead.

        1. Buy Twilio number (UK +44)
        2. Create Vapi assistant with business name in greeting
        3. Configure webhook
        4. Store record
        5. Return number details
        """
        # Buy number from Twilio
        phone_number = await self._buy_twilio_number()

        # Create Vapi assistant
        assistant_id = await self._create_vapi_assistant(business_name, vertical)

        # Configure Twilio number to use Vapi
        await self._configure_twilio_number(phone_number, assistant_id)

        # Calculate expiry date
        now = datetime.utcnow()
        expires_at = now + timedelta(days=14)

        # Store record in database
        demo_number = await self.db.demonumber.create(
            data={
                "twilioSid": phone_number.get("sid"),
                "phoneNumber": phone_number.get("phone_number"),
                "businessName": business_name,
                "contactName": contact_name,
                "contactEmail": contact_email,
                "vertical": vertical,
                "vapiAssistantId": assistant_id,
                "status": "active",
                "callCount": 0,
                "expiresAt": expires_at,
            }
        )

        return self._format_demo_number(demo_number)

    async def _buy_twilio_number(self) -> Dict[str, Any]:
        """Buy a UK phone number from Twilio."""
        if not self.twilio:
            # Mock for development
            return {
                "sid": f"PN{uuid.uuid4().hex[:32]}",
                "phone_number": f"+4419{uuid.uuid4().hex[:8]}",
            }

        # Find available UK number
        available = self.twilio.available_phone_numbers('GB').local.list(limit=1)
        if not available:
            raise Exception("No UK numbers available")

        # Purchase it
        number = self.twilio.incoming_phone_numbers.create(
            phone_number=available[0].phone_number
        )

        return {
            "sid": number.sid,
            "phone_number": number.phone_number,
        }

    async def _create_vapi_assistant(
        self,
        business_name: str,
        vertical: Optional[str] = None,
    ) -> Optional[str]:
        """Create Vapi assistant for this demo number."""
        if not VAPI_API_KEY:
            # Mock for development
            return f"asst_demo_{uuid.uuid4().hex[:8]}"

        system_prompt = f"""You are Gemma, the AI receptionist for {business_name}. You have a warm Northern British accent.

Your role:
- Answer calls professionally and warmly
- Capture caller's name, phone number, and reason for calling
- For emergencies, offer to contact someone immediately
- For enquiries, confirm you'll pass the message on
- Be helpful, friendly, and efficient

Opening: "Hi, thanks for calling {business_name}. I'm Gemma, how can I help you today?"

Always end calls by confirming you have their details and someone will be in touch.
This is a demo of Covered AI's phone answering service."""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{VAPI_BASE_URL}/assistant",
                headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
                json={
                    "name": f"Demo - {business_name}",
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
                    "serverUrl": f"{WEBHOOK_BASE_URL}/api/v1/webhooks/demo-call",
                }
            )
            response.raise_for_status()
            return response.json().get("id")

    async def _configure_twilio_number(self, phone_number: Dict, assistant_id: Optional[str]) -> None:
        """Configure Twilio number to route to Vapi."""
        if not self.twilio or not phone_number.get("sid"):
            return

        # Configure the Twilio number's voice webhook to Vapi's endpoint
        # Vapi typically uses a specific URL format for Twilio integration
        vapi_twilio_url = f"https://api.vapi.ai/twilio/inbound_call"

        try:
            self.twilio.incoming_phone_numbers(phone_number["sid"]).update(
                voice_url=vapi_twilio_url,
                voice_method="POST"
            )
        except Exception as e:
            print(f"Warning: Failed to configure Twilio number webhook: {e}")

    def _format_uk_number(self, number: str) -> str:
        """Format UK number for display."""
        if number.startswith("+44"):
            local = "0" + number[3:]
            if len(local) == 11:
                return f"{local[:5]} {local[5:8]} {local[8:]}"
        return number

    def _format_demo_number(self, record) -> Dict[str, Any]:
        """Format demo number record for API response."""
        return {
            "id": record.id,
            "twilio_sid": record.twilioSid,
            "phone_number": record.phoneNumber,
            "phone_number_display": self._format_uk_number(record.phoneNumber),
            "business_name": record.businessName,
            "contact_name": record.contactName,
            "contact_email": record.contactEmail,
            "vertical": record.vertical,
            "vapi_assistant_id": record.vapiAssistantId,
            "status": record.status,
            "call_count": record.callCount,
            "last_called_at": record.lastCalledAt.isoformat() if record.lastCalledAt else None,
            "created_at": record.createdAt.isoformat(),
            "expires_at": record.expiresAt.isoformat(),
            "converted_at": record.convertedAt.isoformat() if record.convertedAt else None,
            "client_id": record.clientId,
        }

    async def get(self, demo_id: str) -> Optional[Dict[str, Any]]:
        """Get demo number by ID."""
        record = await self.db.demonumber.find_unique(where={"id": demo_id})
        if not record:
            return None
        return self._format_demo_number(record)

    async def get_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get demo number by phone number."""
        record = await self.db.demonumber.find_unique(where={"phoneNumber": phone_number})
        if not record:
            return None
        return self._format_demo_number(record)

    async def list(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all demo numbers."""
        where = {}
        if status:
            where["status"] = status

        records = await self.db.demonumber.find_many(
            where=where,
            order_by={"createdAt": "desc"}
        )
        return [self._format_demo_number(r) for r in records]

    async def record_call(self, demo_id: str, call_data: Dict[str, Any]) -> None:
        """Record a call to a demo number."""
        await self.db.demonumber.update(
            where={"id": demo_id},
            data={
                "callCount": {"increment": 1},
                "lastCalledAt": datetime.utcnow(),
            }
        )

    async def extend(self, demo_id: str, days: int = 7) -> Dict[str, Any]:
        """Extend expiry date."""
        record = await self.db.demonumber.find_unique(where={"id": demo_id})
        if not record:
            raise ValueError("Demo number not found")

        new_expiry = record.expiresAt + timedelta(days=days)
        updated = await self.db.demonumber.update(
            where={"id": demo_id},
            data={"expiresAt": new_expiry}
        )

        return self._format_demo_number(updated)

    async def convert(self, demo_id: str, client_id: str) -> Dict[str, Any]:
        """Mark as converted and link to client."""
        record = await self.db.demonumber.find_unique(where={"id": demo_id})
        if not record:
            raise ValueError("Demo number not found")

        updated = await self.db.demonumber.update(
            where={"id": demo_id},
            data={
                "status": "converted",
                "convertedAt": datetime.utcnow(),
                "clientId": client_id,
            }
        )

        return self._format_demo_number(updated)

    async def release(self, demo_id: str) -> None:
        """Release number back to Twilio."""
        record = await self.db.demonumber.find_unique(where={"id": demo_id})
        if not record:
            raise ValueError("Demo number not found")

        # Release from Twilio
        if self.twilio and record.twilioSid:
            try:
                self.twilio.incoming_phone_numbers(record.twilioSid).delete()
            except Exception as e:
                print(f"Failed to release Twilio number: {e}")

        # Delete Vapi assistant
        if VAPI_API_KEY and record.vapiAssistantId:
            try:
                async with httpx.AsyncClient() as client:
                    await client.delete(
                        f"{VAPI_BASE_URL}/assistant/{record.vapiAssistantId}",
                        headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
                    )
            except Exception as e:
                print(f"Failed to delete Vapi assistant: {e}")

        # Delete from database
        await self.db.demonumber.delete(where={"id": demo_id})

    async def expire_old_numbers(self) -> int:
        """Release all expired numbers. Run daily."""
        now = datetime.utcnow()

        # Find expired active numbers
        expired_numbers = await self.db.demonumber.find_many(
            where={
                "status": "active",
                "expiresAt": {"lt": now}
            }
        )

        count = 0
        for record in expired_numbers:
            try:
                await self.release(record.id)
                count += 1
            except Exception as e:
                print(f"Failed to release expired demo number {record.id}: {e}")

        return count


# Helper function to get service instance
def get_demo_number_service(db: Prisma) -> DemoNumberService:
    return DemoNumberService(db)
