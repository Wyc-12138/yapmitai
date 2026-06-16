from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.db.database import AsyncSessionLocal
from app.growth.services.llm import growth_llm_service
from app.models import Agent
from app.team.models import AiTeam, AiTeamAgent
from app.team.workflow.models import WorkflowRun, WorkflowTask, WorkflowTaskAgent
from app.team.workflow.report import generate_workflow_report


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _agent_dict(agent: Agent) -> dict[str, Any]:
    model = agent.__dict__.get("chat_model_config")
    return {
        "id": agent.id,
        "code": agent.code,
        "name": agent.name,
        "nameEn": agent.name_en or "",
        "description": agent.description or "",
        "category": agent.category,
        "status": agent.status,
        "model": model.display_name if model else "",
    }


async def _get_team_agents(db: AsyncSession, team_id: int) -> list[Agent]:
    return list(
        (
            await db.scalars(
                select(Agent)
                .join(AiTeamAgent, AiTeamAgent.agent_id == Agent.id)
                .where(AiTeamAgent.team_id == team_id)
                .options(selectinload(Agent.chat_model_config))
                .order_by(Agent.id)
            )
        ).all()
    )


async def _ensure_task_agents(db: AsyncSession, task: WorkflowTask) -> None:
    count = await db.scalar(
        select(func.count())
        .select_from(WorkflowTaskAgent)
        .where(WorkflowTaskAgent.task_id == task.id)
    )
    if count:
        return
    agents = await _get_team_agents(db, task.team_id)
    db.add_all(
        WorkflowTaskAgent(task_id=task.id, agent_id=agent.id, sort_order=index)
        for index, agent in enumerate(agents)
    )
    await db.commit()


async def list_team_options(db: AsyncSession) -> list[dict]:
    teams = (await db.scalars(select(AiTeam).order_by(AiTeam.name))).all()
    return [
        {
            "id": team.id,
            "name": team.name,
            "enabled": team.enabled,
            "agents": [_agent_dict(agent) for agent in await _get_team_agents(db, team.id)],
        }
        for team in teams
    ]


async def _ordered_agents(db: AsyncSession, task_id: int) -> list[dict]:
    rows = (
        await db.execute(
            select(WorkflowTaskAgent, Agent)
            .join(Agent, Agent.id == WorkflowTaskAgent.agent_id)
            .where(WorkflowTaskAgent.task_id == task_id)
            .options(selectinload(Agent.chat_model_config))
            .order_by(WorkflowTaskAgent.sort_order, WorkflowTaskAgent.id)
        )
    ).all()
    return [
        {
            **_agent_dict(agent),
            "order": item.sort_order,
            "runStatus": item.run_status,
            "output": item.output,
            "errorMessage": item.error_message,
            "startedAt": item.started_at.isoformat() if item.started_at else None,
            "finishedAt": item.finished_at.isoformat() if item.finished_at else None,
        }
        for item, agent in rows
    ]


async def _latest_run(db: AsyncSession, task_id: int) -> WorkflowRun | None:
    return await db.scalar(
        select(WorkflowRun)
        .where(WorkflowRun.task_id == task_id)
        .order_by(WorkflowRun.started_at.desc())
        .limit(1)
    )


async def _task_dict(db: AsyncSession, task: WorkflowTask, detail: bool = False) -> dict:
    await _ensure_task_agents(db, task)
    team = await db.get(AiTeam, task.team_id)
    agent_count = (
        await db.scalar(
            select(func.count())
            .select_from(WorkflowTaskAgent)
            .where(WorkflowTaskAgent.task_id == task.id)
        )
        or 0
    )
    data = {
        "id": task.id,
        "teamId": task.team_id,
        "teamName": team.name if team else "",
        "name": task.name,
        "description": task.description or "",
        "enabled": task.enabled,
        "status": task.status,
        "agentCount": agent_count,
        "nodeCount": agent_count,
        "createdAt": task.created_at.isoformat() if task.created_at else None,
        "updatedAt": task.updated_at.isoformat() if task.updated_at else None,
    }
    if detail:
        latest = await _latest_run(db, task.id)
        data["agents"] = await _ordered_agents(db, task.id)
        data["latestRun"] = (
            {
                "id": latest.id,
                "status": latest.status,
                "prompt": latest.prompt,
                "pdfReady": bool(latest.pdf_path),
                "errorMessage": latest.error_message,
            }
            if latest
            else None
        )
    return data


