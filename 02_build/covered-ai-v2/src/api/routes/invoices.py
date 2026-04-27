"""
Invoice Routes - Invoice management and cash flow
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

from src.db.client import get_prisma

router = APIRouter()


class InvoiceStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    REMINDED = "REMINDED"
    OVERDUE = "OVERDUE"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    WRITTEN_OFF = "WRITTEN_OFF"


class InvoiceCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    job_id: Optional[str] = None
    amount: float
    description: str
    due_date: date
    send_now: bool = False


class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    due_date: Optional[date] = None


class InvoiceStatusUpdate(BaseModel):
    status: InvoiceStatus
    sent_at: Optional[datetime] = None
    reminder_1_sent_at: Optional[datetime] = None
    reminder_2_sent_at: Optional[datetime] = None
    final_notice_sent_at: Optional[datetime] = None


class MarkPaid(BaseModel):
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None


class CashMetricsUpdate(BaseModel):
    total_outstanding: float
    total_overdue: float
    collected_this_month: float
    collected_last_month: float
    average_dso: int


def invoice_to_response(invoice) -> dict:
    """Convert Prisma invoice to response dict."""
    return {
        "id": invoice.id,
        "client_id": invoice.clientId,
        "job_id": invoice.jobId,
        "customer_name": invoice.customerName,
        "customer_email": invoice.customerEmail,
        "customer_phone": invoice.customerPhone,
        "invoice_number": invoice.invoiceNumber,
        "amount": float(invoice.amount),
        "description": invoice.description,
        "due_date": invoice.dueDate,
        "status": invoice.status,
        "sent_at": invoice.sentAt,
        "reminder_1_sent_at": invoice.reminder1SentAt,
        "reminder_2_sent_at": invoice.reminder2SentAt,
        "final_notice_sent_at": invoice.finalNoticeSentAt,
        "paid_at": invoice.paidAt,
        "paid_amount": float(invoice.paidAmount) if invoice.paidAmount else None,
        "payment_method": invoice.paymentMethod,
        "payment_reference": invoice.paymentReference,
        # PDF & Email fields (Phase 1)
        "pdf_url": invoice.pdfUrl,
        "pdf_generated_at": invoice.pdfGeneratedAt,
        "view_token": invoice.viewToken,
        # Stripe fields (Phase 2)
        "payment_link_url": invoice.paymentLinkUrl,
        "payment_link_id": invoice.paymentLinkId,
        "stripe_payment_intent_id": invoice.stripePaymentIntentId,
        "stripe_charge_id": invoice.stripeChargeId,
        # Xero fields (Phase 4)
        "xero_invoice_id": invoice.xeroInvoiceId,
        "xero_contact_id": invoice.xeroContactId,
        "xero_synced_at": invoice.xeroSyncedAt,
        "xero_sync_error": invoice.xeroSyncError,
        # Timestamps
        "created_at": invoice.createdAt,
        "updated_at": invoice.updatedAt,
    }


async def generate_invoice_number(db, client_id: str) -> str:
    """Generate unique invoice number: INV-YYYYMM-SEQ"""
    now = datetime.utcnow()
    prefix = f"INV-{now.strftime('%Y%m')}"

    # Count existing invoices this month for this client
    count = await db.invoice.count(
        where={
            "clientId": client_id,
            "invoiceNumber": {"startswith": prefix}
        }
    )

    seq = count + 1
    return f"{prefix}-{seq:04d}"


# =============================================================================
# INVOICE ROUTES
# =============================================================================

@router.get("")
async def list_invoices(
    client_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List invoices with optional filters."""
    where = {}

    if client_id:
        where["clientId"] = client_id

    if status:
        # Handle comma-separated statuses
        statuses = [s.strip() for s in status.split(",")]
        if len(statuses) == 1:
            where["status"] = statuses[0]
        else:
            where["status"] = {"in": statuses}

    invoices = await db.invoice.find_many(
        where=where,
        order={"createdAt": "desc"},
        take=limit,
        skip=offset,
    )

    total = await db.invoice.count(where=where)

    return {
        "invoices": [invoice_to_response(inv) for inv in invoices],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("")
async def create_invoice(
    invoice: InvoiceCreate,
    client_id: str,
    db=Depends(get_prisma)
):
    """Create a new invoice."""
    # Verify client exists
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Generate invoice number
    invoice_number = await generate_invoice_number(db, client_id)

    # Create invoice
    new_invoice = await db.invoice.create(
        data={
            "clientId": client_id,
            "jobId": invoice.job_id,
            "customerName": invoice.customer_name,
            "customerEmail": invoice.customer_email,
            "customerPhone": invoice.customer_phone,
            "invoiceNumber": invoice_number,
            "amount": Decimal(str(invoice.amount)),
            "description": invoice.description,
            "dueDate": datetime.combine(invoice.due_date, datetime.min.time()),
            "status": "DRAFT",
        }
    )

    result = {
        "id": new_invoice.id,
        "invoice_number": invoice_number,
        "message": "Invoice created",
        **invoice_to_response(new_invoice)
    }

    # If send_now is True, trigger the send job
    if invoice.send_now:
        # TODO: Trigger send-invoice job via Trigger.dev
        print(f"Invoice {invoice_number} queued for sending")
        result["send_queued"] = True

    return result


@router.get("/clients-with-invoices")
async def get_clients_with_invoices(db=Depends(get_prisma)):
    """Get list of client IDs that have invoices."""
    invoices = await db.invoice.find_many(
        distinct=["clientId"]
    )

    client_ids = list(set(inv.clientId for inv in invoices))

    return {"clientIds": client_ids}


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: str, db=Depends(get_prisma)):
    """Get invoice by ID."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice_to_response(invoice)


@router.patch("/{invoice_id}")
async def update_invoice(
    invoice_id: str,
    update: InvoiceUpdate,
    db=Depends(get_prisma)
):
    """Update invoice (only if DRAFT)."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status != "DRAFT":
        raise HTTPException(
            status_code=400,
            detail="Can only update DRAFT invoices"
        )

    # Build update data
    data = {}
    if update.customer_name is not None:
        data["customerName"] = update.customer_name
    if update.customer_email is not None:
        data["customerEmail"] = update.customer_email
    if update.amount is not None:
        data["amount"] = Decimal(str(update.amount))
    if update.description is not None:
        data["description"] = update.description
    if update.due_date is not None:
        data["dueDate"] = datetime.combine(update.due_date, datetime.min.time())

    if data:
        invoice = await db.invoice.update(
            where={"id": invoice_id},
            data=data
        )

    return {"id": invoice_id, "message": "Invoice updated", **invoice_to_response(invoice)}


