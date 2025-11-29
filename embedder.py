# embedder.py

import os
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("❌ GEMINI_API_KEY missing. Add to .env")

genai.configure(api_key=GEMINI_API_KEY)

DEFAULT_MODEL = "models/text-embedding-004"


def embed_texts(texts: List[str], model: str = DEFAULT_MODEL) -> List[List[float]]:
    """
    Generate embeddings using Gemini.
    Returns list of vectors.
    """
    resp = genai.embed_content(
        model=model,
        content=texts,
        task_type="retrieval_document",
    )

    # single call → returns embeddings array
    # For multiple texts, use batch wrapper
    return resp["embedding"]
