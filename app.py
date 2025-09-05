from fastapi import FastAPI, HTTPException
from src.models.prompt_schema import PromptSchema
from src.models.typesSchema import RefineRequest
from src.chains.pipeline import PromptPipeline
from src.logger import logger
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
import asyncio

app = FastAPI(title="PromptNova API", description="API for refining prompts using multiple styles and a framework.")

@app.post("/refine", response_model=PromptSchema)
async def refine_prompt(prompt_input: PromptSchema):
    """Refines a user prompt using selected styles and framework."""
    try:
        logger.info(f"Received request: user_input={prompt_input.user_input[:50]}..., styles={prompt_input.style}, framework={prompt_input.framework}")
        pipeline = PromptPipeline()
        result = await pipeline.run(prompt_input)
        logger.info(f"Refined prompt: {result.output_str[:50]}...")
        return result
    except Exception as e:
        logger.error(f"Error refining prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error refining prompt: {str(e)}")

@app.post("/refine/style")
async def refine_by_style(input_data: RefineRequest):
    """Refine using a single style with style-specific optional fields."""
    try:
        style = input_data.style
        agents = {
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
            "ape": AutomaticPromptEngineering(),
            "directional_stimulus": DirectionalStimulus(),
        }
        agent = agents.get(style)
        if not agent:
            raise HTTPException(status_code=400, detail=f"Unsupported style: {style}")

        # Build kwargs from input based on style
        kwargs = {}
        if style == "role":
            kwargs["role_persona"] = getattr(input_data, "role_persona", None)
        elif style == "few_shot":
            kwargs["examples"] = getattr(input_data, "examples", None)
        elif style == "cot":
            kwargs["steps"] = getattr(input_data, "steps", None)
        elif style == "in_context":
            kwargs["context"] = getattr(input_data, "context", None)
        elif style == "emotion":
            kwargs["emotion"] = getattr(input_data, "emotion", None)
        # Add more mappings as needed for other styles

        # Remove None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        logger.info(f"Refining by style: {style} with options: {kwargs}")
        refined = await asyncio.to_thread(agent.refine, input_data.user_input, **kwargs)
        return {"style": style, "refined": refined}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refining prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error refining prompt: {str(e)}")