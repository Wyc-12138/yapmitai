import json
from pathlib import Path
from typing import Any

from app.pages.enterprise.inquiry.agents.base import BaseInquiryAgent

PRODUCTS_PATH = Path(__file__).resolve().parent.parent / "data" / "products.json"


class SmartCSAgent(BaseInquiryAgent):
    NAME = "smart_cs"
    PROMPT_FILE = "smart_cs.txt"

    def _load_products(self) -> str:
        products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
        lines = []
        for product in products:
            lines.append(
                f"产品：{product['name']} | MOQ：{product['moq']} | "
                f"价格：{product['price']} | 材质：{product['material']} | "
                f"交期：{product['lead_time']}"
            )
        return "\n".join(lines)

    def _prepare_vars(self, input_data: dict[str, Any]) -> dict[str, Any]:
        return {
            "inquiry_text": input_data.get("inquiry_text", ""),
            "intent": input_data.get("intent", ""),
            "language": input_data.get("language", "English"),
            "products_info": self._load_products(),
        }
