from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Optional, Dict, List

class PromptUpdaterAgent(PromptAgent):
    """Agent that updates a prompt based on structured suggestions."""
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)

    def update(
        self,
        final_prompt: str,
        review_suggestions: Dict,
        style: Optional[List[str]],
        framework: Optional[str],
    ) -> str:
        """Updates a prompt based on structured review suggestions."""
        updater_template = PromptTemplate(
            input_variables=["final_prompt", "review_suggestions", "style", "framework"],
            template="""You are an expert prompt refiner. Your task is to update the following prompt based on the provided suggestions, ensuring it adheres to the specified prompt engineering types (style) and framework. Apply the adjustments to create a new, improved prompt.

Current Prompt to be updated: 
{final_prompt}

Review Suggestions to apply:
{review_suggestions}

Required Prompting Types (Style): {style}
Required Prompting Framework: {framework}

Generate the new, updated prompt. Output ONLY the updated prompt text, with no additional commentary or explanation. The new prompt must conform to the required style and framework."""
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