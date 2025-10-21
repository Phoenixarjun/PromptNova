from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any, Dict, List
import json
import re
from src.logger import logger
from pydantic import BaseModel, Field


class RefinementAgent(PromptAgent):
    """Agent that refines a JSON prompt based on evaluation feedback."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs) -> str:
        """
        Refines a JSON prompt using feedback.

        Args:
            user_input: The user's initial prompt.
            **kwargs: Expects 'json_prompt' and 'issues'.

        Returns:
            A string containing the refined JSON prompt.
        """
        json_prompt = kwargs.get("json_prompt", "")
        issues = kwargs.get("issues", [])

        template = PromptTemplate(
            input_variables=["user_input", "json_prompt", "issues"],    
            template="""You are a Senior Software Engineer and UI/UX specialist specializing in debugging and refinement. Your task is to fix an incomplete or incorrect JSON object based on a list of identified issues, paying close attention to design and structural feedback.

**Original User Goal:** 
{user_input}

**Current (Incorrect) JSON:**
            ```json
            {json_prompt}
            ```

**Issues to Fix:**
            - {issues}
            
**Your Task:**
Rewrite the entire JSON object, correcting all the listed issues. This may involve adding missing sections (like `uiDesign` or `techStack`), correcting values, or restructuring parts of the JSON to meet the requirements. The final output must be a single, complete, and valid JSON object.

**CRITICAL INSTRUCTION:** Your output must be ONLY the raw JSON object, enclosed in ```json ... ```. Do not include any other text, explanations, or wrappers."""
        )
        chain = template | self.llm
        response = await chain.ainvoke({
            "user_input": user_input,
            "json_prompt": json_prompt,
            "issues": "\n- ".join(issues)
        })

        json_string = response.content
        # Use regex to find the JSON block and extract it
        match = re.search(r"```json\n(.*?)\n```", json_string, re.DOTALL)
        if match:
            return match.group(1).strip()
        return json_string.strip()