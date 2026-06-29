from typing import Any

from app.pages.enterprise.inquiry.agents.base import BaseInquiryAgent


class InquiryAnalystAgent(BaseInquiryAgent):
    NAME = "inquiry_analyst"
    PROMPT_FILE = "inquiry_analyst.txt"

    def _prepare_vars(self, input_data: dict[str, Any]) -> dict[str, Any]:
        return {
            "inquiry_text": input_data.get("inquiry_text", ""),
            "source": input_data.get("source", "WhatsApp"),
        }
