from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.growth.services.llm import growth_llm_service
from app.models import ModelConfig

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


@dataclass
class AgentResult:
    success: bool
    agent: str
    result: dict[str, Any]
    raw: str = ""
    error: str | None = None


class BaseInquiryAgent(ABC):
    NAME = ""
    PROMPT_FILE = ""

    def __init__(self, model_config: ModelConfig | None = None) -> None:
        self.model_config = model_config

    def _load_prompt(self) -> str:
        return (PROMPTS_DIR / self.PROMPT_FILE).read_text(encoding="utf-8")

    def _render(self, template: str, variables: dict[str, Any]) -> str:
        rendered = template
        for key, value in variables.items():
            rendered = rendered.replace(f"{{{key}}}", str(value))
        return rendered

    def _prepare_vars(self, input_data: dict[str, Any]) -> dict[str, Any]:
        return input_data

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        try:
            variables = self._prepare_vars(input_data)
            user_prompt = self._render(self._load_prompt(), variables)
            system_prompt = (
                "你是松南国际贸易的询盘 AI 助手。"
                "请严格输出合法 JSON 对象，不要输出 Markdown 或额外说明。"
            )
            result = await growth_llm_service.complete_json(
                system_prompt,
                user_prompt,
                0.3,
                self.model_config,
            )
            return AgentResult(True, self.NAME, result, raw=str(result))
        except Exception as exc:
            return AgentResult(False, self.NAME, {}, error=str(exc))
