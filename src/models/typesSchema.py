from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional

class PromptInput(BaseModel):
    """Base Pydantic model for all prompt refinement inputs."""
    user_input: str = Field(..., min_length=1, description="The original prompt text provided by the user.")
    style: Literal[
        "zero_shot", "one_shot", "cot", "tot", "react", "in_context", "emotion", "role",
        "few_shot", "self_consistency", "meta_prompting", "least_to_most", "multi_task",
        "task_decomposition", "constrained", "generated_knowledge", "automatic_prompt_engineering", "directional_stimulus",
        "chain_of_verification", "skeleton_of_thought", "graph_of_thoughts", "plan_and_solve",
        "maieutic_prompting", "reflexion_type", "chain_of_density", "active_prompt",
        "retrieval_augmented_prompting", "multi_agent_debate", "persona_switching",
        "scaffolded_prompting", "deliberation_prompting", "context_expansion", "goal_oriented_prompting"
    ] = Field(..., description="The desired prompt refinement style.")
    api_key: Optional[str] = Field(None, description="User's API key for the LLM.")

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
    style: Literal["automatic_prompt_engineering"] = "automatic_prompt_engineering"
    optimization_goal: Optional[str] = Field("clarity", description="Goal for prompt optimization (e.g., clarity, brevity).")

class DirectionalStimulusPromptInput(PromptInput):
    """Input schema for Directional Stimulus Prompting style."""
    style: Literal["directional_stimulus"] = "directional_stimulus"
    focus: Optional[str] = Field(None, description="Specific focus area for the prompt (e.g., practical applications).")

class ChainOfVerificationInput(PromptInput):
    style: Literal["chain_of_verification"] = "chain_of_verification"
    verification_steps: Optional[int] = Field(3, ge=1, le=10, description="Number of verification steps to perform.")
    output_format: Optional[str] = Field("structured", description="Format for verification output (structured, text, table).")

class SkeletonOfThoughtInput(PromptInput):
    style: Literal["skeleton_of_thought"] = "skeleton_of_thought"
    focus_points: Optional[int] = Field(3, ge=1, le=10, description="Number of focus points in the thought skeleton.")
    detail_level: Optional[str] = Field("medium", description="Level of detail in skeleton (low, medium, high).")

class GraphOfThoughtsInput(PromptInput):
    style: Literal["graph_of_thoughts"] = "graph_of_thoughts"
    nodes: Optional[int] = Field(5, ge=1, le=20, description="Number of nodes/steps in the thought graph.")
    edges_strategy: Optional[str] = Field("logical", description="Strategy to connect nodes (logical, sequential, random).")

class PlanAndSolveInput(PromptInput):
    style: Literal["plan_and_solve"] = "plan_and_solve"
    plan_steps: Optional[int] = Field(3, ge=1, le=10, description="Number of planning steps before solution.")
    solution_detail: Optional[str] = Field("concise", description="Detail level for solution (concise, detailed).")

class MaieuticPromptingInput(PromptInput):
    style: Literal["maieutic_prompting"] = "maieutic_prompting"
    question_depth: Optional[int] = Field(3, ge=1, le=10, description="Depth of guided questioning for eliciting answers.")
    reflection: Optional[bool] = Field(True, description="Whether to include reflective feedback at each step.")

class ReflexionTypeInput(PromptInput):
    style: Literal["reflexion_type"] = "reflexion_type"
    reflection_criteria: Optional[str] = Field("clarity, accuracy", description="Criteria for self-reflection evaluation.")
    iterations: Optional[int] = Field(2, ge=1, le=5, description="Number of refinement iterations to perform.")

class ChainOfDensityInput(PromptInput):
    style: Literal["chain_of_density"] = "chain_of_density"
    density_level: Optional[str] = Field("medium", description="Density of reasoning steps (low, medium, high).")
    step_format: Optional[str] = Field("text", description="Format for each reasoning step (text, bullet, table).")

