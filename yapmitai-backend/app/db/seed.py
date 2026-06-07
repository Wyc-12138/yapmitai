from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models import Agent, ModelConfig
from app.shared.mock_data import AGENTS


async def seed_database(session: AsyncSession) -> None:
    settings = get_settings()
    existing = {
        (model_type, model_code)
        for model_type, model_code in (
            await session.execute(select(ModelConfig.model_type, ModelConfig.model_code))
        ).all()
    }
    configs = []
    for index, model_code in enumerate(settings.answer_model_list):
        if ("chat", model_code) not in existing:
            configs.append(
                ModelConfig(
                    provider_code="openai",
                    provider_name="OpenAI",
                    model_code=model_code,
                    display_name=model_code,
                    model_type="chat",
                    api_base_url=settings.external_ai_base_url,
                    api_key_encrypted="",
                    api_key_last4="",
                    context_window_tokens=128000,
                    max_output_tokens=4096,
                    default_temperature=0.2,
                    enabled=True,
                    is_default=index == 0,
                    remark="回答模型，请在页面中填写 API Key。",
                )
            )
    for index, model_code in enumerate(settings.embedding_model_list):
        if ("embedding", model_code) not in existing:
            configs.append(
                ModelConfig(
                    provider_code="openai",
                    provider_name="OpenAI",
                    model_code=model_code,
                    display_name=model_code,
                    model_type="embedding",
                    api_base_url=settings.external_ai_base_url,
                    api_key_encrypted="",
                    api_key_last4="",
                    dimension=1536,
                    max_input_tokens=8191,
                    enabled=True,
                    is_default=index == 0,
                    remark="Embedding 模型，请在页面中填写 API Key。",
                )
            )
    if configs:
        session.add_all(configs)
        await session.flush()
    await session.execute(
        update(ModelConfig)
        .where(
            ModelConfig.model_type == "embedding",
            ModelConfig.max_input_tokens.is_(None),
        )
        .values(max_input_tokens=8191)
    )

    default_chat_model_id = await session.scalar(
        select(ModelConfig.id).where(
            ModelConfig.model_type == "chat",
            ModelConfig.enabled.is_(True),
            ModelConfig.is_default.is_(True),
        )
    )
    if not await session.scalar(select(func.count()).select_from(Agent)):
        session.add_all(
            Agent(
                id=item["id"],
                name=item["name"],
                avatar=None,
                chat_model_config_id=default_chat_model_id,
                system_prompt=f"你是{item['name']}，请基于关联知识库完成工作。",
                category=item["category"],
                status=item["status"],
                enabled=item["enabled"],
                today_done=item["todayDone"],
                month_kpi=item["monthKPI"],
            )
            for item in AGENTS
        )
    else:
        await session.execute(
            Agent.__table__.update()
            .where(Agent.chat_model_config_id.is_(None))
            .values(chat_model_config_id=default_chat_model_id)
        )
    await session.commit()
