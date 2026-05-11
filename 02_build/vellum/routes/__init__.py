"""FastAPI router setup for Vellum Brief mode."""

from fastapi import APIRouter

from vellum.routes.brief import router as brief_router
from vellum.routes.webhook import router as webhook_router

router = APIRouter()
router.include_router(brief_router)
router.include_router(webhook_router)

__all__ = ["router"]
