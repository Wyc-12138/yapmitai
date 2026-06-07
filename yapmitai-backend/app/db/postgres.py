from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings
from app.models import Base

engine = create_async_engine(
    get_settings().database_url,
    pool_pre_ping=True,
    poolclass=NullPool,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

LEGACY_TABLES = (
    "agent_tasks",
    "business_records",
    "gateway_configs",
    "knowledge_chunks",
    "knowledge_collections",
    "knowledge_libraries",
    "knowledge_sync_tasks",
    "model_configs",
    "module_configs",
    "tools",
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_database() -> None:
    from app.db.seed import seed_database

    async with engine.begin() as connection:
        await connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_name = 'model_configs'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'model_configs' AND column_name = 'provider_code'
                    ) THEN
                        DROP TABLE model_configs CASCADE;
                    END IF;
                END $$;
                """
            )
        )
        for table in LEGACY_TABLES:
            if table == "model_configs":
                continue
            await connection.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
        await connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'agents' AND column_name = 'name_en'
                    ) THEN
                        DROP TABLE agents CASCADE;
                    END IF;
                END $$;
                """
            )
        )
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'model_configs' AND column_name = 'max_context_tokens'
                    ) AND NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'model_configs' AND column_name = 'max_input_tokens'
                    ) THEN
                        ALTER TABLE model_configs
                        RENAME COLUMN max_context_tokens TO max_input_tokens;
                    END IF;
                END $$;
                """
            )
        )
        await connection.execute(
            text("ALTER TABLE model_configs DROP COLUMN IF EXISTS default_max_tokens")
        )
        for statement in (
            "ALTER TABLE model_configs ADD COLUMN IF NOT EXISTS context_window_tokens INTEGER",
            "ALTER TABLE model_configs ADD COLUMN IF NOT EXISTS max_output_tokens INTEGER",
            "ALTER TABLE model_configs ALTER COLUMN provider_code TYPE VARCHAR(50)",
            "ALTER TABLE model_configs ALTER COLUMN model_code TYPE VARCHAR(100)",
            "ALTER TABLE model_configs ALTER COLUMN display_name TYPE VARCHAR(100)",
            "ALTER TABLE model_configs ALTER COLUMN model_type TYPE VARCHAR(20)",
            "ALTER TABLE model_configs ALTER COLUMN api_key_last4 TYPE VARCHAR(10)",
            "ALTER TABLE model_configs ALTER COLUMN api_key_last4 DROP NOT NULL",
            """
            UPDATE model_configs
            SET context_window_tokens = COALESCE(context_window_tokens, max_input_tokens, 128000),
                max_output_tokens = COALESCE(max_output_tokens, 4096),
                max_input_tokens = NULL,
                dimension = NULL
            WHERE model_type = 'chat'
            """,
            """
            UPDATE model_configs
            SET max_input_tokens = COALESCE(max_input_tokens, 8191),
                dimension = COALESCE(dimension, 1536),
                context_window_tokens = NULL,
                max_output_tokens = NULL,
                default_temperature = NULL
            WHERE model_type = 'embedding'
            """,
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'ck_model_configs_type'
                ) THEN
                    ALTER TABLE model_configs
                    ADD CONSTRAINT ck_model_configs_type
                    CHECK (model_type IN ('chat', 'embedding'));
                END IF;
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'ck_model_configs_type_fields'
                ) THEN
                    ALTER TABLE model_configs
                    ADD CONSTRAINT ck_model_configs_type_fields
                    CHECK (
                        (model_type = 'chat'
                            AND context_window_tokens IS NOT NULL
                            AND max_output_tokens IS NOT NULL)
                        OR
                        (model_type = 'embedding'
                            AND dimension IS NOT NULL
                            AND max_input_tokens IS NOT NULL)
                    );
                END IF;
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'uq_model_configs_provider_model_type'
                ) THEN
                    ALTER TABLE model_configs
                    ADD CONSTRAINT uq_model_configs_provider_model_type
                    UNIQUE (provider_code, model_code, model_type);
                END IF;
            END $$;
            """,
        ):
            await connection.execute(text(statement))
        for statement in (
            "ALTER TABLE agents ADD COLUMN IF NOT EXISTS chat_model_config_id INTEGER",
            "ALTER TABLE knowledge_bases ADD COLUMN IF NOT EXISTS embedding_model_config_id INTEGER",
            "ALTER TABLE knowledge_bases DROP COLUMN IF EXISTS embedding_model",
            "ALTER TABLE knowledge_bases DROP COLUMN IF EXISTS answer_model",
        ):
            await connection.execute(text(statement))
        for statement in (
            "ALTER TABLE agent_call_logs ADD COLUMN IF NOT EXISTS path VARCHAR(500) NOT NULL DEFAULT ''",
            "ALTER TABLE agent_call_logs ADD COLUMN IF NOT EXISTS method VARCHAR(20) NOT NULL DEFAULT 'GET'",
            "ALTER TABLE agent_call_logs ADD COLUMN IF NOT EXISTS prompt_tokens INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE agent_call_logs ADD COLUMN IF NOT EXISTS completion_tokens INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE agent_call_logs ADD COLUMN IF NOT EXISTS total_tokens INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE agent_call_logs ALTER COLUMN agent_id DROP NOT NULL",
        ):
            await connection.execute(text(statement))
    async with AsyncSessionLocal() as session:
        await seed_database(session)
