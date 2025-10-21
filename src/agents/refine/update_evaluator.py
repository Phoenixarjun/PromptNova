from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
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
            template='''You are a Prompt Evaluation Expert. Your task is to evaluate if the 'Updated Prompt' has correctly integrated the 'Improvement Suggestions'.

- **Inputs:**
- Required Style: {style}
- Required Framework: {framework}
- Improvement Suggestions: {suggestions}
- Updated Prompt: {generated_prompt}

**Instructions & Rules:**
1.  **Verify Integration:** Has the 'Updated Prompt' fully applied the 'Improvement Suggestions'? If there is no suggestions means "No".
2.  **Check Alignment:** Does the prompt align with the required 'Style' and 'Framework'?
3.  **Decide Status:**
    - If YES to both, set status to "yes".
    - If NO to either, set status to "no" and **you MUST provide a `summary` object** containing `key_points` (a list of remaining issues) and `guidance` (one actionable fix).

**Output Format:**
You MUST respond ONLY with a valid JSON object. If the status is "no", the `summary` field is REQUIRED.

**Example for a 'no' status:**
```json
{{
  "status": "no",
  "summary": {{
    "key_points": ["The prompt still lacks a clear call to action.", "The tone is too formal for the target audience."],
    "guidance": "Add a direct call to action at the end of the prompt and adjust the tone to be more conversational and engaging."
  }}
}}
```

**Example for a 'yes' status:**
```json
{{
  "status": "yes",
  "summary": null
}}
```'''
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
