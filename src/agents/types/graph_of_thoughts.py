from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class GraphOfThoughts(PromptAgent):
    """Agent for Graph-of-Thoughts (GoT) Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Graph-of-Thoughts prompting."""
        got_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use the Graph-of-Thoughts (GoT) method: instruct the AI to model the problem as a graph where thoughts are nodes and connections are edges. The AI should explore multiple reasoning paths, merge insights from different paths, and synthesize them to produce a comprehensive and robust final answer. This is ideal for complex, non-linear problems.

User Input: {user_input}"""
        )
        chain = got_template | self.llm
        return chain.invoke({"user_input": user_input}).content