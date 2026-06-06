from uuid import uuid4

from app.shared.mock_data import AGENTS

GLOBAL_AGENT_ENABLED = True


def list_agents(category: str | None = None) -> list[dict]:
    if category:
        return [item for item in AGENTS if item["category"] == category]
    return AGENTS


def get_agent(agent_id: int) -> dict | None:
    return next((item for item in AGENTS if item["id"] == agent_id), None)


def toggle_agent(agent_id: int, enabled: bool) -> dict | None:
    agent = get_agent(agent_id)
    if agent:
        agent["enabled"] = enabled
        agent["status"] = "standby" if enabled else "offline"
    return agent


def toggle_global(enabled: bool) -> dict:
    global GLOBAL_AGENT_ENABLED
    GLOBAL_AGENT_ENABLED = enabled
    return {"enabled": GLOBAL_AGENT_ENABLED}


def assign_task(agent_id: int, payload: dict) -> dict:
    return {
        "taskId": str(uuid4()),
        "agentId": agent_id,
        "status": "running",
        **payload,
    }
