from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Prism(PromptAgent):
    """Agent for PRISM Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using PRISM framework."""
        prism_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the PRISM framework for a creative and multifaceted prompt: Perspective (e.g., optimistic, critical), Role (e.g., expert, marketer), Input (the data or context provided), Style (tone, format, voice), and Medium (e.g., blog, tweet, script).

User Input: {user_input}"""
        )
        chain = prism_template | self.llm
        return chain.invoke({"user_input": user_input}).content