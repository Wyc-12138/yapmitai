from fastapi import APIRouter

from app.core.responses import success
from app.schemas.alliance import AllianceMemberCreate
from app.services import alliance

router = APIRouter(prefix="/alliance", tags=["alliance-dashboard"])


@router.get("/dashboard")
async def dashboard() -> dict:
    return success(alliance.get_dashboard())


@router.post("/members")
async def create_member(payload: AllianceMemberCreate) -> dict:
    return success(alliance.create_member(payload.model_dump()))
