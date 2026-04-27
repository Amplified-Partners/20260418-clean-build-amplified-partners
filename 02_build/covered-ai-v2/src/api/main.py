"""
Covered AI v2 - FastAPI Main Application
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Import database client
from src.db.client import connect, disconnect


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print("Covered AI v2 starting...")
    await connect()
    yield
    await disconnect()
    print("Covered AI v2 shutting down...")


app = FastAPI(
    title="Covered AI",
    description="AI phone answering system for UK service businesses",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from src.api.routes import (
    clients,
    leads,
    jobs,
    webhooks,
    invoices,
    unit_economics,
    dashboard,
    auth,
    onboarding,
    actions,
    customers,
    quotes,
    calls,
    reviews,
    settings,
    geo,
    training,
    stripe_connect,
    stripe_webhooks,
    xero,
    xero_sync,
    reports,
    quote_public,
    porting,
    nurture,
    demo_numbers,
    outreach,
    events,
    provisioning,
    website_builder,
    photo_studio,
)

# Auth routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(onboarding.router, prefix="/api/v1/onboarding", tags=["onboarding"])

# Core routes
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(clients.router, prefix="/api/v1/clients", tags=["clients"])
app.include_router(leads.router, prefix="/api/v1/clients/{client_id}/leads", tags=["leads"])
app.include_router(jobs.router, prefix="/api/v1/clients/{client_id}/jobs", tags=["jobs"])
app.include_router(customers.router, prefix="/api/v1/clients/{client_id}/customers", tags=["customers"])
app.include_router(quotes.router, prefix="/api/v1/clients/{client_id}/quotes", tags=["quotes"])
app.include_router(calls.router, prefix="/api/v1/clients/{client_id}/calls", tags=["calls"])
app.include_router(reviews.router, prefix="/api/v1/clients/{client_id}/reviews", tags=["reviews"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["settings"])
app.include_router(invoices.router, prefix="/api/v1/invoices", tags=["invoices"])
app.include_router(unit_economics.router, prefix="/api/v1/unit-economics", tags=["unit-economics"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(actions.router, prefix="/api/v1/actions", tags=["actions"])
app.include_router(geo.router, prefix="/api/v1/clients/{client_id}/geo", tags=["geo"])

# Training & Support routes
app.include_router(training.router, prefix="/api/v1/training", tags=["training"])

# Payment routes
app.include_router(stripe_connect.router, prefix="/api/v1/stripe", tags=["stripe"])
app.include_router(stripe_webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])

# Accounting routes (Xero)
app.include_router(xero.router, prefix="/api/v1/xero", tags=["xero"])
app.include_router(xero_sync.router, prefix="/api/v1/xero", tags=["xero"])

# Reports routes
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])

# Quote public routes (no auth required)
app.include_router(quote_public.router, prefix="/api/v1/quotes", tags=["quotes"])

# Porting routes
app.include_router(porting.router, prefix="/api/v1", tags=["porting"])

# Nurture sequence routes
app.include_router(nurture.router, prefix="/api/v1", tags=["nurture"])

# Demo numbers routes
app.include_router(demo_numbers.router, prefix="/api/v1/demo-numbers", tags=["demo-numbers"])

# Cold outreach routes
app.include_router(outreach.router, prefix="/api/v1/outreach", tags=["outreach"])

# Event log routes
app.include_router(events.router, prefix="/api/v1", tags=["events"])

# Provisioning routes
app.include_router(provisioning.router, prefix="/api/v1", tags=["provisioning"])

# Website builder routes
app.include_router(website_builder.router, prefix="/api/v1", tags=["website-builder"])

# Photo studio routes
app.include_router(photo_studio.router, prefix="/api/v1", tags=["photo-studio"])


@app.get("/")
async def root():
    return {"message": "Covered AI v2", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