async def list_tasks(db: AsyncSession) -> list[dict]:
    tasks = (await db.scalars(select(WorkflowTask).order_by(WorkflowTask.id.desc()))).all()
    return [await _task_dict(db, task) for task in tasks]


async def get_task(db: AsyncSession, task_id: int) -> dict | None:
    task = await db.get(WorkflowTask, task_id)
    return await _task_dict(db, task, detail=True) if task else None


async def create_task(db: AsyncSession, payload: dict) -> dict:
    team = await db.get(AiTeam, payload["team_id"])
    if not team:
        raise ValueError("AI团队不存在")
    agents = await _get_team_agents(db, team.id)
    if not agents:
        raise ValueError("该AI团队还没有员工")
    task = WorkflowTask(**payload, status="ready")
    db.add(task)
    await db.flush()
    db.add_all(
        WorkflowTaskAgent(task_id=task.id, agent_id=agent.id, sort_order=index)
        for index, agent in enumerate(agents)
    )
    await db.commit()
    await db.refresh(task)
    return await _task_dict(db, task, detail=True)


async def update_task(db: AsyncSession, task_id: int, payload: dict) -> dict | None:
    task = await db.get(WorkflowTask, task_id)
    if not task:
        return None
    if "team_id" in payload and payload["team_id"] != task.team_id:
        raise ValueError("已创建任务不能更换AI团队，请新建任务")
    for field, value in payload.items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return await _task_dict(db, task, detail=True)


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    task = await db.get(WorkflowTask, task_id)
    if not task:
        return False
    await db.delete(task)
    await db.commit()
    return True


async def save_order(
    db: AsyncSession, task_id: int, agent_ids: list[int]
) -> dict | None:
    task = await db.get(WorkflowTask, task_id)
    if not task:
        return None
    team_ids = {agent.id for agent in await _get_team_agents(db, task.team_id)}
    if len(agent_ids) != len(set(agent_ids)) or set(agent_ids) != team_ids:
        raise ValueError("排序必须包含该团队的全部AI员工，且不能重复")
    existing = {
        item.agent_id: item
        for item in (
            await db.scalars(
                select(WorkflowTaskAgent).where(WorkflowTaskAgent.task_id == task_id)
            )
        ).all()
    }
    await db.execute(
        delete(WorkflowTaskAgent).where(
            WorkflowTaskAgent.task_id == task_id,
            WorkflowTaskAgent.agent_id.not_in(agent_ids),
        )
    )
    for index, agent_id in enumerate(agent_ids):
        item = existing.get(agent_id)
        if item:
            item.sort_order = index
        else:
            db.add(
                WorkflowTaskAgent(
                    task_id=task_id, agent_id=agent_id, sort_order=index
                )
            )
    task.status = "ready"
    await db.commit()
    return await _task_dict(db, task, detail=True)


async def create_run(db: AsyncSession, task_id: int, prompt: str) -> dict | None:
    task = await db.get(WorkflowTask, task_id)
    if not task:
        return None
    agents = await _ordered_agents(db, task_id)
    if not agents:
        raise ValueError("该工作流没有AI员工")
    items = (
        await db.scalars(
            select(WorkflowTaskAgent).where(WorkflowTaskAgent.task_id == task_id)
        )
    ).all()
    for item in items:
        item.run_status = "queued"
        item.output = None
        item.error_message = None
        item.started_at = None
        item.finished_at = None
    run = WorkflowRun(
        id=f"run-{uuid4().hex[:16]}",
        task_id=task_id,
        status="running",
        prompt=prompt,
        report_data={},
    )
    task.status = "running"
    db.add(run)
    await db.commit()
    return {"runId": run.id, "taskId": task_id, "status": "running"}


