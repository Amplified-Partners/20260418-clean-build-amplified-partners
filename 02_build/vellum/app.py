"""Vellum — contact surface application.

FastAPI app serving:
- REST API for sheets, entries, replies, decisions, read receipts
- Simple HTMX-powered UI for Ewan
- Scheduled morning/evening brief generation

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from vellum.cron.briefs import generate_evening_brief, generate_morning_brief
from vellum.routes import router
from vellum.storage import init_store

log = logging.getLogger("vellum")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

VELLUM_DIR = Path(__file__).parent


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    store = await init_store()
    log.info("Vellum store initialised")

    # Generate a demo morning brief on startup for dev
    sheet_id = await generate_morning_brief()
    log.info("Demo morning brief: %s", sheet_id)

    yield

    await store.close()
    log.info("Vellum store closed")


app = FastAPI(
    title="Vellum",
    description="Contact surface for Ewan and agents — Amplified Partners",
    version="0.1.0",
    lifespan=lifespan,
)

_STATIC_DIR = VELLUM_DIR / "static"
app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")
app.include_router(router)
