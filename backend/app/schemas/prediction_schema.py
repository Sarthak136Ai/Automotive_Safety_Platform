from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class PredictionRequest(BaseModel):
    manufacturer: str = Field(..., description="The name of the vehicle manufacturer", example="Tesla")
    component: str = Field(..., description="The affected vehicle component system", example="Service Brakes")
    summary: str = Field(..., description="Details and description of the safety defect summary", example="The brake pedal may feel sticky and fail to return to resting position.")
    consequence: Optional[str] = Field(None, description="Consequence summary of the safety defect", example="A sticky brake pedal may increase stopping distances, increasing the risk of a crash.")
    remedy: Optional[str] = Field(None, description="Corrective action or remedy summary of the recall", example="Dealers will replace the brake pedal assembly free of charge.")
    model_year: int = Field(..., description="The model year of the affected vehicle", example=2021)

class ShapContributor(BaseModel):
    feature: str = Field(..., description="The feature name or word contributor")
    shap_value: float = Field(..., description="The SHAP contribution value")
    absolute_impact: float = Field(..., description="The absolute impact of this contributor")

class EntityDetails(BaseModel):
    components: List[str] = Field(default_factory=list, description="Extracted automotive component terms")
    failures: List[str] = Field(default_factory=list, description="Extracted failure modes")

class PredictionResponse(BaseModel):
    predicted_risk_tier: str = Field(..., description="Predicted risk tier: Low, Medium, High, or Critical")
    probabilities: Dict[str, float] = Field(..., description="Probability scores per risk class")
    ai_summary: str = Field(..., description="AI-generated recall headline summary")
    entities: EntityDetails = Field(..., description="SpaCy extracted entities")
    shap_explanations: List[ShapContributor] = Field(..., description="SHAP feature importance contributors for explainability")
