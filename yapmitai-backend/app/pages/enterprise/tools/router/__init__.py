from fastapi import APIRouter, HTTPException

from app.core.responses import success
from .. import service
from ..schema import ToolToggle

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
async def get_tools(category: str | None = None) -> dict:
    return success(service.list_tools(category))


@router.patch("/{tool_id}/toggle")
async def toggle_tool(tool_id: int, payload: ToolToggle) -> dict:
    tool = service.toggle_tool(tool_id, payload.enabled)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(tool)
