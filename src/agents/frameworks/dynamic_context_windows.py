from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class DynamicContextWindows(PromptAgent):
    """Agent for Dynamic Context Windows Framework."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Dynamic Context Windows framework."""
        dynamic_context_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Dynamic Context Windows framework: instruct the AI to manage its context window by prioritizing critical information from the conversation history. The prompt should guide the AI to summarize or discard less relevant details to maintain focus and continuity over long interactions.

User Input: {user_input}"""
        )
        chain = dynamic_context_template | self.llm
        return chain.invoke({"user_input": user_input}).content