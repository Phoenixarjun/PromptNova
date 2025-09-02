from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent

class Emotion(PromptAgent):
    """Agent for Emotion Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, emotion: str = "excited", **kwargs) -> str:
        """Refines the user input using Emotion prompting."""
        emotion_template = PromptTemplate(
            input_variables=["user_input", "emotion"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use emotion prompting: infuse the prompt with the specified emotion ({emotion}) to elicit more engaging, empathetic, or motivated responses from the AI. Ensure the emotion enhances the prompt without compromising clarity.

User Input: {user_input}"""
        )
        chain = emotion_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "emotion": emotion
        }).content