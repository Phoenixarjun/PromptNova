from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class TreeOfThought(PromptAgent):
    """Agent for Tree of Thoughts Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, branches: int = 3, **kwargs) -> str:
        """Refines the user input using Tree of Thoughts prompting."""
        tot_template = PromptTemplate(
            input_variables=["user_input", "branches"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. Your task is to create a refined version of the given user input that meets these criteria. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use tree-of-thought prompting: instruct the AI to explore {branches} branching reasoning paths (e.g., creative, analytical, practical), evaluate them, and select the best for the final output. Ensure the branches are detailed and lead to an optimized, high-quality response.

User Input: {user_input}"""
        )
        chain = tot_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "branches": branches
        }).content