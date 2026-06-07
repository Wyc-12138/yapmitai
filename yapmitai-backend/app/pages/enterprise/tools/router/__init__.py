from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.postgres import get_db
from .. import service
from ..schema import ToolToggle

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
async def get_tools(
    category: str | None = None, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.list_tools(db, category))


@router.patch("/{tool_id}/toggle")
async def toggle_tool(
    tool_id: int, payload: ToolToggle, db: AsyncSession = Depends(get_db)
) -> dict:
    tool = await service.toggle_tool(db, tool_id, payload.enabled)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(tool)
