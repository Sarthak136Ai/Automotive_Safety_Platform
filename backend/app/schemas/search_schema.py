from pydantic import BaseModel, Field
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str = Field(..., description="The semantic search query concern", example="brakes locking up")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of top similar recall results to retrieve")

class SearchResultRecall(BaseModel):
    id: int
    record_id: str
    nhtsa_record_id: Optional[str]
    manufacturer: str
    component: str
    summary: str
    consequence: str
    remedy: str
    model_year: int
    risk_label: str
    ai_summary: str
    vehicle_make: Optional[str]
    vehicle_model: Optional[str]
    similarity_score: float = Field(..., description="Cosine similarity score between query and record")

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultRecall]
