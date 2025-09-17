from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class ActivePrompt(PromptAgent):
    """Agent for Active-Prompt (Adaptive) Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Active-Prompt prompting."""
        active_prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Active-Prompt method: instruct the AI to devise a strategy to adapt its own prompting on the fly. This involves generating several prompt variations for the task, scoring them based on a defined metric (e.g., clarity, relevance), and selecting the highest-scoring prompt for execution.

User Input: {user_input}"""
        )
        chain = active_prompt_template | self.llm
        return chain.invoke({"user_input": user_input}).content