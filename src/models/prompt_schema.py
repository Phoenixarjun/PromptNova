from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class PromptSchema(BaseModel):
    """Pydantic model for prompt refinement input and output."""
    user_input: str = Field(..., min_length=1, description="The original prompt text provided by the user.")
    style: List[Literal[
        "zero_shot", "one_shot", "cot", "tot", "react", "in_context", "emotion", "role",
        "few_shot", "self_consistency", "meta_prompting", "least_to_most", "multi_task",
        "task_decomposition", "constrained", "generated_knowledge", "automatic_prompt_engineering", "directional_stimulus",
        "chain_of_verification", "skeleton_of_thought", "graph_of_thoughts", "plan_and_solve",
        "maieutic_prompting", "reflexion_type", "chain_of_density", "active_prompt",
        "retrieval_augmented_prompting", "multi_agent_debate", "persona_switching",
        "scaffolded_prompting", "deliberation_prompting", "context_expansion", "goal_oriented_prompting"
    ]] = Field(..., min_items=1, description="List of prompt refinement styles to apply.")
    framework: Literal[
        "co_star", "tcef", "crispe", "rtf", "ice", "craft", "ape",
        "pecra", "oscar", "rasce", "reflection", "flipped_interaction", "bab",
        "prompt", "soap", "clear", "prism", "grips", "app", "scope",
        "tool_oriented_prompting", "neuro_symbolic_prompting", "dynamic_context_windows",
        "meta_cognitive_prompting", "prompt_ensembles"
    ] = Field(..., description="The single prompt refinement framework to apply.")
    output_str: str = Field("", description="The final refined prompt output.")
    api_key: Optional[str] = Field(None, description="User's API key for the LLM.")
    password: Optional[str] = Field(None, description="Password to decrypt the user's API key.")

    class Config:
        json_encoders = {
            List: lambda v: list(v),  
        }