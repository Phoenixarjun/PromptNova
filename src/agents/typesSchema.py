from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional

class PromptInput(BaseModel):
    """Base Pydantic model for all prompt refinement inputs."""
    user_input: str = Field(..., min_length=1, description="The original prompt text provided by the user.")
    style: Literal[
        "zero_shot", "one_shot", "cot", "tot", "react", "in_context", "emotion", "role",
        "few_shot", "self_consistency", "meta_prompting", "least_to_most", "multi_task",
        "task_decomposition", "constrained", "generated_knowledge", "ape", "directional_stimulus"
    ] = Field(..., description="The desired prompt refinement style.")

class ZeroShotPromptInput(PromptInput):
    """Input schema for Zero-Shot Prompting style."""
    style: Literal["zero_shot"] = "zero_shot"

class OneShotPromptInput(PromptInput):
    """Input schema for One-Shot Prompting style."""
    style: Literal["one_shot"] = "one_shot"
    example_input: Optional[str] = Field(None, description="Optional example input for one-shot prompting.")
    example_output: Optional[str] = Field(None, description="Optional example output for one-shot prompting.")

class ChainOfThoughtPromptInput(PromptInput):
    """Input schema for Chain-of-Thought Prompting style."""
    style: Literal["cot"] = "cot"
    steps: Optional[int] = Field(None, ge=1, description="Optional number of reasoning steps to enforce.")

class TreeOfThoughtPromptInput(PromptInput):
    """Input schema for Tree of Thoughts Prompting style."""
    style: Literal["tot"] = "tot"
    branches: Optional[int] = Field(3, ge=1, le=5, description="Number of reasoning branches to explore (default: 3).")

class ReActPromptInput(PromptInput):
    """Input schema for ReAct (Reason + Act) Prompting style."""
    style: Literal["react"] = "react"
    max_iterations: Optional[int] = Field(3, ge=1, le=10, description="Maximum reasoning-action iterations (default: 3).")

class InContextPromptInput(PromptInput):
    """Input schema for In-Context Learning Prompting style."""
    style: Literal["in_context"] = "in_context"
    context: Optional[str] = Field(None, description="Optional context to include in the prompt.")

class EmotionPromptInput(PromptInput):
    """Input schema for Emotion Prompting style."""
    style: Literal["emotion"] = "emotion"
    emotion: Optional[str] = Field("excited", description="Emotion to infuse in the prompt (e.g., excited, empathetic).")

class RolePromptInput(PromptInput):
    """Input schema for Role Prompting style."""
    style: Literal["role"] = "role"
    role_persona: Optional[str] = Field("expert", description="The professional role to assign to the AI for refinement.")

class FewShotPromptInput(PromptInput):
    """Input schema for Few-Shot Prompting style."""
    style: Literal["few_shot"] = "few_shot"
    examples: Optional[List[dict]] = Field(None, description="List of example input-output pairs, e.g., [{'input': 'x', 'output': 'y'}].")

class SelfConsistencyPromptInput(PromptInput):
    """Input schema for Self-Consistency Prompting style."""
    style: Literal["self_consistency"] = "self_consistency"
    samples: Optional[int] = Field(3, ge=2, le=10, description="Number of samples to generate for consistency voting (default: 3).")

class MetaPromptingInput(PromptInput):
    """Input schema for Meta Prompting style."""
    style: Literal["meta_prompting"] = "meta_prompting"
    iterations: Optional[int] = Field(2, ge=1, le=5, description="Number of iterations to improve the prompt (default: 2).")

class LeastToMostPromptInput(PromptInput):
    """Input schema for Least-to-Most Prompting style."""
    style: Literal["least_to_most"] = "least_to_most"
    sub_tasks: Optional[List[str]] = Field(None, description="Optional list of sub-tasks to break down the prompt.")

class MultiTaskPromptInput(PromptInput):
    """Input schema for Multi-Task Prompting style."""
    style: Literal["multi_task"] = "multi_task"
    tasks: Optional[List[str]] = Field(None, description="List of related tasks to include in the prompt.")

class TaskDecompositionPromptInput(PromptInput):
    """Input schema for Task Decomposition Prompting style."""
    style: Literal["task_decomposition"] = "task_decomposition"
    sub_steps: Optional[List[str]] = Field(None, description="Optional list of sub-steps to decompose the task.")

class ConstrainedPromptInput(PromptInput):
    """Input schema for Constrained Prompting style."""
    style: Literal["constrained"] = "constrained"
    max_words: Optional[int] = Field(None, ge=1, description="Maximum word count for the refined prompt.")
    output_format: Optional[str] = Field(None, description="Desired output format (e.g., bullet points, JSON).")

class GeneratedKnowledgePromptInput(PromptInput):
    """Input schema for Generated Knowledge Prompting style."""
    style: Literal["generated_knowledge"] = "generated_knowledge"
    facts_count: Optional[int] = Field(3, ge=1, le=10, description="Number of facts to generate before refining (default: 3).")

class AutomaticPromptEngineeringInput(PromptInput):
    """Input schema for Automatic Prompt Engineering (APE) style."""
    style: Literal["ape"] = "ape"
    optimization_goal: Optional[str] = Field("clarity", description="Goal for prompt optimization (e.g., clarity, brevity).")

class DirectionalStimulusPromptInput(PromptInput):
    """Input schema for Directional Stimulus Prompting style."""
    style: Literal["directional_stimulus"] = "directional_stimulus"
    focus: Optional[str] = Field(None, description="Specific focus area for the prompt (e.g., practical applications).")

RefineRequest = Union[
    ZeroShotPromptInput, OneShotPromptInput, ChainOfThoughtPromptInput,
    TreeOfThoughtPromptInput, ReActPromptInput, InContextPromptInput,
    EmotionPromptInput, RolePromptInput, FewShotPromptInput,
    SelfConsistencyPromptInput, MetaPromptingInput, LeastToMostPromptInput,
    MultiTaskPromptInput, TaskDecompositionPromptInput, ConstrainedPromptInput,
    GeneratedKnowledgePromptInput, AutomaticPromptEngineeringInput,
    DirectionalStimulusPromptInput
]