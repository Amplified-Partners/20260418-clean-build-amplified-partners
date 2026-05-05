---
title: "Module 11: Referral & Affiliate System"
id: "11-referral-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 11: Referral & Affiliate System

## Overview
Track referrals, pay commissions, and manage the four referral programs:
1. Customer → Customer (£50 each)
2. Rep → Practice (£50)
3. Staff → Boss (£50)
4. Influencer → Followers (£100)

## Expert Panel Input

**Viral Growth Expert**: Make sharing dead simple. One-click share links. Pre-written messages. Track everything.

**Commission Expert**: Pay fast. Within 7 days of the referred customer's first payment. Trust builds advocates.

**Fraud Prevention**: Validate referrals. Same IP? Same payment method? Flag for review.

---

## Features

### 1. Referral Tracking
- Unique referral codes per referrer
- Cookie-based attribution (30 days)
- UTM parameter tracking
- Multi-touch attribution

### 2. Commission Management
- Automatic commission calculation
- Approval workflow
- Payout via Stripe Connect or bank transfer
- Tax documentation

### 3. Referrer Dashboard
- Track referrals and earnings
- Share links and copy
- Payout history

---

## Files to Create

### 1. src/services/referrals/engine.py

```python
"""
Referral & Affiliate Engine

Manages all referral programs and commission tracking.
"""

import os
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid
import hashlib

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")


class ReferralProgram(str, Enum):
    CUSTOMER = "customer"  # Customer → Customer £50 each
    REP = "rep"  # Sales rep → Practice £50
    STAFF = "staff"  # Staff → Boss £50
    INFLUENCER = "influencer"  # Influencer → Followers £100


class ReferralStatus(str, Enum):
    PENDING = "pending"  # Signed up, not yet paid
    QUALIFIED = "qualified"  # First payment received
    APPROVED = "approved"  # Commission approved
    PAID = "paid"  # Commission paid out
    REJECTED = "rejected"  # Fraud or invalid


class CommissionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass
class Referrer:
    id: str
    program: ReferralProgram
    name: str
    email: str
    phone: Optional[str]
    referral_code: str
    referral_link: str
    total_referrals: int = 0
    qualified_referrals: int = 0
    total_earned: float = 0.0
    total_paid: float = 0.0
    stripe_connect_id: Optional[str] = None
    bank_details: Optional[Dict] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Referral:
    id: str
    referrer_id: str
    program: ReferralProgram
    referred_client_id: Optional[str]
    referred_name: str
    referred_email: str
    referred_phone: Optional[str]
    status: ReferralStatus
    commission_amount: float
    ip_address: Optional[str]
    user_agent: Optional[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    qualified_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None


@dataclass
class Commission:
    id: str
    referrer_id: str
    referral_id: str
    amount: float
    status: CommissionStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    payout_reference: Optional[str] = None


# Commission amounts by program
COMMISSION_AMOUNTS = {
    ReferralProgram.CUSTOMER: 50.0,  # £50 each (referrer and referee)
    ReferralProgram.REP: 50.0,  # £50 per practice
    ReferralProgram.STAFF: 50.0,  # £50 for staff member
    ReferralProgram.INFLUENCER: 100.0,  # £100 per signup
}


class ReferralEngine:
    """
    Manages referral tracking and commission payouts.
    """
    
    def __init__(self):
        self.referrers: Dict[str, Referrer] = {}
        self.referrals: Dict[str, Referral] = {}
        self.commissions: Dict[str, Commission] = {}
    
    def generate_referral_code(self, name: str) -> str:
        """Generate a unique, memorable referral code."""
        # Create code from name + random suffix
        base = name.lower().replace(" ", "")[:6]
        suffix = uuid.uuid4().hex[:4].upper()
        return f"{base}{suffix}"
    
    async def create_referrer(
        self,
        program: ReferralProgram,
        name: str,
        email: str,
        phone: Optional[str] = None,
    ) -> Referrer:
        """Create a new referrer."""
        referral_code = self.generate_referral_code(name)
        
        referrer = Referrer(
            id=str(uuid.uuid4()),
            program=program,
            name=name,
            email=email,
            phone=phone,
            referral_code=referral_code,
            referral_link=f"https://covered.ai/r/{referral_code}",
        )
        
        self.referrers[referrer.id] = referrer
        return referrer
    
    async def get_referrer_by_code(self, code: str) -> Optional[Referrer]:
        """Find referrer by their referral code."""
        for referrer in self.referrers.values():
            if referrer.referral_code.lower() == code.lower():
                return referrer
        return None
    
    async def track_referral(
        self,
        referral_code: str,
        referred_name: str,
        referred_email: str,
        referred_phone: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        utm_source: Optional[str] = None,
        utm_medium: Optional[str] = None,
        utm_campaign: Optional[str] = None,
    ) -> Optional[Referral]:
        """Track a new referral signup."""
        referrer = await self.get_referrer_by_code(referral_code)
        if not referrer:
            return None
        
        # Check for fraud signals
        fraud_score = self._calculate_fraud_score(
            referrer, referred_email, ip_address
        )
        
        commission = COMMISSION_AMOUNTS[referrer.program]
        
        referral = Referral(
            id=str(uuid.uuid4()),
            referrer_id=referrer.id,
            program=referrer.program,
            referred_client_id=None,
            referred_name=referred_name,
            referred_email=referred_email,
            referred_phone=referred_phone,
            status=ReferralStatus.PENDING,
            commission_amount=commission,
            ip_address=ip_address,
            user_agent=user_agent,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
        )
        
        self.referrals[referral.id] = referral
        referrer.total_referrals += 1
        
        return referral
    
    def _calculate_fraud_score(
        self,
        referrer: Referrer,
        referred_email: str,
        ip_address: Optional[str],
    ) -> float:
        """Calculate fraud probability (0-1)."""
        score = 0.0
        
        # Same email domain as referrer?
        if referrer.email.split("@")[1] == referred_email.split("@")[1]:
            score += 0.3
        
        # Check for IP reuse among referrer's referrals
        if ip_address:
            ip_reuse = sum(
                1 for r in self.referrals.values()
                if r.referrer_id == referrer.id and r.ip_address == ip_address
            )
            if ip_reuse > 2:
                score += 0.4
        
        # High volume from same referrer in short time
        recent_referrals = sum(
            1 for r in self.referrals.values()
            if r.referrer_id == referrer.id
            and r.created_at > datetime.utcnow() - timedelta(hours=24)
        )
        if recent_referrals > 5:
            score += 0.2
        
        return min(score, 1.0)
    
    async def qualify_referral(
        self,
        referral_id: str,
        client_id: str,
    ) -> Optional[Commission]:
        """
        Mark referral as qualified (customer made first payment).
        Creates commission record.
        """
        referral = self.referrals.get(referral_id)
        if not referral:
            return None
        
        referral.status = ReferralStatus.QUALIFIED
        referral.qualified_at = datetime.utcnow()
        referral.referred_client_id = client_id
        
        # Create commission
        commission = Commission(
            id=str(uuid.uuid4()),
            referrer_id=referral.referrer_id,
            referral_id=referral.id,
            amount=referral.commission_amount,
            status=CommissionStatus.PENDING,
        )
        
        self.commissions[commission.id] = commission
        
        # Update referrer stats
        referrer = self.referrers.get(referral.referrer_id)
        if referrer:
            referrer.qualified_referrals += 1
            referrer.total_earned += commission.amount
        
        # For customer referrals, also credit the new customer
        if referral.program == ReferralProgram.CUSTOMER:
            # TODO: Apply credit to new customer's account
            pass
        
        return commission
    
    async def approve_commission(self, commission_id: str) -> bool:
        """Approve a commission for payout."""
        commission = self.commissions.get(commission_id)
        if not commission or commission.status != CommissionStatus.PENDING:
            return False
        
        commission.status = CommissionStatus.APPROVED
        commission.approved_at = datetime.utcnow()
        
        referral = self.referrals.get(commission.referral_id)
        if referral:
            referral.status = ReferralStatus.APPROVED
        
        return True
    
    async def process_payout(self, commission_id: str) -> Optional[str]:
        """Process commission payout via Stripe."""
        commission = self.commissions.get(commission_id)
        if not commission or commission.status != CommissionStatus.APPROVED:
            return None
        
        referrer = self.referrers.get(commission.referrer_id)
        if not referrer:
            return None
        
        # Payout via Stripe Connect if connected
        if referrer.stripe_connect_id:
            payout_ref = await self._stripe_payout(
                referrer.stripe_connect_id,
                commission.amount,
            )
        else:
            # Manual bank transfer
            payout_ref = f"MANUAL-{uuid.uuid4().hex[:8].upper()}"
        
        commission.status = CommissionStatus.PAID
        commission.paid_at = datetime.utcnow()
        commission.payout_reference = payout_ref
        
        referrer.total_paid += commission.amount
        
        referral = self.referrals.get(commission.referral_id)
        if referral:
            referral.status = ReferralStatus.PAID
            referral.paid_at = datetime.utcnow()
        
        return payout_ref
    
    async def _stripe_payout(self, connect_id: str, amount: float) -> str:
        """Process payout via Stripe Connect."""
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        
        transfer = stripe.Transfer.create(
            amount=int(amount * 100),  # Pence
            currency="gbp",
            destination=connect_id,
        )
        
        return transfer.id
    
    async def get_referrer_dashboard(self, referrer_id: str) -> Dict[str, Any]:
        """Get dashboard data for a referrer."""
        referrer = self.referrers.get(referrer_id)
        if not referrer:
            return {}
        
        referrals = [
            r for r in self.referrals.values()
            if r.referrer_id == referrer_id
        ]
        
        commissions = [
            c for c in self.commissions.values()
            if c.referrer_id == referrer_id
        ]
        
        return {
            "referrer": {
                "name": referrer.name,
                "referral_code": referrer.referral_code,
                "referral_link": referrer.referral_link,
            },
            "stats": {
                "total_referrals": referrer.total_referrals,
                "qualified_referrals": referrer.qualified_referrals,
                "conversion_rate": (
                    referrer.qualified_referrals / referrer.total_referrals * 100
                    if referrer.total_referrals > 0 else 0
                ),
                "total_earned": referrer.total_earned,
                "total_paid": referrer.total_paid,
                "pending_payout": referrer.total_earned - referrer.total_paid,
            },
            "referrals": [
                {
                    "name": r.referred_name,
                    "status": r.status.value,
                    "commission": r.commission_amount,
                    "created_at": r.created_at.isoformat(),
                }
                for r in sorted(referrals, key=lambda x: x.created_at, reverse=True)[:20]
            ],
            "commissions": [
                {
                    "amount": c.amount,
                    "status": c.status.value,
                    "created_at": c.created_at.isoformat(),
                    "paid_at": c.paid_at.isoformat() if c.paid_at else None,
                }
                for c in sorted(commissions, key=lambda x: x.created_at, reverse=True)[:20]
            ],
        }
    
    def get_share_messages(self, referrer: Referrer) -> Dict[str, str]:
        """Get pre-written share messages for different channels."""
        return {
            "sms": f"Hey! I've been using Covered AI for my business - never miss a call now. "
                   f"Use my link and we both get £50: {referrer.referral_link}",
            "email_subject": "Stop missing calls - this changed my business",
            "email_body": f"""Hi,

I wanted to share something that's made a real difference to my business.

It's called Covered - an AI receptionist that answers all my calls 24/7. 
No more missed jobs, no more voicemails that never get returned.

If you sign up using my link, we both get £50 off:
{referrer.referral_link}

Worth checking out!""",
            "whatsapp": f"🔥 Found this great AI phone answering service for businesses. "
                        f"Never miss a call again! Use my link and we both get £50: {referrer.referral_link}",
            "twitter": f"Never miss a business call again 📞 @CoveredAI answers 24/7. "
                       f"Get £50 off: {referrer.referral_link}",
            "facebook": f"Game changer for my business! Covered AI answers all my calls, "
                        f"even at 3am. Use my link for £50 off: {referrer.referral_link}",
        }


# Singleton
referral_engine = ReferralEngine()
```

