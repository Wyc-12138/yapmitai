from fastapi import APIRouter, HTTPException

from app.core.responses import success
from app.schemas.agent_config import GatewayConfigUpdate, ModuleConfigUpdate
from app.services import agent_config

router = APIRouter(prefix="/agent-config", tags=["agent-config"])


@router.get("/gateway")
async def get_gateway_config() -> dict:
    return success(agent_config.get_gateway_config())


@router.put("/gateway")
async def update_gateway_config(payload: GatewayConfigUpdate) -> dict:
    return success(agent_config.update_gateway_config(payload.model_dump()))


@router.post("/connection-test")
async def test_connection() -> dict:
    return success(agent_config.test_connection())


@router.get("/modules/{module}")
async def get_module_config(module: str) -> dict:
    config = agent_config.get_module_config(module)
    if not config:
        raise HTTPException(status_code=404, detail="Module config not found")
    return success(config)


@router.put("/modules/{module}")
async def update_module_config(module: str, payload: ModuleConfigUpdate) -> dict:
    config = agent_config.update_module_config(module, payload.model_dump())
    if not config:
        raise HTTPException(status_code=404, detail="Module config not found")
    return success(config)
