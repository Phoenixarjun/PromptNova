from typing import Any, Dict, List
from langchain_core.prompts import PromptTemplate
from src.agents.prompt_agent import PromptAgent
import json
import re

class RouterAgent(PromptAgent):
    """
    Agent responsible for routing the request to the correct composer 
    and refining the intent if necessary.
    """
    def __init__(self, llm: Any):
        super().__init__(llm)

    def refine(self, user_input: str, **kwargs) -> str:
        # This agent doesn't use the standard refine method in the same way, 
        # but we implement it to satisfy the interface if needed.
        # Ideally, it should be called with specific arguments.
        return user_input

    def route(self, intent: str, template_type: str, variables: List[str]) -> Dict[str, Any]:
        """
        Analyzes the intent and prepares instructions for the composer.
        """
        prompt = PromptTemplate(
            input_variables=["intent", "template_type", "variables"],
            template="""You are an expert AI Architect. Your task is to analyze a user's request for a prompt template and prepare a structured plan for the composer agent.

User Intent: {intent}
Template Type: {template_type}
Variables: {variables}

Analyze the intent and extract key requirements, tone, and specific constraints. 
Return a JSON object with the following structure:
{{
    "enhanced_intent": "A more detailed and technical description of what the template should achieve.",
    "suggested_structure": ["List of sections that should be included in the template"],
    "tone": "The recommended tone for the template (e.g., Professional, Creative, Strict)"
}}

Ensure the output is valid JSON.
"""
        )
        chain = prompt | self.llm
        response = chain.invoke({
            "intent": intent, 
            "template_type": template_type, 
            "variables": ", ".join(variables)
        }).content
        
        try:
            # Extract JSON if wrapped in code blocks
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group(0))
            return json.loads(response)
        except Exception:
            # Fallback if JSON parsing fails
            return {
                "enhanced_intent": intent,
                "suggested_structure": ["Standard Structure"],
                "tone": "Professional"
            }
