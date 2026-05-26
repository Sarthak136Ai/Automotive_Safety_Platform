import numpy as np
import shap
import logging
from backend.app.core.model_loader import ModelLoader

logger = logging.getLogger(__name__)

def get_feature_names():
    """
    Reconstructs the combined feature list from Structured Preprocessor and TF-IDF Vectorizer.
    """
    loader = ModelLoader()
    if not loader.is_ready():
        return []

    try:
        # 1. Get categorical feature names
        cat_encoder = loader.structured_preprocessor.named_transformers_["categorical"]
        categorical_features = ["manufacturer", "component"]
        cat_names = cat_encoder.get_feature_names_out(categorical_features).tolist()
        
        # 2. Get numerical feature names
        num_names = ["vehicle_age", "summary_length", "consequence_length", "manufacturer_frequency"]
        
        # 3. Get text features
        text_names = loader.tfidf_vectorizer.get_feature_names_out().tolist()
        
        # Combined structure matches scipy hstack([struct, text])
        return cat_names + num_names + text_names
    except Exception as e:
        logger.error(f"Error reconstructing feature names: {e}")
        return []

def explain_prediction(X_input, predicted_class_index: int = 0):
    """
    Computes SHAP explanations for a single live inference input matrix.
    Returns a list of dictionaries with feature names and their corresponding SHAP values.
    """
    loader = ModelLoader()
    if not loader.is_ready():
        return []

    try:
        # Load or initialize tree explainer
        explainer = shap.TreeExplainer(loader.model)
        
        # Calculate SHAP values for the input
        # Note: XGBoost multiclass model returns SHAP values of shape [num_classes, num_features] for each input row
        # X_input is a sparse matrix, so we convert it to array for SHAP explainer
        X_dense = X_input.toarray()
        shap_values = explainer.shap_values(X_dense)
        
        # Handle shape structure for multiclass XGBoost vs binary
        # Multiclass: shap_values is a list/array of shape (classes, rows, features) or (rows, features, classes)
        # Binary: shap_values is (rows, features)
        if isinstance(shap_values, list):
            # List of arrays per class, extract for the predicted class
            cls_idx = min(predicted_class_index, len(shap_values) - 1)
            row_shap = shap_values[cls_idx][0]
        elif len(shap_values.shape) == 3:
            # Multi-dimensional array
            cls_idx = min(predicted_class_index, shap_values.shape[2] - 1)
            row_shap = shap_values[0, :, cls_idx]
        else:
            # Single class/binary classification case
            row_shap = shap_values[0]

        feature_names = get_feature_names()
        if not feature_names or len(feature_names) != len(row_shap):
            # Fallback to index mapping if there's a length mismatch
            feature_names = [f"Feature_{i}" for i in range(len(row_shap))]

        # Zip and sort feature values by absolute SHAP impact
        contributors = []
        for name, val in zip(feature_names, row_shap):
            if val != 0.0:  # Skip zero-impact features for compression
                # Clean up names for better user presentation
                clean_name = name
                if name.startswith("categorical__"):
                    clean_name = name.replace("categorical__", "").replace("_", " ").title()
                elif name.startswith("numeric__"):
                    clean_name = name.replace("numeric__", "").replace("_", " ").title()
                
                contributors.append({
                    "feature": clean_name,
                    "shap_value": float(val),
                    "absolute_impact": float(abs(val))
                })

        # Sort by absolute impact descending and return top 15 features
        contributors = sorted(contributors, key=lambda x: x["absolute_impact"], reverse=True)
        return contributors[:15]

    except Exception as e:
        logger.error(f"Failed to generate SHAP explanation: {e}")
        return []
