from fastapi import APIRouter, HTTPException

from app.core.responses import success
from app.schemas.agents import AgentTaskCreate, AgentToggle, GlobalToggle
from app.schemas.common import AgentCallRequest
from app.services import agents
from app.services.gateway import gateway_service

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
async def get_agents(category: str | None = None) -> dict:
    return success(agents.list_agents(category))


@router.get("/status")
async def get_agent_status() -> dict:
    return success(agents.list_agents())


@router.get("/{agent_id}")
async def get_agent(agent_id: int) -> dict:
    agent = agents.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agent)


@router.patch("/{agent_id}/toggle")
async def toggle_agent(agent_id: int, payload: AgentToggle) -> dict:
    agent = agents.toggle_agent(agent_id, payload.enabled)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agent)


@router.post("/global-toggle")
async def toggle_global(payload: GlobalToggle) -> dict:
    return success(agents.toggle_global(payload.enabled))


@router.post("/{agent_id}/tasks")
async def assign_task(agent_id: int, payload: AgentTaskCreate) -> dict:
    if not agents.get_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return success(agents.assign_task(agent_id, payload.model_dump(mode="json")))


@router.post("/{agent_id}/call")
async def call_agent(agent_id: int, payload: AgentCallRequest) -> dict:
    agent = agents.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = await gateway_service.call(
        f"employee-{agent_id}",
        payload.params,
        {"message": f"{agent['name']} completed the mock request"},
    )
    return success(result)
