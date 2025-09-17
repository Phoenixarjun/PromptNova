from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GOOGLE_API_KEY
from typing import Optional

class PromptAgent(ABC):
    """Abstract base class for all prompt refinement agents."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash", model_provider: str = "google", api_key: Optional[str] = None):
        """Initializes the Gemini LLM."""
        key_to_use = api_key 
        print(key_to_use)
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=key_to_use,
            temperature=0.7
        )
    
    @abstractmethod
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input into an effective prompt based on the technique."""
        pass


# from abc import ABC, abstractmethod
# # from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
# from src.config import GROQ_API_KEY

# class PromptAgent(ABC):
#     """Abstract base class for all prompt refinement agents."""

#     def __init__(self, model_name: str = "qwen/qwen3-32b", model_provider: str = "groq"):
#         """Initializes the Groq LLM."""
#         self.llm = ChatGroq(
#             model=model_name,
#             groq_api_key=GROQ_API_KEY,
#             temperature=0.7
#         )

#     def refine(self, user_input: str, **kwargs) -> str:
#         """Refines the user input into an effective prompt based on the technique."""
#         return self.llm.invoke(user_input).content
