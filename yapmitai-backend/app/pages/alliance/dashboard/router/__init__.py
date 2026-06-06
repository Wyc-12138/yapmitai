from fastapi import APIRouter

from app.core.responses import success
from .. import service
from ..schema import AllianceMemberCreate

router = APIRouter(prefix="/alliance", tags=["alliance-dashboard"])


@router.get("/dashboard")
async def dashboard() -> dict:
    return success(service.get_dashboard())


@router.post("/members")
async def create_member(payload: AllianceMemberCreate) -> dict:
    return success(service.create_member(payload.model_dump()))
