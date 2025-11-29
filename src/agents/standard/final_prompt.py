import json
import re
from typing import Any, Dict, Optional

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from src.logger import logger
from ..prompt_agent import PromptAgent
from ..refine.update_evaluator import UpdateEvaluator


class PromptOutput(BaseModel):
    refined_prompt: str
    explanation: str


# -------- UNIVERSAL JSON EXTRACTOR (bulletproof) --------
def extract_json_block(text: str) -> Optional[str]:
    """
    Extracts the largest valid JSON-like block from any LLM output.
    Works even when LLM adds text, markdown, notes, broken fences, etc.
    """
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("’", "'").replace("`", "")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    candidate = text[start:end + 1]

    # collapse weird whitespace
    candidate = re.sub(r"\s+", " ", candidate).strip()

    return candidate


class FinalPrompt(PromptAgent):
    """Agent for integrating refined responses into a final prompt safely."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.evaluator = UpdateEvaluator(llm)
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

        # pick correct refined response
        framework_response = refined_responses.get(framework, "")
        if not framework_response:
            framework_response = next(iter(refined_responses.values()), "")

        # sanitize
        framework_response = re.sub(r"```.*?```", "", framework_response, flags=re.DOTALL)
        type_prompts_str = re.sub(
            r"```.*?```",
            "",
            json.dumps(type_prompts, indent=2),
            flags=re.DOTALL
        )

        # ------------- FULL BASE TEMPLATE (unchanged) --------------
        base_template = f"""
You are a world-class prompt engineer with 20+ years of experience. Your task is to synthesize a final, refined, and actionable prompt.

**Primary Framework:** {{framework}}

**Instructions:**
1. Use the Primary Framework Response as the base.
2. Blend in Supporting Prompt Type Snippets intelligently.
3. Produce a complete, standalone prompt.
4. Do NOT add meta text or conversational filler.
5. Code blocks must specify a language.
6. Keep the explanation concise.

**Primary Framework Response:**
{{framework_response}}

**Supporting Prompt Type Snippets:**
{{type_prompts}}

**User Input:**
{{user_input}}
"""

        output_instructions = """
**Output Format:**
Return ONLY a valid JSON object.
NO markdown.
Keys:
- "refined_prompt"
- "explanation"
"""

        final_template = base_template + output_instructions

        integration_template = PromptTemplate(
            input_variables=[
                "framework_response",
                "type_prompts",
                "user_input",
                "framework",
            ],
            template=final_template,
        )

        response = None

        # ---------- GROQ MODE ----------
        if selected_model.lower() == "groq":
            chain = integration_template | self.llm
            try:
                res = await chain.ainvoke({
                    "framework_response": framework_response,
                    "type_prompts": type_prompts_str,
                    "user_input": user_input,
                    "framework": framework,
                })

                raw = getattr(res, "content", str(res)).strip()
                json_str = extract_json_block(raw)

                if not json_str:
                    raise ValueError("No JSON found in Groq output")

                parsed = json.loads(json_str)
                response = PromptOutput(**parsed)

            except Exception as e:
                logger.error(f"Groq JSON error: {e}")
                return {
                    "refined_prompt": user_input,
                    "explanation": "Groq returned malformed JSON. Using original input.",
                }

        # ---------- STRUCTURED OUTPUT MODE ----------
        else:
            chain = integration_template | self.structured_llm
            try:
                response = await chain.ainvoke({
                    "framework_response": framework_response,
                    "type_prompts": type_prompts_str,
                    "user_input": user_input,
                    "framework": framework,
                })

            except Exception:
                logger.error("Structured output failed. Falling back to JSON extraction.")

                # fallback extraction
                raw = str(response)
                json_str = extract_json_block(raw)

                if not json_str:
                    return {
                        "refined_prompt": user_input,
                        "explanation": "Model failed to return valid JSON.",
                    }

                parsed = json.loads(json_str)
                response = PromptOutput(**parsed)

        # ------------- DEFENSIVE CHECKS -------------
        if response is None or not hasattr(response, "refined_prompt"):
            return {
                "refined_prompt": user_input,
                "explanation": "Invalid or missing response fields.",
            }

        refined_prompt = response.refined_prompt.strip()
        explanation = response.explanation.strip()

        # -------- SELF EVALUATION --------
        try:
            evaluation = self.evaluator.evaluate(
                user_prompt=user_input,
                generated_prompt=refined_prompt,
                suggestions=suggestions,
                style=style,
                framework=framework,
            )

            if evaluation and evaluation.get("status") == "no":
                summary = evaluation.get("summary") or {}
                issues = summary.get("key_points", [])
                guidance = summary.get("guidance", "")
                explanation += (
                    "\n\n**Self-Evaluation Feedback:** Issues detected."
                    f"\n- Issues: {', '.join(issues)}"
                    f"\n- Guidance: {guidance}"
                )
            else:
                explanation += "\n\n**Self-Evaluation:** Passed."

        except Exception as e:
            logger.warning(f"Self-evaluation failed: {e}")

        return {
            "refined_prompt": refined_prompt,
            "explanation": explanation,
        }
