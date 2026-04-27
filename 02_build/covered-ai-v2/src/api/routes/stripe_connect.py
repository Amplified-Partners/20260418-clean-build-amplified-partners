"""
Stripe Connect Routes - Stripe Connect integration for accepting payments
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import os

from src.db.client import get_prisma

# Import Stripe - optional to prevent errors if not installed
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

router = APIRouter()

# Configure Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

if STRIPE_AVAILABLE and STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


class CreateAccountResponse(BaseModel):
    account_id: str
    onboarding_url: str


def check_stripe_configured():
    """Verify Stripe is configured."""
    if not STRIPE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Stripe SDK not installed. Run: pip install stripe"
        )
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe not configured. Set STRIPE_SECRET_KEY environment variable."
        )


# =============================================================================
# STRIPE CONNECT ACCOUNT MANAGEMENT
# =============================================================================

@router.post("/create-account")
async def create_stripe_account(client_id: str, db=Depends(get_prisma)):
    """Create a new Stripe Connect Express account for a client."""
    check_stripe_configured()

    # Check if account already exists
    existing = await db.stripeaccount.find_unique(where={"clientId": client_id})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Stripe account already exists: {existing.stripeAccountId}"
        )

    # Get client info
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    try:
        # Create Stripe Connect Express account
        account = stripe.Account.create(
            type="express",
            country="GB",
            email=client.email,
            business_type="individual",
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },
            business_profile={
                "name": client.businessName,
                "product_description": f"{client.vertical} services",
            },
        )

        # Create onboarding link
        account_link = stripe.AccountLink.create(
            account=account.id,
            refresh_url=f"{os.getenv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000')}/settings/payments?refresh=true",
            return_url=f"{os.getenv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000')}/settings/payments?success=true",
            type="account_onboarding",
        )

        # Save to database
        stripe_account = await db.stripeaccount.create(
            data={
                "clientId": client_id,
                "stripeAccountId": account.id,
                "email": client.email,
                "businessType": "individual",
                "country": "GB",
                "chargesEnabled": False,
                "payoutsEnabled": False,
                "onboardingComplete": False,
            }
        )

        return {
            "account_id": account.id,
            "onboarding_url": account_link.url,
            "message": "Stripe account created",
        }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/onboarding-link")
async def get_onboarding_link(client_id: str, db=Depends(get_prisma)):
    """Get or refresh the Stripe onboarding link."""
    check_stripe_configured()

    stripe_account = await db.stripeaccount.find_unique(where={"clientId": client_id})
    if not stripe_account:
        raise HTTPException(status_code=404, detail="No Stripe account found")

    if stripe_account.onboardingComplete:
        raise HTTPException(
            status_code=400,
            detail="Onboarding already complete"
        )

    try:
        account_link = stripe.AccountLink.create(
            account=stripe_account.stripeAccountId,
            refresh_url=f"{os.getenv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000')}/settings/payments?refresh=true",
            return_url=f"{os.getenv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000')}/settings/payments?success=true",
            type="account_onboarding",
        )

        return {
            "account_id": stripe_account.stripeAccountId,
            "onboarding_url": account_link.url,
        }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status")
async def get_stripe_status(client_id: str, db=Depends(get_prisma)):
    """Check Stripe Connect account status."""
    check_stripe_configured()

    stripe_account = await db.stripeaccount.find_unique(where={"clientId": client_id})
    if not stripe_account:
        return {
            "connected": False,
            "account_id": None,
            "charges_enabled": False,
            "payouts_enabled": False,
            "onboarding_complete": False,
        }

    try:
        # Fetch latest status from Stripe
        account = stripe.Account.retrieve(stripe_account.stripeAccountId)

        # Update database if status changed
        if (account.charges_enabled != stripe_account.chargesEnabled or
            account.payouts_enabled != stripe_account.payoutsEnabled or
            account.details_submitted != stripe_account.onboardingComplete):

            stripe_account = await db.stripeaccount.update(
                where={"clientId": client_id},
                data={
                    "chargesEnabled": account.charges_enabled,
                    "payoutsEnabled": account.payouts_enabled,
                    "onboardingComplete": account.details_submitted,
                }
            )

        return {
            "connected": True,
            "account_id": stripe_account.stripeAccountId,
            "charges_enabled": account.charges_enabled,
            "payouts_enabled": account.payouts_enabled,
            "onboarding_complete": account.details_submitted,
            "business_type": stripe_account.businessType,
        }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/dashboard-link")
async def get_dashboard_link(client_id: str, db=Depends(get_prisma)):
    """Get link to Stripe Express dashboard."""
    check_stripe_configured()

    stripe_account = await db.stripeaccount.find_unique(where={"clientId": client_id})
    if not stripe_account:
        raise HTTPException(status_code=404, detail="No Stripe account found")

    try:
        login_link = stripe.Account.create_login_link(stripe_account.stripeAccountId)

        return {
            "dashboard_url": login_link.url,
        }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("")
async def disconnect_stripe(client_id: str, db=Depends(get_prisma)):
    """Disconnect Stripe account (soft delete)."""
    stripe_account = await db.stripeaccount.find_unique(where={"clientId": client_id})
    if not stripe_account:
        raise HTTPException(status_code=404, detail="No Stripe account found")

    # Delete from database (Stripe account remains on Stripe)
    await db.stripeaccount.delete(where={"clientId": client_id})

    return {
        "message": "Stripe account disconnected",
        "account_id": stripe_account.stripeAccountId,
    }


# =============================================================================
# PAYMENT LINKS FOR INVOICES
# =============================================================================

@router.post("/invoices/{invoice_id}/create-payment-link")
async def create_payment_link(invoice_id: str, db=Depends(get_prisma)):
    """Create a Stripe Payment Link for an invoice."""
    check_stripe_configured()

    # Get invoice with client
    invoice = await db.invoice.find_unique(
        where={"id": invoice_id},
        include={"client": True}
    )

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.paymentLinkUrl:
        return {
            "id": invoice_id,
            "payment_link_url": invoice.paymentLinkUrl,
            "payment_link_id": invoice.paymentLinkId,
            "message": "Payment link already exists",
        }

    # Get client's Stripe account
    stripe_account = await db.stripeaccount.find_unique(
        where={"clientId": invoice.clientId}
    )

    if not stripe_account:
        raise HTTPException(
            status_code=400,
            detail="Client has no Stripe account connected"
        )

    if not stripe_account.chargesEnabled:
        raise HTTPException(
            status_code=400,
            detail="Stripe account not fully onboarded"
        )

    try:
        # Create a product for this invoice
        product = stripe.Product.create(
            name=f"Invoice {invoice.invoiceNumber}",
            description=invoice.description[:500] if invoice.description else "Invoice payment",
            metadata={
                "invoice_id": invoice.id,
                "invoice_number": invoice.invoiceNumber,
                "client_id": invoice.clientId,
            },
        )

        # Create a price (amount in pence)
        amount_pence = int(float(invoice.amount) * 100)
        price = stripe.Price.create(
            product=product.id,
            unit_amount=amount_pence,
            currency="gbp",
        )

        # Create payment link with connected account as destination
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            after_completion={
                "type": "redirect",
                "redirect": {
                    "url": f"{os.getenv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000')}/invoices/payment-success?invoice={invoice.id}"
                }
            },
            application_fee_percent=2.9,  # Platform fee
            transfer_data={
                "destination": stripe_account.stripeAccountId,
            },
            metadata={
                "invoice_id": invoice.id,
                "invoice_number": invoice.invoiceNumber,
                "client_id": invoice.clientId,
            },
        )

        # Update invoice with payment link
        await db.invoice.update(
            where={"id": invoice_id},
            data={
                "paymentLinkUrl": payment_link.url,
                "paymentLinkId": payment_link.id,
            }
        )

        return {
            "id": invoice_id,
            "payment_link_url": payment_link.url,
            "payment_link_id": payment_link.id,
            "message": "Payment link created",
        }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoices/{invoice_id}/payment-status")
async def get_payment_status(invoice_id: str, db=Depends(get_prisma)):
    """Check payment status for an invoice."""
    invoice = await db.invoice.find_unique(where={"id": invoice_id})

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return {
        "id": invoice_id,
        "invoice_number": invoice.invoiceNumber,
        "status": invoice.status,
        "payment_link_url": invoice.paymentLinkUrl,
        "stripe_payment_intent_id": invoice.stripePaymentIntentId,
        "stripe_charge_id": invoice.stripeChargeId,
        "paid_at": invoice.paidAt,
        "paid_amount": float(invoice.paidAmount) if invoice.paidAmount else None,
    }
