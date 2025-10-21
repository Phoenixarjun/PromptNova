from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any, Dict
import json
import re
from src.logger import logger

class EvaluationAgent(PromptAgent):
    """Agent that evaluates the generated JSON prompt."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs) -> Dict:
        """
        Evaluates the generated JSON prompt for quality and correctness.

        Args:
            user_input: The user's initial prompt.
            **kwargs: Expects 'json_prompt' to evaluate.

        Returns:
            A JSON string with evaluation results.
        """
        json_prompt = kwargs.get("json_prompt", "")

        template = PromptTemplate(
            input_variables=["user_input", "json_prompt"],
            template="""You are a meticulous and detail-oriented QA Engineer, UI/UX Analyst, and JSON Schema expert. Your primary role is to validate a generated JSON configuration against the original user request to ensure it is complete, correct, clear, and aligns with modern design and development principles.

**User's Original Goal:** 
{user_input}

**Generated JSON to Evaluate:**
            ```json
            {json_prompt}
            ```

**Evaluation Criteria:**
1.  **Completeness:** Does the JSON object fully capture all the requirements, features, and entities described in the user's goal? Are there any missing keys or sections (e.g., `techStack`, `uiComponents`, `features`)?
2.  **Correctness:** Is the JSON well-formed and syntactically valid? Are the data types appropriate for each value?
3.  **Design & UI/UX Cohesion:** Does the JSON specify a cohesive design direction? Check for the presence and sensibility of `techStack`, `uiComponents`, and a color scheme. Are the choices logical for the application's purpose?
4.  **Clarity & Best Practices:** Is the structure logical and easy to understand? Are the key names clear, consistent, and self-descriptive?

**Your Response:**
Provide your evaluation in a strict JSON format.
- If the generated JSON meets all criteria, respond with: `{{"status": "success", "issues": []}}`
- If there are any issues, respond with: `{{"status": "failure", "issues": ["A detailed list of specific, actionable issues to be fixed."]}}`

Example for failure: `{{"status": "failure", "issues": ["The 'authentication' feature is missing from the features list.", "The 'techStack' is missing a 'frontend' framework.", "A color palette should be suggested in the UI design details."]}}`

            Evaluation:"""
        )
        chain = template | self.llm
        response = await chain.ainvoke({
            "user_input": user_input,
            "json_prompt": json_prompt
        })

        # Basic parsing and fallback
        try:
            json_str = response.content
            match = re.search(r"```json\n(.*?)\n```", json_str, re.DOTALL)
            if match:
                json_str = match.group(1)

            return json.loads(json_str)
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Failed to parse evaluation response: {e}")
            return {"status": "failure", "issues": ["Failed to parse evaluation output."]}