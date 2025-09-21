from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class Soap(PromptAgent):
    """Agent for SOAP Framework."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using SOAP framework."""
        soap_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the SOAP framework: Subject (identify the topic), Objective (state what you want done), Audience (define who will read the output), and Parameters (specify constraints like word count or format). Ensure the prompt is unambiguous and audience-specific.

User Input: {user_input}"""
        )
        chain = soap_template | self.llm
        return chain.invoke({"user_input": user_input}).content