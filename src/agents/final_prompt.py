from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from .update_evaluator import UpdateEvaluator
from typing import Dict, Any, Optional
import json
import re
from src.logger import logger


class FinalPrompt(PromptAgent):
    """Agent for integrating refined responses into a final prompt robustly."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.evaluator = UpdateEvaluator(llm)

    async def refine(self, user_input: str, **kwargs) -> str:
        refined_responses = kwargs.get("refined_responses", {})
        type_prompts = kwargs.get("type_prompts", {})
        if not refined_responses and not type_prompts:
            raise ValueError("No refined or type prompts provided for integration.")
        return await self.integrate(user_input=user_input, **kwargs)

    def _parse_json_response(self, text: str) -> Optional[Dict]:
        """Extracts and parses JSON, handling markdown fences and raw JSON."""

        # 1. JSON inside ```json fences
        match = re.search(r"```(?:json)?\s*({.*?})\s*```", text, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                return json.loads(json_str.strip())
            except json.JSONDecodeError:
                logger.error(f"Failed fenced JSON parse: {json_str}", exc_info=True)

        # 2. Fallback: first { ... last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end > start:
            json_str = text[start:end + 1]
            try:
                return json.loads(json_str.strip())
            except json.JSONDecodeError:
                logger.error(f"Failed raw JSON parse: {json_str}", exc_info=True)

        return None

    def _extract_prompt_directly(self, text: str) -> Dict[str, str]:
        """Extract prompt + explanation directly from markdown/text if no JSON found."""
        prompt_match = re.search(
            r"(?:\*\*Refined Prompt:\*\*|Refined Prompt:)\s*(.*?)(?=\n\n\*\*Explanation|\n\*\*Explanation|\Z)",
            text, re.DOTALL
        )
        explanation_match = re.search(
            r"(?:\*\*Explanation.*?:\*\*|Explanation:)\s*(.*)", text, re.DOTALL
        )

        refined_prompt = prompt_match.group(1).strip() if prompt_match else text.strip()
        explanation = explanation_match.group(1).strip() if explanation_match else "Generated prompt based on framework integration."

        # Strip any stray code fences
        refined_prompt = re.sub(r'^```[a-zA-Z]*\s*\n?', '', refined_prompt)
        refined_prompt = re.sub(r'\n?\s*```$', '', refined_prompt).strip()

        return {
            "refined_prompt": refined_prompt,
            "explanation": explanation
        }

    async def integrate(self, user_input: str, **kwargs) -> str:
        refined_responses = kwargs.get("refined_responses", {})
        type_prompts = kwargs.get("type_prompts", {})
        framework = kwargs.get("framework", "")
        style = kwargs.get("style")
        suggestions = kwargs.get("suggestions")

        framework_response = refined_responses.get(framework, "")
        if not framework_response:
            framework_response = next(iter(refined_responses.values()), "")

        integration_template = PromptTemplate(
            input_variables=["framework_response", "user_input", "framework", "type_prompts"],
            template='''You are a world-class prompt engineer with 20+ years of experience. Your task is to synthesize a final, refined, and actionable prompt.

**Primary Framework:** {framework}

**Instructions:**
1.  **Foundation**: Use the **Primary Framework Response** as the core structure for the new prompt. This is your starting point.
2.  **Layered Blending**: Intelligently integrate relevant concepts from the **Supporting Prompt Type Snippets** to enrich the main prompt. Do not just tack them on; weave them into the core structure to enhance clarity, add constraints, or provide better examples.
3.  **Completeness**: The final output must be a complete, standalone, and actionable prompt ready for an LLM.
4.  **Clarity and Effectiveness**: Ensure the final prompt is clear, effective, and perfectly aligned with the primary framework's goals.
5.  **No Meta-Text**: Do NOT include any meta-text or commentary inside the prompt itself.
6.  **Long-Form and Detailed**: Always provide a detailed, well-defined, and comprehensive long-form prompt for the user, one that follows the full framework carefully and is structured as if you're creating your own agent.

**Primary Framework Response:**
{framework_response}

**Supporting Prompt Type Snippets:**
{type_prompts}

**User Input:**
{user_input}

**Output Format:**
Respond ONLY with a JSON object enclosed in ```json``` with:
- "refined_prompt": the full refined prompt string (properly escaped)
- "explanation": a detailed explanation of the improvements made and how you blended the framework and type prompts.

All strings must be properly escaped for JSON.
'''
        )

        chain = integration_template | self.llm
        response = await chain.ainvoke({
            "framework_response": framework_response,
            "user_input": user_input,
            "framework": framework,
            "type_prompts": json.dumps(type_prompts, indent=2)
        })

        raw_response = getattr(response, "content", str(response))

        # --- Robust parsing pipeline ---
        response_data = self._parse_json_response(raw_response)
        if not response_data or "refined_prompt" not in response_data:
            logger.warning("JSON parsing failed, using direct extraction fallback")
            response_data = self._extract_prompt_directly(raw_response)

        refined_prompt = response_data.get("refined_prompt", "").strip()
        explanation = response_data.get("explanation", "").strip()

        # Final cleanup of fences
        if refined_prompt.startswith("```") and refined_prompt.endswith("```"):
            refined_prompt = re.sub(r'^```[a-zA-Z]*\s*\n?', '', refined_prompt)
            refined_prompt = re.sub(r'\n?\s*```$', '', refined_prompt).strip()

        # --- Self-evaluation ---
        logger.info("Performing self-evaluation on the generated prompt...")
        evaluation_result = self.evaluator.evaluate(
            user_prompt=user_input,
            generated_prompt=refined_prompt,
            suggestions=suggestions,
            style=style,
            framework=framework
        )

        if evaluation_result is None:
            logger.error("Self-evaluation returned None. Skipping feedback.")
            explanation += "\n\n**Self-Evaluation:** Could not be performed due to an internal error."
        elif evaluation_result.get("status") == "no":
            eval_summary = evaluation_result.get("summary", {})
            eval_points = eval_summary.get("key_points", [])
            eval_guidance = eval_summary.get("guidance", "")
            explanation += (
                "\n\n**Self-Evaluation Feedback:** The generated prompt has issues."
                f"\n- **Issues:** {'; '.join(eval_points)}"
                f"\n- **Guidance:** {eval_guidance}"
            )
        else:
            explanation += "\n\n**Self-Evaluation:** Passed."

        return f"**Refined Prompt:**\n{refined_prompt}\n\n**Explanation of Improvements and Rationale:**\n{explanation}"
