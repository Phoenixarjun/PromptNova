from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import List, Dict
import json
import re
from src.logger import logger

class SelfCorrection(PromptAgent):
    """Agent for self-correction evaluation."""
    
    def __init__(self):
        super().__init__()
    
    async def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("SelfCorrection agent is designed for evaluation, not refinement.")
    
    def evaluate(self, prompt: str, user_prompt: str, agents: List[str]) -> Dict:
        """Evaluates the refined prompt against the original user prompt."""
        evaluation_template = PromptTemplate(
            input_variables=["prompt", "user_prompt", "agents"],
            template="""You are an expert prompt evaluator with 25+ years of experience. Evaluate the following refined prompt to determine if it fully meets the intent and requirements expressed in the original user prompt. For each agent ({agents}), assign a percentage score (0-100%) indicating how well the refined prompt aligns with the user's intent using that agent's style. If all scores are 100%, return {{"status": "yes"}}. Otherwise, return a VALID JSON object: {{"status": "no", "agents": {{agent: score, ...}}, "summary": {{"key_points": ["list of issues"], "guidance": {{agent: "improvement suggestion", ...}}}}}}. Output ONLY the JSON object, no markdown, no extra text, no comments, and ensure all strings are properly escaped.

Refined Prompt: {prompt}
User Prompt: {user_prompt}
Agents: {agents}"""
        )
        chain = evaluation_template | self.llm
        response = chain.invoke({"prompt": prompt, "user_prompt": user_prompt, "agents": ', '.join(agents)}).content
        # Clean response to ensure valid JSON
        response = re.sub(r'^```json\s*|\s*```$', '', response, flags=re.MULTILINE)  # Remove markdown
        response = re.sub(r'[^\x00-\x7F]+', '', response)  # Remove non-ASCII characters
        response = re.sub(r'(?<!\\)"', r'\"', response)  # Escape unescaped quotes
        response = re.sub(r'\n+', ' ', response)  # Replace newlines with spaces
        response = response.strip()
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Malformed JSON from LLM in SelfCorrection: {str(e)} - Response: {response}")
            return {
                "status": "no",
                "agents": {agent: 50 for agent in agents}, 
                "summary": {
                    "key_points": ["LLM failed to produce valid JSON. Using default scores and recommending simpler prompt structure."],
                    "guidance": {agent: f"Simplify prompt for {agent} to focus on direct alignment with user intent." for agent in agents}
                }
            }