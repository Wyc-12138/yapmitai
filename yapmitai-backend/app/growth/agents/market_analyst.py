from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service


class MarketAnalystAgent(BaseAgent):
    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        result = await growth_llm_service.complete_json(
            self.config.system_prompt
            or "你是市场分析师。输出 JSON：market_size, industry_trend, target_customer, top_competitors, opportunities。",
            f"产品：{agent_input.product}\n市场：{agent_input.market}\n"
            f"目标用户：{agent_input.target_customer}\n预算：{agent_input.budget}",
            0.25,
            self.config.chat_model_config,
        )
        return self.success(result)
