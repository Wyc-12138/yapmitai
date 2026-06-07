from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.postgres import get_db

from .. import service
from ..schema import ModelConfigCreate, ModelConfigUpdate

router = APIRouter(prefix="/model-configs", tags=["model-configs"])


@router.get("")
async def list_configs(
    model_type: str | None = Query(default=None, pattern="^(chat|embedding)$"),
    enabled: bool | None = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return success(await service.list_configs(db, model_type, enabled))


@router.post("")
async def create_config(
    payload: ModelConfigCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        item = await service.create_config(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return success(item)


@router.get("/{config_id}")
async def get_config(config_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    item = await service.get_config(db, config_id)
    if not item:
        raise HTTPException(status_code=404, detail="Model config not found")
    return success(item)


@router.patch("/{config_id}")
async def update_config(
    config_id: int,
    payload: ModelConfigUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        item = await service.update_config(
            db, config_id, payload.model_dump(exclude_none=True)
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    if not item:
        raise HTTPException(status_code=404, detail="Model config not found")
    return success(item)


@router.delete("/{config_id}")
async def delete_config(config_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    if not await service.delete_config(db, config_id):
        raise HTTPException(status_code=404, detail="Model config not found")
    return success({"deleted": True, "id": config_id})
