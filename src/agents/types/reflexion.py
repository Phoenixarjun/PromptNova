from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Reflexion(PromptAgent):
    """Agent for Reflexion / Self-Refine Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Reflexion prompting."""
        reflexion_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Reflexion/Self-Refine method: instruct the AI to generate an initial response, then critically reflect on its own answer to identify flaws, inconsistencies, or areas for improvement, and finally, use that self-critique to produce a revised, higher-quality final answer.

User Input: {user_input}"""
        )
        chain = reflexion_template | self.llm
        return chain.invoke({"user_input": user_input}).content