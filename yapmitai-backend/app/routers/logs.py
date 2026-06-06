from fastapi import APIRouter

from app.core.responses import success
from app.services import logs

router = APIRouter(tags=["logs-and-stats"])


@router.get("/logs")
async def get_logs(status: str | None = None, module: str | None = None) -> dict:
    return success(logs.list_logs(status, module))


@router.get("/stats/overview")
async def stats_overview() -> dict:
    return success(logs.stats())


@router.get("/stats/trend")
async def stats_trend() -> dict:
    return success(
        [
            {"day": "Mon", "calls": 720},
            {"day": "Tue", "calls": 810},
            {"day": "Wed", "calls": 900},
            {"day": "Thu", "calls": 1040},
            {"day": "Fri", "calls": 1180},
            {"day": "Sat", "calls": 1210},
            {"day": "Sun", "calls": 1248},
        ]
    )


@router.get("/stats/distribution")
async def stats_distribution() -> dict:
    return success(
        [
            {"module": "creation", "value": 32},
            {"module": "customer-service", "value": 24},
            {"module": "outreach", "value": 19},
            {"module": "analytics", "value": 15},
            {"module": "knowledge", "value": 10},
        ]
    )
