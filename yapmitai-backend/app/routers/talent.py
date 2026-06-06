from fastapi import APIRouter

from app.core.responses import success
from app.schemas.talent import TalentAssistantRequest
from app.services import talent

router = APIRouter(prefix="/talent", tags=["talent-workspace"])


@router.get("/home")
async def home() -> dict:
    return success(talent.get_home())


@router.post("/assistant")
async def call_assistant(payload: TalentAssistantRequest) -> dict:
    return success(talent.call_assistant(payload.assistant, payload.prompt))
