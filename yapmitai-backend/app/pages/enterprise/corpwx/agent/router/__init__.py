from fastapi import APIRouter

from app.core.responses import success
from .. import service
from ..schema import CorpWxMessage

router = APIRouter(prefix="/corpwx", tags=["corpwx-agent"])


@router.post("/webhook")
async def corpwx_webhook(payload: CorpWxMessage) -> dict:
    return success(await service.reply(payload.model_dump()))
