from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class SkeletonOfThought(PromptAgent):
    """Agent for Skeleton-of-Thought (SoT) Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Skeleton-of-Thought prompting."""
        sot_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Skeleton-of-Thought (SoT) method: instruct the AI to first generate a concise skeleton or outline of the answer, and then proceed to expand on each point of the skeleton in a structured and detailed manner. This forces planning before generation.

User Input: {user_input}"""
        )
        chain = sot_template | self.llm
        return chain.invoke({"user_input": user_input}).content