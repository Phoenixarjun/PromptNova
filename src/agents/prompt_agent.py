from abc import ABC, abstractmethod
from typing import Any

class PromptAgent(ABC):
    """Abstract base class for all prompt refinement agents."""
    
    def __init__(self, llm: Any):
        """
        Initializes the agent with a language model.

        Args:
            llm: The language model instance to be used by the agent.
        """
        self.llm = llm

    @abstractmethod
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input into an effective prompt based on the technique."""
        pass
