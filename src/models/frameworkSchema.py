from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional
class FrameworkInput(BaseModel):
    """Base Pydantic model for all framework-based prompt refinement inputs."""
    user_input: str = Field(..., min_length=1, description="The original prompt text provided by the user.")
    framework: Literal[
        "co_star", "tcef", "crispe", "rtf", "ice", "craft", "ape",
        "pecra", "oscar", "rasce", "reflection", "flipped_interaction", "bab",
        "prompt", "soap", "clear", "prism", "grips", "app", "scope",
        "tool_oriented_prompting", "neuro_symbolic_prompting", "dynamic_context_windows",
        "meta_cognitive_prompting", "prompt_ensembles"
    ] = Field(..., description="The desired prompt refinement framework.")

class CoStarInput(FrameworkInput):
    """Input schema for CO-STAR Framework."""
    framework: Literal["co_star"] = "co_star"
    context: Optional[str] = Field(None, description="Optional background context for the task.")
    objective: Optional[str] = Field(None, description="Optional goal of the task.")
    style: Optional[str] = Field(None, description="Optional style for the output (e.g., bullet points, narrative).")
    tone: Optional[str] = Field(None, description="Optional tone for the response (e.g., professional, friendly).")
    audience: Optional[str] = Field(None, description="Optional target audience for the response.")
    response_format: Optional[str] = Field(None, description="Optional format for the response (e.g., summary, table).")

class TcefInput(FrameworkInput):
    """Input schema for TCEF Framework."""
    framework: Literal["tcef"] = "tcef"
    task: Optional[str] = Field(None, description="Optional task description to clarify the action.")
    context: Optional[str] = Field(None, description="Optional background context for the task.")
    example: Optional[str] = Field(None, description="Optional example to guide the AI's response.")
    format: Optional[str] = Field(None, description="Optional output format (e.g., table, list).")

class CrispeInput(FrameworkInput):
    """Input schema for CRISPE Framework."""
    framework: Literal["crispe"] = "crispe"
    role: Optional[str] = Field(None, description="Optional role or expertise to assign to the AI (e.g., senior strategist).")
    insight: Optional[str] = Field(None, description="Optional focus area for deep analysis (e.g., data-driven insights).")
    style: Optional[str] = Field(None, description="Optional style for the output (e.g., concise, detailed).")
    persona: Optional[str] = Field(None, description="Optional persona for the AI (e.g., pragmatic PM).")
    example: Optional[str] = Field(None, description="Optional example to demonstrate the desired output.")

class RtfInput(FrameworkInput):
    """Input schema for RTF Framework."""
    framework: Literal["rtf"] = "rtf"
    role: Optional[str] = Field(None, description="Optional role for the AI (e.g., UX designer).")
    task: Optional[str] = Field(None, description="Optional task description to define the action.")
    format: Optional[str] = Field(None, description="Optional output format (e.g., step-by-step list, diagram).")

class IceInput(FrameworkInput):
    """Input schema for ICE Framework."""
    framework: Literal["ice"] = "ice"
    instruction: Optional[str] = Field(None, description="Optional clear instruction for the AI.")
    context: Optional[str] = Field(None, description="Optional background context for the task.")
    example: Optional[str] = Field(None, description="Optional example to guide the AI's response.")

class CraftInput(FrameworkInput):
    """Input schema for CRAFT Framework."""
    framework: Literal["craft"] = "craft"
    capability: Optional[str] = Field(None, description="Optional AI capability to leverage (e.g., data analysis).")
    role: Optional[str] = Field(None, description="Optional role for the AI (e.g., data scientist).")
    action: Optional[str] = Field(None, description="Optional specific action to perform.")
    format: Optional[str] = Field(None, description="Optional output format (e.g., table, report).")
    tone: Optional[str] = Field(None, description="Optional tone for the response (e.g., technical, persuasive).")

class ApeInput(FrameworkInput):
    """Input schema for APE Framework."""
    framework: Literal["ape"] = "ape"
    action: Optional[str] = Field(None, description="Optional specific action to perform.")
    purpose: Optional[str] = Field(None, description="Optional purpose or goal of the task.")
    expectation: Optional[str] = Field(None, description="Optional expected output requirements (e.g., ranked list).")

