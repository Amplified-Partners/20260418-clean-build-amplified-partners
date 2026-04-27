"""
Quotes Routes - Quote management for a client
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum

from src.db.client import get_prisma

router = APIRouter()


class QuoteStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    VIEWED = "VIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CONVERTED = "CONVERTED"


class LineItem(BaseModel):
    description: str
    quantity: float = 1
    unit_price: float
    total: Optional[float] = None


class QuoteCreate(BaseModel):
    customer_id: Optional[str] = None
    lead_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    line_items: List[LineItem]
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    valid_days: int = 30
    vat_rate: float = 0.20
    internal_notes: Optional[str] = None
    customer_notes: Optional[str] = None
    send_now: bool = False


class QuoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    line_items: Optional[List[LineItem]] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    valid_until: Optional[datetime] = None
    vat_rate: Optional[float] = None
    internal_notes: Optional[str] = None
    customer_notes: Optional[str] = None


def quote_to_response(quote) -> dict:
    """Convert Prisma quote to response dict."""
    return {
        "id": quote.id,
        "client_id": quote.clientId,
        "customer_id": quote.customerId,
        "lead_id": quote.leadId,
        "quote_number": quote.quoteNumber,
        "title": quote.title,
        "description": quote.description,
        "line_items": quote.lineItems,
        "subtotal": float(quote.subtotal),
        "vat_rate": float(quote.vatRate),
        "vat_amount": float(quote.vatAmount),
        "total": float(quote.total),
        "customer_name": quote.customerName,
        "customer_email": quote.customerEmail,
        "customer_phone": quote.customerPhone,
        "customer_address": quote.customerAddress,
        "valid_until": quote.validUntil,
        "status": quote.status,
        "sent_at": quote.sentAt,
        "viewed_at": quote.viewedAt,
        "accepted_at": quote.acceptedAt,
        "rejected_at": quote.rejectedAt,
        "rejection_reason": quote.rejectionReason,
        "converted_to_job_id": quote.convertedToJobId,
        "converted_at": quote.convertedAt,
        "internal_notes": quote.internalNotes,
        "customer_notes": quote.customerNotes,
        "created_at": quote.createdAt,
        "updated_at": quote.updatedAt,
    }


async def generate_quote_number(db, client_id: str) -> str:
    """Generate unique quote number: QT-YYYYMM-SEQ"""
    now = datetime.utcnow()
    prefix = f"QT-{now.strftime('%Y%m')}"

    count = await db.quote.count(
        where={
            "clientId": client_id,
            "quoteNumber": {"startswith": prefix}
        }
    )

    seq = count + 1
    return f"{prefix}-{seq:04d}"


def calculate_quote_totals(line_items: List[LineItem], vat_rate: float) -> tuple:
    """Calculate subtotal, VAT amount, and total."""
    subtotal = sum(
        (item.total if item.total else item.quantity * item.unit_price)
        for item in line_items
    )
    vat_amount = subtotal * vat_rate
    total = subtotal + vat_amount
    return subtotal, vat_amount, total


@router.get("")
async def list_quotes(
    client_id: str,
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List quotes for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    where = {"clientId": client_id}

    if status:
        statuses = [s.strip() for s in status.split(",")]
        if len(statuses) == 1:
            where["status"] = statuses[0]
        else:
            where["status"] = {"in": statuses}

    if customer_id:
        where["customerId"] = customer_id

    quotes = await db.quote.find_many(
        where=where,
        order={"createdAt": "desc"},
        take=limit,
        skip=offset,
    )

    total = await db.quote.count(where=where)

    return {
        "quotes": [quote_to_response(q) for q in quotes],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(quotes) < total,
    }


@router.post("")
async def create_quote(
    client_id: str,
    quote: QuoteCreate,
    db=Depends(get_prisma)
):
    """Create a new quote."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Generate quote number
    quote_number = await generate_quote_number(db, client_id)

    # Calculate totals
    subtotal, vat_amount, total = calculate_quote_totals(quote.line_items, quote.vat_rate)

    # Convert line items to JSON-serializable format
    line_items_json = [
        {
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total": item.total or item.quantity * item.unit_price,
        }
        for item in quote.line_items
    ]

    # Calculate valid_until
    valid_until = datetime.utcnow() + timedelta(days=quote.valid_days)

    new_quote = await db.quote.create(
        data={
            "clientId": client_id,
            "customerId": quote.customer_id,
            "leadId": quote.lead_id,
            "quoteNumber": quote_number,
            "title": quote.title,
            "description": quote.description,
            "lineItems": line_items_json,
            "subtotal": Decimal(str(subtotal)),
            "vatRate": Decimal(str(quote.vat_rate)),
            "vatAmount": Decimal(str(vat_amount)),
            "total": Decimal(str(total)),
            "customerName": quote.customer_name,
            "customerEmail": quote.customer_email,
            "customerPhone": quote.customer_phone,
            "customerAddress": quote.customer_address,
            "validUntil": valid_until,
            "status": "DRAFT",
            "internalNotes": quote.internal_notes,
            "customerNotes": quote.customer_notes,
        }
    )

    result = {
        "id": new_quote.id,
        "quote_number": quote_number,
        "message": "Quote created",
        **quote_to_response(new_quote)
    }

    if quote.send_now:
        # TODO: Trigger send-quote job via Trigger.dev
        print(f"Quote {quote_number} queued for sending")
        result["send_queued"] = True

    return result


