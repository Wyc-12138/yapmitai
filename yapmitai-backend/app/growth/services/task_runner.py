from datetime import UTC, datetime
from pathlib import Path

from app.core.config import get_settings
from app.db.database import AsyncSessionLocal
from app.growth.schemas import AgentInput
from app.growth.services.pdf_report import generate_growth_strategy_report
from app.growth.workflow import run_growth_workflow
from app.models.growth_task import GrowthTask


async def create_growth_task_record(
    *, task_id: str, prompt: str, agent_input: AgentInput
) -> GrowthTask:
    async with AsyncSessionLocal() as session:
        task = GrowthTask(
            id=task_id,
            prompt=prompt,
            product=agent_input.product,
            market=agent_input.market,
            target_customer=agent_input.target_customer,
            budget=agent_input.budget,
            status="pending",
            current_step="market_analyst",
            context={},
            agent_outputs=[],
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


async def get_growth_task(task_id: str) -> GrowthTask | None:
    async with AsyncSessionLocal() as session:
        return await session.get(GrowthTask, task_id)


async def execute_growth_task(task_id: str) -> None:
    async with AsyncSessionLocal() as session:
        task = await session.get(GrowthTask, task_id)
        if not task:
            return
        task.status = "running"
        await session.commit()
        agent_input = AgentInput(
            task_id=task.id,
            product=task.product,
            market=task.market,
            target_customer=task.target_customer,
            budget=task.budget,
        )
        snapshot = {
            "prompt": task.prompt,
            "product": task.product,
            "market": task.market,
            "target_customer": task.target_customer,
            "budget": task.budget,
        }
    try:
        state = await run_growth_workflow(agent_input)
        context = {
            "market_report": state.get("market_report", {}),
            "brand_strategy": state.get("brand_strategy", {}),
            "content_assets": state.get("content_assets", {}),
            "media_plan": state.get("media_plan", {}),
        }
        pdf_path = Path(get_settings().growth_reports_dir) / f"{task_id}.pdf"
        generate_growth_strategy_report(
            {"id": task_id, **snapshot, "context": context}, pdf_path
        )
        async with AsyncSessionLocal() as session:
            task = await session.get(GrowthTask, task_id)
            if not task:
                return
            task.status = "completed"
            task.current_step = "completed"
            task.context = context
            task.agent_outputs = state.get("agent_outputs", [])
            task.pdf_path = str(pdf_path.resolve())
            task.completed_at = datetime.now(UTC)
            task.error_message = None
            await session.commit()
    except Exception as exc:
        async with AsyncSessionLocal() as session:
            task = await session.get(GrowthTask, task_id)
            if not task:
                return
            task.status = "failed"
            task.error_message = str(exc) or "增长工作流执行失败"
            await session.commit()
