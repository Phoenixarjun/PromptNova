from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class AppFramework(PromptAgent):
    """Agent for APP Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using APP framework."""
        app_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt for short, transactional tasks, optimized for large language models. Use the APP framework: Ask (state exactly what you want), Provide (supply necessary context or examples), and Perform (instruct how to deliver the output, including format or next steps).

User Input: {user_input}"""
        )
        chain = app_template | self.llm
        return chain.invoke({"user_input": user_input}).content