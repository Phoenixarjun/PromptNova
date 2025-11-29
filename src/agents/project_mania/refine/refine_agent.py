from typing import Any, List
from langchain_core.prompts import PromptTemplate
from src.agents.prompt_agent import PromptAgent

class RefineAgent(PromptAgent):
    """Applies improvements to the template."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    def refine(self, user_input: str, **kwargs) -> str:
        return user_input

    def apply_changes(self, current_template: str, suggestions: List[str]) -> str:
        prompt = PromptTemplate(
            input_variables=["template", "suggestions"],
            template="""You are an Expert Editor. Improve the following prompt template based on the provided suggestions.

Current Template:
{template}

Suggestions for Improvement:
{suggestions}

**Instructions:**
- Apply the suggestions while maintaining the original structure and intent.
- Ensure the tone remains consistent.
- Do not remove variables unless asked.

Return the IMPROVED TEMPLATE only.
"""
        )
        chain = prompt | self.llm
        return chain.invoke({
            "template": current_template,
            "suggestions": "\n- ".join(suggestions)
        }).content
