from typing import Any

from app.pages.enterprise.inquiry.agents.base import BaseInquiryAgent


class FollowUpAgent(BaseInquiryAgent):
    NAME = "follow_up"
    PROMPT_FILE = "follow_up.txt"

    def _prepare_vars(self, input_data: dict[str, Any]) -> dict[str, Any]:
        return {
            "intent": input_data.get("intent", ""),
            "urgency": input_data.get("urgency", 3),
            "reply_sent": input_data.get("reply_content", ""),
            "language": input_data.get("language", "English"),
        }
