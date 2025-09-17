from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class RetrievalAugmentedPrompting(PromptAgent):
    """Agent for Retrieval-Augmented Prompting (RAP) style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Retrieval-Augmented Prompting."""
        rap_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Retrieval-Augmented Prompting (RAP): instruct the AI to first perform a retrieval step to gather fresh, relevant, or domain-specific information from an external knowledge source (e.g., a vector database or search engine). Then, it must use this retrieved context to generate a factually grounded and comprehensive answer, explicitly citing its sources.

User Input: {user_input}"""
        )
        chain = rap_template | self.llm
        return chain.invoke({"user_input": user_input}).content