"""
Customers Routes - Customer management for a client
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from src.db.client import get_prisma

router = APIRouter()


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


def customer_to_response(customer) -> dict:
    """Convert Prisma customer to response dict."""
    return {
        "id": customer.id,
        "client_id": customer.clientId,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "address": customer.address,
        "postcode": customer.postcode,
        "source": customer.source,
        "tags": customer.tags or [],
        "notes": customer.notes,
        "first_job_date": customer.firstJobDate,
        "last_job_date": customer.lastJobDate,
        "total_jobs": customer.totalJobs,
        "total_revenue": float(customer.totalRevenue) if customer.totalRevenue else 0,
        "created_at": customer.createdAt,
        "updated_at": customer.updatedAt,
    }


def customer_with_stats_to_response(customer, job_count: int = 0, invoice_count: int = 0, lead_count: int = 0) -> dict:
    """Convert customer with additional stats."""
    base = customer_to_response(customer)
    base["job_count"] = job_count
    base["invoice_count"] = invoice_count
    base["lead_count"] = lead_count
    return base


@router.get("")
async def list_customers(
    client_id: str,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List customers for a client with optional search."""
    # Verify client exists
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Build where clause
    where = {"clientId": client_id}

    if search:
        where["OR"] = [
            {"name": {"contains": search, "mode": "insensitive"}},
            {"phone": {"contains": search}},
            {"email": {"contains": search, "mode": "insensitive"}},
            {"postcode": {"contains": search, "mode": "insensitive"}},
        ]

    customers = await db.customer.find_many(
        where=where,
        take=limit,
        skip=offset,
        order={"createdAt": "desc"},
    )

    total = await db.customer.count(where=where)

    return {
        "customers": [customer_to_response(c) for c in customers],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(customers) < total,
    }


@router.post("")
async def create_customer(
    client_id: str,
    customer: CustomerCreate,
    db=Depends(get_prisma)
):
    """Create a new customer."""
    # Verify client exists
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Check for duplicate phone
    existing = await db.customer.find_first(
        where={"clientId": client_id, "phone": customer.phone}
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Customer with phone {customer.phone} already exists"
        )

    new_customer = await db.customer.create(
        data={
            "clientId": client_id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "address": customer.address,
            "postcode": customer.postcode,
            "source": customer.source or "manual",
            "tags": customer.tags or [],
            "notes": customer.notes,
        }
    )

    return {
        "id": new_customer.id,
        "message": "Customer created",
        **customer_to_response(new_customer)
    }


@router.get("/{customer_id}")
async def get_customer(
    client_id: str,
    customer_id: str,
    db=Depends(get_prisma)
):
    """Get customer by ID with full details."""
    customer = await db.customer.find_unique(
        where={"id": customer_id},
        include={
            "jobs": {
                "order_by": {"scheduledDate": "desc"},
                "take": 10,
            },
            "leads": {
                "order_by": {"createdAt": "desc"},
                "take": 10,
            },
        }
    )

    if not customer or customer.clientId != client_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Get invoice count
    invoice_count = await db.invoice.count(
        where={"clientId": client_id, "customerEmail": customer.email}
    ) if customer.email else 0

    response = customer_to_response(customer)
    response["jobs"] = [
        {
            "id": job.id,
            "title": job.title,
            "status": job.status,
            "scheduled_date": job.scheduledDate,
            "final_amount": float(job.finalAmount) if job.finalAmount else None,
        }
        for job in (customer.jobs or [])
    ]
    response["leads"] = [
        {
            "id": lead.id,
            "status": lead.status,
            "urgency": lead.urgency,
            "job_type": lead.jobType,
            "created_at": lead.createdAt,
        }
        for lead in (customer.leads or [])
    ]
    response["invoice_count"] = invoice_count

    return response


@router.patch("/{customer_id}")
async def update_customer(
    client_id: str,
    customer_id: str,
    update: CustomerUpdate,
    db=Depends(get_prisma)
):
    """Update a customer."""
    customer = await db.customer.find_unique(where={"id": customer_id})

    if not customer or customer.clientId != client_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Build update data
    data = {}
    if update.name is not None:
        data["name"] = update.name
    if update.phone is not None:
        # Check for duplicate if changing phone
        if update.phone != customer.phone:
            existing = await db.customer.find_first(
                where={"clientId": client_id, "phone": update.phone, "id": {"not": customer_id}}
            )
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Customer with phone {update.phone} already exists"
                )
        data["phone"] = update.phone
    if update.email is not None:
        data["email"] = update.email
    if update.address is not None:
        data["address"] = update.address
    if update.postcode is not None:
        data["postcode"] = update.postcode
    if update.tags is not None:
        data["tags"] = update.tags
    if update.notes is not None:
        data["notes"] = update.notes

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated = await db.customer.update(
        where={"id": customer_id},
        data=data
    )

    return {
        "id": customer_id,
        "message": "Customer updated",
        **customer_to_response(updated)
    }


@router.delete("/{customer_id}")
async def delete_customer(
    client_id: str,
    customer_id: str,
    db=Depends(get_prisma)
):
    """Delete a customer."""
    customer = await db.customer.find_unique(where={"id": customer_id})

    if not customer or customer.clientId != client_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check if customer has jobs
    job_count = await db.job.count(where={"customerId": customer_id})
    if job_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete customer with {job_count} jobs. Archive instead."
        )

    await db.customer.delete(where={"id": customer_id})

    return {"message": "Customer deleted", "id": customer_id}


@router.get("/{customer_id}/timeline")
async def get_customer_timeline(
    client_id: str,
    customer_id: str,
    limit: int = 50,
    db=Depends(get_prisma)
):
    """Get customer activity timeline (jobs, leads, invoices)."""
    customer = await db.customer.find_unique(where={"id": customer_id})

    if not customer or customer.clientId != client_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Get jobs
    jobs = await db.job.find_many(
        where={"customerId": customer_id},
        order={"createdAt": "desc"},
        take=limit,
    )

    # Get leads
    leads = await db.lead.find_many(
        where={"customerId": customer_id},
        order={"createdAt": "desc"},
        take=limit,
    )

    # Get invoices by email if available
    invoices = []
    if customer.email:
        invoices = await db.invoice.find_many(
            where={"clientId": client_id, "customerEmail": customer.email},
            order={"createdAt": "desc"},
            take=limit,
        )

    # Build timeline
    timeline = []

    for job in jobs:
        timeline.append({
            "type": "job",
            "id": job.id,
            "title": job.title,
            "status": job.status,
            "amount": float(job.finalAmount) if job.finalAmount else None,
            "date": job.createdAt,
        })

    for lead in leads:
        timeline.append({
            "type": "lead",
            "id": lead.id,
            "title": f"Call - {lead.jobType or 'Enquiry'}",
            "status": lead.status,
            "urgency": lead.urgency,
            "date": lead.createdAt,
        })

    for invoice in invoices:
        timeline.append({
            "type": "invoice",
            "id": invoice.id,
            "title": f"Invoice {invoice.invoiceNumber}",
            "status": invoice.status,
            "amount": float(invoice.amount),
            "date": invoice.createdAt,
        })

    # Sort by date descending
    timeline.sort(key=lambda x: x["date"], reverse=True)

    return {
        "customer_id": customer_id,
        "timeline": timeline[:limit],
    }
