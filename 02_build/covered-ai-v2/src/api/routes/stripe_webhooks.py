"""
Stripe Webhooks - Handle Stripe webhook events for payments
"""
from fastapi import APIRouter, HTTPException, Request, Header
from datetime import datetime, timezone
from decimal import Decimal
import os
import json

from src.db.client import get_prisma
from prisma import Json

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


@router.post("/stripe")
async def handle_stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature")
):
    """
    Handle Stripe webhook events.

    Handles:
    - checkout.session.completed: Payment completed via Payment Link
    - payment_intent.succeeded: Direct payment successful
    - payment_intent.payment_failed: Payment failed
    - account.updated: Connected account status changed
    """
    if not STRIPE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Stripe SDK not available")

    # Get raw body for signature verification
    payload = await request.body()

    # Verify webhook signature
    if STRIPE_WEBHOOK_SECRET and stripe_signature:
        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        # In development, parse without verification
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = event.get("type") if isinstance(event, dict) else event.type
    event_data = event.get("data", {}).get("object", {}) if isinstance(event, dict) else event.data.object
    event_id = event.get("id") if isinstance(event, dict) else event.id

    db = await get_prisma()

    try:
        # Handle different event types
        if event_type == "checkout.session.completed":
            await handle_checkout_completed(db, event_data, event_id)

        elif event_type == "payment_intent.succeeded":
            await handle_payment_succeeded(db, event_data, event_id)

        elif event_type == "payment_intent.payment_failed":
            await handle_payment_failed(db, event_data, event_id)

        elif event_type == "account.updated":
            await handle_account_updated(db, event_data)

        else:
            # Log unhandled events
            print(f"Unhandled Stripe event: {event_type}")

        return {"status": "ok", "event_type": event_type}

    except Exception as e:
        print(f"Error processing Stripe webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_checkout_completed(db, session, event_id):
    """Handle checkout.session.completed event - Payment Link payment completed."""
    # Get invoice ID from metadata
    metadata = session.get("metadata", {})
    invoice_id = metadata.get("invoice_id")

    if not invoice_id:
        print(f"Checkout completed without invoice_id: {session.get('id')}")
        return

    # Get invoice
    invoice = await db.invoice.find_unique(where={"id": invoice_id})
    if not invoice:
        print(f"Invoice not found: {invoice_id}")
        return

    if invoice.status == "PAID":
        print(f"Invoice already paid: {invoice_id}")
        return

    # Get payment intent for details
    payment_intent_id = session.get("payment_intent")
    amount_total = session.get("amount_total", 0) / 100  # Convert from pence

    # Update invoice as paid
    await db.invoice.update(
        where={"id": invoice_id},
        data={
            "status": "PAID",
            "paidAt": datetime.now(timezone.utc),
            "paidAmount": Decimal(str(amount_total)),
            "paymentMethod": "stripe",
            "stripePaymentIntentId": payment_intent_id,
        }
    )

    # Log payment event
    await db.paymentevent.create(
        data={
            "invoiceId": invoice_id,
            "eventType": "checkout.session.completed",
            "stripeEventId": event_id,
            "eventData": Json(dict(session)),
            "amount": Decimal(str(amount_total)),
            "currency": session.get("currency", "gbp"),
            "status": "succeeded",
        }
    )

    # Log autonomous action
    await db.autonomousaction.create(
        data={
            "clientId": invoice.clientId,
            "actionType": "PAYMENT_RECORDED",
            "description": f"Payment received for invoice {invoice.invoiceNumber} via Stripe (£{amount_total:.2f})",
            "triggerId": invoice_id,
            "triggerType": "stripe_webhook",
            "triggerReason": "Customer completed Stripe checkout",
            "decision": "record_payment",
            "confidence": 1.0,
            "outcome": "SUCCESS",
            "outcomeDetails": f"Payment intent: {payment_intent_id}",
            "outcomeAt": datetime.now(timezone.utc),
        }
    )

    print(f"Invoice {invoice.invoiceNumber} marked as paid via Stripe")


async def handle_payment_succeeded(db, payment_intent, event_id):
    """Handle payment_intent.succeeded event."""
    # Get invoice ID from metadata
    metadata = payment_intent.get("metadata", {})
    invoice_id = metadata.get("invoice_id")

    if not invoice_id:
        # This might be a payment not linked to an invoice
        print(f"Payment succeeded without invoice_id: {payment_intent.get('id')}")
        return

    invoice = await db.invoice.find_unique(where={"id": invoice_id})
    if not invoice:
        print(f"Invoice not found: {invoice_id}")
        return

    if invoice.status == "PAID":
        # Already processed, just log the event
        await db.paymentevent.create(
            data={
                "invoiceId": invoice_id,
                "eventType": "payment_intent.succeeded",
                "stripeEventId": event_id,
                "eventData": Json(dict(payment_intent)),
                "amount": Decimal(str(payment_intent.get("amount", 0) / 100)),
                "currency": payment_intent.get("currency", "gbp"),
                "status": "succeeded",
            }
        )
        return

    # Update invoice
    amount = payment_intent.get("amount", 0) / 100
    charge_id = payment_intent.get("latest_charge")

    await db.invoice.update(
        where={"id": invoice_id},
        data={
            "status": "PAID",
            "paidAt": datetime.now(timezone.utc),
            "paidAmount": Decimal(str(amount)),
            "paymentMethod": "stripe",
            "stripePaymentIntentId": payment_intent.get("id"),
            "stripeChargeId": charge_id,
        }
    )

    # Log payment event
    await db.paymentevent.create(
        data={
            "invoiceId": invoice_id,
            "eventType": "payment_intent.succeeded",
            "stripeEventId": event_id,
            "eventData": Json(dict(payment_intent)),
            "amount": Decimal(str(amount)),
            "currency": payment_intent.get("currency", "gbp"),
            "status": "succeeded",
        }
    )

    print(f"Invoice {invoice.invoiceNumber} payment succeeded")


async def handle_payment_failed(db, payment_intent, event_id):
    """Handle payment_intent.payment_failed event."""
    metadata = payment_intent.get("metadata", {})
    invoice_id = metadata.get("invoice_id")

    if not invoice_id:
        return

    invoice = await db.invoice.find_unique(where={"id": invoice_id})
    if not invoice:
        return

    # Log failed payment event
    await db.paymentevent.create(
        data={
            "invoiceId": invoice_id,
            "eventType": "payment_intent.payment_failed",
            "stripeEventId": event_id,
            "eventData": Json(dict(payment_intent)),
            "amount": Decimal(str(payment_intent.get("amount", 0) / 100)),
            "currency": payment_intent.get("currency", "gbp"),
            "status": "failed",
        }
    )

    # Log notification
    await db.notification.create(
        data={
            "clientId": invoice.clientId,
            "type": "payment_failed",
            "channel": "email",
            "recipient": invoice.customerEmail,
            "subject": f"Payment failed for invoice {invoice.invoiceNumber}",
            "message": f"Payment attempt failed for invoice {invoice.invoiceNumber}",
            "status": "sent",
            "sentAt": datetime.now(timezone.utc),
        }
    )

    print(f"Payment failed for invoice {invoice.invoiceNumber}")


async def handle_account_updated(db, account):
    """Handle account.updated event - Connected account status changed."""
    account_id = account.get("id")

    stripe_account = await db.stripeaccount.find_unique(
        where={"stripeAccountId": account_id}
    )

    if not stripe_account:
        print(f"Stripe account not found in database: {account_id}")
        return

    # Update account status
    await db.stripeaccount.update(
        where={"stripeAccountId": account_id},
        data={
            "chargesEnabled": account.get("charges_enabled", False),
            "payoutsEnabled": account.get("payouts_enabled", False),
            "onboardingComplete": account.get("details_submitted", False),
        }
    )

    print(f"Stripe account {account_id} status updated")