class ActivePromptInput(PromptInput):
    style: Literal["active_prompt"] = "active_prompt"
    adaptivity: Optional[str] = Field("dynamic", description="How adaptive the prompt should be (static, dynamic).")
    feedback_integration: Optional[bool] = Field(True, description="Whether to use user feedback to adjust prompt.")

class RetrievalAugmentedPromptingInput(PromptInput):
    style: Literal["retrieval_augmented_prompting"] = "retrieval_augmented_prompting"
    knowledge_sources: Optional[List[str]] = Field(None, description="External sources/databases to retrieve knowledge from.")
    retrieval_limit: Optional[int] = Field(5, description="Max number of retrieved items to use in the prompt.")

class MultiAgentDebateInput(PromptInput):
    style: Literal["multi_agent_debate"] = "multi_agent_debate"
    agents_count: Optional[int] = Field(3, ge=2, le=10, description="Number of agents participating in the debate.")
    consensus_method: Optional[str] = Field("majority_vote", description="Method for deciding final output (majority_vote, weighted).")

class PersonaSwitchingInput(PromptInput):
    style: Literal["persona_switching"] = "persona_switching"
    personas: Optional[List[str]] = Field(None, description="List of personas to switch between.")
    switch_frequency: Optional[int] = Field(1, description="Frequency of persona switching per prompt/response.")

class ScaffoldedPromptingInput(PromptInput):
    style: Literal["scaffolded_prompting"] = "scaffolded_prompting"
    scaffold_levels: Optional[int] = Field(3, ge=1, le=10, description="Number of scaffold levels to provide incremental guidance.")
    detail_per_level: Optional[str] = Field("medium", description="Amount of detail per scaffold level (low, medium, high).")

class DeliberationPromptingInput(PromptInput):
    style: Literal["deliberation_prompting"] = "deliberation_prompting"
    passes: Optional[int] = Field(2, ge=1, le=5, description="Number of deliberation passes for refining output.")
    reflection: Optional[bool] = Field(True, description="Include reflection on each deliberation pass.")

class ContextExpansionInput(PromptInput):
    style: Literal["context_expansion"] = "context_expansion"
    max_expansion_tokens: Optional[int] = Field(500, description="Maximum number of tokens to expand context.")
    prioritize_relevant: Optional[bool] = Field(True, description="Whether to prioritize relevant context over all available info.")

class GoalOrientedPromptingInput(PromptInput):
    style: Literal["goal_oriented_prompting"] = "goal_oriented_prompting"
    goal: Optional[str] = Field(None, description="Optional goal the AI should focus on achieving.")
    success_criteria: Optional[str] = Field("accuracy, completeness", description="Criteria for evaluating success of the output.")
    guidance_level: Optional[str] = Field("medium", description="Level of guidance to enforce (low, medium, high).")


RefineRequest = Union[
    ZeroShotPromptInput, OneShotPromptInput, ChainOfThoughtPromptInput,
    TreeOfThoughtPromptInput, ReActPromptInput, InContextPromptInput,
    EmotionPromptInput, RolePromptInput, FewShotPromptInput,
    SelfConsistencyPromptInput, MetaPromptingInput, LeastToMostPromptInput,
    MultiTaskPromptInput, TaskDecompositionPromptInput, ConstrainedPromptInput,
    GeneratedKnowledgePromptInput, AutomaticPromptEngineeringInput,
    DirectionalStimulusPromptInput, ChainOfVerificationInput,
    SkeletonOfThoughtInput, GraphOfThoughtsInput, PlanAndSolveInput,
    MaieuticPromptingInput, ReflexionTypeInput, ChainOfDensityInput,
    ActivePromptInput, RetrievalAugmentedPromptingInput, MultiAgentDebateInput,
    PersonaSwitchingInput, ScaffoldedPromptingInput, DeliberationPromptingInput,
    ContextExpansionInput, GoalOrientedPromptingInput
]