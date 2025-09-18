from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, Optional, List, Literal
import json
import re
from src.logger import logger
from pydantic import BaseModel, Field

class EvaluationSummary(BaseModel):
    key_points: List[str] = Field(description="List of remaining issues, including style/framework mismatches.")
    guidance: str = Field(description="A new improvement suggestion to fix the remaining issues.")

class EvaluationResult(BaseModel):
    status: Literal["yes", "no"]
    summary: Optional[EvaluationSummary] = Field(None, description="Summary of issues if status is 'no'.")

class UpdateEvaluator(PromptAgent):
    """Agent for evaluating the updated prompt."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
        self.structured_llm = self.llm.with_structured_output(EvaluationResult)

    async def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("UpdateEvaluator agent is designed for evaluation, not refinement.")

    def evaluate(
        self,
        user_prompt: str,
        generated_prompt: str,
        suggestions: Dict,
        style: Optional[List[str]],
        framework: Optional[str],
    ) -> Dict:
        """Evaluates if the generated_prompt has successfully incorporated the suggestions."""
        evaluation_template = PromptTemplate(
            input_variables=["user_prompt", "generated_prompt", "suggestions", "style", "framework"],
            template="""You are an expert prompt evaluator. Your task is to determine if the 'Updated Prompt' has successfully incorporated the 'Improvement Suggestions' and adheres to the required 'Style' and 'Framework', to better align with the 'Original User Prompt'.

Original User Prompt: {user_prompt}

Improvement Suggestions: {suggestions}

Required Style: {style}
Required Framework: {framework}

Updated Prompt: {generated_prompt}

Evaluation:
1. Does the 'Updated Prompt' address the deficiencies and apply the adjustments from the 'Improvement Suggestions'?
2. Does the 'Updated Prompt' correctly apply the required 'Style' and 'Framework'?
3. Is the 'Updated Prompt' a clear and high-quality prompt that is likely to produce a better result than before?

If all are true, set status to "yes".
Otherwise, set status to "no" and provide a summary with 'key_points' (a list of remaining issues) and 'guidance' (a new improvement suggestion).
"""
        )
        chain = evaluation_template | self.structured_llm
        try:
            response = chain.invoke({
                "user_prompt": user_prompt,
                "generated_prompt": generated_prompt,
                "suggestions": str(suggestions),
                "style": str(style) if style else "Not specified",
                "framework": framework if framework else "Not specified",
            })
            return response.dict()
        except Exception as e:
            logger.error(f"Structured output parsing failed in UpdateEvaluator: {e}", exc_info=True)
            # Fallback for when structured output fails
            return {
                "status": "no",
                "summary": {
                    "key_points": ["LLM failed to produce valid structured JSON during evaluation."],
                    "guidance": "Re-apply the original suggestions, focusing on one change at a time."
                }
            }