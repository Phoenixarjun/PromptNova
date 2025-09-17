from fastapi import FastAPI, HTTPException
from src.models.prompt_schema import PromptSchema
from src.chains.pipeline import PromptPipeline
from src.config import GOOGLE_API_KEY
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import unpad
import base64
from src.logger import logger
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="PromptNova API", description="API for refining prompts using multiple styles and a framework.")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def decrypt_cryptojs_aes(encrypted_str: str, password: str) -> str:
    """Decrypts a string encrypted with CryptoJS.AES.encrypt(message, password)."""
    try:
        encrypted_data = base64.b64decode(encrypted_str)
        # CryptoJS format: "Salted__" (8 bytes) + salt (8 bytes) + ciphertext
        if encrypted_data[:8] != b'Salted__':
            raise ValueError("Invalid encrypted data: missing salt prefix.")
        
        salt = encrypted_data[8:16]
        ciphertext = encrypted_data[16:]
        
        # EVP_BytesToKey logic to derive key and IV from password and salt.
        # CryptoJS uses MD5 by default. It concatenates hashes until key+iv length is met.
        key_iv = b''
        temp = b''
        password_bytes = password.encode('utf-8')
        
        while len(key_iv) < 48: # 32 bytes for key (AES-256) + 16 bytes for IV
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

@app.post("/refine", response_model=PromptSchema)
async def refine_prompt(prompt_input: PromptSchema):
    
    """Refines a user prompt using selected styles and framework."""
    try:
        print(f"Received api_key: {prompt_input.api_key}")
        print(f"Received password: {prompt_input.password}")
        logger.info(f"Received request: user_input={prompt_input.user_input}..., styles={prompt_input.style}, framework={prompt_input.framework}")
        decrypted_api_key = None
        if prompt_input.api_key:
            if not prompt_input.password:
                raise HTTPException(status_code=400, detail="API key is present, but no password was provided.")
            try:
                # Decrypt the API key using the password provided from the cookie.
                # This logic is compatible with CryptoJS.AES.encrypt used on the frontend.
                decrypted_api_key = decrypt_cryptojs_aes(prompt_input.api_key, prompt_input.password)
                print(f"Decrypted API Key: {decrypted_api_key}")
                logger.info("Successfully decrypted and using user-provided API key.")
            except (ValueError, IndexError, TypeError) as e:
                logger.error(f"Failed to decrypt API key: {e}")
                raise HTTPException(status_code=400, detail="Invalid API key or password.")
        
        final_api_key = decrypted_api_key or GOOGLE_API_KEY
        if not final_api_key:
            logger.error("API key not found in request or environment.")
            raise HTTPException(status_code=401, detail="API key not found. Please provide it in the settings or set GOOGLE_API_KEY in your environment.")

        pipeline = PromptPipeline(api_key=final_api_key)
        # Create a new PromptSchema instance for the pipeline, excluding auth fields.
        pipeline_input_data = prompt_input.model_dump(exclude={'api_key', 'password', 'output_str'})
        pipeline_prompt = PromptSchema(**pipeline_input_data)
        result = await pipeline.run(pipeline_prompt)
        logger.info(f"Refined prompt: {result.output_str}...")
        return result
    except Exception as e:
        logger.error(f"Error refining prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error refining prompt: {str(e)}")