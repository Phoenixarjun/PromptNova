from abc import ABC, abstractmethod
from typing import Any


class EvaluateAgent(ABC):
    """Abstract base class for all evaluation agents."""

    def __init__(self, llm: Any):
        self.llm = llm

    @abstractmethod
    async def evaluate(self, *args, **kwargs) -> Any:
        """Runs the evaluation for the specific agent."""
        pass