from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class MetaCognitivePrompting(PromptAgent):
    """Agent for Meta-Cognitive Prompting Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Meta-Cognitive Prompting framework."""
        meta_cognitive_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Meta-Cognitive Prompting framework: instruct the AI to reflect on its own confidence level. The prompt should require the AI to generate an answer and then self-assess its certainty, flagging low-confidence parts and potentially triggering alternative reasoning paths to improve reliability.

User Input: {user_input}"""
        )
        chain = meta_cognitive_template | self.llm
        return chain.invoke({"user_input": user_input}).content