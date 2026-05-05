---
title: "Module 5: Client Onboarding Automation"
id: "05-client-provisioning"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 5: Client Onboarding Automation

## Overview
When onboarding completes, automatically provision everything the client needs: Vapi assistant, Twilio number, webhooks, welcome email.

## Files to Create

### 1. src/services/client_provisioning.py

```python
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


class ClientProvisioning:
    """
    Handles the full provisioning workflow for new clients.
    """
    
    def __init__(self):
        self.http_client = None
    
    async def __aenter__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.http_client:
            await self.http_client.aclose()
    
    async def provision(self, client_id: str) -> ProvisioningResult:
        """
        Run full provisioning workflow.
        
        Steps:
        1. Load client data
        2. Create Vapi assistant
        3. Assign Twilio number
        4. Configure webhooks
        5. Send welcome email
        6. Create invoice (if applicable)
        7. Schedule check-in
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
        # TODO: Replace with actual database fetch
        # For now, return mock data
        return {
            "id": client_id,
            "business_name": "Test Business",
            "contact_name": "Test User",
            "contact_email": "test@example.com",
            "phone": "+447123456789",
            "vertical": "plumber",
            "covered_number": "+441onal234567",
            "is_trial": False,
            "plan": "standard",
            "plan_price": 297,
        }
    
    async def _create_vapi_assistant(self, client: Dict[str, Any]) -> str:
        """Create Vapi assistant with client-specific config."""
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
                "serverUrl": f"{WEBHOOK_BASE_URL}/api/v1/webhooks/v2/vapi?client_id={client['id']}",
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
        # For now, use the covered_number from onboarding
        # TODO: Implement number pool management
        return client.get("covered_number", "")
    
    async def _configure_webhooks(self, client_id: str, assistant_id: str) -> None:
        """Configure Vapi webhooks to point to our API."""
        if not assistant_id:
            return
        
        webhook_url = f"{WEBHOOK_BASE_URL}/api/v1/webhooks/v2/vapi?client_id={client_id}"
        
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
            
            html_content = f"""
            <html>
            <body style="font-family: sans-serif; line-height: 1.6; color: #333;">
                <h1 style="color: #2563eb;">Welcome to Covered AI! 🎉</h1>
                
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
        # from src.services.invoice import invoice_service
        # return await invoice_service.create(client_id=client["id"], amount=client["plan_price"])
        
        return f"INV-{uuid.uuid4().hex[:8].upper()}"
    
    async def _schedule_checkin(self, client_id: str, days: int = 3) -> None:
        """Schedule a check-in task for N days from now."""
        # TODO: Implement using Trigger.dev
        # from src.jobs import schedule_checkin_job
        # await schedule_checkin_job(client_id, days)
        pass
    
    async def _update_client_record(self, client_id: str, updates: Dict[str, Any]) -> None:
        """Update client record in database."""
        # TODO: Implement database update
        # from src.db import prisma
        # await prisma.client.update(where={"id": client_id}, data=updates)
        pass


async def provision_client(client_id: str) -> ProvisioningResult:
    """Helper function to provision a client."""
    provisioning = ClientProvisioning()
    async with provisioning:
        return await provisioning.provision(client_id)
```

### 2. src/api/routes/provisioning.py

