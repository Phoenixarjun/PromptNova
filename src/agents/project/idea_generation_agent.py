from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Any

class IdeaGenerationAgent(PromptAgent):
    """Agent that generates ideas and features from a simple prompt."""

    def __init__(self, llm: Any):
        super().__init__(llm)

    async def refine(self, user_input: str, **kwargs) -> str:
        """
        Brainstorms features and concepts based on the user's input.

        Args:
            user_input: The user's initial prompt (e.g., "Create a web app for task management.").

        Returns:
            A string containing a list of brainstormed ideas and features.
        """
        template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are a creative and experienced Product Manager and a UI/UX Web Developer, renowned for your ability to transform a simple idea into a well-defined product concept. Your task is to brainstorm a comprehensive list of features and concepts for the given user request.

**User Request:** 
"{user_input}"

**Your Task:**
Based on the user request, generate a detailed list of potential features, user roles, and key concepts. Think broadly and deeply. Consider:
- **Core Functionality:** What are the absolute must-have features?
- **User Roles:** Who are the different types of users (e.g., admin, standard user, guest)?
- **UI/UX Design:** What are the key UI components and design considerations? Suggest a color palette and overall aesthetic.
- **Web Development:** What would be a suitable tech stack for the frontend and backend?
- **Secondary Features:** What are the "nice-to-have" features that would enhance the user experience?
- **Potential Integrations:** What other services or APIs could this product connect with?
- **Monetization (if applicable):** How could this product generate revenue?

**Output Format:**
Provide your response as a clear, well-organized, and detailed bulleted list.

**Brainstormed Features and Concepts:**
"""
        )
        chain = template | self.llm
        response = await chain.ainvoke({"user_input": user_input})
        return response.content