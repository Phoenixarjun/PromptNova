from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent
from typing import List

class FewShot(PromptAgent):
    """Agent for Few-Shot Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, examples: List[dict] = None, **kwargs) -> str:
        """Refines the user input using Few-Shot prompting."""
        examples = examples or [{"input": "Tell me about dogs.", "output": "Provide a detailed overview of dog breeds, including history, care tips, and common behaviors, structured in sections for readability."}]
        examples_str = "\n".join([f"Example Input: {ex['input']}\nExample Output: {ex['output']}" for ex in examples])
        
        few_shot_template = PromptTemplate(
            input_variables=["user_input", "examples_str"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use few-shot prompting: include the provided examples to demonstrate the desired style, format, and quality, helping the AI mimic high-quality outputs.

{examples_str}

User Input: {user_input}"""
        )
        chain = few_shot_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "examples_str": examples_str
        }).content