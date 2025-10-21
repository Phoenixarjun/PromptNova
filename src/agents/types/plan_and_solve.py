from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class PlanAndSolve(PromptAgent):
    """Agent for Plan-and-Solve (PS) Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Plan-and-Solve prompting."""
        ps_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Plan-and-Solve (PS) method: instruct the AI to first create a detailed, step-by-step plan to address the user's request, and then execute that plan to generate the final, coherent response. This two-phase approach ensures deliberate reasoning.

User Input: {user_input}"""
        )
        chain = ps_template | self.llm
        return chain.invoke({"user_input": user_input}).content