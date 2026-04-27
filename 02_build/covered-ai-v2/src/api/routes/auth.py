"""
Auth Routes - User authentication (magic link + password)
"""
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel, EmailStr

from src.db.client import get_prisma

router = APIRouter()

# Config
MAGIC_LINK_EXPIRY_MINUTES = 15
SESSION_EXPIRY_DAYS = 30
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class SignupRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: Optional[str] = None  # Optional for magic link signup


class LoginRequest(BaseModel):
    email: EmailStr
    password: Optional[str] = None  # Null for magic link


class MagicLinkVerifyRequest(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class SessionResponse(BaseModel):
    token: str
    user_id: str
    email: str
    name: Optional[str]
    client_id: Optional[str]
    onboarding_complete: bool
    expires_at: datetime


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    import hashlib
    # Simple hash for now - in production use bcrypt
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == hashed


async def get_current_user(request: Request, db=Depends(get_prisma)):
    """Get current user from session token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.replace("Bearer ", "")

    session = await db.session.find_unique(
        where={"token": token},
        include={"user": True}
    )

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session.expiresAt < datetime.now(timezone.utc):
        await db.session.delete(where={"id": session.id})
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user


# =============================================================================
# SIGNUP
# =============================================================================

@router.post("/signup")
async def signup(request: SignupRequest, db=Depends(get_prisma)):
    """
    Create a new user account.

    If password provided: Create account and return session
    If no password: Send magic link email
    """
    # Check if user exists
    existing = await db.user.find_unique(where={"email": request.email})
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered. Please login."
        )

    # Create user
    user_data = {
        "email": request.email,
        "name": request.name,
    }

    if request.password:
        # Password signup
        user_data["passwordHash"] = hash_password(request.password)
        user_data["emailVerified"] = False

        user = await db.user.create(data=user_data)

        # Create session
        session_token = generate_token()
        session = await db.session.create(
            data={
                "userId": user.id,
                "token": session_token,
                "expiresAt": datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRY_DAYS),
            }
        )

        # Create onboarding session
        await db.onboardingsession.create(
            data={
                "userId": user.id,
                "currentStep": "started",
            }
        )

        return {
            "token": session.token,
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "client_id": None,
            "onboarding_complete": False,
            "expires_at": session.expiresAt,
        }
    else:
        # Magic link signup
        magic_token = generate_token()

        user = await db.user.create(
            data={
                **user_data,
                "magicLinkToken": magic_token,
                "magicLinkExpiry": datetime.now(timezone.utc) + timedelta(minutes=MAGIC_LINK_EXPIRY_MINUTES),
            }
        )

        # TODO: Send magic link email via Resend
        magic_link = f"{FRONTEND_URL}/auth/verify?token={magic_token}"
        print(f"Magic link for {request.email}: {magic_link}")

        return {
            "message": "Check your email for a login link",
            "email": request.email,
        }


# =============================================================================
# LOGIN
# =============================================================================

@router.post("/login")
async def login(request: LoginRequest, db=Depends(get_prisma)):
    """
    Login with email/password or request magic link.
    """
    user = await db.user.find_unique(where={"email": request.email})

    if request.password:
        # Password login
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not user.passwordHash:
            raise HTTPException(
                status_code=400,
                detail="This account uses magic link login. Check your email."
            )

        if not verify_password(request.password, user.passwordHash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Create session
        session_token = generate_token()
        session = await db.session.create(
            data={
                "userId": user.id,
                "token": session_token,
                "expiresAt": datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRY_DAYS),
            }
        )

        # Update last login
        await db.user.update(
            where={"id": user.id},
            data={"lastLoginAt": datetime.now(timezone.utc)}
        )

        # Check onboarding status
        onboarding = await db.onboardingsession.find_unique(where={"userId": user.id})
        onboarding_complete = onboarding and onboarding.currentStep == "completed" if onboarding else False

        return {
            "token": session.token,
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "client_id": user.clientId,
            "onboarding_complete": onboarding_complete,
            "expires_at": session.expiresAt,
        }
    else:
        # Magic link login
        if not user:
            # Create new user with magic link
            magic_token = generate_token()
            user = await db.user.create(
                data={
                    "email": request.email,
                    "magicLinkToken": magic_token,
                    "magicLinkExpiry": datetime.now(timezone.utc) + timedelta(minutes=MAGIC_LINK_EXPIRY_MINUTES),
                }
            )
        else:
            # Update magic link token
            magic_token = generate_token()
            await db.user.update(
                where={"id": user.id},
                data={
                    "magicLinkToken": magic_token,
                    "magicLinkExpiry": datetime.now(timezone.utc) + timedelta(minutes=MAGIC_LINK_EXPIRY_MINUTES),
                }
            )

        # TODO: Send magic link email via Resend
        magic_link = f"{FRONTEND_URL}/auth/verify?token={magic_token}"
        print(f"Magic link for {request.email}: {magic_link}")

        return {
            "message": "Check your email for a login link",
            "email": request.email,
        }


# =============================================================================
# MAGIC LINK VERIFICATION
# =============================================================================

@router.post("/verify-magic-link")
async def verify_magic_link(request: MagicLinkVerifyRequest, db=Depends(get_prisma)):
    """
    Verify magic link token and create session.
    """
    user = await db.user.find_first(
        where={
            "magicLinkToken": request.token,
            "magicLinkExpiry": {"gt": datetime.now(timezone.utc)},
        }
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired link")

    # Clear magic link and verify email
    await db.user.update(
        where={"id": user.id},
        data={
            "magicLinkToken": None,
            "magicLinkExpiry": None,
            "emailVerified": True,
            "emailVerifiedAt": datetime.now(timezone.utc),
            "lastLoginAt": datetime.now(timezone.utc),
        }
    )

    # Create session
    session_token = generate_token()
    session = await db.session.create(
        data={
            "userId": user.id,
            "token": session_token,
            "expiresAt": datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRY_DAYS),
        }
    )

    # Ensure onboarding session exists
    onboarding = await db.onboardingsession.find_unique(where={"userId": user.id})
    if not onboarding:
        await db.onboardingsession.create(
            data={
                "userId": user.id,
                "currentStep": "started",
            }
        )
        onboarding_complete = False
    else:
        onboarding_complete = onboarding.currentStep == "completed"

    return {
        "token": session.token,
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "client_id": user.clientId,
        "onboarding_complete": onboarding_complete,
        "expires_at": session.expiresAt,
    }


# =============================================================================
# SESSION MANAGEMENT
# =============================================================================

@router.get("/me")
async def get_me(user=Depends(get_current_user), db=Depends(get_prisma)):
    """Get current user profile."""
    onboarding = await db.onboardingsession.find_unique(where={"userId": user.id})

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "email_verified": user.emailVerified,
        "client_id": user.clientId,
        "onboarding_step": onboarding.currentStep if onboarding else None,
        "onboarding_complete": onboarding and onboarding.currentStep == "completed" if onboarding else False,
        "created_at": user.createdAt,
    }


@router.post("/logout")
async def logout(request: Request, db=Depends(get_prisma)):
    """Logout and invalidate session."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        await db.session.delete_many(where={"token": token})

    return {"message": "Logged out"}


@router.delete("/sessions")
async def delete_all_sessions(user=Depends(get_current_user), db=Depends(get_prisma)):
    """Logout from all devices."""
    await db.session.delete_many(where={"userId": user.id})
    return {"message": "All sessions invalidated"}


# =============================================================================
# PASSWORD RESET
# =============================================================================

@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db=Depends(get_prisma)):
    """Request password reset email."""
    user = await db.user.find_unique(where={"email": request.email})

    # Always return success to prevent email enumeration
    if user and user.passwordHash:
        reset_token = generate_token()
        await db.user.update(
            where={"id": user.id},
            data={
                "resetToken": reset_token,
                "resetTokenExpiry": datetime.now(timezone.utc) + timedelta(hours=1),
            }
        )

        # TODO: Send reset email via Resend
        reset_link = f"{FRONTEND_URL}/auth/reset-password?token={reset_token}"
        print(f"Password reset link for {request.email}: {reset_link}")

    return {"message": "If that email exists, we've sent a password reset link"}


@router.post("/reset-password")
async def reset_password(request: PasswordResetConfirm, db=Depends(get_prisma)):
    """Reset password with token."""
    user = await db.user.find_first(
        where={
            "resetToken": request.token,
            "resetTokenExpiry": {"gt": datetime.now(timezone.utc)},
        }
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")

    # Update password and clear token
    await db.user.update(
        where={"id": user.id},
        data={
            "passwordHash": hash_password(request.new_password),
            "resetToken": None,
            "resetTokenExpiry": None,
        }
    )

    # Invalidate all sessions
    await db.session.delete_many(where={"userId": user.id})

    return {"message": "Password updated. Please login."}
