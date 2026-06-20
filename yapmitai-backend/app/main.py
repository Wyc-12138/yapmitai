import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.responses import failure, success
from app.middleware.auth import ApiKeyMiddleware
from app.middleware.call_logging import CallLoggingMiddleware
from app.pages import api_router
from app.db.database import init_database

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_database()
    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="YAPMITAI Demo 2.0 Agent Gateway backend",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CallLoggingMiddleware)
app.add_middleware(ApiKeyMiddleware)
app.include_router(api_router, prefix=settings.api_v1_prefix)

# Serve generated media files (images / videos)
_generated_dir = os.path.abspath(settings.generated_media_dir)
os.makedirs(_generated_dir, exist_ok=True)
app.mount("/generated", StaticFiles(directory=_generated_dir), name="generated_media")


@app.exception_handler(AppError)
async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=failure(exc.code, exc.message, status_code=exc.status_code),
    )


@app.exception_handler(StarletteHTTPException)
async def handle_http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=failure(exc.status_code, str(exc.detail), status_code=exc.status_code),
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=failure(10422, "请求参数校验失败", exc.errors(), status_code=422),
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=failure(10500, "服务器内部错误", status_code=500),
    )


@app.get("/health", tags=["system"])
async def health() -> dict:
    return success(
        {
            "status": "healthy",
            "environment": settings.app_env,
            "gateway": settings.agent_gateway_url,
        }
    )
