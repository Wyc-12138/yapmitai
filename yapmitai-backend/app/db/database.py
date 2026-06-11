from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings
from app.models import Base

settings = get_settings()
database_url = make_url(settings.database_url)

engine = create_async_engine(
    database_url,
    pool_pre_ping=True,
    poolclass=NullPool,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


async def ensure_mysql_database() -> None:
    if database_url.get_backend_name() != "mysql":
        return
    database_name = database_url.database
    if not database_name:
        raise RuntimeError("DATABASE_URL must include a MySQL database name")
    server_url = database_url.set(database=None)
    server_engine = create_async_engine(
        server_url,
        pool_pre_ping=True,
        poolclass=NullPool,
    )
    try:
        async with server_engine.begin() as connection:
            escaped_name = database_name.replace("`", "``")
            await connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{escaped_name}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
    finally:
        await server_engine.dispose()


async def init_database() -> None:
    from app.db.seed import seed_database

    await ensure_mysql_database()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_database(session)
