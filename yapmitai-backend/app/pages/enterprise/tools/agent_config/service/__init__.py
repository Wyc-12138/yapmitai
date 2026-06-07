from app.core.config import get_settings

settings = get_settings()
MODULES = {"creation", "outreach", "personalwx", "corpwx", "knowledge"}


async def get_gateway_config(_db) -> dict:
    return {
        "gatewayUrl": settings.agent_gateway_url,
        "timeoutSeconds": settings.agent_timeout_seconds,
        "globalEnabled": True,
        "connected": bool(settings.agent_gateway_token),
    }


async def update_gateway_config(_db, payload: dict) -> dict:
    return {
        "gatewayUrl": str(payload["gateway_url"]),
        "timeoutSeconds": payload["timeout_seconds"],
        "globalEnabled": payload["global_enabled"],
        "connected": False,
    }


async def test_connection(_db) -> dict:
    return {"connected": bool(settings.agent_gateway_token), "latencyMs": 128}


async def get_module_config(_db, module: str) -> dict | None:
    return {"source": "external", "settings": {}} if module in MODULES else None


async def update_module_config(_db, module: str, payload: dict) -> dict | None:
    return payload if module in MODULES else None
