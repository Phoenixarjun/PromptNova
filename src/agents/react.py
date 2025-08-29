from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent

class ReAct(PromptAgent):
    """Agent for ReAct Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, max_iterations: int = 3, **kwargs) -> str:
        """Refines the user input using ReAct prompting."""
        react_template = PromptTemplate(
            input_variables=["user_input", "max_iterations"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use ReAct prompting: instruct the AI to alternate between reasoning (think about the task) and acting (produce output), up to {max_iterations} iterations, to iteratively improve the response. Ensure the final output is polished and error-free.

User Input: {user_input}"""
        )
        chain = react_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "max_iterations": max_iterations
        }).content