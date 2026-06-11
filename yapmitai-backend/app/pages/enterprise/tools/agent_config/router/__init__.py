from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.database import get_db
from .. import service
from ..schema import GatewayConfigUpdate, ModuleConfigUpdate

router = APIRouter(prefix="/agent-config", tags=["agent-config"])


@router.get("/gateway")
async def get_gateway_config(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.get_gateway_config(db))


@router.put("/gateway")
async def update_gateway_config(
    payload: GatewayConfigUpdate, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.update_gateway_config(db, payload.model_dump()))


@router.post("/connection-test")
async def test_connection(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.test_connection(db))


@router.get("/modules/{module}")
async def get_module_config(
    module: str, db: AsyncSession = Depends(get_db)
) -> dict:
    config = await service.get_module_config(db, module)
    if not config:
        raise HTTPException(status_code=404, detail="Module config not found")
    return success(config)


@router.put("/modules/{module}")
async def update_module_config(
    module: str,
    payload: ModuleConfigUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    config = await service.update_module_config(db, module, payload.model_dump())
    if not config:
        raise HTTPException(status_code=404, detail="Module config not found")
    return success(config)
