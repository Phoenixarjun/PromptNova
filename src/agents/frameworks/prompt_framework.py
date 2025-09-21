from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class PromptFramework(PromptAgent):
    """Agent for PROMPT Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using PROMPT framework."""
        prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the PROMPT framework: Purpose (define the outcome), Role (assign an expert persona), Output (clarify the desired format), Mode (specify the context like chat or report), Parameters (add constraints like length), and Tone (set the desired voice). Ensure the refined prompt is comprehensive and structured.

User Input: {user_input}"""
        )
        chain = prompt_template | self.llm
        return chain.invoke({"user_input": user_input}).content