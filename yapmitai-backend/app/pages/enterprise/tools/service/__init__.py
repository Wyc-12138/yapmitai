from app.shared.mock_data import TOOLS


async def list_tools(_db, category: str | None = None) -> list[dict]:
    return [item for item in TOOLS if not category or item["category"] == category]


async def toggle_tool(_db, tool_id: int, enabled: bool) -> dict | None:
    tool = next((item for item in TOOLS if item["id"] == tool_id), None)
    if not tool:
        return None
    return {**tool, "enabled": enabled}
