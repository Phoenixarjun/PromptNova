from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import List, Dict, Optional, Literal
import json
import re
from src.logger import logger
from pydantic import BaseModel, Field, conint

class AgentGuidance(BaseModel):
    key_points: List[str] = Field(description="List of issues found in the prompt.")
    guidance: Dict[str, str] = Field(description="Improvement suggestions for each agent.")

class SelfCorrectionResult(BaseModel):
    status: Literal["yes", "no"]
    agents: Optional[Dict[str, conint(ge=0, le=100)]] = Field(None, description="Percentage score for each agent.")
    summary: Optional[AgentGuidance] = Field(None, description="Summary of issues if status is 'no'.")

class SelfCorrection(PromptAgent):
    """Agent for self-correction evaluation."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
        self.structured_llm = self.llm.with_structured_output(SelfCorrectionResult)
    
    async def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("SelfCorrection agent is designed for evaluation, not refinement.")
    
    def evaluate(self, prompt: str, user_prompt: str, agents: List[str]) -> Dict:
        """Evaluates the refined prompt against the original user prompt."""
        evaluation_template = PromptTemplate(
            input_variables=["prompt", "user_prompt", "agents"],
            template="""You are an expert prompt evaluator with 25+ years of experience. Evaluate the following refined prompt to determine if it fully meets the intent and requirements expressed in the original user prompt. For each agent ({agents}), assign a percentage score (0-100%) indicating how well the refined prompt aligns with the user's intent using that agent's style. 
            
If all scores are 100%, set status to "yes". 
Otherwise, set status to "no" and provide a score for each agent in the 'agents' field. Also provide a 'summary' with 'key_points' (a list of issues) and 'guidance' (a dictionary of improvement suggestions for each agent).

Refined Prompt: {prompt}
User Prompt: {user_prompt}
Agents: {agents}"""
        )
        chain = evaluation_template | self.structured_llm
        try:
            response = chain.invoke({"prompt": prompt, "user_prompt": user_prompt, "agents": ', '.join(agents)})
            return response.dict()
        except Exception as e:
            logger.error(f"Structured output parsing failed in SelfCorrection: {e}", exc_info=True)
            return {
                "status": "no",
                "agents": {agent: 50 for agent in agents}, 
                "summary": {
                    "key_points": ["LLM failed to produce valid JSON. Using default scores and recommending simpler prompt structure."],
                    "guidance": {agent: f"Simplify prompt for {agent} to focus on direct alignment with user intent." for agent in agents}
                }
            }