from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional

class Role(PromptAgent):
    """Agent for Role Prompting style."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
    
    def refine(self, user_input: str, role_persona: str = "expert", **kwargs) -> str:
        """Refines the user input using Role prompting."""
        role_template = PromptTemplate(
            input_variables=["user_input", "role_persona"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use role prompting: assign the AI the persona of '{role_persona}' to specialize the response, enhancing relevance and expertise.

User Input: {user_input}"""
        )
        chain = role_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "role_persona": role_persona
        }).content