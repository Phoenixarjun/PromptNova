from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent

class Pecra(PromptAgent):
    """Agent for PECRA Framework."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using PECRA framework."""
        pecra_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the PECRA framework: Purpose (define the goal), Expectation (set output expectations), Context (provide background), Request (specify action), Audience (target reader). Ensure the refined prompt incorporates all elements for user-centered, persuasive outputs.

User Input: {user_input}"""
        )
        chain = pecra_template | self.llm
        return chain.invoke({"user_input": user_input}).content