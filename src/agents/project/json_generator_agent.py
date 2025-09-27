from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any, Dict
import json
import re

class JSONGeneratorAgent(PromptAgent):
    """Agent that generates a structured JSON prompt that adapts to the user’s requirements."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs) -> Dict[str, str]:
        """
        Generates the final JSON prompt based on all gathered information.
        Args:
            user_input: The user's initial prompt.
            **kwargs: Expects 'ideas', 'plan', and 'architecture'.
        Returns:
            A dictionary containing the structured JSON prompt under the 'json' key.
        """
        ideas = kwargs.get("ideas", "")
        plan = kwargs.get("plan", "")
        architecture = kwargs.get("architecture", "")

        template = PromptTemplate(
            input_variables=["user_input", "ideas", "plan", "architecture"],
            template="""You are a Senior Software Engineer and Prompt Engineering specialist with a keen eye for UI/UX and design. 
Your task is to synthesize all available information into a single, comprehensive, and well-structured JSON object. 
This JSON must exactly reflect the **scope specified in the user's goal** (frontend only, backend only, or full-stack). 
Do NOT include sections that are irrelevant to the user's requirements.

**Source Information:**
1. **User's Goal / Scope:** {user_input}
2. **Brainstormed Ideas:**
{ideas}
3. **Structural Plan:**
{plan}
4. **Proposed Architecture (including Tech Stack and Design):**
{architecture}

**Your Task:**
Generate a single, clean, and well-formed JSON object that encapsulates all of the information above. Synthesize the technology stack and UI/UX design details from the architecture proposal.
- If the user only wants **frontend**, include only keys relevant to UI/UX (appName, description, userRoles, features, uiComponents, uiDesign, techStack).
- If the user only wants **backend**, include only backend keys (appName, description, userRoles, apiEndpoints, databaseSchema, techStack).
- If the user wants **full-stack**, include all relevant keys.
- You may introduce or omit keys dynamically to best match the user’s goal.

**JSON Schema Rules:**
- The root JSON object must always contain at least:
  - `appName`: A suitable name for the application.
  - `description`: A detailed description of the application's purpose and functionality.
  - `userRoles`: An array of strings listing the user roles with brief descriptions.
- Add other top-level keys based on the scope:
  - `techStack`: The technology stack from the architecture proposal.
  - `features`: A list of key features.
  - `uiComponents`: A list of UI components from the plan.
  - `apiEndpoints`: A list of API endpoints.
  - `databaseSchema`: The database schema definition.
  - `uiDesign`: If the scope includes a frontend, add this key. It should be an object containing `colorPalette`, `typography`, and `aesthetic` details from the architecture proposal.

**CRITICAL INSTRUCTION:** 
Your output must be a JSON object with a single key "json". 
The value of this key should be the complete, raw JSON object representing the project blueprint. 
Do not include any explanations or text outside of the JSON.

Example:
```json
{{"json": {{...the entire project blueprint, adapted to the user's goal...}} }}
```"""
        )

        chain = template | self.llm
        response = await chain.ainvoke({
            "user_input": user_input,
            "ideas": ideas,
            "plan": plan,
            "architecture": architecture
        })

        json_string = response.content
        match = re.search(r"```json\n(.*?)\n```", json_string, re.DOTALL)
        if match:
            json_string = match.group(1)
        try:
            return {"json": json_string}
        except (json.JSONDecodeError, AttributeError):
            return {"json": json_string}
