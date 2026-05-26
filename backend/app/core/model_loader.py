import os
import joblib
import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelLoader, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, artifacts_dir: str = None):
        if self._initialized:
            return
            
        # Standardize directories to look for artifacts
        if artifacts_dir is None:
            # Check docker vs local path
            possible_dirs = [
                "/app/artifacts",
                "artifacts",
                "../artifacts"
            ]
            for d in possible_dirs:
                if os.path.exists(d):
                    self.artifacts_dir = d
                    break
            else:
                self.artifacts_dir = "artifacts"
        else:
            self.artifacts_dir = artifacts_dir

        self.model = None
        self.label_encoder = None
        self.tfidf_vectorizer = None
        self.structured_preprocessor = None
        
        self.load_artifacts()
        self._initialized = True

    def load_artifacts(self):
        logger.info(f"Loading ML artifacts from {self.artifacts_dir}...")
        
        model_path = os.path.join(self.artifacts_dir, "xgboost_model.pkl")
        le_path = os.path.join(self.artifacts_dir, "label_encoder.pkl")
        tfidf_path = os.path.join(self.artifacts_dir, "tfidf_vectorizer.pkl")
        preprocessor_path = os.path.join(self.artifacts_dir, "structured_preprocessor.pkl")

        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("XGBoost model loaded successfully.")
            else:
                logger.warning(f"XGBoost model not found at {model_path}")

            if os.path.exists(le_path):
                self.label_encoder = joblib.load(le_path)
                logger.info("Label encoder loaded successfully.")
            else:
                logger.warning(f"Label encoder not found at {le_path}")

            if os.path.exists(tfidf_path):
                self.tfidf_vectorizer = joblib.load(tfidf_path)
                logger.info("TF-IDF Vectorizer loaded successfully.")
            else:
                logger.warning(f"TF-IDF Vectorizer not found at {tfidf_path}")

            if os.path.exists(preprocessor_path):
                self.structured_preprocessor = joblib.load(preprocessor_path)
                logger.info("Structured preprocessor loaded successfully.")
            else:
                logger.warning(f"Structured preprocessor not found at {preprocessor_path}")

        except Exception as e:
            logger.error(f"Error loading ML artifacts: {e}")

    def is_ready(self) -> bool:
        return all([
            self.model is not None,
            self.label_encoder is not None,
            self.tfidf_vectorizer is not None,
            self.structured_preprocessor is not None
        ])
