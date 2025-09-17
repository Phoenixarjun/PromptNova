from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class Constrained(PromptAgent):
    """Agent for Constrained Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, max_words: int = None, output_format: str = None, **kwargs) -> str:
        """Refines the user input using Constrained prompting."""
        constrained_template = PromptTemplate(
            input_variables=["user_input", "max_words", "output_format"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use constrained prompting: enforce constraints like maximum {max_words} words and output format ({output_format}) to ensure structured, bounded responses.

User Input: {user_input}"""
        )
        chain = constrained_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "max_words": max_words or 100,
            "output_format": output_format or "bullet points"
        }).content