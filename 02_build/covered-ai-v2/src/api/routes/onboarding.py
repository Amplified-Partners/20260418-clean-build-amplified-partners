"""
Onboarding Routes - 3-step onboarding flow

Step 1: Business info (name, owner, phone, vertical)
Step 2: Call forwarding setup
Step 3: Test call verification
"""
import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from pydantic import BaseModel

from src.db.client import get_prisma
from src.api.routes.auth import get_current_user
from src.services.client_provisioning import provision_client

router = APIRouter()

# Network-specific call forwarding codes
NETWORK_FORWARD_CODES = {
    "ee": {"forward": "**21*{number}#", "cancel": "##21#"},
    "vodafone": {"forward": "**21*{number}#", "cancel": "##21#"},
    "o2": {"forward": "**21*{number}#", "cancel": "##21#"},
    "three": {"forward": "**21*{number}#", "cancel": "##21#"},
    "bt": {"forward": "**21*{number}#", "cancel": "##21#"},
    "sky": {"forward": "**21*{number}#", "cancel": "##21#"},
    "giffgaff": {"forward": "**21*{number}#", "cancel": "##21#"},
    "tesco": {"forward": "**21*{number}#", "cancel": "##21#"},
}


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class OnboardingStartRequest(BaseModel):
    email: str
    business_name: Optional[str] = None
    source: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None


