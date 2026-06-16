import json
from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service


class ContentCreatorAgent(BaseAgent):
    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        result = await growth_llm_service.complete_json(
            self.config.system_prompt
            or "你是内容创作专家。输出 JSON：tiktok, facebook, instagram, xiaohongshu, email。",
            f"产品：{agent_input.product}\n市场：{agent_input.market}\n"
            f"品牌策略：{json.dumps(context.get('brand_strategy', {}), ensure_ascii=False)}",
            0.55,
            self.config.chat_model_config,
        )
        return self.success(result)
