from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, List, Optional
from src.models.prompt_schema import PromptSchema
from src.agents.types.zero_shot import ZeroShot
from src.agents.types.one_shot import OneShot
from src.agents.types.chain_of_thought import ChainOfThought
from src.agents.types.tree_of_thought import TreeOfThought
from src.agents.types.react import ReAct
from src.agents.types.in_context import InContext
from src.agents.types.emotion import Emotion
from src.agents.types.role import Role
from src.agents.types.few_shot import FewShot
from src.agents.types.self_consistency import SelfConsistency
from src.agents.types.meta_prompting import MetaPrompting
from src.agents.types.least_to_most import LeastToMost
from src.agents.types.multi_task import MultiTask
from src.agents.types.task_decomposition import TaskDecomposition
from src.agents.types.constrained import Constrained
from src.agents.types.generated_knowledge import GeneratedKnowledge
from src.agents.types.automatic_prompt_engineering import AutomaticPromptEngineering
from src.agents.types.directional_stimulus import DirectionalStimulus
from src.agents.types.chain_of_verification import ChainOfVerification
from src.agents.types.skeleton_of_thought import SkeletonOfThought
from src.agents.types.graph_of_thoughts import GraphOfThoughts
from src.agents.types.plan_and_solve import PlanAndSolve
from src.agents.types.maieutic_prompting import MaieuticPrompting
from src.agents.types.reflexion import Reflexion as ReflexionType
from src.agents.types.chain_of_density import ChainOfDensity
from src.agents.types.active_prompt import ActivePrompt
from src.agents.types.retrieval_augmented_prompting import RetrievalAugmentedPrompting
from src.agents.types.multi_agent_debate import MultiAgentDebate
from src.agents.types.persona_switching import PersonaSwitching
from src.agents.types.scaffolded_prompting import ScaffoldedPrompting
from src.agents.types.deliberation_prompting import DeliberationPrompting
from src.agents.types.context_expansion import ContextExpansion
from src.agents.types.goal_oriented_prompting import GoalOrientedPrompting
from src.agents.frameworks.co_star import CoStar
from src.agents.frameworks.tcef import Tcef
from src.agents.frameworks.crispe import Crispe
from src.agents.frameworks.rtf import Rtf
from src.agents.frameworks.ice import Ice
from src.agents.frameworks.craft import Craft
from src.agents.frameworks.ape import Ape
from src.agents.frameworks.pecra import Pecra
from src.agents.frameworks.oscar import Oscar
from src.agents.frameworks.rasce import Rasce
from src.agents.frameworks.reflection import Reflection
from src.agents.frameworks.flipped_interaction import FlippedInteraction
from src.agents.frameworks.bab import Bab
from src.agents.frameworks.prompt_framework import PromptFramework
from src.agents.frameworks.soap import Soap
from src.agents.frameworks.clear import Clear
from src.agents.frameworks.prism import Prism
from src.agents.frameworks.grips import Grips
from src.agents.frameworks.app_framework import AppFramework
from src.agents.frameworks.scope import Scope
from src.agents.frameworks.tool_oriented_prompting import ToolOrientedPrompting
from src.agents.frameworks.neuro_symbolic_prompting import NeuroSymbolicPrompting
from src.agents.frameworks.dynamic_context_windows import DynamicContextWindows
from src.agents.frameworks.meta_cognitive_prompting import MetaCognitivePrompting
from src.agents.frameworks.prompt_ensembles import PromptEnsembles
from src.agents.self_correction import SelfCorrection
from src.agents.refine_agent import RefineAgent
from src.agents.final_prompt import FinalPrompt
from src.logger import logger
import asyncio

class PromptState(TypedDict):
    prompt_input: PromptSchema
    type_prompts: Dict[str, str]
    evaluation: Dict
    refined_prompts: Dict[str, str]
    integrated_prompt: str
    output_str: str
    iteration: int

