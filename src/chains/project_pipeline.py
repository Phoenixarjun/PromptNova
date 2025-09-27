from langgraph.graph import StateGraph, END
from typing import TypedDict, Any, Dict
from src.logger import logger
import re
import json
from src.agents.project import (
    IdeaGenerationAgent,
    PlannerAgent,
    ArchitectAgent,
    JSONGeneratorAgent,
    EvaluationAgent,
    RefinementAgent,
)


class BrainstormState(TypedDict):
    """Represents the state of the brainstorming and JSON generation workflow."""
    user_input: str
    ideas: str
    plan: str
    architecture: str
    json_prompt: str
    evaluation: Dict
    iteration: int

class ProjectPipeline:
    """A pipeline to generate a structured JSON prompt from a simple user idea."""

    def __init__(self, llm: Any):
        self.max_iterations = 3
        self.idea_agent = IdeaGenerationAgent(llm=llm)
        self.planner_agent = PlannerAgent(llm=llm)
        self.architect_agent = ArchitectAgent(llm=llm)
        self.generator_agent = JSONGeneratorAgent(llm=llm)
        self.evaluator_agent = EvaluationAgent(llm=llm)
        self.refiner_agent = RefinementAgent(llm=llm)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(BrainstormState)

        async def idea_generation_node(state: BrainstormState) -> Dict:
            logger.info("Node: Generating ideas...")
            ideas = await self.idea_agent.refine(state["user_input"])
            logger.info(f"Generated ideas: {ideas}")
            return {"ideas": ideas}

        async def planner_node(state: BrainstormState) -> Dict:
            logger.info("Node: Planning structure...")
            plan = await self.planner_agent.refine(state["user_input"], ideas=state["ideas"])
            logger.info(f"Generated plan: {plan}")
            return {"plan": plan}

        async def architect_node(state: BrainstormState) -> Dict:
            logger.info("Node: Designing architecture...")
            architecture = await self.architect_agent.refine(
                state["user_input"], ideas=state["ideas"], plan=state["plan"]
            )
            logger.info(f"Generated architecture: {architecture}")
            return {"architecture": architecture}

        async def generate_json_node(state: BrainstormState) -> Dict:
            logger.info("Node: Generating JSON prompt...")
            # The agent returns a dictionary: {"json": "..."}
            json_prompt_dict = await self.generator_agent.refine(
                state["user_input"],
                ideas=state["ideas"],
                plan=state["plan"],
                architecture=state["architecture"],
            )
            logger.info(f"Generated JSON prompt: {json_prompt_dict.get('json')}")
            return {"json_prompt": json_prompt_dict.get("json")}

        async def evaluate_node(state: BrainstormState) -> Dict:
            logger.info(f"Node: Evaluating JSON prompt (Iteration {state['iteration']})...")
            evaluation = await self.evaluator_agent.refine(
                state["user_input"], json_prompt=state["json_prompt"]
            )
            logger.info(f"Evaluation result: {evaluation}")
            return {"evaluation": evaluation, "iteration": state["iteration"] + 1}

        async def refine_node(state: BrainstormState) -> Dict:
            logger.info("Node: Refining JSON prompt...")
            issues = state["evaluation"].get("issues", [])
            if not issues:
                logger.info("No issues found to refine. Ending refinement.")
                return {} # No changes to state if no issues

            refined_prompt = await self.refiner_agent.refine(
                state["user_input"], json_prompt=state["json_prompt"], issues=issues
            )
            logger.info(f"Refined JSON prompt: {refined_prompt}")
            return {"json_prompt": refined_prompt}

        def should_continue(state: BrainstormState) -> str:
            logger.info("Conditional Edge: Checking 'should_continue'...")
            if state["evaluation"].get("status") == "yes":
                logger.info("Decision: Evaluation successful. Ending workflow.")
                return "end"
            if state["iteration"] >= self.max_iterations:
                logger.info("Decision: Max iterations reached. Ending workflow.")
                return "end"
            logger.info("Decision: Evaluation failed. Looping back to refine prompt.")
            return "refine"

        def after_refine_check(state: BrainstormState) -> str:
            logger.info("Conditional Edge: Checking after refinement...")
            if not state["evaluation"].get("issues"):
                logger.info("Decision: No issues were found for refinement. Ending workflow.")
                return "end"
            return "evaluate"

        # Add nodes to the graph
        workflow.add_node("idea_generation", idea_generation_node)
        workflow.add_node("planner", planner_node)
        workflow.add_node("architect", architect_node)
        workflow.add_node("generate_json", generate_json_node)
        workflow.add_node("evaluate", evaluate_node)
        workflow.add_node("refine", refine_node)

        # Set the entrypoint and build the graph
        workflow.set_entry_point("idea_generation")
        workflow.add_edge("idea_generation", "planner")
        workflow.add_edge("planner", "architect")
        workflow.add_edge("architect", "generate_json")
        workflow.add_edge("generate_json", "evaluate")

        workflow.add_conditional_edges(
            "evaluate",
            should_continue,
            {
                "refine": "refine",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "refine",
            after_refine_check,
            {
                "evaluate": "evaluate",
                "end": END,
            },
        )

        return workflow.compile()

    async def run(self, user_input: str) -> Dict:
        """Executes the brainstorming and JSON generation workflow."""
        logger.info("Starting brainstorming pipeline...")
        initial_state: BrainstormState = {
            "user_input": user_input,
            "ideas": "",
            "plan": "",
            "architecture": "",
            "json_prompt": "",
            "evaluation": {},
            "iteration": 0,
        }
        try:
            final_state = await self.graph.ainvoke(initial_state)
            logger.info("Brainstorming pipeline finished.")
            logger.debug(f"Final state: {final_state}")

            json_string = final_state.get("json_prompt", "{}") or "{}"
            
            # Attempt to parse the final JSON. If it's invalid, log and return an error state.
            try:
                # Clean the JSON string by removing markdown fences and any leading/trailing non-JSON characters
                json_match = re.search(r"```json\s*(.*?)\s*```", json_string, re.DOTALL)
                if json_match:
                    cleaned_json_string = json_match.group(1).strip()
                else:
                    cleaned_json_string = json_string.strip()

                final_state["json_prompt"] = json.loads(cleaned_json_string)
            except (json.JSONDecodeError, AttributeError):
                logger.error(f"Final JSON prompt is not valid JSON. Content: {json_string}", exc_info=True)
                final_state["json_prompt"] = {"error": "The generated content was not valid JSON.", "raw_content": json_string}
            return final_state
        except Exception as e:
            logger.error(f"An error occurred during pipeline execution: {e}", exc_info=True)
            # Return the initial state but with an error message to maintain a consistent structure for the frontend.
            return {
                "error": f"An error occurred during pipeline execution: {str(e)}",
                **initial_state,
            }