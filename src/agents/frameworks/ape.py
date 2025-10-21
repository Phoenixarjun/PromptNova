from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Ape(PromptAgent):
    """Agent for APE Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using APE framework."""
        ape_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the APE framework: Action (define the task), Purpose (state the goal), Expectation (specify output requirements). Ensure the refined prompt incorporates all elements for focused, no-nonsense results.

User Input: {user_input}"""
        )
        chain = ape_template | self.llm
        return chain.invoke({"user_input": user_input}).content