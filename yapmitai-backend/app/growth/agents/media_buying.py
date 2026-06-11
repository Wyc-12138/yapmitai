import json
from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service


class MediaBuyingAgent(BaseAgent):
    agent_name = "AI Media Buying Specialist"

    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        market_report = context.get("market_report") or {}
        brand_strategy = context.get("brand_strategy") or {}
        content_assets = context.get("content_assets") or {}
        if not market_report or not brand_strategy or not content_assets:
            raise ValueError(
                "Media Buying requires market_report, brand_strategy and content_assets"
            )
        system_prompt = (
            "你是 AI Media Buying Specialist。生成广告投放方案 JSON。"
            "字段：budget_plan, audience, channel_mix, ab_testing, roi_prediction。"
            "budget_plan 必须包含总预算拆分，以及 Meta、TikTok、Google 预算。"
            "audience 必须包含 age, gender, interests。"
            "ab_testing 为 A/B 测试策略数组。"
            "roi_prediction 必须包含 CTR, CPA, ROAS。"
        )
        user_prompt = (
            f"产品：{agent_input.product}\n"
            f"目标市场：{agent_input.market}\n"
            f"预算：{agent_input.budget}\n"
            f"市场报告：{json.dumps(market_report, ensure_ascii=False)}\n"
            f"品牌方案：{json.dumps(brand_strategy, ensure_ascii=False)}\n"
            f"内容资产：{json.dumps(content_assets, ensure_ascii=False)}"
        )
        result = await growth_llm_service.complete_json(system_prompt, user_prompt, temperature=0.3)
        return self.success(self._normalize(result, agent_input.budget))

    @staticmethod
    def _normalize(result: dict[str, Any], budget: str) -> dict[str, Any]:
        budget_plan = dict(result.get("budget_plan") or {})
        budget_plan.setdefault("total_budget", budget or "待评估")
        budget_plan.setdefault(
            "Meta预算",
            budget_plan.get("Meta预算") or budget_plan.get("meta_budget") or "待分配",
        )
        budget_plan.setdefault(
            "TikTok预算",
            budget_plan.get("TikTok预算") or budget_plan.get("tiktok_budget") or "待分配",
        )
        budget_plan.setdefault(
            "Google预算",
            budget_plan.get("Google预算") or budget_plan.get("google_budget") or "待分配",
        )
        audience = dict(result.get("audience") or {})
        audience.setdefault("age", "")
        audience.setdefault("gender", "")
        audience.setdefault("interests", [])
        roi_prediction = dict(result.get("roi_prediction") or {})
        roi_prediction.setdefault("CTR", "")
        roi_prediction.setdefault("CPA", "")
        roi_prediction.setdefault("ROAS", "")
        return {
            "budget_plan": budget_plan,
            "audience": audience,
            "channel_mix": dict(result.get("channel_mix") or {}),
            "ab_testing": list(result.get("ab_testing") or []),
            "roi_prediction": roi_prediction,
        }
