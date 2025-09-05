from langchain.prompts import PromptTemplate
from .prompt_agent import PromptAgent
from typing import Dict, List
import json
import re
from src.logger import logger

class RefineAgent(PromptAgent):
    """Agent for refining based on feedback."""
    
    def __init__(self):
        super().__init__()
    
    async def refine(self, user_input: str, **kwargs) -> str:
        """Placeholder refine method to satisfy abstract base class requirement."""
        raise NotImplementedError("RefineAgent is designed for feedback-based refinement via refine_based_on_feedback.")
    
    def refine_based_on_feedback(self, user_input: str, feedback: Dict, agents: List[str]) -> Dict:
        """Refines the low-scoring agents based on feedback and returns updated responses."""
        refinement_template = PromptTemplate(
            input_variables=["user_input", "feedback", "agents"],
            template="""You are an expert prompt refiner with 25+ years of experience. Based on the provided feedback, refine the prompts for the low-scoring agents ({agents}) for the given user input. Use the feedback's summary key points to address deficiencies and improve alignment with the user's intent. Preserve correct agents (100% score) unchanged. Return a VALID JSON dictionary with refined prompts for each agent, in the format: {{"agent1": "refined prompt1", "agent2": "refined prompt2", ...}}. Output ONLY the JSON object, no markdown, no extra text, no comments, and ensure all strings are properly escaped.

User Input: {user_input}
Feedback: {feedback}
Agents: {agents}"""
        )
        chain = refinement_template | self.llm
        response = chain.invoke({"user_input": user_input, "feedback": str(feedback), "agents": ', '.join(agents)}).content
        # Clean response to ensure valid JSON
        response = re.sub(r'^```json\s*|\s*```$', '', response, flags=re.MULTILINE)  # Remove markdown
        response = re.sub(r'[^\x00-\x7F]+', '', response)  # Remove non-ASCII characters
        response = re.sub(r'(?<!\\)"', r'\"', response)  # Escape unescaped quotes
        response = re.sub(r'\n+', ' ', response)  # Replace newlines with spaces
        response = response.strip()
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed in RefineAgent: {str(e)} - Response: {response}")
            # Fallback to a DSA-focused prompt based on user input
            return {
                agent: f"You are an expert in Data Structures and Algorithms. Provide a clear and concise solution for solving Data Structures and Algorithms (DAS) problems on LeetCode using the {agent} approach, including problem descriptions, optimized Python code, and brief explanations." 
                for agent in agents
            }