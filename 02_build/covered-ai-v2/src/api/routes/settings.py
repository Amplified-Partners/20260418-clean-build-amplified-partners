"""
Settings Routes - Business profile and client settings management
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from src.db.client import get_prisma

router = APIRouter()


class BusinessProfileUpdate(BaseModel):
    business_name: Optional[str] = None
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    website: Optional[str] = None
    vertical: Optional[str] = None


class NotificationSettingsUpdate(BaseModel):
    notification_email: Optional[str] = None
    notification_phone: Optional[str] = None
    notify_via_email: Optional[bool] = None
    notify_via_sms: Optional[bool] = None
    notify_via_whatsapp: Optional[bool] = None


class GemmaSettingsUpdate(BaseModel):
    """Vapi/Gemma AI assistant settings."""
    vapi_assistant_id: Optional[str] = None
    # Future: custom greeting, keywords, etc.


class IntegrationSettingsUpdate(BaseModel):
    google_place_id: Optional[str] = None
    crm_type: Optional[str] = None
    crm_sheet_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None


def client_to_settings_response(client) -> dict:
    """Convert Prisma client to full settings response."""
    return {
        "id": client.id,
        "business_profile": {
            "business_name": client.businessName,
            "owner_name": client.ownerName,
            "phone": client.phone,
            "email": client.email,
            "address": client.address,
            "postcode": client.postcode,
            "website": client.website,
            "vertical": client.vertical,
        },
        "covered_number": client.coveredNumber,
        "notification_settings": {
            "notification_email": client.notificationEmail,
            "notification_phone": client.notificationPhone,
            "notify_via_email": client.notifyViaEmail,
            "notify_via_sms": client.notifyViaSms,
            "notify_via_whatsapp": client.notifyViaWhatsapp,
        },
        "gemma_settings": {
            "vapi_assistant_id": client.vapiAssistantId,
        },
        "integrations": {
            "google_place_id": client.googlePlaceId,
            "crm_type": client.crmType,
            "crm_sheet_id": client.crmSheetId,
            "stripe_customer_id": client.stripeCustomerId,
        },
        "subscription": {
            "plan": client.subscriptionPlan,
            "status": client.subscriptionStatus,
            "trial_ends_at": client.trialEndsAt,
        },
        "created_at": client.createdAt,
        "updated_at": client.updatedAt,
    }


@router.get("/{client_id}")
async def get_settings(client_id: str, db=Depends(get_prisma)):
    """Get all settings for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client_to_settings_response(client)


@router.get("/{client_id}/business-profile")
async def get_business_profile(client_id: str, db=Depends(get_prisma)):
    """Get business profile for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return {
        "business_name": client.businessName,
        "owner_name": client.ownerName,
        "phone": client.phone,
        "email": client.email,
        "address": client.address,
        "postcode": client.postcode,
        "website": client.website,
        "vertical": client.vertical,
    }


@router.patch("/{client_id}/business-profile")
async def update_business_profile(
    client_id: str,
    update: BusinessProfileUpdate,
    db=Depends(get_prisma)
):
    """Update business profile."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    data = {}
    if update.business_name is not None:
        data["businessName"] = update.business_name
    if update.owner_name is not None:
        data["ownerName"] = update.owner_name
    if update.phone is not None:
        data["phone"] = update.phone
    if update.email is not None:
        data["email"] = update.email
    if update.address is not None:
        data["address"] = update.address
    if update.postcode is not None:
        data["postcode"] = update.postcode
    if update.website is not None:
        data["website"] = update.website
    if update.vertical is not None:
        data["vertical"] = update.vertical

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated = await db.client.update(
        where={"id": client_id},
        data=data
    )

    return {
        "message": "Business profile updated",
        "business_name": updated.businessName,
        "owner_name": updated.ownerName,
        "phone": updated.phone,
        "email": updated.email,
        "address": updated.address,
        "postcode": updated.postcode,
        "website": updated.website,
        "vertical": updated.vertical,
    }