@router.post("/{invoice_id}/send")
async def send_invoice(invoice_id: str, db=Depends(get_prisma)):
    """Send an invoice (trigger send-invoice job)."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status not in ["DRAFT", "SENT"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot send invoice with status {invoice.status}"
        )

    # TODO: Trigger send-invoice job via Trigger.dev
    print(f"Invoice {invoice.invoiceNumber} queued for sending")

    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "message": "Invoice queued for sending",
        "send_queued": True,
    }


@router.post("/{invoice_id}/paid")
async def mark_invoice_paid(
    invoice_id: str,
    payment: MarkPaid,
    db=Depends(get_prisma)
):
    """Mark an invoice as paid."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status == "PAID":
        raise HTTPException(status_code=400, detail="Invoice already paid")

    if invoice.status in ["CANCELLED", "WRITTEN_OFF"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot mark {invoice.status} invoice as paid"
        )

    # Update invoice
    updated = await db.invoice.update(
        where={"id": invoice_id},
        data={
            "status": "PAID",
            "paidAt": datetime.utcnow(),
            "paymentMethod": payment.payment_method,
            "paymentReference": payment.payment_reference,
        }
    )

    # TODO: Trigger update-cash-metrics job
    print(f"Invoice {invoice.invoiceNumber} marked as paid - metrics update triggered")

    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "status": "PAID",
        "paid_at": updated.paidAt,
        "message": "Invoice marked as paid",
    }


