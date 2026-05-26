from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_PATH = (
    DATA_DIR
    / "raw"
    / "nhtsa_vehicle_safety_recall_intelligence_ultimate.csv"
)

INTERIM_DATA_PATH = (
    DATA_DIR
    / "interim"
    / "cleaned_vehicle_recalls.csv"
)

ENGINEERED_DATA_PATH = (
    DATA_DIR
    / "processed"
    / "engineered_vehicle_recalls.csv"
)

ML_READY_DATA_PATH = (
    DATA_DIR
    / "processed"
    / "ml_ready_vehicle_recalls.csv"
)

ARTIFACTS_DIR = BASE_DIR / "artifacts"

PREPROCESSING_ARTIFACTS_DIR = (
    ARTIFACTS_DIR
)

RANDOM_STATE = 42

TFIDF_MAX_FEATURES = 5000

TFIDF_NGRAM_RANGE = (1, 2)