```python
"""
Provisioning API Routes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List

from src.services.client_provisioning import provision_client, ProvisioningResult

router = APIRouter(prefix="/provisioning", tags=["provisioning"])


class ProvisioningStepResponse(BaseModel):
    name: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class ProvisioningResponse(BaseModel):
    success: bool
    client_id: str
    vapi_assistant_id: Optional[str] = None
    twilio_number: Optional[str] = None
    steps: List[ProvisioningStepResponse] = []
    errors: List[str] = []
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# Store results for async lookups
provisioning_results: dict = {}


@router.post("/provision/{client_id}")
async def start_provisioning(client_id: str, background_tasks: BackgroundTasks):
    """
    Trigger provisioning for a client (async).
    Usually called automatically when onboarding completes.
    """
    async def run_provisioning():
        result = await provision_client(client_id)
        provisioning_results[client_id] = result
    
    background_tasks.add_task(run_provisioning)
    return {
        "message": "Provisioning started",
        "client_id": client_id,
        "status_url": f"/api/v1/provisioning/status/{client_id}",
    }


@router.post("/provision/{client_id}/sync", response_model=ProvisioningResponse)
async def provision_client_sync(client_id: str):
    """
    Trigger provisioning synchronously (for testing/debugging).
    Waits for completion and returns full result.
    """
    result = await provision_client(client_id)
    
    # Convert dataclass to response model
    return ProvisioningResponse(
        success=result.success,
        client_id=result.client_id,
        vapi_assistant_id=result.vapi_assistant_id,
        twilio_number=result.twilio_number,
        steps=[
            ProvisioningStepResponse(
                name=s.name,
                status=s.status,
                result=s.result,
                error=s.error,
                started_at=s.started_at,
                completed_at=s.completed_at,
            )
            for s in result.steps
        ],
        errors=result.errors,
        started_at=result.started_at,
        completed_at=result.completed_at,
    )


@router.get("/status/{client_id}")
async def get_provisioning_status(client_id: str):
    """Check provisioning status for a client."""
    if client_id in provisioning_results:
        result = provisioning_results[client_id]
        return {
            "status": "completed" if result.success else "failed",
            "success": result.success,
            "errors": result.errors,
            "vapi_assistant_id": result.vapi_assistant_id,
            "twilio_number": result.twilio_number,
        }
    
    return {
        "status": "pending",
        "message": "Provisioning in progress or not started",
    }


@router.post("/reprovision/{client_id}", response_model=ProvisioningResponse)
async def reprovision_client(client_id: str):
    """
    Re-run provisioning (useful if something failed).
    Runs synchronously.
    """
    result = await provision_client(client_id)
    
    return ProvisioningResponse(
        success=result.success,
        client_id=result.client_id,
        vapi_assistant_id=result.vapi_assistant_id,
        twilio_number=result.twilio_number,
        steps=[
            ProvisioningStepResponse(
                name=s.name,
                status=s.status,
                result=s.result,
                error=s.error,
                started_at=s.started_at,
                completed_at=s.completed_at,
            )
            for s in result.steps
        ],
        errors=result.errors,
        started_at=result.started_at,
        completed_at=result.completed_at,
    )


@router.get("/verticals")
async def list_verticals():
    """List available verticals and their prompts."""
    from src.services.client_provisioning import VERTICAL_PROMPTS
    
    return {
        "verticals": list(VERTICAL_PROMPTS.keys()),
        "default": "default",
    }
```

### 3. Update onboarding completion to trigger provisioning

In src/api/routes/onboarding.py, add this to the step 3 completion:

```python
from fastapi import BackgroundTasks
from src.services.client_provisioning import provision_client

@router.post("/step3/complete")
async def complete_step3(
    client_id: str,
    background_tasks: BackgroundTasks,
):
    """Complete onboarding and trigger provisioning."""
    
    # ... existing step 3 completion logic ...
    
    # Trigger provisioning in background
    async def run_provisioning():
        result = await provision_client(client_id)
        if not result.success:
            # Log error, send alert
            print(f"Provisioning failed for {client_id}: {result.errors}")
    
    background_tasks.add_task(run_provisioning)
    
    return {
        "message": "Onboarding complete - provisioning started",
        "client_id": client_id,
    }
```

### 4. Add to src/api/main.py

```python
from src.api.routes import provisioning
app.include_router(provisioning.router, prefix="/api/v1", tags=["provisioning"])
```

### 5. Add to frontend/src/lib/api.ts

