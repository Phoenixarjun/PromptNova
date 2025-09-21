from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class ChainOfVerification(PromptAgent):
    """Agent for Chain-of-Verification (CoVe) Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Chain-of-Verification prompting."""
        cove_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Chain-of-Verification (CoVe) method: instruct the AI to first generate a baseline response, then devise a verification plan to check its own work for factual accuracy and logical consistency, and finally, produce a refined, verified final answer based on the verification results.

User Input: {user_input}"""
        )
        chain = cove_template | self.llm
        return chain.invoke({"user_input": user_input}).content