import json
from typing import Any

from app.growth.agents.base import BaseAgent
from app.growth.schemas import AgentInput, AgentOutput
from app.growth.services.llm import growth_llm_service

_CONTENT_COUNTS = {
    "tiktok": 10,
    "facebook": 10,
    "instagram": 10,
    "xiaohongshu": 10,
    "email": 5,
}


def _list_field(value: Any, expected: int) -> list[str]:
    items = [str(item) for item in (value or []) if str(item).strip()]
    return items[:expected]


def _text_length(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False))


def _counts_satisfied(result: dict[str, Any]) -> bool:
    return all(len(result.get(key) or []) >= count for key, count in _CONTENT_COUNTS.items())


class ContentCreatorAgent(BaseAgent):
    agent_name = "AI Content Creator"

    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        brand_strategy = context.get("brand_strategy") or {}
        if not brand_strategy:
            raise ValueError("Content Creator requires brand_strategy in workflow context")
        system_prompt = (
            "你是 AI Content Creator。根据品牌方案生成营销内容 JSON。"
            "字段：tiktok, facebook, instagram, xiaohongshu, email。"
            "tiktok/facebook/instagram/xiaohongshu 各 10 条，email 5 条。"
            "支持中英文双语内容（每条可含 English 版本）。"
            "内容总量不少于 5000 字。不要输出占位或空条目。"
        )
        user_prompt = (
            f"产品：{agent_input.product}\n"
            f"目标市场：{agent_input.market}\n"
            f"品牌方案：{json.dumps(brand_strategy, ensure_ascii=False)}"
        )
        result = await growth_llm_service.complete_json(system_prompt, user_prompt, temperature=0.55)
        result = self._normalize(result)
        if _text_length(result) < 5000 or not _counts_satisfied(result):
            expanded = await growth_llm_service.complete_json(
                (
                    "扩充营销内容 JSON，tiktok/facebook/instagram/xiaohongshu 各 10 条、"
                    "email 5 条，总字数不少于 5000 字，支持中英文，不要占位内容。"
                ),
                json.dumps(result, ensure_ascii=False),
                temperature=0.45,
            )
            result = self._normalize(expanded)
        return self.success(result)

    @staticmethod
    def _normalize(result: dict[str, Any]) -> dict[str, Any]:
        return {
            "tiktok": _list_field(result.get("tiktok"), _CONTENT_COUNTS["tiktok"]),
            "facebook": _list_field(result.get("facebook"), _CONTENT_COUNTS["facebook"]),
            "instagram": _list_field(result.get("instagram"), _CONTENT_COUNTS["instagram"]),
            "xiaohongshu": _list_field(result.get("xiaohongshu"), _CONTENT_COUNTS["xiaohongshu"]),
            "email": _list_field(result.get("email"), _CONTENT_COUNTS["email"]),
        }
