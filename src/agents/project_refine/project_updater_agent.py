from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Dict, Any
from langchain_core.output_parsers import JsonOutputParser
import json

class ProjectUpdaterAgent(PromptAgent):
    """Agent that updates project artifacts based on structured suggestions."""
    def __init__(self, llm: Any):
        super().__init__(llm)
        self.parser = JsonOutputParser()

    def update(
        self,
        project_artifacts: str, # Expects a JSON string
        review_suggestions: Dict,
    ) -> Dict: # Returns a dictionary
        """
        Updates project artifacts based on structured review suggestions.
        """
        updater_template = PromptTemplate(
            template='''You are a project architect and planner.

**Task:** Integrate the following 'Adjustments' into the 'Current Project Artifacts' to produce a new, complete version.

**Inputs:**
- Current Project Artifacts (as a JSON string): {project_artifacts}
- Adjustments: {review_suggestions}

**Instructions:**
1.  Carefully analyze the 'Current Project Artifacts' and the 'Adjustments'.
2.  Apply the 'Adjustments' to create an updated version of the project artifacts.
3.  You MUST output ONLY the updated project artifacts as a single, raw JSON object.
4.  The JSON object must contain the full 'architecture' and 'plan' keys, and all other original keys.
{format_instructions}
''',
            input_variables=["project_artifacts", "review_suggestions"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        chain = updater_template | self.llm | self.parser
        response = chain.invoke({
            "project_artifacts": project_artifacts, # This is already a string from the pipeline
            "review_suggestions": str(review_suggestions),
        })
        return response

    def refine(self, user_input: str, **kwargs) -> str:
        raise NotImplementedError("ProjectUpdaterAgent uses the 'update' method, not 'refine'.")
