from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class ZeroShot(PromptAgent):
    """Agent for Zero-Shot Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Zero-Shot prompting."""
        zero_shot_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions for the AI to generate high-quality responses. Avoid ambiguity, include necessary details for context, and ensure it encourages detailed, accurate outputs. Do not add examples or additional reasoning paths—keep it zero-shot.

User Input: {user_input}"""
        )
        chain = zero_shot_template | self.llm
        return chain.invoke({"user_input": user_input}).content