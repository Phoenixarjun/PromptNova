from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class ScaffoldedPrompting(PromptAgent):
    """Agent for Scaffolded / Progressive Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Scaffolded Prompting."""
        scaffold_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Scaffolded/Progressive Prompting: instruct the AI to break down a complex task into a series of small, incremental, and interconnected steps. Each step should build upon the last, providing a clear "scaffold" that guides the model to a reliable and complete solution, reducing cognitive load.

User Input: {user_input}"""
        )
        chain = scaffold_template | self.llm
        return chain.invoke({"user_input": user_input}).content