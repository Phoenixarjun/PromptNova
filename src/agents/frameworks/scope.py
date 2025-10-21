from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Scope(PromptAgent):
    """Agent for SCOPE Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using SCOPE framework."""
        scope_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt for planning larger workflows, optimized for large language models. Use the SCOPE framework: Situation (describe the context/problem), Constraints (list limitations), Objectives (state desired outcomes), Persona (assign a role), and Execution (instruct how to produce the answer, including steps and format).

User Input: {user_input}"""
        )
        chain = scope_template | self.llm
        return chain.invoke({"user_input": user_input}).content