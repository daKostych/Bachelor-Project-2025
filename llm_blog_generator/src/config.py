from pathlib import Path

random_seed = 999

BASE_DIR = Path().resolve().parent

BLOG_DATASET_PATH = BASE_DIR / "data" / "datasets" / "blogs.csv"
PREPROCESSED_BLOG_DATASET_PATH = BASE_DIR / "data" / "datasets" / "preprocessed_blogs.csv"
PAPER_DATASET_PATH = BASE_DIR / "data" / "datasets" / "papers.csv"
PREPROCESSED_PAPER_DATASET_PATH = BASE_DIR / "data" / "datasets" / "preprocessed_papers.csv"
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver-linux64/chromedriver"
EXAMPLES_PATH = BASE_DIR / "data" / "examples"
VECTOR_STORE_PATH = BASE_DIR / "data" / "vector_store"
RESULTS_PATH = BASE_DIR / "data" / "generation_results"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GEMINI_2_FLASH = "gemini-2.0-flash"
GEMINI_2_FLASH_TEMPERATURE = 1

LLM_RPM = 15
LLM_TPM = 1000000
LLM_RPD = 1500
RATE_LIMIT_RPS = 0.25   # One request per 4 seconds (RPM 15)
RATE_LIMIT_BUCKET = 1   # Sequent requests

CLASSIFICATION_MAP = {
    "Excellent": 5,
    "Very Good": 4,
    "Good": 3,
    "Average": 2,
    "Bad": 1
}

CHARACTERS_PER_PAGE = 2700
MIN_PAGE_NUMBER = 20