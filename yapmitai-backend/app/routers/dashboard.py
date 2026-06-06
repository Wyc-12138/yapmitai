from fastapi import APIRouter

from app.core.responses import success
from app.services import dashboard

router = APIRouter(prefix="/dashboard", tags=["enterprise-dashboard"])


@router.get("/overview")
async def overview() -> dict:
    return success(dashboard.get_overview())
