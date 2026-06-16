from collections.abc import AsyncIterator

from sqlalchemy import inspect, text
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


async def ensure_agent_schema() -> bool:
    if database_url.get_backend_name() != "mysql":
        return False
    upgraded = False
    async with engine.begin() as connection:
        rows = await connection.execute(
            text(
                "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'agents'"
            )
        )
        columns = {row[0] for row in rows}
        additions = {
            "code": "ALTER TABLE agents ADD COLUMN code VARCHAR(80) NULL",
            "name_en": "ALTER TABLE agents ADD COLUMN name_en VARCHAR(150) NULL",
            "description": "ALTER TABLE agents ADD COLUMN description TEXT NULL",
        }
        for name, statement in additions.items():
            if name not in columns:
                await connection.execute(text(statement))
                upgraded = True
        if "code" not in columns:
            await connection.execute(
                text("UPDATE agents SET code = CONCAT('employee-', id) WHERE code IS NULL")
            )
            await connection.execute(
                text("ALTER TABLE agents MODIFY COLUMN code VARCHAR(80) NOT NULL")
            )
            await connection.execute(
                text("CREATE UNIQUE INDEX ix_agents_code ON agents (code)")
            )
    return upgraded


async def init_database() -> None:
    from app.db.seed import seed_database

    await ensure_mysql_database()
    async with engine.begin() as connection:
        def remove_legacy_workflow_schema(sync_connection) -> None:
            inspector = inspect(sync_connection)
            tables = set(inspector.get_table_names())
            if "workflow_edges" in tables:
                sync_connection.exec_driver_sql("DROP TABLE workflow_edges")
            if "workflow_nodes" in tables:
                sync_connection.exec_driver_sql("DROP TABLE workflow_nodes")
            if "workflow_runs" in tables:
                columns = {
                    column["name"]
                    for column in inspector.get_columns("workflow_runs")
                }
                if "current_node_id" in columns:
                    sync_connection.exec_driver_sql("DROP TABLE workflow_runs")

        await connection.run_sync(remove_legacy_workflow_schema)
        await connection.run_sync(Base.metadata.create_all)
    agent_schema_upgraded = await ensure_agent_schema()
    async with AsyncSessionLocal() as session:
        await seed_database(session, seed_growth_agents=agent_schema_upgraded)
