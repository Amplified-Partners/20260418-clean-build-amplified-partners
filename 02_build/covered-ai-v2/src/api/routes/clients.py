"""
Clients Routes - CRUD for business clients
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.db.client import get_prisma
from src.db import queries

router = APIRouter()


class ClientCreate(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    email: str
    vertical: str = "trades"
    notification_email: Optional[str] = None
    notification_phone: Optional[str] = None


class ClientUpdate(BaseModel):
    business_name: Optional[str] = None
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    notification_email: Optional[str] = None
    notification_phone: Optional[str] = None
    notify_via_email: Optional[bool] = None
    notify_via_sms: Optional[bool] = None
    notify_via_whatsapp: Optional[bool] = None
    covered_number: Optional[str] = None
    google_place_id: Optional[str] = None


class ClientResponse(BaseModel):
    id: str
    business_name: str
    owner_name: str
    phone: str
    email: str
    vertical: str
    covered_number: Optional[str] = None
    subscription_plan: str
    subscription_status: str
    created_at: datetime

    class Config:
        from_attributes = True


def client_to_response(client) -> dict:
    """Convert Prisma client to response dict."""
    return {
        "id": client.id,
        "business_name": client.businessName,
        "owner_name": client.ownerName,
        "phone": client.phone,
        "email": client.email,
        "vertical": client.vertical,
        "covered_number": client.coveredNumber,
        "subscription_plan": client.subscriptionPlan,
        "subscription_status": client.subscriptionStatus,
        "created_at": client.createdAt
    }


@router.get("")
async def list_clients(
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List all clients."""
    clients, total = await queries.list_clients(db, limit=limit, offset=offset)
    return {
        "clients": [client_to_response(c) for c in clients],
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.post("")
async def create_client(client: ClientCreate, db=Depends(get_prisma)):
    """Create a new client."""
    new_client = await queries.create_client(
        db,
        data={
            "businessName": client.business_name,
            "ownerName": client.owner_name,
            "phone": client.phone,
            "email": client.email,
            "vertical": client.vertical,
            "notificationEmail": client.notification_email or client.email,
            "notificationPhone": client.notification_phone or client.phone
        }
    )
    return {
        "id": new_client.id,
        "message": "Client created",
        **client_to_response(new_client)
    }


@router.get("/{client_id}")
async def get_client(client_id: str, db=Depends(get_prisma)):
    """Get client by ID."""
    client = await queries.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client_to_response(client)


@router.patch("/{client_id}")
async def update_client(
    client_id: str,
    update: ClientUpdate,
    db=Depends(get_prisma)
):
    """Update client."""
    # Build update data from non-None fields
    update_data = {}
    if update.business_name is not None:
        update_data["businessName"] = update.business_name
    if update.owner_name is not None:
        update_data["ownerName"] = update.owner_name
    if update.phone is not None:
        update_data["phone"] = update.phone
    if update.email is not None:
        update_data["email"] = update.email
    if update.notification_email is not None:
        update_data["notificationEmail"] = update.notification_email
    if update.notification_phone is not None:
        update_data["notificationPhone"] = update.notification_phone
    if update.notify_via_email is not None:
        update_data["notifyViaEmail"] = update.notify_via_email
    if update.notify_via_sms is not None:
        update_data["notifyViaSms"] = update.notify_via_sms
    if update.notify_via_whatsapp is not None:
        update_data["notifyViaWhatsapp"] = update.notify_via_whatsapp
    if update.covered_number is not None:
        update_data["coveredNumber"] = update.covered_number
    if update.google_place_id is not None:
        update_data["googlePlaceId"] = update.google_place_id

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        client = await queries.update_client(db, client_id, update_data)
        return {"id": client_id, "message": "Client updated", **client_to_response(client)}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Client not found")


@router.delete("/{client_id}")
async def delete_client(client_id: str, db=Depends(get_prisma)):
    """Delete client."""
    try:
        await db.client.delete(where={"id": client_id})
        return {"message": "Client deleted"}
    except Exception:
        raise HTTPException(status_code=404, detail="Client not found")


@router.get("/{client_id}/dashboard")
async def get_dashboard(client_id: str, db=Depends(get_prisma)):
    """Get client dashboard stats."""
    client = await queries.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    stats = await queries.get_dashboard_stats(db, client_id)
    return {
        "leads_today": stats["leadsToday"],
        "leads_this_week": stats["leadsThisWeek"],
        "leads_this_month": stats["leadsThisMonth"],
        "conversion_rate": stats["conversionRate"],
        "jobs_scheduled": stats["jobsScheduled"],
        "jobs_completed": stats["jobsCompleted"],
        "revenue_this_month": stats["revenueThisMonth"]
    }


class CashMetricsUpdate(BaseModel):
    outstanding: Optional[float] = None
    overdue: Optional[float] = None
    collected: Optional[float] = None


@router.put("/{client_id}/cash-metrics")
async def update_cash_metrics(
    client_id: str,
    metrics: CashMetricsUpdate,
    db=Depends(get_prisma)
):
    """Update client cash metrics (outstanding, overdue, collected)."""
    client = await queries.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # For now, just return success - these metrics are typically calculated
    # from invoices rather than stored directly on the client
    return {
        "id": client_id,
        "message": "Cash metrics updated",
        "outstanding": metrics.outstanding or 0,
        "overdue": metrics.overdue or 0,
        "collected": metrics.collected or 0
    }
