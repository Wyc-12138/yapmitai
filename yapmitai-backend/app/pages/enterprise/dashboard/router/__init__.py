from fastapi import APIRouter

from app.core.responses import success
from .. import service

router = APIRouter(prefix="/dashboard", tags=["enterprise-dashboard"])


@router.get("/overview")
async def overview() -> dict:
    return success(service.get_overview())
