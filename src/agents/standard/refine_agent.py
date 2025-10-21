from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Dict, List, Optional, Any
import json
import re
from src.logger import logger
from pydantic import BaseModel, Field

class RefinedAgentPrompts(BaseModel):
    """A model to hold the refined prompts for each agent."""
    prompts: Dict[str, str] = Field(description="A dictionary where keys are agent names and values are the refined prompts.")

class RefineAgent(PromptAgent):
    """Agent for refining based on feedback."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    async def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("RefineAgent is designed for feedback-based refinement via refine_based_on_feedback.")
    
    async def refine_based_on_feedback(self, user_input: str, feedback: Dict, current_prompts: Dict[str, str], agents: List[str]) -> Dict:
        """Refines the existing prompts based on feedback and returns updated responses."""
        refinement_template = PromptTemplate(
            input_variables=["user_input", "current_prompts", "feedback", "agents"],
            template="""You are an expert prompt refiner. Based on the provided feedback, refine the EXISTING prompts for the specified agents. 

**CRITICAL: You MUST preserve the original intent, framework, and sophistication of each prompt while addressing the feedback.**

**Instructions:**
1.  Analyze the current prompts and the feedback provided.
2.  For each agent, refine the existing prompt to address the feedback while maintaining its core structure and quality.
3.  DO NOT oversimplify or dumb down the prompts. Preserve the expert-level quality.
4.  Return a JSON object with a single key \"prompts\", which is a dictionary where keys are the agent names and values are the refined versions of the original prompts.

**User Input:**
{user_input}

**Current Prompts to Refine:**
{current_prompts}

**Feedback to Address:**
{feedback}

**Agents to refine:**
{agents}

**Output Format:**
You MUST respond with a JSON object enclosed in ```json ... ```. Ensure all strings are properly escaped. Example:
```json
{{
  "prompts": {{
    "react": "[Refined version of the original react prompt]",
    "one_shot": "[Refined version of the original one_shot prompt]"
  }}
}}
```
"""
        )
        
        chain = refinement_template | self.llm
        try:
            response = await chain.ainvoke({
                "user_input": user_input,
                "current_prompts": json.dumps(current_prompts, indent=2),
                "feedback": json.dumps(feedback, indent=2),
                "agents": ', '.join(agents)
            })
            
            json_str = response.content
            match = re.search(r"```json\n(.*?)\n```", json_str, re.DOTALL)
            if match:
                json_str = match.group(1)

            response_data = json.loads(json_str, strict=False)
            validated_data = RefinedAgentPrompts(**response_data)
            return validated_data.prompts
            
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Structured output parsing failed in RefineAgent: {e}", exc_info=True)
            # Fallback: return the original prompts unchanged
            logger.warning("Refinement failed, returning original prompts as fallback")
            return {agent: current_prompts.get(agent, "") for agent in agents}
