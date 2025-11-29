from typing import Any, List, Dict
from langchain_core.prompts import PromptTemplate
from src.agents.prompt_agent import PromptAgent

class GenericTemplateComposer(PromptAgent):
    """Composer for General Prompt Templates."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    def refine(self, user_input: str, **kwargs) -> str:
        # Not used directly
        return user_input

    def compose(self, intent: str, variables: List[str], router_plan: Dict[str, Any], prompt_length: str = "medium") -> str:
        length_instruction = ""
        if prompt_length == "low":
            length_instruction = "Keep the template concise, short, and to the point. Avoid unnecessary elaboration."
        elif prompt_length == "high":
            length_instruction = "Provide a highly detailed, comprehensive, and verbose template. Cover all aspects in depth."
        else:
            length_instruction = "Maintain a balanced length, providing sufficient detail without being overly verbose."

        prompt = PromptTemplate(
            input_variables=["intent", "variables", "plan", "length_instruction"],
            template="""You are an expert Prompt Engineer. Create a high-quality, reusable prompt template based on the following requirements.

User Intent: {intent}
Variables to Include: {variables}
Architect's Plan: {plan}
Length Requirement: {length_instruction}

The template MUST include:
1. **Role Definition**: Clear persona for the AI.
2. **Context**: Background information based on the intent.
3. **Variables Section**: Explicitly list the variables like {{variable_name}}.
4. **Instructions**: Step-by-step rules and logic.
5. **Output Formatting**: Define how the output should look.

**Rules:**
- Use the variables exactly as provided: {variables}.
- Do NOT hallucinate variables not listed.
- Keep it professional and zero-shot (unless specified otherwise).
- The output should be the RAW TEMPLATE itself, ready to be used.
- Adhere strictly to the length requirement: {length_instruction}

Begin Template:
"""
        )
        chain = prompt | self.llm
        return chain.invoke({
            "intent": intent,
            "variables": ", ".join([f"{{{v}}}" for v in variables]),
            "plan": str(router_plan),
            "length_instruction": length_instruction
        }).content
