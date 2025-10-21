import json
import re
from typing import Any, Dict

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from src.logger import logger
from ..prompt_agent import PromptAgent
from ..refine.update_evaluator import UpdateEvaluator


class PromptOutput(BaseModel):
    refined_prompt: str = Field(..., description="The full refined prompt string")
    explanation: str = Field(..., description="Explanation of the improvements made")


class FinalPrompt(PromptAgent):
    """Agent for integrating refined responses into a final prompt robustly."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.evaluator = UpdateEvaluator(llm)
        # Wrap LLM with structured output for models that support it
        self.structured_llm = llm.with_structured_output(PromptOutput)

    async def refine(self, user_input: str, **kwargs) -> Dict[str, str]:
        refined_responses = kwargs.get("refined_responses", {})
        type_prompts = kwargs.get("type_prompts", {})
        if not refined_responses and not type_prompts:
            raise ValueError("No refined or type prompts provided for integration.")
        return await self.integrate(user_input=user_input, **kwargs)

    async def integrate(self, user_input: str, **kwargs) -> Dict[str, str]:
        refined_responses = kwargs.get("refined_responses", {})
        type_prompts = kwargs.get("type_prompts", {})
        framework = kwargs.get("framework", "")
        style = kwargs.get("style")
        suggestions = kwargs.get("suggestions")
        selected_model = kwargs.get("selected_model", "")

        framework_response = refined_responses.get(framework, "")
        if not framework_response:
            framework_response = next(iter(refined_responses.values()), "")

        # Sanitize inputs to remove any code fences
        framework_response = re.sub(r'```[a-zA-Z]*\n?|```', '', framework_response)
        type_prompts_str = json.dumps(type_prompts, indent=2)
        type_prompts_str = re.sub(r'```[a-zA-Z]*\n?|```', '', type_prompts_str)

        # Base template content
        base_template = f'''
You are a world-class prompt engineer with 20+ years of experience. Your task is to synthesize a final, refined, and actionable prompt.

**Primary Framework:** {{framework}}

**Instructions:**
1.  **Foundation**: Use the **Primary Framework Response** as the core structure for the new prompt. This is your starting point.
2.  **Layered Blending**: Intelligently integrate relevant concepts from the **Supporting Prompt Type Snippets** to enrich the main prompt. Do not just tack them on; weave them into the core structure to enhance clarity, add constraints, or provide better examples.
3.  **Completeness**: The final output must be a complete, standalone, and actionable prompt ready for an LLM.
4.  **Clarity and Effectiveness**: Ensure the final prompt is clear, effective, and perfectly aligned with the primary framework's goals.
5.  **No Meta-Text**: The `refined_prompt` output MUST NOT include any meta-text, commentary, or conversational filler like "Okay, here's your prompt". The prompt should be direct and to the point, starting with the core request.
6.  **Long-Form and Detailed**: Always provide a detailed, well-defined, and comprehensive long-form prompt for the user, one that follows the full framework carefully and is structured as if you're creating your own agent.
7.  **Code Block Naming Constraint:** Never return a generic triple-backtick fence alone. Always specify a meaningful language or context, e.g., ```sql, ```json, ```python etc., when returning code blocks.

**Primary Framework Response:**
{{framework_response}}

**Supporting Prompt Type Snippets:**
{{type_prompts}}

**User Input:**
{{user_input}}
'''

        # Model-specific output instructions
        if selected_model.lower() == "groq":
            output_instructions = '''
**Output Format:**
Respond ONLY with a valid JSON object.
Do NOT include any Markdown code fences.
Your JSON object must have exactly two keys:
- "refined_prompt": string containing the complete final prompt
- "explanation": string explaining the improvements
'''
        else:
            output_instructions = '''
**Output Format:**
Respond ONLY with a valid JSON object enclosed in ```json```.
Your JSON object must have exactly two keys:
- "refined_prompt": string containing the complete final prompt
- "explanation": string explaining the improvements
'''

        final_template = base_template + output_instructions

        integration_template = PromptTemplate(
            input_variables=["framework_response", "type_prompts", "user_input", "framework"],
            template=final_template
        )

        response: PromptOutput

        if selected_model.lower() == "groq":
            logger.info("Using Groq model (no JSON fences)...")
            chain = integration_template | self.llm
            response_content = await chain.ainvoke({
                "framework_response": framework_response,
                "type_prompts": type_prompts_str,
                "user_input": user_input,
                "framework": framework
            })

            raw_json_str = getattr(response_content, "content", str(response_content)).strip()
            raw_json_str = re.sub(r'```json|```', '', raw_json_str).strip()

            try:
                response_data = json.loads(raw_json_str)
                response = PromptOutput(**response_data)
            except (json.JSONDecodeError, TypeError) as e:
                logger.error(f"Failed to parse Groq JSON: {e}")
                logger.error(f"Raw response: {raw_json_str}")
                return {
                    "refined_prompt": "Error: Could not parse model output.",
                    "explanation": f"The Groq model returned malformed JSON. Raw output: {raw_json_str}"
                }
        else:
            logger.info("Using structured output model...")
            chain = integration_template | self.structured_llm
            response = await chain.ainvoke({
                "framework_response": framework_response,
                "type_prompts": type_prompts_str,
                "user_input": user_input,
                "framework": framework
            })

        refined_prompt = response.refined_prompt.strip()
        explanation = response.explanation.strip()

        # Self-evaluation
        evaluation_result = self.evaluator.evaluate(
            user_prompt=user_input,
            generated_prompt=refined_prompt,
            suggestions=suggestions,
            style=style,
            framework=framework
        )

        if evaluation_result is None:
            explanation += "\n\n**Self-Evaluation:** Could not be performed due to an internal error."
        elif evaluation_result.get("status") == "no":
            eval_summary = evaluation_result.get("summary") or {}
            eval_points = eval_summary.get("key_points", [])
            eval_guidance = eval_summary.get("guidance", "")
            explanation += (
                "\n\n**Self-Evaluation Feedback:** The generated prompt has issues."
                f"\n- Issues: {'; '.join(eval_points) if eval_points else 'None provided'}"
                f"\n- Guidance: {eval_guidance or 'No guidance available'}"
            )
        else:
            explanation += "\n\n**Self-Evaluation:** Passed."

        return {
            "refined_prompt": refined_prompt,
            "explanation": explanation
        }
