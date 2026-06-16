from uuid import uuid4

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    Agent,
    AgentKnowledgeBase,
    Conversation,
    KnowledgeBase,
    Message,
    ModelConfig,
)


def _agent_dict(agent: Agent) -> dict:
    chat_config = agent.__dict__.get("chat_model_config")
    return {
        "id": agent.id,
        "code": agent.code,
        "name": agent.name,
        "nameEn": agent.name_en or "",
        "description": agent.description or "",
        "avatar": agent.avatar,
        "chatModelConfigId": agent.chat_model_config_id,
        "model": chat_config.display_name if chat_config else "",
        "modelCode": chat_config.model_code if chat_config else "",
        "systemPrompt": agent.system_prompt,
        "status": agent.status,
        "category": agent.category,
        "todayDone": agent.today_done,
        "monthKPI": agent.month_kpi,
        "enabled": agent.enabled,
    }


async def _valid_chat_model(db: AsyncSession, config_id: int | None) -> bool:
    if config_id is None:
        return True
    return bool(
        await db.scalar(
            select(ModelConfig.id).where(
                ModelConfig.id == config_id,
                ModelConfig.model_type == "chat",
            )
        )
    )


async def create_agent(db: AsyncSession, payload: dict) -> dict:
    if await db.scalar(select(Agent.id).where(Agent.code == payload["code"])):
        raise ValueError("Agent code already exists")
    if not await _valid_chat_model(db, payload.get("chat_model_config_id")):
        raise ValueError("Agent can only use a Chat model")
    agent = Agent(
        id=(await db.scalar(select(func.max(Agent.id))) or 0) + 1,
        **payload,
    )
    db.add(agent)
    await db.commit()
    return await get_agent(db, agent.id)


async def update_agent(
    db: AsyncSession, agent_id: int, payload: dict
) -> dict | None:
    agent = await db.get(Agent, agent_id)
    if not agent:
        return None
    if "code" in payload and payload["code"] != agent.code:
        if await db.scalar(select(Agent.id).where(Agent.code == payload["code"])):
            raise ValueError("Agent code already exists")
    if (
        "chat_model_config_id" in payload
        and not await _valid_chat_model(db, payload["chat_model_config_id"])
    ):
        raise ValueError("Agent can only use a Chat model")
    for field, value in payload.items():
        setattr(agent, field, value)
    await db.commit()
    return await get_agent(db, agent_id)


async def delete_agent(db: AsyncSession, agent_id: int) -> bool:
    agent = await db.get(Agent, agent_id)
    if not agent:
        return False
    await db.delete(agent)
    await db.commit()
    return True


async def list_chat_models(db: AsyncSession) -> list[dict]:
    models = (
        await db.scalars(
            select(ModelConfig)
            .where(
                ModelConfig.model_type == "chat",
                ModelConfig.enabled.is_(True),
            )
            .order_by(ModelConfig.is_default.desc(), ModelConfig.display_name)
        )
    ).all()
    return [
        {
            "id": item.id,
            "displayName": item.display_name,
            "modelCode": item.model_code,
            "isDefault": item.is_default,
        }
        for item in models
    ]


async def list_agents(db: AsyncSession, category: str | None = None) -> list[dict]:
    statement = select(Agent).options(selectinload(Agent.chat_model_config)).order_by(Agent.id)
    if category:
        statement = statement.where(Agent.category == category)
    return [_agent_dict(item) for item in (await db.scalars(statement)).all()]


async def get_agent(db: AsyncSession, agent_id: int) -> dict | None:
    agent = await db.scalar(
        select(Agent)
        .where(Agent.id == agent_id)
        .options(selectinload(Agent.chat_model_config))
    )
    return _agent_dict(agent) if agent else None


async def toggle_agent(db: AsyncSession, agent_id: int, enabled: bool) -> dict | None:
    agent = await db.get(Agent, agent_id)
    if not agent:
        return None
    agent.enabled = enabled
    agent.status = "standby" if enabled else "offline"
    await db.commit()
    return await get_agent(db, agent_id)


async def toggle_global(db: AsyncSession, enabled: bool) -> dict:
    await db.execute(
        update(Agent).values(enabled=enabled, status="standby" if enabled else "offline")
    )
    await db.commit()
    return {"enabled": enabled}


async def assign_task(db: AsyncSession, agent_id: int, payload: dict) -> dict:
    conversation = Conversation(
        id=f"conversation-{uuid4().hex[:12]}",
        agent_id=agent_id,
        title=payload["description"][:80],
    )
    db.add(conversation)
    await db.flush()
    db.add(
        Message(
            id=f"message-{uuid4().hex[:12]}",
            conversation_id=conversation.id,
            role="user",
            content=payload["description"],
            sources=[],
        )
    )
    await db.commit()
    return {
        "taskId": conversation.id,
        "agentId": agent_id,
        "status": "running",
        **payload,
    }


async def list_knowledge_bases(db: AsyncSession, agent_id: int) -> list[dict]:
    rows = (
        await db.execute(
            select(KnowledgeBase)
            .join(
                AgentKnowledgeBase,
                AgentKnowledgeBase.knowledge_base_id == KnowledgeBase.id,
            )
            .where(AgentKnowledgeBase.agent_id == agent_id)
            .order_by(KnowledgeBase.name)
        )
    ).scalars().all()
    return [
        {"id": item.id, "name": item.name, "status": item.status}
        for item in rows
    ]


async def set_knowledge_bases(
    db: AsyncSession, agent_id: int, knowledge_base_ids: list[str]
) -> list[dict] | None:
    if not await db.get(Agent, agent_id):
        return None
    await db.execute(
        AgentKnowledgeBase.__table__.delete().where(
            AgentKnowledgeBase.agent_id == agent_id
        )
    )
    if knowledge_base_ids:
        valid_ids = set(
            (
                await db.scalars(
                    select(KnowledgeBase.id).where(
                        KnowledgeBase.id.in_(knowledge_base_ids)
                    )
                )
            ).all()
        )
        db.add_all(
            AgentKnowledgeBase(agent_id=agent_id, knowledge_base_id=item)
            for item in knowledge_base_ids
            if item in valid_ids
        )
    await db.commit()
    return await list_knowledge_bases(db, agent_id)
