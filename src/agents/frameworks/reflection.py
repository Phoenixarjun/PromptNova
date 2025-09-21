from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Reflection(PromptAgent):
    """Agent for Reflection Pattern Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Reflection Pattern framework."""
        reflection_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the Reflection Pattern framework: instruct the AI to generate an initial response, then reflect on it to identify weaknesses, revise, and improve accuracy and quality. Ensure the refined prompt incorporates self-assessment for high-quality outputs.

User Input: {user_input}"""
        )
        chain = reflection_template | self.llm
        return chain.invoke({"user_input": user_input}).content