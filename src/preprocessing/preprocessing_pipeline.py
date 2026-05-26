import joblib
import pandas as pd

from scipy.sparse import hstack

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
    LabelEncoder
)

from sklearn.compose import ColumnTransformer

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from config.settings import (
    TFIDF_MAX_FEATURES,
    TFIDF_NGRAM_RANGE,
    PREPROCESSING_ARTIFACTS_DIR
)


CATEGORICAL_FEATURES = [
    "manufacturer",
    "component"
]

NUMERIC_FEATURES = [
    "vehicle_age",
    "summary_length",
    "consequence_length",
    "manufacturer_frequency"
]


def build_preprocessing_pipeline(df):

    combined_text = (
        df["summary"]
        + " "
        + df["consequence"]
        + " "
        + df["remedy"]
    )

    tfidf_vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        stop_words="english"
    )

    text_features = (
        tfidf_vectorizer
        .fit_transform(combined_text)
    )

    structured_preprocessor = (
        ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    ),
                    CATEGORICAL_FEATURES
                ),
                (
                    "numeric",
                    StandardScaler(),
                    NUMERIC_FEATURES
                )
            ]
        )
    )

    structured_features = (
        structured_preprocessor
        .fit_transform(df)
    )

    X = hstack([
        structured_features,
        text_features
    ])

    label_encoder = LabelEncoder()

    y = label_encoder.fit_transform(
        df["risk_label"]
    )

    joblib.dump(
        tfidf_vectorizer,
        PREPROCESSING_ARTIFACTS_DIR
        / "tfidf_vectorizer.pkl"
    )

    joblib.dump(
        structured_preprocessor,
        PREPROCESSING_ARTIFACTS_DIR
        / "structured_preprocessor.pkl"
    )

    joblib.dump(
        label_encoder,
        PREPROCESSING_ARTIFACTS_DIR
        / "label_encoder.pkl"
    )

    return X, y