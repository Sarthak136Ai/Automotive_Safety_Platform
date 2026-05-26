import os
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class SemanticEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SemanticEngine, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, artifacts_dir: str = None):
        if self._initialized:
            return
            
        # Determine artifacts folder
        if artifacts_dir is None:
            possible_dirs = ["/app/artifacts", "artifacts", "../artifacts"]
            for d in possible_dirs:
                if os.path.exists(d):
                    self.artifacts_dir = d
                    break
            else:
                self.artifacts_dir = "artifacts"
        else:
            self.artifacts_dir = artifacts_dir

        self.embeddings = None
        self.encoder = None
        self.load_engine()
        self._initialized = True

    def load_engine(self):
        logger.info("Initializing SentenceTransformer encoder (all-MiniLM-L6-v2)...")
        try:
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("SentenceTransformer encoder loaded successfully.")
            
            embeddings_path = os.path.join(self.artifacts_dir, "semantic_embeddings.npy")
            if os.path.exists(embeddings_path):
                self.embeddings = np.load(embeddings_path)
                logger.info(f"Loaded semantic embeddings matrix of shape {self.embeddings.shape} successfully.")
            else:
                logger.warning(f"Semantic embeddings not found at {embeddings_path}")
        except Exception as e:
            logger.error(f"Error loading Semantic Engine resources: {e}")

    def query_similar_recalls(self, query: str, top_k: int = 5):
        """
        Embeds a search query and calculates cosine similarity against all safety recalls.
        Returns a list of tuples containing (index, similarity_score).
        """
        if self.encoder is None or self.embeddings is None:
            logger.error("Semantic engine is not fully loaded. Cannot execute semantic search.")
            return []

        try:
            # 1. Encode query
            query_embedding = self.encoder.encode([query])
            
            # 2. Compute similarity
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # 3. Sort indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                results.append({
                    "index": int(idx),
                    "score": float(similarities[idx])
                })
                
            return results
        except Exception as e:
            logger.error(f"Failed semantic query execution: {e}")
            return []
