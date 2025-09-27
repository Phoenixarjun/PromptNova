from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import List, Dict, Optional, Literal, Any
import json
import re
from src.logger import logger
from pydantic import BaseModel, Field, conint

class AgentGuidance(BaseModel):
    key_points: List[str] = Field(description="List of issues found in the prompt.")
    guidance: str = Field(description="A single string of improvement suggestions.")

class SelfCorrectionResult(BaseModel):
    status: Literal["yes", "no"]
    agents: Optional[Dict[str, conint(ge=0, le=100)]] = Field(None, description="Percentage score for each agent.")
    summary: Optional[AgentGuidance] = Field(None, description="Summary of issues if status is 'no'.")

class SelfCorrection(PromptAgent):
    """Agent for self-correction evaluation."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    async def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("SelfCorrection agent is designed for evaluation, not refinement.")
    
    def evaluate(self, prompt: str, user_prompt: str, agents: List[str]) -> Dict:
        """Evaluates the refined prompt against the original user prompt."""
        evaluation_template = PromptTemplate(
            input_variables=["prompt", "user_prompt", "agents"],
            template="""You are an expert prompt evaluator. Evaluate the refined prompt based on the user's original prompt.

**Instructions:**
1.  For each agent in {agents}, provide a percentage score (0-100) representing how well the refined prompt aligns with the user's intent.
2.  If all scores are 100, set status to "yes".
3.  Otherwise, set status to "no" and provide a summary including:
    - `key_points`: A list of the main issues.
    - `guidance`: A single string of actionable advice to fix the issues.

**Refined Prompt:**
{prompt}

**User Prompt:**
{user_prompt}

**Agents to Score:**
{agents}

**Output Format:**
You MUST respond with a JSON object enclosed in ```json ... ```. Ensure all strings are properly escaped. Example for a 'no' status:
```json
{{
  "status": "no",
  "agents": {{
    "one_shot": 80,
    "tot": 75
  }},
  "summary": {{
    "key_points": ["The prompt is too complex for a beginner.", "It assumes prior knowledge of advanced topics."],
    "guidance": "Simplify the prompt to focus on foundational concepts. Remove jargon and start with a basic 'Hello, World!' example to make it more accessible for beginners."
  }}
}}
```
"""
        )
        chain = evaluation_template | self.llm
        try:
            response = chain.invoke({"prompt": prompt, "user_prompt": user_prompt, "agents": ', '.join(agents)})
            json_str = response.content
            match = re.search(r"```json\n(.*?)\n```", json_str, re.DOTALL)
            if match:
                json_str = match.group(1)
            
            response_data = json.loads(json_str, strict=False)
            validated_data = SelfCorrectionResult(**response_data)
            return validated_data.dict()
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Structured output parsing failed in SelfCorrection: {e}", exc_info=True)
            return {
                "status": "no",
                "agents": {agent: 50 for agent in agents},
                "summary": {
                    "key_points": ["LLM failed to produce valid JSON. Using default scores."],
                    "guidance": "Simplify the prompt to focus on direct alignment with user intent."
                }
            }
