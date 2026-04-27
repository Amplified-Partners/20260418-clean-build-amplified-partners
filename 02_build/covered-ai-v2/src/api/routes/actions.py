"""
Actions Routes - Autonomous action logging for audit, training, and improvement
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime, timedelta
from enum import Enum

from src.db.client import get_prisma

router = APIRouter()


class AutonomousActionType(str, Enum):
    CALL_CLASSIFIED = "CALL_CLASSIFIED"
    CALL_ESCALATED = "CALL_ESCALATED"
    CALLBACK_SCHEDULED = "CALLBACK_SCHEDULED"
    EMERGENCY_FLAGGED = "EMERGENCY_FLAGGED"
    INVOICE_CREATED = "INVOICE_CREATED"
    INVOICE_SENT = "INVOICE_SENT"
    REMINDER_SENT = "REMINDER_SENT"
    PAYMENT_RECORDED = "PAYMENT_RECORDED"
    REVIEW_REQUEST_SENT = "REVIEW_REQUEST_SENT"
    FOLLOW_UP_SENT = "FOLLOW_UP_SENT"
    QUOTE_GENERATED = "QUOTE_GENERATED"
    FAQ_GENERATED = "FAQ_GENERATED"
    FAQ_PUBLISHED = "FAQ_PUBLISHED"
    GEO_PAGE_UPDATED = "GEO_PAGE_UPDATED"
    SCHEMA_MARKUP_UPDATED = "SCHEMA_MARKUP_UPDATED"
    ATTENTION_ITEM_CREATED = "ATTENTION_ITEM_CREATED"
    ATTENTION_ITEM_RESOLVED = "ATTENTION_ITEM_RESOLVED"
    NURTURE_EMAIL_SENT = "NURTURE_EMAIL_SENT"
    LEAD_SCORED = "LEAD_SCORED"
    LEAD_QUALIFIED = "LEAD_QUALIFIED"


class ActionOutcome(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    PENDING = "PENDING"
    OVERRIDDEN = "OVERRIDDEN"


class ActionCreate(BaseModel):
    clientId: str
    actionType: AutonomousActionType
    description: str
    triggerId: Optional[str] = None
    triggerType: Optional[str] = None
    triggerReason: str
    decision: str
    alternatives: Optional[List[dict]] = None
    confidence: float
    modelUsed: Optional[str] = None
    promptHash: Optional[str] = None
    executionTimeMs: Optional[int] = None
    tokenCount: Optional[int] = None
    costEstimate: Optional[float] = None


class OutcomeUpdate(BaseModel):
    outcome: ActionOutcome
    outcomeDetails: Optional[str] = None


class OverrideCreate(BaseModel):
    userId: str
    reason: str
    alternativeAction: str


def action_to_response(action) -> dict:
    """Convert Prisma action to response dict."""
    return {
        "id": action.id,
        "clientId": action.clientId,
        "actionType": action.actionType,
        "description": action.description,
        "triggerId": action.triggerId,
        "triggerType": action.triggerType,
        "triggerReason": action.triggerReason,
        "decision": action.decision,
        "alternatives": action.alternatives,
        "confidence": action.confidence,
        "modelUsed": action.modelUsed,
        "promptHash": action.promptHash,
        "outcome": action.outcome,
        "outcomeDetails": action.outcomeDetails,
        "outcomeAt": action.outcomeAt.isoformat() if action.outcomeAt else None,
        "wasOverridden": action.wasOverridden,
        "overriddenBy": action.overriddenBy,
        "overrideReason": action.overrideReason,
        "overrideAction": action.overrideAction,
        "overriddenAt": action.overriddenAt.isoformat() if action.overriddenAt else None,
        "executionTimeMs": action.executionTimeMs,
        "tokenCount": action.tokenCount,
        "costEstimate": action.costEstimate,
        "createdAt": action.createdAt.isoformat(),
    }


# =============================================================================
# CREATE ACTION
# =============================================================================

@router.post("")
async def create_action(action: ActionCreate, db=Depends(get_prisma)):
    """Log a new autonomous action."""
    new_action = await db.autonomousaction.create(
        data={
            "clientId": action.clientId,
            "actionType": action.actionType.value,
            "description": action.description,
            "triggerId": action.triggerId,
            "triggerType": action.triggerType,
            "triggerReason": action.triggerReason,
            "decision": action.decision,
            "alternatives": action.alternatives,
            "confidence": action.confidence,
            "modelUsed": action.modelUsed,
            "promptHash": action.promptHash,
            "executionTimeMs": action.executionTimeMs,
            "tokenCount": action.tokenCount,
            "costEstimate": action.costEstimate,
            "outcome": "PENDING",
        }
    )

    return {"id": new_action.id}


# =============================================================================
# UPDATE OUTCOME
# =============================================================================

@router.patch("/{action_id}/outcome")
async def update_action_outcome(
    action_id: str,
    update: OutcomeUpdate,
    db=Depends(get_prisma)
):
    """Update the outcome of an action."""
    action = await db.autonomousaction.find_unique(where={"id": action_id})
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    updated_action = await db.autonomousaction.update(
        where={"id": action_id},
        data={
            "outcome": update.outcome.value,
            "outcomeDetails": update.outcomeDetails,
            "outcomeAt": datetime.utcnow(),
        }
    )

    return action_to_response(updated_action)


# =============================================================================
# RECORD OVERRIDE
# =============================================================================

@router.post("/{action_id}/override")
async def record_override(
    action_id: str,
    override: OverrideCreate,
    db=Depends(get_prisma)
):
    """Record a human override of an action."""
    action = await db.autonomousaction.find_unique(where={"id": action_id})
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    updated_action = await db.autonomousaction.update(
        where={"id": action_id},
        data={
            "wasOverridden": True,
            "overriddenBy": override.userId,
            "overrideReason": override.reason,
            "overrideAction": override.alternativeAction,
            "overriddenAt": datetime.utcnow(),
            "outcome": "OVERRIDDEN",
        }
    )

    return action_to_response(updated_action)


# =============================================================================
# LIST ACTIONS FOR CLIENT
# =============================================================================

@router.get("/clients/{client_id}")
async def list_client_actions(
    client_id: str,
    type: Optional[AutonomousActionType] = None,
    outcome: Optional[ActionOutcome] = None,
    overridden: Optional[bool] = None,
    lowConfidence: Optional[bool] = None,
    limit: int = Query(default=50, le=100),
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List actions for a client with optional filters."""
    where: dict[str, Any] = {"clientId": client_id}

    if type:
        where["actionType"] = type.value
    if outcome:
        where["outcome"] = outcome.value
    if overridden:
        where["wasOverridden"] = True
    if lowConfidence:
        where["confidence"] = {"lt": 0.7}

    actions = await db.autonomousaction.find_many(
        where=where,
        order={"createdAt": "desc"},
        take=limit,
        skip=offset,
    )

    total = await db.autonomousaction.count(where=where)

    return {
        "actions": [action_to_response(a) for a in actions],
        "total": total,
        "hasMore": offset + len(actions) < total,
    }


