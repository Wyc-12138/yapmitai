from fastapi import APIRouter

from app.core.responses import success
from .. import service
from ..schema import PersonalWxMessage

router = APIRouter(prefix="/personalwx", tags=["personalwx-agent"])


@router.post("/webhook")
async def personalwx_webhook(payload: PersonalWxMessage) -> dict:
    return success(await service.reply(payload.model_dump()))
