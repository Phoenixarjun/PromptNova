from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, Optional

class FinalPrompt(PromptAgent):
    """Agent for integrating refined responses into a final prompt."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    async def refine(self, user_input: str, **kwargs) -> str:
        """Refines the user input by integrating refined responses."""
        refined_responses = kwargs.get("refined_responses", {})
        type_prompts = kwargs.get("type_prompts", {})
        if not refined_responses and not type_prompts:
            raise ValueError("No refined or type prompts provided for integration.")
        return self.integrate(refined_responses, type_prompts, user_input)
    
    def integrate(self, refined_responses: Dict, type_prompts: Dict, user_input: str) -> str:
        """Integrates refined responses into a concise prompt."""
        integration_template = PromptTemplate(
            input_variables=["refined_responses", "type_prompts", "user_input"],
            template="""You are a world-class expert in the relevant domain. Based on the provided refined responses, type prompts, and user input, create a single, concise, and actionable prompt that directly addresses the user's request. Start the prompt with "You are a..." and focus on clarity and specificity. If refined responses are empty, use type prompts or the user input to create a relevant prompt. Output ONLY the final prompt, with no explanations, no meta text, no frameworks, and no additional commentary starts with You are a.... .

Refined Responses: {refined_responses}
Type Prompts: {type_prompts}
User Input: {user_input}"""
        )
        chain = integration_template | self.llm
        return chain.invoke({
            "refined_responses": str(refined_responses),
            "type_prompts": str(type_prompts),
            "user_input": user_input
        }).content