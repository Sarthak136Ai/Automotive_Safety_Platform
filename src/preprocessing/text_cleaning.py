import re
import pandas as pd


TEXT_COLUMNS = [
    "summary",
    "consequence",
    "remedy"
]


def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    text = text.lower()

    text = re.sub(r"<.*?>", " ", text)

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_text_columns(df):

    for column in TEXT_COLUMNS:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype(str)
                .apply(clean_text)
            )

    return df