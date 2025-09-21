from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class NeuroSymbolicPrompting(PromptAgent):
    """Agent for Neuro-Symbolic Prompting Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Neuro-Symbolic Prompting framework."""
        neuro_symbolic_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Neuro-Symbolic Prompting framework: instruct the AI to combine its natural language reasoning with symbolic logic. The prompt should require the AI to generate outputs that are not only creative but also logically consistent and explainable, validating its reasoning against a set of rules.

User Input: {user_input}"""
        )
        chain = neuro_symbolic_template | self.llm
        return chain.invoke({"user_input": user_input}).content