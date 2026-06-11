from typing import Any, TypedDict

from app.growth.schemas import AgentInput


class WorkflowState(TypedDict, total=False):
    task_id: str
    agent_input: AgentInput
    market_report: dict[str, Any]
    brand_strategy: dict[str, Any]
    content_assets: dict[str, Any]
    media_plan: dict[str, Any]
    agent_outputs: list[dict[str, Any]]
    current_step: str