### 2. src/api/routes/referrals.py

```python
"""
Referral System API Routes
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.services.referrals.engine import (
    referral_engine,
    ReferralProgram,
)

router = APIRouter(prefix="/referrals", tags=["referrals"])


class CreateReferrerInput(BaseModel):
    program: str
    name: str
    email: str
    phone: Optional[str] = None


class TrackReferralInput(BaseModel):
    referral_code: str
    name: str
    email: str
    phone: Optional[str] = None


@router.post("/referrers")
async def create_referrer(input: CreateReferrerInput):
    """Create a new referrer."""
    try:
        program = ReferralProgram(input.program)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid program")
    
    referrer = await referral_engine.create_referrer(
        program=program,
        name=input.name,
        email=input.email,
        phone=input.phone,
    )
    
    return {
        "id": referrer.id,
        "referral_code": referrer.referral_code,
        "referral_link": referrer.referral_link,
    }


@router.get("/referrers/{referrer_id}/dashboard")
async def get_referrer_dashboard(referrer_id: str):
    """Get referrer dashboard data."""
    data = await referral_engine.get_referrer_dashboard(referrer_id)
    if not data:
        raise HTTPException(status_code=404, detail="Referrer not found")
    return data


@router.get("/referrers/{referrer_id}/share-messages")
async def get_share_messages(referrer_id: str):
    """Get pre-written share messages."""
    referrer = referral_engine.referrers.get(referrer_id)
    if not referrer:
        raise HTTPException(status_code=404, detail="Referrer not found")
    return referral_engine.get_share_messages(referrer)


@router.post("/track")
async def track_referral(input: TrackReferralInput, request: Request):
    """Track a referral signup."""
    referral = await referral_engine.track_referral(
        referral_code=input.referral_code,
        referred_name=input.name,
        referred_email=input.email,
        referred_phone=input.phone,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    if not referral:
        raise HTTPException(status_code=404, detail="Invalid referral code")
    
    return {
        "referral_id": referral.id,
        "status": referral.status.value,
    }


@router.post("/qualify/{referral_id}")
async def qualify_referral(referral_id: str, client_id: str):
    """Mark referral as qualified (first payment received)."""
    commission = await referral_engine.qualify_referral(referral_id, client_id)
    
    if not commission:
        raise HTTPException(status_code=404, detail="Referral not found")
    
    return {
        "commission_id": commission.id,
        "amount": commission.amount,
        "status": commission.status.value,
    }


@router.post("/commissions/{commission_id}/approve")
async def approve_commission(commission_id: str):
    """Approve a commission for payout."""
    success = await referral_engine.approve_commission(commission_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Cannot approve commission")
    
    return {"status": "approved"}


@router.post("/commissions/{commission_id}/payout")
async def process_payout(commission_id: str):
    """Process commission payout."""
    payout_ref = await referral_engine.process_payout(commission_id)
    
    if not payout_ref:
        raise HTTPException(status_code=400, detail="Cannot process payout")
    
    return {"payout_reference": payout_ref}


@router.get("/lookup/{code}")
async def lookup_referral_code(code: str):
    """Look up a referral code (for landing page)."""
    referrer = await referral_engine.get_referrer_by_code(code)
    
    if not referrer:
        raise HTTPException(status_code=404, detail="Invalid code")
    
    return {
        "valid": True,
        "referrer_name": referrer.name.split()[0],  # First name only
        "program": referrer.program.value,
    }


@router.get("/programs")
async def list_programs():
    """List available referral programs."""
    return {
        "programs": [
            {
                "id": "customer",
                "name": "Customer Referral",
                "commission": "£50 each (you and your friend)",
                "description": "Refer a friend, you both get £50 off",
            },
            {
                "id": "rep",
                "name": "Sales Rep",
                "commission": "£50 per signup",
                "description": "Earn £50 for every business you bring in",
            },
            {
                "id": "staff",
                "name": "Staff Referral",
                "commission": "£50",
                "description": "Tell your boss about Covered, get £50",
            },
            {
                "id": "influencer",
                "name": "Influencer",
                "commission": "£100 per signup",
                "description": "Share with your audience, earn £100 per signup",
            },
        ]
    }
```

### 3. Referral Landing Page

```tsx
// frontend/src/app/(marketing)/r/[code]/page.tsx
import { notFound, redirect } from "next/navigation";

async function getReferrer(code: string) {
  const res = await fetch(`${process.env.API_URL}/api/v1/referrals/lookup/${code}`);
  if (!res.ok) return null;
  return res.json();
}

export default async function ReferralLandingPage({ 
  params 
}: { 
  params: { code: string } 
}) {
  const referrer = await getReferrer(params.code);
  
  if (!referrer) {
    redirect("/");
  }
  
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-20">
      <div className="max-w-2xl mx-auto px-4 text-center">
        <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full inline-block mb-6">
          🎉 {referrer.referrer_name} sent you here!
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Get £50 off Covered AI
        </h1>
        
        <p className="text-xl text-gray-600 mb-8">
          Your friend {referrer.referrer_name} thinks you'd love Covered - 
          the AI receptionist that never misses a call.
        </p>
        
        <a 
          href={`/signup?ref=${params.code}`}
          className="inline-flex items-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700"
        >
          Claim Your £50 Off
        </a>
        
        <p className="mt-4 text-gray-500">
          {referrer.referrer_name} will also get £50 when you sign up
        </p>
      </div>
    </main>
  );
}
```
