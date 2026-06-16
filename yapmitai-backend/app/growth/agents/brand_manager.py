import json
from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service


class BrandManagerAgent(BaseAgent):
    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        result = await growth_llm_service.complete_json(
            self.config.system_prompt
            or "你是品牌营销经理。输出 JSON：positioning, slogan, usp, competitive_advantage, channel_strategy, growth_strategy。",
            f"产品：{agent_input.product}\n市场：{agent_input.market}\n"
            f"市场报告：{json.dumps(context.get('market_report', {}), ensure_ascii=False)}",
            0.35,
            self.config.chat_model_config,
        )
        return self.success(result)
