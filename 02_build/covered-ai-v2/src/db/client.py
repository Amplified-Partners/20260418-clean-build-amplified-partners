"""
Prisma Client Wrapper

Provides a singleton Prisma client for database access.
"""

from prisma import Prisma

# Singleton client instance
prisma = Prisma()


async def get_prisma() -> Prisma:
    """
    Get the Prisma client, connecting if necessary.
    Use this in FastAPI dependency injection.
    """
    if not prisma.is_connected():
        await prisma.connect()
    return prisma


async def connect():
    """Connect to the database."""
    if not prisma.is_connected():
        await prisma.connect()
        print("📀 Database connected")


async def disconnect():
    """Disconnect from the database."""
    if prisma.is_connected():
        await prisma.disconnect()
        print("📀 Database disconnected")
