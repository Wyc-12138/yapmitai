from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.database import AsyncSessionLocal
from app.growth.agents import (
    BrandManagerAgent,
    ContentCreatorAgent,
    MarketAnalystAgent,
    MediaBuyingAgent,
)
from app.growth.schemas import AgentInput
from app.growth.workflow.state import WorkflowState
from app.models import Agent
from app.models.growth_task import GrowthTask

GROWTH_AGENT_CODES = (
    "growth-market-analyst",
    "growth-brand-manager",
    "growth-content-creator",
    "growth-media-buying",
)


async def _persist(task_id: str, next_step: str, partial: dict[str, Any]) -> None:
    async with AsyncSessionLocal() as session:
        task = await session.get(GrowthTask, task_id)
        if not task:
            return
        task.current_step = next_step
        task.context = {**(task.context or {}), **partial}
        await session.commit()


async def _load_growth_agents() -> dict[str, Agent]:
    async with AsyncSessionLocal() as session:
        agents = (
            await session.scalars(
                select(Agent)
                .where(Agent.code.in_(GROWTH_AGENT_CODES))
                .options(selectinload(Agent.chat_model_config))
            )
        ).all()
    configs = {item.code: item for item in agents}
    missing = [
        code
        for code in GROWTH_AGENT_CODES
        if code not in configs or not configs[code].enabled
    ]
    if missing:
        raise RuntimeError(f"增长工作流 Agent 缺失或未启用：{', '.join(missing)}")
    return configs


async def run_growth_workflow(agent_input: AgentInput) -> WorkflowState:
    context: dict[str, Any] = {}
    outputs: list[dict[str, Any]] = []
    configs = await _load_growth_agents()
    steps = [
        (
            "market_analyst",
            "brand_manager",
            MarketAnalystAgent(configs["growth-market-analyst"]),
            "market_report",
        ),
        (
            "brand_manager",
            "content_creator",
            BrandManagerAgent(configs["growth-brand-manager"]),
            "brand_strategy",
        ),
        (
            "content_creator",
            "media_buying",
            ContentCreatorAgent(configs["growth-content-creator"]),
            "content_assets",
        ),
        (
            "media_buying",
            "completed",
            MediaBuyingAgent(configs["growth-media-buying"]),
            "media_plan",
        ),
    ]
    for _, next_step, agent, result_key in steps:
        output = await agent.run(agent_input, context)
        context[result_key] = output.result
        outputs.append(output.model_dump())
        await _persist(agent_input.task_id, next_step, {result_key: output.result})
    return {
        "task_id": agent_input.task_id,
        "agent_input": agent_input,
        **context,
        "agent_outputs": outputs,
        "current_step": "completed",
    }
