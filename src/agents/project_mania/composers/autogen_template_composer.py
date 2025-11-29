from typing import Any, List, Dict
from langchain_core.prompts import PromptTemplate
from src.agents.prompt_agent import PromptAgent

class AutogenTemplateComposer(PromptAgent):
    """Composer for AutoGen Script Templates."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    def refine(self, user_input: str, **kwargs) -> str:
        return user_input

    def compose(self, intent: str, variables: List[str], router_plan: Dict[str, Any], prompt_length: str = "medium") -> str:
        length_instruction = ""
        if prompt_length == "low":
            length_instruction = "Keep the script concise. Use minimal agents and simple interaction logic."
        elif prompt_length == "high":
            length_instruction = "Create a comprehensive and detailed script. Include complex interaction flows, detailed system messages, and robust error handling."
        else:
            length_instruction = "Maintain a balanced script, ensuring sufficient detail for agents and interactions without over-complicating."

        prompt = PromptTemplate(
            input_variables=["intent", "variables", "plan", "length_instruction"],
            template="""You are an expert in Microsoft AutoGen. Generate a robust AutoGen python script based on the user's intent.

User Intent: {intent}
Variables to Inject: {variables}
Architect's Plan: {plan}
Complexity/Length Requirement: {length_instruction}

**Requirements:**
1. **Agents**: Define UserProxyAgent and AssistantAgent(s) with system messages.
2. **Config**: Include llm_config setup (use placeholders for keys).
3. **Interaction**: Define the initiate_chat call.
4. **Termination**: Define clear termination criteria (e.g., "TERMINATE").
5. **Variables**: Inject {variables} into system messages or initial prompts.

**Style:**
- Modular, reusable Python code.
- Clear comments explaining the flow.
- Adhere to the complexity requirement: {length_instruction}

Output the Python code only.
"""
        )
        chain = prompt | self.llm
        return chain.invoke({
            "intent": intent,
            "variables": ", ".join([f"{{{v}}}" for v in variables]),
            "plan": str(router_plan),
            "length_instruction": length_instruction
        }).content
