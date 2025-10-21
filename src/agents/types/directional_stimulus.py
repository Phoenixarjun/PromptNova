from langchain_core.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import Optional, Any

class DirectionalStimulus(PromptAgent):
    """Agent for Directional Stimulus Prompting style."""
    
    def __init__(self, llm: Any):
        super().__init__(llm)
    
    def refine(self, user_input: str, focus: Optional[str] = None, **kwargs) -> str:
        """Refines the user input using Directional Stimulus prompting."""
        directional_stimulus_template = PromptTemplate(
            input_variables=["user_input", "focus"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use directional stimulus prompting: guide the AI with directional cues to focus on a specific aspect ({focus}), ensuring targeted and relevant outputs.

User Input: {user_input}"""
        )
        chain = directional_stimulus_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "focus": focus or "practical applications"
        }).content