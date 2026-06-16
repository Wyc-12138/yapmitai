from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from app.core.responses import success
from app.growth.schemas import AgentInput, TaskStartRequest
from app.growth.services.parser import parse_prompt_to_input
from app.growth.services.task_runner import (
    create_growth_task_record,
    execute_growth_task,
    get_growth_task,
)

router = APIRouter(prefix="/growth/tasks", tags=["growth-team"])


def _serialize(task) -> dict:
    return {
        "taskId": task.id,
        "status": task.status,
        "currentStep": task.current_step,
        "prompt": task.prompt,
        "product": task.product,
        "market": task.market,
        "targetCustomer": task.target_customer,
        "budget": task.budget,
        "context": task.context or {},
        "agentOutputs": task.agent_outputs or [],
        "pdfReady": bool(task.pdf_path),
        "errorMessage": task.error_message,
        "createdAt": task.created_at.isoformat() if task.created_at else None,
        "completedAt": task.completed_at.isoformat() if task.completed_at else None,
    }


@router.post("")
async def start_task(payload: TaskStartRequest, background_tasks: BackgroundTasks) -> dict:
    task_id = f"task-{uuid4().hex[:12]}"
    if payload.prompt and payload.prompt.strip():
        prompt = payload.prompt.strip()
        agent_input = await parse_prompt_to_input(task_id, prompt)
    else:
        prompt = f"将{payload.product}卖到{payload.market}"
        agent_input = AgentInput(
            task_id=task_id,
            product=payload.product or "",
            market=payload.market or "",
            target_customer=payload.target_customer or "潜在消费者",
            budget=payload.budget or "待评估",
        )
    await create_growth_task_record(
        task_id=task_id, prompt=prompt, agent_input=agent_input
    )
    background_tasks.add_task(execute_growth_task, task_id)
    return success(
        {
            "taskId": task_id,
            "status": "running",
            "currentStep": "market_analyst",
            "input": agent_input.model_dump(),
        }
    )


@router.get("/{task_id}")
async def get_task(task_id: str) -> dict:
    task = await get_growth_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return success(_serialize(task))


@router.get("/{task_id}/report")
async def get_report(task_id: str) -> FileResponse:
    task = await get_growth_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "completed" or not task.pdf_path:
        raise HTTPException(status_code=409, detail="Report is not ready")
    path = Path(task.pdf_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report file not found")
    return FileResponse(path, media_type="application/pdf", filename=f"Growth-{task_id}.pdf")
