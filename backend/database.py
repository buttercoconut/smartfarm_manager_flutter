"""Database connection and session utilities.

We use SQLAlchemy 2.0's async API with `asyncpg` as the driver.  The
`get_session` function is a context‑manager that yields an async
`AsyncSession` which can be used with `async with`.

The `Base` class is the declarative base for all ORM models.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from .config import settings

# Create the async engine.  The connection string is expected to be a
# PostgreSQL URL with the asyncpg driver.
engine = create_async_engine(settings["database_url"], echo=False, future=True)

# Create a session factory.  `expire_on_commit=False` keeps objects alive
# after a commit which is handy for API responses.
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base class for ORM models.
Base = declarative_base()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an async database session.

    Usage:
        async with get_session() as session:
            await session.execute(...)
    """
    async with async_session_factory() as session:
        yield session

# Utility to create all tables.  Call this at startup.
async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Utility to drop all tables – useful for tests.
async def drop_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
