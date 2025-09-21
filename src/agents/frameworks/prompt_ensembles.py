from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class PromptEnsembles(PromptAgent):
    """Agent for Prompt Ensembles Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Prompt Ensembles framework."""
        prompt_ensembles_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Prompt Ensembles framework: instruct the AI to generate multiple diverse responses by applying several different strategies or perspectives in parallel. Then, it should merge, weight, or select from these outputs to create a final, more robust and creative answer.

User Input: {user_input}"""
        )
        chain = prompt_ensembles_template | self.llm
        return chain.invoke({"user_input": user_input}).content