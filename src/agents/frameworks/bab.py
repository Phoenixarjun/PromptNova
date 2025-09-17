from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class Bab(PromptAgent):
    """Agent for Before-After-Bridge (BAB) Framework."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Before-After-Bridge (BAB) framework."""
        bab_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the Before-After-Bridge (BAB) framework: Before (describe the current state), After (outline the desired state), Bridge (explain how to transition). Ensure the refined prompt incorporates all elements for persuasive, problem-solving outputs.

User Input: {user_input}"""
        )
        chain = bab_template | self.llm
        return chain.invoke({"user_input": user_input}).content