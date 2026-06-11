import json
from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service
from app.growth.services.tavily_search import tavily_search_service


def _text_length(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False))


class MarketAnalystAgent(BaseAgent):
    agent_name = "AI Market Analyst"

    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        search_query = f"{agent_input.product} market size trends competitors {agent_input.market}"
        search_results = await tavily_search_service.search(search_query)
        search_context = "\n".join(
            f"- {item.get('title', '')}: {item.get('content', '')}"
            for item in search_results[:8]
        )
        system_prompt = (
            "你是 AI Market Analyst。根据产品与目标市场输出标准化市场分析报告 JSON。"
            "字段必须包含：market_size, industry_trend, target_customer, top_competitors, opportunities。"
            "top_competitors 必须是 10 个对象的数组，每个含 name 与 summary。"
            "opportunities 为字符串数组。"
            "所有文本字段使用中文，总字数不少于 1500 字。"
            "必须覆盖：市场规模、用户画像、行业趋势、TOP10竞品、市场机会。"
        )
        user_prompt = (
            f"产品：{agent_input.product}\n"
            f"目标国家/市场：{agent_input.market}\n"
            f"目标用户：{agent_input.target_customer}\n"
            f"预算参考：{agent_input.budget}\n\n"
            f"Tavily 搜索结果：\n{search_context or '暂无外部搜索数据，请基于行业常识分析。'}"
        )
        result = await growth_llm_service.complete_json(system_prompt, user_prompt, temperature=0.25)
        result = self._normalize(result, agent_input)
        if _text_length(result) < 1500 or len(result["top_competitors"]) < 10:
            result = await self._expand(result, agent_input, search_context)
        return self.success(result)

    def _normalize(self, result: dict[str, Any], agent_input: AgentInput) -> dict[str, Any]:
        competitors = result.get("top_competitors") or []
        if isinstance(competitors, list):
            competitors = [
                {
                    "name": str(item.get("name", "")).strip(),
                    "summary": str(item.get("summary", "")).strip(),
                }
                for item in competitors
                if isinstance(item, dict) and str(item.get("name", "")).strip()
            ]
            competitors = competitors[:10]
        else:
            competitors = []
        return {
            "market_size": str(result.get("market_size", "")),
            "industry_trend": str(result.get("industry_trend", "")),
            "target_customer": str(result.get("target_customer", agent_input.target_customer)),
            "top_competitors": competitors,
            "opportunities": list(result.get("opportunities") or []),
        }

    async def _expand(
        self,
        result: dict[str, Any],
        agent_input: AgentInput,
        search_context: str,
    ) -> dict[str, Any]:
        expanded = await growth_llm_service.complete_json(
            (
                "扩充市场分析报告 JSON，保持字段结构不变，总字数不少于 1500 字，"
                "top_competitors 必须包含 10 个真实竞品对象（name + summary），不要用占位内容。"
            ),
            f"原始报告：{json.dumps(result, ensure_ascii=False)}\n"
            f"产品：{agent_input.product}\n市场：{agent_input.market}\n"
            f"搜索：{search_context}",
            temperature=0.2,
        )
        return self._normalize(expanded, agent_input)
