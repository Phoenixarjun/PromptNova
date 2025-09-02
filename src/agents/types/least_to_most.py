from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import List

class LeastToMost(PromptAgent):
    """Agent for Least-to-Most Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, sub_tasks: List[str] = None, **kwargs) -> str:
        """Refines the user input using Least-to-Most prompting."""
        sub_tasks = sub_tasks or ["Identify core intent", "Add basic details", "Enhance with advanced instructions"]
        sub_tasks_str = ", ".join(sub_tasks)
        
        least_to_most_template = PromptTemplate(
            input_variables=["user_input", "sub_tasks_str"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use least-to-most prompting: instruct the AI to break the task into sub-tasks ({sub_tasks_str}), solving from simplest to most complex for cumulative understanding.

User Input: {user_input}"""
        )
        chain = least_to_most_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "sub_tasks_str": sub_tasks_str
        }).content