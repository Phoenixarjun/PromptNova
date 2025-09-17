from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class Grips(PromptAgent):
    """Agent for GRIPS Framework."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using GRIPS framework."""
        grips_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt for complex reasoning tasks, optimized for large language models. Use the GRIPS framework: Goal (clearly state the objective), Role (assign a persona), Input (supply relevant data), Process (describe the thinking steps), and Scope (define the limits like time or length).

User Input: {user_input}"""
        )
        chain = grips_template | self.llm
        return chain.invoke({"user_input": user_input}).content