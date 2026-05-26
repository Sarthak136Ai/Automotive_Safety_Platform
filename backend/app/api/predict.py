import logging
from fastapi import APIRouter, HTTPException
from backend.app.schemas.prediction_schema import PredictionRequest, PredictionResponse, EntityDetails, ShapContributor
from backend.app.core.risk_engine import predict_recall_risk
from backend.app.core.shap_engine import explain_prediction
from backend.app.core.model_loader import ModelLoader

# Import existing preprocessing and NLP modules from the src folder
from src.nlp.entity_extraction import extract_entities
from src.nlp.summarizer import generate_summary_headline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Predictive Analytics"])

@router.post("/predict", response_model=PredictionResponse)
def get_prediction(request: PredictionRequest):
    """
    Execute live safety recall risk assessment.
    Runs text processing, features engineering, XGBoost prediction, SpaCy entity recognition,
    BART summary generation, and computes live SHAP explainability insights.
    """
    loader = ModelLoader()
    if not loader.is_ready():
        raise HTTPException(
            status_code=503, 
            detail="Machine learning core engines are not loaded yet. Please ensure pipeline artifacts exist."
        )

    try:
        logger.info(f"Received recall prediction request for manufacturer: {request.manufacturer}")
        
        # 1. Run core risk prediction
        pred_results = predict_recall_risk(
            manufacturer=request.manufacturer,
            component=request.component,
            summary=request.summary,
            consequence=request.consequence,
            remedy=request.remedy,
            model_year=request.model_year
        )
        
        # 2. Extract predicted class details
        predicted_tier = pred_results["predicted_risk_tier"]
        probabilities = pred_results["probabilities"]
        X_matrix = pred_results["feature_matrix"]
        
        # Find numeric index of predicted class
        classes = loader.label_encoder.classes_.tolist()
        pred_class_idx = classes.index(predicted_tier) if predicted_tier in classes else 0

        # 3. Generate live SHAP explanations
        shap_list = explain_prediction(X_matrix, pred_class_idx)
        shap_contributors = [
            ShapContributor(
                feature=item["feature"],
                shap_value=item["shap_value"],
                absolute_impact=item["absolute_impact"]
            )
            for item in shap_list
        ]

        # 4. SpaCy entity extraction
        combined_text = f"{request.summary} {request.consequence or ''}"
        entities_dict = extract_entities(combined_text)
        entities = EntityDetails(
            components=entities_dict.get("components", []),
            failures=entities_dict.get("failures", [])
        )

        # 5. Live AI Headline Summarization (runs BART with fast extractive fallback if needed)
        ai_summary = generate_summary_headline(request.summary, fast=False)

        return PredictionResponse(
            predicted_risk_tier=predicted_tier,
            probabilities=probabilities,
            ai_summary=ai_summary,
            entities=entities,
            shap_explanations=shap_contributors
        )

    except Exception as e:
        logger.error(f"Error during predictive live execution: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during machine learning analysis: {str(e)}"
        )
