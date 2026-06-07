from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.postgres import get_db
from .. import service
from ..schema import TalentAssistantRequest

router = APIRouter(prefix="/talent", tags=["talent-workspace"])


@router.get("/home")
async def home(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.get_home(db))


@router.post("/assistant")
async def call_assistant(
    payload: TalentAssistantRequest, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.call_assistant(db, payload.assistant, payload.prompt))