async def execute_run(run_id: str) -> None:
    async with AsyncSessionLocal() as db:
        run = await db.get(WorkflowRun, run_id)
        if not run:
            return
        task = await db.get(WorkflowTask, run.task_id)
        team = await db.get(AiTeam, task.team_id) if task else None
        rows = (
            await db.execute(
                select(WorkflowTaskAgent, Agent)
                .join(Agent, Agent.id == WorkflowTaskAgent.agent_id)
                .where(WorkflowTaskAgent.task_id == run.task_id)
                .options(selectinload(Agent.chat_model_config))
                .order_by(WorkflowTaskAgent.sort_order)
            )
        ).all()
        sections: list[dict[str, Any]] = []
        context: dict[str, Any] = {}
        try:
            for item, agent in rows:
                item.run_status = "running"
                item.started_at = _now()
                run.current_agent_id = agent.id
                await db.commit()
                result = await growth_llm_service.complete_json(
                    agent.system_prompt
                    or f"你是{agent.name}，负责{agent.category}。请输出专业、可执行的JSON报告章节。",
                    (
                        f"用户完整需求：{run.prompt}\n"
                        f"当前执行步骤：{item.sort_order + 1}/{len(rows)}\n"
                        f"前序Agent累计结果：{context}\n"
                        "请基于用户需求和前序结果完成你的职责。输出JSON对象，"
                        "至少包含summary、analysis、recommendations、deliverables字段。"
                    ),
                    model_config=agent.chat_model_config,
                )
                item.output = result
                item.run_status = "completed"
                item.finished_at = _now()
                context[agent.code] = result
                sections.append(
                    {
                        "agentId": agent.id,
                        "agentName": agent.name,
                        "title": f"{item.sort_order + 1}. {agent.name}",
                        "content": result,
                    }
                )
                run.report_data = {"sections": sections}
                await db.commit()

            pdf_path = (
                Path(get_settings().growth_reports_dir)
                / "workflows"
                / f"{run.id}.pdf"
            )
            generate_workflow_report(
                task_name=task.name,
                team_name=team.name if team else "",
                prompt=run.prompt,
                sections=sections,
                output_path=pdf_path,
            )
            run.status = "completed"
            run.current_agent_id = None
            run.pdf_path = str(pdf_path.resolve())
            run.completed_at = _now()
            task.status = "completed"
            await db.commit()
        except Exception as exc:
            run.status = "failed"
            run.error_message = str(exc)
            run.completed_at = _now()
            task.status = "failed"
            if run.current_agent_id:
                current = await db.scalar(
                    select(WorkflowTaskAgent).where(
                        WorkflowTaskAgent.task_id == run.task_id,
                        WorkflowTaskAgent.agent_id == run.current_agent_id,
                    )
                )
                if current:
                    current.run_status = "failed"
                    current.error_message = str(exc)
                    current.finished_at = _now()
            await db.commit()


async def get_run(db: AsyncSession, task_id: int, run_id: str) -> dict | None:
    run = await db.get(WorkflowRun, run_id)
    if not run or run.task_id != task_id:
        return None
    return {
        "id": run.id,
        "taskId": run.task_id,
        "status": run.status,
        "currentAgentId": run.current_agent_id,
        "prompt": run.prompt,
        "reportData": run.report_data or {},
        "pdfReady": bool(run.pdf_path),
        "errorMessage": run.error_message,
        "startedAt": run.started_at.isoformat() if run.started_at else None,
        "completedAt": run.completed_at.isoformat() if run.completed_at else None,
        "agents": await _ordered_agents(db, task_id),
    }


async def get_report_path(
    db: AsyncSession, task_id: int, run_id: str
) -> Path | None:
    run = await db.get(WorkflowRun, run_id)
    if (
        not run
        or run.task_id != task_id
        or run.status != "completed"
        or not run.pdf_path
    ):
        return None
    path = Path(run.pdf_path)
    return path if path.exists() else None
