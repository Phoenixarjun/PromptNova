from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class FlippedInteraction(PromptAgent):
    """Agent for Flipped Interaction Pattern Framework."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Flipped Interaction Pattern framework."""
        flipped_interaction_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the Flipped Interaction Pattern framework: instruct the AI to ask clarifying questions first, then use the answers to generate a tailored response, uncovering hidden requirements for a precise output.

User Input: {user_input}"""
        )
        chain = flipped_interaction_template | self.llm
        return chain.invoke({"user_input": user_input}).content