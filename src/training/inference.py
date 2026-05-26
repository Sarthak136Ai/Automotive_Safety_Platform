import joblib


MODEL_PATH = (
    "artifacts/models/xgboost_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_risk(X):

    prediction = model.predict(X)

    probability = (
        model.predict_proba(X)
    )

    return {
        "prediction": prediction.tolist(),
        "probabilities": probability.tolist()
    }