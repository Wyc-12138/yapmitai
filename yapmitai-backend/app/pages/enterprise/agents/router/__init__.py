from fastapi import APIRouter, HTTPException

from app.core.responses import success
from app.shared.gateway import gateway_service
from app.shared.schema import AgentCallRequest

from .. import service
from ..schema import AgentTaskCreate, AgentToggle, GlobalToggle

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
async def get_agents(category: str | None = None) -> dict:
    return success(service.list_agents(category))


@router.get("/status")
async def get_agent_status() -> dict:
    return success(service.list_agents())


@router.get("/{agent_id}")
async def get_agent(agent_id: int) -> dict:
    agent = service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agent)


@router.patch("/{agent_id}/toggle")
async def toggle_agent(agent_id: int, payload: AgentToggle) -> dict:
    agent = service.toggle_agent(agent_id, payload.enabled)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agent)


@router.post("/global-toggle")
async def toggle_global(payload: GlobalToggle) -> dict:
    return success(service.toggle_global(payload.enabled))


@router.post("/{agent_id}/tasks")
async def assign_task(agent_id: int, payload: AgentTaskCreate) -> dict:
    if not service.get_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(service.assign_task(agent_id, payload.model_dump(mode="json")))


@router.post("/{agent_id}/call")
async def call_agent(agent_id: int, payload: AgentCallRequest) -> dict:
    agent = service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = await gateway_service.call(
        f"employee-{agent_id}",
        payload.params,
        {"message": f"{agent['name']} completed the mock request"},
    )
    return success(result)
