from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent

class InContext(PromptAgent):
    """Agent for In-Context Learning Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, context: str = None, **kwargs) -> str:
        """Refines the user input using In-Context Learning prompting."""
        in_context_template = PromptTemplate(
            input_variables=["user_input", "context"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use in-context learning: incorporate the provided context to 'teach' the AI on-the-fly, ensuring the prompt builds on this background for better relevance and accuracy. If no context is provided, infer a suitable one based on the input.

Context: {context}

User Input: {user_input}"""
        )
        chain = in_context_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "context": context or "Ensure responses are comprehensive and factually accurate."
        }).content