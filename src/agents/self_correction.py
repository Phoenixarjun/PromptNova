from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import List, Dict
import json

class SelfCorrection(PromptAgent):
    """Agent for self-correction evaluation."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("SelfCorrection agent is designed for evaluation, not refinement.")
    
    def evaluate(self, prompt: str, user_prompt: str, agents: List[str]) -> Dict:
        """Evaluates the refined prompt against the original user prompt."""
        evaluation_template = PromptTemplate(
            input_variables=["prompt", "user_prompt", "agents"],
            template="""You are an expert prompt evaluator with 25+ years of experience. Evaluate the following refined prompt to determine if it fully meets the intent and requirements expressed in the original user prompt. For each agent ({agents}), assign a percentage score (0-100%) indicating how well the refined prompt aligns with the user's intent using that agent's style. If all scores are 100%, return {'status': 'yes'}. Otherwise, return {'status': 'no', 'agents': {agent: score, ...}, 'summary': {key points on what needs to be refined, including specific guidance on how to improve each low-scoring agent to better align with the user prompt}}.

Refined Prompt: {prompt}
User Prompt: {user_prompt}
Agents: {agents}"""
        )
        chain = evaluation_template | self.llm
        response = chain.invoke({"prompt": prompt, "user_prompt": user_prompt, "agents": ', '.join(agents)}).content
        return json.loads(response)