class PromptPipeline:
    def __init__(self, api_key: Optional[str] = None):
        self.max_iterations = 3
        self.score_threshold = 90
        self.agents = {
            "zero_shot": ZeroShot(api_key=api_key),
            "one_shot": OneShot(api_key=api_key),
            "cot": ChainOfThought(api_key=api_key),
            "tot": TreeOfThought(api_key=api_key),
            "react": ReAct(api_key=api_key),
            "in_context": InContext(api_key=api_key),
            "emotion": Emotion(api_key=api_key),
            "role": Role(api_key=api_key),
            "few_shot": FewShot(api_key=api_key),
            "self_consistency": SelfConsistency(api_key=api_key),
            "meta_prompting": MetaPrompting(api_key=api_key),
            "least_to_most": LeastToMost(api_key=api_key),
            "multi_task": MultiTask(api_key=api_key),
            "task_decomposition": TaskDecomposition(api_key=api_key),
            "constrained": Constrained(api_key=api_key),
            "generated_knowledge": GeneratedKnowledge(api_key=api_key),
            "automatic_prompt_engineering": AutomaticPromptEngineering(api_key=api_key),
            "directional_stimulus": DirectionalStimulus(api_key=api_key),
            "chain_of_verification": ChainOfVerification(api_key=api_key),
            "skeleton_of_thought": SkeletonOfThought(api_key=api_key),
            "graph_of_thoughts": GraphOfThoughts(api_key=api_key),
            "plan_and_solve": PlanAndSolve(api_key=api_key),
            "maieutic_prompting": MaieuticPrompting(api_key=api_key),
            "reflexion_type": ReflexionType(api_key=api_key),
            "chain_of_density": ChainOfDensity(api_key=api_key),
            "active_prompt": ActivePrompt(api_key=api_key),
            "retrieval_augmented_prompting": RetrievalAugmentedPrompting(api_key=api_key),
            "multi_agent_debate": MultiAgentDebate(api_key=api_key),
            "persona_switching": PersonaSwitching(api_key=api_key),
            "scaffolded_prompting": ScaffoldedPrompting(api_key=api_key),
            "deliberation_prompting": DeliberationPrompting(api_key=api_key),
            "context_expansion": ContextExpansion(api_key=api_key),
            "goal_oriented_prompting": GoalOrientedPrompting(api_key=api_key),
            "co_star": CoStar(api_key=api_key),
            "tcef": Tcef(api_key=api_key),
            "crispe": Crispe(api_key=api_key),
            "rtf": Rtf(api_key=api_key),
            "ice": Ice(api_key=api_key),
            "craft": Craft(api_key=api_key),
            "ape": Ape(api_key=api_key),
            "pecra": Pecra(api_key=api_key),
            "oscar": Oscar(api_key=api_key),
            "rasce": Rasce(api_key=api_key),
            "reflection": Reflection(api_key=api_key),
            "flipped_interaction": FlippedInteraction(api_key=api_key),
            "bab": Bab(api_key=api_key),
            "prompt": PromptFramework(api_key=api_key),
            "soap": Soap(api_key=api_key),
            "clear": Clear(api_key=api_key),
            "prism": Prism(api_key=api_key),
            "grips": Grips(api_key=api_key),
            "app": AppFramework(api_key=api_key),
            "scope": Scope(api_key=api_key),
            "tool_oriented_prompting": ToolOrientedPrompting(api_key=api_key),
            "neuro_symbolic_prompting": NeuroSymbolicPrompting(api_key=api_key),
            "dynamic_context_windows": DynamicContextWindows(api_key=api_key),
            "meta_cognitive_prompting": MetaCognitivePrompting(api_key=api_key),
            "prompt_ensembles": PromptEnsembles(api_key=api_key)
        }
        self.self_correction = SelfCorrection(api_key=api_key)
        self.refine_agent = RefineAgent(api_key=api_key)
        self.final_prompt = FinalPrompt(api_key=api_key)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(PromptState)

        async def type_refine_node(state: PromptState) -> PromptState:
            tasks = [
                asyncio.to_thread(self.agents[style].refine, state["prompt_input"].user_input)
                for style in state["prompt_input"].style
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            type_prompts = {
                style: (result if isinstance(result, str) else str(result))
                for style, result in zip(state["prompt_input"].style, results)
            }
            logger.info(f"Type prompts generated: {type_prompts}")
            return {"type_prompts": type_prompts}

        async def evaluate_node(state: PromptState) -> PromptState:
            combined_prompt = "\n".join(state["type_prompts"].values())
            evaluation = await asyncio.to_thread(
                self.self_correction.evaluate,
                combined_prompt,
                state["prompt_input"].user_input,
                state["prompt_input"].style,
            )
            logger.info(f"Evaluation result: {evaluation}")
            return {"evaluation": evaluation, "iteration": state["iteration"] + 1}

        async def refine_node(state: PromptState) -> PromptState:
            if state["evaluation"]["status"] == "yes":
                return state
            logger.info(f"Passing evaluation to RefineAgent: {state['evaluation']}")
            refined_prompts = await asyncio.to_thread(
                self.refine_agent.refine_based_on_feedback,
                state["prompt_input"].user_input,
                state["evaluation"],
                state["prompt_input"].style,
            )
            logger.info(f"Refined prompts: {refined_prompts}")
            return {"refined_prompts": refined_prompts}

        async def integrate_node(state: PromptState) -> PromptState:
            prompts = state["refined_prompts"] if state["refined_prompts"] and all(state["refined_prompts"].values()) else state["type_prompts"]
            logger.info(f"Passing prompts to FinalPrompt.integrate: {prompts}")
            integrated_prompt = self.final_prompt.integrate(
                prompts,
                state["type_prompts"],
                state["prompt_input"].user_input
            )
            logger.info(f"Integrated prompt: {integrated_prompt}")
            return {"integrated_prompt": integrated_prompt}

        async def framework_node(state: PromptState) -> PromptState:
            framework_agent = self.agents[state["prompt_input"].framework]
            output_str = framework_agent.refine(state["integrated_prompt"])
            logger.info(f"Final output: {output_str}")
            return {"output_str": output_str}

        async def should_continue(state: PromptState) -> str:
            if state["evaluation"]["status"] == "yes":
                return "integrate"
            if state["iteration"] >= self.max_iterations:
                return "integrate"
            if all(score >= self.score_threshold for score in state["evaluation"].get("agents", {}).values()):
                return "integrate"
            return "refine"

        workflow.add_node("type_refine", type_refine_node)
        workflow.add_node("evaluate", evaluate_node)
        workflow.add_node("refine", refine_node)
        workflow.add_node("integrate", integrate_node)
        workflow.add_node("framework", framework_node)

        workflow.set_entry_point("type_refine")
        workflow.add_edge("type_refine", "evaluate")
        workflow.add_conditional_edges("evaluate", should_continue, {
            "refine": "refine",
            "integrate": "integrate"
        })
        workflow.add_edge("refine", "evaluate")
        workflow.add_edge("integrate", "framework")
        workflow.add_edge("framework", END)

        return workflow.compile()

    async def run(self, prompt_input: PromptSchema) -> PromptSchema:
        logger.info(f"Running pipeline for input: {prompt_input.user_input[:50]}... with styles: {prompt_input.style}, framework: {prompt_input.framework}")
        state = await self.graph.ainvoke({
            "prompt_input": prompt_input,
            "type_prompts": {},
            "evaluation": {},
            "refined_prompts": {},
            "integrated_prompt": "",
            "output_str": "",
            "iteration": 0
        })
        prompt_input.output_str = state["output_str"]
        return prompt_input