# =============================================================================
# GET METRICS FOR CLIENT
# =============================================================================

@router.get("/clients/{client_id}/metrics")
async def get_client_action_metrics(
    client_id: str,
    days: int = Query(default=30, le=365),
    db=Depends(get_prisma)
):
    """Get aggregated action metrics for a client."""
    since = datetime.utcnow() - timedelta(days=days)

    actions = await db.autonomousaction.find_many(
        where={
            "clientId": client_id,
            "createdAt": {"gte": since},
        }
    )

    total = len(actions)
    successful = sum(1 for a in actions if a.outcome == "SUCCESS")
    failed = sum(1 for a in actions if a.outcome == "FAILED")
    overridden = sum(1 for a in actions if a.wasOverridden)
    low_confidence = sum(1 for a in actions if a.confidence < 0.7)

    avg_confidence = sum(a.confidence for a in actions) / total if total > 0 else 0
    accuracy_rate = (total - overridden) / total if total > 0 else 1.0
    success_rate = successful / total if total > 0 else 0

    # Group by type
    by_type: dict[str, int] = {}
    for a in actions:
        by_type[a.actionType] = by_type.get(a.actionType, 0) + 1

    # Group by day
    by_day: dict[str, int] = {}
    for a in actions:
        day = a.createdAt.strftime("%Y-%m-%d")
        by_day[day] = by_day.get(day, 0) + 1

    return {
        "period": {
            "days": days,
            "since": since.isoformat(),
        },
        "counts": {
            "total": total,
            "successful": successful,
            "failed": failed,
            "overridden": overridden,
            "lowConfidence": low_confidence,
        },
        "rates": {
            "successRate": round(success_rate, 4),
            "accuracyRate": round(accuracy_rate, 4),
            "avgConfidence": round(avg_confidence, 4),
        },
        "byType": by_type,
        "byDay": by_day,
    }


# =============================================================================
# GET SINGLE ACTION
# =============================================================================

@router.get("/{action_id}")
async def get_action(action_id: str, db=Depends(get_prisma)):
    """Get a single action by ID."""
    action = await db.autonomousaction.find_unique(where={"id": action_id})
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    return action_to_response(action)
