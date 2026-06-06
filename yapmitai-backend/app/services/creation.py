from uuid import uuid4

from app.services.gateway import gateway_service


async def create_image(payload: dict) -> dict:
    return await gateway_service.call(
        "creation-image",
        payload,
        {"status": "completed", "imageUrl": "https://placehold.co/1024x1024/png", "cost": 0.42},
    )


async def create_video(payload: dict) -> dict:
    return await gateway_service.call(
        "creation-video",
        payload,
        {"status": "queued", "taskId": str(uuid4()), "progress": 0},
    )


def video_status(task_id: str) -> dict:
    return {"taskId": task_id, "status": "completed", "progress": 100, "videoUrl": "https://example.com/mock-video.mp4"}
