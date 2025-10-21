from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Craft(PromptAgent):
    """Agent for CRAFT Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using CRAFT framework."""
        craft_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the CRAFT framework: Capability (define AI's expertise), Role (assign persona), Action (specify task), Format (set output structure), Tone (define voice). Ensure the refined prompt incorporates all elements for precise, high-stakes results.

User Input: {user_input}"""
        )
        chain = craft_template | self.llm
        return chain.invoke({"user_input": user_input}).content