@router.get("/{quote_id}")
async def get_quote(client_id: str, quote_id: str, db=Depends(get_prisma)):
    """Get quote by ID."""
    quote = await db.quote.find_unique(
        where={"id": quote_id},
        include={"customer": True}
    )

    if not quote or quote.clientId != client_id:
        raise HTTPException(status_code=404, detail="Quote not found")

    response = quote_to_response(quote)
    if quote.customer:
        response["customer"] = {
            "id": quote.customer.id,
            "name": quote.customer.name,
            "phone": quote.customer.phone,
            "email": quote.customer.email,
        }

    return response


@router.patch("/{quote_id}")
async def update_quote(
    client_id: str,
    quote_id: str,
    update: QuoteUpdate,
    db=Depends(get_prisma)
):
    """Update a quote (only if DRAFT)."""
    quote = await db.quote.find_unique(where={"id": quote_id})

    if not quote or quote.clientId != client_id:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status != "DRAFT":
        raise HTTPException(
            status_code=400,
            detail="Can only update DRAFT quotes"
        )

    data = {}
    if update.title is not None:
        data["title"] = update.title
    if update.description is not None:
        data["description"] = update.description
    if update.customer_name is not None:
        data["customerName"] = update.customer_name
    if update.customer_email is not None:
        data["customerEmail"] = update.customer_email
    if update.customer_phone is not None:
        data["customerPhone"] = update.customer_phone
    if update.customer_address is not None:
        data["customerAddress"] = update.customer_address
    if update.valid_until is not None:
        data["validUntil"] = update.valid_until
    if update.internal_notes is not None:
        data["internalNotes"] = update.internal_notes
    if update.customer_notes is not None:
        data["customerNotes"] = update.customer_notes

    # Handle line items update
    if update.line_items is not None:
        vat_rate = float(update.vat_rate) if update.vat_rate else float(quote.vatRate)
        subtotal, vat_amount, total = calculate_quote_totals(update.line_items, vat_rate)

        line_items_json = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.total or item.quantity * item.unit_price,
            }
            for item in update.line_items
        ]

        data["lineItems"] = line_items_json
        data["subtotal"] = Decimal(str(subtotal))
        data["vatAmount"] = Decimal(str(vat_amount))
        data["total"] = Decimal(str(total))

    if update.vat_rate is not None and update.line_items is None:
        # Recalculate with existing line items
        line_items = [LineItem(**item) for item in quote.lineItems]
        subtotal, vat_amount, total = calculate_quote_totals(line_items, update.vat_rate)
        data["vatRate"] = Decimal(str(update.vat_rate))
        data["vatAmount"] = Decimal(str(vat_amount))
        data["total"] = Decimal(str(total))

    if data:
        quote = await db.quote.update(
            where={"id": quote_id},
            data=data
        )

    return {"id": quote_id, "message": "Quote updated", **quote_to_response(quote)}


@router.delete("/{quote_id}")
async def delete_quote(client_id: str, quote_id: str, db=Depends(get_prisma)):
    """Delete a quote (only if DRAFT)."""
    quote = await db.quote.find_unique(where={"id": quote_id})

    if not quote or quote.clientId != client_id:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status != "DRAFT":
        raise HTTPException(
            status_code=400,
            detail="Can only delete DRAFT quotes"
        )

    await db.quote.delete(where={"id": quote_id})

    return {"message": "Quote deleted", "id": quote_id}


