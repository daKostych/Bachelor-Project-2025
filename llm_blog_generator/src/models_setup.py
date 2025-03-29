from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from src.config import (GEMINI_2_FLASH, GEMINI_2_FLASH_TEMPERATURE, RATE_LIMIT_RPS,
                        RATE_LIMIT_BUCKET, EMBEDDING_MODEL_NAME)
#=======================================================================================================================
# API request limit
rate_limiter = InMemoryRateLimiter(
    requests_per_second=RATE_LIMIT_RPS,
    max_bucket_size=RATE_LIMIT_BUCKET,
)
#=======================================================================================================================
# Initializing the LLM model
gemini_2_flash = ChatGoogleGenerativeAI(
    model=GEMINI_2_FLASH,
    temperature=GEMINI_2_FLASH_TEMPERATURE,
    rate_limiter=rate_limiter
)
#=======================================================================================================================
# Embeddings model
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
langchain_embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#=======================================================================================================================