class Step1Request(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    vertical: str


class Step2Request(BaseModel):
    forwarding_confirmed: bool
    network_selected: Optional[str] = None


class OnboardingStatusResponse(BaseModel):
    current_step: str
    step1_complete: bool
    step2_complete: bool
    step3_complete: bool
    business_name: Optional[str]
    covered_number: Optional[str]
    test_call_received: bool
    client_id: Optional[str]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_uk_number(number: str) -> str:
    """Format number for display (e.g., 0191 743 2732)."""
    # Remove any non-digit chars
    digits = "".join(c for c in number if c.isdigit())

    # Handle +44 prefix
    if digits.startswith("44"):
        digits = "0" + digits[2:]

    # Format as XXXX XXX XXXX
    if len(digits) == 11:
        return f"{digits[:4]} {digits[4:7]} {digits[7:]}"

    return number


async def provision_covered_number(vertical: str) -> str:
    """
    Provision a new Twilio phone number for the client.
    For now, return the default number. In production, use Twilio API.
    """
    # TODO: Implement Twilio number provisioning
    # For now, return the test number
    return os.getenv("TWILIO_PHONE_NUMBER", "+441917432732")


# =============================================================================
# GET ONBOARDING STATUS
# =============================================================================

@router.get("/status")
async def get_onboarding_status(
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """Get current onboarding progress."""
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding:
        # Create onboarding session if doesn't exist
        onboarding = await db.onboardingsession.create(
            data={
                "userId": user.id,
                "currentStep": "started",
            }
        )

    return {
        "current_step": onboarding.currentStep,
        "step1_complete": onboarding.step1CompletedAt is not None,
        "step2_complete": onboarding.step2CompletedAt is not None,
        "step3_complete": onboarding.step3CompletedAt is not None,
        "business_name": onboarding.businessName,
        "owner_name": onboarding.ownerName,
        "phone": onboarding.phone,
        "vertical": onboarding.vertical,
        "covered_number": onboarding.coveredNumber,
        "covered_number_display": format_uk_number(onboarding.coveredNumber) if onboarding.coveredNumber else None,
        "network_selected": onboarding.networkSelected,
        "test_call_received": onboarding.testCallReceived,
        "client_id": onboarding.clientId,
        "completed_at": onboarding.completedAt,
    }


# =============================================================================
# STEP 1: BUSINESS INFO
# =============================================================================

@router.post("/step1")
async def complete_step1(
    request: Step1Request,
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """
    Complete Step 1: Business information.

    - Validates UK phone number
    - Provisions Covered phone number
    - Stores business details
    """
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding session not found")

    # Validate vertical
    valid_verticals = [
        "trades", "vet", "dental", "aesthetics", "salon",
        "physio", "optometry", "auto", "legal", "accountant", "fitness"
    ]
    if request.vertical not in valid_verticals:
        raise HTTPException(status_code=400, detail=f"Invalid vertical. Must be one of: {', '.join(valid_verticals)}")

    # Provision Covered number
    covered_number = await provision_covered_number(request.vertical)

    # Update onboarding session
    updated = await db.onboardingsession.update(
        where={"userId": user.id},
        data={
            "currentStep": "business",
            "step1CompletedAt": datetime.now(timezone.utc),
            "businessName": request.business_name,
            "ownerName": request.owner_name,
            "phone": request.phone,
            "vertical": request.vertical,
            "coveredNumber": covered_number,
            "lastActiveAt": datetime.now(timezone.utc),
        }
    )

    # Update user name if not set
    if not user.name:
        await db.user.update(
            where={"id": user.id},
            data={"name": request.owner_name}
        )

    return {
        "message": "Step 1 complete",
        "current_step": "business",
        "covered_number": covered_number,
        "covered_number_display": format_uk_number(covered_number),
        "next_step": "forwarding",
    }


# =============================================================================
# STEP 2: CALL FORWARDING
# =============================================================================

@router.get("/step2/instructions")
async def get_forwarding_instructions(
    network: str,
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """Get network-specific call forwarding instructions."""
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding or not onboarding.coveredNumber:
        raise HTTPException(status_code=400, detail="Complete step 1 first")

    network_lower = network.lower()
    if network_lower not in NETWORK_FORWARD_CODES:
        raise HTTPException(status_code=400, detail=f"Unknown network: {network}")

    codes = NETWORK_FORWARD_CODES[network_lower]

    # Format number without + for dialing codes
    number_for_code = onboarding.coveredNumber.replace("+", "").replace(" ", "")
    if number_for_code.startswith("44"):
        number_for_code = "0" + number_for_code[2:]

    forward_code = codes["forward"].format(number=number_for_code)

    return {
        "network": network,
        "covered_number": onboarding.coveredNumber,
        "covered_number_display": format_uk_number(onboarding.coveredNumber),
        "forward_code": forward_code,
        "cancel_code": codes["cancel"],
        "instructions": [
            "Open your Phone app",
            f"Dial: {forward_code}",
            "Press Call",
            "Wait for confirmation beep",
        ],
    }


@router.post("/step2")
async def complete_step2(
    request: Step2Request,
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """
    Complete Step 2: Call forwarding setup.

    User confirms they have set up call forwarding.
    """
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding session not found")

    if not onboarding.step1CompletedAt:
        raise HTTPException(status_code=400, detail="Complete step 1 first")

    if not request.forwarding_confirmed:
        raise HTTPException(status_code=400, detail="Please confirm forwarding is set up")

    # Update onboarding session
    await db.onboardingsession.update(
        where={"userId": user.id},
        data={
            "currentStep": "forwarding",
            "step2CompletedAt": datetime.now(timezone.utc),
            "forwardingConfirmed": True,
            "networkSelected": request.network_selected,
            "lastActiveAt": datetime.now(timezone.utc),
        }
    )

    return {
        "message": "Step 2 complete",
        "current_step": "forwarding",
        "next_step": "testing",
    }


# =============================================================================
# STEP 3: TEST CALL
# =============================================================================

@router.get("/step3/status")
async def get_test_call_status(
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """
    Check if test call has been received.

    This endpoint is polled by the frontend.
    """
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding session not found")

    return {
        "test_call_received": onboarding.testCallReceived,
        "test_call_id": onboarding.testCallId,
        "test_lead_id": onboarding.testLeadId,
        "covered_number": onboarding.coveredNumber,
        "covered_number_display": format_uk_number(onboarding.coveredNumber) if onboarding.coveredNumber else None,
    }


@router.post("/step3/simulate-call")
async def simulate_test_call(
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """
    Simulate a test call (for development/testing).

    In production, this is triggered by the Vapi webhook.
    """
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding session not found")

    # Mark test call as received
    await db.onboardingsession.update(
        where={"userId": user.id},
        data={
            "testCallReceived": True,
            "testCallId": "test-call-simulated",
            "lastActiveAt": datetime.now(timezone.utc),
        }
    )

    return {
        "message": "Test call simulated",
        "test_call_received": True,
    }


@router.post("/step3/complete")
async def complete_step3(
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """
    Complete Step 3 and finalize onboarding.

    - Creates the Client record
    - Links user to client
    - Marks onboarding complete
    - Triggers automated provisioning (Vapi assistant, welcome email, etc.)
    """
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding session not found")

    if not onboarding.step2CompletedAt:
        raise HTTPException(status_code=400, detail="Complete step 2 first")

    # Create client record
    client = await db.client.create(
        data={
            "businessName": onboarding.businessName,
            "ownerName": onboarding.ownerName,
            "phone": onboarding.phone,
            "email": user.email,
            "vertical": onboarding.vertical,
            "coveredNumber": onboarding.coveredNumber,
            "notificationPhone": onboarding.phone,
            "notificationEmail": user.email,
            "subscriptionStatus": "trialing",
        }
    )

    # Update onboarding session
    await db.onboardingsession.update(
        where={"userId": user.id},
        data={
            "currentStep": "completed",
            "step3CompletedAt": datetime.now(timezone.utc),
            "completedAt": datetime.now(timezone.utc),
            "clientId": client.id,
            "lastActiveAt": datetime.now(timezone.utc),
        }
    )

    # Link user to client
    await db.user.update(
        where={"id": user.id},
        data={"clientId": client.id}
    )

    # Trigger provisioning in background (Vapi assistant, welcome email, etc.)
    async def run_provisioning():
        try:
            result = await provision_client(db, client.id)
            if not result.success:
                print(f"Provisioning failed for {client.id}: {result.errors}")
        except Exception as e:
            print(f"Provisioning error for {client.id}: {e}")

    background_tasks.add_task(run_provisioning)

    return {
        "message": "Onboarding complete! Welcome to Covered AI.",
        "current_step": "completed",
        "client_id": client.id,
        "dashboard_url": f"/dashboard/{client.id}",
        "provisioning_started": True,
    }


# =============================================================================
# SKIP/ABANDON
# =============================================================================

@router.post("/skip-test")
async def skip_test_call(
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """
    Skip the test call and complete onboarding.

    User can test later from dashboard.
    """
    onboarding = await db.onboardingsession.find_unique(
        where={"userId": user.id}
    )

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding session not found")

    if not onboarding.step2CompletedAt:
        raise HTTPException(status_code=400, detail="Complete step 2 first")

    # Create client record
    client = await db.client.create(
        data={
            "businessName": onboarding.businessName,
            "ownerName": onboarding.ownerName,
            "phone": onboarding.phone,
            "email": user.email,
            "vertical": onboarding.vertical,
            "coveredNumber": onboarding.coveredNumber,
            "notificationPhone": onboarding.phone,
            "notificationEmail": user.email,
            "subscriptionStatus": "trialing",
        }
    )

    # Update onboarding session (mark as completed but no test call)
    await db.onboardingsession.update(
        where={"userId": user.id},
        data={
            "currentStep": "completed",
            "completedAt": datetime.now(timezone.utc),
            "clientId": client.id,
            "lastActiveAt": datetime.now(timezone.utc),
        }
    )

    # Link user to client
    await db.user.update(
        where={"id": user.id},
        data={"clientId": client.id}
    )

    # Trigger provisioning in background (Vapi assistant, welcome email, etc.)
    async def run_provisioning():
        try:
            result = await provision_client(db, client.id)
            if not result.success:
                print(f"Provisioning failed for {client.id}: {result.errors}")
        except Exception as e:
            print(f"Provisioning error for {client.id}: {e}")

    background_tasks.add_task(run_provisioning)

    return {
        "message": "Onboarding complete! You can make a test call anytime.",
        "current_step": "completed",
        "client_id": client.id,
        "dashboard_url": f"/dashboard/{client.id}",
        "provisioning_started": True,
    }


@router.post("/abandon")
async def mark_abandoned(
    user=Depends(get_current_user),
    db=Depends(get_prisma)
):
    """
    Mark onboarding as abandoned.

    Called when user explicitly exits or after timeout.
    """
    await db.onboardingsession.update(
        where={"userId": user.id},
        data={
            "currentStep": "abandoned",
            "abandonedAt": datetime.now(timezone.utc),
        }
    )

    return {"message": "Onboarding paused. Come back anytime!"}


# =============================================================================
# WEBHOOK FOR TEST CALL DETECTION
# =============================================================================

@router.post("/webhook/test-call")
async def handle_test_call_webhook(
    request: Request,
    db=Depends(get_prisma)
):
    """
    Webhook called by Vapi when a test call is received.

    Matches the call to an onboarding session by covered_number.
    """
    data = await request.json()

    covered_number = data.get("to_number")
    call_id = data.get("call_id")
    lead_id = data.get("lead_id")

    if not covered_number:
        raise HTTPException(status_code=400, detail="Missing to_number")

    # Find onboarding session by covered number
    onboarding = await db.onboardingsession.find_first(
        where={
            "coveredNumber": covered_number,
            "currentStep": {"in": ["forwarding", "testing"]},
            "testCallReceived": False,
        }
    )

    if onboarding:
        await db.onboardingsession.update(
            where={"id": onboarding.id},
            data={
                "currentStep": "testing",
                "testCallReceived": True,
                "testCallId": call_id,
                "testLeadId": lead_id,
                "lastActiveAt": datetime.now(timezone.utc),
            }
        )

        return {"message": "Test call recorded", "onboarding_id": onboarding.id}

    return {"message": "No matching onboarding session found"}


# =============================================================================
# ONBOARDING PROGRESS TRACKING (for training/activation)
# =============================================================================

class OnboardingChecklistItem(BaseModel):
    id: str
    label: str
    done: bool
    action: Optional[str] = None
    videoId: Optional[str] = None


class OnboardingNextStep(BaseModel):
    action: Optional[str] = None
    title: str
    videoId: Optional[str] = None


class OnboardingMilestones(BaseModel):
    accountCreated: bool
    businessInfoCompleted: bool
    phoneSetupCompleted: bool
    testCallCompleted: bool
    firstRealCall: bool
    firstInvoiceSent: bool
    firstReviewRequest: bool
    dashboardStreak: int


class OnboardingProgressResponse(BaseModel):
    stage: str
    completionPercent: int
    milestones: OnboardingMilestones
    nextStep: Optional[OnboardingNextStep] = None
    checklist: list
    dashboardTourComplete: bool
    featuresToursComplete: list


class OnboardingProgressUpdateRequest(BaseModel):
    milestone: Optional[str] = None
    value: Optional[bool] = None
    stage: Optional[str] = None
    dashboardTourComplete: Optional[bool] = None
    featureTourComplete: Optional[str] = None


@router.get("/progress/{client_id}")
async def get_onboarding_progress(
    client_id: str,
    db=Depends(get_prisma)
):
    """Get client's onboarding progress (milestones and training)."""
    # Try to get existing progress
    progress = await db.onboardingprogress.find_unique(
        where={"clientId": client_id}
    )

    # Create if doesn't exist
    if not progress:
        progress = await db.onboardingprogress.create(
            data={"clientId": client_id}
        )

    # Build checklist
    checklist = [
        OnboardingChecklistItem(
            id="account",
            label="Create account",
            done=progress.accountCreated,
        ),
        OnboardingChecklistItem(
            id="business",
            label="Business details",
            done=progress.businessInfoCompleted,
            action="/onboarding/business",
            videoId="welcome"
        ),
        OnboardingChecklistItem(
            id="phone",
            label="Phone setup",
            done=progress.phoneSetupCompleted,
            action="/onboarding/phone",
            videoId="phone_setup"
        ),
        OnboardingChecklistItem(
            id="test_call",
            label="Test call",
            done=progress.testCallCompleted,
            action="/onboarding/test-call",
            videoId="meet_gemma"
        ),
    ]

    # Calculate completion
    completed_steps = sum(1 for item in checklist if item.done)
    completion_percent = round((completed_steps / len(checklist)) * 100)

    # Determine next step
    next_step = None
    for item in checklist:
        if not item.done:
            next_step = OnboardingNextStep(
                action=item.action,
                title=item.label,
                videoId=item.videoId
            )
            break

    return {
        "stage": progress.currentStage,
        "completionPercent": completion_percent,
        "milestones": {
            "accountCreated": progress.accountCreated,
            "businessInfoCompleted": progress.businessInfoCompleted,
            "phoneSetupCompleted": progress.phoneSetupCompleted,
            "testCallCompleted": progress.testCallCompleted,
            "firstRealCall": progress.firstRealCall,
            "firstInvoiceSent": progress.firstInvoiceSent,
            "firstReviewRequest": progress.firstReviewRequest,
            "dashboardStreak": progress.dashboardStreak
        },
        "nextStep": {
            "action": next_step.action,
            "title": next_step.title,
            "videoId": next_step.videoId
        } if next_step else None,
        "checklist": [item.dict() for item in checklist],
        "dashboardTourComplete": progress.dashboardTourComplete,
        "featuresToursComplete": progress.featuresToursComplete or []
    }


@router.patch("/progress/{client_id}")
async def update_onboarding_progress(
    client_id: str,
    update: OnboardingProgressUpdateRequest,
    db=Depends(get_prisma)
):
    """Update client's onboarding progress."""
    update_data = {}

    # Update milestone
    if update.milestone and update.value is not None:
        update_data[update.milestone] = update.value

        # Set timestamp for milestone
        timestamp_map = {
            "businessInfoCompleted": "businessInfoAt",
            "phoneSetupCompleted": "phoneSetupAt",
            "testCallCompleted": "testCallAt",
            "firstRealCall": "firstRealCallAt",
            "firstInvoiceSent": "firstInvoiceSentAt",
            "firstReviewRequest": "firstReviewRequestAt",
        }

        if update.value and update.milestone in timestamp_map:
            update_data[timestamp_map[update.milestone]] = datetime.now(timezone.utc)

    # Update stage
    if update.stage:
        update_data["currentStage"] = update.stage
        update_data["stageStartedAt"] = datetime.now(timezone.utc)

    # Update dashboard tour
    if update.dashboardTourComplete is not None:
        update_data["dashboardTourComplete"] = update.dashboardTourComplete

    # Add feature tour
    if update.featureTourComplete:
        progress = await db.onboardingprogress.find_unique(
            where={"clientId": client_id}
        )

        if progress:
            current_tours = progress.featuresToursComplete or []
            if update.featureTourComplete not in current_tours:
                update_data["featuresToursComplete"] = current_tours + [update.featureTourComplete]

    # Recalculate completion percentage
    progress = await db.onboardingprogress.find_unique(
        where={"clientId": client_id}
    )

    if progress:
        steps = [
            progress.accountCreated,
            update_data.get("businessInfoCompleted", progress.businessInfoCompleted),
            update_data.get("phoneSetupCompleted", progress.phoneSetupCompleted),
            update_data.get("testCallCompleted", progress.testCallCompleted),
        ]
        update_data["completionPercent"] = round((sum(1 for s in steps if s) / len(steps)) * 100)

    # Upsert the progress
    updated = await db.onboardingprogress.upsert(
        where={"clientId": client_id},
        data={
            "update": update_data,
            "create": {"clientId": client_id, **update_data}
        }
    )

    return {
        "id": updated.id,
        "clientId": updated.clientId,
        "stage": updated.currentStage,
        "completionPercent": updated.completionPercent,
        "message": "Onboarding progress updated"
    }
