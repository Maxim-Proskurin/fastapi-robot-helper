from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine # noqa: F501
from sqlalchemy.orm import declarative_base
from src.app.core.config import settings

DATABASE_URL = settings.DATABASE_URL


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables.")

if DATABASE_URL.startswith("postgresql+psycopg2://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace(
        "postgresql+psycopg2://", "postgresql+asyncpg://"
    )
else:
    ASYNC_DATABASE_URL = DATABASE_URL

engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
