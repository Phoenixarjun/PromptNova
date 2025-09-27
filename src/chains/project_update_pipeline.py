from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, Any
from src.agents.project_refine.project_feedback_analyzer import ProjectFeedbackAnalyzerAgent, ReviewSuggestions
from src.agents.project_refine.project_updater_agent import ProjectUpdaterAgent
from src.agents.project_refine.project_evaluator_agent import ProjectEvaluatorAgent
from src.logger import logger
import asyncio
import json

class ProjectUpdateState(TypedDict):
    """Represents the state of the project update workflow."""
    original_user_prompt: str
    project_artifacts: Dict  # This contains the artifacts being iteratively refined
    user_feedback: str
    suggestions: Optional[ReviewSuggestions]
    evaluation: Optional[Dict]
    iteration: int

class ProjectUpdatePipeline:
    """A pipeline to update project artifacts based on user feedback using a graph-based approach."""
    def __init__(self, llm: Any):
        self.max_iterations = 3
        self.review_agent = ProjectFeedbackAnalyzerAgent(llm=llm)
        self.refiner_agent = ProjectUpdaterAgent(llm=llm)
        self.evaluator_agent = ProjectEvaluatorAgent(llm=llm)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ProjectUpdateState)

        async def analyze_feedback_node(state: ProjectUpdateState) -> Dict:
            logger.info("Node: Analyzing project feedback...")
            suggestions = await asyncio.to_thread(
                self.review_agent.analyze,
                state["original_user_prompt"],
                state["project_artifacts"],
                state["user_feedback"],
            )
            logger.info(f"Generated project suggestions: {suggestions.dict()}")
            return {"suggestions": suggestions}

        async def update_project_node(state: ProjectUpdateState) -> Dict:
            logger.info(f"Node: Updating project artifacts (Iteration {state['iteration']})...")
            suggestions_to_use = {}
            if state['iteration'] == 0:
                if state.get("suggestions"):
                    suggestions_to_use = state["suggestions"].dict()
            else:
                if state.get("evaluation") and state["evaluation"].get("status") == "no":
                    summary = state["evaluation"].get("summary")
                    if summary:
                        suggestions_to_use = {
                            "deficiencies": summary.get("key_points", []),
                            "adjustments": [summary.get("guidance", "")] if summary.get("guidance") else [],
                            "suggestions": []
                        }

            if not suggestions_to_use:
                logger.warning("No suggestions found to update project. Returning current artifacts.")
                return {"project_artifacts": state["project_artifacts"]}

            updated_artifacts = await asyncio.to_thread(
                self.refiner_agent.update,
                json.dumps(state["project_artifacts"]),
                suggestions_to_use,
            )
            logger.info("Generated updated project artifacts for this iteration.")
            return {"project_artifacts": updated_artifacts}

        async def evaluate_update_node(state: ProjectUpdateState) -> Dict:
            logger.info(f"Node: Evaluating updated project artifacts (Iteration {state['iteration']})...")
            suggestions_dict = state["suggestions"].dict() if state.get("suggestions") else {}
            evaluation = await asyncio.to_thread(
                self.evaluator_agent.evaluate,
                state["original_user_prompt"],
                state["project_artifacts"],
                suggestions_dict,
            )
            logger.info(f"Project evaluation result: {evaluation}")
            return {"evaluation": evaluation, "iteration": state["iteration"] + 1}

        def should_continue(state: ProjectUpdateState) -> str:
            logger.info("Conditional Edge: Checking 'should_continue' for project...")
            if state.get("evaluation") and state["evaluation"].get("status") == "yes":
                logger.info("Decision: Project evaluation successful. Ending loop.")
                return "end"
            if state.get("iteration", 0) >= self.max_iterations:
                logger.info("Decision: Max iterations reached for project. Ending loop.")
                return "end"
            logger.info("Decision: Project evaluation failed. Looping back to update project.")
            return "continue"

        workflow.add_node("analyze_feedback", analyze_feedback_node)
        workflow.add_node("update_project", update_project_node)
        workflow.add_node("evaluate_update", evaluate_update_node)

        workflow.set_entry_point("analyze_feedback")
        workflow.add_edge("analyze_feedback", "update_project")
        workflow.add_edge("update_project", "evaluate_update")
        workflow.add_conditional_edges(
            "evaluate_update",
            should_continue,
            {"continue": "update_project", "end": END},
        )

        return workflow.compile()

    async def run(
        self,
        original_user_prompt: str,
        project_artifacts: Dict,
        user_feedback: str,
    ) -> Dict:
        """
        Executes the feedback analysis and project artifact refinement workflow.
        """
        logger.info("Starting project update pipeline...")
        initial_state: ProjectUpdateState = {
            "original_user_prompt": original_user_prompt,
            "project_artifacts": project_artifacts,
            "user_feedback": user_feedback,
            "suggestions": None,
            "evaluation": None,
            "iteration": 0,
        }
        final_state = await self.graph.ainvoke(initial_state)
        logger.info(f"Project update pipeline finished. Final artifacts: {final_state['project_artifacts']}")
        return final_state['project_artifacts']
