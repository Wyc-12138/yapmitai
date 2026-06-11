import json
from datetime import UTC, datetime
from pathlib import Path

from app.core.config import get_settings
from app.db.postgres import AsyncSessionLocal
from app.growth.schemas import AgentInput
from app.growth.services.llm import growth_llm_service
from app.growth.services.pdf_report import generate_growth_strategy_report
from app.growth.workflow import run_growth_workflow
from app.models.growth_task import GrowthTask


async def _build_execution_recommendations(context: dict) -> str:
    payload = await growth_llm_service.complete_json(
        (
            "你是增长战略顾问。根据完整增长方案（市场、品牌、内容、投放）输出 JSON："
            '{"execution_recommendations": "5-8条编号的中文执行建议，涵盖渠道、预算、内容、复盘节奏"}'
        ),
        json.dumps(context, ensure_ascii=False),
        temperature=0.3,
    )
    return str(payload.get("execution_recommendations", "")).strip()


async def execute_growth_task(task_id: str) -> None:
    settings = get_settings()
    async with AsyncSessionLocal() as session:
        task = await session.get(GrowthTask, task_id)
        if not task:
            return
        task.status = "running"
        task.current_step = "market_analyst"
        await session.commit()

    try:
        async with AsyncSessionLocal() as session:
            task = await session.get(GrowthTask, task_id)
            if not task:
                return
            agent_input = AgentInput(
                task_id=task.id,
                product=task.product,
                market=task.market,
                target_customer=task.target_customer,
                budget=task.budget,
            )
            task_snapshot = {
                "prompt": task.prompt,
                "product": task.product,
                "market": task.market,
                "target_customer": task.target_customer,
                "budget": task.budget,
            }
        final_state = await run_growth_workflow(agent_input)
        context = {
            "market_report": final_state.get("market_report") or {},
            "brand_strategy": final_state.get("brand_strategy") or {},
            "content_assets": final_state.get("content_assets") or {},
            "media_plan": final_state.get("media_plan") or {},
        }
        context["execution_recommendations"] = await _build_execution_recommendations(context)
        reports_dir = Path(settings.growth_reports_dir)
        pdf_path = reports_dir / f"{task_id}.pdf"
        generate_growth_strategy_report(
            {
                "id": task_id,
                "prompt": task_snapshot["prompt"],
                "product": task_snapshot["product"],
                "market": task_snapshot["market"],
                "target_customer": task_snapshot["target_customer"],
                "budget": task_snapshot["budget"],
                "status": "completed",
                "context": context,
            },
            pdf_path,
        )
        async with AsyncSessionLocal() as session:
            task = await session.get(GrowthTask, task_id)
            if not task:
                return
            task.status = "completed"
            task.current_step = "completed"
            task.context = context
            task.agent_outputs = final_state.get("agent_outputs") or []
            task.pdf_path = str(pdf_path.resolve())
            task.completed_at = datetime.now(UTC)
            task.error_message = None
            await session.commit()
    except Exception as exc:
        message = str(exc).strip() or f"{type(exc).__name__}: task execution failed"
        async with AsyncSessionLocal() as session:
            task = await session.get(GrowthTask, task_id)
            if not task:
                return
            task.status = "failed"
            task.error_message = message
            await session.commit()


async def create_growth_task_record(
    *,
    task_id: str,
    prompt: str,
    agent_input: AgentInput,
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
