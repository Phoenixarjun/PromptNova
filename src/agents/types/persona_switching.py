from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class PersonaSwitching(PromptAgent):
    """Agent for Persona Switching / Multi-Role Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Persona Switching prompting."""
        persona_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Persona Switching Prompting: instruct the AI to adopt and switch between multiple specified personas or roles within a single response. This allows it to capture different perspectives, tones, or areas of expertise to provide a multi-faceted and comprehensive answer.

User Input: {user_input}"""
        )
        chain = persona_template | self.llm
        return chain.invoke({"user_input": user_input}).content