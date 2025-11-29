from typing import Any, Dict, List
from src.agents.project_mania.refine.analyze_agent import AnalyzeAgent
from src.agents.project_mania.refine.refine_agent import RefineAgent
from src.agents.project_mania.refine.evaluate_agent import EvaluateAgent
from src.logger import logger

class ProjectManiaRefinementPipeline:
    """
    Manages the Analyze -> Refine -> Evaluate loop for Project Mania.
    """
    def __init__(self, llm: Any):
        self.analyze_agent = AnalyzeAgent(llm)
        self.refine_agent = RefineAgent(llm)
        self.evaluate_agent = EvaluateAgent(llm)
        self.max_iterations = 3

    async def run(self, initial_template: str, intent: str) -> Dict[str, Any]:
        current_template = initial_template
        iteration_metadata = []

        for i in range(self.max_iterations):
            logger.info(f"Refinement Iteration {i+1}/{self.max_iterations}")

            # 1. Analyze
            analysis = self.analyze_agent.analyze(current_template, intent)
            logger.info(f"Analysis: {analysis}")

            # 2. Refine
            if analysis.get("suggestions"):
                current_template = self.refine_agent.apply_changes(current_template, analysis["suggestions"])
            
            # 3. Evaluate
            evaluation = self.evaluate_agent.evaluate(current_template, intent)
            logger.info(f"Evaluation: {evaluation}")

            iteration_metadata.append({
                "iteration": i + 1,
                "analysis": analysis,
                "evaluation": evaluation
            })

            if evaluation.get("success", False):
                logger.info("Template passed evaluation.")
                break
        
        return {
            "final_template": current_template,
            "metadata": iteration_metadata
        }
