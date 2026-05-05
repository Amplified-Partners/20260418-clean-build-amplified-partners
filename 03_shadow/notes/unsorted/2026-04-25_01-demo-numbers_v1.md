---
title: "Module 1: Personalized Demo Numbers"
id: "01-demo-numbers"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 1: Personalized Demo Numbers

## Overview
Provision unique Twilio numbers for cold leads. When lead calls, Vapi assistant greets them by business name, creating instant ownership experience.

## Files to Create

### 1. src/services/demo_numbers.py

```python
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
from twilio.rest import Client as TwilioClient
import httpx
import uuid

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_BASE_URL = "https://api.vapi.ai"
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "https://covered-ai-production.up.railway.app")

class DemoNumberService:
    def __init__(self):
        self.twilio = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID else None
        self.numbers: Dict[str, Dict[str, Any]] = {}  # Replace with DB
    
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
        demo_id = str(uuid.uuid4())[:8]
        
        # Buy number from Twilio
        phone_number = await self._buy_twilio_number()
        
        # Create Vapi assistant
        assistant_id = await self._create_vapi_assistant(demo_id, business_name, vertical)
        
        # Configure Twilio number to use Vapi
        await self._configure_twilio_number(phone_number, assistant_id)
        
        # Store record
        now = datetime.utcnow()
        record = {
            "id": demo_id,
            "twilio_sid": phone_number.get("sid"),
            "phone_number": phone_number.get("phone_number"),
            "phone_number_display": self._format_uk_number(phone_number.get("phone_number", "")),
            "business_name": business_name,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "vertical": vertical,
            "vapi_assistant_id": assistant_id,
            "status": "active",
            "call_count": 0,
            "last_called_at": None,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(days=14)).isoformat(),
            "converted_at": None,
            "client_id": None,
        }
        
        self.numbers[demo_id] = record
        return record
    
    async def _buy_twilio_number(self) -> Dict[str, Any]:
        """Buy a UK phone number from Twilio."""
        if not self.twilio:
            # Mock for development
            return {
                "sid": f"PN{uuid.uuid4().hex[:32]}",
                "phone_number": "+441onal234567",
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
        demo_id: str,
        business_name: str,
        vertical: Optional[str] = None,
    ) -> str:
        """Create Vapi assistant for this demo number."""
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
                    "name": f"Demo - {business_name} ({demo_id})",
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
                    "serverUrl": f"{WEBHOOK_BASE_URL}/api/v1/webhooks/demo-call?demo_id={demo_id}",
                }
            )
            response.raise_for_status()
            return response.json().get("id")
    
    async def _configure_twilio_number(self, phone_number: Dict, assistant_id: str) -> None:
        """Configure Twilio number to route to Vapi."""
        # TODO: Set up Twilio webhook to Vapi
        pass
    
    def _format_uk_number(self, number: str) -> str:
        """Format UK number for display."""
        if number.startswith("+44"):
            local = "0" + number[3:]
            if len(local) == 11:
                return f"{local[:5]} {local[5:8]} {local[8:]}"
        return number
    
    async def get(self, demo_id: str) -> Optional[Dict[str, Any]]:
        """Get demo number by ID."""
        return self.numbers.get(demo_id)
    
    async def list(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all demo numbers."""
        numbers = list(self.numbers.values())
        if status:
            numbers = [n for n in numbers if n["status"] == status]
        return sorted(numbers, key=lambda x: x["created_at"], reverse=True)
    
    async def record_call(self, demo_id: str, call_data: Dict[str, Any]) -> None:
        """Record a call to a demo number."""
        if demo_id in self.numbers:
            self.numbers[demo_id]["call_count"] += 1
            self.numbers[demo_id]["last_called_at"] = datetime.utcnow().isoformat()
    
    async def extend(self, demo_id: str, days: int = 7) -> Dict[str, Any]:
        """Extend expiry date."""
        if demo_id not in self.numbers:
            raise ValueError("Demo number not found")
        
        current_expiry = datetime.fromisoformat(self.numbers[demo_id]["expires_at"])
        new_expiry = current_expiry + timedelta(days=days)
        self.numbers[demo_id]["expires_at"] = new_expiry.isoformat()
        
        return self.numbers[demo_id]
    
    async def convert(self, demo_id: str, client_id: str) -> Dict[str, Any]:
        """Mark as converted and link to client."""
        if demo_id not in self.numbers:
            raise ValueError("Demo number not found")
        
        self.numbers[demo_id]["status"] = "converted"
        self.numbers[demo_id]["converted_at"] = datetime.utcnow().isoformat()
        self.numbers[demo_id]["client_id"] = client_id
        
        return self.numbers[demo_id]
    
    async def release(self, demo_id: str) -> None:
        """Release number back to Twilio."""
        record = self.numbers.get(demo_id)
        if not record:
            raise ValueError("Demo number not found")
        
        # Release from Twilio
        if self.twilio and record.get("twilio_sid"):
            try:
                self.twilio.incoming_phone_numbers(record["twilio_sid"]).delete()
            except Exception as e:
                print(f"Failed to release Twilio number: {e}")
        
        # Delete Vapi assistant
        if record.get("vapi_assistant_id"):
            try:
                async with httpx.AsyncClient() as client:
                    await client.delete(
                        f"{VAPI_BASE_URL}/assistant/{record['vapi_assistant_id']}",
                        headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
                    )
            except Exception as e:
                print(f"Failed to delete Vapi assistant: {e}")
        
        # Remove from storage
        del self.numbers[demo_id]
    
    async def expire_old_numbers(self) -> int:
        """Release all expired numbers. Run daily."""
        now = datetime.utcnow()
        expired = []
        
        for demo_id, record in self.numbers.items():
            if record["status"] == "active":
                expires_at = datetime.fromisoformat(record["expires_at"])
                if expires_at < now:
                    expired.append(demo_id)
        
        for demo_id in expired:
            await self.release(demo_id)
        
        return len(expired)

demo_number_service = DemoNumberService()
```

