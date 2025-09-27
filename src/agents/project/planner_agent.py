from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any, Dict

class PlannerAgent(PromptAgent):
    """Agent that plans the structure and flow of the JSON prompt."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs) -> str:
        """
        Plans the structure of the application based on generated ideas.

        Args:
            user_input: The user's initial prompt.
            **kwargs: Expects 'ideas' from the idea generation step.

        Returns:
            A string describing the planned structure (e.g., API endpoints, DB schema).
        """
        ideas = kwargs.get("ideas", "")

        template = PromptTemplate(
            input_variables=["user_input", "ideas"],
            template="""You are a Lead Software Planner and UI/UX Strategist with extensive experience in translating product requirements into actionable technical and design plans. Your task is to create a high-level structural plan for a new application based on the user's goal and brainstormed ideas.

**Input:**
- **User's Goal:** {user_input}
- **Brainstormed Ideas & Features (including UI/UX concepts):** 
{ideas}

**Your Task:**
Based on the user's goal and domain, create a structural plan. This plan should be a blueprint for the development and design teams.

1.  **Analyze Domain:** First, determine if the project is primarily `frontend`, `backend`, or `full-stack` based on the user's goal.
2.  **Plan Accordingly:**
    - If `frontend`, focus heavily on **UI Components** and **User Flow**. Use the brainstormed UI/UX concepts to define components (e.g., 'Login Page', 'Dashboard View', 'Settings Modal') and describe how they connect to create a seamless user experience.
    - If `backend`, focus on **API Endpoints** (RESTful endpoints with methods, paths, and purpose) and **Database Schema** (tables, columns, types like `users(id, email)`).
    - If `full-stack`, provide a balanced plan covering **API Endpoints**, **Database Schema**, and **UI Components** with their user flow.

**Structural Plan:**"""
        )
        chain = template | self.llm
        response = await chain.ainvoke({
            "user_input": user_input,
            "ideas": ideas
        })
        return response.content
