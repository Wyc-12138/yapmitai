from typing import Any

from app.models import ModelConfig
from app.pages.enterprise.inquiry.agents.follow_up import FollowUpAgent
from app.pages.enterprise.inquiry.agents.inquiry_analyst import InquiryAnalystAgent
from app.pages.enterprise.inquiry.agents.smart_cs import SmartCSAgent


class InquiryWorkflow:
    def __init__(self, model_config: ModelConfig | None = None) -> None:
        self.analyst = InquiryAnalystAgent(model_config)
        self.smart_cs = SmartCSAgent(model_config)
        self.follow_up = FollowUpAgent(model_config)

    async def run(self, inquiry_text: str, source: str = "WhatsApp") -> dict[str, Any]:
        result: dict[str, Any] = {
            "inquiry": inquiry_text,
            "source": source,
            "steps": [],
            "status": "running",
        }

        analyst_result = await self.analyst.run(
            {"inquiry_text": inquiry_text, "source": source}
        )
        result["steps"].append(
            {"agent": "inquiry_analyst", "output": analyst_result.result}
        )
        if not analyst_result.success:
            result["status"] = "error"
            result["error"] = analyst_result.error
            return result

        smart_cs_result = await self.smart_cs.run(
            {
                "inquiry_text": inquiry_text,
                "intent": analyst_result.result.get("intent", ""),
                "language": analyst_result.result.get("language", "English"),
            }
        )
        result["steps"].append({"agent": "smart_cs", "output": smart_cs_result.result})
        if not smart_cs_result.success:
            result["status"] = "error"
            result["error"] = smart_cs_result.error
            return result

        urgency = analyst_result.result.get("urgency_score", 3)
        try:
            urgency = int(urgency)
        except (TypeError, ValueError):
            urgency = 3

        follow_up_result = await self.follow_up.run(
            {
                "intent": analyst_result.result.get("intent", ""),
                "urgency": urgency,
                "reply_content": smart_cs_result.result.get("reply", ""),
                "language": analyst_result.result.get("language", "English"),
            }
        )
        result["steps"].append({"agent": "follow_up", "output": follow_up_result.result})
        if not follow_up_result.success:
            result["status"] = "error"
            result["error"] = follow_up_result.error
            return result

        result["status"] = "done"
        result["summary"] = {
            "intent": analyst_result.result.get("intent"),
            "language": analyst_result.result.get("language"),
            "urgency": urgency,
            "needHuman": analyst_result.result.get("need_human", False),
            "briefSummary": analyst_result.result.get("brief_summary"),
            "suggestedReply": smart_cs_result.result.get("reply"),
            "followUpPlan": follow_up_result.result.get("follow_up_plan"),
            "priority": follow_up_result.result.get("priority"),
            "strategyNote": follow_up_result.result.get("strategy_note"),
        }
        return result
