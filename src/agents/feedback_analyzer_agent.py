from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class ReviewSuggestions(BaseModel):
    """Structured output for prompt review suggestions."""
    deficiencies: List[str] = Field(description="Specific deficiencies found in the final prompt (e.g., missing context, unclear instructions, overly verbose).")
    adjustments: List[str] = Field(description="Recommended adjustments to fix the deficiencies (e.g., 'make it shorter', 'be more direct', 'add examples').")
    suggestions: Optional[List[str]] = Field(None, description="Optional new phrasing or style tweaks to consider.")

class FeedbackAnalyzerAgent(PromptAgent):
    """Agent that analyzes feedback and generates structured suggestions."""
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
        # Use with_structured_output to ensure the LLM returns the desired JSON object
        self.structured_llm = self.llm.with_structured_output(ReviewSuggestions)

    def analyze(
        self,
        original_prompt: str,
        final_prompt: str,
        user_feedback: str,
        style: Optional[List[str]],
        framework: Optional[str],
    ) -> ReviewSuggestions:
        """Analyzes prompts and feedback to generate structured suggestions."""
        analyzer_template = PromptTemplate(
            input_variables=["original_prompt", "final_prompt", "user_feedback", "style", "framework"],
            template="""You are a world-class prompt engineering expert. Your task is to analyze the difference between an original prompt and a final generated prompt, taking into account user feedback, the prompt engineering types (style), and framework used. Generate structured recommendations for improvement.

Original Prompt: {original_prompt}
Final Generated Prompt: {final_prompt}
User Feedback: {user_feedback}
Prompting Types (Style): {style}
Prompting Framework: {framework}

Based on the user's feedback, and considering the applied styles and framework, identify specific deficiencies in the final prompt and recommend actionable adjustments. Provide optional suggestions for new phrasing if applicable."""
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