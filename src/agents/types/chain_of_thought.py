from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class ChainOfThought(PromptAgent):
    """Agent for Chain of Thoughts Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, steps: int = None, **kwargs) -> str:
        """Refines the user input using Chain of Thoughts prompting."""
        cot_template = PromptTemplate(
            input_variables=["user_input", "steps"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use chain-of-thought prompting: instruct the AI to think step by step, breaking down the task into {steps} logical steps for better reasoning and output quality. Ensure the steps are detailed and lead to a comprehensive response.

User Input: {user_input}"""
        )
        chain = cot_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "steps": steps or 4
        }).content