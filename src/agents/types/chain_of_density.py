from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class ChainOfDensity(PromptAgent):
    """Agent for Chain-of-Density (CoD) Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Chain-of-Density prompting."""
        cod_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Chain-of-Density (CoD) method: instruct the AI to generate a summary that is progressively densified. It should start with a basic summary, then iteratively revise it to be more succinct and entity-rich without losing key information, resulting in a highly compressed yet comprehensive output.

User Input: {user_input}"""
        )
        chain = cod_template | self.llm
        return chain.invoke({"user_input": user_input}).content