from typing import Any

from langgraph.graph import END, START, StateGraph

from app.db.postgres import AsyncSessionLocal
from app.growth.agents import (
    BrandManagerAgent,
    ContentCreatorAgent,
    MarketAnalystAgent,
    MediaBuyingAgent,
)
from app.growth.schemas import AgentInput
from app.growth.workflow.state import WorkflowState
from app.models.growth_task import GrowthTask

_market_agent = MarketAnalystAgent()
_brand_agent = BrandManagerAgent()
_content_agent = ContentCreatorAgent()
_media_agent = MediaBuyingAgent()


async def _persist_step(state: WorkflowState, step: str, partial: dict[str, Any]) -> None:
    task_id = state.get("task_id")
    if not task_id:
        return
    async with AsyncSessionLocal() as session:
        task = await session.get(GrowthTask, task_id)
        if not task:
            return
        task.current_step = step
        context = dict(task.context or {})
        context.update(partial)
        task.context = context
        await session.commit()


def _context_from_state(state: WorkflowState) -> dict[str, Any]:
    return {
        "market_report": state.get("market_report") or {},
        "brand_strategy": state.get("brand_strategy") or {},
        "content_assets": state.get("content_assets") or {},
        "media_plan": state.get("media_plan") or {},
    }


async def _market_analyst_node(state: WorkflowState) -> dict[str, Any]:
    agent_input = state["agent_input"]
    output = await _market_agent.run(agent_input, _context_from_state(state))
    await _persist_step(state, "brand_manager", {"market_report": output.result})
    return {
        "market_report": output.result,
        "agent_outputs": [output.model_dump()],
        "current_step": "brand_manager",
    }


async def _brand_manager_node(state: WorkflowState) -> dict[str, Any]:
    agent_input = state["agent_input"]
    output = await _brand_agent.run(agent_input, _context_from_state(state))
    await _persist_step(state, "content_creator", {"brand_strategy": output.result})
    return {
        "brand_strategy": output.result,
        "agent_outputs": list(state.get("agent_outputs") or []) + [output.model_dump()],
        "current_step": "content_creator",
    }


async def _content_creator_node(state: WorkflowState) -> dict[str, Any]:
    agent_input = state["agent_input"]
    output = await _content_agent.run(agent_input, _context_from_state(state))
    await _persist_step(state, "media_buying", {"content_assets": output.result})
    return {
        "content_assets": output.result,
        "agent_outputs": list(state.get("agent_outputs") or []) + [output.model_dump()],
        "current_step": "media_buying",
    }


async def _media_buying_node(state: WorkflowState) -> dict[str, Any]:
    agent_input = state["agent_input"]
    output = await _media_agent.run(agent_input, _context_from_state(state))
    await _persist_step(state, "completed", {"media_plan": output.result})
    return {
        "media_plan": output.result,
        "agent_outputs": list(state.get("agent_outputs") or []) + [output.model_dump()],
        "current_step": "completed",
    }


def _build_growth_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("market_analyst", _market_analyst_node)
    graph.add_node("brand_manager", _brand_manager_node)
    graph.add_node("content_creator", _content_creator_node)
    graph.add_node("media_buying", _media_buying_node)
    graph.add_edge(START, "market_analyst")
    graph.add_edge("market_analyst", "brand_manager")
    graph.add_edge("brand_manager", "content_creator")
    graph.add_edge("content_creator", "media_buying")
    graph.add_edge("media_buying", END)
    return graph.compile()


_growth_graph = _build_growth_graph()


async def run_growth_workflow(agent_input: AgentInput) -> WorkflowState:
    initial_state: WorkflowState = {
        "task_id": agent_input.task_id,
        "agent_input": agent_input,
        "market_report": {},
        "brand_strategy": {},
        "content_assets": {},
        "media_plan": {},
        "agent_outputs": [],
        "current_step": "market_analyst",
    }
    return await _growth_graph.ainvoke(initial_state)
