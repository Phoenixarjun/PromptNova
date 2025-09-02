from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import List

class TaskDecomposition(PromptAgent):
    """Agent for Task Decomposition Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, sub_steps: List[str] = None, **kwargs) -> str:
        """Refines the user input using Task Decomposition prompting."""
        sub_steps = sub_steps or ["Break down the problem", "Solve each part", "Integrate results"]
        sub_steps_str = ", ".join(sub_steps)
        
        task_decomposition_template = PromptTemplate(
            input_variables=["user_input", "sub_steps_str"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use task decomposition prompting: instruct the AI to break the task into sub-steps ({sub_steps_str}), solving each to build a complete response.

User Input: {user_input}"""
        )
        chain = task_decomposition_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "sub_steps_str": sub_steps_str
        }).content