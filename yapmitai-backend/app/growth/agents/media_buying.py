import json
from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service


class MediaBuyingAgent(BaseAgent):
    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        result = await growth_llm_service.complete_json(
            self.config.system_prompt
            or "你是广告投放专家。输出 JSON：budget_plan, audience, channel_mix, ab_testing, roi_prediction。",
            f"产品：{agent_input.product}\n市场：{agent_input.market}\n预算：{agent_input.budget}\n"
            f"现有方案：{json.dumps(context, ensure_ascii=False)}",
            0.3,
            self.config.chat_model_config,
        )
        return self.success(result)
