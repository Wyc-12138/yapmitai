import json
from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service


def _text_length(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False))


class BrandManagerAgent(BaseAgent):
    agent_name = "AI Brand Marketing Manager"

    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        market_report = context.get("market_report") or {}
        if not market_report:
            raise ValueError("Brand Manager requires market_report in workflow context")
        system_prompt = (
            "你是 AI Brand Marketing Manager。根据市场分析报告制定品牌战略 JSON。"
            "字段：positioning, slogan, usp, competitive_advantage, channel_strategy, growth_strategy。"
            "必须输出品牌定位、品牌口号、核心卖点、竞争优势、渠道策略、增长策略。"
            "总字数不少于 1000 字，形成完整品牌战略文档。"
        )
        user_prompt = (
            f"产品：{agent_input.product}\n"
            f"目标市场：{agent_input.market}\n"
            f"市场分析报告：{json.dumps(market_report, ensure_ascii=False)}"
        )
        result = await growth_llm_service.complete_json(system_prompt, user_prompt, temperature=0.35)
        result = self._normalize(result)
        if _text_length(result) < 1000:
            expanded = await growth_llm_service.complete_json(
                "扩充品牌战略 JSON，字段不变，总字数不少于 1000 字。",
                json.dumps(result, ensure_ascii=False),
                temperature=0.25,
            )
            result = self._normalize(expanded)
        return self.success(result)

    @staticmethod
    def _normalize(result: dict[str, Any]) -> dict[str, Any]:
        return {
            "positioning": str(result.get("positioning", "")),
            "slogan": str(result.get("slogan", "")),
            "usp": str(result.get("usp", "")),
            "competitive_advantage": str(
                result.get("competitive_advantage", result.get("竞争优势", ""))
            ),
            "channel_strategy": str(result.get("channel_strategy", "")),
            "growth_strategy": str(result.get("growth_strategy", "")),
        }
