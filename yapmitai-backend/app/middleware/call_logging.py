import time
from datetime import UTC, datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.database import AsyncSessionLocal
from app.models import AgentCallLog


class CallLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        started_at = datetime.now(UTC)
        started = time.perf_counter()
        response = await call_next(request)
        latency_ms = round((time.perf_counter() - started) * 1000)
        if "/api/v1/" in request.url.path:
            path_parts = request.url.path.split("/")
            module = path_parts[3] if len(path_parts) > 3 else "system"
            try:
                async with AsyncSessionLocal() as session:
                    session.add(
                        AgentCallLog(
                            agent_id="http-api",
                            module=module,
                            path=request.url.path,
                            method=request.method,
                            request_at=started_at,
                            response_at=datetime.now(UTC),
                            status="success" if response.status_code < 400 else "failed",
                            latency_ms=latency_ms,
                            cost=0,
                        )
                    )
                    await session.commit()
            except Exception:
                pass
        response.headers["X-Trace-Latency-Ms"] = str(latency_ms)
        return response
