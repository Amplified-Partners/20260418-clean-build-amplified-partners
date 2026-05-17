"""Vellum storage — protocol + backend selection.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from vellum.models.entry import SheetEntry
from vellum.models.sheet import Sheet, SheetMeta
from vellum.models.token import ShareToken


@runtime_checkable
class SheetStore(Protocol):

    async def create_sheet(self, meta: SheetMeta) -> Sheet: ...
    async def get_sheet(self, sheet_id: str) -> Sheet | None: ...
    async def list_sheets(self, tenant_id: str) -> list[Sheet]: ...
    async def append_entry(self, sheet_id: str, entry: SheetEntry) -> None: ...
    async def store_token(self, token: ShareToken) -> None: ...
    async def get_token(self, token_id: str) -> ShareToken | None: ...
    async def close(self) -> None: ...
    async def get_decisions(self, tenant_id: str) -> list[SheetEntry]: ...
    async def get_unread(self, tenant_id: str) -> list[SheetEntry]: ...


_store: SheetStore | None = None


def get_store() -> SheetStore:
    if _store is None:
        raise RuntimeError("Store not initialised — call init_store() first")
    return _store


def set_store(store: SheetStore) -> None:
    global _store  # noqa: PLW0603
    _store = store


async def init_store() -> SheetStore:
    from vellum.storage.memory import MemorySheetStore
    store = MemorySheetStore()
    set_store(store)
    return store
