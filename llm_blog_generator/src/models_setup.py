from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

from src.config import (GEMINI_2_FLASH, TEMPERATURE, GEMINI_2_FLASH_RPM, GEMINI_2_FLASH_LITE, GEMINI_2_FLASH_LITE_RPM,
                        GEMINI_1_5_FLASH, GEMINI_1_5_FLASH_RPM,
                        RATE_LIMIT_BUCKET, EMBEDDING_MODEL_NAME)
#=======================================================================================================================
def calculate_rps(rpm):
    return 1 / (60 / rpm)
#=======================================================================================================================
# Gemini 2.0 Flash
gemini_2_flash = ChatGoogleGenerativeAI(
    model=GEMINI_2_FLASH,
    temperature=TEMPERATURE,
    rate_limiter=InMemoryRateLimiter(
        requests_per_second=calculate_rps(GEMINI_2_FLASH_RPM),
        max_bucket_size=RATE_LIMIT_BUCKET,
    )
)
#=======================================================================================================================
# Gemini 2.0 Flash-Lite
gemini_2_flash_lite = ChatGoogleGenerativeAI(
    model=GEMINI_2_FLASH_LITE,
    temperature=TEMPERATURE,
    rate_limiter=InMemoryRateLimiter(
        requests_per_second=calculate_rps(GEMINI_2_FLASH_LITE_RPM),
        max_bucket_size=RATE_LIMIT_BUCKET,
    )
)
#=======================================================================================================================
# Gemini 1.5 Flash
gemini_1_5_flash = ChatGoogleGenerativeAI(
    model=GEMINI_1_5_FLASH,
    temperature=TEMPERATURE,
    rate_limiter=InMemoryRateLimiter(
        requests_per_second=calculate_rps(GEMINI_1_5_FLASH_RPM),
        max_bucket_size=RATE_LIMIT_BUCKET,
    )
)
#=======================================================================================================================
# Embeddings model
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
langchain_embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#=======================================================================================================================