class PecraInput(FrameworkInput):
    """Input schema for PECRA Framework."""
    framework: Literal["pecra"] = "pecra"
    purpose: Optional[str] = Field(None, description="Optional goal of the task (e.g., persuade executives).")
    expectation: Optional[str] = Field(None, description="Optional expected output (e.g., one-paragraph argument).")
    context: Optional[str] = Field(None, description="Optional background context for the task.")
    request: Optional[str] = Field(None, description="Optional specific request for the AI.")
    audience: Optional[str] = Field(None, description="Optional target audience (e.g., company founders).")

class OscarInput(FrameworkInput):
    """Input schema for OSCAR Framework."""
    framework: Literal["oscar"] = "oscar"
    objective: Optional[str] = Field(None, description="Optional goal of the task (e.g., build an MVP).")
    scope: Optional[str] = Field(None, description="Optional boundaries of the task.")
    constraints: Optional[str] = Field(None, description="Optional limits (e.g., budget, time).")
    assumptions: Optional[str] = Field(None, description="Optional assumptions for the task.")
    results: Optional[str] = Field(None, description="Optional expected results (e.g., report with metrics).")

class RasceInput(FrameworkInput):
    """Input schema for RASCE Framework."""
    framework: Literal["rasce"] = "rasce"
    role: Optional[str] = Field(None, description="Optional role for the AI (e.g., project management consultant).")
    action: Optional[str] = Field(None, description="Optional specific action to perform.")
    steps: Optional[List[str]] = Field(None, description="Optional list of steps to break down the task.")
    constraints: Optional[str] = Field(None, description="Optional constraints (e.g., time limits).")
    examples: Optional[str] = Field(None, description="Optional examples to guide the AI.")

class ReflectionInput(FrameworkInput):
    """Input schema for Reflection Pattern Framework."""
    framework: Literal["reflection"] = "reflection"
    review_criteria: Optional[str] = Field(None, description="Optional criteria for self-assessment (e.g., clarity, accuracy).")

class FlippedInteractionInput(FrameworkInput):
    """Input schema for Flipped Interaction Pattern Framework."""
    framework: Literal["flipped_interaction"] = "flipped_interaction"
    question_count: Optional[int] = Field(5, ge=1, le=10, description="Optional number of clarifying questions to ask (default: 5).")

class BabInput(FrameworkInput):
    """Input schema for Before-After-Bridge (BAB) Framework."""
    framework: Literal["bab"] = "bab"
    before: Optional[str] = Field(None, description="Optional description of the current state.")
    after: Optional[str] = Field(None, description="Optional description of the desired state.")
    bridge: Optional[str] = Field(None, description="Optional description of how to transition from current to desired state.")


class PromptFrameworkInput(FrameworkInput):
    framework: Literal["prompt"] = "prompt"
    context: Optional[str] = Field(None, description="Optional background context for the task.")
    style: Optional[str] = Field(None, description="Optional style for the response (e.g., bullet points, narrative).")
    tone: Optional[str] = Field(None, description="Optional tone for the response (e.g., professional, friendly).")
    audience: Optional[str] = Field(None, description="Optional target audience for the response.")
    response_format: Optional[str] = Field(None, description="Optional format for the response (e.g., summary, table).")

class SoapInput(FrameworkInput):
    framework: Literal["soap"] = "soap"
    sections: Optional[List[str]] = Field(["Subjective", "Objective", "Assessment", "Plan"],
                                          description="Optional sections to include in the SOAP response.")
    tone: Optional[str] = Field(None, description="Optional tone for the output (e.g., professional, concise).")
    format: Optional[str] = Field(None, description="Optional output format (e.g., bullet points, paragraph).")

class ClearInput(FrameworkInput):
    framework: Literal["clear"] = "clear"
    steps: Optional[int] = Field(3, ge=1, le=10, description="Optional number of steps to break down the task (default: 3).")
    style: Optional[str] = Field(None, description="Optional style for presenting steps (e.g., numbered, bulleted).")
    audience: Optional[str] = Field(None, description="Optional target audience for the instructions.")

class PrismInput(FrameworkInput):
    framework: Literal["prism"] = "prism"
    perspectives: Optional[int] = Field(3, ge=1, le=10, description="Optional number of perspectives to consider (default: 3).")
    focus_area: Optional[str] = Field(None, description="Optional specific focus area for analysis.")
    format: Optional[str] = Field(None, description="Optional output format (e.g., table, bullet points).")

