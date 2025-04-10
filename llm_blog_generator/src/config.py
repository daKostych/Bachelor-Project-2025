from pathlib import Path

random_seed = 999

BASE_DIR = Path().resolve().parent

DEEPMIND_BLOG_DATASET_PATH = BASE_DIR / "data" / "datasets" / "deepmind_blogs.csv"
PREPROCESSED_DEEPMIND_BLOG_DATASET_PATH = BASE_DIR / "data" / "datasets" / "preprocessed_deepmind_blogs.csv"
BLOG_DATASET_PATH = BASE_DIR / "data" / "datasets" / "medium_blogs.csv"
PREPROCESSED_BLOG_DATASET_PATH = BASE_DIR / "data" / "datasets" / "preprocessed_medium_blogs.csv"
PAPER_DATASET_PATH = BASE_DIR / "data" / "datasets" / "papers.csv"
PREPROCESSED_PAPER_DATASET_PATH = BASE_DIR / "data" / "datasets" / "preprocessed_papers.csv"
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver-linux64/chromedriver"
EXAMPLES_PATH = BASE_DIR / "data" / "examples"
VECTOR_STORE_PATH = BASE_DIR / "data" / "vector_store"
LONG_TERM_MEMORY_PATH = BASE_DIR / "data" / "long_term_memory"
RESULTS_PATH = BASE_DIR / "data" / "generation_results"
NUMERIC_RESULTS_PATH = BASE_DIR / "data" / "experiment_results" / "numeric_evaluation.csv"
NORMALIZED_NUMERIC_RESULTS_PATH = BASE_DIR / "data" / "experiment_results" / "normalized_numeric_evaluation.csv"
CLASSIFICATION_ACC_RESULTS_PATH = BASE_DIR / "data" / "experiment_results" / "classification_acc.csv"
CLASSIFICATION_RMSE_RESULTS_PATH = BASE_DIR / "data" / "experiment_results" / "classification_RMSE.csv"
CLASSIFICATION_MAE_RESULTS_PATH = BASE_DIR / "data" / "experiment_results" / "classification_MAE.csv"
DEEPMIND_BLOG_EVALUATION_RESULTS_PATH = BASE_DIR / "data" / "experiment_results" / "deepmind_blog_evaluation.csv"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

TEMPERATURE = 1

GEMINI_2_FLASH = "gemini-2.0-flash"
GEMINI_2_FLASH_RPM = 15
GEMINI_2_FLASH_TPM = 800000
GEMINI_2_FLASH_RPD = 1500

GEMINI_2_FLASH_LITE = "gemini-2.0-flash-lite"
GEMINI_2_FLASH_LITE_RPM = 30
GEMINI_2_FLASH_LITE_TPM = 800000
GEMINI_2_FLASH_LITE_RPD = 1500

GEMINI_1_5_FLASH = "gemini-1.5-flash"
GEMINI_1_5_FLASH_RPM = 15
GEMINI_1_5_FLASH_TPM = 800000
GEMINI_1_5_FLASH_RPD = 1500

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

DISTANCE_THRESHOLD = 0.8