from langchain.prompts import PromptTemplate
from ..prompt_agent import PromptAgent

class OneShot(PromptAgent):
    """Agent for One-Shot Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, example_input: str = None, example_output: str = None, **kwargs) -> str:
        """Refines the user input using One-Shot prompting."""
        one_shot_template = PromptTemplate(
            input_variables=["user_input", "example_input", "example_output"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI, OpenAI ChatGPT, or any large language model. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use a one-shot approach: include one relevant example to guide the AI, making the prompt more effective without multiple examples. The example should be tailored to demonstrate the desired output style, format, and quality. If no example is provided, generate a suitable one based on the input.

Example Input: {example_input}
Example Output: {example_output}

User Input: {user_input}"""
        )
        chain = one_shot_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "example_input": example_input or "Tell me about dogs.",
            "example_output": example_output or "Provide a detailed overview of dog breeds, including history, care tips, and common behaviors, structured in sections for readability."
        }).content