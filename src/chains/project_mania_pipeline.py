from typing import Any, Dict, List, TypedDict, Optional, Literal
from langgraph.graph import StateGraph, END
import re
import asyncio

from src.models.project_mania_models import ProjectManiaSchema, ProjectManiaResponse
from src.agents.project_mania.router_agent import RouterAgent
from src.agents.project_mania.composers.generic_template_composer import GenericTemplateComposer
from src.agents.project_mania.composers.crewai_template_composer import CrewAITemplateComposer
from src.agents.project_mania.composers.autogen_template_composer import AutogenTemplateComposer
from src.agents.project_mania.refine.analyze_agent import AnalyzeAgent
from src.agents.project_mania.refine.refine_agent import RefineAgent
from src.agents.project_mania.refine.evaluate_agent import EvaluateAgent
from src.logger import logger

class ProjectManiaState(TypedDict):
    intent: str
    variables: List[str]
    template_type: Literal["general", "crewai", "autogen"]
    prompt_length: Literal["low", "medium", "high"]
    plan: Dict
    current_template: str
    analysis: Dict
    evaluation: Dict
    iteration: int
    metadata: List[Dict]
    final_output: str

class ProjectManiaPipeline:
    """
    Main orchestration pipeline for Project Mania using LangGraph.
    Flow: Router -> Composer -> Analyze -> Refine -> Evaluate -> Clean Output
    """
    def __init__(self, llm: Any):
        self.llm = llm
        self.router = RouterAgent(llm)
        self.composers = {
            "general": GenericTemplateComposer(llm),
            "crewai": CrewAITemplateComposer(llm),
            "autogen": AutogenTemplateComposer(llm)
        }
        self.analyze_agent = AnalyzeAgent(llm)
        self.refine_agent = RefineAgent(llm)
        self.evaluate_agent = EvaluateAgent(llm)
        self.max_iterations = 3
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ProjectManiaState)

        # --- Nodes ---

        async def route_node(state: ProjectManiaState) -> ProjectManiaState:
            logger.info(f"Routing intent: {state['intent']}")
            plan = await asyncio.to_thread(
                self.router.route, state['intent'], state['template_type'], state['variables']
            )
            logger.info(f"Router Plan: {plan}")
            return {"plan": plan}

        async def compose_node(state: ProjectManiaState) -> ProjectManiaState:
            logger.info("Composing draft template...")
            composer = self.composers.get(state['template_type'])
            if not composer:
                raise ValueError(f"Unknown template type: {state['template_type']}")
            
            draft_template = await asyncio.to_thread(
                composer.compose, state['intent'], state['variables'], state['plan'], state.get('prompt_length', 'medium')
            )
            logger.info("Draft template composed.")
            return {"current_template": draft_template, "iteration": 0}

        async def analyze_node(state: ProjectManiaState) -> ProjectManiaState:
            iteration = state['iteration'] + 1
            logger.info(f"Refinement Iteration {iteration}/{self.max_iterations} - Analyzing...")
            analysis = await asyncio.to_thread(
                self.analyze_agent.analyze, state['current_template'], state['intent']
            )
            logger.info(f"Analysis: {analysis}")
            return {"analysis": analysis, "iteration": iteration}

        async def refine_node(state: ProjectManiaState) -> ProjectManiaState:
            logger.info("Refining template based on analysis...")
            current_template = state['current_template']
            if state['analysis'].get("suggestions"):
                current_template = await asyncio.to_thread(
                    self.refine_agent.apply_changes, current_template, state['analysis']["suggestions"]
                )
            return {"current_template": current_template}

        async def evaluate_node(state: ProjectManiaState) -> ProjectManiaState:
            logger.info("Evaluating template...")
            evaluation = await asyncio.to_thread(
                self.evaluate_agent.evaluate, state['current_template'], state['intent']
            )
            logger.info(f"Evaluation: {evaluation}")
            
            # Update metadata history
            new_metadata_entry = {
                "iteration": state['iteration'],
                "analysis": state['analysis'],
                "evaluation": evaluation
            }
            current_metadata = state.get('metadata', [])
            return {"evaluation": evaluation, "metadata": current_metadata + [new_metadata_entry]}

        async def clean_output_node(state: ProjectManiaState) -> ProjectManiaState:
            logger.info("Cleaning final output...")
            raw_output = state['current_template']
            
            # Remove markdown fences like ```python, ```jinja, ```
            cleaned_output = re.sub(r'^```\w*\n', '', raw_output) # Remove start fence
            cleaned_output = re.sub(r'\n```$', '', cleaned_output) # Remove end fence
            cleaned_output = cleaned_output.strip()
            
            return {"final_output": cleaned_output}

        # --- Edges ---

        def should_continue(state: ProjectManiaState) -> str:
            if state['evaluation'].get("success", False):
                return "clean_output"
            if state['iteration'] >= self.max_iterations:
                return "clean_output"
            return "analyze"

        workflow.add_node("route", route_node)
        workflow.add_node("compose", compose_node)
        workflow.add_node("analyze", analyze_node)
        workflow.add_node("refine", refine_node)
        workflow.add_node("evaluate", evaluate_node)
        workflow.add_node("clean_output", clean_output_node)

        workflow.set_entry_point("route")
        workflow.add_edge("route", "compose")
        workflow.add_edge("compose", "analyze")
        workflow.add_edge("analyze", "refine")
        workflow.add_edge("refine", "evaluate")
        
        workflow.add_conditional_edges(
            "evaluate",
            should_continue,
            {
                "analyze": "analyze",
                "clean_output": "clean_output"
            }
        )
        
        workflow.add_edge("clean_output", END)

        return workflow.compile()

    async def run(self, input_data: ProjectManiaSchema) -> ProjectManiaResponse:
        logger.info(f"Starting Project Mania generation for intent: {input_data.intent}")
        
        initial_state = {
            "intent": input_data.intent,
            "variables": input_data.variables,
            "template_type": input_data.template_type,
            "prompt_length": input_data.prompt_length,
            "plan": {},
            "current_template": "",
            "analysis": {},
            "evaluation": {},
            "iteration": 0,
            "metadata": [],
            "final_output": ""
        }

        final_state = await self.graph.ainvoke(initial_state)
        
        return ProjectManiaResponse(
            final_template=final_state["final_output"],
            metadata={
                "plan": final_state["plan"],
                "refinement_history": final_state["metadata"],
                "template_type": final_state["template_type"]
            }
        )
