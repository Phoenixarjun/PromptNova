from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class GoalOrientedPrompting(PromptAgent):
    """Agent for Goal-Oriented Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Goal-Oriented Prompting."""
        goal_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Goal-Oriented Prompting: instruct the AI to frame its response around achieving a clearly stated goal. The prompt must include the primary objective, key success criteria, and any constraints, ensuring the AI's output is focused, measurable, and directly aligned with the desired outcome.

User Input: {user_input}"""
        )
        chain = goal_template | self.llm
        return chain.invoke({"user_input": user_input}).content