class GripsInput(FrameworkInput):
    framework: Literal["grips"] = "grips"
    granularity: Optional[str] = Field("medium", description="Optional granularity of the output (low, medium, high).")
    context: Optional[str] = Field(None, description="Optional background context for the task.")
    examples: Optional[str] = Field(None, description="Optional examples to guide the AI's response.")

class AppFrameworkInput(FrameworkInput):
    framework: Literal["app"] = "app"
    target_platform: Optional[str] = Field(None, description="Optional target platform for the app (e.g., web, mobile).")
    audience: Optional[str] = Field(None, description="Optional target audience for the app.")
    style: Optional[str] = Field(None, description="Optional style for output messages or instructions.")

class ScopeInput(FrameworkInput):
    framework: Literal["scope"] = "scope"
    boundaries: Optional[str] = Field(None, description="Optional boundaries for the task (e.g., time, budget, resources).")
    priority: Optional[str] = Field(None, description="Optional priority level of the task (e.g., high, medium, low).")
    outcome_focus: Optional[str] = Field(None, description="Optional expected outcome focus for the AI response.")

# ------------------ Advanced / Specialized Frameworks ------------------

class ToolOrientedPromptingInput(FrameworkInput):
    framework: Literal["tool_oriented_prompting"] = "tool_oriented_prompting"
    tools: Optional[List[str]] = Field(None, description="Optional list of external tools to integrate with the prompt.")
    sequence: Optional[str] = Field(None, description="Optional execution sequence for combining prompts and tools.")
    context: Optional[str] = Field(None, description="Optional background context for tool usage.")

class NeuroSymbolicPromptingInput(FrameworkInput):
    framework: Literal["neuro_symbolic_prompting"] = "neuro_symbolic_prompting"
    logic_rules: Optional[str] = Field(None, description="Optional symbolic logic rules to guide reasoning.")
    focus_area: Optional[str] = Field(None, description="Optional domain or topic for combining logic and LLM output.")
    explanation_depth: Optional[str] = Field("medium", description="Optional level of explanation detail (low, medium, high).")

class DynamicContextWindowsInput(FrameworkInput):
    framework: Literal["dynamic_context_windows"] = "dynamic_context_windows"
    max_window_size: Optional[int] = Field(2000, description="Optional maximum token length for context windows.")
    prioritization_strategy: Optional[str] = Field("recent_first", description="Optional strategy for prioritizing context (recent_first, important_first).")
    retain_history: Optional[bool] = Field(True, description="Whether to retain previous interactions in context.")

class MetaCognitivePromptingInput(FrameworkInput):
    framework: Literal["meta_cognitive_prompting"] = "meta_cognitive_prompting"
    confidence_threshold: Optional[float] = Field(0.7, description="Optional confidence threshold for self-reflection and output verification.")
    introspection_depth: Optional[str] = Field("medium", description="Optional level of self-reflection detail (low, medium, high).")
    explanation_style: Optional[str] = Field(None, description="Optional style for meta-cognitive explanations (concise, detailed).")

class PromptEnsemblesInput(FrameworkInput):
    framework: Literal["prompt_ensembles"] = "prompt_ensembles"
    strategies: Optional[List[str]] = Field(None, description="Optional list of different prompting strategies to blend.")
    weightings: Optional[List[float]] = Field(None, description="Optional weights for each strategy (must match the number of strategies).")
    output_combination_method: Optional[str] = Field("majority_vote", description="Optional method to combine outputs (majority_vote, average, weighted_average).")




FrameworkRequest = Union[
    CoStarInput, TcefInput, CrispeInput, RtfInput, IceInput, CraftInput, ApeInput,
    PecraInput, OscarInput, RasceInput, ReflectionInput, FlippedInteractionInput, BabInput,
    PromptFrameworkInput, SoapInput, ClearInput, PrismInput, GripsInput, AppFrameworkInput,
    ScopeInput, ToolOrientedPromptingInput, NeuroSymbolicPromptingInput,
    DynamicContextWindowsInput, MetaCognitivePromptingInput, PromptEnsemblesInput
]