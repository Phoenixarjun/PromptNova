from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, List, Optional
import json
import re
from src.logger import logger
from pydantic import BaseModel, Field

class RefinedAgentPrompts(BaseModel):
    """A model to hold the refined prompts for each agent."""
    prompts: Dict[str, str] = Field(description="A dictionary where keys are agent names and values are the refined prompts.")

class RefineAgent(PromptAgent):
    """Agent for refining based on feedback."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
        self.structured_llm = self.llm.with_structured_output(RefinedAgentPrompts)
    
    async def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("RefineAgent is designed for feedback-based refinement via refine_based_on_feedback.")
    
    def refine_based_on_feedback(self, user_input: str, feedback: Dict, agents: List[str]) -> Dict:
        """Refines the low-scoring agents based on feedback and returns updated responses."""
        refinement_template = PromptTemplate(
            input_variables=["user_input", "feedback", "agents"],
            template="""You are an expert prompt refiner with 25+ years of experience. Based on the provided feedback, refine the prompts for the low-scoring agents ({agents}) for the given user input. Use the feedback's summary key points to address deficiencies and improve alignment with the user's intent. Preserve correct agents (100% score) unchanged. 
            
Return a JSON object with a single key "prompts", which is a dictionary with refined prompts for each agent. The format should be: {{"prompts": {{"agent1": "refined prompt1", "agent2": "refined prompt2", ...}}}}.

User Input: {user_input}
Feedback: {feedback}
Agents to refine: {agents}"""
        )
        chain = refinement_template | self.structured_llm
        try:
            response = chain.invoke({"user_input": user_input, "feedback": str(feedback), "agents": ', '.join(agents)})
            return response.prompts
        except Exception as e:
            logger.error(f"Structured output parsing failed in RefineAgent: {e}", exc_info=True)
            # Fallback to a DSA-focused prompt based on user input
            return {
                agent: f"You are an expert in Data Structures and Algorithms. Provide a clear and concise solution for solving Data Structures and Algorithms (DAS) problems on LeetCode using the {agent} approach, including problem descriptions, optimized Python code, and brief explanations." 
                for agent in agents
            }