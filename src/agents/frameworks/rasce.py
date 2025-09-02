from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent

class Rasce(PromptAgent):
    """Agent for RASCE Framework."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using RASCE framework."""
        rasce_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the RASCE framework: Role (assign persona), Action (define task), Steps (break down the process), Constraints (set limits), Examples (provide demonstrations). Ensure the refined prompt incorporates all elements for step-by-step, guided outputs.

User Input: {user_input}"""
        )
        chain = rasce_template | self.llm
        return chain.invoke({"user_input": user_input}).content