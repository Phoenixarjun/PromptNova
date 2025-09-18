from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, List
from src.agents.feedback_analyzer_agent import FeedbackAnalyzerAgent, ReviewSuggestions
from src.agents.prompt_updater_agent import PromptUpdaterAgent
from src.agents.update_evaluator import UpdateEvaluator
from src.logger import logger
import asyncio

class UpdateState(TypedDict):
    """Represents the state of the prompt update workflow."""
    original_prompt: str
    final_prompt: str  # This is the prompt being iteratively refined
    user_feedback: str
    style: Optional[List[str]]
    framework: Optional[str]
    suggestions: Optional[ReviewSuggestions]
    evaluation: Optional[Dict]
    iteration: int

class UpdatePipeline:
    """A pipeline to update a prompt based on user feedback using a graph-based approach."""
    def __init__(self, api_key: Optional[str] = None):
        self.max_iterations = 3
        self.review_agent = FeedbackAnalyzerAgent(api_key=api_key)
        self.refiner_agent = PromptUpdaterAgent(api_key=api_key)
        self.evaluator_agent = UpdateEvaluator(api_key=api_key)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(UpdateState)

        async def analyze_feedback_node(state: UpdateState) -> Dict:
            logger.info("Node: Analyzing feedback...")
            suggestions = await asyncio.to_thread(
                self.review_agent.analyze,
                state["original_prompt"],
                state["final_prompt"],
                state["user_feedback"],
                state["style"],
                state["framework"],
            )
            logger.info(f"Generated suggestions: {suggestions.dict()}")
            return {"suggestions": suggestions}

        async def update_prompt_node(state: UpdateState) -> Dict:
            logger.info(f"Node: Updating prompt (Iteration {state['iteration']})...")
            suggestions_to_use = {}
            # On the first iteration, use the initial suggestions from the feedback analyzer.
            if state['iteration'] == 0:
                if state.get("suggestions"):
                    suggestions_to_use = state["suggestions"].dict()
            # On subsequent iterations, use the guidance from the evaluator.
            else:
                if state.get("evaluation") and state["evaluation"].get("status") == "no":
                    # The guidance from the evaluator becomes the new set of suggestions.
                    summary = state["evaluation"].get("summary", {})
                    suggestions_to_use = {
                        "deficiencies": summary.get("key_points", []),
                        "adjustments": [summary.get("guidance", "")] if summary.get("guidance") else [],
                        "suggestions": [] # No new suggestions from evaluator
                    }

            if not suggestions_to_use:
                logger.warning("No suggestions found to update prompt. Returning current prompt.")
                return {"final_prompt": state["final_prompt"]}

            updated_prompt = await asyncio.to_thread(
                self.refiner_agent.update,
                state["final_prompt"],
                suggestions_to_use,
                state["style"],
                state["framework"],
            )
            logger.info(f"Generated updated prompt for this iteration: {updated_prompt}")
            return {"final_prompt": updated_prompt}

        async def evaluate_update_node(state: UpdateState) -> Dict:
            logger.info(f"Node: Evaluating updated prompt (Iteration {state['iteration']})...")
            suggestions_dict = state["suggestions"].dict() if state.get("suggestions") else {}
            evaluation = await asyncio.to_thread(
                self.evaluator_agent.evaluate,
                state["original_prompt"],
                state["final_prompt"],
                suggestions_dict,
                state["style"],
                state["framework"],
            )
            logger.info(f"Evaluation result: {evaluation}")
            return {"evaluation": evaluation, "iteration": state["iteration"] + 1}

        def should_continue(state: UpdateState) -> str:
            logger.info("Conditional Edge: Checking 'should_continue'...")
            if state.get("evaluation") and state["evaluation"].get("status") == "yes":
                logger.info("Decision: Evaluation successful. Ending loop.")
                return "end"
            if state.get("iteration", 0) >= self.max_iterations:
                logger.info("Decision: Max iterations reached. Ending loop.")
                return "end"
            logger.info("Decision: Evaluation failed. Looping back to update prompt.")
            return "continue"

        workflow.add_node("analyze_feedback", analyze_feedback_node)
        workflow.add_node("update_prompt", update_prompt_node)
        workflow.add_node("evaluate_update", evaluate_update_node)

        workflow.set_entry_point("analyze_feedback")
        workflow.add_edge("analyze_feedback", "update_prompt")
        workflow.add_edge("update_prompt", "evaluate_update")
        workflow.add_conditional_edges(
            "evaluate_update",
            should_continue,
            {"continue": "update_prompt", "end": END},
        )

        return workflow.compile()

    async def run(
        self,
        original_prompt: str,
        final_prompt: str,
        user_feedback: str,
        style: Optional[List[str]],
        framework: Optional[str],
    ) -> str:
        """
        Executes the feedback analysis and prompt refinement workflow.
        """
        logger.info("Starting prompt update pipeline...")
        initial_state: UpdateState = {
            "original_prompt": original_prompt,
            "final_prompt": final_prompt,
            "user_feedback": user_feedback,
            "style": style,
            "framework": framework,
            "suggestions": None,
            "evaluation": None,
            "iteration": 0,
        }
        final_state = await self.graph.ainvoke(initial_state)
        logger.info(f"Update pipeline finished. Final prompt: {final_state['final_prompt']}")
        return final_state['final_prompt']