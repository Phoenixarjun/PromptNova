from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class ToolOrientedPrompting(PromptAgent):
    """Agent for Tool-Oriented Prompting (TOP) Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Tool-Oriented Prompting framework."""
        top_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Tool-Oriented Prompting (TOP) framework: instruct the AI to identify opportunities to use external tools, plan the sequence of tool calls, and integrate their outputs back into the reasoning process to produce a comprehensive, action-oriented response.

User Input: {user_input}"""
        )
        chain = top_template | self.llm
        return chain.invoke({"user_input": user_input}).content