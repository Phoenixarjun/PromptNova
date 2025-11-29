from typing import Any, List, Dict
from langchain_core.prompts import PromptTemplate
from src.agents.prompt_agent import PromptAgent

class CrewAITemplateComposer(PromptAgent):
    """Composer for CrewAI Configuration Templates."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    def refine(self, user_input: str, **kwargs) -> str:
        return user_input

    def compose(self, intent: str, variables: List[str], router_plan: Dict[str, Any], prompt_length: str = "medium") -> str:
        length_instruction = ""
        if prompt_length == "low":
            length_instruction = "Keep the configuration concise. Use minimal agents and tasks necessary."
        elif prompt_length == "high":
            length_instruction = "Create a comprehensive and detailed configuration. Include extensive backstories, detailed task descriptions, and multiple agents covering all aspects."
        else:
            length_instruction = "Maintain a balanced configuration, ensuring sufficient detail for agents and tasks without over-engineering."

        prompt = PromptTemplate(
            input_variables=["intent", "variables", "plan", "length_instruction"],
            template="""You are a Senior AI Engineer specializing in CrewAI. Generate a production-ready CrewAI configuration (Python code or YAML structure) based on the user's intent.

User Intent: {intent}
Variables to Inject: {variables}
Architect's Plan: {plan}
Complexity/Length Requirement: {length_instruction}

**Requirements:**
1. **Agents**: Define agents with Name, Role, Goal, Backstory.
2. **Tasks**: Define tasks with Description, Expected Output, and assigned Agent.
3. **Crew**: Orchestration logic (Process.sequential or hierarchical).
4. **Variables**: Use the provided placeholders {variables} where appropriate (e.g., in task descriptions or agent goals).

**Style:**
- Use Python syntax for CrewAI (Agent(), Task(), Crew()).
- Ensure code is clean and commented.
- Follow best practices for agent specificity.
- Adhere to the complexity requirement: {length_instruction}

Output the code/config only.
"""
        )
        chain = prompt | self.llm
        return chain.invoke({
            "intent": intent,
            "variables": ", ".join([f"{{{v}}}" for v in variables]),
            "plan": str(router_plan),
            "length_instruction": length_instruction
        }).content
