import pandas as pd


VALID_LABELS = [
    "Low",
    "Medium",
    "High",
    "Critical"
]


def generate_risk_labels(df):

    df["risk_label"] = (
        df["risk_tier"]
        .astype(str)
        .str.title()
        .replace({"Moderate": "Medium"})
    )

    df = df[
        df["risk_label"]
        .isin(VALID_LABELS)
    ]

    return df