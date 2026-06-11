from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.database import get_db
from .. import service
from ..schema import AllianceMemberCreate

router = APIRouter(prefix="/alliance", tags=["alliance-dashboard"])


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.get_dashboard(db))


@router.post("/members")
async def create_member(
    payload: AllianceMemberCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.create_member(db, payload.model_dump()))
