"""
Quote Public Routes - No authentication required
Public endpoints for quote viewing and acceptance
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.db.client import get_prisma

router = APIRouter()


# =============================================================================
# MODELS
# =============================================================================

class QuoteLineItem(BaseModel):
    """Line item in a quote"""
    description: str
    quantity: int
    unitPrice: float
    amount: float


class QuotePublicView(BaseModel):
    """Public quote view response"""
    id: str
    quoteNumber: str
    title: str
    description: Optional[str]
    status: str

    # Customer details
    customerName: str
    customerAddress: Optional[str]

    # Business details
    businessName: str
    businessLogoUrl: Optional[str]
    businessPhone: Optional[str]
    businessEmail: Optional[str]

    # Line items
    lineItems: list[QuoteLineItem]

    # Totals
    subtotal: float
    vatRate: float
    vatAmount: float
    total: float

    # Dates
    validUntil: str
    createdAt: str

    # State
    isExpired: bool
    canAccept: bool
    canReject: bool

    # PDF
    pdfUrl: Optional[str]

    # Terms
    quoteTerms: Optional[str]


class QuoteResponseRequest(BaseModel):
    """Request to accept or reject a quote"""
    action: str  # "accept" or "reject"
    rejectionReason: Optional[str] = None


class QuoteResponseResult(BaseModel):
    """Result of accepting or rejecting a quote"""
    success: bool
    message: str
    status: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/view/{token}", response_model=QuotePublicView)
async def get_quote_by_token(token: str):
    """
    Get quote details for public viewing
    No authentication required - token provides access
    """
    prisma = get_prisma()

    # Find quote by view token
    quote = await prisma.quote.find_unique(
        where={"viewToken": token},
        include={"client": True}
    )

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )

    # Mark as viewed if first time
    if not quote.viewedAt:
        await prisma.quote.update(
            where={"id": quote.id},
            data={
                "viewedAt": datetime.utcnow(),
                "status": "VIEWED" if quote.status == "SENT" else quote.status
            }
        )

    # Check if expired
    is_expired = quote.validUntil < datetime.utcnow()

    # Update status to EXPIRED if needed
    if is_expired and quote.status not in ["ACCEPTED", "REJECTED", "CONVERTED", "EXPIRED"]:
        await prisma.quote.update(
            where={"id": quote.id},
            data={"status": "EXPIRED"}
        )

    # Determine if customer can accept or reject
    can_accept = quote.status in ["DRAFT", "SENT", "VIEWED"] and not is_expired
    can_reject = quote.status in ["DRAFT", "SENT", "VIEWED"] and not is_expired

    # Parse line items
    line_items = []
    if quote.lineItems:
        try:
            raw_items = quote.lineItems if isinstance(quote.lineItems, list) else []
            for item in raw_items:
                line_items.append(QuoteLineItem(
                    description=item.get("description", ""),
                    quantity=item.get("quantity", 1),
                    unitPrice=float(item.get("unitPrice", 0)),
                    amount=float(item.get("amount") or item.get("total") or (item.get("quantity", 1) * item.get("unitPrice", 0)))
                ))
        except Exception:
            # Fallback to single item
            line_items = [QuoteLineItem(
                description=quote.title,
                quantity=1,
                unitPrice=float(quote.subtotal),
                amount=float(quote.subtotal)
            )]

    return QuotePublicView(
        id=quote.id,
        quoteNumber=quote.quoteNumber,
        title=quote.title,
        description=quote.description,
        status=quote.status,
        customerName=quote.customerName,
        customerAddress=quote.customerAddress,
        businessName=quote.client.businessName,
        businessLogoUrl=quote.client.logoUrl,
        businessPhone=quote.client.phone,
        businessEmail=quote.client.email,
        lineItems=line_items,
        subtotal=float(quote.subtotal),
        vatRate=float(quote.vatRate),
        vatAmount=float(quote.vatAmount),
        total=float(quote.total),
        validUntil=quote.validUntil.isoformat(),
        createdAt=quote.createdAt.isoformat(),
        isExpired=is_expired,
        canAccept=can_accept,
        canReject=can_reject,
        pdfUrl=quote.pdfUrl,
        quoteTerms=quote.client.quoteTerms
    )


@router.post("/view/{token}/respond", response_model=QuoteResponseResult)
async def respond_to_quote(token: str, request: QuoteResponseRequest):
    """
    Accept or reject a quote
    No authentication required - token provides access
    """
    prisma = get_prisma()

    # Find quote by view token
    quote = await prisma.quote.find_unique(
        where={"viewToken": token},
        include={"client": True}
    )

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )

    # Check if already responded
    if quote.status in ["ACCEPTED", "REJECTED", "CONVERTED"]:
        return QuoteResponseResult(
            success=False,
            message=f"Quote has already been {quote.status.lower()}",
            status=quote.status
        )

    # Check if expired
    if quote.validUntil < datetime.utcnow():
        return QuoteResponseResult(
            success=False,
            message="Quote has expired and cannot be accepted",
            status="EXPIRED"
        )

    # Validate action
    if request.action not in ["accept", "reject"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be 'accept' or 'reject'"
        )

    # Process the response
    now = datetime.utcnow()

    if request.action == "accept":
        await prisma.quote.update(
            where={"id": quote.id},
            data={
                "status": "ACCEPTED",
                "acceptedAt": now
            }
        )

        # Log notification
        await prisma.notification.create(
            data={
                "clientId": quote.clientId,
                "type": "quote_accepted",
                "channel": "email",
                "recipient": quote.client.email,
                "subject": f"Quote {quote.quoteNumber} accepted!",
                "message": f"{quote.customerName} has accepted your quote for £{float(quote.total):.2f}",
                "status": "pending"
            }
        )

        # Log autonomous action
        await prisma.autonomousAction.create(
            data={
                "clientId": quote.clientId,
                "actionType": "QUOTE_GENERATED",
                "description": f"Quote {quote.quoteNumber} accepted by {quote.customerName}",
                "triggerId": quote.id,
                "triggerType": "quote",
                "triggerReason": "Customer clicked Accept button",
                "decision": "record_acceptance",
                "confidence": 1.0,
                "outcome": "SUCCESS",
                "outcomeDetails": f"Quote accepted, ready to convert to job",
                "outcomeAt": now
            }
        )

        return QuoteResponseResult(
            success=True,
            message="Quote accepted successfully! We will be in touch shortly to schedule the work.",
            status="ACCEPTED"
        )

    else:  # reject
        await prisma.quote.update(
            where={"id": quote.id},
            data={
                "status": "REJECTED",
                "rejectedAt": now,
                "rejectionReason": request.rejectionReason
            }
        )

        # Log notification
        await prisma.notification.create(
            data={
                "clientId": quote.clientId,
                "type": "quote_rejected",
                "channel": "email",
                "recipient": quote.client.email,
                "subject": f"Quote {quote.quoteNumber} rejected",
                "message": f"{quote.customerName} has rejected your quote" + (f": {request.rejectionReason}" if request.rejectionReason else ""),
                "status": "pending"
            }
        )

        return QuoteResponseResult(
            success=True,
            message="Quote declined. Thank you for letting us know.",
            status="REJECTED"
        )


@router.get("/view/{token}/pdf")
async def get_quote_pdf(token: str):
    """
    Redirect to quote PDF
    """
    prisma = get_prisma()

    quote = await prisma.quote.find_unique(
        where={"viewToken": token}
    )

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )

    if not quote.pdfUrl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote PDF not yet generated"
        )

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=quote.pdfUrl)
