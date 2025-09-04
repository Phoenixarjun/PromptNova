from pydantic import BaseModel, Field
from typing import List, Literal

class PromptSchema(BaseModel):
    """Pydantic model for prompt refinement input and output."""
    user_input: str = Field(..., min_length=1, description="The original prompt text provided by the user.")
    style: List[Literal[
        "zero_shot", "one_shot", "cot", "tot", "react", "in_context", "emotion", "role",
        "few_shot", "self_consistency", "meta_prompting", "least_to_most", "multi_task",
        "task_decomposition", "constrained", "generated_knowledge", "ape", "directional_stimulus"
    ]] = Field(..., min_items=1, description="List of prompt refinement styles to apply.")
    framework: Literal[
        "co_star", "tcef", "crispe", "rtf", "ice", "craft", "ape",
        "pecra", "oscar", "rasce", "reflection", "flipped_interaction", "bab"
    ] = Field(..., description="The single prompt refinement framework to apply.")
    output_str: str = Field("", description="The final refined prompt output.")

    class Config:
        json_encoders = {
            List: lambda v: list(v),  
        }