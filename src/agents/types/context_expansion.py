from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class ContextExpansion(PromptAgent):
    """Agent for Context Expansion / Compression Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Context Expansion/Compression prompting."""
        context_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Context Expansion/Compression: instruct the AI to dynamically manage its context. If the input is too brief, it should expand it with relevant details. If the context is too long or noisy, it should compress it to its most essential parts before generating the final answer, ensuring optimal use of the context window.

User Input: {user_input}"""
        )
        chain = context_template | self.llm
        return chain.invoke({"user_input": user_input}).content