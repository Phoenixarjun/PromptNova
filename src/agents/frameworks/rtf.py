from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Rtf(PromptAgent):
    """Agent for RTF Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using RTF framework."""
        rtf_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the RTF framework: Role (assign a persona), Task (define the action), Format (specify output structure). Ensure the refined prompt incorporates all elements for quick, structured, and effective results.

User Input: {user_input}"""
        )
        chain = rtf_template | self.llm
        return chain.invoke({"user_input": user_input}).content