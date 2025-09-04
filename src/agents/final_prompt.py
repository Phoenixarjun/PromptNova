from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict

class FinalPrompt(PromptAgent):
    """Agent for integrating refined responses into a final prompt."""
    
    def __init__(self):
        super().__init__()
    
    def integrate(self, refined_responses: Dict) -> str:
        """Integrates all refined responses into a wholesome prompt."""
        integration_template = PromptTemplate(
            input_variables=["refined_responses"],
            template="""You are an expert prompt integrator with 25+ years of experience. Combine the following refined responses from different agents into a single, cohesive, top-tier prompt optimized for Gemini AI. Ensure the final prompt incorporates all strengths, is clear, concise, specific, actionable, and fully aligns with the user's intent.

Refined Responses: {refined_responses}"""
        )
        chain = integration_template | self.llm
        return chain.invoke({"refined_responses": str(refined_responses)}).content