from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
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
        """
        updater_template = PromptTemplate(
            input_variables=["final_prompt", "review_suggestions", "style", "framework"],
            template='''You are a prompt refining expert.

**Task:** Integrate the following adjustments into the 'Current Prompt' while preserving its structure.

**Inputs:**
- Style: {style}
- Framework: {framework}
- Current Prompt: {final_prompt}
- Adjustments: {review_suggestions}

**Instructions:**
1.  Apply the 'Adjustments' to the 'Current Prompt'.
2.  Do NOT rewrite, reorder, or remove any other sections of the prompt.
3.  Output ONLY the updated prompt text.'''
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
