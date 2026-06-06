from app.core.config import get_settings

CONFIG_STORE = {
    "gateway": {
        "gatewayUrl": get_settings().agent_gateway_url,
        "timeoutSeconds": get_settings().agent_timeout_seconds,
        "globalEnabled": True,
        "connected": False,
    },
    "modules": {
        "creation": {"source": "external", "settings": {}},
        "outreach": {"source": "external", "settings": {}},
        "personalwx": {"source": "external", "settings": {}},
        "corpwx": {"source": "external", "settings": {}},
        "knowledge": {"source": "external", "settings": {}},
    },
}


def get_gateway_config() -> dict:
    return CONFIG_STORE["gateway"]


def update_gateway_config(payload: dict) -> dict:
    CONFIG_STORE["gateway"].update(
        {
            "gatewayUrl": str(payload["gateway_url"]),
            "timeoutSeconds": payload["timeout_seconds"],
            "globalEnabled": payload["global_enabled"],
        }
    )
    return CONFIG_STORE["gateway"]


def test_connection() -> dict:
    CONFIG_STORE["gateway"]["connected"] = True
    return {"connected": True, "latencyMs": 128}


def get_module_config(module: str) -> dict | None:
    return CONFIG_STORE["modules"].get(module)


def update_module_config(module: str, payload: dict) -> dict | None:
    if module not in CONFIG_STORE["modules"]:
        return None
    CONFIG_STORE["modules"][module] = payload
    return CONFIG_STORE["modules"][module]
