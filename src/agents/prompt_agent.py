from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import config

class PromptAgent(ABC):
    """Abstract base class for all prompt refinement agents."""
    
    def __init__(self, model_name: str = "gemini-1.5-flash", model_provider: str = "google"):
        """Initializes the Gemini LLM."""
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.7
        )
    
    @abstractmethod
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input into an effective prompt based on the technique."""
        pass