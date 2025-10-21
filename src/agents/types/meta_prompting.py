from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class MetaPrompting(PromptAgent):
    """Agent for Meta Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, iterations: int = 2, **kwargs) -> str:
        """Refines the user input using Meta Prompting."""
        meta_prompting_template = PromptTemplate(
            input_variables=["user_input", "iterations"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use meta prompting: instruct the AI to generate and refine its own prompt over {iterations} iterations, creating a meta-layer for optimization.

User Input: {user_input}"""
        )
        chain = meta_prompting_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "iterations": iterations
        }).content