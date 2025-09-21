from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class MaieuticPrompting(PromptAgent):
    """Agent for Maieutic Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Maieutic Prompting."""
        maieutic_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Maieutic (Socratic) Prompting: instruct the AI to ask clarifying questions to itself or the user to surface missing information and refine the problem space before providing a final, precise answer. This helps uncover hidden requirements.

User Input: {user_input}"""
        )
        chain = maieutic_template | self.llm
        return chain.invoke({"user_input": user_input}).content