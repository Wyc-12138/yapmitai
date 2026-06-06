from fastapi import APIRouter, HTTPException

from app.core.responses import success
from app.schemas.tools import ToolToggle
from app.services import tools

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
async def get_tools(category: str | None = None) -> dict:
    return success(tools.list_tools(category))


@router.patch("/{tool_id}/toggle")
async def toggle_tool(tool_id: int, payload: ToolToggle) -> dict:
    tool = tools.toggle_tool(tool_id, payload.enabled)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return success(tool)
