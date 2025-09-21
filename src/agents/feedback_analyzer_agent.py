from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ReviewSuggestions(BaseModel):
    """Structured output for prompt review suggestions."""
    deficiencies: List[str] = Field(
        description="Specific deficiencies in the final prompt (e.g., missing context, vague tone, misaligned with style/framework, redundant or overly verbose)."
    )
    adjustments: List[str] = Field(
        description="Actionable recommendations to correct deficiencies (e.g., 'clarify instructions', 'align with {framework}', 'reduce length', 'add examples')."
    )
    suggestions: Optional[List[str]] = Field(
        None,
        description="Optional high-quality phrasing or stylistic alternatives to consider. Must remain faithful to the intended style and framework."
    )

class FeedbackAnalyzerAgent(PromptAgent):
    """Agent that analyzes feedback and generates structured suggestions."""
    def __init__(self, llm: Any):
        super().__init__(llm)
        self.structured_llm = self.llm.with_structured_output(ReviewSuggestions)

    def analyze(
        self,
        original_prompt: str,
        final_prompt: str,
        user_feedback: str,
        style: Optional[List[str]],
        framework: Optional[str],
    ) -> ReviewSuggestions:
        """
        Analyzes prompts and feedback to generate structured suggestions.
        Constraints:
        - Maintain fidelity to final_prompt structure.
        - Focus only on actionable refinements tied to feedback, style, and framework.
        - Output strictly follows ReviewSuggestions schema.
        """
        analyzer_template = PromptTemplate(
            input_variables=["original_prompt", "final_prompt", "user_feedback", "style", "framework"],
            template="""You are a world-class Prompt Engineering Expert with 20+ years of experience optimizing prompts for advanced LLMs.
Your role: act as an impartial, rigorous reviewer who provides only structured, actionable improvement insights.
Do not rewrite the prompt. Do not expand outside scope. Only diagnose deficiencies, propose adjustments, and optionally offer phrasing suggestions.

Guidelines:
- Stay focused on user feedback.
- Ensure recommendations explicitly align with the declared style and framework.
- Be precise, concise, and avoid generic advice.
- Output must strictly follow the JSON schema (ReviewSuggestions).

Original Prompt:
{original_prompt}

Final Generated Prompt (to evaluate):
{final_prompt}

User Feedback:
{user_feedback}

Prompting Types (Style): {style}
Prompting Framework: {framework}

Now analyze carefully and return:
1. Specific deficiencies in the final prompt.
2. Concrete, actionable adjustments to fix them.
3. Optional phrasing or stylistic suggestions that remain faithful to the required style/framework."""
        )
        chain = analyzer_template | self.structured_llm
        return chain.invoke({
            "original_prompt": original_prompt,
            "final_prompt": final_prompt,
            "user_feedback": user_feedback,
            "style": str(style) if style else "Not specified",
            "framework": framework if framework else "Not specified",
        })

    def refine(self, user_input: str, **kwargs) -> str:
        raise NotImplementedError("FeedbackAnalyzerAgent uses the 'analyze' method, not 'refine'.")
