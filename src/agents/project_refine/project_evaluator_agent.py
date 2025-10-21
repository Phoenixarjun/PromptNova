from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Dict, Optional, List, Any, Literal
from pydantic import BaseModel, Field

class EvaluationSummary(BaseModel):
    key_points: List[str] = Field(
        description="List of remaining issues, such as missed suggestions, incomplete implementation, or new inconsistencies."
    )
    guidance: str = Field(
        description="A clear, actionable recommendation to fix the remaining issues. Must be concise and directly relevant."
    )

class EvaluationResult(BaseModel):
    status: Literal["yes", "no"]
    summary: Optional[EvaluationSummary] = Field(
        None, description="Summary of issues if status is 'no'."
    )

class ProjectEvaluatorAgent(PromptAgent):
    """Top-tier agent for rigorously evaluating updated project artifacts."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.structured_llm = self.llm.with_structured_output(EvaluationResult)

    async def refine(self, user_input: str, **kwargs) -> str:
        raise NotImplementedError("ProjectEvaluatorAgent agent is designed for evaluation, not refinement.")

    def evaluate(
        self,
        original_user_prompt: str,
        updated_project_artifacts: Dict,
        suggestions: Dict,
    ) -> Dict:
        """Evaluates whether the updated project artifacts have correctly applied improvements."""
        evaluation_template = PromptTemplate(
            input_variables=["original_user_prompt", "updated_project_artifacts", "suggestions"],
            template='''You are a Project Evaluation Expert. Your task is to evaluate if the 'Updated Project Artifacts' have correctly integrated the 'Improvement Suggestions'.

- **Inputs:**
- Original User Prompt: {original_user_prompt}
- Improvement Suggestions: {suggestions}
- Updated Project Artifacts: {updated_project_artifacts}

**Instructions & Rules:**
1.  **Verify Integration:** Has the 'Updated Project Artifacts' fully applied the 'Improvement Suggestions'?
2.  **Check Alignment:** Do the artifacts still align with the 'Original User Prompt'?
3.  **Decide Status:**
    - If YES to both, set status to "yes".
    - If NO to either, set status to "no" and **you MUST provide a `summary` object** containing `key_points` (a list of remaining issues) and `guidance` (one actionable fix).

**Output Format:**
You MUST respond ONLY with a valid JSON object. If the status is "no", the `summary` field is REQUIRED.
'''
        )
        chain = evaluation_template | self.structured_llm
        try:
            response = chain.invoke({
                "original_user_prompt": original_user_prompt,
                "updated_project_artifacts": str(updated_project_artifacts),
                "suggestions": str(suggestions),
            })
            return response.dict()
        except Exception as e:
            logger.error(f"Structured output parsing failed in ProjectEvaluatorAgent: {e}", exc_info=True)
            return {
                "status": "no",
                "summary": {
                    "key_points": [
                        "LLM failed to produce valid structured JSON during evaluation."
                    ],
                    "guidance": "Re-run evaluation with stricter schema enforcement and narrower scope."
                }
            }
