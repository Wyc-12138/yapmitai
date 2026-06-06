from fastapi import APIRouter, HTTPException

from app.core.responses import success
from .. import service
from ..schema import KnowledgeQuery, KnowledgeSyncRequest

router = APIRouter(prefix="/knowledge", tags=["knowledge-agent"])


@router.post("/sync")
async def sync(payload: KnowledgeSyncRequest) -> dict:
    return success(service.start_sync(payload.sources))


@router.get("/sync/{task_id}")
async def sync_status(task_id: str) -> dict:
    result = service.sync_status(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sync task not found")
    return success(result)


@router.get("/status")
async def status() -> dict:
    return success(service.status())


@router.post("/query")
async def query(payload: KnowledgeQuery) -> dict:
    return success(service.query(payload.query, payload.limit))
