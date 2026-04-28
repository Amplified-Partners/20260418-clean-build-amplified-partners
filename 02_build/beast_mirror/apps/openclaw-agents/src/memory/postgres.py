"""
PostgreSQL Checkpointing & Long-Term Store
===========================================
Why AsyncConnectionPool and not create_async_engine:
  - LangGraph checkpoint-postgres expects raw psycopg connections
  - autocommit=True is mandatory — LangGraph manages its own transactions
  - dict_row factory so LangGraph can access columns by name
  - application_name lets us identify openclaw connections in pg_stat_activity

Two separate pools: one for the checkpointer (conversation state),
one for the store (long-term cross-conversation memory).
"""

from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

from config import settings


def _pool_kwargs(pool_name: str) -> dict:
    """Common connection kwargs. application_name shows up in pg_stat_activity."""
    return {
        "autocommit": True,
        "row_factory": dict_row,
        "application_name": f"openclaw-{pool_name}",
    }


@asynccontextmanager
async def get_postgres_saver():
    """Yields an AsyncPostgresSaver for conversation checkpointing."""
    async with AsyncConnectionPool(
        settings.postgres_dsn,
        min_size=settings.POSTGRES_MIN_CONNECTIONS,
        max_size=settings.POSTGRES_MAX_CONNECTIONS,
        kwargs=_pool_kwargs("checkpointer"),
        check=AsyncConnectionPool.check_connection,
    ) as pool:
        saver = AsyncPostgresSaver(pool)
        await saver.setup()
        yield saver


@asynccontextmanager
async def get_postgres_store():
    """Yields an AsyncPostgresStore for long-term cross-conversation memory."""
    async with AsyncConnectionPool(
        settings.postgres_dsn,
        min_size=1,
        max_size=settings.POSTGRES_MAX_CONNECTIONS // 2,
        kwargs=_pool_kwargs("store"),
        check=AsyncConnectionPool.check_connection,
    ) as pool:
        store = AsyncPostgresStore(pool)
        await store.setup()
        yield store
