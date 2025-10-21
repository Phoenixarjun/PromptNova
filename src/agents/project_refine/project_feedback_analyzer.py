from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field

class ReviewSuggestions(BaseModel):
    """Structured output for prompt review suggestions."""
    deficiencies: List[str] = Field(
        description="Specific deficiencies in the project artifacts (e.g., unclear architecture, incomplete plan, misaligned with user prompt)."
    )
    adjustments: List[str] = Field(
        description="Actionable recommendations to correct deficiencies (e.g., 'clarify component interaction', 'add detailed steps for feature X', 'ensure plan covers all user requirements')."
    )
    suggestions: Optional[List[str]] = Field(
        None,
        description="Optional high-quality phrasing or structural alternatives to consider for the project artifacts."
    )

class ProjectFeedbackAnalyzerAgent(PromptAgent):
    """Agent that analyzes user feedback on project artifacts and generates structured suggestions."""
    def __init__(self, llm: Any):
        super().__init__(llm)
        self.structured_llm = self.llm.with_structured_output(ReviewSuggestions)

    def analyze(
        self,
        original_user_prompt: str,
        project_artifacts: Dict, # Contains architecture, plans, etc.
        user_feedback: str,
    ) -> ReviewSuggestions:
        """
        Analyzes project artifacts and user feedback to generate structured suggestions.
        """
        analyzer_template = PromptTemplate(
            input_variables=["original_user_prompt", "project_artifacts", "user_feedback"],
            template='''You are an expert Project Reviewer.

**Task:** Analyze the 'Current Project Artifacts' based on the 'User Feedback' and the 'Original User Prompt' to provide structured improvement suggestions.

**Inputs:**
- Original User Prompt: {original_user_prompt}
- Current Project Artifacts: {project_artifacts}
- User Feedback: {user_feedback}

**Instructions:**
1.  **Identify Deficiencies:** List specific weaknesses in the 'Current Project Artifacts' according to the feedback and original prompt.
2.  **Suggest Adjustments:** You MUST provide actionable recommendations to fix the deficiencies.
3.  **Offer Phrasing (Optional):** Suggest alternative phrasing or structural changes for clarity and completeness.

Your output must be a JSON object conforming to the required schema.
'''
        )
        chain = analyzer_template | self.structured_llm
        return chain.invoke({
            "original_user_prompt": original_user_prompt,
            "project_artifacts": str(project_artifacts),
            "user_feedback": user_feedback,
        })

    def refine(self, user_input: str, **kwargs) -> str:
        raise NotImplementedError("ProjectFeedbackAnalyzerAgent uses the 'analyze' method, not 'refine'.")
