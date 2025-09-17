from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class Tcef(PromptAgent):
    """Agent for TCEF Framework."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using TCEF framework."""
        tcef_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the TCEF framework: Task (define the action), Context (provide background), Example (include a demonstration), Format (specify output structure). Ensure the refined prompt incorporates all elements for quick and effective results.

User Input: {user_input}"""
        )
        chain = tcef_template | self.llm
        return chain.invoke({"user_input": user_input}).content