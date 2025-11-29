from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from src.agents.prompt_agent import PromptAgent
import json
import re

class AnalyzeAgent(PromptAgent):
    """Analyzes the draft template for improvements."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    def refine(self, user_input: str, **kwargs) -> str:
        return user_input

    def analyze(self, current_template: str, intent: str) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["template", "intent"],
            template="""You are a QA Specialist for AI Prompts. Analyze the following prompt template against the user's intent.

User Intent: {intent}
Current Template:
{template}

Identify weaknesses, missing sections, ambiguities, or potential hallucinations.
Return a JSON object:
{{
    "critique": "Summary of issues found.",
    "suggestions": ["List of specific actionable improvements"],
    "score": 0-100
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
            return {"critique": "Analysis failed", "suggestions": [], "score": 50}