### 2. src/api/routes/demo_numbers.py

```python
"""
Demo Numbers API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from src.services.demo_numbers import demo_number_service

router = APIRouter(prefix="/demo-numbers", tags=["demo-numbers"])


class ProvisionRequest(BaseModel):
    business_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    vertical: Optional[str] = None


class DemoNumberResponse(BaseModel):
    id: str
    phone_number: str
    phone_number_display: str
    business_name: str
    contact_name: Optional[str]
    contact_email: Optional[str]
    vertical: Optional[str]
    status: str
    call_count: int
    created_at: str
    expires_at: str


@router.post("/provision", response_model=DemoNumberResponse)
async def provision_demo_number(request: ProvisionRequest):
    """Provision a new personalized demo number."""
    result = await demo_number_service.provision(
        business_name=request.business_name,
        contact_name=request.contact_name,
        contact_email=request.contact_email,
        vertical=request.vertical,
    )
    return result


@router.get("", response_model=List[DemoNumberResponse])
async def list_demo_numbers(status: Optional[str] = None):
    """List all demo numbers."""
    return await demo_number_service.list(status=status)


@router.get("/{demo_id}", response_model=DemoNumberResponse)
async def get_demo_number(demo_id: str):
    """Get demo number details."""
    result = await demo_number_service.get(demo_id)
    if not result:
        raise HTTPException(status_code=404, detail="Demo number not found")
    return result


@router.post("/{demo_id}/extend")
async def extend_demo_number(demo_id: str, days: int = 7):
    """Extend demo number expiry."""
    try:
        result = await demo_number_service.extend(demo_id, days)
        return {"message": f"Extended by {days} days", "expires_at": result["expires_at"]}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{demo_id}/convert")
async def convert_demo_number(demo_id: str, client_id: str):
    """Mark demo as converted."""
    try:
        await demo_number_service.convert(demo_id, client_id)
        return {"message": "Marked as converted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{demo_id}")
async def release_demo_number(demo_id: str):
    """Release demo number."""
    try:
        await demo_number_service.release(demo_id)
        return {"message": "Number released"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/expire")
async def expire_old_numbers():
    """Manually trigger expiry of old numbers (admin)."""
    count = await demo_number_service.expire_old_numbers()
    return {"message": f"Expired {count} numbers"}
```

### 3. Add to src/api/main.py

```python
from src.api.routes import demo_numbers
app.include_router(demo_numbers.router, prefix="/api/v1", tags=["demo-numbers"])
```

### 4. Add to frontend/src/lib/api.ts

```typescript
export const demoNumbersApi = {
  provision: (data: { business_name: string; contact_name?: string; contact_email?: string; vertical?: string }) =>
    fetchApi<DemoNumber>("/demo-numbers/provision", { method: "POST", body: JSON.stringify(data) }),
  
  list: (status?: string) =>
    fetchApi<DemoNumber[]>(`/demo-numbers${status ? `?status=${status}` : ""}`),
  
  get: (id: string) =>
    fetchApi<DemoNumber>(`/demo-numbers/${id}`),
  
  extend: (id: string, days?: number) =>
    fetchApi<{ message: string; expires_at: string }>(`/demo-numbers/${id}/extend?days=${days || 7}`, { method: "POST" }),
  
  convert: (id: string, clientId: string) =>
    fetchApi<{ message: string }>(`/demo-numbers/${id}/convert?client_id=${clientId}`, { method: "POST" }),
  
  release: (id: string) =>
    fetchApi<{ message: string }>(`/demo-numbers/${id}`, { method: "DELETE" }),
};

export interface DemoNumber {
  id: string;
  phone_number: string;
  phone_number_display: string;
  business_name: string;
  contact_name: string | null;
  contact_email: string | null;
  vertical: string | null;
  status: string;
  call_count: number;
  created_at: string;
  expires_at: string;
}
```

## Database Schema (add to prisma/schema.prisma)

```prisma
model DemoNumber {
  id              String    @id @default(cuid())
  twilioSid       String    @unique
  phoneNumber     String    @unique
  businessName    String
  contactName     String?
  contactEmail    String?
  vertical        String?
  vapiAssistantId String?
  status          String    @default("active")
  callCount       Int       @default(0)
  lastCalledAt    DateTime?
  createdAt       DateTime  @default(now())
  expiresAt       DateTime
  convertedAt     DateTime?
  clientId        String?
}
```

## Webhook for Demo Calls

Add to webhooks_v2.py or create dedicated handler:

```python
@router.post("/demo-call")
async def demo_call_webhook(request: Request, demo_id: str):
    """Handle calls to demo numbers."""
    payload = await request.json()
    
    # Record the call
    await demo_number_service.record_call(demo_id, payload)
    
    # Log event
    await event_log_service.log(
        source=EventSource.VAPI,
        event_type="demo_call",
        payload=payload,
        demo_number_id=demo_id,
    )
    
    return {"status": "ok"}
```
