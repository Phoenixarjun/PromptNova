from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, Optional, List, Literal, Any
from src.logger import logger
from pydantic import BaseModel, Field

class EvaluationSummary(BaseModel):
    key_points: List[str] = Field(
        description="List of remaining issues, including style/framework mismatches, clarity gaps, or missed suggestions."
    )
    guidance: str = Field(
        description="A clear, actionable recommendation to fix the remaining issues. Must be concise and directly relevant."
    )

class EvaluationResult(BaseModel):
    status: Literal["yes", "no"]
    summary: Optional[EvaluationSummary] = Field(
        None, description="Summary of issues if status is 'no'."
    )

class UpdateEvaluator(PromptAgent):
    """Top-tier agent for rigorously evaluating an updated prompt."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.structured_llm = self.llm.with_structured_output(EvaluationResult)

    async def refine(self, user_input: str, **kwargs) -> str:
        raise NotImplementedError("UpdateEvaluator agent is designed for evaluation, not refinement.")

    def evaluate(
        self,
        user_prompt: str,
        generated_prompt: str,
        suggestions: Dict,
        style: Optional[List[str]],
        framework: Optional[str],
    ) -> Dict:
        """Evaluates whether the updated prompt has correctly applied improvements and meets expert-level quality."""
        evaluation_template = PromptTemplate(
            input_variables=["user_prompt", "generated_prompt", "suggestions", "style", "framework"],
            template="""You are a world-class Prompt Evaluation Expert with decades of experience in advanced LLM optimization. 
Your role: rigorously assess whether the 'Updated Prompt' integrates the required improvements while maintaining fidelity to style, framework, and user intent. 

Strict constraints:
- Do NOT rewrite the prompt.
- Output must strictly match the EvaluationResult schema.
- Only mark status = "yes" if ALL criteria are satisfied.

Evaluation Criteria:
1. Has the Updated Prompt fully applied the 'Improvement Suggestions'?
2. Does it correctly implement the required Style and Framework?
3. Is it clear, precise, and demonstrably stronger than the original?

Original User Prompt:
{user_prompt}

Improvement Suggestions:
{suggestions}

Required Style: {style}
Required Framework: {framework}

Updated Prompt:
{generated_prompt}

Now respond ONLY with:
- status: "yes" if all criteria are satisfied, otherwise "no".
- If "no", include:
  - key_points: list of specific remaining issues.
  - guidance: one actionable suggestion to fix those issues.
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
            return {
                "status": "no",
                "summary": {
                    "key_points": [
                        "LLM failed to produce valid structured JSON during evaluation."
                    ],
                    "guidance": "Re-run evaluation with stricter schema enforcement and narrower scope."
                }
            }
