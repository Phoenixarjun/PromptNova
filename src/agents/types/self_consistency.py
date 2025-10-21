from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class SelfConsistency(PromptAgent):
    """Agent for Self-Consistency Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, samples: int = 3, **kwargs) -> str:
        """Refines the user input using Self-Consistency prompting."""
        self_consistency_template = PromptTemplate(
            input_variables=["user_input", "samples"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use self-consistency prompting: instruct the AI to generate {samples} variations of the response and select the most consistent one to reduce hallucinations and improve reliability.

User Input: {user_input}"""
        )
        chain = self_consistency_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "samples": samples
        }).content