from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, List, Optional, Any
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
from src.agents.standard.self_correction import SelfCorrection
from src.agents.standard.refine_agent import RefineAgent
from src.agents.standard.final_prompt import FinalPrompt
from src.logger import logger
import asyncio

class PromptState(TypedDict):
    prompt_input: PromptSchema
    framework_output: str
    type_prompts: Dict[str, str]
    evaluation: Dict
    refined_prompts: Dict[str, str]
    output_str: str
    iteration: int

class PromptPipeline:
    def __init__(self, llm: Any):
        self.max_iterations = 3
        self.score_threshold = 90
        self.agents = {
            "zero_shot": ZeroShot(llm=llm),
            "one_shot": OneShot(llm=llm),
            "cot": ChainOfThought(llm=llm),
            "tot": TreeOfThought(llm=llm),
            "react": ReAct(llm=llm),
            "in_context": InContext(llm=llm),
            "emotion": Emotion(llm=llm),
            "role": Role(llm=llm),
            "few_shot": FewShot(llm=llm),
            "self_consistency": SelfConsistency(llm=llm),
            "meta_prompting": MetaPrompting(llm=llm),
            "least_to_most": LeastToMost(llm=llm),
            "multi_task": MultiTask(llm=llm),
            "task_decomposition": TaskDecomposition(llm=llm),
            "constrained": Constrained(llm=llm),
            "generated_knowledge": GeneratedKnowledge(llm=llm),
            "automatic_prompt_engineering": AutomaticPromptEngineering(llm=llm),
            "directional_stimulus": DirectionalStimulus(llm=llm),
            "chain_of_verification": ChainOfVerification(llm=llm),
            "skeleton_of_thought": SkeletonOfThought(llm=llm),
            "graph_of_thoughts": GraphOfThoughts(llm=llm),
            "plan_and_solve": PlanAndSolve(llm=llm),
            "maieutic_prompting": MaieuticPrompting(llm=llm),
            "reflexion_type": ReflexionType(llm=llm),
            "chain_of_density": ChainOfDensity(llm=llm),
            "active_prompt": ActivePrompt(llm=llm),
            "retrieval_augmented_prompting": RetrievalAugmentedPrompting(llm=llm),
            "multi_agent_debate": MultiAgentDebate(llm=llm),
            "persona_switching": PersonaSwitching(llm=llm),
            "scaffolded_prompting": ScaffoldedPrompting(llm=llm),
            "deliberation_prompting": DeliberationPrompting(llm=llm),
            "context_expansion": ContextExpansion(llm=llm),
            "goal_oriented_prompting": GoalOrientedPrompting(llm=llm),
            "co_star": CoStar(llm=llm),
            "tcef": Tcef(llm=llm),
            "crispe": Crispe(llm=llm),
            "rtf": Rtf(llm=llm),
            "ice": Ice(llm=llm),
            "craft": Craft(llm=llm),
            "ape": Ape(llm=llm),
            "pecra": Pecra(llm=llm),
            "oscar": Oscar(llm=llm),
            "rasce": Rasce(llm=llm),
            "reflection": Reflection(llm=llm),
            "flipped_interaction": FlippedInteraction(llm=llm),
            "bab": Bab(llm=llm),
            "prompt": PromptFramework(llm=llm),
            "soap": Soap(llm=llm),
            "clear": Clear(llm=llm),
            "prism": Prism(llm=llm),
            "grips": Grips(llm=llm),
            "app": AppFramework(llm=llm),
            "scope": Scope(llm=llm),
            "tool_oriented_prompting": ToolOrientedPrompting(llm=llm),
            "neuro_symbolic_prompting": NeuroSymbolicPrompting(llm=llm),
            "dynamic_context_windows": DynamicContextWindows(llm=llm),
            "meta_cognitive_prompting": MetaCognitivePrompting(llm=llm),
            "prompt_ensembles": PromptEnsembles(llm=llm)
        }
        self.self_correction = SelfCorrection(llm=llm)
        self.refine_agent = RefineAgent(llm=llm)
        self.final_prompt = FinalPrompt(llm=llm)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(PromptState)

        async def framework_node(state: PromptState) -> PromptState:
            framework = state["prompt_input"].framework
            if framework in self.agents:
                framework_output = await asyncio.to_thread(
                    self.agents[framework].refine, state["prompt_input"].user_input
                )
                logger.info(f"Framework '{framework}' output: {framework_output}")
                return {"framework_output": framework_output}
            else:
                logger.warning(f"Framework '{framework}' not found, using user input directly.")
                return {"framework_output": state["prompt_input"].user_input}

        async def type_refine_node(state: PromptState) -> PromptState:
            input_for_types = state["framework_output"]
            tasks = [
                asyncio.to_thread(self.agents[style].refine, input_for_types)
                for style in state["prompt_input"].style
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            type_prompts = {
                style: (result if isinstance(result, str) else str(result))
                for style, result in zip(state["prompt_input"].style, results)
            }
            logger.info(f"Type prompts generated: {type_prompts}")
            return {"type_prompts": type_prompts, "refined_prompts": {}} # Clear refined prompts

        async def evaluate_node(state: PromptState) -> PromptState:
            prompts_to_evaluate = state["refined_prompts"] if state["refined_prompts"] else state["type_prompts"]
            combined_prompt = "\n".join(prompts_to_evaluate.values())
            evaluation = await asyncio.to_thread(
                self.self_correction.evaluate,
                combined_prompt,
                state["prompt_input"].user_input,
                list(prompts_to_evaluate.keys()),
            )
            logger.info(f"Evaluation result: {evaluation}")
            return {"evaluation": evaluation, "iteration": state["iteration"] + 1}

        async def refine_node(state: PromptState) -> PromptState:
            if state["evaluation"]["status"] == "yes":
                return {"refined_prompts": state["refined_prompts"] or state["type_prompts"]}
            logger.info(f"Passing evaluation to RefineAgent: {state['evaluation']}")
            refined_prompts = await self.refine_agent.refine_based_on_feedback(
                state["prompt_input"].user_input,
                state["evaluation"],
                state["type_prompts"],  # Pass the actual prompts
                list(state["type_prompts"].keys()),
            )
            logger.info(f"Refined prompts: {refined_prompts}")
            return {"refined_prompts": refined_prompts}

        async def integrate_node(state: PromptState) -> PromptState:
            prompts = state["refined_prompts"] if state["refined_prompts"] and all(state["refined_prompts"].values()) else state["type_prompts"]
            all_prompts = {state["prompt_input"].framework: state["framework_output"], **prompts}
            logger.info(f"Passing prompts to FinalPrompt.integrate: {all_prompts}")
            output_str = await self.final_prompt.integrate(
                refined_responses=all_prompts,
                type_prompts=state["type_prompts"],
                user_input=state["prompt_input"].user_input,
                framework=state["prompt_input"].framework
            )
            logger.info(f"Final output: {output_str}")
            return {"output_str": output_str}

        def should_continue(state: PromptState) -> str:
            if state["evaluation"]["status"] == "yes":
                return "integrate"
            if state["iteration"] >= self.max_iterations:
                return "integrate"
            return "refine"

        workflow.add_node("framework", framework_node)
        workflow.add_node("type_refine", type_refine_node)
        workflow.add_node("evaluate", evaluate_node)
        workflow.add_node("refine", refine_node)
        workflow.add_node("integrate", integrate_node)

        workflow.set_entry_point("framework")
        workflow.add_edge("framework", "type_refine")
        workflow.add_edge("type_refine", "evaluate")
        workflow.add_conditional_edges("evaluate", should_continue, {
            "refine": "refine",
            "integrate": "integrate"
        })
        workflow.add_edge("refine", "evaluate")
        workflow.add_edge("integrate", END)

        return workflow.compile()

    async def run(self, prompt_input: PromptSchema) -> PromptSchema:
        logger.info(f"Running pipeline for input: {prompt_input.user_input[:50]}... with styles: {prompt_input.style}, framework: {prompt_input.framework}")
        initial_state = {
            "prompt_input": prompt_input,
            "framework_output": "",
            "type_prompts": {},
            "evaluation": {},
            "refined_prompts": {},
            "output_str": "",
            "iteration": 0
        }
        state = await self.graph.ainvoke(initial_state)
        prompt_input.output_str = state["output_str"]
        return prompt_input
