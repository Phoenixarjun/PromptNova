from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, List
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
    def __init__(self):
        self.max_iterations = 3
        self.score_threshold = 90
        self.agents = {
            "zero_shot": ZeroShot(),
            "one_shot": OneShot(),
            "cot": ChainOfThought(),
            "tot": TreeOfThought(),
            "react": ReAct(),
            "in_context": InContext(),
            "emotion": Emotion(),
            "role": Role(),
            "few_shot": FewShot(),
            "self_consistency": SelfConsistency(),
            "meta_prompting": MetaPrompting(),
            "least_to_most": LeastToMost(),
            "multi_task": MultiTask(),
            "task_decomposition": TaskDecomposition(),
            "constrained": Constrained(),
            "generated_knowledge": GeneratedKnowledge(),
            "automatic_prompt_engineering": AutomaticPromptEngineering(),
            "directional_stimulus": DirectionalStimulus(),
            "co_star": CoStar(),
            "tcef": Tcef(),
            "crispe": Crispe(),
            "rtf": Rtf(),
            "ice": Ice(),
            "craft": Craft(),
            "ape": Ape(),
            "pecra": Pecra(),
            "oscar": Oscar(),
            "rasce": Rasce(),
            "reflection": Reflection(),
            "flipped_interaction": FlippedInteraction(),
            "bab": Bab()
        }
        self.self_correction = SelfCorrection()
        self.refine_agent = RefineAgent()
        self.final_prompt = FinalPrompt()
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(PromptState)

        async def type_refine_node(state: PromptState) -> PromptState:
            tasks = [
                self.agents[style].refine(state["prompt_input"].user_input)
                for style in state["prompt_input"].style
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            type_prompts = {
                style: result if isinstance(result, str) else str(result)
                for style, result in zip(state["prompt_input"].style, results)
            }
            logger.info(f"Type prompts generated: {type_prompts}")
            return {"type_prompts": type_prompts}

        async def evaluate_node(state: PromptState) -> PromptState:
            combined_prompt = "\n".join(state["type_prompts"].values())
            evaluation = self.self_correction.evaluate(
                prompt=combined_prompt,
                user_prompt=state["prompt_input"].user_input,
                agents=state["prompt_input"].style
            )
            logger.info(f"Evaluation result: {evaluation}")
            return {"evaluation": evaluation, "iteration": state["iteration"] + 1}

        async def refine_node(state: PromptState) -> PromptState:
            if state["evaluation"]["status"] == "yes":
                return state
            refined_prompts = self.refine_agent.refine_based_on_feedback(
                user_input=state["prompt_input"].user_input,
                feedback=state["evaluation"],
                agents=state["prompt_input"].style
            )
            logger.info(f"Refined prompts: {refined_prompts}")
            return {"refined_prompts": refined_prompts}

        async def integrate_node(state: PromptState) -> PromptState:
            prompts = state["refined_prompts"] if state["refined_prompts"] else state["type_prompts"]
            integrated_prompt = self.final_prompt.integrate(prompts)
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