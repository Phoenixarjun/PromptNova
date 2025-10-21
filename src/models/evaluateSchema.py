from pydantic import BaseModel, Field
from typing import Optional, Literal


class EvaluatePipelineInput(BaseModel):
    """
    Input for the prompt evaluation pipeline.
    """
    prompt_to_evaluate: str = Field(
        ...,
        description="The prompt that needs to be evaluated."
    )
    initial_prompt: Optional[str] = Field(
        None,
        description="Optional: The original, un-refined prompt. Used as a baseline for comparison."
    )
    selected_model: Optional[Literal["gemini", "mistral", "groq"]] = Field('gemini', description="The selected model provider.")
    selected_groq_model: Optional[str] = Field(None, description="The selected Groq model, if applicable.")
    api_key: Optional[str] = Field(None, description="User's encrypted API key for the LLM.")
    password: Optional[str] = Field(None, description="Password to decrypt the user's API key."
    )


class LLMAsJudgeOutput(BaseModel):
    """
    Output from the LLM-as-a-Judge agent.
    """
    clarity: int = Field(..., description="Rating for clarity (1-10).")
    specificity: int = Field(..., description="Rating for specificity (1-10).")
    context: int = Field(..., description="Rating for context completeness (1-10).")
    goal_alignment: int = Field(..., description="Rating for goal alignment (1-10).")
    measurability: int = Field(..., description="Rating for output measurability (1-10).")
    overall: int = Field(..., description="Overall score (1-10).")
    comment: str = Field(..., description="A 1-line justification for the overall score.")


class TRAGOutput(BaseModel):
    """
    Output from the T-RAG agent.
    """
    intent_alignment: int = Field(..., description="Rating for intent alignment (1-10).")
    completeness: int = Field(..., description="Rating for instruction completeness (1-10).")
    relevance: int = Field(..., description="Rating for expected relevance of output (1-10).")
    ambiguity: int = Field(..., description="Rating for ambiguity (1-10, lower is better).")
    overall: int = Field(..., description="Overall score (1-10).")


class MARFrameworkOutput(BaseModel):
    """
    Output from the MAR Framework agent.
    """
    clarity: float = Field(..., description="Score for clarity.")
    completeness: float = Field(..., description="Score for completeness.")
    relevance: float = Field(..., description="Score for relevance.")
    structure: float = Field(..., description="Score for structure and constraints.")
    creativity_precision_balance: float = Field(..., description="Score for creativity/precision balance.")
    overall_score: float = Field(..., description="Final weighted average score.")


class FinalEvaluationOutput(BaseModel):
    """
    The final, consolidated output from the evaluation pipeline.
    """
    final_score: float = Field(..., description="A final, normalized score from 0 to 100, representing overall prompt quality.")
    strengths: str = Field(..., description="A summary of the prompt's key strengths based on the evaluations.")
    areas_for_improvement: str = Field(..., description="Actionable suggestions for how the prompt could be improved.")
    report: str = Field(..., description="A detailed breakdown of the scores from each evaluation framework.")


class FullEvaluationResult(BaseModel):
    """
    A comprehensive model holding all intermediate and final results.
    """
    llm_as_judge: LLMAsJudgeOutput
    t_rag: TRAGOutput
    mar_framework: MARFrameworkOutput
    final_evaluation: FinalEvaluationOutput
