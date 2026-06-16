from abc import ABC, abstractmethod
from typing import Any

from app.growth.schemas import AgentInput, AgentOutput
from app.models import Agent


class BaseAgent(ABC):
    agent_name: str

    def __init__(self, config: Agent) -> None:
        self.config = config
        self.agent_name = config.name

    @abstractmethod
    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        """Run one isolated agent step."""

    def success(self, result: dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.agent_name, result=result)
