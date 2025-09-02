from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent

class Oscar(PromptAgent):
    """Agent for OSCAR Framework."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using OSCAR framework."""
        oscar_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use the OSCAR framework: Objective (state the goal), Scope (define boundaries), Constraints (list limits), Assumptions (set premises), Results (specify expected output). Ensure the refined prompt incorporates all elements for realistic, project-focused planning.

User Input: {user_input}"""
        )
        chain = oscar_template | self.llm
        return chain.invoke({"user_input": user_input}).content