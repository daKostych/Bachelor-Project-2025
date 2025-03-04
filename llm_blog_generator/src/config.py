from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "datasets" / "data.csv"
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver-linux64/chromedriver"