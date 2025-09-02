from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent

class Crispe(PromptAgent):
    """Agent for CRISPE Framework."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using CRISPE framework."""
        crispe_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the CRISPE framework: Capacity & Role (assign expertise and persona), Insight (focus on deep analysis), Statement (clear task), Personality (set tone and style), Example (demonstrate desired output). Ensure the refined prompt incorporates all elements for expert-level, insightful responses.

User Input: {user_input}"""
        )
        chain = crispe_template | self.llm
        return chain.invoke({"user_input": user_input}).content