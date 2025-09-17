from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import List, Optional

class MultiTask(PromptAgent):
    """Agent for Multi-Task Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, tasks: List[str] = None, **kwargs) -> str:
        """Refines the user input using Multi-Task prompting."""
        tasks = tasks or ["Generate ideas", "Structure the response", "Provide examples"]
        tasks_str = ", ".join(tasks)
        
        multi_task_template = PromptTemplate(
            input_variables=["user_input", "tasks_str"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use multi-task prompting: instruct the AI to handle multiple related tasks ({tasks_str}) in one prompt, leveraging multitasking for efficiency and comprehensive outputs.

User Input: {user_input}"""
        )
        chain = multi_task_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "tasks_str": tasks_str
        }).content