@router.post("/{quote_id}/send")
async def send_quote(client_id: str, quote_id: str, db=Depends(get_prisma)):
    """Send a quote to the customer."""
    quote = await db.quote.find_unique(where={"id": quote_id})

    if not quote or quote.clientId != client_id:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status not in ["DRAFT", "SENT"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot send quote with status {quote.status}"
        )

    if not quote.customerEmail:
        raise HTTPException(
            status_code=400,
            detail="Quote has no customer email"
        )

    # Update status
    updated = await db.quote.update(
        where={"id": quote_id},
        data={
            "status": "SENT",
            "sentAt": datetime.utcnow(),
        }
    )

    # TODO: Trigger send-quote job via Trigger.dev
    print(f"Quote {quote.quoteNumber} sent to {quote.customerEmail}")

    return {
        "id": quote_id,
        "quote_number": quote.quoteNumber,
        "message": "Quote sent",
        "sent_to": quote.customerEmail,
    }


@router.post("/{quote_id}/accept")
async def accept_quote(client_id: str, quote_id: str, db=Depends(get_prisma)):
    """Mark a quote as accepted."""
    quote = await db.quote.find_unique(where={"id": quote_id})

    if not quote or quote.clientId != client_id:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status in ["ACCEPTED", "CONVERTED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot accept quote with status {quote.status}"
        )

    updated = await db.quote.update(
        where={"id": quote_id},
        data={
            "status": "ACCEPTED",
            "acceptedAt": datetime.utcnow(),
        }
    )

    return {
        "id": quote_id,
        "status": "ACCEPTED",
        "message": "Quote accepted",
    }


@router.post("/{quote_id}/reject")
async def reject_quote(
    client_id: str,
    quote_id: str,
    reason: Optional[str] = None,
    db=Depends(get_prisma)
):
    """Mark a quote as rejected."""
    quote = await db.quote.find_unique(where={"id": quote_id})

    if not quote or quote.clientId != client_id:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status in ["ACCEPTED", "CONVERTED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reject quote with status {quote.status}"
        )

    updated = await db.quote.update(
        where={"id": quote_id},
        data={
            "status": "REJECTED",
            "rejectedAt": datetime.utcnow(),
            "rejectionReason": reason,
        }
    )

    return {
        "id": quote_id,
        "status": "REJECTED",
        "reason": reason,
        "message": "Quote rejected",
    }


@router.post("/{quote_id}/convert")
async def convert_quote_to_job(
    client_id: str,
    quote_id: str,
    scheduled_date: datetime,
    scheduled_time: Optional[str] = None,
    db=Depends(get_prisma)
):
    """Convert an accepted quote to a job."""
    quote = await db.quote.find_unique(
        where={"id": quote_id},
        include={"customer": True}
    )

    if not quote or quote.clientId != client_id:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status not in ["ACCEPTED", "SENT", "VIEWED"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot convert quote with status {quote.status}"
        )

    if quote.convertedToJobId:
        raise HTTPException(
            status_code=400,
            detail=f"Quote already converted to job {quote.convertedToJobId}"
        )

    # Create job from quote
    job = await db.job.create(
        data={
            "clientId": client_id,
            "customerId": quote.customerId,
            "leadId": quote.leadId,
            "title": quote.title,
            "description": quote.description,
            "address": quote.customerAddress or "",
            "scheduledDate": scheduled_date,
            "scheduledTime": scheduled_time,
            "quotedAmount": quote.total,
            "status": "scheduled",
        },
        include={"customer": True}
    )

    # Update quote
    await db.quote.update(
        where={"id": quote_id},
        data={
            "status": "CONVERTED",
            "convertedToJobId": job.id,
            "convertedAt": datetime.utcnow(),
        }
    )

    return {
        "id": quote_id,
        "status": "CONVERTED",
        "job_id": job.id,
        "message": "Quote converted to job",
        "job": {
            "id": job.id,
            "title": job.title,
            "scheduled_date": job.scheduledDate,
            "quoted_amount": float(quote.total),
        }
    }
