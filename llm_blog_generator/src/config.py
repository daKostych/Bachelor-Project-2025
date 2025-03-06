from pathlib import Path

random_seed = 999

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "data.csv"
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver-linux64/chromedriver"

GEMINI_2_FLASH = "gemini-2.0-flash"
GEMINI_2_FLASH_TEMPERATURE = 1

RATE_LIMIT_RPS = 0.25   # One request per 4 seconds (RPM 15)
RATE_LIMIT_BUCKET = 1   # Sequent requests

CLASSIFICATION_MAP = {
    "Excellent": 5,
    "Very Good": 4,
    "Good": 3,
    "Average": 2,
    "Bad": 1
}