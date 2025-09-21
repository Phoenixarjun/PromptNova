from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class MultiAgentDebate(PromptAgent):
    """Agent for Multi-Agent Debate/Consensus Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input using Multi-Agent Debate prompting."""
        debate_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following user input into a top-tier, expert-level prompt optimized for large language models. Use Multi-Agent Debate Prompting: instruct the AI to simulate a debate between multiple agents, each with a distinct perspective or role. The agents should challenge each other's reasoning and arguments. Finally, a neutral moderator agent should synthesize the debate to produce a final, consensus-based answer that considers all viewpoints.\n\nUser Input: {user_input}"""
        )
        chain = debate_template | self.llm
        return chain.invoke({"user_input": user_input}).content