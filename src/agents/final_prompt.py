from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, Any, Optional
import json
import re
from src.logger import logger


class FinalPrompt(PromptAgent):
    """Agent for integrating refined responses into a final prompt robustly."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs) -> str:
        refined_responses = kwargs.get("refined_responses", {})
        type_prompts = kwargs.get("type_prompts", {})
        framework = kwargs.get("framework", "")
        if not refined_responses and not type_prompts:
            raise ValueError("No refined or type prompts provided for integration.")
        return await self.integrate(refined_responses, type_prompts, user_input, framework)

    async def integrate(
            self, refined_responses: Dict, type_prompts: Dict, user_input: str, framework: str
    ) -> str:

        # Extract the primary framework response
        framework_response = refined_responses.get(framework, "")
        if not framework_response:
            # Fallback: use the first available response
            framework_response = next(iter(refined_responses.values()), "")

        integration_template = PromptTemplate(
            input_variables=["framework_response", "user_input", "framework", "available_types"],
            template="""You are a world-class prompt engineer with 20+ years of experience. Your task is to create a 
refined, actionable prompt based on the user's input and the primary framework response.

**Primary Framework:** {framework}
**Available Prompt Types:** {available_types}

**Instructions:**
1. Refine the prompt using the primary framework response as the foundation.
2. Optionally incorporate useful elements from other prompt types if they enhance the primary framework.
3. The refined prompt should be a complete, standalone prompt ready for an LLM.
4. Focus on clarity, effectiveness, and alignment with the primary framework.
5. Do NOT include any meta-text or commentary inside the prompt itself.
6. Always provide a detailed, well-defined, and comprehensive long prompt for the user one that follows the full framework carefully and is structured as if you’re creating your own agent.


**Primary Framework Response:**
{framework_response}

**User Input:**
{user_input}

**Output Format:**
Respond ONLY with a JSON object enclosed in ```json ... ``` with:
- "refined_prompt": the full refined prompt string (properly escaped)
- "explanation": explanation of improvements and how you incorporated the framework approach

All strings must be properly escaped for JSON.
"""
        )

        # Get available types for context
        available_types = list(type_prompts.keys())

        chain = integration_template | self.llm
        response = await chain.ainvoke({
            "framework_response": framework_response,
            "user_input": user_input,
            "framework": framework,
            "available_types": ", ".join(available_types)
        })

        raw_response = getattr(response, "content", str(response))

        def extract_json(text: str) -> str:
            """Extracts a JSON object from a string, including from within markdown fences."""
            # Remove markdown fences
            text = re.sub(r"```(json|prompt)?", "", text, flags=re.IGNORECASE).strip()

            # Find the first '{' and the last '}'
            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1 and end > start:
                return text[start:end + 1]
            return ""

        def attempt_parse(text: str) -> Optional[Dict]:
            """Tries to parse text as JSON, returns None on failure."""
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return None

        # Attempt 1: Parse the raw response directly.
        response_data = attempt_parse(raw_response)

        # Attempt 2: If the first attempt fails, extract from markdown fences and parse that.
        if not response_data:
            json_from_fences = extract_json(raw_response)
            if json_from_fences:
                response_data = attempt_parse(json_from_fences)

        # Check if parsing was successful and the required key exists.
        if response_data and "refined_prompt" in response_data:
            refined_prompt = response_data.get("refined_prompt", "")
            explanation = response_data.get("explanation", "")

            # Format the final output
            prompt_part = f"**Refined Prompt:**\n```\n{refined_prompt.strip()}\n```"
            explanation_part = f"**Explanation of Improvements and Rationale:**\n{explanation.strip()}"

            return f"{prompt_part}\n\n{explanation_part}"

        else:
            # If parsing fails, create a sensible fallback using the framework response
            logger.warning("JSON parsing failed, creating fallback prompt from framework response")

            # Create a clean fallback prompt
            fallback_prompt = self._create_fallback_prompt(framework_response, user_input, framework)
            explanation = "Created prompt based on primary framework response due to integration issues."

            prompt_part = f"**Refined Prompt:**\n```\n{fallback_prompt}\n```"
            explanation_part = f"**Explanation:**\n{explanation}"

            return f"{promback_part}\n\n{explanation_part}"

    def _create_fallback_prompt(self, framework_response: str, user_input: str, framework: str) -> str:
        """Create a fallback prompt when integration fails."""
        # Extract the main content from the framework response
        # Remove any meta-commentary or explanations
        lines = framework_response.split('\n')
        prompt_lines = []

        # Look for the actual prompt content (usually after explanations)
        in_prompt_section = False

        for line in lines:
            if '```' in line or 'prompt:' in line.lower() or 'instruction:' in line.lower():
                in_prompt_section = True
                continue
            if in_prompt_section and line.strip():
                prompt_lines.append(line)

        if prompt_lines:
            # Use the extracted prompt content
            cleaned_prompt = '\n'.join(prompt_lines).strip()
        else:
            # Fallback: use the original framework response with basic cleaning
            cleaned_prompt = framework_response.replace('**Refined Prompt:**', '').replace('```', '').strip()

        # Ensure it starts with a role assignment if missing
        if not cleaned_prompt.lower().startswith(('you are', 'assume the role', 'act as')):
            role_prefix = f"You are an expert following the {framework} framework. "
            cleaned_prompt = role_prefix + cleaned_prompt

        return cleaned_prompt