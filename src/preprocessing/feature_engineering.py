from datetime import datetime


CURRENT_YEAR = datetime.now().year


COMPONENT_SEVERITY = {
    "Airbags": 5,
    "Brakes": 5,
    "Battery": 5,
    "Fuel System": 5,
    "Steering": 5,
    "Engine": 4,
    "Electrical System": 4,
    "Transmission": 3,
    "Seat Belts": 4,
    "Suspension": 2,
    "Other": 1
}


KEYWORDS = [
    "fire",
    "crash",
    "injury",
    "fatal",
    "death",
    "stall",
    "overheat",
    "shutdown",
    "loss of control"
]


def contains_keyword(text, keyword):

    return int(
        keyword in text.lower()
    )


def engineer_features(df):

    df["vehicle_age"] = (
        CURRENT_YEAR - df["model_year"]
    )

    df["summary_length"] = (
        df["summary"]
        .astype(str)
        .str.len()
    )

    df["consequence_length"] = (
        df["consequence"]
        .astype(str)
        .str.len()
    )

    df["component_severity"] = (
        df["component"]
        .map(COMPONENT_SEVERITY)
        .fillna(1)
    )

    combined_text = (
        df["summary"]
        + " "
        + df["consequence"]
    )

    for keyword in KEYWORDS:

        column_name = (
            "contains_"
            + keyword.replace(" ", "_")
        )

        df[column_name] = (
            combined_text
            .apply(
                lambda x: contains_keyword(
                    x,
                    keyword
                )
            )
        )

    manufacturer_counts = (
        df["manufacturer"]
        .value_counts()
    )

    df["manufacturer_frequency"] = (
        df["manufacturer"]
        .map(manufacturer_counts)
    )

    return df