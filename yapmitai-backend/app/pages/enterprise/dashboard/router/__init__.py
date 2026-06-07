from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.postgres import get_db
from .. import service

router = APIRouter(prefix="/dashboard", tags=["enterprise-dashboard"])


@router.get("/overview")
async def overview(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.get_overview(db))
