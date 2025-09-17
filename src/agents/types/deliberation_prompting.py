from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class DeliberationPrompting(PromptAgent):
    """Agent for Deliberation / Double-Pass Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Deliberation Prompting."""
        deliberation_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Deliberation/Double-Pass Prompting: instruct the AI to first generate an initial, high-level "deliberation" or draft of its thought process. Then, in a second pass, it should use this deliberation as a guide to produce a more refined, detailed, and accurate final answer.

User Input: {user_input}"""
        )
        chain = deliberation_template | self.llm
        return chain.invoke({"user_input": user_input}).content