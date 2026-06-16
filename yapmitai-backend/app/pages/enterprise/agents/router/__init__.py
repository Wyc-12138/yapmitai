from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.database import get_db
from app.shared.gateway import gateway_service
from app.shared.schema import AgentCallRequest

from .. import service
from ..schema import (
    AgentCreate,
    AgentKnowledgeBaseUpdate,
    AgentTaskCreate,
    AgentToggle,
    AgentUpdate,
    GlobalToggle,
)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
async def get_agents(
    category: str | None = None, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.list_agents(db, category))


@router.get("/status")
async def get_agent_status(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_agents(db))


@router.get("/chat-models")
async def get_chat_models(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_chat_models(db))


@router.post("")
async def create_agent(
    payload: AgentCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        return success(await service.create_agent(db, payload.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/{agent_id}/knowledge-bases")
async def get_agent_knowledge_bases(
    agent_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    if not await service.get_agent(db, agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(await service.list_knowledge_bases(db, agent_id))


@router.put("/{agent_id}/knowledge-bases")
async def set_agent_knowledge_bases(
    agent_id: int,
    payload: AgentKnowledgeBaseUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await service.set_knowledge_bases(
        db, agent_id, payload.knowledge_base_ids
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(result)


@router.get("/{agent_id}")
async def get_agent(agent_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    agent = await service.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agent)


@router.patch("/{agent_id}")
async def update_agent(
    agent_id: int, payload: AgentUpdate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        agent = await service.update_agent(
            db, agent_id, payload.model_dump(exclude_unset=True)
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agent)


@router.delete("/{agent_id}")
async def delete_agent(agent_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    if not await service.delete_agent(db, agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return success({"deleted": True, "id": agent_id})


@router.patch("/{agent_id}/toggle")
async def toggle_agent(
    agent_id: int, payload: AgentToggle, db: AsyncSession = Depends(get_db)
) -> dict:
    agent = await service.toggle_agent(db, agent_id, payload.enabled)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agent)


@router.post("/global-toggle")
async def toggle_global(
    payload: GlobalToggle, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.toggle_global(db, payload.enabled))


@router.post("/{agent_id}/tasks")
async def assign_task(
    agent_id: int, payload: AgentTaskCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    if not await service.get_agent(db, agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(
        await service.assign_task(db, agent_id, payload.model_dump(mode="json"))
    )


@router.post("/{agent_id}/call")
async def call_agent(
    agent_id: int, payload: AgentCallRequest, db: AsyncSession = Depends(get_db)
) -> dict:
    agent = await service.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = await gateway_service.call(
        f"employee-{agent_id}",
        payload.params,
        {"message": f"{agent['name']} completed the mock request"},
    )
    return success(result)
