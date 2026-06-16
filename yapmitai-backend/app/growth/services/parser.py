import re

from app.core.exceptions import AgentUnavailableError
from app.growth.schemas import AgentInput
from app.growth.services.llm import growth_llm_service


async def parse_prompt_to_input(task_id: str, prompt: str) -> AgentInput:
    text = prompt.strip()
    try:
        data = await growth_llm_service.complete_json(
            "从增长需求中提取 JSON 字段：product, market, target_customer, budget。",
            text,
            temperature=0.1,
        )
        return AgentInput(
            task_id=task_id,
            product=str(data.get("product", "")).strip(),
            market=str(data.get("market", "")).strip(),
            target_customer=str(data.get("target_customer", "潜在消费者")).strip(),
            budget=str(data.get("budget", "待评估")).strip(),
        )
    except AgentUnavailableError:
        pass

    match = re.search(r"卖到(.+?)(市场|国家|地区)?$", text)
    market = match.group(1).strip() if match else "目标市场"
    product = text.split("卖到")[0].replace("我要把", "").replace("把", "").strip()
    return AgentInput(
        task_id=task_id,
        product=product or text,
        market=market,
        target_customer="潜在消费者",
        budget="待评估",
    )
