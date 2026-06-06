from fastapi import APIRouter

from app.core.responses import success
from .. import service
from ..schema import ImageCreateRequest, VideoCreateRequest

router = APIRouter(prefix="/creation", tags=["creation-agent"])


@router.post("/image")
async def create_image(payload: ImageCreateRequest) -> dict:
    return success(await service.create_image(payload.model_dump()))


@router.post("/video")
async def create_video(payload: VideoCreateRequest) -> dict:
    return success(await service.create_video(payload.model_dump()))


@router.get("/video/{task_id}")
async def get_video_status(task_id: str) -> dict:
    return success(service.video_status(task_id))
