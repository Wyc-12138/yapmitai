from app.services.mock_data import TOOLS


def list_tools(category: str | None = None) -> list[dict]:
    return [item for item in TOOLS if not category or item["category"] == category]


def toggle_tool(tool_id: int, enabled: bool) -> dict | None:
    tool = next((item for item in TOOLS if item["id"] == tool_id), None)
    if tool:
        tool["enabled"] = enabled
    return tool
