from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Dict, List, Any
import json
import re
from src.logger import logger
from pydantic import BaseModel, Field


class RefinedAgentPrompts(BaseModel):
    prompts: Dict[str, str]


def extract_json_from_text(text: str) -> str:
    """
    Safely extract the largest valid JSON block from messy LLM output.
    """
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("’", "'")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in LLM output.")

    json_str = text[start:end + 1]
    json_str = re.sub(r"\s+", " ", json_str)
    return json_str.strip()


class RefineAgent(PromptAgent):

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs):
        raise NotImplementedError("Use refine_based_on_feedback() instead.")

    async def refine_based_on_feedback(
        self, user_input: str, feedback: Dict,
        current_prompts: Dict[str, str], agents: List[str]
    ) -> Dict:

        refinement_template = PromptTemplate(
            input_variables=["user_input", "current_prompts", "feedback", "agents"],
            template="""
You are an expert prompt refiner. Improve ONLY the existing prompts based on the feedback.

STRICT RULES:
- Preserve original intent.
- Keep JSON compact.
- Do NOT add explanations outside JSON.
- Output ONLY JSON.

Your Output MUST follow exactly this shape:

{
  "prompts": {
      "agent1": "refined prompt",
      "agent2": "refined prompt"
  }
}

Anything else is invalid.

USER INPUT:
{user_input}

CURRENT PROMPTS:
{current_prompts}

FEEDBACK:
{feedback}

AGENTS:
{agents}
"""
        )

        chain = refinement_template | self.llm

        try:
            response_obj = await chain.ainvoke({
                "user_input": user_input,
                "current_prompts": json.dumps(current_prompts, indent=2),
                "feedback": json.dumps(feedback, indent=2),
                "agents": ", ".join(agents),
            })

            raw = (
                getattr(response_obj, "content", None)
                or getattr(response_obj, "text", None)
                or str(response_obj)
            ).strip()

            json_str = extract_json_from_text(raw)
            parsed = json.loads(json_str)

            if "prompts" not in parsed:
                raise ValueError("JSON missing 'prompts' key.")

            validated = RefinedAgentPrompts(**parsed)
            return validated.prompts

        except Exception as e:
            logger.error(f"RefineAgent failed: {e}")
            logger.warning("Returning original prompts.")
            return {agent: current_prompts.get(agent, "") for agent in agents}
