import re

from app.growth.schemas import AgentInput
from app.growth.services.llm import growth_llm_service


async def parse_prompt_to_input(task_id: str, prompt: str) -> AgentInput:
    text = prompt.strip()
    if growth_llm_service.configured:
        data = await growth_llm_service.complete_json(
            system_prompt=(
                "你是需求解析器。从用户一句话增长需求中提取结构化字段，"
                "返回 JSON：product, market, target_customer, budget。"
                "未提及的字段给出合理推断，budget 可写“待评估”。"
            ),
            user_prompt=text,
            temperature=0.1,
        )
        return AgentInput(
            task_id=task_id,
            product=str(data.get("product", "")).strip(),
            market=str(data.get("market", "")).strip(),
            target_customer=str(data.get("target_customer", "")).strip(),
            budget=str(data.get("budget", "待评估")).strip(),
        )
    return _heuristic_parse(task_id, text)


def _heuristic_parse(task_id: str, text: str) -> AgentInput:
    product = text
    market = ""
    match = re.search(r"卖到(.+?)(市场|国家|地区)?", text)
    if match:
        market = match.group(1).strip()
        product = text.split("卖到")[0].replace("我要把", "").replace("把", "").strip()
    return AgentInput(
        task_id=task_id,
        product=product or text,
        market=market or "目标市场",
        target_customer="潜在消费者",
        budget="待评估",
    )