@router.post("/{invoice_id}/cancel")
async def cancel_invoice(invoice_id: str, db=Depends(get_prisma)):
    """Cancel an invoice."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status == "PAID":
        raise HTTPException(status_code=400, detail="Cannot cancel paid invoice")

    updated = await db.invoice.update(
        where={"id": invoice_id},
        data={"status": "CANCELLED"}
    )

    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "status": "CANCELLED",
        "message": "Invoice cancelled",
    }


@router.post("/{invoice_id}/write-off")
async def write_off_invoice(invoice_id: str, db=Depends(get_prisma)):
    """Write off an invoice as uncollectable."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status == "PAID":
        raise HTTPException(status_code=400, detail="Cannot write off paid invoice")

    updated = await db.invoice.update(
        where={"id": invoice_id},
        data={"status": "WRITTEN_OFF"}
    )

    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "status": "WRITTEN_OFF",
        "message": "Invoice written off",
    }


class SendReminderRequest(BaseModel):
    reminder_type: int = 1  # 1, 2, or 3 (final)


@router.post("/{invoice_id}/send-reminder")
async def send_invoice_reminder(
    invoice_id: str,
    request: SendReminderRequest,
    db=Depends(get_prisma)
):
    """Manually trigger a payment reminder for an invoice."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status == "PAID":
        raise HTTPException(status_code=400, detail="Cannot send reminder for paid invoice")

    if invoice.status == "CANCELLED" or invoice.status == "WRITTEN_OFF":
        raise HTTPException(status_code=400, detail="Cannot send reminder for cancelled/written-off invoice")

    # Convert reminder_type to the expected format
    reminder_type = "final" if request.reminder_type == 3 else request.reminder_type

    # Return task queued response
    # In production, this would trigger the Trigger.dev job
    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "reminder_type": request.reminder_type,
        "message": f"Reminder {request.reminder_type} queued for sending",
        "queued": True,
    }


@router.get("/overdue")
async def list_overdue_invoices(
    client_id: str = Query(...),
    db=Depends(get_prisma)
):
    """List all overdue invoices for a client."""
    from datetime import datetime

    now = datetime.now()

    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "status": {"in": ["SENT", "REMINDED", "OVERDUE"]},
            "dueDate": {"lt": now},
        },
        order={"dueDate": "asc"},
    )

    return {
        "invoices": [invoice_to_response(inv) for inv in invoices],
        "total": len(invoices),
    }


# =============================================================================
# CASH METRICS ROUTES
# =============================================================================

@router.get("/clients/{client_id}/cash-metrics")
async def get_cash_metrics(client_id: str, db=Depends(get_prisma)):
    """Get cash flow metrics for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    metrics = await db.clientcashmetrics.find_unique(
        where={"clientId": client_id}
    )

    if not metrics:
        # Return default metrics if none exist
        return {
            "client_id": client_id,
            "total_outstanding": 0,
            "total_overdue": 0,
            "collected_this_month": 0,
            "collected_last_month": 0,
            "average_dso": 0,
            "updated_at": None,
        }

    return {
        "client_id": client_id,
        "total_outstanding": float(metrics.totalOutstanding),
        "total_overdue": float(metrics.totalOverdue),
        "collected_this_month": float(metrics.collectedThisMonth),
        "collected_last_month": float(metrics.collectedLastMonth),
        "average_dso": metrics.averageDSO,
        "updated_at": metrics.updatedAt,
    }


