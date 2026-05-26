import logging
import sys
from pathlib import Path

# Add project root and backend folder to sys.path so modules can find each other correctly
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.api import predict, manufacturers, search
from backend.app.database.database import init_db, ingest_initial_data
from backend.app.core.model_loader import ModelLoader
from backend.app.core.semantic_engine import SemanticEngine

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/backend.log", mode="a", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI App
app = FastAPI(
    title="AutoSentinel AI",
    description="Explainable Automotive Recall Intelligence Platform Backend API",
    version="1.0.0"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(predict.router)
app.include_router(manufacturers.router)
app.include_router(search.router)


@app.on_event("startup")
def startup_event():
    """
    Lifespan startup trigger: Initialize schemas, load model artifacts into RAM,
    ingest initial safety recall dataset, and warm up sentence embedder.
    """
    logger.info("Starting AutoSentinel AI Backend Platform...")
    
    # 1. Initialize DB tables
    init_db()
    
    # 2. Ingest processed safety recalls from CSV
    ingest_initial_data()
    
    # 3. Warm up machine learning models in background
    logger.info("Initializing ML Model Core...")
    loader = ModelLoader()
    if loader.is_ready():
        logger.info("ML Models are fully armed and ready.")
    else:
        logger.warning("ML Models could not be loaded on startup. Ensure pipeline run completed.")

    # 4. Warm up semantic embedding engines
    logger.info("Initializing Semantic Embedder Core...")
    semantic_engine = SemanticEngine()
    if semantic_engine.encoder is not None and semantic_engine.embeddings is not None:
        logger.info("Semantic Search vector engine is fully armed and ready.")
    else:
        logger.warning("Semantic vector index could not be loaded. Precompute embeddings first.")

@app.get("/api/download/dataset")
def download_dataset():
    """
    Exposes a file download response for the processed NHTSA recall CSV dataset.
    """
    from fastapi.responses import FileResponse
    from fastapi import HTTPException
    from pathlib import Path
    
    project_dir = Path(__file__).resolve().parent.parent.parent
    
    # 1. Primary: ML Ready Processed Dataset
    csv_path = project_dir / "data/processed/ml_ready_vehicle_recalls.csv"
    if csv_path.exists():
        return FileResponse(
            path=str(csv_path),
            filename="autosentinel_safety_recalls.csv",
            media_type="text/csv"
        )
        
    # 2. Secondary: Engineered Dataset
    engineered_path = project_dir / "data/processed/engineered_vehicle_recalls.csv"
    if engineered_path.exists():
        return FileResponse(
            path=str(engineered_path),
            filename="autosentinel_safety_recalls.csv",
            media_type="text/csv"
        )
        
    # 3. Fallback: Raw dataset
    raw_path = project_dir / "data/raw/nhtsa_vehicle_safety_recall_intelligence_ultimate.csv"
    if raw_path.exists():
        return FileResponse(
            path=str(raw_path),
            filename="nhtsa_raw_safety_recalls.csv",
            media_type="text/csv"
        )
        
    raise HTTPException(status_code=404, detail="Recall dataset files not found.")

@app.get("/api/health")
def read_health():
    """
    Health check endpoint displaying system state, ML readiness, and metadata.
    """
    loader = ModelLoader()
    semantic_engine = SemanticEngine()
    
    return {
        "status": "online",
        "service": "AutoSentinel AI Backend Platform",
        "version": "1.0.0",
        "engines": {
            "ml_model_loaded": loader.is_ready(),
            "vector_search_loaded": semantic_engine.embeddings is not None
        }
    }

# Mount Static Files to serve the Single Page Application on "/" at the end to prevent routing intercept bugs
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
    logger.info(f"Static web client successfully mounted from {static_dir}")
else:
    logger.warning(f"Static directory not found at {static_dir}. Static web client is disabled.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
