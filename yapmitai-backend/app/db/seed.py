from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models import Agent, AiTool, ModelConfig
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
    existing_tools = {
        code for code in (await session.execute(select(AiTool.code))).scalars().all()
    }
    default_tools = [
        {
            "name": "AI多语言文案",
            "name_en": "AI Copywriting",
            "code": "ai-copywriting",
            "category": "内容生成",
            "description": "一键生成中英日韩多语言品牌文案。",
            "icon": "文",
            "prompt_template": "请基于任务简报生成多语言品牌文案，任务：{{task}}",
            "sort_order": 10,
        },
        {
            "name": "AI短视频脚本",
            "name_en": "AI Video Script",
            "code": "ai-video-script",
            "category": "内容生成",
            "description": "TikTok、Reels、小红书脚本自动生成。",
            "icon": "影",
            "prompt_template": "请生成短视频脚本，包含分镜、口播、标题和发布建议，任务：{{task}}",
            "sort_order": 20,
        },
        {
            "name": "AI销售数据分析",
            "name_en": "AI Sales Analytics",
            "code": "ai-sales-analytics",
            "category": "数据分析",
            "description": "亚马逊/独立站销售数据一键分析。",
            "icon": "数",
            "prompt_template": "请分析销售数据并输出洞察、异常、建议动作，任务：{{task}}",
            "sort_order": 30,
        },
        {
            "name": "AI广告优化",
            "name_en": "AI Ad Optimizer",
            "code": "ai-ad-optimizer",
            "category": "营销投放",
            "description": "广告素材评分和投放建议自动生成。",
            "icon": "投",
            "prompt_template": "请评估广告素材和投放计划，输出优化建议，任务：{{task}}",
            "sort_order": 40,
        },
        {
            "name": "AI客服回复",
            "name_en": "AI Customer Reply",
            "code": "ai-customer-reply",
            "category": "客户管理",
            "description": "多语言询盘自动回复，响应时间小于30秒。",
            "icon": "客",
            "prompt_template": "请生成客服回复，要求专业、克制、可直接发送，任务：{{task}}",
            "sort_order": 50,
        },
        {
            "name": "AI竞品分析",
            "name_en": "AI Competitor Intel",
            "code": "ai-competitor-intel",
            "category": "数据分析",
            "description": "追踪竞品定价、评价与策略变化。",
            "icon": "竞",
            "prompt_template": "请做竞品分析，输出目标、建议动作和交付物，任务：{{task}}",
            "sort_order": 60,
        },
    ]
    new_tools = [
        AiTool(
            **item,
            model_config_id=default_chat_model_id,
            input_schema={"fields": [{"name": "task", "label": "任务简报", "type": "textarea"}]},
            output_schema={
                "type": "object",
                "fields": ["title", "target", "suggested_action", "deliverables"],
            },
            enabled=True,
            is_system=True,
            call_count=0,
        )
        for item in default_tools
        if item["code"] not in existing_tools
    ]
    if new_tools:
        session.add_all(new_tools)

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
