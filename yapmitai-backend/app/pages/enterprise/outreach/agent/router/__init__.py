from fastapi import APIRouter

from app.core.exceptions import InvalidParameterError
from app.core.responses import success
from .. import service
from ..schema import CallTaskRequest, LeadSearchRequest

router = APIRouter(prefix="/outreach", tags=["outreach-agent"])


@router.post("/leads")
async def search_leads(payload: LeadSearchRequest) -> dict:
    return success(await service.search_leads(payload.model_dump()))


@router.post("/calls")
async def create_call_task(payload: CallTaskRequest) -> dict:
    if not payload.consentFlag:
        raise InvalidParameterError("consentFlag must be true for outbound calls")
    return success(await service.create_call_task(payload.model_dump()))
