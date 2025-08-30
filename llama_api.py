
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Body
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import logging
from dmk import apply_dmk_loss
from dckg import generate_keywords

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GenerateRequest(BaseModel):
    prompt: str
    max_words: int = 800
    domain: str

app = FastAPI()


@app.post("/generate")
async def generate(data: GenerateRequest = Body(...)):
    prompt = data.prompt
    max_words = data.max_words
    domain = data.domain

    # DCKG: Generate keywords for the domain/context
    keywords = generate_keywords(prompt, domain)
    logger.info(f"Generated keywords: {keywords}")

    # DMK: Apply DMK loss to enforce keywords in output
    prompt_with_keywords = apply_dmk_loss(prompt, keywords)
    logger.info(f"Prompt after DMK: {prompt_with_keywords}")

    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a professional content writer. Always complete your sentences and paragraphs. Never end abruptly or leave sentences unfinished. Ensure your response is complete and well-structured."},
            {"role": "user", "content": prompt_with_keywords}
        ],
        "max_tokens": int(max_words * 1.8),
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": None
    }
    response = requests.post(groq_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        text = result["choices"][0]["message"]["content"]
        
        # Clean up the text to ensure it ends properly
        text = text.strip()
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            # If the last "sentence" is very short, it's likely incomplete
            text = '.'.join(sentences[:-1]) + '.'
        
        logger.info("Text generated successfully.")
        # DMK post-generation enforcement
        dmk_ok, missing_keywords = apply_dmk_loss(prompt, keywords, generated_text=text)
        if not dmk_ok:
            logger.warning(f"DMK constraint not satisfied. Missing keywords: {missing_keywords}")
            return JSONResponse(content={
                "text": text,
                "keywords": keywords,
                "dmk_ok": False,
                "missing_keywords": missing_keywords,
                "warning": f"The generated text is missing the following keywords: {', '.join(missing_keywords)}."
            })
        return JSONResponse(content={"text": text, "keywords": keywords, "dmk_ok": True})
    else:
        logger.error(f"Groq API error: {response.text}")
        return JSONResponse(content={"error": response.text}, status_code=500)