import joblib
import numpy as np

from pathlib import Path

from scipy.sparse import save_npz

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from xgboost import XGBClassifier


MODEL_DIR = Path(
    "artifacts"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def train_xgboost_model(X, y):

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )
    )

    unique_classes = np.unique(y)

    num_classes = len(unique_classes)

    print(f"\nDetected Classes: {num_classes}")

    # -------------------------
    # BINARY CLASSIFICATION
    # -------------------------

    if num_classes == 2:

        model = XGBClassifier(
            objective="binary:logistic",
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42
        )

    # -------------------------
    # MULTICLASS CLASSIFICATION
    # -------------------------

    else:

        model = XGBClassifier(
            objective="multi:softmax",
            num_class=num_classes,
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="mlogloss",
            random_state=42
        )

    print("\nTraining XGBoost model...\n")

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    print("\nAccuracy Score:\n")

    print(
        accuracy_score(
            y_test,
            predictions
        )
    )

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    print("\nConfusion Matrix:\n")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    # -------------------------
    # SAVE MODEL
    # -------------------------

    joblib.dump(
        model,
        MODEL_DIR / "xgboost_model.pkl"
    )

    save_npz(
        "data/processed/X_test.npz",
        X_test
    )

    np.save(
        "data/processed/y_test.npy",
        y_test
    )

    print("\nModel saved successfully.")

    return model, X_test, y_test