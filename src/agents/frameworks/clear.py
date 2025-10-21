from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Clear(PromptAgent):
    """Agent for CLEAR Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using CLEAR framework."""
        clear_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the CLEAR framework: ensure the prompt is Concise (complete but not wordy), Logical (ordered correctly), Explicit (no assumptions), Actionable (the AI can do it), and Relevant (related to the outcome). The final prompt must be sharp and executable.

User Input: {user_input}"""
        )
        chain = clear_template | self.llm
        return chain.invoke({"user_input": user_input}).content