@router.get("/{client_id}/notifications")
async def get_notification_settings(client_id: str, db=Depends(get_prisma)):
    """Get notification settings for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return {
        "notification_email": client.notificationEmail,
        "notification_phone": client.notificationPhone,
        "notify_via_email": client.notifyViaEmail,
        "notify_via_sms": client.notifyViaSms,
        "notify_via_whatsapp": client.notifyViaWhatsapp,
    }


@router.patch("/{client_id}/notifications")
async def update_notification_settings(
    client_id: str,
    update: NotificationSettingsUpdate,
    db=Depends(get_prisma)
):
    """Update notification settings."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    data = {}
    if update.notification_email is not None:
        data["notificationEmail"] = update.notification_email
    if update.notification_phone is not None:
        data["notificationPhone"] = update.notification_phone
    if update.notify_via_email is not None:
        data["notifyViaEmail"] = update.notify_via_email
    if update.notify_via_sms is not None:
        data["notifyViaSms"] = update.notify_via_sms
    if update.notify_via_whatsapp is not None:
        data["notifyViaWhatsapp"] = update.notify_via_whatsapp

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated = await db.client.update(
        where={"id": client_id},
        data=data
    )

    return {
        "message": "Notification settings updated",
        "notification_email": updated.notificationEmail,
        "notification_phone": updated.notificationPhone,
        "notify_via_email": updated.notifyViaEmail,
        "notify_via_sms": updated.notifyViaSms,
        "notify_via_whatsapp": updated.notifyViaWhatsapp,
    }


@router.get("/{client_id}/gemma")
async def get_gemma_settings(client_id: str, db=Depends(get_prisma)):
    """Get Gemma AI assistant settings."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return {
        "vapi_assistant_id": client.vapiAssistantId,
        "covered_number": client.coveredNumber,
        "vertical": client.vertical,
        # Future: custom greeting, keywords, etc.
    }


@router.patch("/{client_id}/gemma")
async def update_gemma_settings(
    client_id: str,
    update: GemmaSettingsUpdate,
    db=Depends(get_prisma)
):
    """Update Gemma AI assistant settings."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    data = {}
    if update.vapi_assistant_id is not None:
        data["vapiAssistantId"] = update.vapi_assistant_id

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated = await db.client.update(
        where={"id": client_id},
        data=data
    )

    return {
        "message": "Gemma settings updated",
        "vapi_assistant_id": updated.vapiAssistantId,
    }


@router.get("/{client_id}/integrations")
async def get_integration_settings(client_id: str, db=Depends(get_prisma)):
    """Get integration settings."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return {
        "google_place_id": client.googlePlaceId,
        "crm_type": client.crmType,
        "crm_sheet_id": client.crmSheetId,
        "stripe_customer_id": client.stripeCustomerId,
    }


@router.patch("/{client_id}/integrations")
async def update_integration_settings(
    client_id: str,
    update: IntegrationSettingsUpdate,
    db=Depends(get_prisma)
):
    """Update integration settings."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    data = {}
    if update.google_place_id is not None:
        data["googlePlaceId"] = update.google_place_id
    if update.crm_type is not None:
        data["crmType"] = update.crm_type
    if update.crm_sheet_id is not None:
        data["crmSheetId"] = update.crm_sheet_id
    if update.stripe_customer_id is not None:
        data["stripeCustomerId"] = update.stripe_customer_id

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated = await db.client.update(
        where={"id": client_id},
        data=data
    )

    return {
        "message": "Integration settings updated",
        "google_place_id": updated.googlePlaceId,
        "crm_type": updated.crmType,
        "crm_sheet_id": updated.crmSheetId,
        "stripe_customer_id": updated.stripeCustomerId,
    }


@router.get("/{client_id}/subscription")
async def get_subscription_info(client_id: str, db=Depends(get_prisma)):
    """Get subscription information."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Check if trial is active
    is_trial = client.subscriptionStatus == "trial"
    trial_days_remaining = None
    if is_trial and client.trialEndsAt:
        delta = client.trialEndsAt - datetime.utcnow()
        trial_days_remaining = max(0, delta.days)

    return {
        "plan": client.subscriptionPlan,
        "status": client.subscriptionStatus,
        "is_trial": is_trial,
        "trial_ends_at": client.trialEndsAt,
        "trial_days_remaining": trial_days_remaining,
        "stripe_customer_id": client.stripeCustomerId,
    }
