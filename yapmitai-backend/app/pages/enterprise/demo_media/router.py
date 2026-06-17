"""Demo media router — text-to-image / text-to-video endpoints."""

import httpx
from fastapi import APIRouter, HTTPException

from app.core.responses import success
from . import service
from .schema import (
    TextToImageRequest,
    TextToVideoRequest,
)

router = APIRouter(prefix="/demo-media", tags=["demo-media"])


def _api_error(exc: Exception) -> HTTPException:
    if isinstance(exc, httpx.HTTPStatusError):
        detail = f"外部API错误 ({exc.response.status_code})"
        try:
            body = exc.response.json()
        except Exception:
            body = {}
        msg = body.get("message") or body.get("error", {}).get("message") or str(exc)
        detail = f"{detail}: {msg}"
        return HTTPException(status_code=502, detail=detail)
    return HTTPException(status_code=503, detail=str(exc))


@router.post("/text-to-image")
async def text_to_image(payload: TextToImageRequest) -> dict:
    try:
        results = await service.text_to_image(
            prompt=payload.prompt,
            size=payload.size,
            style=payload.style,
            quantity=payload.quantity,
        )
    except (RuntimeError, httpx.HTTPError) as exc:
        raise _api_error(exc) from exc
    return success(results)


@router.post("/text-to-video")
async def text_to_video(payload: TextToVideoRequest) -> dict:
    try:
        result = await service.text_to_video(
            prompt=payload.prompt,
            ratio=payload.ratio,
            duration=payload.duration,
            style=payload.style,
        )
    except (RuntimeError, httpx.HTTPError) as exc:
        raise _api_error(exc) from exc
    return success(result)


@router.get("/video-status/{task_id}")
async def video_status(task_id: str) -> dict:
    result = service.get_video_status(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Video task not found")
    return success(result)
