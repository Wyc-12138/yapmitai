from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.core.responses import failure


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Browser CORS preflight requests do not carry application credentials.
        # Let CORSMiddleware validate and answer them before enforcing API keys.
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        protected = path.startswith(get_settings().api_v1_prefix) or path.startswith("/api/task")
        if protected:
            supplied_key = request.headers.get("X-API-Key")
            if supplied_key != get_settings().api_key:
                return JSONResponse(
                    status_code=401,
                    content=failure(401, "Unauthorized: invalid X-API-Key"),
                )
        return await call_next(request)
