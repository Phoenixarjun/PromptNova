from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any, Dict

class ArchitectAgent(PromptAgent):
    """Agent that designs the overall architecture of the JSON prompt."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs) -> str:
        """
        Designs the technical architecture based on the user prompt and generated ideas.

        Args:
            user_input: The user's initial prompt.
            **kwargs: Expects 'ideas' and 'plan' from previous steps.

        Returns:
            A string describing the proposed architecture.
        """
        ideas = kwargs.get("ideas", "")
        plan = kwargs.get("plan", "")

        template = PromptTemplate(
            input_variables=["user_input", "ideas", "plan"],
            template="""You are a Principal Solutions Architect and a UI/UX expert with over 20 years of experience designing scalable, robust, and aesthetically pleasing software systems. Your task is to create a comprehensive technical and design architecture proposal based on the provided project details.

**Project Context:**
- **User's Goal:** {user_input}
- **Brainstormed Features & Concepts (including UI/UX ideas):** 
{ideas}
- **Structural Plan (APIs, DB Schema, UI Components):** 
{plan}

**Your Task:**
Based on the context above, design a detailed technical and design architecture. Your proposal must include:
1.  **Technology Stack:** Based on the project's domain (frontend, backend, or full-stack), propose a specific and justified technology stack. For example:
    - `frontend`: React with Next.js, TailwindCSS.
    - `backend`: Python with FastAPI, PostgreSQL, Redis for caching.
    - `full-stack`: A combination of the above.
2.  **Design and UI/UX:** Based on the brainstormed ideas, suggest a cohesive design direction.
    - **Color Palette:** Propose a primary, secondary, and accent color scheme.
    - **Typography:** Suggest suitable fonts for headings and body text.
    - **Overall Aesthetic:** Describe the look and feel (e.g., modern, minimalist, playful).
3.  **High-Level Architecture:** Describe the system design (e.g., Microservices, Monolith, Serverless) relevant to the domain. Explain how components interact.
4.  **Data Flow:** Briefly explain the data flow for a key feature. If frontend-only, describe component data flow.
5.  **Scalability and Performance:** Mention relevant considerations for the specified domain.

            Architecture Proposal:"""
        )
        chain = template | self.llm
        response = await chain.ainvoke({
            "user_input": user_input,
            "ideas": ideas,
            "plan": plan
        })
        return response.content