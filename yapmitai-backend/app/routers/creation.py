from fastapi import APIRouter

from app.core.responses import success
from app.schemas.creation import ImageCreateRequest, VideoCreateRequest
from app.services import creation

router = APIRouter(prefix="/creation", tags=["creation-agent"])


@router.post("/image")
async def create_image(payload: ImageCreateRequest) -> dict:
    return success(await creation.create_image(payload.model_dump()))


@router.post("/video")
async def create_video(payload: VideoCreateRequest) -> dict:
    return success(await creation.create_video(payload.model_dump()))


@router.get("/video/{task_id}")
async def get_video_status(task_id: str) -> dict:
    return success(creation.video_status(task_id))
