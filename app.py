from fastapi import FastAPI, HTTPException
from src.models.prompt_schema import PromptSchema, UpdatePromptSchema, UpdateProjectSchema, PickAgentSchema
from src.models.evaluateSchema import EvaluatePipelineInput, FullEvaluationResult
from src.chains.pipeline import PromptPipeline
from src.chains.project_pipeline import ProjectPipeline
from src.chains.update_pipeline import UpdatePipeline
from src.chains.project_update_pipeline import ProjectUpdatePipeline
from src.chains.evaluate_pipleline import EvaluatePipeline
from src.models.project_mania_models import ProjectManiaSchema, ProjectManiaResponse
from src.chains.project_mania_pipeline import ProjectManiaPipeline
import re
import json
from src.agents.pick_agent import PickAgent
from src.config import GOOGLE_API_KEY, GROQ_API_KEY, MISTRAL_API_KEY
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import unpad
import base64
from src.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI

app = FastAPI(title="PromptNova API", description="API for refining prompts using multiple styles and a framework.")

# Allow specific origins for local development and the Render backend itself.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://promptnova.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://prompt-nova(-[a-zA-Z0-9-]+)?\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def decrypt_cryptojs_aes(encrypted_str: str, password: str) -> str:
    try:
        encrypted_data = base64.b64decode(encrypted_str)
        if encrypted_data[:8] != b'Salted__':
            raise ValueError("Invalid encrypted data: missing salt prefix.")

        salt = encrypted_data[8:16]
        ciphertext = encrypted_data[16:]

        key_iv = b''
        temp = b''
        password_bytes = password.encode('utf-8')

        while len(key_iv) < 48:
            md5 = MD5.new()
            if temp:
                md5.update(temp)
            md5.update(password_bytes)
            md5.update(salt)
            temp = md5.digest()
            key_iv += temp

        key = key_iv[:32]
        iv = key_iv[32:48]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted_padded, AES.block_size).decode('utf-8')
        return decrypted
    except Exception as e:
        logger.error(f"CryptoJS AES decryption failed: {e}")
        raise ValueError("Decryption failed. Invalid API key or password.")


def get_llm(prompt_input):
    decrypted_api_key = None
    if prompt_input.api_key:
        if not prompt_input.password:
            raise HTTPException(status_code=400, detail="API key is present, but no password was provided.")
        try:
            decrypted_api_key = decrypt_cryptojs_aes(prompt_input.api_key, prompt_input.password)
        except (ValueError, IndexError, TypeError) as e:
            raise HTTPException(status_code=400, detail="Invalid API key or password.")

    model_provider = prompt_input.selected_model or 'gemini' # Default to gemini if not provided

    if model_provider == 'gemini':
        api_key = decrypted_api_key or GOOGLE_API_KEY
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.7)

    elif model_provider == 'groq':
        api_key = decrypted_api_key or GROQ_API_KEY
        model_name = prompt_input.selected_groq_model
        return ChatGroq(model_name=model_name, api_key=api_key, temperature=0.7)

    elif model_provider == 'mistral':
        api_key = decrypted_api_key or MISTRAL_API_KEY
        return ChatMistralAI(model="mistral-large-latest", api_key=api_key, temperature=0.7)

    else:
        raise HTTPException(status_code=400, detail=f"Invalid model provider selected: {model_provider}")


@app.post("/refine", response_model=PromptSchema)
async def refine_prompt(prompt_input: PromptSchema):
    try:
        llm = get_llm(prompt_input)
        pipeline = PromptPipeline(llm=llm)
        result = await pipeline.run(prompt_input)
        return result
    except Exception as e:
        logger.error(f"Error refining prompt: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error refining prompt: {str(e)}")

@app.post("/project")
async def generate_project_prompt(prompt_input: PromptSchema):
    try:
        llm = get_llm(prompt_input)
        pipeline = ProjectPipeline(llm=llm)
        result = await pipeline.run(prompt_input)
        return result
    except Exception as e:
        logger.error(f"Error generating project prompt: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating project prompt: {str(e)}")

