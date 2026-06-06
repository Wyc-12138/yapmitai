from fastapi import APIRouter

from app.core.responses import success
from .. import service
from ..schema import TalentAssistantRequest

router = APIRouter(prefix="/talent", tags=["talent-workspace"])


@router.get("/home")
async def home() -> dict:
    return success(service.get_home())


@router.post("/assistant")
async def call_assistant(payload: TalentAssistantRequest) -> dict:
    return success(service.call_assistant(payload.assistant, payload.prompt))
