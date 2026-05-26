import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.search_schema import SearchRequest, SearchResponse, SearchResultRecall
from backend.app.core.semantic_engine import SemanticEngine
from backend.app.database.database import get_db
from backend.app.database.models import Recall

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Semantic Search & Vector Retrieval"])

@router.post("/search", response_model=SearchResponse)
def semantic_search_endpoint(request: SearchRequest, db: Session = Depends(get_db)):
    """
    Executes semantic query search over the entire historical recall database.
    Generates dynamic sentence embeddings for the search query and retrieves
    matching recalls using vector similarity indices mapped to database records.
    """
    engine = SemanticEngine()
    if engine.encoder is None or engine.embeddings is None:
        raise HTTPException(
            status_code=503,
            detail="Semantic search vector index is not fully initialized. Precompute embeddings first."
        )

    try:
        logger.info(f"Received semantic search request: '{request.query}' (top_k={request.top_k})")
        
        # 1. Query vector index
        similarities = engine.query_similar_recalls(request.query, request.top_k)
        
        results = []
        for match in similarities:
            row_idx = match["index"]
            similarity_score = match["score"]
            
            # Since rows in ml_ready_vehicle_recalls.csv are inserted in-order:
            # Row index `row_idx` (0-indexed) corresponds to DB primary key `row_idx + 1`
            recall_record = db.query(Recall).filter(Recall.id == row_idx + 1).first()
            
            if recall_record:
                results.append(
                    SearchResultRecall(
                        id=recall_record.id,
                        record_id=recall_record.record_id,
                        nhtsa_record_id=recall_record.nhtsa_record_id,
                        manufacturer=recall_record.manufacturer,
                        component=recall_record.component,
                        summary=recall_record.summary,
                        consequence=recall_record.consequence or "No consequence provided",
                        remedy=recall_record.remedy or "No remedy provided",
                        model_year=recall_record.model_year,
                        risk_label=recall_record.risk_label,
                        ai_summary=recall_record.ai_summary or "General safety recall",
                        vehicle_make=recall_record.vehicle_make,
                        vehicle_model=recall_record.vehicle_model,
                        similarity_score=similarity_score
                    )
                )
            else:
                logger.warning(f"Database record mismatch. Could not find Recall ID: {row_idx + 1}")

        return SearchResponse(
            query=request.query,
            results=results
        )

    except Exception as e:
        logger.error(f"Error during semantic vector search execution: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during vector search retrieval: {str(e)}"
        )
