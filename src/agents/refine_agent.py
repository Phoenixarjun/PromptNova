from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, List

class RefineAgent(PromptAgent):
    """Agent for refining based on feedback."""
    
    def __init__(self):
        super().__init__()
    
    def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("RefineAgent is designed for feedback-based refinement via refine_based_on_feedback.")
    
    def refine_based_on_feedback(self, user_input: str, feedback: Dict, agents: List[str]) -> Dict:
        """Refines the low-scoring agents based on feedback and returns updated responses."""
        refinement_template = PromptTemplate(
            input_variables=["user_input", "feedback", "agents"],
            template="""You are an expert prompt refiner with 25+ years of experience. Based on the provided feedback, refine the prompts for the low-scoring agents ({agents}) for the given user input. Use the feedback's summary key points to address deficiencies and improve alignment with the user's intent. Preserve correct agents (100% score) unchanged. Return a dictionary with refined prompts for each agent.

User Input: {user_input}
Feedback: {feedback}
Agents: {agents}"""
        )
        chain = refinement_template | self.llm
        response = chain.invoke({"user_input": user_input, "feedback": str(feedback), "agents": ', '.join(agents)}).content
        return eval(response)  # Assuming the output is a dict string