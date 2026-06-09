from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.postgres import get_db
from .. import service
from ..schema import ToolCreate, ToolRun, ToolToggle, ToolUpdate

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
async def get_tools(
    category: str | None = None,
    enabled: bool | None = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return success(await service.list_tools(db, category, enabled))


@router.get("/chat-models")
async def get_chat_models(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_chat_models(db))


@router.post("")
async def create_tool(payload: ToolCreate, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        item = await service.create_tool(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return success(item)


@router.get("/{tool_id}")
async def get_tool(tool_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    item = await service.get_tool(db, tool_id)
    if not item:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(item)


@router.patch("/{tool_id}")
async def update_tool(
    tool_id: int, payload: ToolUpdate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        item = await service.update_tool(
            db, tool_id, payload.model_dump(exclude_unset=True)
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    if not item:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(item)


@router.delete("/{tool_id}")
async def delete_tool(tool_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    if not await service.delete_tool(db, tool_id):
        raise HTTPException(status_code=404, detail="Tool not found")
    return success({"deleted": True, "id": tool_id})


@router.patch("/{tool_id}/toggle")
async def toggle_tool(
    tool_id: int, payload: ToolToggle, db: AsyncSession = Depends(get_db)
) -> dict:
    tool = await service.toggle_tool(db, tool_id, payload.enabled)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(tool)


@router.post("/{tool_id}/run")
async def run_tool(
    tool_id: int,
    payload: ToolRun,
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await service.run_tool(
        db, tool_id, payload.task, payload.model_config_id
    )
    if not result:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(result)


@router.get("/{tool_id}/records")
async def get_tool_records(
    tool_id: int,
    limit: int = Query(default=3, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
) -> dict:
    item = await service.get_tool(db, tool_id)
    if not item:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(item["recentRecords"][:limit])
