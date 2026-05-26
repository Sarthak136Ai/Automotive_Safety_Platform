import json
import shap
import joblib
import numpy as np

from pathlib import Path


SHAP_DIR = Path(
    "artifacts"
)

SHAP_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def generate_shap_explanations(
    model,
    X_sample
):

    print("\nGenerating SHAP explanations...\n")

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(
        X_sample
    )

    joblib.dump(
        explainer,
        SHAP_DIR / "shap_explainer.pkl"
    )

    explanation_payload = []

    for i in range(min(5, X_sample.shape[0])):

        sample_explanation = {
            "sample_index": int(i),
            "predicted_risk_contributors": (
                np.abs(
                    shap_values[
                        np.argmax(
                            model.predict_proba(
                                X_sample[i]
                            )
                        )
                    ][i]
                )
                .argsort()[-10:]
                .tolist()
            )
        }

        explanation_payload.append(
            sample_explanation
        )

    with open(
        SHAP_DIR / "sample_explanations.json",
        "w"
    ) as file:

        json.dump(
            explanation_payload,
            file,
            indent=4
        )

    print(
        "\nSHAP explanations saved."
    )