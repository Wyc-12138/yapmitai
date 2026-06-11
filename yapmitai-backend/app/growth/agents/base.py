from abc import ABC, abstractmethod
from typing import Any

from app.growth.schemas import AgentInput, AgentOutput


class BaseAgent(ABC):
    agent_name: str

    @abstractmethod
    async def run(self, agent_input: AgentInput, context: dict[str, Any]) -> AgentOutput:
        """Execute agent logic. Agents must not call each other directly."""

    def success(self, result: dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.agent_name, status="success", result=result)