```typescript
export const provisioningApi = {
  start: (clientId: string) =>
    fetchApi<{ message: string; client_id: string; status_url: string }>(
      `/provisioning/provision/${clientId}`,
      { method: "POST" }
    ),
  
  startSync: (clientId: string) =>
    fetchApi<ProvisioningResult>(`/provisioning/provision/${clientId}/sync`, { method: "POST" }),
  
  getStatus: (clientId: string) =>
    fetchApi<ProvisioningStatus>(`/provisioning/status/${clientId}`),
  
  reprovision: (clientId: string) =>
    fetchApi<ProvisioningResult>(`/provisioning/reprovision/${clientId}`, { method: "POST" }),
  
  listVerticals: () =>
    fetchApi<{ verticals: string[]; default: string }>("/provisioning/verticals"),
};

export interface ProvisioningStep {
  name: string;
  status: string;
  result: any | null;
  error: string | null;
  started_at: string | null;
  completed_at: string | null;
}

export interface ProvisioningResult {
  success: boolean;
  client_id: string;
  vapi_assistant_id: string | null;
  twilio_number: string | null;
  steps: ProvisioningStep[];
  errors: string[];
  started_at: string | null;
  completed_at: string | null;
}

export interface ProvisioningStatus {
  status: "pending" | "completed" | "failed";
  success?: boolean;
  errors?: string[];
  vapi_assistant_id?: string;
  twilio_number?: string;
  message?: string;
}
```

### 6. Trigger.dev Job for Scheduled Check-in

Create src/jobs/checkin_reminder.py or trigger-jobs/checkin-reminder.ts:

```typescript
import { schedules, task } from "@trigger.dev/sdk/v3";

// Scheduled daily to check for pending check-ins
export const processCheckins = schedules.task({
  id: "process-client-checkins",
  cron: "0 9 * * *", // Daily at 9am
  run: async () => {
    // Fetch clients due for check-in
    const response = await fetch(
      `${process.env.API_URL}/api/v1/clients?needs_checkin=true`
    );
    const clients = await response.json();
    
    // Send check-in emails
    for (const client of clients) {
      await sendCheckinEmail(client);
    }
    
    return { processed: clients.length };
  },
});

// Individual check-in task (can be triggered)
export const sendClientCheckin = task({
  id: "send-client-checkin",
  run: async (payload: { clientId: string; daysSinceSignup: number }) => {
    const { clientId, daysSinceSignup } = payload;
    
    // Fetch client
    const response = await fetch(
      `${process.env.API_URL}/api/v1/clients/${clientId}`
    );
    const client = await response.json();
    
    // Send appropriate email based on days
    if (daysSinceSignup === 3) {
      await sendDay3Email(client);
    } else if (daysSinceSignup === 7) {
      await sendDay7Email(client);
    } else if (daysSinceSignup === 14) {
      await sendDay14Email(client);
    }
    
    return { sent: true, clientId };
  },
});

async function sendCheckinEmail(client: any) {
  // Implementation
}

async function sendDay3Email(client: any) {
  // "How are the first few days going?"
}

async function sendDay7Email(client: any) {
  // "Week 1 - how many calls has Gemma handled?"
}

async function sendDay14Email(client: any) {
  // "2 weeks in - quick survey"
}
```

## Database Schema Updates

```prisma
model Client {
  id                String    @id @default(cuid())
  businessName      String
  contactName       String
  contactEmail      String
  phone             String?
  vertical          String?
  
  // Provisioning
  vapiAssistantId   String?
  coveredNumber     String?
  status            String    @default("pending") // pending, provisioning, active, suspended
  provisionedAt     DateTime?
  
  // Plan
  plan              String    @default("standard")
  planPrice         Int       @default(297)
  isTrial           Boolean   @default(false)
  trialEndsAt       DateTime?
  
  // Check-ins
  lastCheckinAt     DateTime?
  nextCheckinAt     DateTime?
  
  createdAt         DateTime  @default(now())
  updatedAt         DateTime  @updatedAt
  
  @@index([status])
  @@index([nextCheckinAt])
}
```

## Testing the Provisioning Flow

```bash
# Test sync provisioning (returns immediately with results)
curl -X POST http://localhost:8000/api/v1/provisioning/provision/test-client-123/sync

# Test async provisioning (returns immediately, runs in background)
curl -X POST http://localhost:8000/api/v1/provisioning/provision/test-client-123

# Check status
curl http://localhost:8000/api/v1/provisioning/status/test-client-123

# Reprovision if failed
curl -X POST http://localhost:8000/api/v1/provisioning/reprovision/test-client-123
```