@router.put("/clients/{client_id}/cash-metrics")
async def update_cash_metrics(
    client_id: str,
    metrics: CashMetricsUpdate,
    db=Depends(get_prisma)
):
    """Update cash flow metrics for a client (called by scheduled job)."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Upsert metrics
    updated = await db.clientcashmetrics.upsert(
        where={"clientId": client_id},
        data={
            "create": {
                "clientId": client_id,
                "totalOutstanding": Decimal(str(metrics.total_outstanding)),
                "totalOverdue": Decimal(str(metrics.total_overdue)),
                "collectedThisMonth": Decimal(str(metrics.collected_this_month)),
                "collectedLastMonth": Decimal(str(metrics.collected_last_month)),
                "averageDSO": metrics.average_dso,
            },
            "update": {
                "totalOutstanding": Decimal(str(metrics.total_outstanding)),
                "totalOverdue": Decimal(str(metrics.total_overdue)),
                "collectedThisMonth": Decimal(str(metrics.collected_this_month)),
                "collectedLastMonth": Decimal(str(metrics.collected_last_month)),
                "averageDSO": metrics.average_dso,
            }
        }
    )

    return {
        "client_id": client_id,
        "message": "Metrics updated",
        "updated_at": updated.updatedAt,
    }


# =============================================================================
# JOB INVOICE CREATION
# =============================================================================

@router.post("/jobs/{job_id}/create-invoice")
async def create_invoice_from_job(job_id: str, db=Depends(get_prisma)):
    """Create an invoice pre-filled from job data."""
    # Get job with customer
    job = await db.job.find_unique(
        where={"id": job_id},
        include={"customer": True, "client": True}
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if not job.customer:
        raise HTTPException(status_code=400, detail="Job has no customer")

    # Check if invoice already exists for this job
    existing = await db.invoice.find_unique(where={"jobId": job_id})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Invoice {existing.invoiceNumber} already exists for this job"
        )

    # Generate invoice number
    invoice_number = await generate_invoice_number(db, job.clientId)

    # Determine amount (use final if available, otherwise quoted)
    amount = job.finalAmount or job.quotedAmount
    if not amount:
        raise HTTPException(
            status_code=400,
            detail="Job has no quoted or final amount"
        )

    # Create invoice
    invoice = await db.invoice.create(
        data={
            "clientId": job.clientId,
            "jobId": job.id,
            "customerName": job.customer.name,
            "customerEmail": job.customer.email or "",
            "customerPhone": job.customer.phone,
            "invoiceNumber": invoice_number,
            "amount": amount,
            "description": job.title or job.description or "Services rendered",
            "dueDate": datetime.utcnow(),  # Due immediately by default
            "status": "DRAFT",
        }
    )

    return {
        "id": invoice.id,
        "invoice_number": invoice_number,
        "message": "Invoice created from job",
        "job_id": job_id,
        **invoice_to_response(invoice)
    }


# =============================================================================
# PDF GENERATION (Phase 1)
# =============================================================================

@router.post("/{invoice_id}/generate-pdf")
async def generate_pdf(
    invoice_id: str,
    regenerate: bool = Query(False, description="Force regenerate even if PDF exists"),
    db=Depends(get_prisma)
):
    """Generate PDF for an invoice (triggers background job)."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # If PDF already exists and not regenerating, return existing
    if invoice.pdfUrl and not regenerate:
        return {
            "id": invoice_id,
            "invoice_number": invoice.invoiceNumber,
            "pdf_url": invoice.pdfUrl,
            "pdf_generated_at": invoice.pdfGeneratedAt,
            "message": "PDF already exists",
            "queued": False,
        }

    # TODO: Trigger generate-invoice-pdf job via Trigger.dev
    # For now, just return that it's queued
    print(f"PDF generation queued for invoice {invoice.invoiceNumber}")

    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "message": "PDF generation queued",
        "queued": True,
    }


@router.get("/{invoice_id}/pdf")
async def get_pdf_url(invoice_id: str, db=Depends(get_prisma)):
    """Get the PDF URL for an invoice."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if not invoice.pdfUrl:
        raise HTTPException(status_code=404, detail="PDF not yet generated")

    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "pdf_url": invoice.pdfUrl,
        "pdf_generated_at": invoice.pdfGeneratedAt,
    }


# =============================================================================
# PUBLIC INVOICE VIEW (No Auth Required)
# =============================================================================

@router.get("/view/{view_token}")
async def get_invoice_by_token(view_token: str, db=Depends(get_prisma)):
    """Get invoice details by view token (public, no auth required)."""
    invoice = await db.invoice.find_unique(
        where={"viewToken": view_token},
        include={"client": True}
    )

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Return public-safe invoice data
    return {
        "invoice_number": invoice.invoiceNumber,
        "business_name": invoice.client.businessName,
        "business_logo_url": invoice.client.logoUrl,
        "business_address": invoice.client.address,
        "business_phone": invoice.client.phone,
        "business_email": invoice.client.email,
        "customer_name": invoice.customerName,
        "amount": float(invoice.amount),
        "description": invoice.description,
        "due_date": invoice.dueDate,
        "status": invoice.status,
        "payment_link_url": invoice.paymentLinkUrl,
        "pdf_url": invoice.pdfUrl,
        # Bank details for manual payment
        "bank_account_name": invoice.client.bankAccountName,
        "bank_sort_code": invoice.client.bankSortCode,
        "bank_account_number": invoice.client.bankAccountNumber,
        "payment_terms": invoice.client.invoiceTerms,
    }
