from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent

class GeneratedKnowledge(PromptAgent):
    """Agent for Generated Knowledge Prompting style."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, facts_count: int = 3, **kwargs) -> str:
        """Refines the user input using Generated Knowledge prompting."""
        generated_knowledge_template = PromptTemplate(
            input_variables=["user_input", "facts_count"],
            template="""You are an expert prompt engineer with 25+ years of experience. Transform the following raw, improper user input into a top-tier, expert-level prompt optimized for Gemini AI. The refined prompt should be clear, concise, specific, actionable, and structured with precise instructions. Use generated knowledge prompting: instruct the AI to first generate {facts_count} relevant facts, then use them to inform and enhance the final response for better factual accuracy.

User Input: {user_input}"""
        )
        chain = generated_knowledge_template | self.llm
        return chain.invoke({
            "user_input": user_input,
            "facts_count": facts_count
        }).content