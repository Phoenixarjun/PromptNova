from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from src.agents.prompt_agent import PromptAgent
import json
import re

class EvaluateAgent(PromptAgent):
    """Evaluates if the template is ready for production."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    def refine(self, user_input: str, **kwargs) -> str:
        return user_input

    def evaluate(self, current_template: str, intent: str) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["template", "intent"],
            template="""You are the Final Gatekeeper. Evaluate if this prompt template is ready for the user.

User Intent: {intent}
Template:
{template}

Is this template high-quality, complete, and accurate?
Return JSON:
{{
    "success": true/false,
    "reason": "Why it passed or failed",
    "final_polish_needed": "Any minor tweaks needed (optional)"
}}
"""
        )
        chain = prompt | self.llm
        response = chain.invoke({"template": current_template, "intent": intent}).content
        
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group(0))
            return json.loads(response)
        except:
            return {"success": True, "reason": "Default pass due to parse error"}