@app.post("/update_prompt")
async def update_prompt_endpoint(update_input: UpdatePromptSchema):
    try:
        class LLMInput:
            def __init__(self, **kwargs):
                self.selected_model = kwargs.get("selected_model")
                self.selected_groq_model = kwargs.get("selected_groq_model")
                self.api_key = kwargs.get("api_key")
                self.password = kwargs.get("password")
        llm_input = LLMInput(**update_input.dict())
        llm = get_llm(llm_input)
        pipeline = UpdatePipeline(llm=llm)
        updated_prompt = await pipeline.run(
            original_prompt=update_input.original_prompt,
            final_prompt=update_input.final_prompt,
            user_feedback=update_input.user_feedback,
            style=update_input.style,
            framework=update_input.framework,
        )
        print(f"Updated prompt: {updated_prompt}")
        return {"updated_prompt": updated_prompt}
    except Exception as e:
        logger.error(f"An unexpected error occurred in /update_prompt: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/project_update")
async def project_update_endpoint(update_input: UpdateProjectSchema):
    try:
        class LLMInput:
            def __init__(self, **kwargs):
                self.selected_model = kwargs.get("selected_model")
                self.selected_groq_model = kwargs.get("selected_groq_model")
                self.api_key = kwargs.get("api_key")
                self.password = kwargs.get("password")
        llm_input = LLMInput(**update_input.dict())
        llm = get_llm(llm_input)
        pipeline = ProjectUpdatePipeline(llm=llm)
        updated_artifacts = await pipeline.run(
            original_user_prompt=update_input.original_user_prompt,
            project_artifacts=update_input.project_artifacts,
            user_feedback=update_input.user_feedback,
        )
        return {"updated_artifacts": updated_artifacts}
    except Exception as e:
        logger.error(f"An unexpected error occurred in /project_update: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/pick_agent", response_model=dict)
async def pick_agent_endpoint(pick_agent_input: PickAgentSchema) -> dict:
    """
    Selects prompt types and a framework based on user input.
    """
    try:
        logger.info(pick_agent_input.user_input)
        llm = get_llm(pick_agent_input)
        # print(pick_agent_input)
        agent = PickAgent(llm=llm)
        result_str = agent.pick(pick_agent_input.user_input)
        # print(result_str)
        logger.info(result_str)
        
        json_match = re.search(r'\{[\s\S]*\}', result_str)
        if not json_match:
            raise ValueError("No valid JSON object found in the LLM's response.")
        
        return json.loads(json_match.group(0))
    except Exception as e:
        logger.error(f"Error picking agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error picking agent: {str(e)}")

@app.post("/evaluate", response_model=FullEvaluationResult)
async def evaluate_prompt_endpoint(eval_input: EvaluatePipelineInput):
    """
    Evaluates a given prompt using a multi-agent framework.
    """
    try:
        llm = get_llm(eval_input)
        pipeline = EvaluatePipeline(llm=llm)
        result = await pipeline.run(eval_input)
        return result
    except Exception as e:
        logger.error(f"Error evaluating prompt: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error evaluating prompt: {str(e)}")

@app.post("/project-mania/generate", response_model=ProjectManiaResponse)
async def generate_project_mania(input_data: ProjectManiaSchema):
    try:
        class LLMInput:
            def __init__(self, **kwargs):
                self.selected_model = kwargs.get("selected_model")
                self.selected_groq_model = kwargs.get("selected_groq_model")
                self.api_key = kwargs.get("api_key")
                self.password = kwargs.get("password")
        
        llm_input = LLMInput(**input_data.dict())
        llm = get_llm(llm_input)
        
        pipeline = ProjectManiaPipeline(llm=llm)
        result = await pipeline.run(input_data)
        return result
    except Exception as e:
        logger.error(f"Error in Project Mania generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")

frontend_dir = Path("promptnova/out")

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            raise ex

if frontend_dir.exists() and frontend_dir.is_dir():
    app.mount("/", SPAStaticFiles(directory=frontend_dir, html=True), name="static")
