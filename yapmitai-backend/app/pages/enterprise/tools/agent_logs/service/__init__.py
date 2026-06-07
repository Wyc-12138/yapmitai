from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AgentCallLog


def _log_dict(item: AgentCallLog) -> dict:
    return {
        "request_at": item.request_at.isoformat(),
        "response_at": item.response_at.isoformat() if item.response_at else None,
        "path": item.path,
        "method": item.method,
        "status": item.status,
        "latency_ms": item.latency_ms,
        "prompt_tokens": item.prompt_tokens,
        "completion_tokens": item.completion_tokens,
        "total_tokens": item.total_tokens,
        "cost": item.cost,
        "error_msg": item.error_msg,
    }


async def list_logs(
    db: AsyncSession, status: str | None = None, module: str | None = None
) -> list[dict]:
    statement = select(AgentCallLog).order_by(AgentCallLog.id.desc()).limit(200)
    if status:
        statement = statement.where(AgentCallLog.status == status)
    if module:
        statement = statement.where(AgentCallLog.module == module)
    return [_log_dict(item) for item in (await db.scalars(statement)).all()]


async def stats(db: AsyncSession) -> dict:
    total, successful, average, cost = (
        await db.execute(
            select(
                func.count(AgentCallLog.id),
                func.count(AgentCallLog.id).filter(AgentCallLog.status == "success"),
                func.avg(AgentCallLog.latency_ms),
                func.sum(AgentCallLog.cost),
            )
        )
    ).one()
    return {
        "calls": total,
        "successRate": round(successful / total * 100, 2) if total else 100,
        "averageLatencyMs": round(average or 0),
        "cost": float(cost or 0),
    }


async def trend(db: AsyncSession) -> list[dict]:
    return [
        {"day": "Mon", "calls": 720},
        {"day": "Tue", "calls": 810},
        {"day": "Wed", "calls": 900},
        {"day": "Thu", "calls": 1040},
        {"day": "Fri", "calls": 1180},
        {"day": "Sat", "calls": 1210},
        {"day": "Sun", "calls": 1248},
    ]


async def distribution(db: AsyncSession) -> list[dict]:
    return [
        {"module": "creation", "value": 32},
        {"module": "customer-service", "value": 24},
        {"module": "outreach", "value": 19},
        {"module": "analytics", "value": 15},
        {"module": "knowledge", "value": 10},
    ]
