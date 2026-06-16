from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.database import get_db
from app.team.workflow import service
from app.team.workflow.schema import (
    WorkflowOrderUpdate,
    WorkflowRunCreate,
    WorkflowTaskCreate,
    WorkflowTaskUpdate,
)

router = APIRouter(prefix="/workflows", tags=["AI团队工作流"])


@router.get("")
async def list_tasks(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_tasks(db))


@router.get("/team-options")
async def list_team_options(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_team_options(db))


@router.post("")
async def create_task(
    payload: WorkflowTaskCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        return success(await service.create_task(db, payload.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    task = await service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="工作流任务不存在")
    return success(task)


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    payload: WorkflowTaskUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        task = await service.update_task(
            db, task_id, payload.model_dump(exclude_unset=True)
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not task:
        raise HTTPException(status_code=404, detail="工作流任务不存在")
    return success(task)


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    if not await service.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="工作流任务不存在")
    return success({"deleted": True, "id": task_id})


@router.put("/{task_id}/agent-order")
async def save_agent_order(
    task_id: int,
    payload: WorkflowOrderUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        task = await service.save_order(db, task_id, payload.agent_ids)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not task:
        raise HTTPException(status_code=404, detail="工作流任务不存在")
    return success(task)


@router.post("/{task_id}/runs")
async def start_run(
    task_id: int,
    payload: WorkflowRunCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        run = await service.create_run(db, task_id, payload.prompt)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not run:
        raise HTTPException(status_code=404, detail="工作流任务不存在")
    background_tasks.add_task(service.execute_run, run["runId"])
    return success(run)


@router.get("/{task_id}/runs/{run_id}")
async def get_run(
    task_id: int, run_id: str, db: AsyncSession = Depends(get_db)
) -> dict:
    run = await service.get_run(db, task_id, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="工作流运行记录不存在")
    return success(run)


@router.get("/{task_id}/runs/{run_id}/report")
async def download_report(
    task_id: int, run_id: str, db: AsyncSession = Depends(get_db)
) -> FileResponse:
    path = await service.get_report_path(db, task_id, run_id)
    if not path:
        raise HTTPException(status_code=409, detail="PDF报告尚未生成")
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=f"Workflow-{task_id}-{run_id}.pdf",
    )
