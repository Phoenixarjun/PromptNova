from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent

class AutomaticPromptEngineering(PromptAgent):
    """Agent for Automatic Prompt Engineering (APE) style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, optimization_goal: str = "clarity", **kwargs) -> str:
        """Refines the user input using Automatic Prompt Engineering prompting."""
        ape_template = PromptTemplate(
            input_variables=["user_input", "optimization_goal"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use automatic prompt engineering (APE): instruct the AI to iteratively evolve the prompt towards the optimization goal ({optimization_goal}), automating refinement for the best results.

User Input: {user_input}"""
        )
        chain = ape_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "optimization_goal": optimization_goal
        }).content