"""
Xero OAuth Routes - Xero integration for accounting sync
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone, timedelta
from urllib.parse import urlencode
import os
import base64
import httpx
import secrets

from src.db.client import get_prisma

router = APIRouter()

# Xero OAuth configuration
XERO_CLIENT_ID = os.getenv("XERO_CLIENT_ID")
XERO_CLIENT_SECRET = os.getenv("XERO_CLIENT_SECRET")
XERO_REDIRECT_URI = os.getenv("XERO_REDIRECT_URI", "http://localhost:3000/api/xero/callback")
XERO_AUTH_URL = "https://login.xero.com/identity/connect/authorize"
XERO_TOKEN_URL = "https://identity.xero.com/connect/token"
XERO_CONNECTIONS_URL = "https://api.xero.com/connections"

# Scopes needed for invoice sync
XERO_SCOPES = "openid profile email accounting.transactions accounting.contacts offline_access"


def check_xero_configured():
    """Verify Xero is configured."""
    if not XERO_CLIENT_ID or not XERO_CLIENT_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Xero not configured. Set XERO_CLIENT_ID and XERO_CLIENT_SECRET."
        )


# Simple encryption for tokens (in production, use proper encryption lib)
def encrypt_token(token: str) -> str:
    """Encrypt token for storage."""
    # In production, use proper encryption with ENCRYPTION_KEY
    # For now, base64 encode (not secure, replace in production)
    return base64.b64encode(token.encode()).decode()


def decrypt_token(encrypted: str) -> str:
    """Decrypt stored token."""
    return base64.b64decode(encrypted.encode()).decode()


class XeroConnectionStatus(BaseModel):
    connected: bool
    tenant_id: Optional[str] = None
    tenant_name: Optional[str] = None
    last_sync_at: Optional[datetime] = None
    auto_sync_invoices: bool = True
    last_sync_error: Optional[str] = None


@router.get("/connect")
async def connect_xero(client_id: str = Query(...)):
    """
    Initiate Xero OAuth flow.
    Redirects to Xero for authorization.
    """
    check_xero_configured()

    # Generate state for CSRF protection
    state = f"{client_id}:{secrets.token_urlsafe(16)}"

    params = {
        "response_type": "code",
        "client_id": XERO_CLIENT_ID,
        "redirect_uri": XERO_REDIRECT_URI,
        "scope": XERO_SCOPES,
        "state": state,
    }

    auth_url = f"{XERO_AUTH_URL}?{urlencode(params)}"

    return {"redirect_url": auth_url, "state": state}


@router.get("/callback")
async def xero_callback(
    code: str = Query(...),
    state: str = Query(...),
    db=Depends(get_prisma)
):
    """
    Handle Xero OAuth callback.
    Exchange code for tokens and store connection.
    """
    check_xero_configured()

    # Parse client_id from state
    try:
        client_id, _ = state.split(":", 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid state")

    # Exchange code for tokens
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": XERO_REDIRECT_URI,
    }

    auth_header = base64.b64encode(
        f"{XERO_CLIENT_ID}:{XERO_CLIENT_SECRET}".encode()
    ).decode()

    async with httpx.AsyncClient() as client:
        # Get tokens
        token_response = await client.post(
            XERO_TOKEN_URL,
            data=token_data,
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get tokens: {token_response.text}"
            )

        tokens = token_response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        expires_in = tokens.get("expires_in", 1800)  # Default 30 minutes

        # Get connected tenants
        connections_response = await client.get(
            XERO_CONNECTIONS_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if connections_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail="Failed to get Xero connections"
            )

        connections = connections_response.json()

        if not connections:
            raise HTTPException(
                status_code=400,
                detail="No Xero organizations found"
            )

        # Use first tenant
        tenant = connections[0]
        tenant_id = tenant["tenantId"]
        tenant_name = tenant.get("tenantName", "Unknown")

    # Calculate token expiry
    token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    # Store connection (upsert)
    existing = await db.xeroconnection.find_unique(where={"clientId": client_id})

    if existing:
        await db.xeroconnection.update(
            where={"clientId": client_id},
            data={
                "tenantId": tenant_id,
                "tenantName": tenant_name,
                "accessToken": encrypt_token(access_token),
                "refreshToken": encrypt_token(refresh_token),
                "tokenExpiresAt": token_expires_at,
                "connected": True,
                "lastSyncError": None,
            }
        )
    else:
        await db.xeroconnection.create(
            data={
                "clientId": client_id,
                "tenantId": tenant_id,
                "tenantName": tenant_name,
                "accessToken": encrypt_token(access_token),
                "refreshToken": encrypt_token(refresh_token),
                "tokenExpiresAt": token_expires_at,
                "connected": True,
            }
        )

    # Redirect to settings page with success
    app_url = os.getenv("NEXT_PUBLIC_APP_URL", "http://localhost:3000")
    return RedirectResponse(f"{app_url}/settings/accounting?success=true")


@router.get("/status")
async def get_xero_status(client_id: str = Query(...), db=Depends(get_prisma)):
    """Get Xero connection status."""
    connection = await db.xeroconnection.find_unique(where={"clientId": client_id})

    if not connection:
        return XeroConnectionStatus(connected=False)

    return XeroConnectionStatus(
        connected=connection.connected,
        tenant_id=connection.tenantId,
        tenant_name=connection.tenantName,
        last_sync_at=connection.lastSyncAt,
        auto_sync_invoices=connection.autoSyncInvoices,
        last_sync_error=connection.lastSyncError,
    )


@router.delete("")
async def disconnect_xero(client_id: str = Query(...), db=Depends(get_prisma)):
    """Disconnect Xero integration."""
    connection = await db.xeroconnection.find_unique(where={"clientId": client_id})

    if not connection:
        raise HTTPException(status_code=404, detail="No Xero connection found")

    await db.xeroconnection.delete(where={"clientId": client_id})

    return {"message": "Xero disconnected", "tenant_name": connection.tenantName}


class ToggleAutoSyncRequest(BaseModel):
    auto_sync: bool


@router.patch("/auto-sync")
async def toggle_auto_sync(
    client_id: str,
    request: ToggleAutoSyncRequest,
    db=Depends(get_prisma)
):
    """Toggle auto-sync for invoices."""
    connection = await db.xeroconnection.find_unique(where={"clientId": client_id})

    if not connection:
        raise HTTPException(status_code=404, detail="No Xero connection found")

    updated = await db.xeroconnection.update(
        where={"clientId": client_id},
        data={"autoSyncInvoices": request.auto_sync}
    )

    return {
        "client_id": client_id,
        "auto_sync_invoices": updated.autoSyncInvoices,
    }
