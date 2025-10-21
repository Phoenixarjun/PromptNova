from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional, List, Any
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
        """
        analyzer_template = PromptTemplate(
            input_variables=["original_prompt", "final_prompt", "user_feedback", "style", "framework"],
            template='''You are an expert Prompt Reviewer.

**Task:** Analyze the 'Final Prompt' based on the 'User Feedback' and provide structured improvement suggestions.

**Inputs:**
- Style: {style}
- Framework: {framework}
- Original Prompt: {original_prompt}
- Final Prompt: {final_prompt}
- User Feedback: {user_feedback}

**Instructions:**
1.  **Identify Deficiencies:** List specific weaknesses in the 'Final Prompt' according to the feedback.
2.  **Suggest Adjustments:** Must Provide actionable recommendations to fix the deficiencies.
3.  **Offer Phrasing (Optional):** Suggest alternative phrasing.

Your output must be a JSON object.'''
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
