from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, Optional
from pydantic import BaseModel, Field

class FinalPromptOutput(BaseModel):
    """Structured output for the final integrated prompt."""
    refined_prompt: str = Field(description="The final, integrated, and refined prompt ready for use.")
    explanation: str = Field(description="A detailed explanation of the improvements made and the rationale behind them.")

class FinalPrompt(PromptAgent):
    """Agent for integrating refined responses into a final prompt."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
        self.structured_llm = self.llm.with_structured_output(FinalPromptOutput)
    
    async def refine(self, user_input: str, **kwargs) -> str:
        refined_responses = kwargs.get("refined_responses", {})
        type_prompts = kwargs.get("type_prompts", {})
        if not refined_responses and not type_prompts:
            raise ValueError("No refined or type prompts provided for integration.")
        return await self.integrate(refined_responses, type_prompts, user_input)
    
    async def integrate(self, refined_responses: Dict, type_prompts: Dict, user_input: str, framework: str) -> str:
        integration_template = PromptTemplate(
            input_variables=["refined_responses", "type_prompts", "user_input", "framework"],
            template="""You are a world-class prompt engineer with 20+ years of experience.
Your task is to create a refined, actionable prompt based on the user's input and the provided context, applying the principles of the {framework} framework.
Additionally, you must provide a detailed explanation of the improvements you made and the rationale behind them.

**1. Refine the Prompt:**
- Using ONLY the content from the 'Refined Responses', 'Type Prompts', and 'User Input' sections below, create ONE single, clear, and actionable prompt.

**2. Provide Explanation:**
- Explain the improvements made and the rationale. Justify why the new prompt is better.
- Explain how the refined prompt aligns with the {framework} framework.

**STRICT RULES for the refined prompt:**
- It MUST begin with a role assignment (e.g., "You are a...").
- It must be a complete, standalone prompt ready for an LLM.
- Do NOT include any meta-text, commentary, or framework names within the prompt itself.
- It should follow the framework structure and include all the types in the prompt must return in the framework format only!!!.

        Refined Responses: {refined_responses}
        Type Prompts: {type_prompts}
        User Input: {user_input}
        Framework to apply: {framework}

You must respond with a JSON object with two keys: "refined_prompt" and "explanation"."""
        )

        chain = integration_template | self.structured_llm
        response_obj = await chain.ainvoke({
            "refined_responses": str(refined_responses),
            "type_prompts": str(type_prompts),
            "user_input": user_input,
            "framework": framework
        })

        # Construct the string format that the frontend expects.
        prompt_part = f"**Refined Prompt:**\n```\n{response_obj.refined_prompt.strip()}\n```"
        explanation_part = f"**Explanation of Improvements and Rationale:**\n{response_obj.explanation.strip()}"
        
        return f"{prompt_part}\n\n{explanation_part}"
