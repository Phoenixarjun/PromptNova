from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Optional, Dict, List, Any

class PromptUpdaterAgent(PromptAgent):
    """Agent that updates a prompt based on structured suggestions with strict constraints."""
    def __init__(self, llm: Any):
        super().__init__(llm)

    def update(
        self,
        final_prompt: str,
        review_suggestions: Dict,
        style: Optional[List[str]],
        framework: Optional[str],
    ) -> str:
        """
        Updates a prompt based on structured review suggestions.
        Constraints:
        - Preserve the structure and pattern of final_prompt.
        - Apply review_suggestions only as adjustments.
        - Ensure updated prompt aligns with required style and framework.
        """
        updater_template = PromptTemplate(
            input_variables=["final_prompt", "review_suggestions", "style", "framework"],
            template="""You are a world-class Prompt Engineering Expert with 20+ years of experience designing high-performance prompts for LLMs.
Your task: update the given prompt ONLY by integrating the review suggestions while strictly preserving its structure, sequence, and framework.
Do not remove or reorder sections. Do not rewrite the overall format. 
Simply refine the wording and inject the feedback so the final result is clear, polished, and exactly aligned with the required style and framework.

Current Prompt (must preserve structure):
{final_prompt}

Review Suggestions (to integrate without breaking structure):
{review_suggestions}

Required Prompting Types (Style): {style}
Required Prompting Framework: {framework}

Output ONLY the updated prompt text with the same structure as the input, adjusted to reflect the feedback and constraints. 
Do not add commentary, explanations, or metadata."""
        )
        chain = updater_template | self.llm
        return chain.invoke({
            "final_prompt": final_prompt,
            "review_suggestions": str(review_suggestions),
            "style": str(style) if style else "Not specified",
            "framework": framework if framework else "Not specified",
        }).content

    def refine(self, user_input: str, **kwargs) -> str:
        raise NotImplementedError("PromptUpdaterAgent uses the 'update' method, not 'refine'.")
