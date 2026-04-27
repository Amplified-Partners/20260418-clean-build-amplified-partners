"""
Xero Sync Routes - Sync invoices to Xero
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
import os
import base64
import httpx

from src.db.client import get_prisma

router = APIRouter()

XERO_API_URL = "https://api.xero.com/api.xro/2.0"


def decrypt_token(encrypted: str) -> str:
    """Decrypt stored token."""
    return base64.b64decode(encrypted.encode()).decode()


class SyncInvoiceResponse(BaseModel):
    invoice_id: str
    invoice_number: str
    xero_invoice_id: Optional[str] = None
    success: bool
    error: Optional[str] = None


async def get_valid_access_token(db, client_id: str) -> tuple[str, str]:
    """Get valid access token, refreshing if necessary."""
    connection = await db.xeroconnection.find_unique(where={"clientId": client_id})

    if not connection:
        raise HTTPException(status_code=404, detail="No Xero connection found")

    if not connection.connected:
        raise HTTPException(status_code=400, detail="Xero not connected")

    # Check if token needs refresh (refresh if expiring in next 5 minutes)
    now = datetime.now(timezone.utc)
    if connection.tokenExpiresAt and connection.tokenExpiresAt.replace(tzinfo=timezone.utc) <= now:
        # Token expired, need to refresh
        raise HTTPException(
            status_code=401,
            detail="Xero token expired. Please reconnect."
        )

    return decrypt_token(connection.accessToken), connection.tenantId


async def create_xero_contact(
    access_token: str,
    tenant_id: str,
    name: str,
    email: str,
    phone: Optional[str] = None
) -> str:
    """Create or find a contact in Xero."""
    async with httpx.AsyncClient() as client:
        # First, try to find existing contact by name
        search_response = await client.get(
            f"{XERO_API_URL}/Contacts",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Xero-Tenant-Id": tenant_id,
                "Accept": "application/json",
            },
            params={"where": f'Name=="{name}"'},
        )

        if search_response.status_code == 200:
            contacts = search_response.json().get("Contacts", [])
            if contacts:
                return contacts[0]["ContactID"]

        # Create new contact
        contact_data = {
            "Contacts": [{
                "Name": name,
                "EmailAddress": email,
            }]
        }

        if phone:
            contact_data["Contacts"][0]["Phones"] = [{
                "PhoneType": "DEFAULT",
                "PhoneNumber": phone,
            }]

        create_response = await client.post(
            f"{XERO_API_URL}/Contacts",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Xero-Tenant-Id": tenant_id,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=contact_data,
        )

        if create_response.status_code not in [200, 201]:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to create Xero contact: {create_response.text}"
            )

        contacts = create_response.json().get("Contacts", [])
        if not contacts:
            raise HTTPException(status_code=400, detail="Failed to create Xero contact")

        return contacts[0]["ContactID"]


@router.post("/invoices/{invoice_id}/sync-to-xero")
async def sync_invoice_to_xero(invoice_id: str, db=Depends(get_prisma)):
    """Sync a single invoice to Xero."""
    # Get invoice with client
    invoice = await db.invoice.find_unique(
        where={"id": invoice_id},
        include={"client": True},
    )

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Check if already synced
    if invoice.xeroInvoiceId:
        return SyncInvoiceResponse(
            invoice_id=invoice_id,
            invoice_number=invoice.invoiceNumber,
            xero_invoice_id=invoice.xeroInvoiceId,
            success=True,
            error="Already synced to Xero",
        )

    # Get access token
    access_token, tenant_id = await get_valid_access_token(db, invoice.clientId)

    try:
        # Create or find contact
        contact_id = await create_xero_contact(
            access_token,
            tenant_id,
            invoice.customerName,
            invoice.customerEmail,
            invoice.customerPhone,
        )

        # Create invoice in Xero
        xero_invoice_data = {
            "Invoices": [{
                "Type": "ACCREC",  # Accounts Receivable
                "Contact": {"ContactID": contact_id},
                "LineItems": [{
                    "Description": invoice.description,
                    "Quantity": 1,
                    "UnitAmount": float(invoice.amount),
                    "AccountCode": "200",  # Sales account (configurable)
                }],
                "Date": invoice.createdAt.strftime("%Y-%m-%d") if invoice.createdAt else datetime.now().strftime("%Y-%m-%d"),
                "DueDate": invoice.dueDate.strftime("%Y-%m-%d") if invoice.dueDate else None,
                "Reference": invoice.invoiceNumber,
                "Status": "AUTHORISED",  # Ready to send
            }]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{XERO_API_URL}/Invoices",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Xero-Tenant-Id": tenant_id,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json=xero_invoice_data,
            )

            if response.status_code not in [200, 201]:
                error_msg = response.text
                await db.invoice.update(
                    where={"id": invoice_id},
                    data={"xeroSyncError": error_msg[:500]},
                )
                return SyncInvoiceResponse(
                    invoice_id=invoice_id,
                    invoice_number=invoice.invoiceNumber,
                    success=False,
                    error=f"Xero API error: {error_msg}",
                )

            xero_invoices = response.json().get("Invoices", [])
            if not xero_invoices:
                return SyncInvoiceResponse(
                    invoice_id=invoice_id,
                    invoice_number=invoice.invoiceNumber,
                    success=False,
                    error="Xero returned empty response",
                )

            xero_invoice_id = xero_invoices[0]["InvoiceID"]

        # Update invoice with Xero IDs
        await db.invoice.update(
            where={"id": invoice_id},
            data={
                "xeroInvoiceId": xero_invoice_id,
                "xeroContactId": contact_id,
                "xeroSyncedAt": datetime.now(timezone.utc),
                "xeroSyncError": None,
            },
        )

        # Update connection last sync
        await db.xeroconnection.update(
            where={"clientId": invoice.clientId},
            data={"lastSyncAt": datetime.now(timezone.utc), "lastSyncError": None},
        )

        return SyncInvoiceResponse(
            invoice_id=invoice_id,
            invoice_number=invoice.invoiceNumber,
            xero_invoice_id=xero_invoice_id,
            success=True,
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        await db.invoice.update(
            where={"id": invoice_id},
            data={"xeroSyncError": error_msg[:500]},
        )
        return SyncInvoiceResponse(
            invoice_id=invoice_id,
            invoice_number=invoice.invoiceNumber,
            success=False,
            error=error_msg,
        )


@router.post("/sync-all")
async def sync_all_invoices(client_id: str, db=Depends(get_prisma)):
    """Sync all unsynced invoices to Xero."""
    # Get connection to verify it exists
    connection = await db.xeroconnection.find_unique(where={"clientId": client_id})

    if not connection or not connection.connected:
        raise HTTPException(status_code=400, detail="Xero not connected")

    # Get unsynced invoices
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "xeroInvoiceId": None,
            "status": {"in": ["SENT", "REMINDED", "OVERDUE", "PAID"]},
        },
        order={"createdAt": "asc"},
    )

    results = []
    for invoice in invoices:
        try:
            result = await sync_invoice_to_xero(invoice.id, db)
            results.append(result)
        except Exception as e:
            results.append(SyncInvoiceResponse(
                invoice_id=invoice.id,
                invoice_number=invoice.invoiceNumber,
                success=False,
                error=str(e),
            ))

    succeeded = sum(1 for r in results if r.success)
    failed = len(results) - succeeded

    return {
        "total": len(results),
        "succeeded": succeeded,
        "failed": failed,
        "results": results,
    }
