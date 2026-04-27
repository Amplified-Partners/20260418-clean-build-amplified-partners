"""
Amplified CRM - Main Application

FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import interview, contacts, companies, deals, activities, orchestrator, telegram_bridge, calendar_routes, intelligence_routes, stripe_routes, retell_integration  # xero_routes, quickbooks_routes disabled
from app.api import marketing_live as marketing  # Live database version
from app.api.auth import APIKeyMiddleware
# Temporarily disabled voice_bridge due to deepgram SDK compatibility issue
# from app.api.routes import voice_bridge
from app.database import init_db, close_db
from app.orchestrator import start_orchestrator_worker, stop_orchestrator_worker
from app.content.router import router as content_router
from app.content.waitlist import router as waitlist_router
from app.content.scheduler import start_content_scheduler, stop_content_scheduler
from app.content.telegram_gate import start_review_bot, stop_review_bot
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    await init_db()
    await start_orchestrator_worker()
    start_content_scheduler()
    await start_review_bot()
    yield
    # Shutdown
    await stop_review_bot()
    stop_content_scheduler()
    await stop_orchestrator_worker()
    await close_db()


app = FastAPI(
    title="Amplified CRM",
    description="AI-powered SMB consultancy platform",
    version="1.0.0",
    lifespan=lifespan,
)

# API key auth (X-API-Key header) — whitelists /, /health, /docs, /openapi.json, /redoc
app.add_middleware(APIKeyMiddleware)

# CORS middleware for frontend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-API-Key"],
)

# Include routers
app.include_router(orchestrator.router, prefix="/api/orchestrator", tags=["Orchestrator"])
app.include_router(telegram_bridge.router, tags=["Telegram"])  # No prefix - already in router
# app.include_router(voice_bridge.router, tags=["Voice Bridge"])  # Temporarily disabled for testing
app.include_router(calendar_routes.router, tags=["Calendar"])  # No prefix - already in router (/calendar)
# app.include_router(xero_routes.router, tags=["Xero"])  # Temporarily disabled - Python 3.13 compatibility
# app.include_router(quickbooks_routes.router, tags=["QuickBooks"])  # Temporarily disabled - import issue
app.include_router(intelligence_routes.router, tags=["Intelligence"])  # No prefix - already in router (/intelligence)
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
app.include_router(deals.router, prefix="/api/deals", tags=["Deals"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
app.include_router(marketing.router, tags=["Marketing"])  # Marketing Machine
app.include_router(stripe_routes.router, tags=["Stripe"])  # Stripe payment integration
app.include_router(retell_integration.router, tags=["Retell AI"])  # Voice AI platform
app.include_router(content_router, tags=["Content Engine"])  # Gary Vee atomisation pipeline
app.include_router(waitlist_router, tags=["Waitlist"])       # Covered AI pre-launch waiting list


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "Amplified CRM",
        "status": "running",
        "version": "1.0.0",
        "message": "The interview IS the product",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
