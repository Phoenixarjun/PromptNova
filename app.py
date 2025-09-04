from fastapi import FastAPI, HTTPException
from src.models.prompt_schema import PromptSchema
from src.chains.pipeline import PromptPipeline
from src.logger import logger
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