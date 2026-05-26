import pandas as pd

from utils.file_utils import (
    create_directories
)

from config.settings import (
    RAW_DATA_PATH,
    INTERIM_DATA_PATH,
    ENGINEERED_DATA_PATH,
    ML_READY_DATA_PATH
)

from preprocessing.clean_data import (
    clean_dataset
)

from preprocessing.text_cleaning import (
    clean_text_columns
)

from preprocessing.feature_engineering import (
    engineer_features
)

from preprocessing.risk_labeling import (
    generate_risk_labels
)

from preprocessing.preprocessing_pipeline import (
    build_preprocessing_pipeline
)

from training.train_model import (
    train_xgboost_model
)

from training.shap_explainer import (
    generate_shap_explanations
)

from nlp.entity_extraction import (
    extract_entities
)

from nlp.summarizer import (
    generate_summary_headline
)

from nlp.semantic_search import (
    semantic_search
)


def main():

    # -----------------------------------------
    # CREATE DIRECTORIES
    # -----------------------------------------

    print("\nCreating directories...")

    create_directories()

    # -----------------------------------------
    # LOAD DATASET
    # -----------------------------------------

    print("\nLoading dataset...")

    df = pd.read_csv(
        RAW_DATA_PATH,
        low_memory=False
    )

    print(f"Total raw rows: {len(df)}")
    if len(df) > 5000:
        print("Sampling 5000 rows for memory-efficient, rapid pipeline execution...")
        df = df.sample(5000, random_state=42).reset_index(drop=True)

    print("\nDataset Columns:")

    print(df.columns.tolist())

    # -----------------------------------------
    # CLEAN DATASET
    # -----------------------------------------

    print("\nCleaning dataset...")

    df = clean_dataset(df)

    # -----------------------------------------
    # CLEAN TEXT
    # -----------------------------------------

    print("\nCleaning text columns...")

    df = clean_text_columns(df)

    # -----------------------------------------
    # SAVE CLEANED DATA
    # -----------------------------------------

    df.to_csv(
        INTERIM_DATA_PATH,
        index=False
    )

    print(
        "\nCleaned dataset saved to:"
    )

    print(INTERIM_DATA_PATH)

    # -----------------------------------------
    # FEATURE ENGINEERING
    # -----------------------------------------

    print("\nEngineering features...")

    df = engineer_features(df)

    # -----------------------------------------
    # GENERATE RISK LABELS
    # -----------------------------------------

    print("\nGenerating risk labels...")

    df = generate_risk_labels(df)

    # -----------------------------------------
    # GENERATE AI SUMMARIES
    # -----------------------------------------

    print(
        "\nGenerating AI summaries..."
    )

    df["ai_summary"] = (
        df["summary"]
        .astype(str)
        .apply(generate_summary_headline)
    )

    # -----------------------------------------
    # SAVE ENGINEERED DATA
    # -----------------------------------------

    df.to_csv(
        ENGINEERED_DATA_PATH,
        index=False
    )
    df.to_csv(
        ML_READY_DATA_PATH,
        index=False
    )

    print(
        "\nEngineered and ML Ready datasets saved to:"
    )
    print(ENGINEERED_DATA_PATH)
    print(ML_READY_DATA_PATH)

    # -----------------------------------------
    # DATA VALIDATION
    # -----------------------------------------

    print("\nRisk Label Distribution:\n")

    print(
        df["risk_label"]
        .value_counts()
    )

    print("\nComponent Distribution:\n")

    print(
        df["component"]
        .value_counts()
    )

    print("\nSample Cleaned Text:\n")

    print(
        df[
            [
                "summary",
                "consequence",
                "remedy"
            ]
        ].head()
    )

    # -----------------------------------------
    # DISPLAY AI SUMMARIES
    # -----------------------------------------

    print("\nSample AI Summaries:\n")

    print(
        df[
            [
                "summary",
                "ai_summary"
            ]
        ]
        .head(5)
    )

    # -----------------------------------------
    # BUILD PREPROCESSING PIPELINE
    # -----------------------------------------

    print(
        "\nBuilding preprocessing pipeline..."
    )

    X, y = build_preprocessing_pipeline(df)

    print(
        "\nPreprocessing pipeline completed."
    )

    print("\nFeature Matrix Shape:")

    print(X.shape)

    print("\nTarget Shape:")

    print(y.shape)

    # -----------------------------------------
    # TRAIN MACHINE LEARNING MODEL
    # -----------------------------------------

    print("\nTraining ML model...")

    model, X_test, y_test = (
        train_xgboost_model(X, y)
    )

    # -----------------------------------------
    # GENERATE SHAP EXPLANATIONS
    # -----------------------------------------

    print(
        "\nGenerating SHAP explanations..."
    )

    generate_shap_explanations(
        model,
        X_test[:50]
    )

    # -----------------------------------------
    # NLP ENTITY EXTRACTION
    # -----------------------------------------

    print(
        "\nTesting NLP Entity Extraction..."
    )

    sample_text = (
        df.iloc[0]["summary"]
    )

    entities = extract_entities(
        sample_text
    )

    print("\nExtracted Entities:\n")

    print(entities)

    # -----------------------------------------
    # AI SUMMARY GENERATION TEST
    # -----------------------------------------

    print(
        "\nGenerating AI Summary..."
    )

    summary = generate_summary_headline(
        sample_text
    )

    print("\nGenerated Summary:\n")

    print(summary)

    # -----------------------------------------
    # SEMANTIC SEARCH TESTING
    # -----------------------------------------

    print(
        "\nRunning Semantic Search..."
    )

    sample_texts = (
        df["ai_summary"]
        .astype(str)
        .sample(1000, random_state=42)
        .tolist()
    )

    results = semantic_search(
        query="battery overheating",
        texts=sample_texts,
        top_k=3
    )

    print("\nTop Semantic Search Results:\n")

    for index, result in enumerate(results):

        print(
            f"\nResult {index + 1}"
        )

        print(
            "\nSimilarity Score:"
        )

        print(
            result["similarity_score"]
        )

        print(
            "\nMatched Recall:"
        )

        print(
            result["text"]
        )

    # -----------------------------------------
    # SAVE ALL SEMANTIC EMBEDDINGS & METADATA
    # -----------------------------------------
    print("\nGenerating and saving semantic embeddings for all processed records...")
    from nlp.embedding_pipeline import generate_embeddings
    import numpy as np
    import json

    # We embed the concatenated manufacturer, component, and summary to capture semantic context
    embedding_texts = (
        df["manufacturer"].astype(str) + " - " + 
        df["component"].astype(str) + " - " + 
        df["summary"].astype(str)
    ).tolist()

    embeddings = generate_embeddings(embedding_texts)
    
    np.save("artifacts/semantic_embeddings.npy", embeddings)
    print("Semantic embeddings saved successfully to artifacts/semantic_embeddings.npy")

    print("\nSaving pipeline metadata...")
    metadata = {
        "dataset_size": len(df),
        "columns": df.columns.tolist(),
        "classes": ["Low", "Medium", "High", "Critical"],
        "pipeline_completed_at": str(pd.Timestamp.now()),
        "model_type": "XGBClassifier",
        "random_state": 42
    }
    with open("artifacts/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    print("Metadata saved successfully to artifacts/metadata.json")

    # -----------------------------------------
    # FINAL COMPLETION MESSAGE
    # -----------------------------------------

    print(
        "\nPipeline execution completed successfully."
    )


if __name__ == "__main__":
    main()